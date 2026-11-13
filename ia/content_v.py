# Atlas de l'IA : chapitre 78, exploiter les poids ouverts d'un modèle comme Qwen 3.8 27B (entraîner, modifier, transformer)
GROUPS = [("Voir l’IA en 3D", ["poidsouverts"])]
P = lambda q, ch, a, w: dict(q=q, choices=ch, answer=a, why=f"<p>{w}</p>")
LEG = '<p><b>Code couleur</b> : blanc = poids <b>gelés</b> (inchangés), rouge = poids <b>modifiés</b>, bleu = poids <b>ajoutés</b>, gris = retiré ou externe. La pile représente les 64 couches, par paquets de 4.</p>'
def W(key, title, sub, mode, plate, facts, cap=""):
    return dict(key=key, title=title, sub=sub, kind="openw", mode=mode, cap=cap, plate=plate, facts=facts, cam=dict(az=6, el=7))

CHAPTERS = [dict(dir="poidsouverts", no=78, title="Exploiter des poids ouverts", sub="entraîner, modifier, transformer un modèle comme Qwen 3.8 27B",
 cnt="Toutes les possibilités : de la quantification à LoRA, DPO, fusion, édition, distillation", alt="Une pile de couches où certains blocs sont modifiés, d’autres ajoutés",
 scenes=[
  dict(key="carte", title="La carte des possibilités", sub="du plus léger au plus lourd", kind="pipeline", per=4, bw=2.1, gap=0.7, y=1.4,
       stages=[dict(n="Utiliser", s="prompt, RAG, outils, réglages"), dict(n="Convertir", s="quantifier, changer de format", pal="blue"), dict(n="Adapter", s="LoRA, QLoRA", pal="blue"),
               dict(n="Réentraîner", s="affinage complet, préférences, RL", pal="red"), dict(n="Modifier sans entraîner", s="fusion, édition, pilotage", pal="red"), dict(n="Transformer", s="élaguer, distiller, nouvelle tête"),],
       plate="Avoir les poids, c’est avoir le modèle entier : on peut l’utiliser sans rien changer, le convertir, lui ajouter de petits adaptateurs, le réentraîner en partie ou en totalité, le modifier par calcul direct sur les poids, ou en faire un autre modèle (plus petit, multimodal, classifieur). Le coût en matériel croît de gauche à droite, sauf pour les modifications sans entraînement, qui sont bon marché.",
       facts=[["fichiers", "safetensors + config + tokeniseur"], ["licence", "à vérifier sur le dépôt"], ["le plus courant", "LoRA / QLoRA"]]),
  W("full", "Affinage complet", "tous les poids bougent", "full", "Tous les poids sont réentraînés (rouge) : c’est le plus puissant, et le plus cher. Il faut stocker, pour chaque poids, le poids lui-même, son gradient et l’état de l’optimiseur (Adam en garde deux) : environ 16 octets par poids en précision mixte.", [["mémoire", "~16 octets par poids"], ["27B", "~430 Go + activations"], ["risque", "oubli catastrophique"]], "tout est réentraîné"),
  W("freeze", "Geler une partie", "n’entraîner que le haut", "freeze", "On gèle les premières couches (blanc) et on n’entraîne que les dernières (rouge) et éventuellement la tête : moins de mémoire, moins de risque d’abîmer les connaissances générales, mais moins d’effet.", [["gelées", "couches basses"], ["entraînées", "couches hautes"], ["coût", "proportionnel à la part entraînée"]], "couches 49 à 64 entraînées"),
  W("lora", "LoRA", "de petites matrices ajoutées", "lora", "LoRA gèle tous les poids d’origine et ajoute, à côté de certaines matrices, deux petites matrices (bleu) dont le produit corrige la grande. Seules ces petites matrices s’entraînent : quelques dizaines à quelques centaines de millions de nombres au lieu de 27 milliards.", [["entraînés", "< 1 % des poids"], ["fichier", "adaptateur de quelques centaines de Mo"], ["après", "on le garde à part ou on le fusionne"]], "base gelée + adaptateurs"),
  W("qlora", "QLoRA", "LoRA sur une base en 4 bits", "qlora", "QLoRA charge la base gelée en 4 bits (≈ 15 à 20 Go pour 27B) et entraîne des adaptateurs LoRA en 16 bits par-dessus. C’est ce qui rend l’affinage d’un 27B possible sur un seul GPU de 24 à 48 Go, ou sur un Mac à grande mémoire unifiée (plus lentement).", [["base", "4 bits, gelée"], ["adaptateurs", "16 bits, entraînés"], ["matériel", "un GPU 24–48 Go ou un Mac"]], "base 4 bits gelée + LoRA"),
  W("pref", "Préférences et renforcement", "apprendre ce qui est mieux", "pref", "Après l’affinage supervisé, on peut apprendre au modèle à préférer certaines réponses : DPO, ORPO ou KTO à partir de paires « meilleure / moins bonne », ou du renforcement (PPO, GRPO) avec une récompense : un modèle de récompense, ou un vérificateur automatique (le code passe les tests, le calcul est juste). Ces méthodes s’utilisent en affinage complet ou avec LoRA.", [["DPO", "paires de réponses, sans récompense"], ["GRPO", "plusieurs réponses notées, on renforce les meilleures"], ["vérifiable", "maths, code, formats"]], "comportement ajusté"),
  W("distill", "Distillation", "imiter un maître", "distill", "Un modèle élève apprend à reproduire les probabilités (ou les réponses, y compris le raisonnement) d’un modèle maître plus grand. Le 27B peut être l’élève d’un modèle plus gros, ou le maître d’un modèle plus petit qui ira encore plus vite.", [["signal", "les probabilités du maître"], ["usage", "un petit modèle presque aussi bon"], ["attention", "licence des sorties du maître"]], "l’élève imite le maître"),
  W("merge", "Fusion de modèles", "additionner des poids, sans entraîner", "merge", "Deux versions affinées du même modèle de base peuvent être fusionnées par calcul sur les poids : moyenne, interpolation sphérique (SLERP), ou méthodes qui ne gardent que les changements importants (TIES, DARE, arithmétique de tâches). Quelques minutes de calcul, aucun GPU d’entraînement.", [["condition", "même modèle de base"], ["méthodes", "moyenne, SLERP, TIES, DARE"], ["outil", "mergekit"]], "A et B fusionnés"),
  W("edit", "Éditer une connaissance", "modifier quelques poids précis", "edit", "Des méthodes comme ROME ou MEMIT repèrent dans les MLP du milieu du modèle où est stocké un fait (« la capitale de X est Y ») et modifient quelques poids par un calcul direct pour le changer. Rapide, mais fragile : les effets de bord sont fréquents.", [["où", "MLP des couches du milieu"], ["méthodes", "ROME, MEMIT"], ["limite", "effets de bord, faits liés"]], "quelques MLP modifiés"),
  W("steer", "Piloter sans rien changer", "ajouter une direction au flux", "steer", "On repère une direction dans les activations (par exemple « ton formel ») en comparant des exemples, puis on l’ajoute au flux à une certaine profondeur pendant l’inférence. Aucun poids n’est modifié ; le réglage s’allume ou s’éteint à volonté.", [["poids modifiés", "aucun"], ["réglage", "force de la direction"], ["usage", "ton, style, recherche"]], "un vecteur ajouté au flux"),
  W("abl", "Retirer une direction", "l’« ablitération »", "abl", "Variante permanente : on projette les poids pour qu’ils ne puissent plus écrire une direction donnée, par exemple celle qui déclenche les refus. Technique connue, mais qui retire aussi des garde-fous : la responsabilité de l’usage revient à celui qui publie le modèle modifié.", [["poids", "projetés, pas réentraînés"], ["effet", "une direction supprimée"], ["risque", "garde-fous affaiblis"]], "une direction retirée"),
  W("prune", "Élaguer", "retirer des couches ou des experts", "prune", "On retire les couches les moins utiles (repérées en mesurant combien elles changent le flux), des neurones, ou des experts peu utilisés dans un MoE, puis on réentraîne un peu (souvent avec de la distillation) pour réparer. Le modèle devient plus petit et plus rapide.", [["retirer", "couches, neurones, experts"], ["réparer", "court réentraînement"], ["gain", "taille et vitesse"]], "3 paquets de couches retirés"),
  W("head", "Changer la tête", "un autre usage du même cerveau", "head", "On remplace la tête de sortie (qui prédit le token suivant) par une autre : une classe (classifieur), une note (modèle de récompense), ou un vecteur (modèle d’embeddings pour la recherche). Le corps du modèle est gelé ou affiné avec LoRA.", [["classifieur", "spam, sentiment, catégorie"], ["récompense", "noter des réponses"], ["embeddings", "recherche, RAG"]], "nouvelle tête"),
  W("vision", "Ajouter des sens", "images, son", "vision", "Pour qu’un modèle de texte voie, on lui branche un encodeur d’images et un petit projecteur (bleu) qui traduit l’image en vecteurs du même espace que les embeddings. On entraîne d’abord le projecteur seul, puis l’ensemble avec LoRA (méthode de type LLaVA).", [["ajouté", "encodeur + projecteur"], ["étape 1", "projecteur seul"], ["étape 2", "ensemble, souvent LoRA"]], "un encodeur branché"),
  W("vocab", "Étendre le vocabulaire", "de nouveaux tokens", "vocab", "Pour une langue, un jargon ou des balises spéciales, on ajoute des tokens au tokeniseur : il faut alors ajouter des lignes aux embeddings et à la tête (bleu), puis les entraîner.", [["ajouté", "lignes d’embeddings et de tête"], ["usage", "langue, jargon, balises d’outils"], ["coût", "court entraînement"]], "nouveaux tokens"),
  dict(key="cout", title="Ce que ça coûte en mémoire", sub="pour un 27B, ordres de grandeur", kind="qbars", sp=2.6,
       bars=[dict(n="inférence 4 bits", v=20, pal="paper", s="~20 Go"), dict(n="QLoRA", v=30, pal="blue", s="~25–35 Go"), dict(n="LoRA 16 bits", v=70, pal="blue", s="~60–80 Go"), dict(n="affinage complet", v=450, pal="red", s="~430 Go +")],
       info="hors activations : elles croissent avec la longueur des exemples et la taille des lots", max=450, h=6.0,
       plate="Ordres de grandeur pour 27 milliards de poids. Inférence en 4 bits : ~20 Go. QLoRA : la base en 4 bits plus les adaptateurs, leurs gradients et les activations, ~25 à 35 Go. LoRA sur une base en 16 bits : ~54 Go de poids plus le reste. Affinage complet : ~16 octets par poids, soit ~430 Go avant les activations, donc plusieurs GPU de 80 Go.",
       facts=[["QLoRA", "un GPU 24–48 Go"], ["LoRA 16 bits", "un GPU 80 Go"], ["complet", "plusieurs GPU 80 Go"]]),
 ],
 pages=[
  dict(kicker="Chapitre 78 · tous niveaux", title="Exploiter des poids ouverts", sub="tout ce qu’on peut faire d’un modèle qu’on possède", scene="carte", body="""
    <p class="lede">Un modèle à <b>poids ouverts</b>, comme Qwen 3.8 27B, se télécharge en entier : on a le même objet que ses créateurs, sauf les données et le code d’entraînement.</p>
    <p>Concrètement : des fichiers <i>safetensors</i> (les matrices de poids, en 16 bits), un <i>config.json</i> (64 couches, tailles, types de couches) et le tokeniseur. Avec eux, on peut :</p>
    <ul class="rules">
      <li>l’<b>utiliser</b> sans le changer, ou le <b>convertir</b> ;</li>
      <li>l’<b>adapter</b> avec de petits ajouts (LoRA) ou le <b>réentraîner</b> ;</li>
      <li>le <b>modifier par calcul</b>, sans entraînement ;</li>
      <li>le <b>transformer</b> en un autre modèle.</li>
    </ul>
    <p>Avant tout : lire la <b>licence</b> du dépôt (la plupart des Qwen sont sous Apache 2.0, qui permet l’usage commercial et la redistribution des versions modifiées).</p>"""),
  dict(kicker="78.1", title="Sans toucher aux poids", sub="utiliser, convertir", scene="carte", body="""
    <p class="lede">Beaucoup de besoins se règlent sans entraîner quoi que ce soit.</p>
    <ul class="rules">
      <li><b>Le prompt système</b> et des exemples dans la requête : le moyen le plus rapide de changer le ton ou la tâche.</li>
      <li><b>Le RAG</b> (chapitre 20) : donner au modèle vos documents au moment de la question. Préférable à l’affinage pour ajouter des <i>connaissances</i>.</li>
      <li><b>Les outils</b> (chapitre 9) et la <b>sortie structurée</b> : une grammaire ou un schéma JSON force le format de la réponse.</li>
      <li><b>Les réglages</b> d’échantillonnage (chapitre 4) et du serveur (chapitre 76).</li>
      <li><b>Quantifier, convertir</b> : vers MLX (Mac), GGUF (llama.cpp), AWQ ou GPTQ (GPU). On peut faire sa propre quantification dynamique, en mesurant sur des exemples (calibration) quelles parties sont sensibles.</li>
    </ul>
    <p>Règle utile : le RAG pour <b>savoir</b>, l’affinage pour <b>savoir-faire</b> (un style, un format, une tâche).</p>"""),
  dict(kicker="78.2", title="L’affinage complet", sub="tout réentraîner", scene="full", body="""
    <p class="lede">On reprend l’entraînement sur ses propres données, en modifiant <b>tous</b> les poids.</p>
    """ + LEG + """
    <p>Le plus puissant, mais le plus coûteux : environ <b>16 octets par poids</b> (poids, gradients, état de l’optimiseur), soit ~430 Go pour 27 milliards, plus les activations. Il faut plusieurs GPU de 80 Go et des outils de répartition (FSDP, DeepSpeed).</p>
    <p>Risque principal : l’<b>oubli catastrophique</b>. Entraîné trop fort sur une seule tâche, le modèle perd des capacités générales. On mélange donc ses données avec des données générales et on garde un taux d’apprentissage faible.</p>"""),
  dict(kicker="78.3", title="Geler une partie", sub="n’entraîner que le haut du modèle", scene="freeze", body="""
    <p class="lede">Compromis simple : on <b>gèle</b> les couches basses (le « socle » : syntaxe, connaissances générales) et on n’entraîne que les couches hautes et la tête.</p>
    <p>Moins de mémoire (pas de gradients ni d’optimiseur pour les couches gelées), moins de risque d’oubli. Moins d’effet aussi : c’est surtout utile quand la tâche ressemble déjà à ce que le modèle sait faire. Aujourd’hui, LoRA a largement remplacé cette méthode.</p>"""),
  dict(kicker="78.4", title="LoRA", sub="adapter avec de petites matrices", scene="lora", body="""
    <p class="lede"><b>LoRA</b> (<i>low-rank adaptation</i>) gèle le modèle et ajoute à côté de chaque grande matrice choisie deux petites matrices A et B.</p>
    <div class="eq">W′ = W + B·A</div>
    <p>Si W fait 5 000 × 5 000, A et B font 5 000 × <i>r</i> avec un <b>rang</b> <i>r</i> de 8 à 64 : on entraîne moins de 1 % des nombres. Le résultat est un <b>adaptateur</b> de quelques centaines de Mo, qu’on peut :</p>
    <ul class="rules">
      <li>charger à part, en changer selon la tâche, en servir plusieurs avec la même base ;</li>
      <li>ou <b>fusionner</b> dans les poids (W′ calculé une fois), puis requantifier.</li>
    </ul>
    <p>Variantes : DoRA, rsLoRA, et des méthodes encore plus légères (adaptation par préfixe, IA³).</p>"""),
  dict(kicker="78.5", title="QLoRA", sub="affiner un 27B sur une seule machine", scene="qlora", body="""
    <p class="lede"><b>QLoRA</b> = la base gelée en <b>4 bits</b> + des adaptateurs LoRA en 16 bits.</p>
    <p>Pour un 27B : ~15 à 20 Go de base, plus les adaptateurs, leurs gradients et les activations. Cela tient sur un GPU de 24 à 48 Go, ou sur un Mac à grande mémoire unifiée avec <b>mlx-lm</b> (son module LoRA travaille directement sur un modèle MLX quantifié, plus lentement qu’un GPU).</p>
    <p>Pour un modèle hybride comme celui-ci (couches GDN), vérifier que la bibliothèque d’entraînement gère ce type de couche : il faut des noyaux de calcul dédiés et une version récente.</p>"""),
  dict(kicker="78.6", title="Quelles données, quel objectif", sub="ce qu’on apprend au modèle", scene="pref", body="""
    <table class="data">
      <tr><th>méthode</th><th>données</th><th>pour</th></tr>
      <tr><td>pré-entraînement continu</td><td>texte brut du domaine</td><td>un vocabulaire, un domaine (droit, médecine)</td></tr>
      <tr><td>affinage supervisé (SFT)</td><td>paires question → bonne réponse</td><td>un format, un style, une tâche</td></tr>
      <tr><td>DPO, ORPO, KTO</td><td>paires meilleure / moins bonne</td><td>préférences, ton, sécurité</td></tr>
      <tr><td>RL (PPO, GRPO)</td><td>une récompense ou un vérificateur</td><td>raisonnement, code, maths, agents</td></tr>
    </table>
    <p>Ordre classique : SFT, puis préférences ou renforcement. Quelques centaines d’exemples bien choisis suffisent souvent pour un style ; il en faut bien plus pour une compétence nouvelle. Pour un modèle à raisonnement, garder ou désactiver la phase de réflexion dans les exemples selon l’usage visé.</p>"""),
  dict(kicker="78.7", title="La distillation", sub="apprendre d’un maître", scene="distill", body="""
    <p class="lede">L’élève apprend à reproduire les <b>probabilités</b> du maître sur chaque token, un signal bien plus riche qu’une seule bonne réponse.</p>
    <ul class="rules">
      <li><b>Vers le bas</b> : le 27B sert de maître à un modèle de 1 à 8 milliards, plus rapide, pour une tâche précise.</li>
      <li><b>Vers le haut</b> : le 27B apprend des réponses (ou des raisonnements) d’un modèle plus grand. Vérifier la licence : certains fournisseurs interdisent d’entraîner un modèle sur leurs sorties.</li>
      <li><b>Un brouillon</b> : on peut entraîner une petite tête ou un petit modèle de devinette (comme la tête MTP du chapitre 76) pour accélérer le décodage spéculatif.</li>
    </ul>"""),
  dict(kicker="78.8", title="Fusionner des modèles", sub="additionner, sans entraîner", scene="merge", body="""
    <p class="lede">Deux versions affinées du <b>même modèle de base</b> peuvent être fusionnées par simple calcul sur leurs poids.</p>
    <ul class="rules">
      <li><b>Moyenne</b> ou <b>SLERP</b> : interpoler entre deux modèles.</li>
      <li><b>Arithmétique de tâches</b> : (affiné − base) est un « vecteur de tâche » qu’on peut ajouter, soustraire, doser.</li>
      <li><b>TIES</b>, <b>DARE</b> : ne garder que les changements importants et résoudre les conflits de signe.</li>
    </ul>
    <p>L’outil courant est <b>mergekit</b> ; quelques minutes sur un ordinateur ordinaire. Résultats imprévisibles : toujours évaluer.</p>"""),
  dict(kicker="78.9", title="Modifier sans entraîner", sub="éditer, piloter, retirer", scene="edit", body="""
    <p class="lede">Les poids sont des nombres : on peut les changer par calcul direct, à partir de ce que l’interprétabilité (chapitre 30) a appris.</p>
    <ul class="rules">
      <li><b>Éditer un fait</b> (ROME, MEMIT) : modifier quelques poids des MLP du milieu pour changer une association précise.</li>
      <li><b>Piloter</b> : ajouter un vecteur de direction au flux pendant l’inférence (style, ton) ; aucun poids touché (figure suivante).</li>
      <li><b>Retirer une direction</b> (« ablitération ») : projeter les poids pour supprimer une direction, souvent celle du refus. Cela affaiblit les garde-fous : celui qui publie le modèle modifié en porte la responsabilité.</li>
      <li><b>Analyser</b> : autoencodeurs parcimonieux, sondes, <i>logit lens</i>, pour comprendre avant de modifier.</li>
    </ul>"""),
  dict(kicker="78.10", title="Piloter par une direction", sub="un vecteur ajouté au flux", scene="steer", body="""
    <p class="lede">On fait passer des exemples « formels » et « familiers », on prend la différence moyenne de leurs activations à une couche : c’est la <b>direction</b> du ton.</p>
    <p>À l’inférence, on ajoute cette direction (multipliée par une force) au flux à la même profondeur. Le modèle répond plus formellement, sans aucun entraînement. La même technique sert en recherche pour tester ce qu’une direction représente.</p>"""),
  dict(kicker="78.11", title="Transformer le modèle", sub="élaguer, nouvelle tête, nouveaux sens", scene="prune", body="""
    <ul class="rules">
      <li><b>Élaguer</b> (figure) : retirer des couches peu utiles, des neurones ou, dans un MoE (chapitre 77), des experts rarement choisis ; puis réparer par un court entraînement.</li>
      <li><b>Nouvelle tête</b> : classifieur, modèle de récompense, modèle d’embeddings.</li>
      <li><b>Nouveaux sens</b> : brancher un encodeur d’images ou de son.</li>
      <li><b>Nouveau vocabulaire</b> : ajouter des tokens.</li>
      <li><b>Contexte plus long</b> : étendre l’encodage des positions des couches d’attention (méthodes de type YaRN), puis entraîner sur de longs textes.</li>
    </ul>"""),
  dict(kicker="78.12", title="Changer la tête", sub="classer, noter, chercher", scene="head", body="""
    <p class="lede">Le corps du modèle produit, pour chaque texte, un vecteur riche. La tête décide de ce qu’on en fait.</p>
    <p>En remplaçant la tête de sortie par une petite couche qui donne une <b>classe</b>, une <b>note</b> ou un <b>vecteur</b>, on obtient un classifieur, un modèle de récompense (utile pour le renforcement de la page 78.6) ou un modèle d’embeddings pour le RAG. On entraîne la nouvelle tête, et souvent le corps avec LoRA.</p>"""),
  dict(kicker="78.13", title="Ajouter des sens", sub="un modèle de texte qui voit", scene="vision", body="""
    <p class="lede">Un encodeur d’images transforme une image en vecteurs ; un petit <b>projecteur</b> les traduit dans l’espace des embeddings du modèle.</p>
    <ol class="rules">
      <li>On entraîne le projecteur seul, sur des paires image → légende.</li>
      <li>On affine l’ensemble (souvent avec LoRA) sur des questions sur des images.</li>
    </ol>
    <p>Même principe pour le son. Si une version multimodale officielle existe, mieux vaut partir d’elle.</p>"""),
  dict(kicker="78.14", title="Étendre le vocabulaire", sub="de nouveaux tokens", scene="vocab", body="""
    <p class="lede">Ajouter des tokens au tokeniseur (balises d’un outil, mots d’une langue rare) impose d’ajouter autant de lignes aux <b>embeddings</b> et à la <b>tête de sortie</b>.</p>
    <p>Les nouvelles lignes sont initialisées (par exemple par la moyenne des tokens qui composaient le mot) puis entraînées. Avec ~250 000 tokens, le vocabulaire de Qwen couvre déjà beaucoup de langues : c’est rarement nécessaire.</p>"""),
  dict(kicker="78.15", title="Le coût et les outils", sub="mémoire, bibliothèques", scene="cout", body="""
    <table class="data">
      <tr><th>outil</th><th>pour</th></tr>
      <tr><td>transformers, PEFT, TRL</td><td>la base : charger, LoRA, SFT, DPO, GRPO</td></tr>
      <tr><td>Unsloth, Axolotl, LLaMA-Factory</td><td>affinage prêt à l’emploi, économe en mémoire</td></tr>
      <tr><td>torchtune, DeepSpeed, FSDP</td><td>gros entraînements sur plusieurs GPU</td></tr>
      <tr><td>mlx-lm</td><td>LoRA et conversion sur Mac</td></tr>
      <tr><td>mergekit</td><td>fusion de modèles</td></tr>
      <tr><td>llama.cpp</td><td>conversion GGUF, quantification</td></tr>
      <tr><td>lm-evaluation-harness</td><td>mesurer avant / après</td></tr>
    </table>"""),
  dict(kicker="78.16", title="Évaluer, publier, choisir", sub="la boucle complète", scene="carte", body="""
    <p class="lede">Toute modification se juge à la mesure : bancs d’essai généraux (pour détecter l’oubli), tests de votre tâche, et comparaison à l’original (divergence KL, accord sur le mot suivant, comme au chapitre 76).</p>
    <table class="data">
      <tr><th>besoin</th><th>méthode</th></tr>
      <tr><td>connaître mes documents</td><td>RAG, pas d’entraînement</td></tr>
      <tr><td>un style, un format</td><td>QLoRA + SFT, quelques centaines d’exemples</td></tr>
      <tr><td>mieux raisonner sur un domaine vérifiable</td><td>LoRA + GRPO</td></tr>
      <tr><td>combiner deux versions</td><td>fusion</td></tr>
      <tr><td>plus petit, plus rapide</td><td>distillation, élagage, quantification</td></tr>
      <tr><td>classer, noter, chercher</td><td>nouvelle tête</td></tr>
    </table>
    <p>Pour publier : fusionner ou fournir l’adaptateur, requantifier (MLX, GGUF), décrire les données et les changements, respecter la licence d’origine.</p>"""),
 ],
 practice={
  1: [P("Vous voulez que le modèle connaisse vos documents internes, mis à jour chaque semaine. Que choisir ?", ["un affinage complet chaque semaine", "le RAG", "l’ablitération", "élaguer le modèle"], 1, "Le RAG apporte les connaissances au moment de la question ; l’affinage sert plutôt au savoir-faire.")],
  4: [P("Que contient un adaptateur LoRA ?", ["une copie complète du modèle", "deux petites matrices par matrice adaptée", "un nouveau tokeniseur", "les données d’entraînement"], 1, "W′ = W + B·A : seules A et B sont entraînées et stockées.")],
  5: [P("Pourquoi QLoRA permet-il d’affiner un 27B sur un seul GPU de 24 à 48 Go ?", ["la base gelée est chargée en 4 bits", "il n’entraîne rien", "il supprime la moitié des couches", "il n’utilise pas de gradients"], 0, "~15 à 20 Go de base en 4 bits, plus de petits adaptateurs en 16 bits.")],
  8: [P("Quelle condition faut-il pour fusionner deux modèles ?", ["qu’ils aient la même licence uniquement", "qu’ils viennent du même modèle de base", "qu’ils soient en 4 bits", "aucune"], 1, "Les poids doivent correspondre un à un : même architecture, même point de départ.")],
 }),
]
