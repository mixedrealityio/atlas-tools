#!/usr/bin/env python3
"""Met à jour la copie d'Atlas of Physics (servie sur le port 8000) depuis le dépôt GitHub amont
(https://github.com/nathanliow/atlas-of-physics, lien en haut à droite de la page de garde).
- git pull du dépôt dans ~/atlas-upstream
- pour chaque fichier du site ajouté ou modifié en amont : copie, réapplique les réglages hors ligne
  (three.js et polices locaux) sur les pages HTML, puis retraduit en français (atlas_translate.py)
- sauvegarde les fichiers remplacés dans ~/atlas-backups/AAAAMMJJ/. Journal : ~/atlas-update.log"""
import os, re, sys, fcntl, shutil, subprocess, time
sys.path.insert(0, os.path.dirname(__file__))
import atlas_translate as T
UP = os.path.expanduser("~/atlas-upstream"); LAST = os.path.expanduser("~/atlas-upstream.last")
SITE = T.ROOT; LOG = os.path.expanduser("~/atlas-update.log")
SKIP = re.compile(r"^(\.git|tools/|README\.md|package(-lock)?\.json|\.gitignore)|\.mjs$")
def log(m): open(LOG, "a").write(time.strftime("%Y-%m-%d %H:%M:%S ") + m + "\n")
def git(*a): return subprocess.run(["git", "-C", UP, *a], capture_output=True, text=True, check=True).stdout
def blob(rev, path):
    r = subprocess.run(["git", "-C", UP, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def rewrite_html(s):
    s = s.replace("https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js", "/vendor/three/build/three.module.js")
    s = s.replace("https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.core.js", "/vendor/three/build/three.core.js")
    s = s.replace("https://cdn.jsdelivr.net/npm/three@0.186.1/examples/jsm/", "/vendor/three/examples/jsm/")
    s = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">', '<link href="/vendor/fonts/fonts.css" rel="stylesheet">', s)
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\n?', "", s)
    s = s.replace("Drag to turn · shift-drag to pan · click to break it down", "Glissez pour tourner · Maj + glisser pour déplacer · cliquez pour décomposer")
    s = s.replace("Scroll to turn the page", "Faites défiler pour tourner la page")
    return s
LINK = '<a href="complements/index.html" style="color:inherit">Compléments</a>'
def ensure_links():
    """réinsère le lien vers les compléments sur la page d'accueil (le fichier est remplacé quand l'amont le modifie)"""
    p = SITE + "index.html"; s = open(p, encoding="utf8").read()
    if "complements/index.html" in s: return
    m = re.search(r'<a href="equations/index.html"[^>]*>[^<]*</a>', s)
    if not m: log("lien Compléments : ancre introuvable dans index.html"); return
    open(p, "w", encoding="utf8").write(s[:m.end()] + LINK + s[m.end():]); log("lien Compléments réinséré sur l'accueil")
def main():
    lock = open(os.path.expanduser("~/.atlas-update.lock"), "w")
    try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: log("déjà en cours, abandon"); return
    old = open(LAST).read().strip()
    git("pull", "--ff-only", "-q"); new = git("rev-parse", "HEAD").strip()
    files = [f for f in git("ls-files").split("\n") if f and not SKIP.search(f)]
    todo = []
    for f in files:
        if not os.path.exists(SITE + f) or (old != new and blob(old, f) != blob(new, f)): todo.append(f)
    if not todo: ensure_links(); log(f"à jour ({new[:7]}), rien à faire"); return
    log(f"{old[:7]} → {new[:7]} : {len(todo)} fichier(s) à mettre à jour")
    bk = os.path.expanduser("~/atlas-backups/") + time.strftime("%Y%m%d") + "/"
    PROT = set()
    for f in todo + [x for x in files if x.endswith(".js")]:
        try: PROT |= T.protected_tokens(open(UP + "/" + f, encoding="utf8").read())
        except Exception: pass
    for f in todo:
        src = UP + "/" + f; dst = SITE + f
        if os.path.exists(dst):
            os.makedirs(os.path.dirname(bk + f), exist_ok=True); shutil.copy2(dst, bk + f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if f.endswith((".html", ".js", ".css")):
            txt = open(src, encoding="utf8").read()
            if f.endswith(".html"): txt = rewrite_html(txt)
            open(dst, "w", encoding="utf8").write(txt)
            os.makedirs(os.path.dirname(T.BK + f), exist_ok=True); shutil.copy2(src, T.BK + f)  # original anglais
            if f.endswith((".html", ".js")) and not f.startswith("engine/book.css"):
                try: T.do_file(f, PROT)
                except Exception as e: log(f"  {f}: traduction impossible ({e}), laissé en anglais")
        else:
            shutil.copy2(src, dst)
    ensure_links()
    ensure_compact_css()
    open(LAST, "w").write(new)
    log("terminé")
MATHS_UP = os.path.expanduser("~/atlas-maths-upstream"); MATHS_LAST = os.path.expanduser("~/atlas-maths-upstream.last")
MATHS_SKIP = re.compile(r"^(\.git|README\.md|\.gitignore|package(-lock)?\.json)|\.mjs$")
def sync_repo(label, UP, LASTF, sub):
    """Atlas en français (maths, chimie…) : dépôt GitHub de l'utilisateur → site/<sub>/ ; aucune traduction"""
    lock = open(os.path.expanduser("~/.atlas-update.lock"), "w")
    try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: log(f"{label} : déjà en cours"); return
    g = lambda *a: subprocess.run(["git", "-C", UP, *a], capture_output=True, text=True, check=True).stdout
    bl = lambda rev, f: (lambda r: r.stdout if r.returncode == 0 else None)(subprocess.run(["git", "-C", UP, "show", f"{rev}:{f}"], capture_output=True))
    if not g("ls-remote", "--heads", "origin", "main").strip(): log(f"{label} : dépôt GitHub encore vide, rien à synchroniser"); return
    old = open(LASTF).read().strip(); g("pull", "--rebase", "--autostash", "-q"); new = g("rev-parse", "HEAD").strip()
    dest = SITE + sub + "/"; bk = os.path.expanduser("~/atlas-backups/") + time.strftime("%Y%m%d") + "/" + sub + "/"
    todo = [f for f in g("ls-files").split("\n") if f and not MATHS_SKIP.search(f)
            and (not os.path.exists(dest + f) or (old != new and bl(old, f) != bl(new, f)))]
    if not todo: log(f"{label} à jour ({new[:7]})"); return
    log(f"{label} {old[:7]} → {new[:7]} : {len(todo)} fichier(s)")
    for f in todo:
        d = dest + f
        if os.path.exists(d): os.makedirs(os.path.dirname(bk + f), exist_ok=True); shutil.copy2(d, bk + f)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if f.endswith(".html"): open(d, "w", encoding="utf8").write(rewrite_html(open(UP + "/" + f, encoding="utf8").read()))
        else: shutil.copy2(UP + "/" + f, d)
        if f.endswith(".js"):
            shutil.copy2(d, "/tmp/_m_sync.mjs")
            if subprocess.run(["node", "--check", "/tmp/_m_sync.mjs"], capture_output=True).returncode:
                log(f"  {sub}/{f}: syntaxe invalide, ancienne version restaurée")
                if os.path.exists(bk + f): shutil.copy2(bk + f, d)
    open(LASTF, "w").write(new); log(f"{label} terminé")
REPOS = [("maths", MATHS_UP, MATHS_LAST, "maths"),
         ("chimie", os.path.expanduser("~/atlas-chimie-upstream"), os.path.expanduser("~/atlas-chimie-upstream.last"), "chimie"),
         ("annales", os.path.expanduser("~/annales-upstream"), os.path.expanduser("~/annales-upstream.last"), "annales"),
         ("complements", os.path.expanduser("~/atlas-complements-upstream"), os.path.expanduser("~/atlas-complements-upstream.last"), "complements"),
         ("ia", os.path.expanduser("~/atlas-ia-upstream"), os.path.expanduser("~/atlas-ia-upstream.last"), "ia"),
         ("3d", os.path.expanduser("~/atlas-3d-upstream"), os.path.expanduser("~/atlas-3d-upstream.last"), "3d")]
SHEET_LINKS = [("maths", '<span>Collège · lycée · MPSI</span>', '<span><a href="equations/index.html" style="color:inherit">Feuille d’équations</a> · Collège · lycée · MPSI</span>'),
               ("chimie", '</span></header>', '<a class="gh" href="equations/">équations</a></span></header>'),
               ("complements", '</span></header>', '<a class="gh" href="equations/">équations</a></span></header>')]
def ensure_sheet_links():
    """lien « équations » dans l'en-tête des sommaires de maths, chimie et compléments (fichiers remplacés par la synchronisation GitHub)"""
    for sub, old, new in SHEET_LINKS:
        p = SITE + sub + "/index.html"
        if not os.path.exists(p) or not os.path.exists(SITE + sub + "/equations/index.html"): continue
        t = open(p, encoding="utf8").read()
        if 'href="equations/' in t: continue
        if t.count(old) < 1: log(f"lien équations : ancre introuvable dans {sub}/index.html"); continue
        i = t.index("<header")
        j = t.index(old, i)
        open(p, "w", encoding="utf8").write(t[:j] + new + t[j + len(old):]); log(f"lien équations réinséré dans {sub}/index.html")
COMPACT_MARK = "typographie resserrée de la page de gauche"
def ensure_compact_css():
    """réajoute la typographie resserrée aux feuilles book.css des atlas du VPS (elles sont remplacées quand l'amont les modifie)"""
    block = open(os.path.expanduser("~/atlas-tools/compact.css"), encoding="utf8").read()
    for d in ("engine", "maths/engine", "chimie/engine", "complements/engine"):
        p = SITE + d + "/book.css"
        if os.path.exists(p):
            t = open(p, encoding="utf8").read()
            if COMPACT_MARK not in t: open(p, "w", encoding="utf8").write(t + block); log(f"typographie resserrée réajoutée à {d}/book.css")
def sync_all():
    for label, up, last, sub in REPOS:
        try: sync_repo(label, up, last, sub)
        except Exception as e: log(f"ERREUR {label}: {e}")
    ensure_sheet_links()
    ensure_compact_css()
if __name__ == "__main__":
    try: main()
    except Exception as e: log(f"ERREUR: {e}")
    sync_all()
