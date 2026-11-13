# Atlas de l'IA : chapitres 30 à 34 (interprétabilité, évaluation, biais, droit, sûreté) et ajouts à des chapitres existants
GROUPS = [("Comprendre, évaluer, encadrer", ["interpretabilite", "evaluer", "biais", "droit", "surete"])]
P = lambda q, ch, a, w: dict(q=q, choices=ch, answer=a, why=f"<p>{w}</p>")
def pipe(key, title, sub, stages, plate, facts, per=3, bw=2.3, gap=0.8, **kw):
    return dict(key=key, title=title, sub=sub, kind="pipeline", per=per, bw=bw, gap=gap, y=1.4, stages=[dict(n=a, s=b, **({"pal": c} if c else {})) for a, b, c in stages], plate=plate, facts=facts, **kw)

CHAPTERS = [
dict(dir="interpretabilite", no=30, title="Ouvrir la boîte noire", sub="explications, circuits, caractéristiques", cnt="Comment savoir ce qui se passe dans un réseau", alt="Un réseau dont on étudie les circuits internes",
 scenes=[
  pipe("posthoc", "Expliquer après coup", "quelle partie de l’entrée a compté ?", [("Entrée", "texte ou image", None), ("Modèle", "boîte noire", "dark"), ("Sortie", "la prédiction", None), ("Perturbation", "masquer, modifier", "blue"), ("Attribution", "poids par mot ou pixel", "red"), ("Carte", "ce qui a compté", None)],
       "Les méthodes post-hoc (saliency, LIME, SHAP) mesurent l’effet de modifications de l’entrée sur la sortie et en déduisent l’importance de chaque morceau. Elles décrivent le comportement, pas le mécanisme interne.", [["LIME", "modèle local simple"], ["SHAP", "valeurs de Shapley"], ["limite", "corrélation, pas cause"]]),
  dict(key="circuit", title="Un circuit", sub="têtes d’induction", kind="net", layers=[3, 4, 4, 3], names=["Jetons", "Tête A : précédent", "Tête B : copie", "Sortie"], params="deux têtes qui coopèrent pour répéter un motif",
       plate="Les chercheurs en interprétabilité mécaniste cherchent des « circuits » : de petits groupes de composants qui réalisent une fonction. Exemple connu : la tête d’induction, qui repère qu’un motif « A B … A » a déjà eu lieu et prédit « B ».",
       facts=[["tête d’induction", "complète les motifs répétés"], ["méthode", "ablation, patching"]]),
  pipe("sae", "Autoencodeur parcimonieux", "séparer les concepts mêlés", [("Activations", "mélange dense", None), ("Encodeur", "beaucoup de directions", "blue"), ("Parcimonie", "peu de traits actifs", "red"), ("Décodeur", "reconstruit", "blue"), ("Caractéristiques", "concepts lisibles", None), ("Intervention", "amplifier ou couper", "red")],
       "Un neurone représente souvent plusieurs concepts (superposition). Un autoencodeur parcimonieux, entraîné sur les activations, en extrait des directions plus lisibles : « Golden Gate », « code incorrect »… On peut les amplifier pour changer le comportement.", [["superposition", "plus de concepts que de neurones"], ["résultat", "millions de traits identifiés"], ["limite", "couverture partielle"]]),
 ],
 pages=[
  dict(kicker="Chapitre 30 · comprendre", title="Ouvrir la boîte noire", sub="peut-on expliquer un modèle ?", scene="posthoc", body="""
    <p class="lede">Un réseau de milliards de paramètres ne s’explique pas par lecture. L’<b>interprétabilité</b> cherche à comprendre pourquoi il répond ce qu’il répond.</p>
    <p>Enjeux : confiance, détection d’erreurs et de biais, sûreté, exigences réglementaires d’explication. Deux approches : expliquer <b>de l’extérieur</b> (post-hoc), ou comprendre <b>de l’intérieur</b> (interprétabilité mécaniste).</p>"""),
  dict(kicker="30.1", title="Les explications post-hoc", sub="saliency, LIME, SHAP", scene="posthoc", body="""
    <ul class="rules">
      <li><b>Saliency</b> : le gradient de la sortie par rapport à l’entrée montre quels pixels ou mots comptent.</li>
      <li><b>LIME</b> : approcher le modèle, autour d’un exemple, par un modèle simple lisible.</li>
      <li><b>SHAP</b> : répartir la prédiction entre les variables selon les valeurs de Shapley (théorie des jeux).</li>
    </ul>
    <p>Ces cartes sont utiles mais peuvent être instables, et rien ne garantit qu’elles reflètent le vrai mécanisme : elles montrent une corrélation.</p>"""),
  dict(kicker="30.2", title="Circuits et têtes d’induction", sub="l’interprétabilité mécaniste", scene="circuit", body="""
    <p class="lede">L’<b>interprétabilité mécaniste</b> traite un réseau comme un programme à rétro-concevoir.</p>
    <p>Les chercheurs ont identifié des circuits : la <b>tête d’induction</b> (compléter un motif déjà vu), des circuits d’addition modulaire, d’indirection… On les valide par des expériences : <b>ablation</b> (couper un composant) et <b>patching</b> (remplacer ses activations par celles d’une autre exécution) pour voir si la sortie change.</p>
    <p>Les succès concernent surtout de petits modèles ou des comportements précis.</p>"""),
  dict(kicker="30.3", title="Superposition et caractéristiques", sub="un neurone, plusieurs idées", scene="sae", body="""
    <p class="lede">Un neurone isolé répond souvent à plusieurs concepts sans rapport : le réseau stocke plus de concepts que de neurones, en les superposant.</p>
    <p>Les <b>autoencodeurs parcimonieux</b> (<i>sparse autoencoders</i>) apprennent à décomposer les activations en <b>caractéristiques</b> plus lisibles. Des travaux de 2024 en ont extrait des millions dans de grands modèles, et montré qu’amplifier l’une d’elles infléchit le comportement.</p>
    <p>Reste à vérifier qu’elles couvrent tout ce que fait le modèle : la couverture est partielle.</p>"""),
  dict(kicker="30.4", title="Ce qu’on peut en attendre", sub="et ce qui reste ouvert", scene="circuit", body="""
    <ul class="rules">
      <li><b>Utile aujourd’hui</b> : déboguer un comportement précis, repérer des raccourcis appris, auditer un biais.</li>
      <li><b>Prometteur</b> : détecter la tromperie ou des objectifs cachés, contrôler un comportement par intervention directe.</li>
      <li><b>Ouvert</b> : passer à l’échelle des plus grands modèles, vérifier qu’une explication est fidèle, comprendre les raisonnements longs.</li>
    </ul>
    <p>Un modèle expliqué par une carte colorée n’est pas pour autant <b>compris</b>.</p>"""),
 ],
 practice={1:[P("Que mesure une méthode post-hoc comme SHAP ?", ["l’effet de chaque variable d’entrée sur la sortie", "le nombre de couches", "la vitesse du GPU", "le vocabulaire"], 0, "Elle répartit la prédiction entre variables : elle décrit le comportement sans ouvrir le mécanisme.")],
           2:[P("Pourquoi fait-on des ablations en interprétabilité mécaniste ?", ["pour valider qu’un composant est bien utilisé pour une fonction", "pour réduire la taille du fichier", "pour accélérer l’entraînement", "pour changer de langue"], 0, "Couper un composant et observer le changement de sortie teste son rôle causal.")],
           3:[P("Qu’est-ce que la superposition ?", ["un réseau stocke plus de concepts que de neurones en les mêlant", "deux GPU superposés", "deux modèles fusionnés", "une couche dupliquée"], 0, "Les concepts sont représentés par des directions, pas par des neurones individuels.")]}
),
dict(dir="evaluer", no=31, title="Évaluer et fiabiliser", sub="benchmarks, contamination, arène, hallucinations", cnt="Comment mesurer un modèle sans se tromper", alt="Une courbe de score qui sature",
 scenes=[
  dict(key="satur", title="Un benchmark saturé", sub="du défi à l’évidence", kind="curve", fn="saturation",
       plate="Chaque benchmark finit par être « résolu » : les scores approchent du plafond et ne distinguent plus les modèles. D’où le renouvellement permanent (MMLU, puis GPQA, ARC-AGI, SWE-bench, des examens plus durs). Courbes illustratives.",
       facts=[["saturation", "le score plafonne"], ["conséquence", "il faut des tests plus durs"]]),
  pipe("bench", "Les familles de tests", "ce qu’on mesure", [("Connaissances", "MMLU, GPQA", "blue"), ("Raisonnement", "maths, ARC-AGI", "blue"), ("Code", "SWE-bench", "blue"), ("Agents", "tâches en environnement", "red"), ("Préférences", "arène humaine", None), ("Sécurité", "refus, jailbreaks", None)],
       "Aucun test ne mesure « l’intelligence ». On en combine : connaissances à choix multiples, problèmes de raisonnement, résolution de tickets de code, tâches d’agents, préférences humaines, résistance aux attaques.",
       [["limite", "chaque test mesure peu de choses"], ["conseil", "regarder plusieurs tests"]]),
  pipe("contam", "La contamination", "tricher sans le vouloir", [("Test public", "sur Internet", None), ("Corpus du modèle", "aspire le web", "blue"), ("Fuite", "le test est dans l’entraînement", "red"), ("Score gonflé", "mémoire, pas capacité", "red"), ("Parades", "tests privés, renouvelés", "blue"), ("Contrôle", "recherche de doublons", None)],
       "Si les questions d’un test se retrouvent dans les données d’entraînement, le modèle peut les avoir apprises. Parades : tests privés, tests renouvelés régulièrement, détection de recoupements.", [["problème", "score non fiable"], ["parade", "tests nouveaux ou privés"]]),
  pipe("juge", "Arène et modèle-juge", "mesurer l’utilité perçue", [("Deux réponses", "anonymes", None), ("Juge", "humain ou modèle", "blue"), ("Vote", "A, B ou égalité", "red"), ("Classement Elo", "mis à jour", "blue"), ("Biais", "longueur, style, auto-préférence", "red"), ("Contrôles", "ordre, longueur", None)],
       "Une arène compare des paires de réponses et calcule un classement Elo. Un modèle peut aussi jouer le juge, à coût réduit, mais il préfère les réponses longues et celles qui ressemblent aux siennes. Il faut contrôler ces biais.", [["Elo", "classement par duels"], ["biais", "longueur, position, style"]]),
  pipe("halluc", "Réduire les hallucinations", "ancrer les réponses", [("Question", "factuelle", None), ("Récupération", "documents fiables (RAG)", "blue"), ("Génération", "réponse avec sources", "blue"), ("Vérification", "citations contrôlées", "red"), ("Abstention", "« je ne sais pas »", "red"), ("Journal", "erreurs mesurées", None)],
       "Un modèle produit du texte plausible, pas vérifié. On réduit les erreurs en lui fournissant les sources (chapitre 20), en exigeant des citations, en vérifiant automatiquement, en l’entraînant à dire qu’il ne sait pas, et en mesurant le taux d’erreur sur son propre usage.", [["cause", "plausible ≠ vrai"], ["remède", "sources, citations, abstention"]]),
 ],
 pages=[
  dict(kicker="Chapitre 31 · évaluer", title="Évaluer et fiabiliser", sub="un score n’est pas une garantie", scene="satur", body="""
    <p class="lede">Choisir ou valider un modèle suppose de le mesurer. Or mesurer est difficile : les tests vieillissent, fuient, et ne représentent jamais votre usage.</p>
    <p>Ce chapitre présente les grandes familles de tests, leurs pièges, et la seule évaluation qui compte vraiment : la vôtre.</p>"""),
  dict(kicker="31.1", title="Les benchmarks", sub="ce qu’ils mesurent", scene="bench", body="""
    <ul class="rules">
      <li><b>Connaissances</b> : MMLU (questions de niveau universitaire), GPQA (sciences difficiles).</li>
      <li><b>Raisonnement</b> : problèmes de mathématiques, ARC-AGI (puzzles visuels de généralisation).</li>
      <li><b>Code</b> : SWE-bench (corriger de vrais tickets de dépôts), exercices de programmation.</li>
      <li><b>Agents</b> : tâches longues en environnement (navigation, bureau, terminal).</li>
    </ul>
    <p>Un chiffre sans le protocole (nombre d’essais, aides, outils) ne se compare pas.</p>"""),
  dict(kicker="31.2", title="Saturation et contamination", sub="deux pièges", scene="satur", body="""
    <p class="lede">Un test <b>sature</b> quand les meilleurs modèles s’approchent du maximum : il ne départage plus.</p>
    <p>La <b>contamination</b> aggrave le problème : si les questions d’un test sont dans les données d’entraînement, le score mesure la mémoire. Un modèle peut aussi être <b>optimisé pour le test</b> sans être meilleur en général.</p>"""),
  dict(kicker="31.3", title="Contamination en détail", sub="comment s’en protéger", scene="contam", body="""
    <ul class="rules">
      <li>Préférer des tests <b>privés</b> ou <b>renouvelés</b> régulièrement.</li>
      <li>Rechercher des <b>recoupements</b> entre le test et le corpus.</li>
      <li>Comparer sur des variantes reformulées : si le score s’effondre, c’était de la mémoire.</li>
    </ul>"""),
  dict(kicker="31.4", title="Arène et modèle-juge", sub="évaluer l’utilité perçue", scene="juge", body="""
    <p class="lede">Pour les tâches ouvertes (rédiger, conseiller), il n’y a pas de bonne réponse unique.</p>
    <p>Une <b>arène</b> montre deux réponses anonymes à des utilisateurs, qui votent ; on calcule un classement <b>Elo</b>. Un <b>modèle-juge</b> automatise le vote à bas coût, mais favorise les réponses longues et celles qui lui ressemblent : on contrôle l’ordre de présentation et la longueur.</p>"""),
  dict(kicker="31.5", title="Les hallucinations", sub="plausible n’est pas vrai", scene="halluc", body="""
    <p class="lede">Un modèle de langage prédit le texte vraisemblable ; il peut inventer un fait, une citation, une référence.</p>
    <p>On les réduit en <b>ancrant</b> la réponse dans des sources (RAG), en demandant des <b>citations vérifiables</b>, en laissant le modèle <b>s’abstenir</b>, et en vérifiant automatiquement ce qui peut l’être (code exécuté, calcul refait). On ne les supprime pas : on les mesure et on organise la vérification.</p>"""),
  dict(kicker="31.6", title="Votre propre jeu d’évaluation", sub="le test qui compte", scene="bench", body="""
    <ul class="rules">
      <li>Rassembler 50 à 200 <b>cas réels</b> de votre usage, avec la réponse attendue ou une grille.</li>
      <li>Le garder <b>privé</b> et le faire évoluer avec les échecs rencontrés.</li>
      <li>À chaque changement de modèle, de prompt ou d’outil, <b>relancer</b> et comparer.</li>
      <li>Mesurer aussi le <b>coût</b>, la <b>latence</b> et les <b>refus à tort</b>.</li>
    </ul>
    <p>C’est l’équivalent des tests unitaires pour l’IA.</p>"""),
 ],
 practice={2:[P("Que signifie la contamination d’un benchmark ?", ["le test se retrouve dans les données d’entraînement", "le test contient des virus", "le test est trop long", "le modèle est trop petit"], 0, "Le score mesure alors une mémoire, pas une capacité générale.")],
           4:[P("Quel biais courant touche un modèle-juge ?", ["il préfère les réponses longues", "il refuse de noter", "il ne lit que le début", "il ignore les chiffres"], 0, "La longueur et la ressemblance avec ses propres réponses faussent le jugement.")],
           6:[P("Quel est le meilleur test pour choisir un modèle pour votre usage ?", ["un jeu d’évaluation tiré de vos cas réels", "le classement public", "le nombre de paramètres", "le prix seul"], 0, "Seul un jeu représentatif de votre usage mesure ce qui vous intéresse.")]}
),
dict(dir="biais", no=32, title="Biais, équité et désinformation", sub="mesurer l’injustice, reconnaître le faux", cnt="Les risques sociaux de l’IA", alt="Une balance et un filigrane de provenance",
 scenes=[
  pipe("sourcebiais", "D’où vient le biais", "de la donnée à la décision", [("Monde", "inégalités réelles", None), ("Données", "échantillon biaisé", "red"), ("Modèle", "reproduit les motifs", "blue"), ("Décision", "inégale selon les groupes", "red"), ("Boucle", "la décision change le monde", "red"), ("Audit", "mesurer par groupe", "blue")],
       "Un modèle apprend les régularités de ses données, y compris les injustices. Des données mal représentatives, des étiquettes humaines biaisées ou des variables « proxys » (code postal) produisent des décisions inégales, qui peuvent renforcer les données futures.", [["sources", "données, étiquettes, proxys"], ["effet", "boucle de renforcement"]]),
  pipe("equite", "Plusieurs définitions de l’équité", "on ne peut pas tout avoir", [("Parité", "mêmes taux de décision", None), ("Égalité des chances", "mêmes taux de vrais positifs", None), ("Calibration", "un score vaut pareil partout", None), ("Théorème", "incompatibles si les groupes diffèrent", "red"), ("Choix", "selon l’enjeu et la loi", "blue"), ("Documentation", "expliquer le compromis", "blue")],
       "Les définitions mathématiques de l’équité (parité, égalité des chances, calibration) ne peuvent en général pas être satisfaites ensemble quand les taux de base des groupes diffèrent. Choisir est une décision de société, à documenter.", [["résultat", "impossibilité de tout satisfaire"], ["action", "choisir, documenter, auditer"]]),
  pipe("provenance", "Prouver l’origine", "filigrane, signature, métadonnées", [("Création", "caméra ou IA", None), ("Signature", "métadonnées C2PA", "blue"), ("Édition", "historique ajouté", "blue"), ("Publication", "plateforme", None), ("Vérification", "contrôle de la chaîne", "red"), ("Limites", "métadonnées effaçables", "red")],
       "La norme C2PA (« Content Credentials ») attache à un fichier un historique signé. Des filigranes invisibles sont aussi insérés dans les contenus générés. Mais métadonnées et filigranes peuvent être supprimés, et un contenu sans signature n’est pas forcément faux.", [["C2PA", "provenance signée"], ["limite", "effaçable, adoption partielle"]]),
 ],
 pages=[
  dict(kicker="Chapitre 32 · société", title="Biais, équité et désinformation", sub="ce qu’un modèle reproduit, ce qu’il permet de produire", scene="sourcebiais", body="""
    <p class="lede">Un modèle n’est pas neutre : il hérite de ses données, et il rend facile la fabrication de faux crédibles.</p>
    <p>Ce chapitre traite de deux risques sociaux : les <b>décisions inégales</b> et les <b>contenus trompeurs</b>.</p>"""),
  dict(kicker="32.1", title="D’où viennent les biais", sub="données, étiquettes, proxys", scene="sourcebiais", body="""
    <ul class="rules">
      <li><b>Représentation</b> : certains groupes sont rares dans les données, le modèle y est moins fiable (reconnaissance faciale moins précise sur certains visages).</li>
      <li><b>Étiquettes</b> : des décisions humaines passées biaisées (embauches, crédits) deviennent la « vérité » à imiter.</li>
      <li><b>Proxys</b> : retirer la variable sensible ne suffit pas, d’autres variables (code postal, prénom) la reconstituent.</li>
    </ul>
    <p>Les modèles de langage reflètent aussi les stéréotypes du texte aspiré.</p>"""),
  dict(kicker="32.2", title="Mesurer l’équité", sub="trois définitions", scene="equite", body="""
    <p class="lede">Trois idées courantes : <b>parité démographique</b> (mêmes taux de décisions favorables), <b>égalité des chances</b> (mêmes taux de vrais positifs), <b>calibration</b> (un score de 70 % signifie 70 % pour tous).</p>
    <p>Des résultats théoriques (Kleinberg, Chouldechova, 2016-2017) montrent qu’on ne peut en général pas toutes les satisfaire si les groupes ont des taux de base différents. Il faut <b>choisir</b>, selon l’enjeu et la loi, et documenter ce choix.</p>"""),
  dict(kicker="32.3", title="Auditer et corriger", sub="avant, pendant, après", scene="sourcebiais", body="""
    <ul class="rules">
      <li><b>Avant</b> : diversifier et documenter les données (fiches de données).</li>
      <li><b>Pendant</b> : contraintes d’équité à l’entraînement, rééquilibrage.</li>
      <li><b>Après</b> : mesurer les erreurs <b>par groupe</b>, recours humain, voies de contestation.</li>
    </ul>
    <p>Pour les décisions à fort enjeu (emploi, crédit, justice), l’IA assiste et un humain <b>décide</b> ; la loi l’exige souvent.</p>"""),
  dict(kicker="32.4", title="Contenus synthétiques et désinformation", sub="le faux devient bon marché", scene="provenance", body="""
    <p class="lede">Générer un texte, une image, une voix ou une vidéo crédibles coûte presque rien.</p>
    <p>Risques : <b>hypertrucages</b> (<i>deepfakes</i>) pour l’arnaque ou la manipulation, usurpation de voix, fabrication de faux avis ou de faux comptes, bruit informationnel. Autre effet : le « dividende du menteur », quand un vrai document peut être nié comme « faux ».</p>"""),
  dict(kicker="32.5", title="Provenance et vérification", sub="C2PA, filigranes, bon sens", scene="provenance", body="""
    <ul class="rules">
      <li><b>C2PA</b> : un historique signé attaché au fichier, de la création aux modifications.</li>
      <li><b>Filigranes invisibles</b> dans les contenus générés.</li>
      <li><b>Détecteurs</b> : peu fiables, donc à ne pas prendre pour des preuves.</li>
      <li><b>Réflexes</b> : source, contexte, recoupement, image inversée.</li>
    </ul>
    <p>Aucune technique ne suffit seule : l’absence de signature ne prouve pas que c’est faux.</p>"""),
 ],
 practice={2:[P("Pourquoi ne peut-on en général pas satisfaire toutes les définitions d’équité ?", ["elles sont mathématiquement incompatibles si les taux de base diffèrent", "les ordinateurs sont trop lents", "elles ne sont pas mesurables", "la loi l’interdit"], 0, "Il faut choisir le critère adapté à l’enjeu et le documenter.")],
           1:[P("Retirer la variable « origine » suffit-il à supprimer le biais ?", ["oui, toujours", "non, des variables proxys peuvent la reconstituer", "oui, si le modèle est assez gros", "non, car les modèles n’en ont pas besoin"], 1, "Code postal, prénom, etc. peuvent encoder la même information.")],
           5:[P("Que garantit l’absence de signature C2PA sur une image ?", ["qu’elle est fausse", "qu’elle est vraie", "rien : elle n’est simplement pas signée", "qu’elle est ancienne"], 2, "Beaucoup de contenus authentiques ne sont pas signés ; les métadonnées peuvent aussi être effacées.")]}
),
dict(dir="droit", no=33, title="Droit et gouvernance", sub="AI Act, données personnelles, droit d’auteur, responsabilité", cnt="Les règles qui encadrent l’IA", alt="Une pyramide de niveaux de risque",
 scenes=[
  dict(key="risques", title="Les niveaux de risque", sub="l’approche du règlement européen", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Interdit", s="pratiques inacceptables", pal="red"), dict(n="Haut risque", s="emploi, crédit, santé, justice…", pal="red"), dict(n="Transparence", s="chatbots, contenus générés", pal="blue"), dict(n="Risque minimal", s="la plupart des usages"), dict(n="Modèles généralistes", s="obligations propres", pal="blue"), dict(n="Contrôle", s="autorités, amendes")],
       plate="Le règlement européen sur l’IA (« AI Act », 2024) classe les usages par niveau de risque : certains sont interdits, d’autres « à haut risque » demandent évaluation, documentation et supervision humaine, d’autres imposent la transparence. Les dates d’application sont échelonnées : à vérifier au Journal officiel de l’UE.",
       facts=[["adoption", "règlement (UE) 2024/1689"], ["calendrier", "échelonné, à vérifier"], ["sanctions", "jusqu’à un pourcentage du chiffre d’affaires"]]),
  dict(key="donnees", title="Données personnelles", sub="RGPD et IA", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Base légale", s="consentement, intérêt légitime…", pal="blue"), dict(n="Minimisation", s="seulement le nécessaire", pal="blue"), dict(n="Droits", s="accès, effacement, opposition", pal="red"), dict(n="Décision automatisée", s="droit à intervention humaine", pal="red"), dict(n="Analyse d’impact", s="pour les usages risqués"), dict(n="Sécurité", s="chiffrement, accès, hébergement")],
       plate="Le RGPD s’applique dès qu’un système traite des données de personnes : base légale, minimisation, droits des personnes, encadrement des décisions entièrement automatisées, analyse d’impact. Un modèle entraîné sur des données personnelles pose en plus la question de l’effacement.",
       facts=[["RGPD", "en vigueur depuis 2018"], ["en pratique", "éviter d’envoyer des données sensibles à un service tiers"]]),
  dict(key="auteur", title="Droit d’auteur", sub="entraînement, sorties, licences", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Entraînement", s="exception de fouille ? licence ?", pal="red"), dict(n="Opt-out", s="refus des ayants droit", pal="blue"), dict(n="Sortie", s="peut ressembler à une œuvre", pal="red"), dict(n="Titularité", s="une œuvre générée est-elle protégée ?", pal="blue"), dict(n="Accords", s="licences avec éditeurs"), dict(n="Procès", s="en cours, solutions non stabilisées", pal="red")],
       plate="Trois questions juridiques : peut-on entraîner sur des œuvres protégées (exception de fouille de textes, opt-out, ou licence) ; une sortie qui ressemble trop à une œuvre est-elle une contrefaçon ; une œuvre générée est-elle protégeable. Les réponses varient selon les pays et évoluent avec les jugements.",
       facts=[["UE", "exception de fouille avec droit d’opposition"], ["situation", "contentieux en cours"]]),
  dict(key="monde", title="Les approches dans le monde", sub="trois philosophies", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Union européenne", s="règlement transversal par risques", pal="blue"), dict(n="États-Unis", s="textes sectoriels et d’États, décrets", pal="blue"), dict(n="Chine", s="règles par application, enregistrement", pal="blue"), dict(n="Normes", s="ISO/IEC 42001, NIST AI RMF"), dict(n="Coopération", s="sommets, instituts de sûreté"), dict(n="Tendance", s="réglementation en mouvement", pal="red")],
       plate="L’Union européenne privilégie un règlement transversal fondé sur les risques ; les États-Unis procèdent par textes sectoriels, décrets et lois d’États ; la Chine encadre des applications précises (algorithmes de recommandation, IA générative) avec enregistrement. Des normes volontaires (ISO/IEC 42001, NIST AI RMF) servent de référence commune.",
       facts=[["normes", "ISO/IEC 42001, NIST AI RMF"], ["avertissement", "textes et dates évoluent vite"]]),
 ],
 pages=[
  dict(kicker="Chapitre 33 · droit", title="Droit et gouvernance", sub="ce qu’il faut savoir avant de déployer", scene="risques", body="""
    <p class="lede">Utiliser l’IA en entreprise ou dans un service public engage des règles : données personnelles, droit d’auteur, responsabilité, réglementation propre à l’IA.</p>
    <p>Ce chapitre donne des repères, <b>pas un avis juridique</b> : les textes, calendriers et jugements évoluent vite, et il faut les vérifier à la source avant toute décision.</p>"""),
  dict(kicker="33.1", title="Le règlement européen sur l’IA", sub="par niveaux de risque", scene="risques", body="""
    <ul class="rules">
      <li><b>Interdits</b> : par exemple la notation sociale par les autorités ou l’exploitation de vulnérabilités.</li>
      <li><b>Systèmes à haut risque</b> (emploi, crédit, éducation, santé, justice…) : gestion des risques, qualité des données, documentation, supervision humaine, robustesse.</li>
      <li><b>Obligations de transparence</b> : indiquer qu’on parle à une IA, signaler les contenus générés.</li>
      <li><b>Modèles d’IA à usage général</b> : documentation, politique de droit d’auteur, évaluation renforcée pour les plus puissants.</li>
    </ul>
    <p>Application <b>échelonnée</b> depuis 2024 : <b>vérifier le calendrier au Journal officiel</b>.</p>"""),
  dict(kicker="33.2", title="Données personnelles", sub="le RGPD s’applique", scene="donnees", body="""
    <p class="lede">Dès qu’un prompt, un document ou une base contient des données de personnes, le <b>RGPD</b> s’applique.</p>
    <ul class="rules">
      <li>Savoir <b>pourquoi</b> on traite (base légale) et ne garder que le nécessaire.</li>
      <li>Respecter les <b>droits</b> : accès, rectification, effacement, opposition.</li>
      <li>Encadrer les <b>décisions automatisées</b> ayant des effets importants.</li>
      <li>Réfléchir à l’<b>hébergement</b> : un service en ligne reçoit vos données (chapitre 21 pour le sur site).</li>
    </ul>"""),
  dict(kicker="33.3", title="Droit d’auteur", sub="entraînement et sorties", scene="auteur", body="""
    <p class="lede">Les modèles sont entraînés sur d’immenses corpus qui contiennent des œuvres protégées.</p>
    <p>Plusieurs débats : l’entraînement relève-t-il d’une exception (fouille de textes) ou exige-t-il une licence ; que faire des sorties proches d’une œuvre ; une création générée est-elle protégeable (souvent, sans apport humain créatif, non). Des procès et des accords de licence avec éditeurs sont en cours : <b>aucune règle mondiale stable</b> à ce jour.</p>
    <p>Pratique : vérifier les conditions de l’outil, éviter de faire reproduire une œuvre, garder trace de l’apport humain.</p>"""),
  dict(kicker="33.4", title="Responsabilité et gouvernance interne", sub="qui répond d’une erreur ?", scene="risques", body="""
    <ul class="rules">
      <li><b>Responsabilité</b> : l’organisation qui déploie répond de l’usage ; contrats avec le fournisseur, assurance, preuve des contrôles.</li>
      <li><b>Gouvernance interne</b> : inventaire des usages d’IA, classification par risque, politique d’usage, formation (le règlement européen demande une « maîtrise de l’IA »).</li>
      <li><b>Traçabilité</b> : journaux des requêtes et des décisions, versions de modèles.</li>
      <li><b>Humain dans la boucle</b> pour les décisions à enjeu.</li>
    </ul>"""),
  dict(kicker="33.5", title="Dans le monde", sub="trois philosophies", scene="monde", body="""
    <p class="lede">Aucune approche mondiale unique.</p>
    <p>L’<b>UE</b> a un règlement transversal par risques. Les <b>États-Unis</b> combinent textes sectoriels, décrets et lois d’États. La <b>Chine</b> réglemente des applications précises avec enregistrement des services. Des <b>normes volontaires</b> (ISO/IEC 42001 pour un système de management de l’IA, NIST AI Risk Management Framework) servent de langage commun, et des <b>instituts de sûreté</b> nationaux évaluent les modèles les plus puissants.</p>
    <p>Pour une organisation internationale : viser le niveau d’exigence le plus élevé qui la concerne.</p>"""),
 ],
 practice={1:[P("Comment le règlement européen sur l’IA organise-t-il ses obligations ?", ["selon le niveau de risque de l’usage", "selon la taille du modèle uniquement", "selon le pays du fournisseur seulement", "il n’impose rien"], 0, "Interdit, haut risque, transparence, risque minimal, avec des règles propres aux modèles généralistes.")],
           2:[P("Quelle précaution avant d’envoyer des données de clients à un service d’IA en ligne ?", ["vérifier la base légale, les conditions et l’hébergement", "aucune, c’est anonyme par nature", "les écrire en majuscules", "attendre la fin du mois"], 0, "Le RGPD s’applique à ces données ; un service tiers les reçoit.")],
           3:[P("Où en est le droit d’auteur face à l’entraînement des modèles ?", ["des règles stables et mondiales existent", "les questions sont ouvertes et en contentieux selon les pays", "tout est interdit", "tout est libre partout"], 1, "Exceptions, opt-out, licences et procès coexistent ; la situation évolue.")]}
),
dict(dir="surete", no=34, title="AGI, alignement et sûreté", sub="ce qui est établi, ce qui est débattu", cnt="Les grandes questions sur l’avenir de l’IA", alt="Une flèche d’alignement entre objectif voulu et objectif obtenu",
 scenes=[
  pipe("agi", "Qu’appelle-t-on AGI ?", "une définition floue", [("IA étroite", "une tâche", None), ("IA généraliste", "beaucoup de tâches", "blue"), ("Niveau humain ?", "sur quelle mesure ?", "red"), ("Autonomie", "agir sur de longues durées", "blue"), ("Définitions", "varient selon les acteurs", "red"), ("Débat", "calendrier très incertain", "red")],
       "« AGI » (intelligence artificielle générale) n’a pas de définition consensuelle : égaler un humain sur la plupart des tâches économiques, ou raisonner de façon flexible, ou être autonome ? Les prévisions de calendrier vont de quelques années à jamais ; aucune n’est solide.", [["définition", "pas de consensus"], ["prévisions", "très dispersées"]]),
  pipe("alignement", "Le problème d’alignement", "obtenir ce qu’on veut vraiment", [("Objectif voulu", "intention humaine", None), ("Objectif écrit", "récompense, consigne", "blue"), ("Écart", "spécification imparfaite", "red"), ("Détournement", "exploiter la lettre", "red"), ("Contrôle", "préférences, règles, supervision", "blue"), ("Vérification", "tests, interprétabilité", "blue")],
       "Les modèles optimisent ce qu’on leur donne, pas ce qu’on veut. Un écart entre les deux produit du détournement de récompense (exploiter la lettre de la consigne). L’alignement cherche à réduire cet écart et à le vérifier.", [["exemple", "détournement de récompense"], ["outils", "RLHF, constitution, supervision"]]),
  pipe("risques", "Risques : court, moyen, long terme", "un spectre", [("Aujourd’hui", "erreurs, biais, fraude, désinformation", "blue"), ("Bientôt", "cyberattaques, usage dual, dépendance", "blue"), ("Plus tard", "perte de contrôle ? concentration du pouvoir", "red"), ("Mesures", "évaluations, tests adverses", "blue"), ("Politique", "règles, audits, coopération", "blue"), ("Humilité", "incertitude forte", "red")],
       "Les risques vont de problèmes déjà observés (erreurs, fraude, biais) à des risques plus incertains (usages malveillants avancés, perte de contrôle de systèmes autonomes). Il est utile de ne pas opposer les deux : on traite les premiers tout en préparant les seconds.", [["observé", "erreurs, fraude, biais"], ["incertain", "systèmes très autonomes"]]),
  pipe("sureteprat", "La sûreté en pratique", "des pratiques déjà utilisées", [("Évaluations", "capacités dangereuses", "blue"), ("Red teaming", "attaquer son propre modèle", "red"), ("Garde-fous", "filtres, refus", "blue"), ("Politiques d’échelle", "seuils avant déploiement", "blue"), ("Surveillance", "usage, incidents", None), ("Signalement", "partage d’incidents", None)],
       "Les laboratoires et les régulateurs combinent des évaluations de capacités dangereuses, du red teaming, des garde-fous, des politiques à seuils (on renforce les protections quand une capacité sensible apparaît) et une surveillance des usages.", [["red teaming", "attaque encadrée du modèle"], ["politiques à seuils", "protections graduées"]]),
 ],
 pages=[
  dict(kicker="Chapitre 34 · avenir", title="AGI, alignement et sûreté", sub="séparer les faits, les débats et les spéculations", scene="agi", body="""
    <p class="lede">C’est le sujet où l’on entend le plus d’affirmations assurées, souvent opposées.</p>
    <p>Ce chapitre distingue ce qui est <b>établi</b> (les modèles se trompent, peuvent être détournés, optimisent mal une consigne), ce qui est <b>débattu</b> (le calendrier d’une IA généraliste, l’ampleur des risques à long terme) et ce qui reste <b>spéculatif</b>.</p>"""),
  dict(kicker="34.1", title="Que veut dire AGI ?", sub="un mot, plusieurs sens", scene="agi", body="""
    <p class="lede">Il n’existe pas de définition acceptée. Selon les auteurs : égaler l’humain sur la plupart des tâches économiques, résoudre des problèmes nouveaux, apprendre aussi efficacement qu’un enfant, agir en autonomie longue.</p>
    <p>Les modèles actuels sont très forts sur beaucoup de tâches et fragiles sur d’autres (chapitre 24) : l’image « humain-ou-pas » est trop simple. Les prévisions de date sont très dispersées et peu fiables ; mieux vaut suivre des <b>capacités mesurées</b> que des étiquettes.</p>"""),
  dict(kicker="34.2", title="Le problème d’alignement", sub="optimiser la lettre, pas l’esprit", scene="alignement", body="""
    <p class="lede">On ne sait pas écrire exactement ce qu’on veut ; on écrit un substitut (une récompense, une consigne) et le modèle l’optimise à la lettre.</p>
    <ul class="rules">
      <li><b>Détournement de récompense</b> : un agent trouve une faille du score plutôt que de faire la tâche voulue.</li>
      <li><b>Flagornerie</b> : un modèle entraîné à plaire dit ce que l’utilisateur veut entendre.</li>
      <li><b>Désalignement d’objectifs</b> : un comportement appris qui diffère de l’intention, difficile à voir par les tests seuls.</li>
    </ul>
    <p>Réponses : préférences humaines (RLHF), règles explicites (constitutions), supervision, et interprétabilité (chapitre 30).</p>"""),
  dict(kicker="34.3", title="Un spectre de risques", sub="du déjà observé à l’incertain", scene="risques", body="""
    <ul class="rules">
      <li><b>Déjà observés</b> : erreurs présentées avec assurance, biais, fraude et usurpation, désinformation, fuites de données.</li>
      <li><b>Proches</b> : aide à des cyberattaques, usage dual en biologie ou chimie, dépendance excessive, automatisation sans contrôle.</li>
      <li><b>Plus incertains</b> : systèmes très autonomes difficiles à contrôler, concentration du pouvoir économique ou politique.</li>
    </ul>
    <p>Des chercheurs et des institutions jugent ces derniers sérieux, d’autres les jugent exagérés ; l’incertitude est réelle. Les deux types de risques se traitent en parallèle.</p>"""),
  dict(kicker="34.4", title="La sûreté en pratique", sub="ce que font les acteurs", scene="sureteprat", body="""
    <ul class="rules">
      <li><b>Évaluations</b> avant diffusion, y compris de capacités sensibles.</li>
      <li><b>Red teaming</b> : des équipes attaquent le modèle avant les malveillants.</li>
      <li><b>Politiques à seuils</b> : plus de protections quand une capacité dangereuse apparaît.</li>
      <li><b>Surveillance des usages</b> et partage des incidents.</li>
      <li><b>Instituts publics de sûreté</b> et accords internationaux de coopération.</li>
    </ul>
    <p>Pour une organisation : humain dans la boucle, moindres privilèges pour les agents (chapitres 10 et 22), journaux, plan de repli.</p>"""),
  dict(kicker="34.5", title="Garder l’esprit critique", sub="trois réflexes", scene="agi", body="""
    <ul class="rules">
      <li><b>Chercher les mesures</b> derrière une affirmation : quelle tâche, quel protocole, quel résultat ?</li>
      <li><b>Se méfier des extrêmes</b> : ni « tout est sous contrôle » ni « tout est perdu ».</li>
      <li><b>Regarder les intérêts</b> de qui parle (laboratoire, concurrent, régulateur).</li>
    </ul>
    <p>Et garder en tête la leçon de l’histoire (chapitre 25) : les prévisions de calendrier se sont souvent trompées, dans les deux sens.</p>"""),
 ],
 practice={2:[P("Qu’est-ce que le détournement de récompense ?", ["exploiter la lettre d’une récompense au lieu de faire la tâche voulue", "voler un serveur", "changer de modèle en cours d’entraînement", "supprimer le gradient"], 0, "L’agent optimise le substitut, pas l’intention.")],
           3:[P("Les risques actuels et les risques à long terme…", ["s’excluent : il faut choisir", "se traitent en parallèle", "n’existent pas", "sont identiques"], 1, "On corrige les problèmes observés tout en préparant les plus incertains.")],
           1:[P("Pourquoi l’AGI est-elle difficile à situer dans le temps ?", ["il n’y a pas de définition consensuelle", "les ordinateurs sont trop lents", "c’est interdit par la loi", "le mot est récent"], 0, "Sans définition commune, aucune date n’est comparable.")]}
),
]

