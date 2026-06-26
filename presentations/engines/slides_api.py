#!/usr/bin/env python3
# Copyright 2026 Eluu Labs — Apache-2.0 (see ../LICENSE)
"""
slides_api — build Google Slides `batchUpdate` request payloads for a native deck.

The Google Slides API has only a few verbs (create / batchUpdate / get /
getThumbnail), but batchUpdate is enough to assemble a premium deck from native
text boxes, shapes, tables, and images. This module emits the request dicts so
you can author a deck the same way pptx_deck builds a .pptx — measured text on a
grid — then POST them through whatever Slides client you have.

Canvas: a default 16:9 Slides page is 720 x 405 pt (9144000 x 5143500 EMU).
Work in pt; helpers convert to EMU (1pt = 12700).

WORKFLOW (the ordering matters):
  1. presentations.create(title)  -> grab presentationId (the response is huge;
     extract just the id).
  2. batchUpdate: delete the default slide, createSlide(BLANK) x N, set any dark
     page backgrounds.  (see `setup_requests`)
  3. batchUpdate the TEXT/SHAPE requests, in chunks per slide-group. These never
     touch the network, so they always succeed.
  4. WARM your chart host (HTTP GET every image URL), THEN batchUpdate the IMAGE
     requests. createImage fetches the URL at insert time; if the host cold-starts
     the fetch can time out and roll back the whole atomic batch. Once inserted,
     Slides stores a copy in the deck (it becomes self-contained).
  5. QA each page with presentations.pages.getThumbnail and inspect the PNG.

GOTCHAS:
  - objectId must be >= 5 chars. Use ids like "slide1", "txt0001", "rec0001".
  - batchUpdate is atomic: one bad request rolls back the whole batch. Chunk by
    slide group and isolate images from text.
  - Typeset only in real Google Fonts names (Slides ignores embedded fonts).
"""
EMU=12700
def E(pt): return int(round(pt*EMU))
def rgb(h):
    h=h.lstrip("#"); return {"red":int(h[0:2],16)/255,"green":int(h[2:4],16)/255,"blue":int(h[4:6],16)/255}

_n=[0]
def oid(p="elem"):
    _n[0]+=1; return f"{p}{_n[0]:04d}"

def setup_requests(slide_ids, dark_ids=(), default_slide="p", ink_hex="#0E1A2B"):
    """Delete the default slide, create N blank slides, set dark backgrounds."""
    reqs=[{"deleteObject":{"objectId":default_slide}}]
    for sid in slide_ids:
        reqs.append({"createSlide":{"objectId":sid,"slideLayoutReference":{"predefinedLayout":"BLANK"}}})
    for sid in dark_ids:
        reqs.append({"updatePageProperties":{"objectId":sid,"fields":"pageBackgroundFill.solidFill.color",
            "pageProperties":{"pageBackgroundFill":{"solidFill":{"color":{"rgbColor":rgb(ink_hex)}}}}}})
    return reqs

def image(sid,url,x,y,w,h,oid_=None):
    return [{"createImage":{"objectId":oid_ or oid("img"),"url":url,
        "elementProperties":{"pageObjectId":sid,
        "size":{"width":{"magnitude":E(w),"unit":"EMU"},"height":{"magnitude":E(h),"unit":"EMU"}},
        "transform":{"scaleX":1,"scaleY":1,"translateX":E(x),"translateY":E(y),"unit":"EMU"}}}}]

def rect(sid,x,y,w,h,fill_hex):
    o=oid("rec")
    return [{"createShape":{"objectId":o,"shapeType":"RECTANGLE","elementProperties":{"pageObjectId":sid,
        "size":{"width":{"magnitude":E(w),"unit":"EMU"},"height":{"magnitude":E(h),"unit":"EMU"}},
        "transform":{"scaleX":1,"scaleY":1,"translateX":E(x),"translateY":E(y),"unit":"EMU"}}}},
        {"updateShapeProperties":{"objectId":o,"fields":"shapeBackgroundFill.solidFill.color,outline.outlineFill.solidFill.color,outline.weight",
         "shapeProperties":{"shapeBackgroundFill":{"solidFill":{"color":{"rgbColor":rgb(fill_hex)}}},
         "outline":{"outlineFill":{"solidFill":{"color":{"rgbColor":rgb(fill_hex)}}},"weight":{"magnitude":3175,"unit":"EMU"}}}}}]

def text(sid,x,y,w,h,runs,align="START",valign="TOP"):
    """runs: list of (string, google_font_name, size_pt, hex, bold). Per-run styling by range."""
    o=oid("txt"); full="".join(r[0] for r in runs)
    reqs=[{"createShape":{"objectId":o,"shapeType":"TEXT_BOX","elementProperties":{"pageObjectId":sid,
        "size":{"width":{"magnitude":E(w),"unit":"EMU"},"height":{"magnitude":E(h),"unit":"EMU"}},
        "transform":{"scaleX":1,"scaleY":1,"translateX":E(x),"translateY":E(y),"unit":"EMU"}}}},
        {"insertText":{"objectId":o,"text":full}}]
    if valign!="TOP":
        reqs.append({"updateShapeProperties":{"objectId":o,"fields":"contentAlignment","shapeProperties":{"contentAlignment":valign}}})
    if align!="START":
        reqs.append({"updateParagraphStyle":{"objectId":o,"fields":"alignment","style":{"alignment":align},"textRange":{"type":"ALL"}}})
    i=0
    for s,font,size,hexc,bold in runs:
        j=i+len(s)
        reqs.append({"updateTextStyle":{"objectId":o,"fields":"fontFamily,fontSize,bold,foregroundColor",
            "style":{"fontFamily":font,"fontSize":{"magnitude":size,"unit":"PT"},"bold":bold,
            "foregroundColor":{"opaqueColor":{"rgbColor":rgb(hexc)}}},
            "textRange":{"type":"FIXED_RANGE","startIndex":i,"endIndex":j}}})
        i=j
    return reqs

# Example grammar: a kicker + action title + rule + footer for a content slide.
def kicker(sid,txt,accent="#2563EB",x=36,y=22):
    return rect(sid,x,y+4,7,7,accent)+text(sid,x+12,y,500,16,[(txt,"Roboto",8.5,accent,True)],valign="MIDDLE")
def title(sid,txt,ink="#0E1A2B",x=36,y=38,w=648,font="Montserrat",size=15.5):
    return text(sid,x,y,w,40,[(txt,font,size,ink,True)])
def rule(sid,color="#D6DEE9",x=36,y=74,w=648):
    return rect(sid,x,y,w,0.8,color)
def footer(sid,num,total,brand="ELUU  ·  ILLUSTRATIVE",col="#64748B"):
    return (text(sid,36,392,420,12,[(brand,"Roboto",7,col,False)],valign="MIDDLE")
            +text(sid,604,392,80,12,[(f"{num:02d} / {total:02d}","Roboto",7,col,False)],align="END",valign="MIDDLE"))

if __name__=="__main__":
    import json
    sid="slide3"
    reqs=(kicker(sid,"GROWTH")+title(sid,"ARR compounded 2.7x year over year.")+rule(sid)
          +image(sid,"https://example.tryeluu.com/charts/arr.png",90,88,540,284)
          +footer(sid,3,11))
    print(json.dumps({"requests":reqs},indent=1)[:1200],"...")
