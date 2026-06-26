#!/usr/bin/env python3
# Copyright 2026 Eluu Labs — Apache-2.0 (see ../LICENSE)
"""
layout_check — an automated layout-quality gate for generated decks.

Reads the per-element geometry that the build emits (*.layout.json, written by
pptx_deck.save(layout_dir=...)) and flags the defects an eyeball pass misses:

  - text overlapping other text
  - text that starts inside a filled container but overflows it
  - a filled container whose text has too little bottom padding
  - a text box too short for its line count at its font size
  - kicker marker/label pairs whose centres don't line up
  - any element outside the slide bounds

Each layout element is {order, kind, bbox:[x,y,w,h], name?, text?,
resolvedFontSize?, textLayout:{lineCount}?, fillColor?}. Errors block; warnings
are advisory (tight display leading and intentional label/value groupings are
expected warnings — confirm with a render).

Usage: python layout_check.py <layout-dir> [--warn-only]
Exit code 2 on errors (unless --warn-only).
"""
import sys, os, glob, json, math, re

MIN_GAP=16; MAX_TT_OVERLAP=10  # px^2

def bbox(e):
    b=e.get("bbox")
    if not b or len(b)!=4: return None
    x,y,w,h=[float(v) for v in b]
    return {"x":x,"y":y,"w":w,"h":h,"x2":x+w,"y2":y+h}
def area(b): return max(0,b["w"])*max(0,b["h"])
def inter(a,b):
    x=max(a["x"],b["x"]); y=max(a["y"],b["y"]); x2=min(a["x2"],b["x2"]); y2=min(a["y2"],b["y2"])
    return {"x":x,"y":y,"w":max(0,x2-x),"h":max(0,y2-y),"x2":x2,"y2":y2}
def has_text(e): return bool(e.get("text"))
def lbl(e): return e.get("name") or (e.get("text") or "")[:40] or f'{e.get("kind")}#{e.get("order")}'
def est_height(e):
    lc=(e.get("textLayout") or {}).get("lineCount") or 1
    fs=float(e.get("resolvedFontSize") or 0)
    if fs<=0 or lc<=0: return None
    return lc,fs,fs*lc*1.15
def contains(c,ch): return ch["x"]>=c["x"] and ch["y"]>=c["y"] and ch["x2"]<=c["x2"] and ch["y2"]<=c["y2"]
def starts_inside(c,ch): return c["x"]<=ch["x"]<c["x2"] and c["y"]<=ch["y"]<c["y2"]
def usable_container(shape,box,tbox,slidebox):
    return (area(box)>area(tbox)*1.15 and box["h"]>=40 and area(box)<area(slidebox)*0.8
            and box["w"]>=max(120,tbox["w"]*1.15)
            and shape.get("fillColor") and shape["fillColor"]!="rgba(0, 0, 0, 0)")
def gap(a,b):
    dx=max(0,max(a["x"],b["x"])-min(a["x2"],b["x2"])); dy=max(0,max(a["y"],b["y"])-min(a["y2"],b["y2"]))
    if dx==0 and dy==0: return 0
    if dx==0: return dy
    if dy==0: return dx
    return math.hypot(dx,dy)
def in_slide(b,s,tol=1):
    return b["x"]>=s["x"]-tol and b["y"]>=s["y"]-tol and b["x2"]<=s["x2"]+tol and b["y2"]<=s["y2"]+tol

