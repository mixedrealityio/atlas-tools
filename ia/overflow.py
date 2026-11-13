#!/home/toto/ia-test/venv/bin/python
"""Mesure le débordement de la page de gauche (texte) de chaque page de chaque chapitre, à plusieurs tailles de fenêtre.
usage: overflow.py <port> <préfixe d'URL> <chapitre> [chapitre ...]"""
import sys, glob, os, json
from playwright.sync_api import sync_playwright
port, pre, chs = sys.argv[1], sys.argv[2], sys.argv[3:]
exe = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux*/chrome")))[0]
SIZES = [tuple(map(int, x.split("x"))) for x in os.environ.get("SIZES", "1366x768,1440x900,1920x1080,1280x720").split(",")]
JS = """() => { const L = document.getElementById('left'), S = document.getElementById('sheet'); if (!L || !S) return null;
  const lr = L.getBoundingClientRect(); let wide = [];
  S.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.width > 0 && (r.right > lr.right + 1 || r.left < lr.left - 1)) wide.push(e.tagName.toLowerCase() + '.' + (e.className || '')); });
  const f = document.querySelector('.folio'), fr = f ? f.getBoundingClientRect() : null, sr = S.getBoundingClientRect();
  return { ch: L.clientHeight, sh: L.scrollHeight, cw: L.clientWidth, sw: L.scrollWidth, sheetW: S.scrollWidth, sheetCW: S.clientWidth, wide: [...new Set(wide)].slice(0, 4), folioOverlap: fr ? sr.bottom > fr.top + 2 : false, title: (S.querySelector('h1') || {}).textContent } }"""
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for ch in chs:
        for (W, H) in SIZES:
            pg = b.new_page(viewport={"width": W, "height": H}); pg.goto(f"http://127.0.0.1:{port}/{pre}{ch}/index.html", wait_until="networkidle"); pg.wait_for_timeout(1000)
            n = pg.evaluate("document.querySelectorAll('#dots button').length") or 1
            for i in range(n):
                pg.evaluate(f"window.scrollTo(0, {i} * innerHeight)"); pg.wait_for_timeout(900)
                m = pg.evaluate(JS)
                if not m: continue
                v = m["sh"] - m["ch"]; h = max(m["sw"] - m["cw"], m["sheetW"] - m["sheetCW"])
                if v > 2 or h > 2 or m["wide"] or m["folioOverlap"]:
                    bad += 1; print(f"{ch} p{i} {W}x{H}: vertical +{v}px, horizontal +{h}px, large={m['wide']}, chevauche le pied={m['folioOverlap']} ({(m['title'] or '')[:30]})")
            pg.close()
    b.close()
print("pages à problème :", bad)
