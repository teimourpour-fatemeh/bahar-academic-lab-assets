# -*- coding: utf-8 -*-
"""Faceless text reels (1080x1920, silent). Usage: python3 -I tools/reels.py <out_dir> [key ...]"""
import os, sys, re, html, subprocess
from playwright.sync_api import sync_playwright

HANDLE = "@bahar.academy.lab"
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
CREAM, BROWN, CORAL, GOLD = "#FEFAEE", "#3C3026", "#E65356", "#C99C58"
SEC = 3.6  # seconds per scene (hook scene 3.0)

REELS = {
 "reel-01-stuck": {"label": "همراه پژوهشی شما", "scenes": [
   ("hook", "وسط پایان‌نامه گیر کرده‌ای؟"),
   ("pt", "بیشتر گیرها از نوشتن شروع نمی‌شود"),
   ("pt", "از سؤالی شروع می‌شود که هنوز شفاف نیست"),
   ("pt", "پروپوزال، پایان‌نامه، مقاله، تحلیل داده، SOP و CV: قدم‌به‌قدم همراهی می‌کنیم"),
   ("cta", "زیر همین پست بنویس: کدام فصل؟"),
 ], "caption": "گیر کردن وسط پایان‌نامه؛ از کجا شروع می‌شود؟\n\nبیشتر گیرها مشکل نوشتن نیستند و از سؤالی شروع می‌شوند که هنوز شفاف نیست. اگر الان روی یک فصل گیر کرده‌اید، زیر همین پست بنویسید کدام فصل.\n\n#بهار_آکادمیک_لب #پایان_نامه #پروپوزال #کارشناسی_ارشد #دکتری #دانشجویان_ایرانی"},
 "reel-02-proposal": {"label": "اشتباهات رایج", "scenes": [
   ("hook", "پروپوزالت برگشت خورد؟ احتمالاً یکی از این سه‌تاست"),
   ("pt", "۱. بیان مسئله، مسئله را نمی‌گوید؛ فقط موضوع را توضیح می‌دهد"),
   ("pt", "۲. هدف‌ها با روش تحقیق جور نیستند"),
   ("pt", "۳. شکاف پژوهشی خالی است؛ نگفته‌ای چرا این کار باید الان انجام شود"),
   ("cta", "ذخیره کن و برای همکلاسی‌ات بفرست"),
 ], "caption": "۳ دلیل رایج برگشت خوردن پروپوزال ارشد\n\nبیان مسئله‌ای که فقط موضوع را توضیح می‌دهد، هدف‌هایی که با روش تحقیق نمی‌خوانند، و شکاف پژوهشی که روشن نیست. این ریل را ذخیره کنید و پروپوزال‌تان را با آن بسنجید.\n\n#بهار_آکادمیک_لب #پروپوزال #پایان_نامه #بیان_مسئله #کارشناسی_ارشد #دانشجویان_ایرانی"},
 "reel-03-sources": {"label": "اسطوره‌ها", "scenes": [
   ("hook", "۱۵۰ تا منبع آوردی؟ شاید مشکل همین است"),
   ("pt", "مرور منابع قرار نیست همه‌چیز را بگوید"),
   ("pt", "باید نشان بدهد دیگران به کجا رسیده‌اند و کجا گیر کرده‌اند"),
   ("pt", "به‌جای خلاصه مقاله‌ها پشت سر هم، منابع را بر اساس سؤال دسته‌بندی کن"),
   ("cta", "این را برای همکلاسی‌ای بفرست که فصل ۲ می‌نویسد"),
 ], "caption": "منابع بیشتر یعنی پایان‌نامه بهتر؟ نه لزوماً\n\nمرور منابع خوب منابع را بر اساس سؤال دسته‌بندی می‌کند و شکاف پژوهش را نشان می‌دهد. این ریل را برای همکلاسی‌تان بفرستید.\n\n#بهار_آکادمیک_لب #مرور_منابع #پایان_نامه #مقاله_نویسی #کارشناسی_ارشد #دکتری #دانشجویان_ایرانی"},
 "reel-04-question": {"label": "پشت صحنه مشاوره", "scenes": [
   ("hook", "اولین سؤالی که از هر دانشجو می‌پرسم"),
   ("pt", "می‌توانی در یک جمله بگویی به چه سؤالی جواب می‌دهی؟"),
   ("pt", "اگر نه، مشکل نوشتنت نیست؛ سؤالت هنوز شفاف نیست"),
   ("pt", "بیشتر گیرها از همین‌جا شروع می‌شود"),
   ("cta", "سؤالت را بفرست؛ در مشاوره اولیه رایگان شفافش می‌کنیم. لینک در بیو"),
 ], "caption": "اولین سؤالی که در مشاوره می‌پرسم\n\nاگر نمی‌توانید سؤال پژوهش‌تان را در یک جمله بگویید، هنوز وقت شفاف کردن آن است. سؤال‌تان را در تلگرام برای @BaharTeimorpour بفرستید (لینک در بیو)؛ مشاوره اولیه رایگان است.\n\n#بهار_آکادمیک_لب #سوال_پژوهش #پایان_نامه #پروپوزال #کارشناسی_ارشد #دانشجویان_ایرانی"},
}

