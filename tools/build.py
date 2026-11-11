# -*- coding: utf-8 -*-
import re, sys, os, html
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__))
from content import CAROUSELS, HANDLE

OUT = sys.argv[1]
only = sys.argv[2:] 
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
CREAM, BROWN, CORAL, GOLD = "#FEFAEE", "#3C3026", "#E65356", "#C99C58"

def ltr(s):
    s = html.escape(s)
    return re.sub(r'([A-Za-z@][A-Za-z0-9@._\-]*(?: [A-Za-z][A-Za-z0-9\-]*)*)', r'<span dir="ltr">\1</span>', s)

CSS = f"""
@font-face{{font-family:V;font-weight:400;src:url('file://{FONTS}/vazirmatn-arabic-400-normal.woff2');unicode-range:U+0600-06FF,U+200C-200E,U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE80-FEFC}}
@font-face{{font-family:V;font-weight:700;src:url('file://{FONTS}/vazirmatn-arabic-700-normal.woff2');unicode-range:U+0600-06FF,U+200C-200E,U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE80-FEFC}}
@font-face{{font-family:V;font-weight:900;src:url('file://{FONTS}/vazirmatn-arabic-900-normal.woff2');unicode-range:U+0600-06FF,U+200C-200E,U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE80-FEFC}}
@font-face{{font-family:V;font-weight:400;src:url('file://{FONTS}/vazirmatn-latin-400-normal.woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}
@font-face{{font-family:V;font-weight:700;src:url('file://{FONTS}/vazirmatn-latin-700-normal.woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}
@font-face{{font-family:V;font-weight:900;src:url('file://{FONTS}/vazirmatn-latin-700-normal.woff2');unicode-range:U+0000-00FF}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px}}
body{{font-family:V,sans-serif;direction:rtl;position:relative;overflow:hidden}}
.slide{{width:1080px;height:1350px;position:relative;padding:110px 100px 150px}}
.cream{{background:{CREAM};color:{BROWN}}}
.coral{{background:{CORAL};color:{CREAM}}}
.brown{{background:{BROWN};color:{CREAM}}}
.foot{{position:absolute;left:100px;right:100px;bottom:70px;display:flex;justify-content:space-between;align-items:center;font-size:30px;direction:rtl}}
.foot .h{{font-weight:700;letter-spacing:.5px}}
.foot .pg{{opacity:.8}}
.rule{{width:140px;height:8px;background:{GOLD};border-radius:4px;margin:0 0 50px 0}}
.pill{{display:inline-block;border:3px solid {GOLD};color:{GOLD};border-radius:40px;padding:8px 34px;font-size:32px;font-weight:700}}
.coral .pill{{border-color:{CREAM};color:{CREAM}}}
.cover{{display:flex;flex-direction:column;justify-content:center;height:100%}}
.cover h1{{font-size:112px;line-height:1.35;font-weight:900;margin:40px 0 36px}}
.cover .sub{{font-size:46px;line-height:1.7;font-weight:400;opacity:.95}}
.cover .sw{{margin-top:60px;font-size:34px;font-weight:700}}
h2{{font-size:78px;line-height:1.4;font-weight:900;color:{CORAL};margin-bottom:46px}}
p.body{{font-size:54px;line-height:1.85;font-weight:400}}
ul{{list-style:none}}
li{{font-size:50px;line-height:1.7;font-weight:400;padding-right:60px;position:relative;margin-bottom:34px}}
li:before{{content:"";position:absolute;right:0;top:30px;width:26px;height:26px;border-radius:50%;background:{GOLD}}}
.num{{width:150px;height:150px;border-radius:50%;background:{CORAL};color:{CREAM};font-size:92px;font-weight:900;display:flex;align-items:center;justify-content:center;margin-bottom:50px;line-height:1}}
.vcenter{{display:flex;flex-direction:column;justify-content:center;height:100%;margin-top:-30px}}
.box{{border-radius:36px;padding:54px 56px;font-size:50px;line-height:1.8}}
.bad{{background:#F4E3DA;border:4px solid {CORAL}}}
.good{{background:#F6EBCF;border:4px solid {GOLD}}}
.tag{{font-size:34px;font-weight:700;margin-bottom:14px}}
.bad .tag{{color:{CORAL}}} .good .tag{{color:#8A6320}}
.note{{font-size:32px;opacity:.7;margin-top:36px}}
.cta h2{{color:{GOLD}}}
.cta p.body{{color:{CREAM}}}
.cta .tg{{margin-top:60px;display:inline-block;background:{CORAL};color:{CREAM};border-radius:60px;padding:18px 54px;font-size:46px;font-weight:700}}
"""

