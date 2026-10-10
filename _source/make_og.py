"""Render 1200x630 social share images (JPEG) for every article, EN + FR."""
import json, glob, os, sys
from playwright.sync_api import sync_playwright
from covers import cover_svg
from i18n import CAT
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "og"); os.makedirs(OUT, exist_ok=True)
posts = [json.load(open(f)) | {"slug": os.path.basename(f)[:-5]} for f in sorted(glob.glob(os.path.join(HERE, "content", "*.json")))]
seen = {}
for p in sorted(posts, key=lambda p: p["slug"]):
    k = (p["category"], p.get("cover_motif")); p["variant"] = seen.get(k, 0); seen[k] = p["variant"] + 1
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    for p in posts:
        for L in ("en", "fr"):
            out = os.path.join(OUT, p["slug"] + ("" if L == "en" else "-fr") + ".jpg")
            svg = cover_svg(p["slug"], p["category"], p.get("cover_motif"), title=p[L]["title"], label=CAT[L][p["category"]], variant=p["variant"])
            pg.set_content(f'<html><body style="margin:0">{svg}</body></html>')
            pg.screenshot(path=out, type="jpeg", quality=86, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
    b.close()
print(len(os.listdir(OUT)), "images")
