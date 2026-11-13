#!/usr/bin/env python3
"""Génère l'atlas de l’ingénieur IA à partir des contenus content_*.py : chapitres, sommaire, exercices.
Usage : python3 build.py [dir-du-chapitre ...]   (sans argument : tout)"""
import os, sys, json, html, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = os.path.expanduser("~/atlas-ingenieur-upstream")
FONTS = '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
IMPORTMAP = '{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js", "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.186.1/examples/jsm/" } }'

def load():
    ch = []; groups = []
    for m in sorted(f[:-3] for f in os.listdir(HERE) if f.startswith("content_") and f.endswith(".py")):
        mod = importlib.import_module(m); importlib.reload(mod); ch += mod.CHAPTERS
        groups += getattr(mod, "GROUPS", [])
    ch.sort(key=lambda c: c["no"])
    for m in sorted(f[:-3] for f in os.listdir(HERE) if f.startswith("content_") and f.endswith(".py")):
        for d, add in getattr(importlib.import_module(m), "ADDITIONS", {}).items():
            c = next(x for x in ch if x["dir"] == d); n0 = len(c["pages"])
            c["scenes"] += add.get("scenes", []); c["pages"] += add["pages"]
            for i, v in add.get("practice", {}).items(): c["practice"].setdefault(n0 + i, []).extend(v)
            for i, p in enumerate(c["pages"]): p.setdefault("kicker", f"{c['no']}.{i}")  # pages ajoutées : numérotées à la suite
    merged = {}
    for t, ds in groups: merged.setdefault(t, []).extend(d for d in ds if d not in merged.get(t, []))
    order = {c["dir"]: c.get("shelf", c["no"]) for c in ch}  # « shelf » place un chapitre ailleurs dans son rayon (l’introduction en tête)
    nos = {c["dir"]: c["no"] for c in ch}
    return ch, sorted([(t, sorted(ds, key=lambda d: order.get(d, 99))) for t, ds in merged.items()], key=lambda g: min(nos.get(d, 999) for d in g[1]))

def js(x): return json.dumps(x, ensure_ascii=False)

REMAP = {}
PANEL_KINDS = ("pipeline", "cycle")
def panel_html(s):
    E = html.escape
    items = s.get("stages") or s.get("nodes") or []
    li = "".join(f'<li class="{it.get("pal", "")}"><span class="st"><b>{E(it["n"])}</b><i>{E(it.get("s", ""))}</i></span>'
                 + (f'<pre class="ex">{E(it["ex"])}</pre>' if it.get("ex") else "<span></span>") + "</li>" for it in items)
    loop = f'<div class="loop">↺ retour à l’étape 1{(" · " + E(s["center"])) if s.get("center") else ""}</div>' if s["kind"] == "cycle" else ""
    facts = "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in s.get("facts", []))
    return (f'<h2>{E(s["title"])}</h2><div class="psub">{E(s.get("sub", ""))}</div><ol class="flow">{li}</ol>{loop}'
            f'<p class="note">{s.get("plate", "")}</p>' + (f'<table class="data">{facts}</table>' if facts else ""))
def chapter_files(c):
    d = f"{OUT}/{c['dir']}"; os.makedirs(d, exist_ok=True)
    scenes = []; plates = {}; cams = {}
    panels = {s["key"]: panel_html(s) for s in c["scenes"] if s["kind"] in PANEL_KINDS}
    for i, s in enumerate([s for s in c["scenes"] if s["kind"] not in PANEL_KINDS]):
        s = dict(s); s["x0"] = 40 * i
        cam = s.pop("cam", {}); plate = s.pop("plate", ""); facts = s.pop("facts", [])
        cams[s["key"]] = dict(target=[s["x0"], 1.8, 0], az=cam.get("az", 8), el=cam.get("el", 7), dist=26, auto=True)
        plates[s["key"]] = (plate, facts); scenes.append(s)
    # pages.js
    P = []
    for p in c["pages"]:
        key = p.get("scene", c["scenes"][0]["key"]); cam = dict(cams.get(key, dict(target=[0, 1.8, 0], az=8, el=7, dist=26))); cam.update(p.get("cam", {}))
        if key in panels: cam.pop("auto", None)
        P.append(dict(kicker=p["kicker"], title=p["title"], sub=p["sub"], body=p["body"], cam=cam, lit=p.get("lit", key), look={}, scene=key, fig=p.get("fig", ""), panel=panel_html(p["fiche"]) if p.get("fiche") else panels.get(key, "")))
    pj = "export const PAGES = " + json.dumps(P, ensure_ascii=False, indent=1) + ";\nexport const PLATES = {\n" + ",\n".join(
        f"  {k}: {{ text: {js(t)}, facts: () => {js(f)} }}" for k, (t, f) in plates.items()) + "\n};\n"
    open(d + "/pages.js", "w", encoding="utf8").write("// Chapitre " + str(c["no"]) + " : " + c["title"] + " (généré par build.py)\n" + pj)
    open(d + "/scenes.js", "w", encoding="utf8").write("export const SPECS = " + json.dumps(scenes, ensure_ascii=False, indent=1) + ";\n")
    pr = {}
    for i, v in c.get("practice", {}).items(): pr.setdefault(REMAP.get(c["dir"], {}).get(i, i), []).extend(v)
    open(d + "/practice.js", "w", encoding="utf8").write("export const PRACTICE = " + json.dumps(pr, ensure_ascii=False, indent=1) + ";\n")
    open(d + "/main.js", "w", encoding="utf8").write(f"""import {{ startBook }} from '../engine/book.js';
import {{ buildScenes }} from '../engine/iakit.js';
import {{ PAGES, PLATES }} from './pages.js';
import {{ SPECS }} from './scenes.js';

let W;
startBook({{
  no: {c['no']}, PAGES, PLATES, clock0: 0, lookKeys: [],
  buildWorld(E) {{
    W = buildScenes(E, SPECS);
    for (const p of PAGES) if (p.cam.auto) Object.assign(p.cam, W.frame(p.scene));
    return {{ update: s => W.update(s), labels: W.labels }};
  }},
  state: (clock, reduced) => ({{ t: reduced ? 4 : clock }}),
  readout: (s, p) => W.info(p.scene),
}});
""")
    n = f"{c['no']:02d}"
    open(d + "/index.html", "w", encoding="utf8").write(f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(c['title'])} · Atlas de l’ingénieur IA</title>
