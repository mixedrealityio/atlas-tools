import os,re,sys
R=os.path.expanduser("~/vault/atlas_of_physics_local/atlas-of-physics.vercel.app/"); B=os.path.expanduser("~/hermes-backup-20261026/atlas-original-en/")
import bisect
def skeleton_lines(s):
    """squelette du code (hors littéraux de chaîne) par ligne ; l'état des gabarits `...` est suivi sur tout le fichier"""
    nl=[m.start() for m in re.finditer("\n",s)]; per=[[] for _ in range(len(nl)+1)]; n=len(s)
    def emit(pos,t): per[bisect.bisect_left(nl,pos)].append(t)
    def q(i,qc):
        while i<n:
            if s[i]=="\\": i+=2; continue
            if s[i]==qc: return i+1
            if s[i]=="\n": return i
            i+=1
        return i
    def tpl(i):
        while i<n:
            c=s[i]
            if c=="\\": i+=2; continue
            if c=="`": return i+1
            if c=="$" and i+1<n and s[i+1]=="{":
                emit(i,"${"); i+=2; d=1
                while i<n and d:
                    c=s[i]
                    if c in "'\"": emit(i,"S"); i=q(i+1,c); continue
                    if c=="`": emit(i,"T"); i=tpl(i+1); continue
                    if c=="{": d+=1
                    if c=="}": d-=1
                    emit(i,c); i+=1
                continue
            i+=1
        return i
    i=0
    while i<n:
        c=s[i]
        if c in "'\"": emit(i,"S"); i=q(i+1,c); continue
        if c=="`": emit(i,"T"); i=tpl(i+1); continue
        if c=="/" and s[i:i+2]=="//":
            while i<n and s[i]!="\n": i+=1
            continue
        emit(i,c); i+=1
    return [re.sub(r"\s+","","".join(x)) for x in per]
def skeleton(s): return "".join(skeleton_lines(s))
def html_skel(s): return re.sub(r"\s+","",re.sub(r">[^<]*<","><",s))
def bad_files():
    bad=[]
    for dp,_,fs in os.walk(B):
        for f in fs:
            b=os.path.join(dp,f); rel=os.path.relpath(b,B)
            if rel.startswith("html-chapitres") or not rel.endswith((".js",".html")) or not os.path.exists(R+rel): continue
            o=open(b,encoding="utf8").read(); nw=open(R+rel,encoding="utf8").read()
            if o==nw: continue
            if rel.endswith(".js"):
                ok=skeleton(o)==skeleton(nw)
            else:
                ok=True  # HTML : texte seul, contrôlé par balises à l'écriture
            nums=re.findall(r"\d+\.\d+",o)==re.findall(r"\d+\.\d+",nw) and len(re.findall(r"\d,\d",nw))<=len(re.findall(r"\d,\d",o))
            if not (ok and nums): bad.append(rel)
    return bad
if __name__=="__main__":
    print(bad_files())
