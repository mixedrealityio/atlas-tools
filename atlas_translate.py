import os,re,sys,json,time,glob,shutil,subprocess,threading,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor
ROOT=os.path.expanduser("~/vault/atlas_of_physics_local/atlas-of-physics.vercel.app/")
BK=os.path.expanduser("~/hermes-backup-20261026/atlas-original-en/")
LOG=os.path.expanduser("~/atlas-trad.log")
env={}
for l in open(os.path.expanduser("~/.hermes/profiles/vps/.env")):
    if "=" in l and not l.startswith("#"): k,v=l.rstrip("\n").split("=",1); env[k]=v.strip().strip('"\'')
MODELS=[("https://api.mistral.ai/v1","ministral-14b-2512",env["MISTRAL_API_KEY"]),
        ("https://api.mistral.ai/v1","ministral-14b-2512",env["MISTRAL_API_KEY"]),
        ("https://integrate.api.nvidia.com/v1","nvidia/nemotron-3-ultra-550b-a55b",env["NVIDIA_API_KEY"])]
SYS="""Tu es traducteur technique anglais → français pour un site de physique (niveau lycée/AP Physics). Tu reçois un extrait d'un fichier source (JavaScript ou HTML). Tu renvoies le MÊME extrait, avec EXACTEMENT le même nombre de lignes, où seul le texte anglais destiné à être affiché à l'utilisateur est traduit en français.
RÈGLES STRICTES :
- Ne change JAMAIS le code : identifiants, noms de variables, clés d'objets, noms de classes CSS, ids, attributs, URLs, ponctuation de code, indentation, expressions ${...} (garde-les identiques), balises HTML (garde-les identiques, y compris <i>, <sub>, <b>).
- Ne traduis PAS : les commentaires de code, les valeurs servant d'identifiants (par ex. 'ball', 'boardX', 'vec red', 'tick', 'pull', 'rain'), les noms de fichiers, les symboles et formules, les unités (m, s, N, J…).
- Traduis : les phrases et libellés visibles (corps de texte, titres, sous-titres, légendes, étiquettes, info-bulles, aria-label, title="…", textes de boutons, <title>), y compris ceux qui sont dans des conditions ternaires à l'intérieur de ${...} ou de listes.
- N'utilise JAMAIS l'apostrophe droite ' ni le guillemet droit " ni l'accent grave dans le texte traduit : utilise l'apostrophe typographique ’ (ex. : l’énergie) et les guillemets « » . Ne modifie pas les guillemets/apostrophes du code.
- Garde les nombres, les points décimaux et les symboles tels quels. Conserve les majuscules de début de phrase.
- Vocabulaire : velocity = vitesse (vecteur) ; speed = vitesse scalaire ; displacement = déplacement ; acceleration = accélération ; tip to tail = bout à bout ; free-body diagram = diagramme des forces ; torque = moment de force ; angular momentum = moment cinétique ; momentum = quantité de mouvement ; impulse = impulsion ; work = travail ; power = puissance ; capacitor = condensateur ; inductor = bobine ; field = champ ; flux = flux ; "Chapter" = Chapitre ; "AP Physics C" reste tel quel ; "Breakdown" = Décomposition ; "Click" = Cliquez ; "Drag" (geste) = Glissez.
- Ta réponse contient UNIQUEMENT l'extrait traduit, sans explication, sans balises de code markdown.
"""
lock=threading.Lock()
def log(m):
    with lock: open(LOG,"a").write(time.strftime("%H:%M:%S ")+m+"\n")
_rl={"mistral":threading.Lock(),"nvidia":threading.Lock()}; _last={"mistral":0.0,"nvidia":0.0}
GAP={"mistral":6.0,"nvidia":2.5}   # clé Mistral (30 req/min) partagée avec Hermes : ≈ 10/min ; NVIDIA ≈ 24/min
def _throttle(kind):
    with _rl[kind]:
        w=_last[kind]+GAP[kind]-time.time()
        if w>0: time.sleep(w)
        _last[kind]=time.time()
