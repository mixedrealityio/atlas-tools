# Outils communs aux contenus de l'Atlas de la 3D : chapitres, pages, scènes, exercices
def P(q, ch, a, w): return dict(q=q, choices=ch, answer=a, why=f"<p>{w}</p>")
def B(*parts):
    out = []; first = True
    for p in parts:
        if isinstance(p, list): out.append('<ul class="rules">' + "".join(f"<li>{x}</li>" for x in p) + "</ul>")
        elif isinstance(p, tuple): out.append('<table class="data">' + "".join("<tr>" + "".join((f"<th>{c}</th>" if i == 0 else f"<td>{c}</td>") for c in row) + "</tr>" for i, row in enumerate(p)) + "</table>")
        elif p.startswith("="): out.append(f'<div class="eq">{p[1:]}</div>')
        elif p.startswith("<"): out.append(p)
        else: out.append(f'<p class="lede">{p}</p>' if first else f"<p>{p}</p>"); first = False
    return "\n    ".join(out)
def pg(title, sub, scene, *parts, cam=None):
    d = dict(title=title, sub=sub, scene=scene, body=B(*parts))
    if cam: d["cam"] = cam
    return d
def SC(key, title, sub, kind, plate, facts, **kw): return dict(key=key, title=title, sub=sub, kind=kind, plate=plate, facts=facts, **kw)
def PIPE(key, title, sub, stages, plate, facts, per=3, **kw):
    return dict(key=key, title=title, sub=sub, kind="pipeline", per=per, bw=kw.pop("bw", 2.2), gap=kw.pop("gap", 0.75), y=1.4,
                stages=[dict(n=a, s=b, **({"pal": c} if c else {})) for a, b, c in stages], plate=plate, facts=facts, **kw)
def CH(dir, no, mod, title, sub, cnt, alt, scenes, pages, practice=None):
    for i, p in enumerate(pages): p["kicker"] = f"Chapitre {no} · {mod}" if i == 0 else f"{no}.{i}"
    return dict(dir=dir, no=no, title=title, sub=sub, cnt=cnt, alt=alt, scenes=scenes, pages=pages, practice=practice or {})