ADDITIONS = {
 "cluster": dict(scenes=[pipe("energie", "Où va l’énergie", "du réseau électrique au calcul", [("Réseau électrique", "contrat, mégawatts", None), ("Alimentation", "conversion, pertes", "blue"), ("Puces", "calcul", "red"), ("Chaleur", "presque tout", "red"), ("Refroidissement", "air ou liquide", "blue"), ("Indicateur", "PUE, kWh par requête", None)],
       "Presque toute l’électricité devient de la chaleur qu’il faut évacuer. L’indicateur PUE (énergie totale / énergie des machines) vaut environ 1,1 à 1,5 selon les sites. Ordres de grandeur seulement : les chiffres varient selon le matériel et la charge.", [["PUE", "≈ 1,1 à 1,5"], ["entraînement GPT-3", "ordre de 1 à 2 GWh"], ["inférence", "souvent plus que l’entraînement sur la vie du modèle"]])],
   pages=[dict(kicker="18.5", title="Énergie et sobriété", sub="ce que consomme l’IA", scene="energie", body="""
    <p class="lede">L’IA consomme de l’électricité à deux moments : l’<b>entraînement</b> (une fois, très intense) et l’<b>inférence</b> (chaque requête, pendant des années).</p>
    <ul class="rules">
      <li>GPT-3 : de l’ordre de <b>1 à 2 GWh</b> d’entraînement selon les estimations publiées (estimation, pas mesure).</li>
      <li>Sur la vie d’un modèle très utilisé, l’<b>inférence</b> dépasse souvent l’entraînement.</li>
    </ul>
    <p><b>Sobriété</b> : le plus petit modèle qui suffit, quantification, cache, routage des requêtes faciles vers de petits modèles, mesure des kWh.</p>""")],
   practice={0:[P("Quel facteur domine souvent l’énergie totale d’un modèle très utilisé ?", ["l’inférence cumulée", "le nom du modèle", "la couleur de l’interface", "le nombre de dossiers"], 0, "L’entraînement se fait une fois ; l’inférence se répète à chaque requête.")]}),
 "limites": dict(scenes=[pipe("neurosym", "Neuro-symbolique", "intuition + vérification", [("Modèle neuronal", "propose", "blue"), ("Outil symbolique", "solveur, prouveur, code", "red"), ("Vérification", "exacte et déterministe", "red"), ("Retour", "erreur → nouvelle tentative", "blue"), ("Résultat", "fiable parce que vérifié", None), ("Exemple", "AlphaProof + Lean", None)],
       "Le modèle propose ; un outil symbolique (solveur, prouveur, interpréteur de code) vérifie. L’intuition vient du réseau, la garantie de la vérification exacte. Exemple : des systèmes de preuve mathématique couplés à l’assistant de preuve Lean.", [["idée", "proposer puis vérifier"], ["outils", "code, solveur, prouveur"], ["limite", "il faut un vérificateur"]])],
   pages=[dict(kicker="24.8", title="Symbolique, causal, neuro-symbolique", sub="associer apprentissage et vérification", scene="neurosym", body="""
    <p class="lede">Les réseaux apprennent des corrélations ; ils peinent à garantir un raisonnement exact ou à distinguer cause et corrélation.</p>
    <ul class="rules">
      <li><b>Symbolique</b> : règles, logique, solveurs : exacts mais rigides.</li>
      <li><b>Causal</b> : distinguer « A cause B » de « A accompagne B », pour décider et intervenir.</li>
      <li><b>Neuro-symbolique</b> : un modèle <b>propose</b>, un outil exact <b>vérifie</b> (exécuter le code, prouver le théorème, résoudre la contrainte).</li>
    </ul>
    <p>C’est la logique des <b>agents qui testent leur code</b> (chapitres 9 à 11) : partout où une vérification exacte existe, mieux vaut l’utiliser.</p>""")],
   practice={0:[P("Quel est le principe d’une approche neuro-symbolique ?", ["le réseau propose, un outil exact vérifie", "le réseau remplace toute logique", "l’outil symbolique propose sans vérifier", "on supprime les données"], 0, "L’association donne l’intuition du réseau et la garantie de la vérification.")]}),
 "fabrication": dict(scenes=[pipe("ouvert", "Ouvert ou fermé ?", "ce que contient un modèle publié", [("Poids", "les paramètres appris", "blue"), ("Code", "architecture, inférence", "blue"), ("Données", "souvent non publiées", "red"), ("Recette", "hyperparamètres, étapes", "red"), ("Licence", "usage permis ou limité", "blue"), ("Ouvert au sens fort", "tout est public", None)],
       "Un modèle « à poids ouverts » publie ses paramètres, ce qui permet de l’exécuter chez soi et de l’affiner. Mais données, recette et parfois licence restent fermées : « ouvert » ne veut pas dire entièrement transparent ni libre de tout usage.", [["poids ouverts", "exécutables localement"], ["rare", "données et recette publiques"], ["à lire", "la licence"]])],
   pages=[dict(kicker="5.5", title="Ouvert ou fermé ?", sub="ce qu’on peut vraiment faire d’un modèle", scene="ouvert", body="""
    <p class="lede">Un modèle peut être accessible par une <b>API</b> (fermé) ou publié avec ses <b>poids</b> (ouvert).</p>
    <ul class="rules">
      <li><b>Fermé</b> : simple à utiliser, souvent le plus performant, mais vos données partent chez le fournisseur et le modèle peut changer ou disparaître.</li>
      <li><b>Poids ouverts</b> : exécution locale (chapitres 19, 21, 23), affinage, maîtrise des données ; mais licence à lire (limites d’usage, de taille d’entreprise) et exigences de matériel.</li>
      <li><b>Open source au sens strict</b> : poids, code, données et recette publiés : rare.</li>
    </ul>
    <p>Un choix pragmatique : fermé pour les tâches les plus dures, ouvert pour les données sensibles et les usages à fort volume ; on garde la possibilité de changer.</p>""")],
   practice={0:[P("Un modèle « à poids ouverts » est-il forcément transparent ?", ["oui, tout est public", "non, données, recette ou licence peuvent rester fermées", "oui, mais sans licence", "non, car il n’a pas de poids"], 1, "Les poids permettent l’exécution locale, mais ne disent pas tout de la fabrication.")]}),
}
