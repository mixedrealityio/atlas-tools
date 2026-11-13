#!/home/toto/ia-test/venv/bin/python
"""usage: sheet.py sortie.png chap:page chap:page ... — planche de contact des figures (panneau de droite)"""
import sys, subprocess, os
from PIL import Image, ImageDraw
out, items = sys.argv[1], sys.argv[2:]; tiles = []
for it in items:
    ch, pg = it.split(":"); f = f"/home/toto/ia-test/{ch}-{pg}.png"
    r = subprocess.run(["/home/toto/atlas-tools/ia/shot.py", ch, pg], capture_output=True, text=True, env={**os.environ, "WAIT": os.environ.get("WAIT", "3000")})
    errs = [l for l in r.stdout.splitlines() if "!" in l]
    im = Image.open(f).crop((580, 62, 1372, 790)).resize((528, 485)); d = ImageDraw.Draw(im); d.rectangle((0, 0, 528, 16), fill="white"); d.text((4, 2), f"{it} {'ERR ' + errs[0][:60] if errs else ''}", fill="black"); tiles.append(im)
cols = 3; rows = (len(tiles) + cols - 1) // cols; W = Image.new("RGB", (528 * cols, 485 * rows), "white")
for i, t in enumerate(tiles): W.paste(t, ((i % cols) * 528, (i // cols) * 485))
W.save(out); print("→", out)
