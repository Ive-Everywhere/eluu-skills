#!/usr/bin/env python3
# Copyright 2026 Eluu Labs — Apache-2.0 (see ../LICENSE)
"""
chart_kit — clean, finance-grade matplotlib charts for decks.

House style: white background, no top/right spines, hairline y-grid, direct
value labels, one accent colour, optional brand font. Charts carry NO title —
the slide's action title states the conclusion; the chart is the proof object.

For the PowerPoint path, save PNGs locally and place them with
pptx_deck / the Slides image helper.

For the NATIVE GOOGLE SLIDES path, Slides' createImage needs a PUBLIC URL it can
fetch at insert time. The lightweight pattern: deploy a tiny app that GENERATES
the PNGs server-side on startup and serves them statically, e.g.

    # server.py
    import http.server, socketserver, os, chart_kit
    for fn in chart_kit.ALL: fn()          # render PNGs into ./charts
    os.chdir(os.path.dirname(__file__))
    socketserver.TCPServer(("", int(os.environ.get("PORT","8000"))),
                           http.server.SimpleHTTPRequestHandler).serve_forever()

Then reference https://<host>/charts/<name>.png from createImage. Warm the host
(HTTP GET each URL) right before inserting images so the fetch doesn't cold-start.
Only small source + data travels to the host; charts render there.
"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter

OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(OUT, exist_ok=True)

INK="#0E1A2B"; ACCENT="#2563EB"; GOOD="#16A34A"; BAD="#DC2626"
SLATE="#64748B"; GRID="#E9EDF3"; PANEL="#E7ECF3"

# Optional: register a brand font (point FONT_TTF at a .ttf to match the deck).
FONT_FAMILY="DejaVu Sans"
FONT_TTF=os.environ.get("CHART_FONT_TTF")
if FONT_TTF and os.path.exists(FONT_TTF):
    try: fm.fontManager.addfont(FONT_TTF); FONT_FAMILY=fm.FontProperties(fname=FONT_TTF).get_name()
    except Exception: pass
plt.rcParams.update({"font.family":FONT_FAMILY,"font.size":13,"axes.edgecolor":"#C7D0DC",
    "axes.linewidth":1.0,"figure.dpi":200})

def base(w=7.4,h=3.9):
    fig,ax=plt.subplots(figsize=(w,h)); fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.tick_params(length=0,colors=SLATE); ax.grid(axis="y",color=GRID,lw=1,zorder=0); ax.set_axisbelow(True)
    return fig,ax
def save(fig,name):
    fig.tight_layout(pad=0.7)
    fig.savefig(os.path.join(OUT,name),facecolor="white",bbox_inches="tight",pad_inches=0.12)
    plt.close(fig)

def bar(labels,values,name,unit="",accent_last=True,fmt="{:.0f}"):
    fig,ax=base()
    bars=ax.bar(labels,values,color=ACCENT,width=0.62,zorder=3)
    if accent_last: bars[-1].set_color(INK)
    top=max(values)
    for x,v in zip(labels,values):
        ax.text(x,v+top*0.02,(fmt.format(v))+unit,ha="center",va="bottom",fontsize=12,color=INK,fontweight="bold")
    ax.set_ylim(0,top*1.16)
    if unit: ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f"{int(v)}{unit}"))
    save(fig,name)

def line(labels,values,name,unit="",fmt="{:.0f}",label_ends=True):
    fig,ax=base()
    ax.plot(labels,values,color=INK,lw=2.6,marker="o",ms=6,mfc=ACCENT,mec="white",zorder=3)
    top=max(values)
    if label_ends:
        for i in (0,len(values)-1):
            ax.text(labels[i],values[i]+top*0.04,(fmt.format(values[i]))+unit,ha="center",fontsize=12,color=INK,fontweight="bold")
    ax.set_ylim(0,top*1.18)
    if unit: ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f"{int(v)}{unit}"))
    save(fig,name)

# Charts to render when run as a server bootstrap. Replace with your real data.
def _demo_bar():  bar(["Q1","Q2","Q3","Q4"],[3.2,6.5,12.1,24.2],"demo_bar.png",unit="M",fmt="${:.1f}")
def _demo_line(): line(["Q1","Q2","Q3","Q4"],[18,27,38,55],"demo_line.png",unit="k",fmt="${:.0f}")
ALL=[_demo_bar,_demo_line]

if __name__=="__main__":
    for f in ALL: f()
    print("charts ->", sorted(os.listdir(OUT)))
