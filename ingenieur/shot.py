#!/home/toto/ia-test/venv/bin/python
"""usage: shot.py <chapitre> <page> [sortie.png] — capture une page d'un chapitre et affiche les erreurs JavaScript."""
import sys, glob, os
from playwright.sync_api import sync_playwright
ch, pg = sys.argv[1], int(sys.argv[2]); out = sys.argv[3] if len(sys.argv) > 3 else f"/home/toto/ia-test/ing-{ch}-{pg}.png"
exe = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux*/chrome")))[0]
port = os.environ.get("PORT", "8004")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pgx = b.new_page(viewport={"width": 1400, "height": 820}); errs = []
    pgx.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:300]))
    pgx.on("console", lambda m: errs.append("console." + m.type + ": " + m.text[:300]) if m.type in ("error",) else None)
    pgx.on("requestfailed", lambda r: errs.append("requête échouée: " + r.url[:120]))
    pgx.goto(f"http://127.0.0.1:{port}/{ch}/index.html", wait_until="networkidle")
    pgx.wait_for_timeout(1500)
    if pg: pgx.evaluate(f"window.scrollTo(0, {pg} * innerHeight)"); pgx.wait_for_timeout(int(os.environ.get("WAIT", "3500")))
    pgx.screenshot(path=out); b.close()
print("→", out); [print("  !", e) for e in errs[:8]]
