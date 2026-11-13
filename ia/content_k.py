# Atlas de l'IA : chapitre 38, le simulateur de LLM local (paramétrable), avec le service à l'échelle
import json, html
GROUPS = [("Paramétrer et dimensionner", ["simulateur"])]
P = lambda q, ch, a, w: dict(q=q, choices=ch, answer=a, why=f"<p>{w}</p>")
MODELS = [("m8", "8 Md (dense)"), ("m14", "14 Md (dense)"), ("m32", "32 Md (dense)"), ("m70", "70 Md (dense)"), ("mx", "47 Md en 8 experts (13 Md actifs)"), ("q235", "235 Md en experts (22 Md actifs)"), ("m405", "405 Md (dense)")]
WQ = [("fp16", "FP16 / BF16 (16 bits)"), ("q8", "Q8_0 (≈ 8,5 bits)"), ("q6", "Q6_K (≈ 6,6)"), ("q5", "Q5_K_M (≈ 5,7)"), ("q4", "Q4_K_M (≈ 4,85)"), ("q3", "Q3_K_M (≈ 3,9)"), ("q2", "Q2_K (≈ 3,35)")]
KQ = [("kv16", "FP16"), ("kv8", "Q8"), ("kv4", "Q4")]
HW = [("cpu", "PC sans GPU (DDR5)"), ("g3060", "RTX 3060 12 Go"), ("g3090", "RTX 3090 24 Go"), ("g4090", "RTX 4090 24 Go"), ("g5090", "RTX 5090 32 Go"), ("m4max", "Mac M4 Max 128 Go (≈ 96 utilisables)"), ("m3u", "Mac M3 Ultra 512 Go (≈ 448)"), ("halo", "PC à mémoire unifiée 128 Go (≈ 96)"), ("spark", "Mini-station 128 Go unifiée"), ("a100", "A100 80 Go"), ("h100", "H100 80 Go"), ("h200", "H200 141 Go"), ("custom", "personnalisé")]
def sel(key, lab, opts): return f'<label>{lab}<select data-sim="{key}">' + "".join(f'<option value="{k}">{v}</option>' for k, v in opts) + '</select></label>'
def rng(key, lab, lo, hi, step=1, log=False): return f'<label>{lab} : <b data-out="{key}"></b><input type="range" data-sim="{key}" min="{lo}" max="{hi}" step="{step}"' + (' data-log="1"' if log else '') + '></label>'
def out(*pairs): return '<div class="simout">' + "".join(f'<span>{a}</span><span data-out="{k}"></span>' for a, k in pairs) + '</div>'
def ctl(*c): return '<div class="simctl">' + "".join(c) + '</div>'
def btn(lab, d): return f'<button type="button" data-simset="{html.escape(json.dumps(d), quote=True)}">{lab}</button>'
SCEN = [
 ("8 Md Q4 sur RTX 4090", dict(model="m8", wq="q4", kq="kv16", ctx=4096, gen=256, batch=1, hw="g4090", ngpu=1)),
 ("70 Md Q4 sur RTX 4090 (déborde en RAM)", dict(model="m70", wq="q4", kq="kv16", ctx=4096, gen=256, batch=1, hw="g4090", ngpu=1)),
 ("70 Md Q4 sur Mac M4 Max", dict(model="m70", wq="q4", kq="kv16", ctx=8192, gen=256, batch=1, hw="m4max", ngpu=1)),
 ("32 Md Q4, contexte 32 k, RTX 3090", dict(model="m32", wq="q4", kq="kv8", ctx=32768, gen=256, batch=1, hw="g3090", ngpu=1)),
 ("235 Md en experts, Q4, Mac M3 Ultra", dict(model="q235", wq="q4", kq="kv16", ctx=8192, gen=256, batch=1, hw="m3u", ngpu=1)),
 ("70 Md FP16, 2× H100, 16 requêtes", dict(model="m70", wq="fp16", kq="kv16", ctx=2048, gen=256, batch=16, hw="h100", ngpu=2)),
 ("8 Md Q4 sur PC sans GPU", dict(model="m8", wq="q4", kq="kv16", ctx=4096, gen=256, batch=1, hw="cpu", ngpu=1)),
]
def pipe(key, title, sub, stages, plate, facts, per=3, bw=2.3, gap=0.8):
    return dict(key=key, title=title, sub=sub, kind="pipeline", per=per, bw=bw, gap=gap, y=1.4, stages=[dict(n=a, s=b, **({"pal": c} if c else {})) for a, b, c in stages], plate=plate, facts=facts)

