#!/home/toto/ia-test/venv/bin/python
"""Visite chaque page de chaque chapitre et signale toute erreur JavaScript ou ressource manquante."""
import sys, glob, os
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.expanduser("~/atlas-tools/ingenieur")); import build
chs, _ = build.load(); only = sys.argv[1:]; chs = [c for c in chs if not only or c["dir"] in only]
exe = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux*/chrome")))[0]
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for c in chs:
        pg = b.new_page(viewport={"width": 1400, "height": 820}); errs = []
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:200]))
        pg.on("console", lambda m: errs.append("console: " + m.text[:200]) if m.type == "error" else None)
        pg.on("requestfailed", lambda r: errs.append("requête échouée: " + r.url[:100]))
        pg.goto(f"http://127.0.0.1:8004/{c['dir']}/index.html", wait_until="networkidle"); pg.wait_for_timeout(1200)
        for i in range(len(c["pages"])):
            pg.evaluate(f"window.scrollTo(0, {i} * innerHeight)"); pg.wait_for_timeout(700)
        n = pg.evaluate("document.querySelectorAll('#labels .lbl').length")
        print(("ERREURS " if errs else "ok      ") + c["dir"], len(c["pages"]), "pages,", n, "étiquettes", *errs[:3]); bad += bool(errs); pg.close()
    b.close()
sys.exit(1 if bad else 0)
