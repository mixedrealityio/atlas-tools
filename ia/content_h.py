# Atlas de l'IA : chapitres 25 à 29 (histoire, généralisation, architectures, génération, échelle et raisonnement)
GROUPS = [("Les fondations", ["histoire", "generaliser", "architectures"]), ("Génération, échelle et raisonnement", ["generer", "echelle"])]
CHAPTERS = [
dict(dir="histoire", no=25, title="Soixante-dix ans d’IA", sub="précurseurs, hivers, renaissance, ère du langage", cnt="Pourquoi l’IA avance par vagues", alt="Une frise chronologique de l’intelligence artificielle avec deux hivers",
 scenes=[
  dict(key="frise", title="La frise", sub="de 1940 à aujourd’hui", kind="timeline", **{"from": 1940, "to": 2030}, spans=[dict(a=1974, b=1980, n="1er hiver"), dict(a=1987, b=1993, n="2e hiver")],
       events=[dict(y=1943, n="neurone formel", pal="paper"), dict(y=1950, n="test de Turing"), dict(y=1956, n="Dartmouth", pal="blue"), dict(y=1958, n="perceptron"), dict(y=1969, n="Minsky et Papert"), dict(y=1986, n="rétropropagation", pal="blue"), dict(y=1997, n="Deep Blue"), dict(y=2012, n="AlexNet", pal="blue"), dict(y=2016, n="AlphaGo"), dict(y=2017, n="Transformer", pal="blue"), dict(y=2020, n="GPT-3"), dict(y=2022, n="ChatGPT", pal="red"), dict(y=2024, n="raisonnement et agents")],
       plate="L’IA avance par vagues : des idées, un enthousiasme excessif, une déception, des financements coupés (les « hivers »), puis un renouveau quand le calcul, les données ou une idée nouvelle changent la donne. Les dates sont celles des travaux fondateurs les plus cités.",
       facts=[["hivers", "≈ 1974–1980 et ≈ 1987–1993"], ["déclic de 2012", "données + GPU + algorithmes"], ["déclic de 2017", "le transformeur"]]),
  dict(key="precurseurs", title="Les précurseurs", sub="de la logique à la machine", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Logique formelle", s="Leibniz, Boole, Frege"), dict(n="Calculabilité", s="Gödel, Turing 1936", pal="blue"), dict(n="Neurone formel", s="McCulloch et Pitts 1943", pal="blue"), dict(n="Perceptron", s="Rosenblatt 1958", pal="red")],
       plate="Avant les ordinateurs, la logique avait formalisé le raisonnement ; Turing a défini ce qu’une machine peut calculer ; McCulloch et Pitts ont proposé un modèle mathématique de neurone ; Rosenblatt en a fait une machine qui apprend.",
       facts=[["1936", "machine universelle de Turing"], ["1943", "premier neurone formel"], ["1958", "perceptron"]]),
  dict(key="hivers", title="La mécanique d’un hiver", sub="promesse, déception, coupe, renouveau", kind="cycle", unit="temps", speed=0.4,
       nodes=[dict(n="Promesses", pal="blue"), dict(n="Déception", pal="red"), dict(n="Financements coupés", pal="red"), dict(n="Années calmes"), dict(n="Nouvelle idée", pal="blue")], center="les cycles",
       plate="Chaque hiver suit le même schéma : des promesses disproportionnées, des résultats en deçà, une coupe des financements, puis des années où des chercheurs persévèrent jusqu’à une idée ou une ressource nouvelle (réseaux multicouches, données, GPU).",
       facts=[["1er hiver", "limites du perceptron, rapport Lighthill"], ["2e hiver", "systèmes experts coûteux et fragiles"]]),
  dict(key="renaissance", title="La renaissance de 2012", sub="trois ingrédients réunis", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Données", s="ImageNet : 1,2 million d’images", pal="blue"), dict(n="Calcul", s="GPU de jeu vidéo", pal="blue"), dict(n="Algorithmes", s="rétropropagation, ReLU, dropout", pal="blue"), dict(n="AlexNet", s="2012 : erreur presque divisée par deux", pal="red"), dict(n="Course au deep learning", s="vision, parole, langage")],
       plate="En 2012, AlexNet a gagné le concours ImageNet avec une avance nette sur les méthodes classiques. Elle réunissait de grandes quantités d’images étiquetées, le calcul parallèle de deux GPU et des algorithmes de réseaux profonds éprouvés. Tout le domaine a basculé.",
       facts=[["ImageNet", "≈ 1,2 million d’images d’entraînement"], ["AlexNet", "2 GPU, ≈ 60 millions de paramètres"], ["effet", "le deep learning devient la norme"]]),
  dict(key="langage", title="La marche vers le langage", sub="des séquences au transformeur", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Réseaux récurrents", s="LSTM, années 2010"), dict(n="Attention", s="2014–2015", pal="blue"), dict(n="Transformeur", s="2017", pal="red"), dict(n="Pré-entraînement", s="BERT et GPT, 2018", pal="blue"), dict(n="Échelle", s="GPT-3, 2020", pal="blue"), dict(n="Assistants", s="ChatGPT, 2022", pal="red")],
       plate="Les réseaux récurrents ont mené au mécanisme d’attention, puis au transformeur (2017) qui supprime la récurrence. Le pré-entraînement sur d’immenses textes (2018), l’augmentation d’échelle (2020) et l’alignement par préférences ont donné les assistants de 2022.",
       facts=[["2017", "« Attention is all you need »"], ["2018", "BERT (encodeur), GPT (décodeur)"], ["2022", "assistants grand public"]]),
 ],
 pages=[
  dict(kicker="Chapitre 25 · culture", title="Soixante-dix ans d’IA", sub="comprendre le présent par ses cycles", scene="frise", body="""
    <p class="lede">L’IA n’est pas née en 2022. Elle a connu des enthousiasmes, deux « hivers » et des renaissances.</p>
    <p>Connaître cette histoire aide à juger les promesses d’aujourd’hui : on voit ce qui a été durable (apprendre à partir de données) et ce qui ne l’a pas été (les règles écrites à la main à grande échelle). La frise résume les dates repères ; les pages suivantes racontent les quatre grandes étapes.</p>"""),
  dict(kicker="25.1", title="Précurseurs et Dartmouth", sub="avant 1956, et l’été fondateur", scene="precurseurs", body="""
    <p class="lede">Avant l’ordinateur, la logique avait formalisé le raisonnement (Boole, Frege), et en 1936 Turing définit ce qu’une machine peut calculer.</p>
    <p>En 1943, McCulloch et Pitts proposent un neurone formel. En 1950, Turing pose la question « les machines peuvent-elles penser ? » et propose un test. À l’été 1956, un atelier à Dartmouth réunit McCarthy, Minsky, Shannon et d’autres : le terme « intelligence artificielle » y est adopté.</p>
    <p>En 1958, le <b>perceptron</b> de Rosenblatt montre une machine qui apprend à classer.</p>"""),
  dict(kicker="25.2", title="Les hivers", sub="1974–1980 et 1987–1993", scene="hivers", body="""
    <p class="lede">Deux fois, l’enthousiasme est retombé brutalement.</p>
    <ul class="rules">
      <li><b>Premier hiver</b> (années 1970) : en 1969, Minsky et Papert montrent les limites d’un perceptron à une seule couche ; en 1973, le rapport Lighthill juge sévèrement les résultats au Royaume-Uni. Les financements baissent.</li>
      <li><b>Second hiver</b> (fin des années 1980) : les <b>systèmes experts</b>, bases de règles écrites à la main, coûtent cher à maintenir et se révèlent fragiles ; le marché des machines spécialisées s’effondre.</li>
    </ul>
    <p>Pendant ces périodes, des chercheurs poursuivent : en 1986, la <b>rétropropagation</b> est popularisée et permet d’entraîner des réseaux à plusieurs couches.</p>"""),
  dict(kicker="25.3", title="La renaissance du deep learning", sub="2012", scene="renaissance", body="""
    <p class="lede">En 2012, <b>AlexNet</b> gagne le concours ImageNet avec une erreur presque deux fois moindre que la méthode classique suivante.</p>
    <p>Trois ingrédients se rencontrent : des <b>données</b> (ImageNet, 1,2 million d’images étiquetées), du <b>calcul</b> (des GPU, conçus pour le jeu vidéo, parfaits pour les produits de matrices), et des <b>algorithmes</b> (réseaux profonds, activation ReLU, dropout).</p>
    <p>La vision, puis la parole, puis le langage basculent vers l’apprentissage profond. En 2016, AlphaGo bat un champion de Go en combinant réseaux profonds et recherche.</p>"""),
  dict(kicker="25.4", title="L’ère du langage", sub="du transformeur à l’assistant", scene="langage", body="""
    <p class="lede">Le tournant décisif est l’article de 2017 sur le <b>transformeur</b> (chapitre 2).</p>
    <p>En 2018, <b>BERT</b> (encodeur, qui comprend) et <b>GPT</b> (décodeur, qui prédit) montrent l’intérêt du pré-entraînement sur d’immenses textes. En 2020, GPT-3 et les lois d’échelle (chapitre 29) montrent que plus de calcul donne de meilleures capacités. En 2022, l’affinage par préférences humaines (chapitre 7) donne les assistants grand public.</p>
    <p>Depuis 2024, les modèles de <b>raisonnement</b> et les <b>agents</b> (chapitres 10 et 29) ajoutent du calcul au moment de répondre.</p>"""),
  dict(kicker="25.5", title="Ce que l’histoire enseigne", sub="trois leçons", scene="frise", body="""
    <ul class="rules">
      <li><b>Les cycles sont normaux</b> : un résultat spectaculaire est suivi d’une extrapolation excessive. Se méfier des dates promises.</li>
      <li><b>Les méthodes générales gagnent</b> : Richard Sutton a résumé en 2019 cette « leçon amère » : à long terme, les méthodes qui exploitent le calcul et l’apprentissage l’emportent sur celles qui encodent le savoir humain à la main.</li>
      <li><b>Les ressources déclenchent les idées</b> : le deep learning attendait des données et des GPU. Aujourd’hui, l’énergie, les données de qualité et la fiabilité sont les nouveaux verrous.</li>
    </ul>"""),
 ],
 practice={2:[dict(q="Pourquoi parle-t-on d’« hivers » de l’IA ?", choices=["des périodes où les financements ont chuté après des promesses non tenues", "des périodes où les ordinateurs chauffaient trop", "des saisons de concours", "des pannes de courant"], answer=0, why="<p>Promesses excessives, résultats décevants, baisse des financements.</p>")],
           3:[dict(q="Quels trois ingrédients ont rendu possible la percée de 2012 ?", choices=["données, calcul GPU, algorithmes de réseaux profonds", "robots, caméras, câbles", "satellites, logiciels, brevets", "disques, souris, claviers"], answer=0, why="<p>ImageNet, les GPU et les réseaux profonds éprouvés.</p>")],
           4:[dict(q="En quelle année a été publié l’article sur le transformeur ?", choices=["1986", "2002", "2017", "2022"], answer=2, why="<p>« Attention is all you need », 2017.</p>")]}
),
dict(dir="generaliser", no=26, title="Généraliser", sub="biais, variance, surapprentissage, double descente", cnt="Pourquoi un modèle réussit sur ses exemples et échoue sur les autres", alt="Des courbes d’erreur selon la complexité d’un modèle",
 scenes=[
  dict(key="biaisvar", title="Biais et variance", sub="le compromis classique", kind="curve", fn="biasvar",
       plate="L’erreur d’un modèle sur des données neuves vient de trois sources : le biais (le modèle est trop simple pour la réalité), la variance (il est trop sensible aux exemples particuliers) et le bruit irréductible. Augmenter la complexité baisse le biais et monte la variance : l’erreur totale a une forme en U. Courbes illustratives.",
       facts=[["erreur", "biais² + variance + bruit"], ["trop simple", "sous-apprentissage"], ["trop souple", "surapprentissage"]]),
  dict(key="surapprentissage", title="Entraînement et validation", sub="quand les courbes se séparent", kind="curve", fn="overfit",
       plate="La perte d’entraînement baisse toujours ; la perte de validation (des exemples jamais vus) baisse puis remonte. Le point de séparation est le moment où l’on arrête, ou où l’on régularise.",
       facts=[["jeux", "entraînement / validation / test"], ["règle", "ne jamais régler sur le jeu de test"]]),
  dict(key="remedes", title="Les remèdes au surapprentissage", sub="contraindre, enrichir, arrêter", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Plus de données", s="le meilleur remède", pal="blue"), dict(n="Augmentation", s="variantes des exemples", pal="blue"), dict(n="Pénalité L1 / L2", s="poids petits ou épars"), dict(n="Dropout", s="éteindre des neurones au hasard"), dict(n="Arrêt précoce", s="stopper à la meilleure validation", pal="red"), dict(n="Modèle plus simple", s="moins de paramètres")],
       plate="On peut agir sur les données (en ajouter, les varier) ou sur le modèle : pénaliser les poids trop grands (L2) ou nombreux (L1), éteindre au hasard des neurones pendant l’entraînement (dropout), s’arrêter quand la validation cesse de s’améliorer, ou choisir un modèle plus petit.",
       facts=[["L2", "« weight decay » dans AdamW"], ["dropout", "souvent 0,1 à 0,5"], ["arrêt précoce", "surveiller la validation"]]),
  dict(key="doubledescente", title="La double descente", sub="quand plus de paramètres généralisent mieux", kind="curve", fn="doubledescent",
       plate="Pour de très grands modèles, l’erreur redescend après un pic situé au seuil où le modèle peut juste apprendre tous ses exemples par cœur. C’est la double descente : les très grands réseaux, malgré leurs milliards de paramètres, généralisent. Courbes illustratives.",
       facts=[["pic", "au seuil d’interpolation"], ["après", "l’erreur redescend"], ["raison", "régularisation implicite de la descente de gradient"]]),
 ],
 pages=[
  dict(kicker="Chapitre 26 · fondations", title="Généraliser", sub="le vrai but de l’apprentissage", scene="biaisvar", body="""
    <p class="lede">Apprendre par cœur est facile. L’objectif est de réussir sur des cas <b>jamais vus</b> : c’est la généralisation.</p>
    <p>Presque tous les problèmes pratiques de l’apprentissage (un modèle brillant en laboratoire et médiocre en production, un score qui s’effondre sur de nouveaux clients) sont des problèmes de généralisation. Ce chapitre donne les notions pour les comprendre.</p>"""),
  dict(kicker="26.1", title="Biais et variance", sub="le compromis", scene="biaisvar", body="""
    <p class="lede">Un modèle trop simple (une droite pour des données courbes) a un <b>biais</b> élevé : il se trompe toujours de la même façon. Un modèle trop souple a une <b>variance</b> élevée : son résultat change beaucoup d’un échantillon à l’autre.</p>
    <div class="eq">erreur attendue = biais<sup>2</sup> + variance + bruit</div>
    <p>La courbe en U de la figure est le compromis classique. Le <b>bruit</b> est la part irréductible : même un modèle parfait ne la supprime pas.</p>"""),
  dict(kicker="26.2", title="Le surapprentissage", sub="repérer le moment où l’on apprend par cœur", scene="surapprentissage", body="""
    <p class="lede">Le signe du surapprentissage est l’écart entre l’erreur d’entraînement (très basse) et celle de validation (qui remonte).</p>
    <ul class="rules">
      <li><b>Trois jeux de données</b> : entraînement (pour apprendre), validation (pour régler), test (pour juger une seule fois à la fin).</li>
      <li><b>Fuite de données</b> : si une information du test s’est glissée dans l’entraînement (doublons, même client, futur), le score est faussement flatteur.</li>
      <li><b>Changement de distribution</b> : les données de production diffèrent de celles d’entraînement ; la validation ne le voit pas.</li>
    </ul>"""),
  dict(kicker="26.3", title="Régularisation", sub="contraindre pour mieux généraliser", scene="remedes", body="""
    <p class="lede">Régulariser, c’est rendre le surapprentissage plus difficile.</p>
    <ul class="rules">
      <li><b>L2 (weight decay)</b> : pénalise les gros poids ; <b>L1</b> : pousse beaucoup de poids vers zéro.</li>
      <li><b>Dropout</b> : à chaque étape, éteindre au hasard une fraction des neurones, pour que le réseau ne dépende pas d’un seul.</li>
      <li><b>Arrêt précoce</b> : garder les poids du meilleur point de validation.</li>
      <li><b>Augmentation de données</b> : retourner, recadrer, bruiter les exemples ; pour le texte, reformuler.</li>
    </ul>
    <p>Mais le meilleur remède reste <b>plus de données</b>, plus variées.</p>"""),
  dict(kicker="26.4", title="La double descente", sub="le résultat qui a surpris", scene="doubledescente", body="""
    <p class="lede">Selon la théorie classique, un modèle avec plus de paramètres que d’exemples devrait surapprendre. Or les réseaux actuels ont des milliards de paramètres et généralisent bien.</p>
    <p>La <b>double descente</b> (Belkin et collaborateurs, 2019) décrit ce paradoxe : l’erreur monte jusqu’au seuil où le modèle peut tout juste mémoriser ses données, puis <b>redescend</b> quand on agrandit encore. Parmi les nombreuses solutions qui mémorisent tout, la descente de gradient en choisit une « simple », ce qui joue le rôle d’une régularisation implicite.</p>
    <p>La théorie est encore en construction : c’est un bon rappel que l’intuition classique ne s’applique pas telle quelle aux grands modèles.</p>"""),
 ],
 practice={1:[dict(q="Un modèle trop simple pour les données souffre surtout de…", choices=["variance élevée", "biais élevé", "bruit nul", "fuite de données"], answer=1, why="<p>Il se trompe de façon systématique : c’est le biais.</p>")],
           2:[dict(q="Pourquoi ne règle-t-on pas ses hyperparamètres sur le jeu de test ?", choices=["pour gagner du temps", "le score de test serait faussé : le modèle serait choisi pour lui", "le jeu de test est trop petit", "ce n’est pas interdit"], answer=1, why="<p>Le test sert à juger une seule fois, sans y avoir « triché ».</p>")],
           4:[dict(q="Que décrit la double descente ?", choices=["l’erreur qui remonte après le pic puis redescend avec plus de paramètres", "la descente de deux optimiseurs", "deux couches de neurones", "la perte de deux jeux"], answer=0, why="<p>Au-delà du seuil d’interpolation, l’erreur de test baisse à nouveau.</p>")]}
),
dict(dir="architectures", no=27, title="Au-delà du transformeur", sub="réseaux récurrents, experts, modèles à état, graphes", cnt="Les autres manières de traiter des séquences et des relations", alt="Un réseau récurrent déroulé dans le temps et un routeur d’experts",
 scenes=[
  dict(key="rnn", title="Un réseau récurrent", sub="une mémoire passée de pas en pas", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Mot 1", s="x₁"), dict(n="État h₁", s="résumé de « mot 1 »", pal="blue"), dict(n="État h₂", s="+ « mot 2 »", pal="blue"), dict(n="État h₃", s="+ « mot 3 »", pal="red")],
       plate="Un réseau récurrent lit les mots un par un et conserve un état unique h, mis à jour à chaque mot. Il doit tout résumer dans h : l’information des mots anciens s’efface, et on ne peut pas calculer plusieurs positions en parallèle.",
       facts=[["état", "un vecteur de taille fixe"], ["défaut", "séquentiel, mémoire courte"]]),
  dict(key="lstm", title="Les portes du LSTM", sub="oublier, écrire, lire", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Mémoire de cellule", s="le fil conducteur", pal="blue"), dict(n="Porte d’oubli", s="que garder ?", pal="red"), dict(n="Porte d’entrée", s="que écrire ?", pal="red"), dict(n="Porte de sortie", s="que montrer ?", pal="red")],
       plate="Le LSTM (1997) ajoute une mémoire de cellule et trois portes apprises qui décident quoi oublier, quoi écrire et quoi lire. Cela réduit le problème du gradient qui s’évanouit et permet de retenir plus loin, sans jamais égaler l’attention sur de longs textes.",
       facts=[["inventeurs", "Hochreiter et Schmidhuber, 1997"], ["variante", "GRU : deux portes, plus simple"]]),
  dict(key="cout", title="Le coût de l’attention", sub="n² contre n", kind="curve", fn="complexite",
       plate="L’attention compare chaque jeton à tous les autres : son coût croît comme le carré de la longueur. Les modèles récurrents ou à état ont un coût proportionnel à la longueur, mais retiennent moins bien. Tout l’enjeu est d’obtenir la qualité de l’attention au coût du linéaire.",
       facts=[["attention", "coût ∝ n²"], ["modèle à état", "coût ∝ n"], ["astuce", "FlashAttention : même calcul, moins de mémoire"]]),
  dict(key="moe", title="Mélange d’experts", sub="n’activer qu’une partie du modèle", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Jeton", s="un vecteur"), dict(n="Routeur", s="choisit 2 experts sur 8", pal="red"), dict(n="Expert 3", s="un MLP spécialisé", pal="blue"), dict(n="Expert 7", s="un autre MLP", pal="blue"), dict(n="Somme pondérée", s="des deux sorties"), dict(n="Jeton suivant", s="couche suivante")],
       plate="Dans un mélange d’experts, le MLP d’un bloc est remplacé par plusieurs experts et un routeur. Chaque jeton n’en traverse que deux ou quelques-uns : le modèle a beaucoup de paramètres au total mais peu d’actifs par jeton, donc un coût de calcul réduit.",
       facts=[["exemple", "Mixtral 8×7B : ≈ 47 Md au total, ≈ 13 Md actifs"], ["coût", "toute la mémoire reste nécessaire"]]),
  dict(key="ssm", title="Les modèles à espace d’état", sub="Mamba et les hybrides", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Entrée", s="le jeton courant"), dict(n="État compact", s="taille fixe", pal="blue"), dict(n="Mise à jour sélective", s="dépend de l’entrée", pal="red"), dict(n="Sortie", s="coût linéaire")],
       plate="Les modèles à espace d’état (comme Mamba, 2023) gardent un état de taille fixe mis à jour de façon sélective selon l’entrée, avec un coût linéaire en longueur et un calcul parallélisable à l’entraînement. Des modèles hybrides les mélangent avec des couches d’attention.",
       facts=[["avantage", "contextes très longs, peu de mémoire"], ["limite", "rappel exact moins fiable"]]),
  dict(key="gnn", title="Les réseaux de graphes", sub="raisonner en relations", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4, loop="plusieurs tours",
       stages=[dict(n="Nœud", s="un atome, une personne"), dict(n="Messages", s="des voisins", pal="blue"), dict(n="Agrégation", s="somme, moyenne", pal="blue"), dict(n="Nouvel état", s="du nœud", pal="red")],
       plate="Un réseau de graphes traite des données faites de nœuds et de liens (molécules, réseaux sociaux, routes). À chaque tour, chaque nœud reçoit des messages de ses voisins, les agrège et met à jour son état.",
       facts=[["usages", "molécules, routes, recommandations"], ["principe", "passage de messages"]]),
 ],
 pages=[
  dict(kicker="Chapitre 27 · avancé", title="Au-delà du transformeur", sub="des idées qui complètent ou concurrencent l’attention", scene="rnn", body="""
    <p class="lede">Le transformeur domine, mais il a des défauts : coût quadratique, mémoire de cache, calcul massif. D’autres architectures traitent mieux certains problèmes.</p>
    <p>Ce chapitre rappelle d’où l’on vient (les réseaux récurrents), pourquoi le transformeur l’a emporté, et ce que proposent ses challengers : mélanges d’experts, modèles à état, réseaux de graphes, calcul neuromorphique.</p>"""),
  dict(kicker="27.1", title="Les réseaux récurrents", sub="lire un mot après l’autre", scene="rnn", body="""
    <p class="lede">Avant 2017, on traitait le texte par des <b>réseaux récurrents</b> (RNN).</p>
    <p>Le réseau lit les mots un à un et met à jour un <b>état caché</b> <i>h</i> : le résumé de tout ce qu’il a lu. Pour apprendre, on déroule le réseau dans le temps et on rétropropage.</p>
    <p>Deux défauts : tout doit tenir dans un seul vecteur <i>h</i>, et le calcul est <b>séquentiel</b> : on ne peut pas traiter les mots en parallèle, donc on exploite mal les GPU. De plus, le gradient s’évanouit ou explose sur de longues séquences.</p>"""),
  dict(kicker="27.2", title="LSTM et GRU", sub="des portes pour retenir", scene="lstm", body="""
    <p class="lede">Le <b>LSTM</b> (<i>long short-term memory</i>) ajoute à l’état une <b>mémoire de cellule</b> et trois portes apprises.</p>
    <ul class="rules">
      <li>la porte d’<b>oubli</b> décide ce qu’on efface de la mémoire ;</li>
      <li>la porte d’<b>entrée</b> décide ce qu’on y écrit ;</li>
      <li>la porte de <b>sortie</b> décide ce qu’on en montre.</li>
    </ul>
    <p>Le <b>GRU</b> en est une version plus simple. Ces modèles ont dominé la traduction, la parole et la prévision de séries pendant des années. Ils retiennent mieux que les RNN simples, mais restent séquentiels et limités sur de longs textes.</p>"""),
  dict(kicker="27.3", title="Pourquoi le transformeur a gagné", sub="parallélisme et échelle", scene="cout", body="""
    <p class="lede">Le transformeur traite <b>tous les jetons en parallèle</b> à l’entraînement, ce qui exploite à plein les GPU et permet d’entraîner sur d’énormes corpus.</p>
    <p>Son défaut est le <b>coût de l’attention</b>, quadratique en longueur : doubler le contexte quadruple ce coût. On l’atténue par des astuces de calcul (FlashAttention), des attentions locales ou creuses, et le cache KV (chapitre 3).</p>
    <p>D’où la recherche d’architectures qui gardent la qualité de l’attention au coût d’un calcul linéaire.</p>"""),
  dict(kicker="27.4", title="Mélange d’experts", sub="beaucoup de paramètres, peu d’activés", scene="moe", body="""
    <p class="lede">Dans un <b>mélange d’experts</b> (MoE), un routeur envoie chaque jeton vers quelques experts parmi plusieurs.</p>
    <p>Le modèle gagne en <b>capacité</b> (beaucoup de paramètres au total) sans payer en calcul (peu sont actifs). Mixtral 8×7B, par exemple, a environ 47 milliards de paramètres dont environ 13 milliards actifs par jeton ; certains modèles récents ont plusieurs centaines de milliards au total pour quelques dizaines actifs.</p>
    <p>Mais <b>toute la mémoire</b> doit être disponible, et le routage doit être équilibré pour que tous les experts servent.</p>"""),
  dict(kicker="27.5", title="Modèles à état et hybrides", sub="Mamba", scene="ssm", body="""
    <p class="lede">Les <b>modèles à espace d’état</b> reviennent à un état de taille fixe, mais avec une mise à jour <b>sélective</b> : ce que le modèle retient dépend de l’entrée.</p>
    <p>Mamba (2023) et ses dérivés ont un coût linéaire en longueur et une mémoire constante à l’inférence, très utile pour de très longs contextes. Leur point faible est le rappel exact d’un détail précis lu longtemps avant.</p>
    <p>Une voie prometteuse : les <b>hybrides</b> qui alternent quelques couches d’attention avec des couches à état.</p>"""),
  dict(kicker="27.6", title="Graphes et calcul neuromorphique", sub="d’autres structures", scene="gnn", body="""
    <p class="lede">Les <b>réseaux de graphes</b> (GNN) traitent des données reliées : molécules, routes, réseaux sociaux. Ils sont utilisés en chimie, en prévision de trafic et en recommandation.</p>
    <p>Le calcul <b>neuromorphique</b> s’inspire du cerveau : des neurones qui émettent des impulsions, un calcul piloté par les événements et une consommation très faible. Des puces existent (Loihi d’Intel par exemple) mais restent expérimentales.</p>
    <p>Aucune de ces voies n’a, à ce jour, remplacé le transformeur ; elles le complètent.</p>"""),
 ],
 practice={1:[dict(q="Pourquoi un réseau récurrent exploite-t-il mal les GPU ?", choices=["il calcule les positions l’une après l’autre", "il est trop petit", "il n’a pas de paramètres", "il utilise la vidéo"], answer=0, why="<p>L’état de l’étape n dépend de l’étape n−1 : pas de parallélisme sur la séquence.</p>")],
           3:[dict(q="Quel est le défaut principal de l’attention classique ?", choices=["son coût qui croît comme le carré de la longueur", "elle ne peut pas être entraînée", "elle ignore l’ordre", "elle n’utilise pas de matrices"], answer=0, why="<p>Chaque jeton compare à tous les autres : n × n comparaisons.</p>")],
           4:[dict(q="Dans un mélange d’experts, que reste-t-il nécessaire en mémoire ?", choices=["seulement les experts actifs", "tous les paramètres", "uniquement le routeur", "aucun poids"], answer=1, why="<p>Les experts inactifs d’un jeton servent à d’autres : tout doit être en mémoire.</p>")]}
),
dict(dir="generer", no=28, title="Générer", sub="autoencodeurs, GAN, diffusion, autorégression, audio et vidéo", cnt="Comment une machine fabrique des images, des sons et des vidéos", alt="Un autoencodeur et un duel entre générateur et discriminateur",
 scenes=[
  dict(key="ae", title="L’autoencodeur", sub="compresser puis reconstruire", kind="net", layers=[8, 5, 2, 5, 8], names=["Entrée", "Encodeur", "Espace latent", "Décodeur", "Sortie"], params="goulot de 2 valeurs : une description compacte",
       plate="Un autoencodeur apprend à compresser une donnée en peu de nombres (l’espace latent) puis à la reconstruire. Pour générer, on choisit un point de l’espace latent et on le décode. Le goulot oblige le réseau à garder l’essentiel.",
       facts=[["objectif", "sortie ≈ entrée"], ["espace latent", "la description compacte"], ["version générative", "VAE"]]),
  dict(key="vae", title="L’autoencodeur variationnel", sub="un espace latent bien rangé", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Donnée", s="une image"), dict(n="Encodeur", s="prédit μ et σ", pal="blue"), dict(n="Tirage de z", s="dans une loi normale", pal="red"), dict(n="Décodeur", s="reconstruit", pal="blue"), dict(n="Perte", s="reconstruction + KL"), dict(n="Génération", s="tirer z, décoder", pal="red")],
       plate="Le VAE force l’encodeur à produire une distribution plutôt qu’un point, et une pénalité (KL) la rapproche d’une loi normale. L’espace latent devient continu et bien rangé : tirer un point au hasard et le décoder donne une donnée plausible.",
       facts=[["perte", "reconstruction + divergence KL"], ["défaut", "images souvent floues"]]),
  dict(key="gan", title="Le duel des GAN", sub="un faussaire et un expert", kind="cycle", unit="temps", speed=0.45,
       nodes=[dict(n="Générateur : fabrique", pal="red"), dict(n="Faux exemples"), dict(n="Discriminateur : juge", pal="blue"), dict(n="Retour : qui a gagné ?")], center="jeu à deux",
       plate="Un GAN (2014) oppose deux réseaux : un générateur qui fabrique de faux exemples, et un discriminateur qui distingue le vrai du faux. Chacun progresse contre l’autre. L’entraînement est instable et le générateur peut se limiter à quelques types d’exemples (effondrement de modes).",
       facts=[["inventeur", "Goodfellow et collaborateurs, 2014"], ["difficulté", "entraînement instable"]]),
  dict(key="diffusion2", title="La diffusion, pas à pas", sub="du bruit à l’image", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Bruit pur", s="t = T", pal="dark"), dict(n="Pas de débruitage", s="le réseau prédit le bruit", pal="blue"), dict(n="…× 20 à 50", s="guidé par le texte", pal="blue"), dict(n="Image", s="nette", pal="red")],
       plate="Un modèle de diffusion apprend à retirer un peu de bruit d’une image bruitée. Pour générer, on part de bruit pur et on répète le débruitage, en guidant avec un texte (guidage sans classifieur). Les modèles récents travaillent dans un espace latent compressé et utilisent des transformeurs.",
       facts=[["étapes", "20 à 50 à l’inférence"], ["espace", "latent (plus rapide)"], ["guidage", "texte → image"]]),
  dict(key="auto", title="Autorégression ou diffusion", sub="deux manières de fabriquer", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Autorégressif", s="un jeton après l’autre", pal="blue"), dict(n="Texte, audio, images en jetons", s="même mécanique que le LLM"), dict(n="Séquentiel", s="lent, mais exact et contrôlable"), dict(n="Diffusion", s="toute l’image à la fois", pal="red"), dict(n="Étapes de raffinement", s="du bruit à la netteté"), dict(n="Parallèle", s="rapide, bon pour les images")],
       plate="Deux philosophies : produire une suite de jetons un à un (comme un LLM, appliqué à l’audio ou aux images codées en jetons), ou raffiner un objet complet depuis du bruit. Les images et la vidéo ont surtout choisi la diffusion ; le texte, l’autorégression.",
       facts=[["texte", "autorégressif"], ["images, vidéo", "souvent diffusion"], ["tendance", "mélanger les deux"]]),
  dict(key="audiovisuel", title="Voix, musique, vidéo", sub="du texte au son et à l’image animée", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Texte ou son", s="la demande"), dict(n="Codec neuronal", s="son → jetons", pal="blue"), dict(n="Modèle génératif", s="jetons audio ou latents vidéo", pal="red"), dict(n="Décodeur", s="jetons → forme d’onde, images", pal="blue"), dict(n="Cohérence temporelle", s="le plus dur", pal="red"), dict(n="Sortie", s="voix, musique, vidéo")],
       plate="La voix et la musique sont codées en jetons par un codec neuronal puis générées comme du texte. La vidéo traite des « blocs » d’espace-temps. Le plus difficile est la cohérence dans le temps : visages, objets et physique qui restent stables.",
       facts=[["voix", "quasi indiscernable"], ["vidéo", "physique approximative"], ["coût", "élevé"]]),
 ],
 pages=[
  dict(kicker="Chapitre 28 · avancé", title="Générer", sub="fabriquer plutôt que classer", scene="ae", body="""
    <p class="lede">Classer une image consiste à répondre « c’est un chat ». <b>Générer</b> consiste à produire un chat qui n’existait pas.</p>
    <p>Quatre grandes familles se sont succédé : <b>autoencodeurs variationnels</b>, <b>GAN</b>, <b>modèles de diffusion</b> et <b>modèles autorégressifs</b>. Elles reposent toutes sur l’idée d’apprendre la forme des données pour en tirer de nouvelles.</p>"""),
  dict(kicker="28.1", title="Autoencodeurs et VAE", sub="compresser pour comprendre", scene="vae", body="""
    <p class="lede">Un <b>autoencodeur</b> apprend à compresser une donnée en quelques nombres (l’espace latent) puis à la reconstruire.</p>
    <p>Le <b>VAE</b> y ajoute une contrainte : l’encodeur produit une <b>distribution</b>, rapprochée d’une loi normale par une pénalité. L’espace latent devient continu : en tirant un point au hasard et en le décodant, on obtient une donnée plausible, et on peut interpoler d’un visage à un autre.</p>
    <p>Défaut : les images produites sont souvent floues.</p>"""),
  dict(kicker="28.2", title="Les GAN", sub="un faussaire contre un expert", scene="gan", body="""
    <p class="lede">En 2014, Goodfellow propose d’entraîner <b>deux réseaux l’un contre l’autre</b>.</p>
    <p>Le <b>générateur</b> fabrique de fausses images à partir de bruit ; le <b>discriminateur</b> apprend à distinguer vrai et faux ; le générateur apprend à le tromper. À l’équilibre, les faux sont difficiles à distinguer.</p>
    <p>Les GAN ont donné les premiers visages synthétiques réalistes. Mais l’entraînement est capricieux, et le générateur peut se limiter à quelques types d’images. Les modèles de diffusion les ont largement remplacés.</p>"""),
  dict(kicker="28.3", title="La diffusion", sub="apprendre en débruitant", scene="diffusion2", body="""
    <p class="lede">Les modèles de <b>diffusion</b> (2020) dominent la génération d’images.</p>
    <p>On apprend à <b>retirer un peu de bruit</b> d’une image. Pour générer, on part de bruit pur et on répète 20 à 50 fois. Le <b>guidage</b> par un texte (via un encodeur comme CLIP, chapitre 8) oriente le résultat ; la force du guidage règle le compromis entre fidélité au texte et diversité.</p>
    <p>La <b>diffusion latente</b> (Stable Diffusion, 2022) travaille sur une version compressée de l’image, ce qui a rendu la génération accessible sur un GPU grand public. Des variantes récentes simplifient l’entraînement (<i>flow matching</i>).</p>"""),
  dict(kicker="28.4", title="Autorégression contre diffusion", sub="deux philosophies", scene="auto", body="""
    <p class="lede">Comment fabriquer un objet complexe ?</p>
    <ul class="rules">
      <li><b>Autorégression</b> : le produire pièce par pièce, un jeton après l’autre, comme un LLM. On peut y appliquer les mêmes méthodes (contexte, échantillonnage, chapitre 4) à du texte, de l’audio ou des images en jetons.</li>
      <li><b>Diffusion</b> : partir d’un brouillon (du bruit) et le raffiner en entier à chaque étape.</li>
    </ul>
    <p>Aujourd’hui : texte et code en autorégression, images et vidéo surtout en diffusion, audio des deux. Les modèles multimodaux mêlent souvent les deux.</p>"""),
  dict(kicker="28.5", title="Voix, musique et vidéo", sub="du texte aux médias animés", scene="audiovisuel", body="""
    <ul class="rules">
      <li><b>Voix</b> : depuis WaveNet (2016), la synthèse a gagné en naturel ; des voix sont maintenant presque indiscernables d’une voix réelle, ce qui pose des problèmes d’usurpation (chapitre 32).</li>
      <li><b>Musique</b> : des services générant des chansons à partir d’un texte combinent codec audio, modèle de langage et diffusion.</li>
      <li><b>Vidéo</b> : des modèles comme Sora ou Veo traitent des blocs d’espace-temps ; ils produisent des scènes plausibles, mais violent encore parfois la physique (objets qui apparaissent, mouvements impossibles).</li>
    </ul>
    <p>Le coût de calcul de la vidéo est très supérieur à celui du texte.</p>"""),
  dict(kicker="28.6", title="Contrôler et reconnaître", sub="commander, retoucher, détecter", scene="diffusion2", body="""
    <p class="lede">Générer au hasard ne suffit pas : on veut <b>commander</b>.</p>
    <ul class="rules">
      <li><b>ControlNet</b> et méthodes voisines : imposer une pose, un contour, une carte de profondeur.</li>
      <li><b>Retouche locale</b> (<i>inpainting</i>) : régénérer seulement une zone.</li>
      <li><b>Style et identité</b> : adapter un modèle à un style ou à un personnage avec peu d’exemples (LoRA, chapitre 6).</li>
    </ul>
    <p>Limites : mains, texte dans l’image, cohérence entre images. Et une image générée peut être confondue avec une photo : le chapitre 32 traite de la provenance.</p>"""),
 ],
 practice={1:[dict(q="Qu’apporte la contrainte du VAE par rapport à un autoencodeur simple ?", choices=["un espace latent continu où l’on peut tirer et interpoler", "une image plus grande", "moins de paramètres", "un gradient plus petit"], answer=0, why="<p>L’espace latent est bien rangé : un point tiré au hasard se décode en donnée plausible.</p>")],
           2:[dict(q="Quel est le principe d’un GAN ?", choices=["deux réseaux s’entraînent l’un contre l’autre", "un seul réseau très profond", "un réseau sans poids", "deux ordinateurs en réseau"], answer=0, why="<p>Un générateur fabrique, un discriminateur juge : l’un progresse contre l’autre.</p>")],
           3:[dict(q="Pour générer une image par diffusion, on part de…", choices=["une image réelle", "du bruit pur", "un texte brut", "un maillage 3D"], answer=1, why="<p>On débruite pas à pas, guidé par le texte.</p>")]}
),
dict(dir="echelle", no=29, title="Échelle, émergence et raisonnement", sub="lois d’échelle, chaîne de pensée, calcul à l’inférence", cnt="Pourquoi plus gros donne mieux, et ce qui vient ensuite", alt="Une courbe de perte qui baisse avec le calcul",
 scenes=[
  dict(key="loi", title="La loi de puissance", sub="plus de calcul, moins de perte", kind="curve", fn="scaling",
       plate="Kaplan et collaborateurs (2020) ont montré que la perte d’un modèle de langage baisse selon une loi de puissance en fonction du calcul, des données et des paramètres, sur de nombreux ordres de grandeur. Cette régularité permet de prévoir ce que donnera un entraînement plus grand.",
       facts=[["variables", "paramètres N, données D, calcul C"], ["forme", "perte = plancher + a × C^−α"]]),
  dict(key="optimal", title="Le bon équilibre", sub="Chinchilla : autant de données que de paramètres", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Budget de calcul fixé", s="C ≈ 6 N D", pal="blue"), dict(n="Trop de paramètres", s="peu de données : gaspillage"), dict(n="Trop de données", s="petit modèle : plafond"), dict(n="Optimal (2022)", s="≈ 20 jetons par paramètre", pal="red"), dict(n="Pratique actuelle", s="bien plus : servir moins cher", pal="blue"), dict(n="Compromis", s="entraînement vs inférence")],
       plate="Pour un budget de calcul donné, il existe un équilibre entre taille du modèle et quantité de données. L’étude « Chinchilla » (2022) a trouvé environ 20 jetons par paramètre. Les modèles récents s’entraînent bien plus longtemps, pour obtenir un petit modèle bon marché à servir.",
       facts=[["Chinchilla", "≈ 20 jetons par paramètre"], ["actuel", "souvent plus de 100"], ["raison", "le coût d’inférence domine"]]),
  dict(key="emergence", title="Émergence ou mirage ?", sub="le débat", kind="curve", fn="emergence",
       plate="Certaines capacités semblent apparaître brusquement à partir d’une certaine taille. Selon une analyse critique (2023), l’aspect de saut vient en partie de la mesure : une métrique tout-ou-rien (réponse exacte) donne un saut, une métrique continue donne une progression régulière. Courbes illustratives.",
       facts=[["thèse « émergence »", "sauts à certaines tailles"], ["thèse « mirage »", "effet de la métrique"], ["consensus", "débat ouvert"]]),
  dict(key="cot", title="La chaîne de pensée", sub="raisonner à voix haute", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Question", s="un problème à étapes"), dict(n="Étapes écrites", s="une par une", pal="blue"), dict(n="Vérifications", s="calculs intermédiaires", pal="blue"), dict(n="Réponse", s="déduite des étapes", pal="red")],
       plate="En demandant au modèle d’écrire son raisonnement avant de répondre, on améliore nettement ses réponses aux problèmes à plusieurs étapes : chaque jeton produit devient une étape de calcul supplémentaire. Le raisonnement écrit n’est pas toujours fidèle à ce qui se passe réellement dans le réseau.",
       facts=[["idée", "plus de jetons = plus de calcul"], ["variantes", "autocohérence : voter sur plusieurs chaînes"]]),
  dict(key="testtime", title="Calculer au moment de répondre", sub="le calcul à l’inférence", kind="curve", fn="testtime",
       plate="Les modèles de raisonnement sont entraînés, par renforcement sur des problèmes vérifiables (chapitre 7), à produire de longues réflexions. Leur performance progresse avec le calcul dépensé à répondre : c’est un second axe d’échelle, en plus de l’entraînement. Courbes illustratives.",
       facts=[["axe 1", "calcul d’entraînement"], ["axe 2", "calcul à l’inférence"], ["coût", "plus de jetons, plus lent, plus cher"]]),
  dict(key="murs", title="Les limites de la course à l’échelle", sub="quatre murs", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Données", s="le texte public est fini", pal="red"), dict(n="Énergie", s="mégawatts, réseau électrique", pal="red"), dict(n="Argent", s="milliards par entraînement", pal="red"), dict(n="Fiabilité", s="hallucinations persistent", pal="blue")],
       plate="Quatre obstacles pèsent sur la poursuite de l’échelle : le stock de textes de qualité (que l’on complète par des données synthétiques), l’énergie, le coût, et le fait que certaines limites (faits, physique, fiabilité) ne s’effacent pas seulement avec plus de calcul.",
       facts=[["données synthétiques", "produites par d’autres modèles"], ["autres leviers", "algorithmes, inférence, outils"]]),
 ],
 pages=[
  dict(kicker="Chapitre 29 · avancé", title="Échelle, émergence et raisonnement", sub="pourquoi plus gros, plus longtemps, plus profond", scene="loi", body="""
    <p class="lede">Entre 2018 et 2024, l’essentiel des progrès des modèles de langage est venu d’un <b>changement d’échelle</b> : plus de paramètres, plus de données, plus de calcul.</p>
    <p>Ce chapitre explique la régularité mathématique derrière ces progrès (les lois d’échelle), le débat sur l’<b>émergence</b> de capacités, puis les deux leviers récents : le <b>raisonnement écrit</b> (chaîne de pensée) et le <b>calcul à l’inférence</b>.</p>"""),
  dict(kicker="29.1", title="Les lois d’échelle", sub="une régularité inattendue", scene="loi", body="""
    <p class="lede">En 2020, Kaplan et ses collègues observent que la <b>perte</b> d’un modèle de langage baisse selon une <b>loi de puissance</b> quand on augmente le calcul, les données ou les paramètres, sur plusieurs ordres de grandeur.</p>
    <div class="eq">perte ≈ plancher + <i>a</i> × <i>C</i><sup>−α</sup></div>
    <p>Conséquence pratique : on peut <b>prévoir</b> la perte d’un gros entraînement à partir de petits essais, et justifier un investissement. Conséquence théorique : la perte baisse lentement, et chaque gain demande de multiplier les ressources.</p>"""),
  dict(kicker="29.2", title="Chinchilla et le bon équilibre", sub="la taille et les données", scene="optimal", body="""
    <p class="lede">Avec un budget de calcul donné (≈ 6 × paramètres × jetons), faut-il un gros modèle peu entraîné ou un petit très entraîné ?</p>
    <p>L’étude <b>Chinchilla</b> (2022) a montré que les modèles de l’époque étaient trop gros pour leurs données, et qu’il fallait environ <b>20 jetons par paramètre</b>. Depuis, la pratique a changé : comme on sert un modèle des millions de fois, on préfère un modèle plus petit et <b>beaucoup plus entraîné</b>, qui coûte moins à l’inférence.</p>
    <p>L’optimum dépend donc de ce qu’on compte : le coût d’entraînement seul, ou le coût total de vie du modèle.</p>"""),
  dict(kicker="29.3", title="Les capacités émergentes", sub="un débat ouvert", scene="emergence", body="""
    <p class="lede">Certaines capacités (arithmétique à plusieurs chiffres, certains raisonnements) semblent absentes des petits modèles puis <b>apparaissent brusquement</b> à partir d’une certaine taille.</p>
    <p>Wei et ses collègues (2022) ont décrit ces « capacités émergentes ». Schaeffer et ses collègues (2023) ont répondu que le saut vient en partie de la <b>métrique</b> : une mesure tout-ou-rien (réponse exacte) fait apparaître un saut là où une mesure continue montre une progression régulière.</p>
    <p>Retenez : on ne sait pas toujours prévoir <b>quand</b> un modèle saura faire une tâche, même si la perte moyenne se prévoit bien.</p>"""),
  dict(kicker="29.4", title="La chaîne de pensée", sub="écrire pour raisonner", scene="cot", body="""
    <p class="lede">Écrire les étapes avant la réponse améliore nettement les résultats sur des problèmes à plusieurs étapes.</p>
    <p>Pourquoi ? Un modèle fait un calcul de taille fixe par jeton ; en produisant des jetons intermédiaires, il se donne <b>plus de calcul</b> et un espace de travail. Des variantes : <b>« réfléchissons étape par étape »</b>, quelques exemples de raisonnement, <b>autocohérence</b> (plusieurs chaînes, vote sur la réponse).</p>
    <p>Attention : la chaîne écrite n’est <b>pas toujours fidèle</b> au calcul réel du réseau (chapitre 30) : elle peut être plausible sans être la vraie cause de la réponse.</p>"""),
  dict(kicker="29.5", title="Les modèles de raisonnement", sub="un second axe d’échelle", scene="testtime", body="""
    <p class="lede">Depuis 2024, des modèles sont entraînés par <b>renforcement</b> (chapitre 7) pour produire de longues réflexions avant de répondre, avec une récompense vérifiable (maths, code).</p>
    <p>Résultat : plus le modèle <b>réfléchit longtemps</b>, mieux il réussit, ce qui ajoute un axe d’échelle au moment de l’<b>inférence</b>, et pas seulement à l’entraînement. Le prix : plus de jetons, de la latence, un coût multiplié par la longueur de la réflexion.</p>
    <p>On l’emploie là où la vérification existe (code, mathématiques) ou là où la réponse mérite d’être soignée.</p>"""),
  dict(kicker="29.6", title="Les murs", sub="jusqu’où l’échelle ?", scene="murs", body="""
    <ul class="rules">
      <li><b>Données</b> : le texte public de qualité est un stock fini ; on le complète par des données synthétiques, avec le risque de boucler sur ses propres erreurs.</li>
      <li><b>Énergie</b> : un grand cluster demande des mégawatts (chapitre 18).</li>
      <li><b>Argent</b> : un entraînement de pointe se compte en centaines de millions de dollars ou plus.</li>
      <li><b>Fiabilité</b> : certaines limites ne s’effacent pas avec l’échelle seule (chapitre 24).</li>
    </ul>
    <p>D’où la recherche de nouveaux leviers : <b>algorithmes plus efficaces</b>, calcul à l’inférence, <b>outils</b> et boucles (chapitres 9 à 11), données de meilleure qualité.</p>"""),
 ],
 practice={1:[dict(q="Que permet de faire une loi d’échelle ?", choices=["prévoir la perte d’un gros entraînement à partir de petits essais", "supprimer le bruit des données", "éviter le GPU", "écrire un tokenizer"], answer=0, why="<p>La régularité de la loi de puissance autorise l’extrapolation.</p>")],
           2:[dict(q="Pourquoi entraîne-t-on souvent un petit modèle bien au-delà de l’optimum de Chinchilla ?", choices=["par erreur", "pour qu’il coûte moins cher à servir ensuite", "parce que les données sont gratuites", "pour réduire le vocabulaire"], answer=1, why="<p>Le coût d’inférence cumulé domine : un modèle plus petit et plus entraîné est plus économique.</p>")],
           4:[dict(q="Pourquoi une chaîne de pensée améliore-t-elle les réponses ?", choices=["elle ajoute du calcul sous forme de jetons intermédiaires", "elle réduit la taille du modèle", "elle supprime l’attention", "elle change le vocabulaire"], answer=0, why="<p>Chaque jeton produit est une étape de calcul supplémentaire.</p>")]}
)]