def foot(i, n, dark=False):
    return f'<div class="foot"><span class="h">{ltr(HANDLE)}</span><span class="pg">{i} / {n}</span></div>'.replace("0","۰").replace("1","۱").replace("2","۲").replace("3","۳").replace("4","۴").replace("5","۵").replace("6","۶").replace("7","۷").replace("8","۸").replace("9","۹") if False else f'<div class="foot"><span class="h">{ltr(HANDLE)}</span><span class="pg">{fa(i)} / {fa(n)}</span></div>'

def fa(n):
    return str(n).translate(str.maketrans("0123456789","۰۱۲۳۴۵۶۷۸۹"))

def render(slide, i, n, label):
    t = slide["t"]
    if t == "cover":
        body = f'<div class="slide coral"><div class="cover"><div><span class="pill">{ltr(label)}</span></div><h1>{ltr(slide["title"])}</h1><div class="rule" style="background:{CREAM}"></div><div class="sub">{ltr(slide["sub"])}</div><div class="sw">ورق بزنید ←</div></div>{foot(i,n)}</div>'
    elif t == "step":
        body = f'<div class="slide cream"><div class="vcenter"><div class="num">{slide["num"]}</div><h2>{ltr(slide["title"])}</h2><p class="body">{ltr(slide["body"])}</p></div>{foot(i,n)}</div>'
    elif t == "plain":
        inner = f'<h2>{ltr(slide["title"])}</h2><div class="rule"></div>'
        if "body" in slide: inner += f'<p class="body">{ltr(slide["body"])}</p>'
        else: inner += "<ul>" + "".join(f"<li>{ltr(b)}</li>" for b in slide["bullets"]) + "</ul>"
        body = f'<div class="slide cream"><div class="vcenter">{inner}</div>{foot(i,n)}</div>'
    elif t == "compare":
        note = slide.get("note","")
        nt = f'<div class="note">{ltr(note)}</div>' if note and not note.isdigit() and not re.match(r'^[۰-۹]+$', note) else ""
        head = f'<div class="num" style="width:110px;height:110px;font-size:64px;margin-bottom:40px">{note}</div>' if note and re.match(r'^[۰-۹]+$', note) else ""
        body = f'<div class="slide cream"><div class="vcenter">{head}<div class="box bad"><div class="tag">✗ به‌جای این</div>{ltr(slide["bad"])}</div><div style="height:36px"></div><div class="box good"><div class="tag">✓ این را بنویسید</div>{ltr(slide["good"])}</div>{nt}</div>{foot(i,n)}</div>'
    elif t == "cta":
        body = f'<div class="slide brown cta"><div class="vcenter"><h2>{ltr(slide["title"])}</h2><div class="rule"></div><p class="body">{ltr(slide["body"])}</p></div>{foot(i,n)}</div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox","--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width":1080,"height":1350})
    for key, c in CAROUSELS.items():
        if only and key not in only: continue
        d = os.path.join(OUT, key); os.makedirs(d, exist_ok=True)
        n = len(c["slides"])
        for i, s in enumerate(c["slides"], 1):
            fp = f"/tmp/slide_{key}_{i}.html"
            open(fp, "w", encoding="utf-8").write(render(s, i, n, c["label"]))
            pg.goto("file://" + fp); pg.wait_for_timeout(250)
            pg.screenshot(path=os.path.join(d, f"{i:02d}.png"))
        print(key, n, "slides")
    b.close()
