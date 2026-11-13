#!/home/toto/ia-test/venv/bin/python
"""Fabrique img/<chapitre>.jpg : la figure de la première page de chaque chapitre (capture du panneau de droite)."""
import sys, subprocess, os, glob
from PIL import Image
sys.path.insert(0, os.path.expanduser("~/atlas-tools/3d")); import build
chs, _ = build.load(); only = sys.argv[1:]
os.makedirs(build.OUT + "/img", exist_ok=True)
for c in chs:
    if only and c["dir"] not in only: continue
    pg = int(c.get("cover_page", 1)); out = f"/home/toto/ia-test/cover3d-{c['dir']}.png"
    subprocess.run(["/home/toto/atlas-tools/3d/shot.py", c["dir"], str(pg), out], capture_output=True, env={**os.environ, "WAIT": "4500"})
    im = Image.open(out).convert("RGB").crop((582, 66, 1368, 786)); im = im.resize((560, 513)); im.save(f"{build.OUT}/img/{c['dir']}.jpg", quality=84)
    print("couverture", c["dir"], os.path.getsize(f"{build.OUT}/img/{c['dir']}.jpg") // 1024, "Ko")
