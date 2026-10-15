"""Render 1200x630 social share images (JPEG) for every article, in EN, FR and AR.
usage: python3 make_og.py [ar]   -> 'ar' renders only the Arabic images"""
import json, glob, os, sys
from playwright.sync_api import sync_playwright
from covers import cover_svg
import i18n, i18n_extra, i18n_ar  # noqa: F401
from i18n import CAT
from i18n_extra import X
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "og"); os.makedirs(OUT, exist_ok=True)
ONLY = sys.argv[1:] or ["en", "fr", "ar"]
FONT = os.path.join(HERE, "static", "fonts")
FACE = (f'<style>@font-face{{font-family:"IBM Plex Sans Arabic";font-weight:700;src:url("file://{FONT}/ibm-plex-sans-arabic-700.woff2")}}'
        f'@font-face{{font-family:"IBM Plex Sans Arabic";font-weight:400;src:url("file://{FONT}/ibm-plex-sans-arabic-400.woff2")}}</style>')
posts = []
for f in sorted(glob.glob(os.path.join(HERE, "content", "*.json"))):
    p = json.load(open(f, encoding="utf-8")); p["slug"] = os.path.basename(f)[:-5]
    af = os.path.join(HERE, "content_ar", p["slug"] + ".json")
    if os.path.exists(af): p["ar"] = json.load(open(af, encoding="utf-8"))["ar"]
    posts.append(p)
seen = {}
for p in sorted(posts, key=lambda p: p["slug"]):
    k = (p["category"], p.get("cover_motif")); p["variant"] = seen.get(k, 0); seen[k] = p["variant"] + 1
suffix = lambda L: "" if L == "en" else "-" + L
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    def shot(svg, out, rtl):
        pg.set_content(f'<html><head>{FACE if rtl else ""}</head><body style="margin:0">{svg}</body></html>')
        if rtl: pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(60 if rtl else 0)
        pg.screenshot(path=out, type="jpeg", quality=86, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
    for p in posts:
        for L in ONLY:
            if L not in p: continue
            svg = cover_svg(p["slug"], p["category"], p.get("cover_motif"), title=p[L]["title"], label=CAT[L][p["category"]], variant=p["variant"], rtl=(L == "ar"))
            shot(svg, os.path.join(OUT, p["slug"] + suffix(L) + ".jpg"), L == "ar")
    for slug, cat, motif in [("directory", "startups", "network-nodes"), ("regulation-tracker", "regulation", "scales-law")]:
        for L in ONLY:
            title = X[L]["dir_h1"] if slug == "directory" else X[L]["reg_h1"]
            lab = X[L]["tool_dir"] if slug == "directory" else X[L]["tool_reg"]
            shot(cover_svg(slug, cat, motif, title=title, label=lab, rtl=(L == "ar")), os.path.join(OUT, slug + suffix(L) + ".jpg"), L == "ar")
    b.close()
print(len(os.listdir(OUT)), "images in og/")