def esc(s):
    s = html.escape(s)
    return re.sub(r'([A-Za-z@][A-Za-z0-9@._\-]*(?: [A-Za-z][A-Za-z0-9\-]*)*)', r'<span dir="ltr">\1</span>', s)

def ff(w, f): return f"@font-face{{font-family:V;font-weight:{w};src:url('file://{FONTS}/{f}')}}"
CSS = f"""{ff(400,'vazirmatn-arabic-400-normal.woff2')}{ff(700,'vazirmatn-arabic-700-normal.woff2')}{ff(900,'vazirmatn-arabic-900-normal.woff2')}
@font-face{{font-family:L;font-weight:700;src:url('file://{FONTS}/vazirmatn-latin-700-normal.woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;font-family:V,L,sans-serif;direction:rtl;overflow:hidden}}
.s{{width:1080px;height:1920px;padding:260px 100px 360px;display:flex;flex-direction:column;justify-content:center;position:relative}}
.coral{{background:{CORAL};color:{CREAM}}} .cream{{background:{CREAM};color:{BROWN}}} .brown{{background:{BROWN};color:{CREAM}}}
.t{{font-size:84px;line-height:1.65;font-weight:900}}
.cream .t{{font-weight:700;font-size:78px}}
.brown .t{{color:{GOLD}}}
.rule{{width:150px;height:9px;border-radius:5px;background:{GOLD};margin-bottom:56px}} .coral .rule{{background:{CREAM}}}
.pill{{align-self:flex-start;border:3px solid {CREAM};border-radius:44px;padding:8px 36px;font-size:34px;font-weight:700;margin-bottom:56px}}
.h{{position:absolute;bottom:230px;left:0;right:0;text-align:center;font-family:L,V;font-size:34px;font-weight:700;direction:ltr;opacity:.85}}
"""
def page(kind, text, label):
    cls = {"hook":"coral","pt":"cream","cta":"brown"}[kind]
    pill = f'<div class="pill">{esc(label)}</div>' if kind == "hook" else ""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s {cls}">{pill}<div class="rule"></div><div class="t">{esc(text)}</div><div class="h">{HANDLE}</div></div></body></html>'

def run(*a): subprocess.run(a, check=True, capture_output=True)

if __name__ == "__main__":
    out = sys.argv[1]; only = sys.argv[2:]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width":1080,"height":1920})
        for key, r in REELS.items():
            if only and key not in only: continue
            d = os.path.join(out, key); os.makedirs(d, exist_ok=True)
            parts = []
            for i, (k, t) in enumerate(r["scenes"], 1):
                fp = f"/tmp/{key}_{i}.html"; open(fp, "w", encoding="utf-8").write(page(k, t, r["label"]))
                pg.goto("file://" + fp); pg.wait_for_timeout(250)
                png = os.path.join(d, f"scene{i}.png"); pg.screenshot(path=png)
                dur = 3.2 if k == "hook" else (4.6 if len(t) > 55 else 3.8)
                mp4 = f"/tmp/{key}_{i}.tmp.mp4"; fin = f"/tmp/{key}_{i}.mp4"
                run("ffmpeg","-y","-framerate","30","-i",png,"-vf",f"format=yuv420p,loop=-1:1,trim=duration={dur},fade=t=in:st=0:d=0.25,fade=t=out:st={dur-0.25}:d=0.25",
                    "-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p","-r","30",mp4)
                os.rename(mp4, fin); parts.append(fin)
            lst = f"/tmp/{key}_list.txt"; open(lst,"w").write("".join(f"file '{x}'\n" for x in parts))
            tmp = os.path.join(d, "reel.tmp.mp4")
            run("ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy","-movflags","+faststart",tmp)
            os.rename(tmp, os.path.join(d, "reel.mp4"))
            for f in os.listdir(d):
                if f.endswith(".png"): os.remove(os.path.join(d, f)) if f != "scene1.png" else None
            print(key, "ok")
        b.close()