CHAPTERS = [dict(dir="simulateur", no=38, title="Simulateur de LLM local", sub="un modèle en 3D : requête, inférence, mémoire, débit", cnt="Réglez le modèle, la quantification, le contexte et le matériel, et voyez le débit", alt="Un grand modèle en 3D avec son cache KV, sa mémoire et son débit",
 scenes=[dict(key="sim", title="Le simulateur", sub="modifiez les réglages dans la page de gauche", kind="llmsim",
   plate="Le modèle est une pile de tranches de couches : leur largeur croît avec la taille des poids en Go (la quantification l’amincit), bleu = en mémoire GPU, clair = déporté en RAM. Les barres rouges à droite de chaque tranche sont le cache KV, qui grandit pendant la génération. La mémoire GPU et la RAM sont les deux barres de droite ; les deux dernières barres comparent le temps de lecture mémoire et le temps de calcul pour un jeton : la plus haute est le facteur limitant. Valeurs estimées par un modèle simple (roofline) à partir de fiches techniques arrondies : ordres de grandeur.",
   facts=[["limite en génération", "bande passante mémoire"], ["limite au préremplissage", "calcul"], ["précision", "ordre de grandeur, ±30 %"]]),
  pipe("serving", "Servir à l’échelle", "ce que font vLLM et ses semblables", [("File de requêtes", "arrivées au fil de l’eau", None), ("Lot continu", "ajouter et retirer des requêtes à chaque pas", "blue"), ("Cache paginé", "KV découpé en blocs (PagedAttention)", "blue"), ("Préfixe partagé", "réutiliser un prompt commun", "blue"), ("Décodage spéculatif", "un petit modèle propose, le grand valide", "red"), ("Résultat", "plus de débit pour le même GPU", None)],
   "Un moteur de service ne traite pas les requêtes une à une : il regroupe en continu celles en cours (lot continu), range le cache KV en blocs pour limiter le gaspillage (PagedAttention), réutilise un préfixe de prompt commun et peut accélérer la génération avec un petit modèle qui propose des jetons validés par le grand. Ces optimisations ne sont pas simulées ici.",
   [["lot continu", "pas de file d’attente figée"], ["spéculatif", "gain typique 1,5 à 3 fois"], ["non simulé", "ici : un modèle simple"]])],
 pages=[
  dict(kicker="Chapitre 38 · simulateur", title="Simulateur de LLM local", sub="réglez, regardez, comparez", scene="sim", body="""
    <p class="lede">Un grand modèle en 3D : une requête entre, le préremplissage traverse les couches, puis chaque jeton de la réponse est calculé un par un.</p>
    <p>Les réglages des pages suivantes agissent tous sur la même figure. Ou essayez un scénario :</p>
    <div class="simbtns">""" + "".join(btn(a, b) for a, b in SCEN) + """</div>
    """ + out(("génération", "tpsSeq"), ("mémoire", "fit"), ("premier jeton", "ttft"))),
  dict(kicker="38.1", title="Le modèle", sub="taille, couches, têtes KV", scene="sim", body="""
    <p class="lede">La taille fixe la mémoire à lire à chaque jeton ; les couches et les têtes KV fixent la taille du cache.</p>
    """ + ctl(sel("model", "modèle", MODELS)) + out(("paramètres", "params"), ("profondeur", "layers"), ("cache KV", "heads"), ("poids", "W")) + """
    <p>Pour un modèle <b>à experts</b>, seuls quelques experts travaillent par jeton : la lecture est plus faible, mais toute la mémoire reste nécessaire (chapitre 27).</p>"""),
  dict(kicker="38.2", title="La quantification", sub="moins de bits, moins de mémoire", scene="sim", body="""
    <p class="lede">Chaque poids passe de 16 bits à 4 ou 5 : le modèle est environ 3,3 fois plus petit, donc se lit environ 3,3 fois plus vite.</p>
    """ + ctl(sel("wq", "poids", WQ), sel("kq", "cache KV", KQ)) + out(("poids", "W"), ("bits", "bits"), ("cache KV", "kv"), ("mémoire", "memuse")) + """
    <p>Perte de qualité : faible à Q8, modérée à Q4, nette sous Q3 selon le modèle et la tâche. Quantifier le cache KV libère de la mémoire pour du contexte, avec un petit coût en précision.</p>"""),
  dict(kicker="38.3", title="La requête", sub="contexte, longueur de réponse, requêtes parallèles", scene="sim", body="""
    <p class="lede">Chaque jeton de contexte laisse en mémoire 2 × couches × têtes KV × dimension × bits d’octets.</p>
    """ + ctl(rng("ctx", "contexte", 7, 17, 0.5, True), rng("gen", "réponse", 16, 2048, 16), rng("batch", "requêtes simultanées", 1, 64, 1)) + out(("cache KV", "kv"), ("contexte max", "ctxMax")) + """
    <p>Doubler le contexte ou les requêtes double le cache KV.</p>"""),
  dict(kicker="38.4", title="Le matériel", sub="mémoire, bande passante, calcul", scene="sim", body="""
    <p class="lede">Trois nombres décident : la <b>mémoire</b> (ce qui tient), la <b>bande passante</b> (la vitesse de génération), les <b>TFLOPS</b> (le préremplissage).</p>
    """ + ctl(sel("hw", "matériel", HW), rng("mem", "mémoire GPU", 0, 512, 4), rng("bw", "bande passante", 0, 5000, 10), rng("tf", "calcul", 1, 1000, 1)) + out(("mémoire", "memuse"), ("ajustement", "fit")) + """
    <p>Valeurs de fiches techniques arrondies : à vérifier pour votre machine.</p>"""),
  dict(kicker="38.5", title="Déborder en RAM, multiplier les GPU", sub="le précipice de la mémoire", scene="sim", body="""
    <p class="lede">Si le modèle ne tient pas en mémoire GPU, une partie reste en RAM, bien plus lente : le débit s’effondre.</p>
    """ + ctl(rng("ngpu", "nombre de GPU", 1, 8, 1), rng("ram", "RAM système", 0, 512, 8), rng("rambw", "bande passante RAM", 10, 200, 5)) + out(("génération", "tpsSeq"), ("mémoire", "fit")) + """
    <p>Plusieurs GPU additionnent mémoire et bande passante (≈ 7 % de perte par GPU ajouté).</p>"""),
  dict(kicker="38.6", title="Le débit en génération", sub="octets lus ÷ bande passante", scene="sim", body="""
    <div class="eq">jetons/s ≈ bande passante × efficacité ÷ octets lus par jeton</div>
    <p>Chaque jeton relit les poids actifs et le cache KV. Avec plusieurs requêtes, les poids sont lus une fois pour le lot : le débit total monte jusqu’à ce que le calcul limite.</p>
    """ + ctl(rng("batch", "requêtes simultanées", 1, 64, 1), rng("eff", "efficacité du moteur", 40, 95, 5)) + out(("par requête", "tpsSeq"), ("total", "tpsTot"), ("limite", "bound"))),
  dict(kicker="38.7", title="Le temps avant le premier jeton", sub="le préremplissage", scene="sim", body="""
    <p class="lede">Le prompt est traité d’un coup : c’est limité par le <b>calcul</b>, pas par la mémoire.</p>
    """ + ctl(rng("ctx", "contexte", 7, 17, 0.5, True)) + out(("premier jeton", "ttft"), ("préremplissage", "pre"), ("réponse complète", "latency")) + """
    <p>L’attention croît comme le carré du contexte (chapitre 27).</p>"""),
  dict(kicker="38.8", title="Servir à l’échelle", sub="lot continu, cache paginé, décodage spéculatif", scene="serving", body="""
    <ul class="rules">
      <li><b>Lot continu</b> : ajouter et retirer des requêtes à chaque pas pour garder le GPU plein.</li>
      <li><b>PagedAttention</b> : le cache KV en blocs, comme la mémoire virtuelle, pour limiter le gaspillage.</li>
      <li><b>Préfixe partagé</b> : ne pas recalculer un prompt système commun.</li>
      <li><b>Décodage spéculatif</b> : un petit modèle propose plusieurs jetons, le grand les valide d’un coup.</li>
    </ul>
    <p>Ils améliorent le débit réel au-delà de ce que le simulateur affiche.</p>"""),
  dict(kicker="38.9", title="Limites du simulateur", sub="ce qui n’est pas modélisé", scene="sim", body="""
    <ul class="rules">
      <li>Un modèle <b>roofline</b> simple : en vrai, ±30 % selon moteur, noyaux et version.</li>
      <li>Non pris en compte : températures, bridage, FlashAttention précise, placement des experts, latences réseau.</li>
      <li>Les modèles et valeurs matérielles sont des <b>approximations</b> des fiches publiques.</li>
      <li>La <b>qualité</b> des réponses n’est pas simulée : seul le débit l’est.</li>
    </ul>
    <p>Pour mesurer pour de vrai : <code>llama-bench</code> ou le banc de votre moteur d’inférence.</p>"""),
 ],
 practice={2:[P("Quantifier un modèle de 16 à environ 4,85 bits par poids le rend…", ["environ 3,3 fois plus petit et plus rapide à lire", "plus gros", "inchangé", "dix fois plus rapide"], 0, "16 / 4,85 ≈ 3,3 : moins d’octets à stocker et à relire à chaque jeton.")],
   3:[P("Qu’est-ce qui fait croître le cache KV ?", ["le contexte, la réponse et le nombre de requêtes", "uniquement la taille du vocabulaire", "la couleur du GPU", "le nombre de GPU"], 0, "Il est proportionnel au nombre total de jetons gardés en mémoire.")],
   5:[P("Que se passe-t-il quand le modèle ne tient pas en mémoire GPU ?", ["le débit chute car une partie est lue depuis la RAM, plus lente", "il va plus vite", "rien", "le modèle devient plus petit"], 0, "La bande passante de la RAM est beaucoup plus basse que celle de la mémoire GPU.")],
   6:[P("En génération à une seule requête, qu’est-ce qui limite le plus souvent la vitesse ?", ["la bande passante mémoire", "la fréquence de l’écran", "le nombre de jetons du prompt", "le tokenizer"], 0, "Chaque jeton relit tous les poids actifs : octets lus ÷ bande passante.")],
   7:[P("Pourquoi le préremplissage est-il plutôt limité par le calcul ?", ["tous les jetons du prompt sont traités ensemble", "il n’utilise pas le GPU", "il lit la RAM", "il est sans poids"], 0, "Beaucoup de calcul pour une seule lecture des poids.")]}
)]