<link rel="icon" href="data:,">
{FONTS}
<link rel="stylesheet" href="../atlas.css">
<link rel="stylesheet" href="../engine/book.css">
<link rel="expect" href="#right" blocking="render">
<script src="../engine/cover.js"></script>
<script type="importmap">
{IMPORTMAP}
</script>
</head>
<body class="book-body">
  <header class="topbar">
    <a href="../" class="brand">Atlas de l’ingénieur IA</a>
    <span class="crumb">N° {n} · {html.escape(c['title'])}</span>
    <nav class="dots" id="dots" aria-label="Pages"></nav>
  </header>

  <div class="scroll-space" id="space"></div>

  <main class="book" id="book">
    <section class="page left" id="left" aria-live="polite">
      <article class="sheet" id="sheet"></article>
      <article class="plate" id="plate" hidden></article>
      <footer class="folio"><span>{html.escape(c['title'])}</span><span id="folio">1</span></footer>
    </section>

    <section class="page right" id="right">
      <div class="figure">
        <canvas id="gl" aria-label="Figure interactive : {html.escape(c['alt'])}. Survolez un objet et cliquez pour le décomposer."></canvas>
        <div id="labels" aria-hidden="true"></div>
        <div class="panel" id="panel" hidden></div>
        <div class="corner tl" id="figno">Fig. 1</div>
        <div class="corner tr" id="figtitle"></div>
        <div class="corner bl" id="hint">Glisser pour tourner · Maj+glisser pour déplacer · clic pour décomposer</div>
        <div class="corner br readout" id="readout"></div>
      </div>
    </section>

    <div class="leaf" id="leaf" aria-hidden="true">
      <div class="leaf-front"><span id="leafnext"></span></div>
      <div class="leaf-back"><article class="sheet" id="leafsheet"></article></div>
    </div>
    <div class="spine" aria-hidden="true"></div>
  </main>

  <p class="scroll-cue" id="cue">Faites défiler pour tourner la page</p>
  <script type="module" src="main.js"></script>
</body>
</html>
""")

def index_html(chs, groups):
    tpl = open(os.path.expanduser("~/atlas-complements-upstream/index.html"), encoding="utf8").read()
    style = tpl[tpl.index("<style>"):tpl.index("</style>") + 8]
    byd = {c["dir"]: c for c in chs}; sec = ""
    for title, dirs in groups:
        cards = "".join(f"""    <a class="card" href="{d}/">
      <div class="no"><span>N° {byd[d]['no']:02d}</span><span>{len(byd[d]['pages'])} pages</span></div>
      <h2>{html.escape(byd[d]['title'])}</h2><i>{html.escape(byd[d]['sub'])}</i>
      <span class="cnt">{html.escape(byd[d].get('cnt', ''))}</span>
      <img src="img/{d}.jpg" alt="{html.escape(byd[d]['alt'])}">
    </a>
""" for d in dirs if d in byd)
        if cards: sec += f'  <h2 class="section">{html.escape(title)}</h2>\n  <section class="shelf">\n{cards}  </section>\n'
    total = sum(len(c["pages"]) for c in chs)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atlas de l’ingénieur IA</title>
<link rel="icon" href="data:,">
{FONTS}
<link rel="stylesheet" href="atlas.css">
<script src="engine/cover.js" data-contents></script>
<link rel="prefetch" href="https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js" crossorigin>
<link rel="prefetch" href="https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.core.js" crossorigin>
{style}
</head>
<body>
  <header><b>Atlas de l’ingénieur IA</b><span><a class="gh" href="../">← l’atlas</a></span></header>
  <section class="hero">
    <h1>Devenir ingénieur IA.</h1>
    <p>{len(chs)} chapitres, {total} pages : de Python aux systèmes d’IA en production : modèles de langage, RAG, agents, évaluation, inférence, MLOps, sécurité et conception de systèmes, en 23 étapes</p>
  </section>
{sec}</body>
</html>
"""

def main():
    chs, groups = load(); only = sys.argv[1:]
    for c in chs:
        if not only or c["dir"] in only: chapter_files(c)
    open(OUT + "/index.html", "w", encoding="utf8").write(index_html(chs, groups))
    print("chapitres générés:", [c["dir"] for c in chs if not only or c["dir"] in only])
if __name__ == "__main__": main()
