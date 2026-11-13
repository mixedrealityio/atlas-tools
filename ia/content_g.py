# Atlas de l'IA : chapitres 23 et 24 (agent conversationnel pour robot, limites et IA hybride)
GROUPS = [("Aller plus loin", ["agentlocal", "limites"])]
CHAPTERS = [
dict(dir="agentlocal", no=23, title="Un agent conversationnel pour un robot", sub="entendre, voir, se souvenir, raisonner, s’exprimer", cnt="Entraîner et faire tourner son IA locale, avec mémoire et émotions simulées", alt="L’architecture d’un robot qui dialogue avec mémoire et état émotionnel",
 scenes=[
  dict(key="archi", title="L’architecture d’ensemble", sub="une boucle de dialogue et d’action", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4, loop="boucle de dialogue",
       stages=[dict(n="Micro, caméra", s="signaux bruts"), dict(n="Perception", s="parole, scène, sons", pal="blue"), dict(n="Mémoire", s="rappeler, enregistrer", pal="blue"), dict(n="Raisonnement", s="le modèle de langage", pal="red"), dict(n="État affectif", s="humeur simulée", pal="blue"), dict(n="Expression", s="voix, gestes, regard"), dict(n="Actions", s="API du robot, sous contrôle", pal="red"), dict(n="Capteurs", s="résultat observé")],
       plate="Un agent pour robot enchaîne perception, mémoire, raisonnement par un modèle de langage, un état affectif qui règle la manière de s’exprimer, puis l’expression et les actions, sous une couche de sécurité. Les capteurs ferment la boucle.",
       facts=[["entrée", "voix, images, capteurs"], ["sortie", "parole, gestes, actions"], ["garde-fou", "couche de sécurité indépendante"]]),
  dict(key="memoire", title="Quatre mémoires", sub="le modèle seul n’en a aucune", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Court terme", s="le contexte en cours", pal="blue"), dict(n="Épisodique", s="journal des échanges", pal="red"), dict(n="Sémantique", s="faits, préférences", pal="red"), dict(n="Procédurale", s="savoir-faire, compétences", pal="blue")],
       plate="Un modèle ne se souvient de rien d’une conversation à l’autre. On construit donc la mémoire autour de lui : le contexte pour l’instant, un journal consultable pour les épisodes, une base de faits et de préférences, et une bibliothèque de compétences que le robot sait exécuter.",
       facts=[["où ça vit", "hors des poids du modèle"], ["accès", "recherche, comme un RAG"], ["données personnelles", "consentement et effacement"]]),
  dict(key="affect", title="L’état affectif", sub="valence et activation", kind="scatter", by=2.4,
       points=[dict(n="neutre", x=0, y=0), dict(n="joie", x=2.6, y=1.2, c="red"), dict(n="enthousiasme", x=1.4, y=2.5, c="red"), dict(n="colère", x=-2.4, y=2.3, c="blue"), dict(n="peur", x=-2.9, y=1.2, c="blue"), dict(n="tristesse", x=-2.6, y=-1.7, c="blue"), dict(n="ennui", x=-0.6, y=-2.5), dict(n="calme", x=2.4, y=-1.8, c="red")],
       arrows=[["neutre", "joie", "plus agréable"], ["neutre", "colère", "plus tendu"]], walk=["neutre", "joie", "enthousiasme", "calme", "tristesse", "ennui"], info="x : agréable → désagréable · y : calme → activé",
       plate="Un modèle simple d’émotion place l’état du robot sur deux axes : la valence (agréable ou non) et l’activation (calme ou excité). Les événements déplacent ce point, qui règle ensuite le ton, le rythme de la voix et les gestes. C’est un réglage de comportement, pas un ressenti.",
       facts=[["axes", "valence × activation"], ["effet", "ton, rythme, gestes"], ["nature", "simulation, pas ressenti"]], cam=dict(az=2, el=4)),
  dict(key="creatif", title="La boucle créative", sub="diverger, critiquer, converger", kind="cycle", unit="temps", speed=0.5,
       nodes=[dict(n="Générer plusieurs idées", pal="blue"), dict(n="Critiquer", pal="red"), dict(n="Combiner"), dict(n="Choisir")], center="créer, c’est trier",
       plate="La créativité d’un système vient d’une boucle : produire beaucoup d’idées variées (température plus haute), les critiquer avec des critères explicites, combiner les meilleures, choisir. Le tri compte autant que la variété.",
       facts=[["variété", "température, top-p, plusieurs tirages"], ["tri", "critères, juge, humain"]]),
  dict(key="entrainement", title="La recette d’entraînement", sub="huit étapes, du modèle de base au robot", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4, loop="amélioration continue",
       stages=[dict(n="Modèle ouvert de base", s="7 à 14 milliards", pal="blue"), dict(n="Données", s="dialogues, appels d’outils"), dict(n="SFT (LoRA)", s="persona, format", pal="blue"), dict(n="Préférences (DPO)", s="ton, concision, prudence", pal="blue"), dict(n="Évaluation", s="scénarios et sécurité", pal="red"), dict(n="Quantification", s="4 bits"), dict(n="Déploiement", s="module embarqué", pal="red"), dict(n="Journaux", s="avec consentement")],
       plate="On part d’un modèle ouvert, on l’affine avec LoRA sur des dialogues et des appels d’outils, on règle le ton par préférences, on évalue sur des scénarios (dont la sécurité), on quantifie et on déploie. La mémoire et les émotions ne s’entraînent pas dans les poids : elles s’ingénient autour.",
       facts=[["entraîné", "style, format, appels d’outils"], ["pas entraîné", "mémoire, état affectif"], ["matériel", "une carte de 24 Go suffit avec QLoRA"]]),
  dict(key="embarque", title="Tout sur un module embarqué", sub="mémoire d’un module de 16 Go", kind="mem", scale=0.2, limit=16, limitLabel="module de 16 Go",
       configs=[dict(n="Agent local", segs=[["Modèle de langage 8B, 4 bits", 4.9, "blue"], ["Vision-langage 2B", 2.2, "red"], ["Parole (reconnaissance + voix)", 1.5, "dark"], ["Cache KV", 1.0, "paper"], ["Système et marge", 3, "ink"]])],
       info="ordres de grandeur ; dépend des modèles choisis",
       plate="Un robot ne peut pas compter sur le cloud pour chaque mot. Sur un module embarqué de 16 Go, on fait tenir un modèle de langage de 8 milliards en 4 bits, un petit modèle de vision, la reconnaissance et la synthèse vocales, un cache et de la marge.",
       facts=[["total ici", "≈ 12,6 Go sur 16"], ["latence visée", "premier son en moins d’une seconde"]], cam=dict(az=4, el=4)),
 ],
 pages=[
  dict(kicker="Chapitre 23 · avancé", title="Un agent conversationnel pour un robot", sub="rassembler les briques de l’atlas", scene="archi", body="""
    <p class="lede">Un robot qui dialogue réunit presque tout cet atlas : un modèle de langage (chapitres 1 à 4), un entraînement local (6), de la perception (8), des outils et une boucle (9 à 11), un corps (12).</p>
    <p>Ce chapitre décrit comment les assembler en un <b>agent local</b>, qui tourne sur la machine du robot, avec une <b>mémoire</b>, un <b>raisonnement</b>, un état <b>affectif simulé</b> et un peu de <b>créativité</b>, et comment l’<b>entraîner</b>.</p>"""),
  dict(kicker="23.1", title="Entendre et voir", sub="la perception multimodale", scene="archi", body="""
    <ul class="rules">
      <li><b>Parole</b> : détection de la voix, reconnaissance en flux, identification de qui parle ; un modèle de reconnaissance de la famille Whisper tourne en local.</li>
      <li><b>Vision</b> : un modèle vision-langage (chapitre 8) décrit la scène et répond aux questions sur l’image : « qu’est-ce qui est sur la table ? »</li>
      <li><b>Sons et capteurs</b> : bruit de porte, chute, distance aux obstacles ; transformés en événements textuels que le modèle comprend.</li>
      <li><b>Fusion</b> : tout est converti en un court « rapport de situation » mis dans le contexte à chaque tour.</li>
    </ul>"""),
  dict(kicker="23.2", title="Se souvenir", sub="une mémoire construite autour du modèle", scene="memoire", body="""
    <p class="lede">Le modèle n’a pas de mémoire propre : on la construit en quatre morceaux.</p>
    <ul class="rules">
      <li><b>Court terme</b> : le contexte de la conversation.</li>
      <li><b>Épisodique</b> : un journal des échanges résumés, retrouvés par recherche (chapitre 20).</li>
      <li><b>Sémantique</b> : faits stables et préférences (« Léa n’aime pas le bruit »).</li>
      <li><b>Procédurale</b> : les compétences que le robot sait déclencher.</li>
    </ul>
    <p>Il faut aussi <b>oublier</b> : résumer, supprimer, et laisser la personne effacer ce qu’on a retenu d’elle.</p>"""),
  dict(kicker="23.3", title="Raisonner et agir", sub="le modèle décide, le robot exécute sous contrôle", scene="archi", body="""
    <p class="lede">Le modèle de langage sert de <b>planificateur</b> : il lit la situation et la mémoire, et choisit une action parmi celles que le robot sait faire.</p>
    <p>Les actions passent par des <b>appels d’outils</b> (chapitre 9) : avancer de deux mètres, saisir un objet, dire une phrase. Une <b>couche de sécurité indépendante du modèle</b> vérifie chaque ordre (vitesse, zone, force) avant de l’envoyer aux moteurs.</p>
    <p>Deux vitesses : la <b>réflexion lente</b> du modèle (secondes) et les <b>réflexes rapides</b> du robot (équilibre, évitement, arrêt d’urgence), qui ne l’attendent pas.</p>"""),
  dict(kicker="23.4", title="Des émotions simulées", sub="un état qui règle l’expression", scene="affect", body="""
    <p class="lede">Un robot qui répond toujours du même ton paraît mécanique. On lui donne un <b>état affectif</b> : un point sur deux axes, valence et activation.</p>
    <p>Des événements le déplacent (un compliment, un bruit fort, une longue absence) et il revient doucement vers le calme. Cet état est donné au modèle (« tu es plutôt détendu et content ») et règle la voix, le rythme et les gestes.</p>
    <p><b>Mise en garde</b> : c’est une simulation de comportement, pas un ressenti. Elle doit rester <b>honnête</b> : le robot ne prétend pas souffrir, et n’exploite pas l’attachement de la personne.</p>"""),
  dict(kicker="23.5", title="La créativité", sub="diversité plus tri", scene="creatif", body="""
    <p class="lede">Un modèle « créatif » se fabrique à deux niveaux.</p>
    <ul class="rules">
      <li><b>Diversité</b> : température et top-p plus élevés (chapitre 4), plusieurs tirages, consignes d’exploration.</li>
      <li><b>Tri</b> : des critères explicites (original, adapté à l’enfant, faisable avec ce que le robot a sous la main), un modèle critique, ou la personne.</li>
    </ul>
    <p>Un robot qui invente une histoire, un jeu ou une danse produit dix versions, en retient une, et demande « ça te plaît ? ». L’avis reçu devient une préférence en mémoire.</p>"""),
  dict(kicker="23.6", title="L’entraîner", sub="ce qu’on entraîne, ce qu’on construit", scene="entrainement", body="""
    <p class="lede">On entraîne ce qui se prête à l’entraînement : le <b>style</b>, le <b>format</b> des appels d’outils, la <b>prudence</b>.</p>
    <ol class="rules">
      <li>Partir d’un modèle ouvert de 7 à 14 milliards de paramètres.</li>
      <li>Rassembler des exemples : dialogues dans le ton voulu, appels d’outils justes, refus appropriés.</li>
      <li>Affiner avec LoRA ou QLoRA (chapitre 6), puis régler le ton par préférences.</li>
      <li>Évaluer sur des scénarios réalistes, <b>dont la sécurité</b> (chapitre 22).</li>
      <li>Quantifier et mesurer la latence sur le module du robot.</li>
    </ol>
    <p>La mémoire et l’état affectif ne s’entraînent pas : ce sont des composants logiciels.</p>"""),
  dict(kicker="23.7", title="Le faire tourner sur le robot", sub="mémoire, latence, secours", scene="embarque", body="""
    <p class="lede">Un module embarqué de 16 Go doit contenir <b>tout</b> : langage, vision, parole, cache.</p>
    <p>Ordres de grandeur : modèle de langage de 8 milliards en 4 bits ≈ 5 Go, petit modèle de vision ≈ 2 Go, parole ≈ 1,5 Go, cache ≈ 1 Go, système et marge ≈ 3 Go. Le but est un <b>premier son en moins d’une seconde</b> (chapitre 20).</p>
    <p>Prévoir un <b>mode dégradé</b> : si le gros modèle est trop lent ou plante, le robot répond avec un petit modèle ou des phrases préparées, et ses réflexes de sécurité continuent de fonctionner.</p>"""),
 ],
 practice={2:[dict(q="Pourquoi ajoute-t-on une couche de sécurité indépendante du modèle ?", choices=["pour accélérer la voix", "parce que le modèle peut se tromper et que chaque ordre doit être vérifié avant les moteurs", "pour réduire la mémoire", "pour remplacer la perception"], answer=1, why="<p>Le modèle propose ; une vérification déterministe (vitesse, zone, force) décide ce qui est exécuté.</p>")],
           4:[dict(q="Qu’est-ce qu’on entraîne vraiment dans les poids d’un tel agent ?", choices=["le style, le format d’outils et la prudence", "la mémoire de chaque personne", "l’état émotionnel à chaque seconde", "le micro"], answer=0, why="<p>La mémoire et l’état affectif sont des composants logiciels, hors des poids.</p>")],
           5:[dict(q="Quatre mémoires d’un agent : court terme, épisodique, sémantique et…", choices=["procédurale", "magnétique", "thermique", "optique"], answer=0, why="<p>La mémoire procédurale regroupe les compétences que l’agent sait exécuter.</p>")]}
),
dict(dir="limites", no=24, title="Les limites de l’IA et l’IA hybride", sub="monde physique, calcul, cellules vivantes, robots quadrupèdes", cnt="Ce que les modèles ne savent pas faire, et d’autres voies", alt="Un réseau de cellules vivantes sur des électrodes et un robot quadrupède",
 scenes=[
  dict(key="limites", title="Six limites des modèles de langage", sub="ce qu’ils font mal ou pas du tout", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Calcul exact", s="sans outil, des erreurs", pal="red"), dict(n="Faits fiables", s="inventent parfois", pal="red"), dict(n="Causalité", s="corrélation ≠ cause"), dict(n="Planification longue", s="les erreurs s’accumulent"), dict(n="Mémoire durable", s="aucune en propre"), dict(n="Corps", s="pas de monde physique", pal="blue")],
       plate="Un modèle de langage prédit du texte plausible. Il calcule mal sans outil, peut inventer des faits, confond corrélation et cause, perd le fil des longues chaînes d’actions, n’a pas de mémoire propre, et n’a jamais touché ni déplacé un objet.",
       facts=[["remèdes partiels", "outils, recherche, boucles, vérificateurs"], ["pas résolu", "le monde physique"]]),
  dict(key="genie", title="Prédire des mondes à la force du calcul", sub="le cas de Genie", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4, loop="image suivante",
       stages=[dict(n="Image + action", s="« avance », « tourne »"), dict(n="Modèle autorégressif", s="génère l’image suivante", pal="blue"), dict(n="Historique", s="la trajectoire grandit à chaque image", pal="red"), dict(n="24 images/s", s="en temps réel"), dict(n="Calcul massif", s="matériel de centre de données", pal="red"), dict(n="Cohérence", s="quelques minutes, pas plus", pal="blue")],
       plate="Des modèles comme Genie génèrent des mondes interactifs image par image, en tenant compte de tout ce qui s’est passé avant. À 24 images par seconde en 720p, la cohérence ne tient que quelques minutes et le calcul est considérable : le modèle apprend la physique en regardant des vidéos, à grand frais.",
       facts=[["Genie 3", "720p, 24 images/s, cohérence de quelques minutes"], ["coût", "croît avec l’historique"], ["déploiement", "centre de données"]]),
  dict(key="approches", title="Calculer moins", sub="six pistes pour comprendre le monde à moindre coût", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Prédire en latent", s="JEPA : l’abstrait, pas les pixels", pal="blue"), dict(n="Simulateur + correction", s="la physique connue, le reste appris", pal="blue"), dict(n="Modèles creux", s="experts : peu de poids actifs"), dict(n="Capteurs événementiels", s="ne voir que ce qui change"), dict(n="Apprendre en agissant", s="interaction plutôt que vidéos", pal="red"), dict(n="Calculer à la demande", s="plus de calcul si le cas est dur")],
       plate="Plutôt que de prédire chaque pixel, on peut prédire des représentations abstraites, combiner un simulateur physique et un modèle qui apprend ses écarts, n’activer qu’une fraction du modèle, ne traiter que ce qui change dans l’image, et apprendre par l’interaction. Aucune n’a encore remplacé la force brute.",
       facts=[["idée commune", "mettre de la connaissance dans la structure"], ["état", "recherche"]]),
  dict(key="energie", title="Cerveau et machines", sub="la puissance électrique, en watts", kind="logbars", unit="W", axis="échelle logarithmique, ordres de grandeur",
       items=[dict(n="Cerveau humain", v=20, pal="red"), dict(n="GPU H100", v=700, pal="blue"), dict(n="Serveur 8 GPU", v=10000, pal="blue"), dict(n="10 000 GPU", v=14000000, pal="dark")],
       plate="Un cerveau humain, environ 86 milliards de neurones, consomme de l’ordre de 20 W. Un GPU de centre de données en consomme 700, un serveur de huit GPU une dizaine de milliers, un cluster de dix mille GPU plusieurs mégawatts. La comparaison est approximative (les tâches diffèrent) mais l’écart est énorme.",
       facts=[["cerveau", "≈ 20 W"], ["GPU H100", "≈ 700 W"], ["cluster de 10 000 GPU", "≈ 10 MW ou plus"]]),
  dict(key="culture", title="Des cellules sur des électrodes", sub="biocalcul : lire et stimuler des neurones cultivés", kind="mea",
       plate="Des neurones cultivés sont posés sur un réseau d’électrodes. On stimule certaines électrodes (entrée) et on lit l’activité des autres (sortie). Des équipes ont montré qu’ils pouvaient s’adapter : environ 800 000 cellules ont appris à jouer à Pong en quelques minutes dans l’expérience DishBrain.",
       facts=[["DishBrain (2022)", "≈ 800 000 cellules, Pong"], ["organoïdes FinalSpark", "≈ 10 000 neurones chacun ; durée de vie ≈ 100 jours"], ["énergie annoncée", "très inférieure : estimations, non démontrée"]]),
  dict(key="hybride", title="Un modèle hybride", sub="du vivant, du silicium, un robot", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4, loop="retour sensoriel",
       stages=[dict(n="Cellules cultivées", s="support de vie, nutriments", pal="red"), dict(n="Électrodes", s="lire et stimuler", pal="blue"), dict(n="Puce d’interface", s="signaux ↔ numérique", pal="blue"), dict(n="Logiciel", s="apprentissage, décodage"), dict(n="Robot", s="mouvements, capteurs", pal="red"), dict(n="Capteurs", s="renvoient des signaux")],
       plate="Dans un système hybride, des cellules cultivées sont reliées par électrodes à une puce, qui convertit leurs signaux en commandes pour un robot, et les signaux des capteurs en stimulations. En 2024, une équipe chinoise (système MetaBOC) a présenté un organoïde cérébral sur puce pilotant un robot pour éviter des obstacles et saisir un objet.",
       facts=[["MetaBOC", "Tianjin Univ. et SUSTech, 2024"], ["limites", "maturité, nutriments, durée de vie"], ["échelle", "loin d’un GPU"]]),
  dict(key="chien", title="Un robot quadrupède", sub="perception, équilibre, marche", kind="quad",
       plate="Un robot quadrupède marche en alternant ses pattes en diagonale. Il combine caméras et LiDAR (voir), centrale inertielle (sentir l’équilibre), capteurs de force dans les pieds (sentir le sol) et des politiques de marche apprises en simulation puis ajustées sur le robot.",
       facts=[["marche", "trot : pattes en diagonale"], ["capteurs", "caméras, LiDAR, IMU, force"], ["autonomie", "quelques heures de batterie"]], cam=dict(az=12, el=8)),
 ],
 pages=[
  dict(kicker="Chapitre 24 · avancé", title="Les limites de l’IA et l’IA hybride", sub="ce que les modèles ne savent pas faire", scene="limites", body="""
    <p class="lede">Les modèles de langage impressionnent, mais ils ont des limites précises. Les connaître permet d’éviter des erreurs coûteuses et de repérer les pistes de recherche.</p>
    <p>Ce chapitre en dresse la liste, puis se concentre sur la plus profonde : la <b>compréhension du monde physique</b>. Il montre ce que coûte de la compenser par la <b>force brute</b> (Genie), comment on pourrait <b>calculer moins</b>, et ce que l’on peut attendre de systèmes <b>hybrides</b> utilisant des cellules vivantes, jusqu’aux robots quadrupèdes.</p>"""),
  dict(kicker="24.1", title="Ce que les LLM ne font pas bien", sub="six limites", scene="limites", body="""
    <ul class="rules">
      <li><b>Calcul exact</b> : ils prédisent des chiffres plausibles ; avec un outil de calcul, le problème disparaît.</li>
      <li><b>Faits</b> : ils peuvent inventer avec aplomb (hallucination) ; la recherche et les sources aident (chapitre 20).</li>
      <li><b>Causalité</b> : ils savent ce qui va avec quoi, pas toujours ce qui provoque quoi.</li>
      <li><b>Planification longue</b> : les erreurs s’accumulent (chapitre 10).</li>
      <li><b>Mémoire</b> : aucune en propre ; il faut la construire autour (chapitre 23).</li>
      <li><b>Corps</b> : ils n’ont jamais poussé un objet : leur physique vient de textes.</li>
    </ul>"""),
  dict(kicker="24.2", title="Le monde physique", sub="la limite la plus profonde", scene="limites", body="""
    <p class="lede">Un enfant de deux ans sait qu’un objet lâché tombe, qu’un verre peut se renverser, qu’une porte s’ouvre dans un sens. Il l’a appris en <b>agissant</b>.</p>
    <p>Un modèle de langage a lu des millions de descriptions de la physique, mais ne l’a pas éprouvée : il se trompe sur les contacts, les frottements, la stabilité, les quantités, les trajectoires. Le texte ne contient presque pas ce savoir implicite, trop évident pour être écrit.</p>
    <p>Les modèles du monde (chapitre 13) et la robotique (chapitre 12) tentent de combler ce vide, mais ils achètent cette compréhension au prix fort.</p>"""),
  dict(kicker="24.3", title="La force brute : le cas de Genie", sub="apprendre la physique en regardant des vidéos", scene="genie", body="""
    <p class="lede">Des modèles comme <b>Genie</b> (DeepMind) génèrent des mondes interactifs : on donne une image ou un texte, on appuie sur des touches, le modèle produit l’image suivante.</p>
    <p>Pour Genie 3, annoncé en 2025, on parle d’une résolution de 720p, de 24 images par seconde, et d’une cohérence qui tient quelques minutes. Chaque image doit tenir compte de toute la trajectoire précédente, qui grandit : le calcul est considérable, et le déploiement se fait en centre de données.</p>
    <p>Le modèle semble « comprendre » l’eau et la lumière, mais cette compréhension est <b>statistique</b>, apprise par des quantités énormes de vidéos, et elle se dégrade avec le temps.</p>"""),
  dict(kicker="24.4", title="Calculer moins", sub="d’autres façons de comprendre le monde", scene="approches", body="""
    <p class="lede">Prédire chaque pixel est ruineux. D’autres approches cherchent à mettre davantage de <b>structure</b> dans le modèle.</p>
    <ul class="rules">
      <li><b>Prédire l’abstrait</b> (JEPA) : ne pas deviner les détails imprévisibles.</li>
      <li><b>Simulateur + correction apprise</b> : la physique connue est calculée, seul l’écart est appris.</li>
      <li><b>Modèles creux</b> : n’activer qu’une partie des paramètres à chaque pas.</li>
      <li><b>Capteurs événementiels</b> : ne traiter que ce qui bouge.</li>
      <li><b>Apprendre en agissant</b>, dans un corps ou un simulateur, plutôt que par des millions d’heures de vidéo.</li>
    </ul>
    <p>Ces pistes sont étudiées ; aucune n’a, à ce jour, détrôné l’échelle.</p>"""),
  dict(kicker="24.5", title="Le cerveau comme repère", sub="20 watts", scene="energie", body="""
    <p class="lede">Un cerveau humain, d’environ 86 milliards de neurones, consomme de l’ordre de <b>20 W</b>, et apprend avec peu d’exemples.</p>
    <p>Un GPU de centre de données consomme 700 W, un serveur de huit GPU environ 10 kW, et un cluster d’entraînement des mégawatts. La comparaison est approximative (le cerveau ne fait pas la même chose), mais l’écart de plusieurs ordres de grandeur explique l’intérêt pour les approches inspirées du vivant.</p>
    <p>Les puces <b>neuromorphiques</b> imitent ses impulsions électriques, et le <b>biocalcul</b> va plus loin : il utilise de vraies cellules.</p>"""),
  dict(kicker="24.6", title="Cellules vivantes et IA hybride", sub="de DishBrain à MetaBOC", scene="culture", body="""
    <p class="lede">Des neurones cultivés sur des électrodes peuvent être stimulés et lus. En 2022, <b>DishBrain</b> (Cortical Labs) a montré qu’environ 800 000 cellules apprenaient à jouer à Pong en quelques minutes.</p>
    <p><b>FinalSpark</b> (Suisse) loue l’accès à des organoïdes d’environ 10 000 neurones. En Chine, <b>MetaBOC</b> (Tianjin, SUSTech, 2024) a relié un organoïde à une puce pour piloter un robot.</p>
    <p><b>Précautions</b> : vie courte (≈ 100 jours), échelle minuscule, gains d’énergie annoncés (jusqu’à un million de fois) seulement <b>estimés</b>, questions éthiques.</p>"""),
  dict(kicker="24.7", title="Robots quadrupèdes et usages de défense", sub="ce qui existe, ce qui reste difficile", scene="chien", body="""
    <p class="lede">Les robots quadrupèdes, souvent surnommés « chiens », marchent sur des terrains variés. Leurs usages civils : inspection de sites, logistique, secours en décombres ; leurs usages de défense : reconnaissance, transport, détection d’engins.</p>
    <ul class="rules">
      <li><b>Ce qu’ils font bien</b> : marcher, garder l’équilibre, cartographier avec LiDAR et caméras.</li>
      <li><b>Ce qui reste dur</b> : comprendre une scène imprévue, fonctionner sans communication, durer plus que quelques heures de batterie, résister à la boue, à l’eau, aux chocs.</li>
      <li><b>Un système hybride biologique</b> n’est pas envisageable sur le terrain : il exige un support de vie en laboratoire.</li>
    </ul>
    <p><b>Cadre éthique et juridique</b> : l’emploi de systèmes autonomes en situation de combat est vivement débattu, notamment à l’ONU. Le droit humanitaire (distinction, proportionnalité) exige un jugement humain ; beaucoup demandent un <b>contrôle humain significatif</b> et certains fabricants refusent d’armer leurs robots. Cet atlas ne décrit pas leur armement.</p>"""),
 ],
 practice={1:[dict(q="Pourquoi un modèle de langage comprend-il mal la physique du quotidien ?", choices=["il manque de mémoire vive", "son savoir vient de textes, pas d’actions ni de contacts avec le monde", "il est trop petit", "il calcule trop vite"], answer=1, why="<p>La physique intuitive vient de l’expérience corporelle, presque absente des textes.</p>")],
           5:[dict(q="Environ quelle puissance consomme un cerveau humain ?", choices=["2 W", "20 W", "200 W", "2 000 W"], answer=1, why="<p>De l’ordre de 20 W, contre 700 W pour un GPU de centre de données.</p>")],
           6:[dict(q="Pourquoi les gains d’énergie annoncés pour le biocalcul sont-ils à prendre avec prudence ?", choices=["ce sont des estimations, non démontrées à l’échelle", "ils sont mesurés dans un cluster", "ils concernent des GPU", "ils sont interdits"], answer=0, why="<p>Les systèmes actuels sont minuscules, de courte durée de vie, et les chiffres annoncés sont des estimations.</p>")]}
)]
