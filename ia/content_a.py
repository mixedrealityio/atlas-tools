# Atlas de l'IA : chapitres 1 à 4 (modèles de langage). Balisage HTML libre dans les corps de page.
eq = lambda s: f'<div class="eq">{s}</div>'
LOGITS = [6.0, 3.2, 2.6, 2.2, 1.9, 1.6, 1.2, 0.8]
WORDS = ["Paris", "la", "une", "Lyon", "située", "le", "en", "Marseille"]
BAR = dict(kind="bars", labels=WORDS, logits=LOGITS, cam=dict(dx=0, y=2.2, dist=19, az=6, el=7, radius=4.5))

GROUPS = [("Les modèles de langage", ["texte", "attention", "inference", "echantillonnage"])]
CHAPTERS = [dict(
  dir="echantillonnage", no=4, title="Les réglages d’inférence", sub="température, top-k, top-p, min-p, pénalités",
  cnt="Pour un modèle à poids ouverts : tout se règle", alt="Des barres de probabilité sur les mots suivants possibles",
  scenes=[
    dict(key="temp", title="La température", sub="aplatir ou durcir la distribution", mode="temp",
         plate="Le modèle produit un score (logit) par mot possible. La température divise ces scores avant le softmax : T petit durcit la distribution (le mot le plus probable écrase les autres), T grand l’aplatit.",
         facts=[["entrée", "8 scores (logits)"], ["formule", "p = softmax(z / T)"], ["T → 0", "choix du plus probable"]], **BAR),
    dict(key="topk", title="Le top-k", sub="ne garder que les k meilleurs mots", mode="topk",
         plate="Top-k garde les k mots les plus probables, met les autres à zéro puis renormalise. Le nombre de candidats est fixe, quelle que soit la forme de la distribution.",
         facts=[["k = 1", "décodage glouton"], ["k grand", "presque aucun effet"]], **BAR),
    dict(key="topp", title="Le top-p (noyau)", sub="le plus petit ensemble qui atteint la probabilité p", mode="topp",
         plate="Top-p garde les mots les plus probables jusqu’à ce que leur probabilité cumulée atteigne p. Le nombre de candidats s’adapte : peu quand le modèle est sûr, beaucoup quand il hésite.",
         facts=[["p = 1", "aucun filtre"], ["valeurs courantes", "0,9 à 0,95"]], **BAR),
    dict(key="minp", title="Le min-p", sub="un seuil relatif au meilleur mot", mode="minp",
         plate="Min-p écarte tout mot dont la probabilité est inférieure à min_p fois celle du meilleur mot. Le seuil suit la confiance du modèle : strict quand il est sûr, souple quand il hésite.",
         facts=[["seuil", "min_p × p(meilleur)"], ["valeurs courantes", "0,02 à 0,1"]], **BAR),
    dict(key="penalty", title="La pénalité de répétition", sub="décourager les mots déjà écrits", mode="penalty", seen=[0],
         plate="La pénalité de répétition affaiblit le score des mots déjà présents dans le texte. Trop forte, elle empêche de répéter un nom propre ou un terme technique, même quand il le faudrait.",
         facts=[["effet", "z / r si z > 0 ; z × r sinon"], ["r = 1", "aucune pénalité"]], **BAR),
    dict(key="chain", title="La chaîne d’échantillonnage", sub="les réglages s’appliquent dans un ordre", kind="pipeline", per=3, bw=2.1, gap=0.9,
         stages=[dict(n="Logits", s="scores bruts", pal="paper"), dict(n="Pénalités", s="répétition…"), dict(n="Température", s="÷ T"), dict(n="top-k", s="garder k"), dict(n="top-p / min-p", s="filtrer"), dict(n="Tirage", s="avec la graine", pal="red")],
         plate="Un moteur d’inférence applique ses réglages en chaîne. L’ordre compte : filtrer avant ou après la température ne donne pas le même résultat, et chaque moteur a son ordre par défaut.",
         facts=[["à vérifier", "l’ordre dans votre moteur"], ["graine", "même graine = même texte"]], cam=dict(dx=0, y=1.9, dist=24, az=6, el=8, radius=7)),
  ],
  pages=[
   dict(kicker="Chapitre 4 · tous niveaux", title="Les réglages d’inférence", sub="ce que vous contrôlez vraiment", scene="temp", body=f"""
     <p class="lede">À chaque mot, un modèle ne « choisit » rien : il calcule un score pour chaque mot de son vocabulaire (des dizaines de milliers). Ce sont <b>les réglages d’échantillonnage</b> qui transforment ces scores en un mot.</p>
     <p>Avec un modèle <b>à poids ouverts</b>, vous les réglez tous, et vous voyez les scores. Avec une API, certains sont fixés ou cachés. Le même modèle peut ainsi sembler prudent, créatif ou délirant, sans qu’aucun de ses poids ne change.</p>
     <p>La figure montre huit mots possibles après « La capitale de la France est ». Les barres sont les probabilités ; la barre rouge est le mot tiré à cet instant.</p>"""),
   dict(kicker="4.1", title="La température", sub="aplatir ou durcir", scene="temp", body=f"""
     <p class="lede">La <b>température</b> <i>T</i> divise les scores avant le softmax.</p>
     {eq("<i>p</i><sub>i</sub> = e<sup>z<sub>i</sub>/T</sup> / Σ<sub>j</sub> e<sup>z<sub>j</sub>/T</sup>")}
     <p>À <i>T</i> = 1, on garde les probabilités du modèle. Quand <i>T</i> descend vers 0, le mot le plus probable absorbe presque toute la probabilité : c’est le <b>décodage glouton</b>, déterministe. Quand <i>T</i> monte, la distribution s’aplatit et les mots improbables deviennent possibles.</p>
     <p>Ordres de grandeur : 0 à 0,3 pour du code ou de l’extraction, 0,7 à 1 pour de la rédaction. Au-delà de 1,2 le texte devient vite incohérent.</p>"""),
   dict(kicker="4.2", title="Top-k et top-p", sub="couper la queue de la distribution", scene="topk", body=f"""
     <p class="lede">La température garde tous les mots, même absurdes. Les <b>filtres</b> les écartent.</p>
     <p><b>Top-k</b> garde les <i>k</i> mots les plus probables. Simple, mais le nombre de candidats ne s’adapte pas : <i>k</i> = 40 est trop large quand le modèle est sûr de lui, et peut être trop étroit quand il hésite.</p>
     <p><b>Top-p</b> (échantillonnage par noyau) garde le plus petit ensemble de mots dont la probabilité cumulée atteint <i>p</i>. Il s’élargit quand le modèle hésite et se resserre quand il est sûr. Valeurs courantes : <i>p</i> = 0,9 à 0,95.</p>
     <p class="hintline">Page suivante : le top-p en mouvement.</p>"""),
   dict(kicker="4.3", title="Le noyau (top-p)", sub="un nombre de candidats qui s’adapte", scene="topp", body=f"""
     <p class="lede">Regardez le nombre de barres bleues quand <i>p</i> varie : il change, et il change aussi d’une distribution à l’autre.</p>
     <p>Après le filtre, les probabilités restantes sont <b>renormalisées</b> pour que leur somme vaille 1, puis un mot est tiré au hasard. À <i>p</i> = 1, aucun filtre ; à <i>p</i> très petit, un seul mot : on retombe sur le glouton.</p>
     <p>Top-k et top-p se combinent : on applique d’abord l’un, puis l’autre, et un mot doit passer les deux.</p>"""),
   dict(kicker="4.4", title="Min-p", sub="un seuil qui suit la confiance du modèle", scene="minp", body=f"""
     <p class="lede"><b>Min-p</b> écarte les mots dont la probabilité est inférieure à <i>min_p</i> fois celle du meilleur mot.</p>
     <p>Si le meilleur mot a 80 % et <i>min_p</i> = 0,1, le seuil est 8 % : presque tout est coupé. S’il n’a que 20 %, le seuil tombe à 2 % et beaucoup de mots restent. Le filtre est donc strict quand le modèle est sûr et souple quand il hésite, ce qui marche bien à température élevée.</p>
     <p>Valeurs courantes : 0,02 à 0,1. Le réglage existe dans les moteurs à poids ouverts les plus répandus, mais pas dans toutes les API.</p>"""),
   dict(kicker="4.5", title="Pénalités de répétition", sub="éviter de tourner en rond", scene="penalty", body=f"""
     <p class="lede">Un petit modèle ou une température basse peuvent boucler : « et puis et puis et puis… ».</p>
     <p>La <b>pénalité de répétition</b> divise le score des mots déjà présents (multiplie s’il est négatif). Les <b>pénalités de présence et de fréquence</b> soustraient un montant fixe, ou proportionnel au nombre d’occurrences.</p>
     <p>Piège : trop forte, la pénalité interdit de répéter un nom propre, un identifiant de code ou un mot de la question. Commencez à 1,05 à 1,15, et pas plus sans raison.</p>"""),
   dict(kicker="4.6", title="Tous les autres réglages", sub="longueur, arrêt, graine, contexte", scene="chain", body=f"""
     <p class="lede">Les réglages s’appliquent <b>en chaîne</b>. L’ordre dépend du moteur : vérifiez-le dans le vôtre.</p>
     <ul class="rules">
       <li><b>max_tokens</b> : borne la longueur de la réponse (et le coût). Trop bas, le texte est coupé net.</li>
       <li><b>stop</b> : chaînes qui arrêtent la génération (utile pour des formats structurés).</li>
       <li><b>seed</b> : fixe le tirage ; même graine et mêmes réglages donnent souvent le même texte, mais pas toujours sur des machines différentes.</li>
       <li><b>logit_bias, grammaires</b> : interdire ou imposer des mots, ou contraindre la sortie à un format (JSON, grammaire).</li>
       <li><b>fenêtre de contexte</b> : le nombre de jetons que le modèle peut lire ; au-delà, il faut résumer ou chercher.</li>
     </ul>"""),
  ],
  practice={0:[dict(q="Une température de 0 revient à…", choices=["tirer au hasard parmi tous les mots", "toujours choisir le mot le plus probable", "ignorer le contexte", "doubler la longueur de la réponse"], answer=1,
                     why="<p>À T → 0, la distribution se concentre sur le mot dont le score est maximal : c’est le décodage glouton.</p>")],
            1:[dict(q="Quel réglage aplatit la distribution de probabilités ?", choices=["baisser la température", "monter la température", "baisser top-p", "monter la pénalité de répétition"], answer=1,
                     why="<p>Diviser les scores par un T plus grand les rapproche les uns des autres : les mots improbables gagnent des chances.</p>")],
            2:[dict(q="Un modèle est très sûr de lui : un mot a 95 % de probabilité. Avec top-p = 0,9, combien de mots reste-t-il ?", choices=["1", "9", "tout le vocabulaire", "aucun"], answer=0,
                     why="<p>Le mot le plus probable seul atteint 95 % ≥ 90 % : l’ensemble minimal n’a qu’un mot. Top-p s’adapte, contrairement à top-k.</p>")],
            4:[dict(q="Pourquoi une pénalité de répétition trop forte pose-t-elle problème ?", choices=["elle ralentit le GPU", "elle empêche de répéter des mots nécessaires (noms propres, code)", "elle fait grandir le contexte", "elle désactive la température"], answer=1,
                     why="<p>Elle abaisse le score de tout mot déjà écrit, y compris ceux qu’il faut précisément reprendre.</p>")]}
)]
