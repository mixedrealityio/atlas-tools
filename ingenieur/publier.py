#!/usr/bin/env python3
"""Copie l'atlas de l'ingénieur IA (~/atlas-ingenieur-upstream) dans le site servi, sous /ingenieur/.
Les pages HTML passent par rewrite_html d'atlas-update.py (three.js et polices locaux).
Usage : python3 publier.py"""
import os, sys, shutil
sys.path.insert(0, os.path.expanduser("~/atlas-tools"))
from importlib import import_module
U = import_module("atlas-update")
SRC = os.path.expanduser("~/atlas-ingenieur-upstream")
DST = U.SITE + "ingenieur"
n = 0
for racine, dossiers, fichiers in os.walk(SRC):
    dossiers[:] = [d for d in dossiers if d != ".git"]
    for f in fichiers:
        s = os.path.join(racine, f); d = os.path.join(DST, os.path.relpath(s, SRC))
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if f.endswith(".html"):
            open(d, "w", encoding="utf8").write(U.rewrite_html(open(s, encoding="utf8").read()))
        else:
            shutil.copy2(s, d)
        n += 1
print(n, "fichiers copiés vers", DST)