def check(path):
    data=json.load(open(path)); base=os.path.basename(path)
    fr=data["slide"]["frame"]; slidebox={"x":0,"y":0,"w":fr["width"],"h":fr["height"],"x2":fr["width"],"y2":fr["height"]}
    els=[e for e in data.get("elements",[]) if bbox(e)]
    texts=[e for e in els if has_text(e)]
    shapes=[e for e in els if e.get("kind")=="shape" and not has_text(e)]
    major=[e for e in els if area(bbox(e))>1200 and e.get("kind")!="shape"]
    P=[]
    def add(sev,idc,msg): P.append((sev,f"{base}:{idc}",msg))
    for e in els:
        if not in_slide(bbox(e),slidebox): add("error",f"bounds:{e['order']}",f"{lbl(e)} extends outside slide bounds.")
    for i in range(len(texts)):
        for j in range(i+1,len(texts)):
            ov=area(inter(bbox(texts[i]),bbox(texts[j])))
            if ov>MAX_TT_OVERLAP:
                add("error",f"text-text:{texts[i]['order']}:{texts[j]['order']}",
                    f"{lbl(texts[i])} overlaps {lbl(texts[j])} by {round(ov)}px.")
    for t in texts:
        est=est_height(t)
        if est and bbox(t)["h"]<est[2]:
            add("warning",f"tight-text:{t['order']}",f"{lbl(t)} box tight: {round(bbox(t)['h'])}px for {est[0]} line(s) @ {est[1]}px.")
    for t in texts:
        tb=bbox(t); est=est_height(t)
        if not est: continue
        cands=sorted([(s,bbox(s)) for s in shapes if contains(bbox(s),tb) and usable_container(s,bbox(s),tb,slidebox)],key=lambda c:area(c[1]))
        if not cands: continue
        sh,box=cands[0]; bottom=box["y2"]-tb["y2"]; need=16 if est[0]>1 else 12
        if bottom<need:
            inside=sum(1 for x in texts if starts_inside(box,bbox(x)))
            add("error" if inside>=3 else "warning",f"box-bottom-pad:{sh['order']}:{t['order']}",
                f"{lbl(t)} has {round(bottom)}px bottom padding in its box; need >= {need}px.")
    for t in texts:
        tb=bbox(t)
        cands=sorted([(s,bbox(s)) for s in shapes if starts_inside(bbox(s),tb) and usable_container(s,bbox(s),tb,slidebox) and not contains(bbox(s),tb)],key=lambda c:area(c[1]))
        if not cands: continue
        sh,box=cands[0]; ob=max(0,tb["y2"]-box["y2"]); orr=max(0,tb["x2"]-box["x2"])
        desc=" and ".join([f"{round(orr)}px right" for _ in [1] if orr>0]+[f"{round(ob)}px bottom" for _ in [1] if ob>0])
        add("error",f"box-overflow:{sh['order']}:{t['order']}",f"{lbl(t)} starts inside a box but overflows by {desc}.")
    for i in range(len(major)):
        for j in range(i+1,len(major)):
            d=gap(bbox(major[i]),bbox(major[j]))
            if 0<d<MIN_GAP: add("warning",f"gutter:{major[i]['order']}:{major[j]['order']}",f"{lbl(major[i])} only {round(d)}px from {lbl(major[j])}.")
    pairs={}
    for e in els:
        m=re.match(r"^(kicker(?:-[A-Za-z0-9]+)?)-(marker|label)$",e.get("name") or "")
        if m: pairs.setdefault(m.group(1),{})[m.group(2)]=e
    for k,pr in pairs.items():
        if not pr.get("marker") or not pr.get("label"):
            add("warning",f"kicker-pair:{k}",f"{k} missing marker/label pair."); continue
        mb=bbox(pr["marker"]); lb=bbox(pr["label"])
        d=abs((mb["y"]+mb["h"]/2)-(lb["y"]+lb["h"]/2))
        if d>1: add("error",f"kicker-centerline:{k}",f"{k} marker/label centres differ by {d:.1f}px; need <= 1px.")
    return P

def main():
    args=[a for a in sys.argv[1:] if not a.startswith("--")]
    warn_only="--warn-only" in sys.argv
    layouts=sorted(glob.glob(os.path.join(args[0],"*.layout.json"))) if args else []
    if not layouts: print("no layout files found"); sys.exit(1)
    allp=[p for lp in layouts for p in check(lp)]
    for sev,idc,msg in allp: print(f"[{sev}] {idc}: {msg}")
    errs=[p for p in allp if p[0]=="error"]; warns=[p for p in allp if p[0]=="warning"]
    print(f"Checked {len(layouts)} layout(s): {len(errs)} error(s), {len(warns)} warning(s).")
    if errs and not warn_only: sys.exit(2)

if __name__=="__main__": main()
