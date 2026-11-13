# Atlas de l'IA : chapitres 5 à 7 (fabrication, entraînement, apprentissage par renforcement)
eq = lambda s: f'<div class="eq">{s}</div>'
GROUPS = [("Fabriquer et entraîner un modèle", ["fabrication", "entrainement", "rl"])]
CHAPTERS = [
dict(dir="fabrication", no=5, title="Les étapes de fabrication d’un modèle", sub="des données au déploiement", cnt="Neuf étapes, de la collecte à la mise en ligne", alt="La chaîne de fabrication d’un modèle en neuf étapes",
 scenes=[
  dict(key="chaine", title="La chaîne de fabrication", sub="neuf étapes", kind="pipeline", per=3, bw=2.4, gap=0.9, y=1.4,
       stages=[dict(n="Données", s="collecter"), dict(n="Nettoyage", s="filtrer, dédupliquer"), dict(n="Tokenizer", s="vocabulaire"), dict(n="Pré-entraînement", s="prédire le jeton suivant", pal="blue"), dict(n="Mi-entraînement", s="contexte long, données ciblées", pal="blue"), dict(n="Affinage supervisé", s="SFT : imiter des exemples", pal="red"), dict(n="Préférences", s="RLHF / DPO", pal="red"), dict(n="Évaluation", s="tests, sécurité"), dict(n="Déploiement", s="quantifier, servir")],
       plate="Un modèle d’assistant naît en neuf étapes. Les trois premières préparent le texte ; le pré-entraînement donne la connaissance (c’est de loin l’étape la plus coûteuse) ; l’affinage et les préférences en font un assistant ; l’évaluation et le déploiement le rendent utilisable.",
       facts=[["pré-entraînement", "≈ 95 % du calcul"], ["affinage", "quelques milliers d’exemples à quelques millions"], ["sortie", "des poids (un fichier)"]]),
  dict(key="donnees", title="Le tri des données", sub="de l’entonnoir au corpus", kind="pipeline", per=3, bw=2.3, gap=0.9, y=1.4,
       stages=[dict(n="Web brut", s="pages, livres, code"), dict(n="Extraction", s="texte propre"), dict(n="Filtres qualité", s="langue, bruit, toxicité"), dict(n="Déduplication", s="doublons exacts et proches"), dict(n="Mélange", s="proportions par source", pal="blue"), dict(n="Corpus", s="des trillions de jetons", pal="red")],
       plate="Les données brutes sont très bruitées. On extrait le texte, on filtre (langue, qualité, contenus indésirables), on retire les doublons exacts et quasi exacts, puis on règle le mélange des sources : code, mathématiques, textes encyclopédiques, conversations.",
       facts=[["corpus d’un modèle récent", "10 à 30 trillions de jetons"], ["déduplication", "évite la mémorisation"], ["qualité", "pèse plus que la quantité"]]),
  dict(key="echelle", title="Les lois d’échelle", sub="plus de calcul, une perte plus basse", kind="curve", fn="scaling",
       plate="Quand on multiplie le calcul, la perte baisse selon une loi de puissance régulière, vers un plancher que l’on ne peut pas franchir avec ces données. Cette régularité permet de prévoir, sur de petits essais, ce que donnera un très gros entraînement.",
       facts=[["calcul total", "≈ 6 × paramètres × jetons"], ["échelle", "logarithmique en abscisse"]]),
  dict(key="post", title="Du modèle de base à l’assistant", sub="trois étapes d’alignement", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Modèle de base", s="continue un texte"), dict(n="SFT", s="suit des consignes", pal="blue"), dict(n="Préférences", s="réponses préférées", pal="blue"), dict(n="RL vérifiable", s="raisonner, coder", pal="red")],
       plate="Le modèle de base ne sait que continuer un texte. L’affinage supervisé lui apprend le format d’une conversation ; l’optimisation des préférences l’oriente vers les réponses jugées meilleures ; l’apprentissage par renforcement sur des problèmes vérifiables développe le raisonnement.",
       facts=[["modèle de base", "pas de format de dialogue"], ["modèle « instruct »", "après SFT et préférences"]]),
 ],
 pages=[
  dict(kicker="Chapitre 5 · tous niveaux", title="Les étapes de fabrication d’un modèle", sub="une chaîne, pas un seul entraînement", scene="chaine", body="""
    <p class="lede">Un assistant comme ceux que vous utilisez n’est pas le résultat d’un seul entraînement, mais d’une <b>chaîne d’étapes</b>, chacune avec ses données, son objectif et son coût.</p>
    <p>La figure en donne les neuf maillons. Le plus gros est le <b>pré-entraînement</b> : le modèle y lit des milliers de milliards de jetons et apprend à prédire le suivant. Tout le reste (affinage, préférences, évaluation) sert à orienter et à vérifier ce que cette étape a produit.</p>
    <p>Un modèle <b>à poids ouverts</b> est le résultat final de cette chaîne, publié sous la forme de ses poids : ce qu’on peut ensuite réentraîner ou régler soi-même (chapitres 4 et 6).</p>"""),
  dict(kicker="5.1", title="Les données", sub="collecter, nettoyer, mélanger", scene="donnees", body="""
    <p class="lede">La qualité d’un modèle dépend d’abord de ses données, et on en retire beaucoup plus qu’on n’en garde.</p>
    <ul class="rules">
      <li><b>Collecte</b> : pages web, livres, articles, code, conversations, données synthétiques produites par d’autres modèles.</li>
      <li><b>Filtrage</b> : langue, qualité, contenus illicites ou toxiques, informations personnelles.</li>
      <li><b>Déduplication</b> : un texte vu cent fois est mémorisé presque mot pour mot, et fausse l’évaluation.</li>
      <li><b>Mélange</b> : les proportions de code, de maths, de texte, de chaque langue décident des compétences. On les règle par des essais à petite échelle.</li>
    </ul>"""),
  dict(kicker="5.2", title="Le pré-entraînement", sub="prédire le jeton suivant, des milliers de milliards de fois", scene="echelle", body="""
    <p class="lede">Le modèle voit un texte, prédit chaque jeton à partir des précédents, et ajuste ses poids pour que la bonne réponse devienne plus probable.</p>
    <div class="eq">calcul ≈ 6 × <i>N</i> × <i>D</i> opérations</div>
    <p>avec <i>N</i> paramètres et <i>D</i> jetons. Pour 8 milliards de paramètres et 15 000 milliards de jetons : environ 7 × 10²³ opérations, de l’ordre de 500 000 heures de GPU récents, soit trois semaines sur mille GPU. Ce chiffre est un ordre de grandeur.</p>
    <p>Les <b>lois d’échelle</b> (figure) montrent que la perte baisse régulièrement avec le calcul. Le travail de 2022 sur « Chinchilla » conseillait environ 20 jetons par paramètre pour un budget donné ; les modèles récents s’entraînent bien plus longtemps, parce qu’un petit modèle très entraîné coûte moins cher à servir.</p>"""),
  dict(kicker="5.3", title="Après le pré-entraînement", sub="SFT, préférences, renforcement", scene="post", body="""
    <p class="lede">Un modèle de base ne répond pas à une question : il <b>continue un texte</b>. Trois étapes en font un assistant.</p>
    <ul class="rules">
      <li><b>SFT</b> (affinage supervisé) : on l’entraîne sur des paires consigne-réponse écrites ou validées par des humains. Il apprend le format du dialogue.</li>
      <li><b>Préférences</b> : on lui montre deux réponses, dont l’une est préférée. Avec RLHF ou DPO (chapitre 7), il apprend à produire le type de réponse préféré.</li>
      <li><b>Renforcement sur tâches vérifiables</b> : maths, code, raisonnement ; la récompense vient d’un test automatique. C’est ce qui développe les modèles de « raisonnement ».</li>
    </ul>"""),
  dict(kicker="5.4", title="Évaluer et déployer", sub="mesurer, sécuriser, servir", scene="chaine", body="""
    <p class="lede">Avant la mise en ligne, on mesure ce que le modèle sait faire, et ce qu’il ne devrait pas faire.</p>
    <ul class="rules">
      <li><b>Bancs d’essai</b> (connaissances, maths, code, raisonnement) : utiles mais sujets à la <b>contamination</b> quand les questions ont fuité dans les données d’entraînement.</li>
      <li><b>Évaluations humaines et par modèle-juge</b> : plus proches de l’usage, mais plus coûteuses et biaisées.</li>
      <li><b>Tests d’attaque</b> (<i>red teaming</i>) : chercher les contournements et les contenus dangereux.</li>
      <li><b>Déploiement</b> : quantification, choix du moteur d’inférence (chapitre 3), surveillance.</li>
    </ul>
    <p>« Poids ouverts » ne veut pas dire « logiciel libre » : la licence peut limiter l’usage, et les données d’entraînement ne sont généralement pas publiées.</p>"""),
 ],
 practice={1:[dict(q="Pourquoi supprime-t-on les doublons dans les données d’entraînement ?", choices=["pour gagner de la place sur le disque uniquement", "pour éviter que le modèle mémorise des textes et pour ne pas fausser l’évaluation", "pour augmenter la taille du vocabulaire", "parce que les doublons sont toujours faux"], answer=1, why="<p>Un texte répété est appris presque mot pour mot, et peut aussi contaminer les bancs d’essai.</p>")],
           2:[dict(q="Pour 10 milliards de paramètres et 2 000 milliards de jetons, le calcul d’entraînement vaut environ…", choices=["1,2 × 10²¹", "1,2 × 10²³", "1,2 × 10²⁵", "1,2 × 10²⁷"], answer=1, why="<p>6 × 10¹⁰ × 2 × 10¹² = 1,2 × 10²³ opérations.</p>")],
           3:[dict(q="Quelle étape apprend au modèle le format d’une conversation ?", choices=["la tokenisation", "le pré-entraînement seul", "l’affinage supervisé (SFT)", "la quantification"], answer=2, why="<p>Le SFT présente des paires consigne-réponse : le modèle apprend à répondre plutôt qu’à continuer le texte.</p>")]}
),
dict(dir="entrainement", no=6, title="Entraîner son modèle", sub="boucle, optimiseur, mémoire, LoRA", cnt="Hyperparamètres, mémoire GPU, affinage d’un modèle ouvert", alt="La boucle d’entraînement et la mémoire d’un GPU",
 scenes=[
  dict(key="boucle", title="La boucle d’entraînement", sub="six temps répétés des millions de fois", kind="cycle", unit="temps",
       nodes=[dict(n="Lot de textes"), dict(n="Passe avant", pal="blue"), dict(n="Perte", pal="red"), dict(n="Rétropropagation", pal="blue"), dict(n="Optimiseur"), dict(n="Poids à jour", pal="red")], center="une étape", speed=0.6,
       plate="À chaque étape : on lit un lot de textes, on calcule les prédictions (passe avant), on mesure l’erreur (la perte), on calcule comment chaque poids a contribué à l’erreur (rétropropagation), et l’optimiseur ajuste les poids.",
       facts=[["perte", "entropie croisée"], ["gradient", "direction qui augmente l’erreur"], ["étape", "poids −= taux × direction"]]),
  dict(key="perte", title="Le taux d’apprentissage", sub="trop faible, adapté, trop fort", kind="curve", fn="loss",
       plate="Le taux d’apprentissage règle la taille du pas. Trop faible : la perte baisse à peine. Trop fort : elle oscille ou diverge. Adapté : elle baisse vite puis se stabilise. Courbes illustratives.",
       facts=[["pré-entraînement", "≈ 10⁻⁴ à 3 × 10⁻⁴"], ["affinage complet", "≈ 10⁻⁵"], ["LoRA", "≈ 10⁻⁴"]]),
  dict(key="planning", title="Le calendrier du taux", sub="échauffement puis décroissance en cosinus", kind="curve", fn="lrsched",
       plate="On ne garde pas le taux constant : on le monte lentement au début (échauffement, pour stabiliser les premières étapes) puis on le fait redescendre en cosinus vers une petite valeur, ce qui améliore la perte finale.",
       facts=[["échauffement", "≈ 0,1 % à 2 % des étapes"], ["décroissance", "cosinus vers ≈ 10 % du pic"]]),
  dict(key="memoire", title="La mémoire pour entraîner", sub="7 milliards de paramètres, en gigaoctets", kind="mem", scale=0.045, limit=80, limitLabel="GPU 80 Go",
       configs=[dict(n="Inférence 16 bits", segs=[["Poids", 14, "blue"]]), dict(n="Entraînement complet", segs=[["Poids", 14, "blue"], ["Gradients", 14, "red"], ["Poids maîtres", 28, "dark"], ["États Adam", 56, "ink"]]), dict(n="LoRA", segs=[["Poids gelés", 14, "blue"], ["Adaptateurs + optimiseur", 0.7, "red"]]), dict(n="QLoRA", segs=[["Poids 4 bits", 4, "blue"], ["Adaptateurs + optimiseur", 0.7, "red"]])],
       info="hors activations (qui dépendent du lot et de la longueur)",
       plate="L’entraînement complet d’un modèle en précision mixte avec AdamW demande environ 16 octets par paramètre : 112 Go pour 7 milliards, avant même les activations. LoRA ne met à jour que de petits adaptateurs ; QLoRA garde en plus les poids gelés en 4 bits.",
       facts=[["poids bf16", "2 octets"], ["gradients", "2 octets"], ["poids maîtres fp32", "4 octets"], ["états Adam (m, v)", "8 octets"]]),
  dict(key="lora", title="LoRA", sub="apprendre une petite correction", kind="pipeline", per=4, bw=2.0, gap=0.7, y=1.4,
       stages=[dict(n="Entrée x", s=""), dict(n="W gelé", s="d × d, inchangé", pal="paper"), dict(n="+ B·A", s="rang r ≪ d, appris", pal="red"), dict(n="Sortie", s="W·x + (α/r)·B·A·x", pal="blue")],
       plate="Au lieu de modifier la grande matrice W, LoRA ajoute le produit de deux petites matrices B (d×r) et A (r×d). Seules A et B sont entraînées : 2·d·r nombres par matrice au lieu de d². Les adaptateurs se rangent dans un petit fichier et peuvent être fusionnés avec les poids.",
       facts=[["paramètres entraînés", "2 · d · r par matrice"], ["rang r courant", "8 à 64"], ["initialisation", "B = 0 : au départ, rien ne change"]]),
  dict(key="surapp", title="Le surapprentissage", sub="l’erreur sur les données vues et non vues", kind="curve", fn="overfit",
       plate="La perte d’entraînement continue de baisser, mais celle de validation (des textes jamais vus) remonte à partir d’un certain point : le modèle apprend les exemples par cœur. On arrête avant, ou on réduit le nombre d’époques.",
       facts=[["à surveiller", "perte de validation"], ["remèdes", "moins d’époques, plus de données, régularisation"]]),
 ],
 pages=[
  dict(kicker="Chapitre 6 · débutant à avancé", title="Entraîner son modèle", sub="la boucle, de A à Z", scene="boucle", body="""
    <p class="lede">Entraîner un modèle, c’est répéter une petite boucle des millions de fois : <b>prédire, mesurer l’erreur, corriger</b>.</p>
    <p>La mesure d’erreur est l’<b>entropie croisée</b> : −log <i>p</i>, où <i>p</i> est la probabilité que le modèle donnait au vrai jeton suivant. La <b>rétropropagation</b> calcule, pour chacun des milliards de poids, de combien l’erreur changerait s’il bougeait un peu : c’est le <b>gradient</b>. L’optimiseur déplace alors chaque poids dans le sens qui réduit l’erreur.</p>
    """),
  dict(kicker="6.1", title="Optimiseur et taux d’apprentissage", sub="AdamW, échauffement, cosinus", scene="perte", body="""
    <p class="lede">Le <b>taux d’apprentissage</b> est le réglage le plus sensible de tout l’entraînement.</p>
    <p>L’optimiseur standard est <b>AdamW</b> : il garde, pour chaque poids, une moyenne des gradients et de leurs carrés, ce qui adapte le pas à chaque poids, et applique une décroissance de poids séparée. Réglages usuels : β = (0,9 ; 0,95), décroissance de poids 0,1 en pré-entraînement.</p>
    <ul class="rules">
      <li><b>Taux</b> : de l’ordre de 10⁻⁴ pour pré-entraîner, 10⁻⁵ pour affiner tout le modèle, 10⁻⁴ pour LoRA. Plus le modèle est gros, plus le taux optimal baisse.</li>
      <li><b>Taille de lot</b> : en jetons par étape (de l’ordre de millions en pré-entraînement). Un lot plus gros donne un gradient moins bruité.</li>
      <li><b>Écrêtage du gradient</b> à 1,0 : évite qu’un lot aberrant ne casse l’entraînement.</li>
    </ul>"""),
  dict(kicker="6.2", title="Le calendrier du taux", sub="échauffer puis décroître", scene="planning", body="""
    <p class="lede">Un taux constant n’est ni stable au début ni précis à la fin.</p>
    <p>On monte donc linéairement pendant l’<b>échauffement</b> (quelques centaines à quelques milliers d’étapes), puis on décroît en <b>cosinus</b> jusqu’à environ un dixième du pic. Cela stabilise le début, quand les gradients sont encore chaotiques, et affine la fin.</p>
    <p>Quand une courbe de perte explose soudain (un « pic »), on suspecte d’abord un taux trop fort, un lot corrompu, ou une précision numérique insuffisante.</p>"""),
  dict(kicker="6.3", title="La mémoire d’entraînement", sub="16 octets par paramètre", scene="memoire", body="""
    <p class="lede">En inférence, il suffit de garder les poids. En entraînement, il faut aussi <b>tout ce dont l’optimiseur a besoin</b>.</p>
    <p>En précision mixte avec AdamW : poids en bf16 (2 octets), gradients (2), copie maîtresse en fp32 (4) et deux états Adam (8), soit <b>environ 16 octets par paramètre</b>. Pour 7 milliards de paramètres : 112 Go, plus les <b>activations</b>, qui croissent avec la taille du lot et la longueur de séquence.</p>
    <p>On les réduit avec le <b>recalcul d’activations</b> (on en oublie et on les recalcule : plus de calcul, moins de mémoire), des lots plus petits avec <b>accumulation de gradients</b>, ou en changeant de méthode : LoRA et QLoRA (page 6.5).</p>"""),
  dict(kicker="6.4", title="Plusieurs GPU", sub="découper les données, les matrices, les couches, les états", scene="boucle", body="""
    <p class="lede">Aucun GPU ne contient seul un grand modèle en entraînement : on répartit le travail.</p>
    <ul class="rules">
      <li><b>Parallélisme de données</b> : chaque GPU a une copie du modèle et traite un lot différent ; les gradients sont moyennés.</li>
      <li><b>Parallélisme de tenseurs</b> : on découpe les grandes matrices entre GPU d’une même machine.</li>
      <li><b>Parallélisme de pipeline</b> : chaque GPU porte quelques couches.</li>
      <li><b>ZeRO et FSDP</b> : on répartit aussi les gradients et les états de l’optimiseur entre les GPU, ce qui divise la mémoire par le nombre de GPU.</li>
      <li><b>Experts</b> : dans un mélange d’experts, chaque GPU porte quelques experts.</li>
    </ul>
    <p>Le coût réel vient de la <b>communication</b> entre GPU : un entraînement bien conçu l’empile derrière le calcul.</p>"""),
  dict(kicker="6.5", title="Affiner un modèle ouvert", sub="LoRA et QLoRA", scene="lora", body="""
    <p class="lede">Réentraîner entièrement un modèle de 7 milliards de paramètres demande 112 Go. <b>LoRA</b> évite cela en n’entraînant que de petites matrices ajoutées aux grandes.</p>
    <p>Au lieu de modifier la matrice <i>W</i>, on apprend deux petites matrices <i>B</i> et <i>A</i> dont le produit est la correction. Au départ <i>B</i> vaut zéro : le modèle n’a pas bougé.</p>
    <p><b>QLoRA</b> garde en plus les poids gelés en 4 bits, ce qui permet d’affiner un modèle de 7 à 14 milliards sur une carte de 16 à 24 Go. Quelques milliers d’exemples <b>de bonne qualité</b> valent mieux que des centaines de milliers d’exemples médiocres.</p>"""),
  dict(kicker="6.6", title="Les réglages de LoRA", sub="ordres de grandeur", scene="lora", body="""
    <table class="data">
      <tr><th>réglage</th><th>ordre de grandeur</th><th>effet</th></tr>
      <tr><td>rang <i>r</i></td><td>8 à 64</td><td>capacité de l’adaptateur</td></tr>
      <tr><td>α (alpha)</td><td>≈ <i>r</i> à 2<i>r</i></td><td>échelle de la correction (α/<i>r</i>)</td></tr>
      <tr><td>taux</td><td>10⁻⁴ à 2 × 10⁻⁴</td><td>trop fort : oubli ; trop faible : rien ne change</td></tr>
      <tr><td>époques</td><td>1 à 3</td><td>plus : surapprentissage</td></tr>
      <tr><td>lot effectif</td><td>16 à 128</td><td>stabilité (accumulation de gradients)</td></tr>
    </table>"""),
  dict(kicker="6.7", title="Ce qui peut mal tourner", sub="surapprentissage, oubli, évaluation", scene="surapp", body="""
    <p class="lede">Un affinage réussi sur les exemples vus peut dégrader tout le reste.</p>
    <ul class="rules">
      <li><b>Surapprentissage</b> : la perte d’entraînement baisse, celle de validation remonte (figure). Gardez un jeu de validation, jamais utilisé pour entraîner.</li>
      <li><b>Oubli catastrophique</b> : affiner sur un domaine étroit abîme les autres compétences. Mélangez des données générales, baissez le taux, ou limitez le rang.</li>
      <li><b>Format de conversation</b> : un modèle affiné avec un gabarit de dialogue différent de celui prévu répond mal. Respectez le gabarit exact du modèle.</li>
      <li><b>Évaluation</b> : comparez avant et après sur des cas que vous n’avez pas utilisés pour entraîner, et relisez des sorties.</li>
    </ul>"""),
 ],
 practice={0:[dict(q="Qu’appelle-t-on « gradient » dans l’entraînement ?", choices=["la longueur du texte lu", "pour chaque poids, la variation de l’erreur qu’il provoquerait en bougeant un peu", "le nombre de GPU utilisés", "la vitesse de génération"], answer=1, why="<p>Le gradient indique comment l’erreur varie avec chaque poids ; l’optimiseur s’en sert pour corriger.</p>")],
           2:[dict(q="Combien de mémoire, environ, pour entraîner complètement un modèle de 3 milliards de paramètres (16 octets par paramètre, hors activations) ?", choices=["6 Go", "12 Go", "48 Go", "480 Go"], answer=2, why="<p>3 × 10⁹ × 16 octets = 48 Go.</p>")],
           4:[dict(q="Dans LoRA avec une matrice W de 4 096 × 4 096 et un rang r = 16, combien de paramètres sont entraînés pour cette matrice ?", choices=["≈ 16,8 millions", "≈ 131 000", "≈ 65 000", "≈ 4 096"], answer=1, why="<p>2 · d · r = 2 × 4 096 × 16 = 131 072, contre 16,8 millions pour la matrice entière.</p>")],
           5:[dict(q="La perte de validation remonte alors que celle d’entraînement baisse encore. Il s’agit…", choices=["d’un taux trop faible", "d’un surapprentissage", "d’une quantification trop forte", "d’un bon signe"], answer=1, why="<p>Le modèle apprend les exemples par cœur et généralise moins : il faut arrêter plus tôt.</p>")]}
),
dict(dir="rl", no=7, title="L’apprentissage par renforcement", sub="récompenses, politiques, RLHF, DPO, GRPO", cnt="Comment un modèle apprend de ses propres essais", alt="Un agent qui explore une grille pour atteindre un but",
 scenes=[
  dict(key="agent", title="Agent et environnement", sub="la boucle du renforcement", kind="cycle", unit="temps", speed=0.5,
       nodes=[dict(n="Agent (politique)", pal="blue"), dict(n="Action"), dict(n="Environnement", pal="red"), dict(n="État + récompense")], center="essai et erreur",
       plate="L’agent observe l’état, choisit une action selon sa politique ; l’environnement change d’état et renvoie une récompense. L’agent n’a pas de bonne réponse à imiter : il ajuste sa politique pour que la somme des récompenses futures grandisse.",
       facts=[["objectif", "maximiser la somme des récompenses"], ["politique", "π(action | état)"]]),
  dict(key="grille", title="Un monde en grille", sub="chemin appris et chemin hasardeux", kind="grid", rows=4, cols=6, walls=[[1, 1], [1, 2], [2, 4]], goal=[0, 5], traps=[[3, 3]], goalLabel="+1",
       paths=[dict(cells=[[3, 0], [2, 0], [2, 1], [2, 2], [1, 3], [0, 3], [0, 4], [0, 5]], info="politique apprise : atteint le but en 7 pas"), dict(cells=[[3, 0], [3, 1], [3, 2], [3, 3]], info="essai au hasard : tombe dans le piège (−1)")],
       plate="Au départ, l’agent essaie au hasard et tombe dans le piège. Avec la récompense (+1 au but, −1 dans le piège), il apprend quelles actions mènent au but et finit par suivre un chemin court.",
       facts=[["but", "+1"], ["piège", "−1"], ["facteur d’actualisation γ", "0,9 à 0,99"]]),
  dict(key="rlhf", title="Renforcement pour un modèle de langage", sub="écrire, noter, corriger", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4, loop="mise à jour de la politique",
       stages=[dict(n="Invite", s="une consigne"), dict(n="Réponses", s="k essais par invite", pal="blue"), dict(n="Juge", s="préférence, test…", pal="red"), dict(n="Avantage", s="mieux que la moyenne ?"), dict(n="Mise à jour", s="poids du modèle", pal="blue"), dict(n="Garde-fou", s="rester près du modèle initial (KL)")],
       plate="Pour un modèle de langage, l’agent est le modèle, l’action est un jeton, une réponse complète est un « épisode », et la récompense vient d’un juge : un modèle de récompense appris sur des préférences humaines, ou un test automatique (code, maths).",
       facts=[["RLHF", "récompense apprise des humains"], ["RLVR", "récompense vérifiable par un test"], ["KL", "limite la dérive"]]),
  dict(key="hacking", title="Quand la récompense trompe", sub="proxy contre qualité réelle", kind="curve", fn="reward",
       plate="La récompense est un indicateur de la qualité, pas la qualité. Optimisée trop fort, la politique exploite les failles du juge : la récompense monte pendant que la qualité réelle redescend. C’est le détournement de récompense (reward hacking).",
       facts=[["remèdes", "garde-fou KL, juges variés, arrêt précoce"], ["courbes", "illustratives"]]),
 ],
 pages=[
  dict(kicker="Chapitre 7 · avancé", title="L’apprentissage par renforcement", sub="apprendre de ses essais", scene="agent", body="""
    <p class="lede">Dans l’apprentissage supervisé, on montre au modèle la bonne réponse. Dans l’<b>apprentissage par renforcement</b> (RL), on ne lui donne qu’une <b>note</b> après coup, et il doit découvrir seul quoi faire.</p>
    <p>Le cadre : un <b>agent</b> observe un <b>état</b>, choisit une <b>action</b> selon sa <b>politique</b>, l’<b>environnement</b> change et renvoie une <b>récompense</b>. Le but est de maximiser la somme des récompenses futures. C’est la méthode qui a appris à des programmes à jouer au Go et aux jeux vidéo, à des robots à marcher, et qui sert aujourd’hui à entraîner le raisonnement des modèles de langage.</p>"""),
  dict(kicker="7.1", title="Le cadre", sub="état, action, récompense, valeur", scene="grille", body="""
    <p class="lede">Un monde en grille suffit à voir toutes les notions.</p>
    <ul class="rules">
      <li>L’<b>état</b> est la case où se trouve l’agent ; l’<b>action</b> est un déplacement.</li>
      <li>La <b>récompense</b> arrive rarement : +1 au but, −1 dans un piège.</li>
      <li>Le <b>retour</b> est la somme des récompenses futures, pondérées par un <b>facteur d’actualisation</b> γ &lt; 1 : une récompense proche vaut plus qu’une lointaine.</li>
      <li>La <b>valeur</b> d’un état est le retour moyen qu’on peut en espérer en suivant la politique.</li>
      <li>Le dilemme : <b>explorer</b> des actions inconnues ou <b>exploiter</b> la meilleure connue.</li>
    </ul>"""),
  dict(kicker="7.2", title="Apprendre une politique", sub="gradient de politique, PPO", scene="agent", body="""
    <p class="lede">Le <b>gradient de politique</b> augmente la probabilité des actions qui ont mené à plus de récompense que d’habitude.</p>
    <div class="eq">∇<i>J</i> = E [ ∇ log π(<i>a</i> | <i>s</i>) × <i>A</i> ]</div>
    <p>L’<b>avantage</b> <i>A</i> compare le retour obtenu à ce qu’on attendait en moyenne : positif, on renforce l’action ; négatif, on l’affaiblit. <b>PPO</b> (2017) limite chaque mise à jour : le rapport entre la nouvelle et l’ancienne politique est borné (typiquement entre 0,8 et 1,2), ce qui évite les pas trop grands.</p>
    <p>PPO a longtemps été l’algorithme par défaut, pour les jeux comme pour le RLHF.</p>"""),
  dict(kicker="7.3", title="Le RL pour les modèles de langage", sub="RLHF, DPO, GRPO, RLVR", scene="rlhf", body="""
    <p class="lede">Pour un modèle de langage, l’action est un jeton ; la récompense tombe à la fin de la réponse.</p>
    <ul class="rules">
      <li><b>RLHF</b> : un <b>modèle de récompense</b> appris sur des comparaisons humaines, puis PPO avec un terme qui garde le modèle près de son point de départ.</li>
      <li><b>DPO</b> : sans RL ; une perte sur des paires « préférée / rejetée » règle la politique.</li>
      <li><b>GRPO</b> : on compare la note de chaque réponse à celle de son groupe ; pas de réseau de valeur.</li>
      <li><b>RLVR</b> : récompense <b>vérifiable</b> (réponse juste, tests réussis), voie des modèles de raisonnement.</li>
    </ul>"""),
  dict(kicker="7.4", title="Les pièges", sub="détournement, récompenses rares, instabilité", scene="hacking", body="""
    <p class="lede">Le RL optimise <b>exactement ce qu’on mesure</b>, y compris ses défauts.</p>
    <ul class="rules">
      <li><b>Détournement de récompense</b> : la politique exploite une faille du juge (réponses longues, flatteuses, qui trompent le modèle de récompense).</li>
      <li><b>Récompenses rares</b> : si la réussite est exceptionnelle, il n’y a presque rien à apprendre ; on commence par des tâches plus faciles.</li>
      <li><b>Effondrement de l’entropie</b> : la politique devient trop déterministe et cesse d’explorer.</li>
      <li><b>Instabilité et coût</b> : beaucoup de réponses à générer, des réglages fragiles.</li>
    </ul>
    <p>Protections : garde-fou KL, juges variés, évaluations à l’écart, arrêt anticipé.</p>"""),
 ],
 practice={0:[dict(q="Quelle différence entre l’apprentissage supervisé et le renforcement ?", choices=["le renforcement n’utilise pas de données", "en renforcement, on ne donne qu’une récompense après coup, pas la bonne réponse", "le supervisé n’utilise pas de réseau de neurones", "il n’y en a aucune"], answer=1, why="<p>Le renforcement apprend d’une note, obtenue par essai et erreur ; le supervisé imite des réponses données.</p>")],
           1:[dict(q="Avec γ = 0,9, une récompense de 1 obtenue dans 2 pas vaut aujourd’hui…", choices=["0,9", "0,81", "0,5", "2"], answer=1, why="<p>γ² = 0,9² = 0,81.</p>")],
           3:[dict(q="Que signifie RLVR ?", choices=["un renforcement avec récompense vérifiable par un test", "un renforcement sans récompense", "un réseau de neurones à vision", "une variante de la quantification"], answer=0, why="<p>La récompense vient d’un vérificateur automatique : réponse juste, tests de code réussis.</p>")]}
)]