def call(model,prompt):
    base,mid,key=model
    body=json.dumps({"model":mid,"temperature":0,"max_tokens":12000,"messages":[{"role":"system","content":SYS},{"role":"user","content":prompt}]}).encode()
    for _ in range(6):
        _throttle('nvidia' if 'nvidia' in base else 'mistral')
        try:
            r=urllib.request.urlopen(urllib.request.Request(base+"/chat/completions",body,{"Authorization":"Bearer "+key,"Content-Type":"application/json"}),timeout=240)
            return json.load(r)["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(45); continue
            return None
        except Exception: time.sleep(5)
    return None
KEYS=r"(?:lit|scene|cls|key|tone|pal|cursor|kind|type|shape|id|unit)"
def protected_tokens(text):
    P=set()
    for m in re.finditer(r"'([^'\s]+)'",text):
        t=m.group(1)
        if re.search(r"[a-z][A-Z0-9]|[_\-./#\[:]|^[A-Z]{2,}$|^[a-z]+[0-9]",t): P.add(t)
    for rx in (KEYS+r":\s*'([A-Za-z]+)'", r"\b(?:asm|label|arrow|part)\(\s*(?:\w+,\s*)?'([A-Za-z]+)'"):
        for m in re.finditer(rx,text): P.add(m.group(1))
    return P
def mask_expr(s):
    return sorted(re.sub(r"'[^']*'","''",e) for e in re.findall(r"\$\{[^}]*\}",s))
def valid(old,new,PROT):
    if new is None: return "pas de réponse"
    new=re.sub(r"^```\w*\n|\n```\s*$","",new.strip("\n"))
    if len(new.split("\n"))!=len(old.split("\n")): return "nb de lignes"
    for q in ("'",'"',"`","{","}","$"):
        if old.count(q)!=new.count(q): return f"compte de {q}"
    if mask_expr(old)!=mask_expr(new): return "expressions ${}"
    tag=lambda s:re.findall(r"</?[A-Za-z][A-Za-z0-9]*",s)
    if tag(old)!=tag(new): return "balises"
    for a in ("class","id","href","src","style","viewBox","data-[a-z]+"):
        f=lambda s:re.findall(r'\b'+a+r'="[^"]*"',s)
        if f(old)!=f(new): return "attribut "+a
    if re.findall(r"\d+\.\d+",old)!=re.findall(r"\d+\.\d+",new): return "nombres décimaux"
    if len(re.findall(r"\d,\d",new))>len(re.findall(r"\d,\d",old)): return "virgule décimale"
    if re.findall(r"[=<>+*/%-]\s*\d|\d\s*[=<>+*/%]",old)!=re.findall(r"[=<>+*/%-]\s*\d|\d\s*[=<>+*/%]",new): return "opérateurs et nombres"
    tail=lambda l:re.search(r"[,;{}\[\]()]*\s*$",l).group(0).strip()
    if [tail(l) for l in old.split("\n")]!=[tail(l) for l in new.split("\n")]: return "ponctuation de fin de ligne"
    for t in PROT:
        for qq in ("'"+t+"'",'"'+t+'"'):
            if new.count(qq)<old.count(qq): return "jeton protégé "+t
    return None
def chunks(text,maxc=5500,maxl=70):
    lines=text.split("\n"); out=[]; cur=[]; n=0
    for l in lines:
        if cur and (n+len(l)>maxc or len(cur)>=maxl): out.append("\n".join(cur)); cur=[]; n=0
        cur.append(l); n+=len(l)+1
    if cur: out.append("\n".join(cur))
    return out
def fix_decimals(old,new):
    if new is None: return new
    for d in set(re.findall(r"\d+\.\d+",old)): new=new.replace(d.replace(".",","),d)
    return new
import itertools
_cnt=itertools.count()
def pick(): return MODELS[2] if next(_cnt)%3 else MODELS[0]   # 2/3 NVIDIA, 1/3 Mistral
def tr_chunk(c,PROT,model=None):
    model=model or pick()
    if not re.search(r"[A-Za-z]{3,}[ ,.][A-Za-z]{2,}",c): return c,0
    out=call(model,c)
    if out is None and model is not MODELS[0]: out=call(MODELS[0],c)
    out=fix_decimals(c,out)
    if valid(c,out,PROT) is None: return re.sub(r"^```\w*\n|\n```\s*$","",out.strip("\n")),0
    L=c.split("\n")
    if len(L)<=1: return c,1
    m=len(L)//2
    x,f1=tr_chunk("\n".join(L[:m]),PROT); y,f2=tr_chunk("\n".join(L[m:]),PROT)
    return x+"\n"+y,f1+f2
def syntax_err(rel,text):
    tmp="/tmp/_chk_"+rel.replace("/","_")+".mjs"; open(tmp,"w",encoding="utf8").write(text)
    r=subprocess.run(["node","--check",tmp],capture_output=True,text=True); os.remove(tmp)
    if r.returncode==0: return None
    m=re.search(r"\.mjs:(\d+)",r.stderr); return int(m.group(1)) if m else 0
def do_file(rel,PROT):
    p=ROOT+rel; src=open(p,encoding="utf8").read(); orig=chunks(src,3500,40)
    with ThreadPoolExecutor(6) as ex: parts=list(ex.map(lambda c:tr_chunk(c,PROT),orig))
    texts=[x for x,_ in parts]; fails=sum(f for _,f in parts); reverted=0
    if rel.endswith(".js"):
        import atlas_audit as A
        so=A.skeleton_lines(src); sn=A.skeleton_lines("\n".join(texts)); ln=0
        for i,t in enumerate(texts):
            k=len(orig[i].split("\n"))
            if so[ln:ln+k]!=sn[ln:ln+k] and t!=orig[i]: texts[i]=orig[i]; reverted+=1
            ln+=k
    if rel.endswith(".js"):
        for _ in range(12):
            new="\n".join(texts); ln=syntax_err(rel,new)
            if ln is None: break
            if ln==0: ln=1
            acc=0; hit=None
            for i,t in enumerate(texts):
                n=t.count("\n")+1
                if acc<ln<=acc+n: hit=i; break
                acc+=n
            if hit is None or texts[hit]==orig[hit]:
                # l'erreur peut venir du bloc précédent (chaîne ouverte) : on remonte d'un bloc
                hit=hit-1 if hit else None
                if hit is None or hit<0 or texts[hit]==orig[hit]: log(f"{rel}: ÉCHEC syntaxe persistant, non écrit"); return
            texts[hit]=orig[hit]; reverted+=1
        else: log(f"{rel}: ÉCHEC syntaxe, non écrit"); return
    new="\n".join(texts)
    if not os.path.exists(BK+rel):
        os.makedirs(os.path.dirname(BK+rel),exist_ok=True); shutil.copy2(p,BK+rel)
    open(p+".new","w",encoding="utf8").write(new); os.replace(p+".new",p)
    log(f"{rel}: écrit ({fails} ligne(s) et {reverted} bloc(s) laissé(s) en anglais)")
if __name__=="__main__":
    os.chdir(ROOT)
    files=[]
    for d in sorted(os.listdir(".")):
        if os.path.isdir(d) and os.path.exists(d+"/index.html") and d not in ("atlas_of_physics_full","vendor","_vercel","engine","img","complements","maths"):
            for f in ("index.html","pages.js","world.js","main.js","model.js"):
                if d=="kinematics" and f in ("pages.js","world.js","main.js"): continue
                if os.path.exists(f"{d}/{f}"): files.append(f"{d}/{f}")
    files+=["index.html","engine/xrefs.js","engine/cover.js","engine/render.js","engine/parts.js"]
    files=[f for f in files if os.path.exists(f)]
    PROT=set()
    for f in files+["engine/book.js"]: PROT|=protected_tokens(open(f,encoding="utf8").read())
    only=sys.argv[1:]
    if os.environ.get("ATLAS_ONLY_MISSING"):
        rd=lambda p:open(p,encoding="utf8").read()
        files=[f for f in files if not (os.path.exists(BK+f) and rd(BK+f)!=rd(ROOT+f))]
    if only: files=[f for f in files if f in only]
    log(f"début: {len(files)} fichiers, {len(PROT)} jetons protégés")
    with ThreadPoolExecutor(4) as ex: list(ex.map(lambda f:do_file(f,PROT),files))
    log("TERMINÉ")
