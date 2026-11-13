# Atlas de l'IA : chapitres 11 à 13 (loop engineering, robotique, modèles du monde)
GROUPS = [("Agir : harnais, agents, boucles", ["harnais", "agents", "loop"]), ("Le monde physique", ["robotique", "mondes"])]
CHAPTERS = [
dict(dir="loop", no=11, title="Le loop engineering", sub="concevoir la boucle autour du modèle", cnt="Vérifier, borner, reprendre, mesurer", alt="Une boucle qui génère, vérifie et corrige",
 scenes=[
  dict(key="gv", title="Générer, vérifier, corriger", sub="la boucle de base", kind="cycle", unit="temps", speed=0.5,
       nodes=[dict(n="Générer", pal="blue"), dict(n="Vérifier", pal="red"), dict(n="Diagnostiquer"), dict(n="Corriger")], center="jusqu’à validation",
       plate="Le modèle produit une solution, un vérificateur la teste (tests, règles, juge), le diagnostic dit ce qui ne va pas, et le modèle corrige. La qualité de la boucle est plafonnée par la qualité du vérificateur.",
       facts=[["vérificateur", "tests, types, règles, juge"], ["diagnostic", "message d’erreur lisible"], ["arrêt", "validé ou budget épuisé"]]),
  dict(key="passk", title="Essayer plusieurs fois", sub="pass@k : réussir au moins une fois en k essais", kind="curve", fn="passk",
       plate="Si chaque essai réussit avec la probabilité p, au moins un réussit sur k avec 1 − (1 − p)^k. Avec un vérificateur fiable, multiplier les essais transforme un modèle moyen en système fiable ; sans vérificateur, on ne sait pas lequel choisir.",
       facts=[["p = 0,15, k = 10", "≈ 80 %"], ["condition", "essais indépendants et vérifiables"]]),
  dict(key="budget", title="Les garde-fous", sub="une boucle sans limite est un risque", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Nombre de tours", s="plafond dur", pal="red"), dict(n="Coût", s="jetons, argent"), dict(n="Temps", s="délai maximal"), dict(n="Pas de progrès", s="détecter les boucles", pal="red")],
       plate="Toute boucle doit être bornée : nombre de tours, coût, durée, et détection de l’absence de progrès (même erreur trois fois de suite). Une boucle sans limite peut consommer un budget entier sur une erreur triviale.",
       facts=[["plafond", "obligatoire"], ["alerte", "même erreur répétée"]]),
  dict(key="memoire", title="Tenir sur la durée", sub="le contexte se remplit", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4, loop="contexte propre",
       stages=[dict(n="Travailler", s="le contexte se remplit", pal="blue"), dict(n="Contexte plein", s="limite atteinte", pal="red"), dict(n="Compacter", s="résumer l’essentiel"), dict(n="Notes dans des fichiers", s="plan, décisions, état"), dict(n="Contexte propre", s="relire les notes")],
       plate="Une longue tâche dépasse la fenêtre de contexte. On résume l’historique, on enregistre l’état dans des fichiers (plan, décisions, ce qui reste), et on repart d’un contexte propre qui relit ces notes. Les sous-agents isolent aussi des contextes entiers.",
       facts=[["compaction", "résumé de l’historique"], ["fichiers", "mémoire durable"], ["risque", "un résumé qui perd un détail clé"]]),
  dict(key="obs", title="Observer", sub="on ne corrige que ce qu’on voit", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Journaux", s="chaque appel"), dict(n="Traces", s="la trajectoire complète", pal="blue"), dict(n="Évaluations", s="suite de tâches test", pal="blue"), dict(n="Alertes", s="coût, échecs", pal="red")],
       plate="On garde la trace de chaque tour (entrées, sorties, outils, coûts). On rejoue une suite de tâches de référence à chaque changement de modèle ou de consigne pour détecter les régressions, et on surveille coûts et échecs en production.",
       facts=[["évaluations", "suite fixe, rejouée à chaque changement"], ["mesures", "réussite, coût, durée"]]),
 ],
 pages=[
  dict(kicker="Chapitre 11 · avancé", title="Le loop engineering", sub="l’ingénierie de la boucle", scene="gv", body="""
    <p class="lede">Dans un système à base d’agents, le modèle est une pièce. L’autre pièce, qui décide souvent de la réussite, est la <b>boucle</b> qui l’entoure.</p>
    <p>Concevoir cette boucle revient à répondre à cinq questions : <b>que voit le modèle</b> à chaque tour, <b>comment vérifie-t-on</b> son travail, <b>quand s’arrête-t-on</b>, <b>que garde-t-on</b> d’un tour à l’autre, et <b>comment mesure-t-on</b> ce qui se passe.</p>
    <p>On appelle cela le <i>loop engineering</i> : le même modèle peut échouer dans une mauvaise boucle et réussir dans une bonne.</p>"""),
  dict(kicker="11.1", title="Générer, vérifier, corriger", sub="le vérificateur décide de tout", scene="gv", body="""
    <p class="lede">Un modèle se juge mal lui-même : il trouve ses propres erreurs moins bien qu’un test.</p>
    <p>La boucle la plus solide <b>sépare la génération de la vérification</b>, et vérifie par quelque chose d’indépendant du modèle : des <b>tests</b> qui passent ou non, un compilateur, des règles de format, une exécution réelle. Le message d’erreur est ensuite ajouté au contexte, ce qui permet de corriger.</p>
    <p>Quand aucun test automatique n’existe, on peut utiliser un autre modèle comme <b>juge</b>, mais il a ses propres biais : il aime les réponses longues, ou celles du même modèle que lui.</p>"""),
  dict(kicker="11.2", title="Plusieurs essais et pass@k", sub="échanger du calcul contre de la fiabilité", scene="passk", body="""
    <p class="lede">Quand un modèle ne réussit qu’une fois sur sept, on peut l’essayer plusieurs fois et garder le bon résultat.</p>
    <div class="eq">pass@<i>k</i> = 1 − (1 − <i>p</i>)<sup><i>k</i></sup></div>
    <p>Avec <i>p</i> = 0,15 : un essai donne 15 %, dix essais environ 80 %. Cela suppose des essais <b>indépendants</b> et un moyen de <b>reconnaître le bon</b> : c’est le rôle du vérificateur. Sans lui, on parle de vote majoritaire ou de classement par un juge, bien moins fiables.</p>
    <p>C’est exactement ce que le renforcement à récompense vérifiable (chapitre 7) exploite pendant l’entraînement.</p>"""),
  dict(kicker="11.3", title="Borner la boucle", sub="tours, coût, durée, progrès", scene="budget", body="""
    <p class="lede">Une boucle sans limite finira, un jour, par tourner à vide.</p>
    <ul class="rules">
      <li><b>Nombre de tours</b> maximal, quoi qu’il arrive.</li>
      <li><b>Budget</b> en jetons ou en argent, vérifié à chaque tour.</li>
      <li><b>Délai</b> maximal pour la tâche entière.</li>
      <li><b>Détection de l’absence de progrès</b> : la même erreur trois fois, le même fichier modifié en boucle, un test qui échoue toujours de la même façon. On change alors de stratégie ou on s’arrête et on demande de l’aide.</li>
    </ul>
    <p>Un bon arrêt est un résultat : « je n’y arrive pas, voici ce que j’ai essayé » vaut mieux qu’une réponse inventée.</p>"""),
  dict(kicker="11.4", title="Tenir sur la durée", sub="contexte, notes, sous-agents", scene="memoire", body="""
    <p class="lede">Plus une tâche dure, plus le contexte s’encombre : anciens résultats d’outils, essais abandonnés, détails oubliés.</p>
    <ul class="rules">
      <li><b>Compacter</b> : résumer l’historique en gardant décisions, état et prochaines étapes.</li>
      <li><b>Écrire des notes</b> dans des fichiers (plan, journal, liste de tâches) : une mémoire que la compaction ne détruit pas.</li>
      <li><b>Isoler</b> des sous-tâches dans des sous-agents au contexte propre.</li>
      <li><b>Retirer</b> des résultats d’outils volumineux une fois exploités.</li>
    </ul>
    <p>Attention : un résumé peut perdre une contrainte importante. Les notes qui comptent doivent être écrites, pas seulement résumées.</p>"""),
  dict(kicker="11.5", title="Observer et mesurer", sub="traces, évaluations, régressions", scene="obs", body="""
    <p class="lede">On ne peut pas améliorer une boucle qu’on ne voit pas.</p>
    <ul class="rules">
      <li><b>Traces</b> : chaque tour (contexte, réponse, outils, résultat, coût) est conservé et consultable.</li>
      <li><b>Suite d’évaluations</b> : des tâches de référence rejouées à chaque changement de modèle, de consigne ou d’outil, pour détecter une régression.</li>
      <li><b>Mesures utiles</b> : taux de réussite sur plusieurs essais, coût moyen, durée, nombre de tours.</li>
      <li><b>Pièges</b> : un agent qui triche aux tests (il modifie le test au lieu du code), une boucle sans fin, une évaluation qui a fuité dans les consignes.</li>
    </ul>"""),
 ],
 practice={1:[dict(q="Pourquoi vaut-il mieux vérifier avec des tests qu’en demandant au modèle de se relire ?", choices=["les tests sont plus rapides à écrire", "un test est indépendant du modèle et ne se trompe pas comme lui", "un modèle ne sait pas relire", "les tests utilisent moins de jetons"], answer=1, why="<p>Un vérificateur indépendant détecte des erreurs que le modèle, qui a fait la même hypothèse en écrivant, ne verrait pas.</p>")],
           2:[dict(q="Chaque essai réussit avec p = 0,2. Environ quelle probabilité de réussir au moins une fois en 5 essais ?", choices=["20 %", "33 %", "67 %", "100 %"], answer=2, why="<p>1 − 0,8⁵ = 1 − 0,328 ≈ 0,67.</p>")],
           3:[dict(q="Un agent modifie le même fichier cinq fois de suite sans que le test passe. Que faire ?", choices=["continuer indéfiniment", "détecter l’absence de progrès, changer de stratégie ou s’arrêter", "augmenter la température à 2", "supprimer le test"], answer=1, why="<p>Une bonne boucle repère l’absence de progrès et change de méthode ou demande de l’aide.</p>")]}
),
dict(dir="robotique", no=12, title="L’IA et la robotique", sub="percevoir, planifier, agir", cnt="Du bras industriel aux modèles vision-langage-action", alt="Un bras robotique guidé par une caméra",
 scenes=[
  dict(key="boucle", title="La boucle du robot", sub="percevoir, comprendre, décider, agir", kind="cycle", unit="temps", speed=0.5,
       nodes=[dict(n="Percevoir", pal="blue"), dict(n="Comprendre"), dict(n="Planifier", pal="red"), dict(n="Agir")], center="des dizaines de fois par seconde",
       plate="Un robot répète en boucle : percevoir (caméras, capteurs), comprendre la scène, planifier un mouvement, l’exécuter, puis percevoir à nouveau le résultat. La boucle de commande bas niveau tourne à plus de 100 fois par seconde.",
       facts=[["perception", "caméras, profondeur, force"], ["commande", "100 à 1000 Hz"], ["décision", "1 à 10 Hz"]]),
  dict(key="bras", title="Un bras qui saisit", sub="deux articulations, une caméra", kind="arm", targetName="Objet à saisir", targetLabel="objet",
       plate="La caméra localise l’objet. Un calcul de cinématique inverse trouve les angles des articulations pour amener la pince dessus ; un contrôleur les suit. L’ensemble paraît simple et exige perception, géométrie et contrôle.",
       facts=[["entrée", "position de l’objet"], ["sortie", "angles θ₁ et θ₂"], ["méthode", "cinématique inverse"]]),
  dict(key="vla", title="Les modèles vision-langage-action", sub="une consigne, des images, des mouvements", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Images", s="caméras du robot"), dict(n="Consigne", s="« range la tasse »"), dict(n="Modèle VLA", s="vision + langage + action", pal="blue"), dict(n="Actions", s="mouvements des articulations", pal="red"), dict(n="Robot", s="exécute"), dict(n="Nouvelles images", s="retour au début")],
       plate="Un modèle vision-langage-action reçoit les images de caméra et une consigne en langage, et produit directement des commandes de mouvement, sous forme de jetons d’actions ou par un modèle génératif. Il hérite des connaissances d’un modèle vision-langage préentraîné.",
       facts=[["entrée", "images + texte"], ["sortie", "actions"], ["entraînement", "démonstrations de robots"]]),
  dict(key="sim", title="De la simulation au réel", sub="s’entraîner des millions de fois sans casser un robot", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Simulateur", s="millions d’essais", pal="blue"), dict(n="Randomisation", s="masses, frottements, lumière"), dict(n="Politique apprise", s="par renforcement", pal="red"), dict(n="Robot réel", s="test et ajustements"), dict(n="Écart sim-réel", s="ce que la simulation rate"), dict(n="Données réelles", s="pour corriger", pal="blue")],
       plate="On entraîne la politique dans un simulateur, où les essais sont gratuits et parallèles. Pour qu’elle tienne dans le monde réel, on randomise la simulation (masses, frottements, lumières) afin que le réel soit un cas parmi d’autres. Un écart subsiste, qu’on réduit avec des données réelles.",
       facts=[["avantage", "des milliers de robots virtuels"], ["limite", "la simulation n’est pas la réalité"]]),
 ],
 pages=[
  dict(kicker="Chapitre 12 · tous niveaux", title="L’IA et la robotique", sub="donner un corps à un modèle", scene="boucle", body="""
    <p class="lede">Un robot doit percevoir un monde bruité, décider, et agir sur lui, sans pouvoir annuler ses erreurs. C’est bien plus dur que de produire du texte.</p>
    <p>Les robots industriels classiques exécutent des mouvements programmés dans un environnement contrôlé. L’IA leur apporte la capacité de gérer des situations <b>non prévues</b> : un objet déplacé, un éclairage différent, une consigne en langage naturel.</p>
    <p>Ce chapitre suit la boucle du robot, l’apprentissage par imitation et renforcement, le passage de la simulation au réel, et les modèles qui relient la vision, le langage et l’action.</p>"""),
  dict(kicker="12.1", title="Percevoir, planifier, commander", sub="l’approche classique", scene="bras", body="""
    <p class="lede">La robotique classique découpe le problème en blocs.</p>
    <ul class="rules">
      <li><b>Perception</b> : caméras, capteurs de profondeur, de force ; reconnaître et localiser les objets.</li>
      <li><b>Planification</b> : trouver un chemin sans collision jusqu’à la cible.</li>
      <li><b>Cinématique inverse</b> : convertir une position voulue de la pince en angles d’articulations.</li>
      <li><b>Commande</b> : un contrôleur (souvent un PID) suit la trajectoire en corrigeant à plus de 100 Hz.</li>
    </ul>
    <p>Cette approche est fiable et explicable, mais chaque bloc demande des modèles précis du robot et du monde.</p>"""),
  dict(kicker="12.2", title="Apprendre à agir", sub="imitation et renforcement", scene="boucle", body="""
    <p class="lede">Plutôt que d’écrire les mouvements, on peut les <b>apprendre</b>.</p>
    <ul class="rules">
      <li><b>Imitation</b> (<i>behavior cloning</i>) : un opérateur guide le robot (télé-opération) ; un réseau apprend à reproduire ses gestes à partir des images. Simple et efficace, mais il dérive quand il sort de ce qu’il a vu.</li>
      <li><b>Renforcement</b> (chapitre 7) : le robot essaie, reçoit une récompense (tâche réussie) et améliore sa politique. Puissant, mais nécessite énormément d’essais.</li>
    </ul>
    <p>Les deux se combinent : imiter pour démarrer, puis renforcer pour dépasser les démonstrations.</p>"""),
  dict(kicker="12.3", title="De la simulation au monde réel", sub="s’entraîner virtuellement", scene="sim", body="""
    <p class="lede">Un robot réel est lent, cher et fragile. Un simulateur peut faire tourner des <b>milliers de robots virtuels</b> en parallèle, bien plus vite que le temps réel.</p>
    <p>Problème : la simulation n’est qu’une approximation (frottements, déformations, bruit des capteurs). Une politique parfaite en simulation peut échouer sur le vrai robot. La <b>randomisation de domaine</b> varie la simulation (masses, frottements, couleurs, retards) pour que la politique apprenne à tolérer ces écarts.</p>
    <p>Le dernier tronçon se règle avec quelques données réelles.</p>"""),
  dict(kicker="12.4", title="Vision, langage, action", sub="les modèles VLA", scene="vla", body="""
    <p class="lede">L’idée récente : partir d’un modèle <b>vision-langage</b> préentraîné sur d’immenses corpus, et lui apprendre aussi à <b>produire des actions</b>.</p>
    <p>Le modèle reçoit les images de la caméra et une consigne (« mets la tasse dans l’évier ») et sort des commandes de mouvement : soit des <b>jetons d’action</b> traités comme du texte, soit une sortie continue produite par un modèle génératif.</p>
    <p>Des exemples publics existent (RT-2, OpenVLA, π0). L’intérêt : le robot hérite de connaissances générales (reconnaître un objet jamais vu, comprendre une consigne inédite). La difficulté : les <b>données de robots</b> sont rares et chères comparées au texte.</p>"""),
  dict(kicker="12.5", title="Données, sécurité, limites", sub="ce qui reste difficile", scene="boucle", body="""
    <p class="lede">Un robot agit dans le monde physique : une erreur de prédiction devient un geste.</p>
    <ul class="rules">
      <li><b>Données</b> : collectées par des humains, une démonstration à la fois ; la diversité des situations manque.</li>
      <li><b>Cas rares</b> : un objet glissant, un humain qui passe : le modèle doit rester sûr hors de sa zone de confort.</li>
      <li><b>Sécurité</b> : limites de force et de vitesse, arrêts d’urgence, zones interdites, qu’aucun modèle ne doit pouvoir contourner.</li>
      <li><b>Latence</b> : un gros modèle qui réfléchit lentement ne peut pas commander seul un mouvement rapide ; on le combine à une commande rapide.</li>
    </ul>"""),
 ],
 practice={0:[dict(q="Pourquoi randomise-t-on la simulation (masses, frottements, couleurs) ?", choices=["pour accélérer le calcul", "pour que le monde réel ressemble à l’un des cas vus pendant l’entraînement", "pour économiser de la mémoire", "pour supprimer le bruit"], answer=1, why="<p>La politique apprend à tolérer des variations ; le réel devient un cas de plus.</p>")],
           2:[dict(q="Quel est le principal inconvénient de l’imitation seule ?", choices=["elle est impossible avec des images", "le robot dérive quand il rencontre des situations absentes des démonstrations", "elle exige un simulateur", "elle ne fonctionne que pour les bras"], answer=1, why="<p>Une petite erreur l’amène dans un état jamais vu, où il n’a pas appris quoi faire : les erreurs s’accumulent.</p>")],
           3:[dict(q="Un modèle vision-langage-action produit…", choices=["uniquement du texte", "des actions (mouvements) à partir d’images et d’une consigne", "des images", "des plongements de mots"], answer=1, why="<p>Il reçoit images et consigne, et renvoie des commandes de mouvement.</p>")]}
),
dict(dir="mondes", no=13, title="Les modèles du monde", sub="prédire, imaginer, planifier", cnt="Comment une IA se représente ce qui va arriver", alt="Un agent qui imagine plusieurs trajectoires avant d’agir",
 scenes=[
  dict(key="latent", title="Un modèle du monde", sub="encoder, prédire, comparer", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4, loop="l’état suivant devient l’état courant",
       stages=[dict(n="Observation", s="image, capteurs"), dict(n="Encodeur", s="vers un état latent", pal="blue"), dict(n="État latent", s="résumé compact"), dict(n="Dynamique", s="état + action → état suivant", pal="red"), dict(n="Prédiction", s="état suivant"), dict(n="Comparaison", s="avec la réalité")],
       plate="Un modèle du monde apprend une fonction qui prédit l’état suivant à partir de l’état courant et d’une action. Il travaille souvent sur un résumé compact (état latent) plutôt que sur les pixels, et s’entraîne en comparant ses prédictions à ce qui arrive vraiment.",
       facts=[["entrée", "état + action"], ["sortie", "état suivant"], ["entraînement", "erreur de prédiction"]]),
  dict(key="imagine", title="Imaginer avant d’agir", sub="plusieurs futurs essayés dans la tête", kind="grid", rows=4, cols=6, walls=[[1, 1], [1, 2], [2, 4]], goal=[0, 5], traps=[[3, 3]], goalLabel="but", showGhost=True,
       paths=[dict(cells=[[3, 0], [3, 1], [3, 2], [3, 3]], ghost=True, pal="blue"), dict(cells=[[3, 0], [2, 0], [2, 1], [2, 2], [2, 3]], ghost=True, pal="blue"), dict(cells=[[3, 0], [2, 0], [2, 1], [2, 2], [1, 3], [0, 3], [0, 4], [0, 5]], info="trajectoire choisie : la meilleure parmi celles imaginées")],
       plate="Avec un modèle du monde, l’agent peut simuler dans sa tête plusieurs suites d’actions (points bleus), évaluer où elles mènent, puis exécuter la meilleure sans avoir pris les mauvaises dans la réalité.",
       facts=[["planification", "recherche dans le modèle"], ["avantage", "peu d’essais réels"], ["risque", "un modèle faux, un plan faux"]]),
  dict(key="jepa", title="Prédire des représentations", sub="l’idée JEPA", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Contexte", s="partie visible"), dict(n="Encodeur", s="représentation", pal="blue"), dict(n="Prédicteur", s="devine la représentation masquée", pal="red"), dict(n="Cible", s="représentation de la partie masquée"), dict(n="Erreur", s="dans l’espace des représentations"), dict(n="Pas de pixels", s="on ne prédit pas chaque détail", pal="paper")],
       plate="Plutôt que de prédire chaque pixel de la suite d’une vidéo, impossible à deviner dans les détails, JEPA prédit une représentation abstraite de la partie manquante. Le modèle apprend ce qui est prévisible (le mouvement d’un objet) et ignore ce qui ne l’est pas (la position d’une feuille).",
       facts=[["JEPA", "joint embedding predictive architecture"], ["pari", "prédire l’abstrait plutôt que le détail"]]),
  dict(key="video", title="Les modèles du monde génératifs", sub="générer la suite d’une scène", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4, loop="on recommence",
       stages=[dict(n="Image + action", s="« avance », « saute »"), dict(n="Modèle génératif", s="vidéo, jeu, simulation", pal="blue"), dict(n="Image suivante", s="la scène qui évolue", pal="red")],
       plate="Des modèles génèrent la suite d’une scène à partir d’images et d’actions : une vidéo, ou même un environnement jouable. Ils produisent un monde plausible, mais pas toujours cohérent à long terme : objets qui apparaissent, physique approximative.",
       facts=[["entrée", "image + action"], ["sortie", "image suivante"], ["limite", "cohérence à long terme"]]),
 ],
 pages=[
  dict(kicker="Chapitre 13 · avancé", title="Les modèles du monde", sub="prédire ce qui va arriver", scene="latent", body="""
    <p class="lede">Un modèle de langage prédit le <b>mot</b> suivant. Un <b>modèle du monde</b> prédit <b>l’état suivant du monde</b> : ce qui se passera si l’on agit de telle ou telle façon.</p>
    <p>Un humain qui tend la main vers un verre anticipe sans y penser ce qui arrivera s’il le lâche. Donner cette capacité à une IA permet d’<b>essayer des actions dans sa tête</b> avant de les tenter pour de bon, ce qui est précieux dès que les essais réels coûtent cher ou sont dangereux : un robot, une voiture, un jeu complexe.</p>"""),
  dict(kicker="13.1", title="L’idée", sub="un état, une action, un état suivant", scene="latent", body="""
    <p class="lede">Le cœur d’un modèle du monde est une fonction : <b>état suivant = f(état, action)</b>.</p>
    <p>Elle est apprise sur des données d’interaction : on observe, on agit, on observe le résultat, et on ajuste la fonction pour que ses prédictions collent à la réalité.</p>
    <p>Comme on ne veut pas prédire chaque pixel, on encode d’abord l’observation dans un <b>état latent</b>, bien plus petit, qui garde ce qui compte pour décider. C’est la méthode de modèles comme <b>Dreamer</b>, qui apprennent à jouer en s’entraînant surtout dans leur imagination.</p>"""),
  dict(kicker="13.2", title="Planifier dans l’imagination", sub="essayer des futurs dans la tête", scene="imagine", body="""
    <p class="lede">Avec un modèle du monde, on peut <b>chercher</b> plutôt que réagir.</p>
    <p>L’agent déroule plusieurs suites d’actions dans le modèle, estime ce que chacune rapporte, et exécute la meilleure ; à chaque pas, il recommence avec l’observation réelle (c’est le principe de la commande prédictive). Dans <b>MuZero</b> (2019), un modèle appris sert de base à une recherche arborescente et a permis de jouer au Go, aux échecs et aux jeux vidéo sans connaître les règles à l’avance.</p>
    <p>Le prix : un modèle imparfait donne des plans imparfaits, et l’erreur grandit avec la longueur de l’horizon.</p>"""),
  dict(kicker="13.3", title="Prédire l’abstrait", sub="JEPA", scene="jepa", body="""
    <p class="lede">Prédire chaque pixel de la suite d’une vidéo est à la fois énorme et vain : mille détails n’ont aucune importance et sont imprévisibles.</p>
    <p>L’approche <b>JEPA</b> (<i>joint embedding predictive architecture</i>) propose de prédire non pas l’image mais sa <b>représentation</b> : le modèle devine l’abstraction de ce qui est caché ou à venir, et laisse tomber les détails imprévisibles. Les modèles de la famille V-JEPA suivent cette idée sur des vidéos.</p>
    <p>C’est un pari sur la manière de construire des modèles du monde qui comprennent la physique du quotidien. Les résultats existent, mais la question reste ouverte.</p>"""),
  dict(kicker="13.4", title="Générer des mondes", sub="vidéo, jeux, simulations", scene="video", body="""
    <p class="lede">Une autre voie génère directement <b>l’image suivante</b>, y compris en réponse à des actions.</p>
    <p>Des modèles de génération vidéo produisent des scènes plausibles sur plusieurs secondes ; d’autres créent des <b>environnements jouables</b> à partir d’images : le joueur appuie sur une touche, le modèle imagine la scène qui en résulte.</p>
    <p>Cela suggère qu’ils ont appris quelque chose de la dynamique du monde. Mais ils trichent parfois avec la physique : objets qui apparaissent ou changent de forme, mouvements impossibles, oubli de ce qui sort de l’écran.</p>"""),
  dict(kicker="13.5", title="Limites et questions ouvertes", sub="ce qu’un modèle du monde ne sait pas encore faire", scene="latent", body="""
    <p class="lede">Prédire un instant est facile ; prédire longtemps l’est beaucoup moins.</p>
    <ul class="rules">
      <li><b>Dérive</b> : à chaque pas, une petite erreur s’ajoute ; au bout de dizaines de pas, la prédiction n’est plus fiable.</li>
      <li><b>Évaluation</b> : comment mesurer qu’un modèle a « compris » la physique, plutôt qu’imité des vidéos ?</li>
      <li><b>Causalité</b> : savoir ce qui arrive ensemble n’est pas savoir ce que provoque une action.</li>
      <li><b>Coût</b> : entraîner sur de la vidéo demande bien plus de calcul que sur du texte.</li>
    </ul>
    <p>Pour les robots (chapitre 12), un bon modèle du monde est l’une des pistes les plus étudiées pour réduire le nombre d’essais réels.</p>"""),
 ],
 practice={0:[dict(q="Quelle fonction apprend un modèle du monde ?", choices=["mot suivant = f(mots précédents)", "état suivant = f(état, action)", "classe = f(image)", "texte = f(bruit)"], answer=1, why="<p>Il prédit comment l’état du monde évolue quand on agit.</p>")],
           2:[dict(q="Dans JEPA, que prédit le modèle ?", choices=["chaque pixel de la suite", "une représentation abstraite de la partie manquante", "le mot suivant", "l’action à exécuter"], answer=1, why="<p>Il prédit dans l’espace des représentations, ce qui évite de deviner des détails imprévisibles.</p>")],
           4:[dict(q="Pourquoi les prédictions d’un modèle du monde se dégradent-elles sur un long horizon ?", choices=["le GPU chauffe", "les petites erreurs s’additionnent à chaque pas", "le vocabulaire est trop petit", "l’image est trop grande"], answer=1, why="<p>Chaque pas part de la prédiction précédente, qui contient déjà une erreur.</p>")]}
)]
