#!/usr/bin/env python3
"""Pousse sur GitHub les ajouts faits sur le VPS aux dépôts de l'utilisateur : la feuille d'équations (equations/index.html)
et le lien « équations » de index.html. Rien d'autre n'est jamais ajouté ni poussé, jamais de force. Journal : ~/atlas-push.log"""
import os, re, sys, time, fcntl, subprocess, importlib.util
H = os.path.expanduser("~")
LOG = H + "/atlas-push.log"
REPOS = [  # (nom, clone local, sous-dossier du site)  — ajouter ici le 3e dépôt une fois connu
    ("maths", H + "/atlas-maths-upstream"),
    ("chimie", H + "/atlas-chimie-upstream"),
    ("complements", H + "/atlas-complements-upstream"),
]
spec = importlib.util.spec_from_file_location("mk", H + "/atlas-tools/make-equations.py"); mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
def log(m): open(LOG, "a").write(time.strftime("%Y-%m-%d %H:%M:%S ") + m + "\n")
def git(repo, *a, check=True):
    r = subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True)
    if check and r.returncode: raise RuntimeError(f"git {' '.join(a)} : {r.stderr.strip()[:300]}")
    return r.stdout.strip()
LINKS = {
 "maths": ('<span>Collège · lycée · MPSI</span>', '<span><a href="equations/index.html" style="color:inherit">Feuille d’équations</a> · Collège · lycée · MPSI</span>'),
 "chimie": ('</span></header>', '<a class="gh" href="equations/">équations</a></span></header>'),
 "complements": ('</span></header>', '<a class="gh" href="equations/">équations</a></span></header>'),
}
def push_one(name, repo):
    if git(repo, "ls-remote", "--heads", "origin", "main"):   # dépôt encore vide : rien à récupérer
        git(repo, "pull", "--rebase", "--autostash", "-q")
    d = repo + "/equations"; os.makedirs(d, exist_ok=True)
    open(d + "/index.html", "w", encoding="utf8").write(mk.repo_sheet(name))
    idx = repo + "/index.html"; t = open(idx, encoding="utf8").read()
    if 'href="equations/' not in t and "<header" in t:
        old, new = LINKS[name]; j = t.index(old, t.index("<header"))
        open(idx, "w", encoding="utf8").write(t[:j] + new + t[j + len(old):])
    git(repo, "add", "--", "equations/index.html", "index.html")
    if git(repo, "status", "--porcelain", "--", "equations/index.html", "index.html"):
        git(repo, "commit", "-q", "-m", "Feuille d’équations (générée sur le VPS)", "--", "equations/index.html", "index.html")
    elif not git(repo, "rev-list", "origin/main..HEAD"):
        log(f"{name} : rien à pousser"); return   # sinon : un commit local attend encore d'être poussé (clé non autorisée, réseau…)
    git(repo, "push", "-q", "origin", "HEAD:main")
    log(f"{name} : poussé ({git(repo, 'rev-parse', '--short', 'HEAD')})")
def main():
    lock = open(H + "/.atlas-update.lock", "w"); fcntl.flock(lock, fcntl.LOCK_EX)   # ne pas croiser la mise à jour quotidienne
    for name, repo in REPOS:
        try: push_one(name, repo)
        except Exception as e:
            log(f"{name} : ÉCHEC ({e})")
            subprocess.run(["git", "-C", repo, "rebase", "--abort"], capture_output=True)
if __name__ == "__main__": main()
