#!/usr/bin/env python3
"""Sauvegarde le site de physique (version française, y compris les compléments) dans le dépôt GitHub atlas-de-physique.
- copie uniquement les fichiers du site de physique ; jamais vendor/, _vercel/, vercel.json (redirection vers un autre site), ni maths/ et chimie/ (autres dépôts)
- remet les adresses du CDN (three.js, polices) à la place des copies locales du VPS, pour que le dépôt soit déployable tel quel
- ne force jamais ; journal : ~/atlas-push.log"""
import os, re, sys, time, shutil, fcntl, subprocess
H = os.path.expanduser("~"); SITE = H + "/vault/atlas_of_physics_local/atlas-of-physics.vercel.app/"; REPO = H + "/atlas-physique-repo"; LOG = H + "/atlas-push.log"
INCLUDE_TOP = ["index.html", "atlas.css", "LICENSE", "engine", "img", "equations"]
CHAPTERS = "kinematics newton circular energy momentum oscillations rotation fluids electrostatics gauss potential capacitors circuits magnetism induction".split()
CDN = "https://cdn.jsdelivr.net/npm/three@0.186.1/"
FONTS = '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
def log(m): open(LOG, "a").write(time.strftime("%Y-%m-%d %H:%M:%S ") + "physique : " + m + "\n")
def git(*a, check=True):
    r = subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True)
    if check and r.returncode: raise RuntimeError(f"git {' '.join(a)} : {r.stderr.strip()[:300]}")
    return r.stdout.strip()
def to_cdn(t):
    t = t.replace("/vendor/three/build/three.module.js", CDN + "build/three.module.js").replace("/vendor/three/build/three.core.js", CDN + "build/three.core.js")
    t = t.replace("/vendor/three/examples/jsm/", CDN + "examples/jsm/")
    return t.replace('<link href="/vendor/fonts/fonts.css" rel="stylesheet">', FONTS)
README = """# Atlas de physique (version française)

Sauvegarde du site de physique : les 15 chapitres de l’[Atlas of Physics](https://github.com/nathanliow/atlas-of-physics) de Nathan Liow (licence MIT), traduits en français, avec la feuille d’équations les sept chapitres de compléments sont dans le dépôt `atlas-de-physique-complements`.

Ce dépôt est mis à jour automatiquement depuis le VPS. Le moteur de rendu (three.js, pages qui se tournent, figures décomposables) et les chapitres d’origine viennent du projet de Nathan Liow ; la licence MIT d’origine est conservée dans `LICENSE`.

Les atlas de maths et de chimie sont dans des dépôts séparés : `atlas-des-maths` et `atlas-de-chimie`.
"""
def main():
    lock = open(H + "/.atlas-update.lock", "w"); fcntl.flock(lock, fcntl.LOCK_EX)
    git("pull", "--rebase", "--autostash", "-q")
    wanted = INCLUDE_TOP + CHAPTERS
    for name in os.listdir(REPO):   # supprime du dépôt ce qui n'est plus dans le site (sauf .git et README.md)
        if name not in wanted + [".git", "README.md"]:
            shutil.rmtree(REPO + "/" + name) if os.path.isdir(REPO + "/" + name) else os.remove(REPO + "/" + name)
    for name in wanted:
        src, dst = SITE + name, REPO + "/" + name
        if not os.path.exists(src): continue
        if os.path.isdir(src):
            if os.path.exists(dst): shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else: shutil.copy2(src, dst)
    for dp, _, fs in os.walk(REPO):
        if ".git" in dp.split(os.sep): continue
        for f in fs:
            if f.endswith(".html"):
                p = os.path.join(dp, f); t = open(p, encoding="utf8").read(); n = to_cdn(t)
                if n != t: open(p, "w", encoding="utf8").write(n)
    open(REPO + "/README.md", "w", encoding="utf8").write(README)
    git("add", "-A")
    if os.environ.get("DRY"): print("essai à blanc : rien n'est validé ni poussé"); return
    if not git("status", "--porcelain"):
        if not git("rev-list", "origin/main..HEAD"): log("rien à sauvegarder"); return
    else: git("commit", "-q", "-m", "Sauvegarde du site de physique (français)")
    git("push", "-q", "origin", "HEAD:main"); log(f"sauvegardé ({git('rev-parse', '--short', 'HEAD')}, {git('ls-files').count(chr(10)) + 1} fichiers)")
if __name__ == "__main__":
    try: main()
    except Exception as e:
        log(f"ÉCHEC ({e})"); subprocess.run(["git", "-C", REPO, "rebase", "--abort"], capture_output=True)
