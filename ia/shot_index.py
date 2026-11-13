#!/home/toto/ia-test/venv/bin/python
import glob, os
from playwright.sync_api import sync_playwright
exe = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux*/chrome")))[0]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe, args=["--no-sandbox"]); pg = b.new_page(viewport={"width": 1300, "height": 900}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:200])); pg.goto("http://127.0.0.1:8002/index.html", wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.screenshot(path="/home/toto/ia-test/index.png", full_page=True); b.close(); print("erreurs:", errs)
