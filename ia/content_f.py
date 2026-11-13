# Atlas de l'IA : chapitres 20 à 22 (RAG, infrastructure sur site, sécurité)
GROUPS = [("Mettre en production", ["rag", "onprem", "securite"])]
CHAPTERS = [
dict(dir="rag", no=20, title="Le RAG, du prototype à la production", sub="recherche, boucles, wiki, voix", cnt="Ce qui fait qu’un RAG fonctionne vraiment", alt="Un système de recherche qui lit des documents puis répond avec ses sources",
 scenes=[
  dict(key="ingest", title="L’ingestion", sub="de documents à un index", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Documents", s="PDF, pages, tickets"), dict(n="Extraction", s="texte propre, tableaux"), dict(n="Découpage", s="passages cohérents", pal="blue"), dict(n="Plongements", s="un vecteur par passage", pal="blue"), dict(n="Métadonnées", s="source, date, droits"), dict(n="Index", s="vecteurs + mots-clés", pal="red")],
       plate="Avant toute question, on transforme les documents en passages que l’on sait retrouver : extraction du texte, découpage, vecteur par passage, métadonnées (source, date, droits d’accès), puis un index qui sait chercher par le sens et par les mots.",
       facts=[["passage typique", "quelques centaines de jetons"], ["à garder", "source, date, droits"], ["piège", "un mauvais découpage coupe l’information"]]),
  dict(key="requete", title="La recherche et la réponse", sub="chercher large, reclasser, répondre avec sources", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4, loop="reformuler",
       stages=[dict(n="Question", s="de l’utilisateur"), dict(n="Réécriture", s="plus précise", pal="blue"), dict(n="Recherche hybride", s="sens + mots-clés", pal="blue"), dict(n="Reclassement", s="garder les meilleurs", pal="red"), dict(n="Contexte", s="passages + consigne"), dict(n="Réponse", s="avec citations", pal="red")],
       plate="La recherche hybride combine la proximité de sens (vecteurs) et la correspondance exacte (mots-clés, BM25) ; les deux se trompent sur des questions différentes. Un reclassement par un modèle plus fin garde quelques passages, que le modèle cite dans sa réponse.",
       facts=[["fusion", "RRF : somme de rangs"], ["reclassement", "modèle plus précis, plus lent"], ["sortie", "réponse + passages cités"]]),
  dict(key="espace", title="Chercher par le sens", sub="les passages proches de la question", kind="scatter", by=2.4,
       points=[dict(n="question", x=-0.4, y=0.2, c="red"), dict(n="passage A", x=-1.6, y=0.9, c="blue"), dict(n="passage B", x=0.9, y=1.1, c="blue"), dict(n="passage C", x=0.3, y=-0.9, c="blue"), dict(n="hors sujet 1", x=3.4, y=1.4), dict(n="hors sujet 2", x=3.0, y=-1.5), dict(n="hors sujet 3", x=-3.6, y=-1.3)],
       arrows=[["question", "passage A", ""], ["question", "passage B", ""], ["question", "passage C", ""]], walk=["question", "passage A", "passage B", "passage C"], info="les k passages les plus proches sont renvoyés",
       plate="Chaque passage et la question sont des points d’un même espace. On renvoie les k points les plus proches de la question. La qualité dépend des plongements, du découpage, et de ce qu’on demande : une question vague trouve des passages vagues.",
       facts=[["k courant", "5 à 20 avant reclassement"], ["mesure", "angle entre vecteurs (cosinus)"]], cam=dict(az=2, el=4)),
  dict(key="agentique", title="Le RAG en boucle", sub="chercher, lire, juger, recommencer", kind="cycle", unit="temps", speed=0.5,
       nodes=[dict(n="Planifier", pal="blue"), dict(n="Chercher", pal="blue"), dict(n="Lire"), dict(n="Juger : suffisant ?", pal="red"), dict(n="Répondre")], center="boucle jusqu’à preuve",
       plate="Un RAG « agentique » ne cherche pas une seule fois. Il décompose la question, cherche, lit, juge si les passages suffisent, et reformule ou cherche ailleurs sinon. Chaque tour coûte du temps et des jetons, d’où un nombre de tours borné.",
       facts=[["bornes", "tours, jetons, durée"], ["gain", "questions à plusieurs étapes"], ["risque", "boucler sans nouvelle information"]]),
  dict(key="wiki", title="Le wiki tenu par un LLM", sub="compiler la connaissance une fois, la relire ensuite", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4, loop="mise à jour",
       stages=[dict(n="Sources brutes", s="notes, articles, rapports"), dict(n="LLM rédacteur", s="résume, relie, classe", pal="blue"), dict(n="Wiki", s="pages, index, liens", pal="red"), dict(n="Questions", s="lisent le wiki"), dict(n="Contrôle", s="contradictions, pages périmées", pal="blue")],
       plate="Variante décrite début 2026 : au lieu de retrouver des passages bruts à chaque question, un LLM écrit et tient à jour un wiki de pages liées entre elles (un index, des résumés, des renvois). La connaissance est compilée une fois, lisible par un humain, versionnable. Convient aux petits corpus.",
       facts=[["avantage", "lisible, sans base vectorielle"], ["limite", "petits corpus, coût d’écriture"], ["risque", "une erreur écrite est relue partout"]]),
  dict(key="voix", title="Le budget de latence d’un RAG vocal", sub="de la fin de parole au premier son", kind="mem", unit="ms", scale=0.0042, limit=800, limitLabel="budget d’environ 800 ms",
       configs=[dict(n="Séquentiel", segs=[["Fin de parole", 50, "dark"], ["Reconnaissance", 150, "blue"], ["Recherche", 100, "red"], ["LLM : 1er jeton", 400, "blue"], ["Synthèse : 1er son", 150, "paper"]]), dict(n="Recherche en parallèle", segs=[["Fin de parole", 50, "dark"], ["Reconnaissance", 150, "blue"], ["LLM : 1er jeton", 400, "blue"], ["Synthèse : 1er son", 150, "paper"]])],
       info="ordres de grandeur d’un assistant vocal en flux",
       plate="Une conversation vocale naturelle demande de répondre en moins d’une seconde environ. Le budget se partage entre détection de fin de parole, reconnaissance, recherche, premier jeton du LLM et premier son. La recherche, qui dépasse facilement le budget, doit se faire en parallèle ou en cache.",
       facts=[["budget cible", "≈ 800 ms jusqu’au premier son"], ["mesure", "médiane et percentile 95"], ["interruption", "barge-in : couper la voix si on parle"]]),
  dict(key="prod", title="Ce qui industrialise un RAG", sub="cinq chantiers permanents", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Évaluation", s="jeu de référence rejoué", pal="red"), dict(n="Droits d’accès", s="filtrer avant de répondre", pal="red"), dict(n="Fraîcheur", s="réindexer ce qui change", pal="blue"), dict(n="Observabilité", s="traces, métriques, alertes", pal="blue"), dict(n="Coûts", s="cache, modèles adaptés"), dict(n="Sécurité", s="documents non fiables", pal="red")],
       plate="Un RAG de démonstration réussit sur dix questions. En production, il faut mesurer en continu (jeu de questions de référence), respecter les droits d’accès, garder l’index à jour, observer les échecs, maîtriser les coûts, et traiter les documents comme non fiables.",
       facts=[["jeu de référence", "questions + passages attendus"], ["droits", "filtrer à la recherche, pas après"], ["dérive", "silencieuse : à surveiller"]]),
 ],
 pages=[
  dict(kicker="Chapitre 20 · pratique", title="Le RAG, du prototype à la production", sub="faire répondre un modèle avec vos documents", scene="ingest", body="""
    <p class="lede">Un modèle ne connaît ni vos documents, ni les événements récents. Le <b>RAG</b> (<i>retrieval-augmented generation</i>) lui donne les passages utiles <b>au moment de répondre</b>.</p>
    <p>Une démonstration se monte en une après-midi ; un système fiable est un chantier. Ce chapitre décrit les <b>quatre ingrédients</b> d’un RAG qui marche (ingestion, recherche, évaluation, boucle de vérification), une variante (le <b>wiki tenu par un LLM</b>), son usage <b>vocal</b>, et ce qui l’<b>industrialise</b>.</p>"""),
  dict(kicker="20.1", title="L’ingestion", sub="tout se joue avant la question", scene="ingest", body="""
    <p class="lede">La plupart des RAG médiocres le sont à cause de leurs données, pas du modèle.</p>
    <ul class="rules">
      <li><b>Extraction</b> : un PDF mal lu (colonnes mélangées, tableaux aplatis) donne un texte inutilisable.</li>
      <li><b>Découpage</b> : par structure (titres, paragraphes) plutôt que par longueur fixe ; passages de quelques centaines de jetons, avec un peu de chevauchement.</li>
      <li><b>Métadonnées</b> : source, date, auteur, section, droits d’accès. Elles servent à filtrer et à citer.</li>
      <li><b>« Petit pour chercher, grand pour lire »</b> : on cherche sur de petits passages et on donne au modèle le contexte plus large autour.</li>
    </ul>"""),
  dict(kicker="20.2", title="Chercher, reclasser", sub="le sens et les mots", scene="requete", body="""
    <p class="lede">Chercher par le sens (vecteurs) échoue sur les références exactes : un code d’erreur, un nom propre, un numéro de pièce.</p>
    <p>On combine donc la <b>recherche vectorielle</b> et la <b>recherche par mots-clés</b> (BM25), et on fusionne les classements (par exemple par somme des inverses des rangs). Puis un <b>modèle de reclassement</b>, plus précis mais plus lent, trie les quelques dizaines de candidats pour n’en garder que cinq à dix.</p>
    <p>Une <b>réécriture de la question</b> par le modèle (la préciser, la décomposer) améliore souvent le rappel pour peu de coût.</p>"""),
  dict(kicker="20.3", title="Mesurer", sub="sans évaluation, on ne progresse pas", scene="espace", body="""
    <p class="lede">On évalue séparément la <b>recherche</b> et la <b>réponse</b>.</p>
    <ul class="rules">
      <li><b>Recherche</b> : le bon passage est-il parmi les <i>k</i> premiers ? (rappel@<i>k</i>, rang moyen du premier bon résultat.)</li>
      <li><b>Réponse</b> : est-elle <b>fidèle</b> aux passages (pas d’invention) et <b>pertinente</b> pour la question ? Mesurée par des relecteurs ou par un modèle juge, avec ses biais.</li>
    </ul>
    <p>La base de l’évaluation est un <b>jeu de référence</b> : quelques dizaines à centaines de vraies questions, avec les passages et les réponses attendus. On le rejoue à chaque changement de découpage, de modèle ou de consigne. Sans cela, une amélioration sur un cas en dégrade silencieusement dix autres.</p>"""),
  dict(kicker="20.4", title="Le RAG en boucle", sub="chercher, juger, recommencer", scene="agentique", body="""
    <p class="lede">Une seule recherche ne suffit pas pour une question comme « comment le contrat X diffère-t-il du contrat Y ? ».</p>
    <p>Un RAG <b>agentique</b> décompose la question, cherche pour chaque partie, <b>juge si les passages suffisent</b>, et reformule ou élargit sinon. Il peut aussi vérifier sa réponse contre les sources avant de la rendre.</p>
    <p>Ce que cela exige (chapitre 11) : des <b>bornes</b> (nombre de tours, jetons, durée), une détection de l’absence de progrès, et une sortie honnête (« je n’ai pas trouvé ») plutôt qu’une réponse inventée.</p>"""),
  dict(kicker="20.5", title="Le wiki tenu par un LLM", sub="une alternative pour les petits corpus", scene="wiki", body="""
    <p class="lede">Idée décrite début 2026 par des comptes rendus de blog : plutôt que de retrouver des passages bruts à chaque question, un LLM <b>écrit et tient à jour un wiki</b>.</p>
    <p>Il lit les sources, rédige des pages de synthèse, crée un index et des liens, et repasse périodiquement pour signaler les contradictions. Les questions lisent ce wiki, en texte simple, lisible par un humain et versionnable. La recherche reste utile pour retrouver la bonne page.</p>
    <p>Limites : adapté à des corpus de taille modeste (quelques dizaines de milliers de jetons à quelques centaines de pages) ; une erreur écrite dans le wiki est relue partout ; l’écriture coûte des appels au modèle. Au-delà, le RAG classique reprend l’avantage.</p>"""),
  dict(kicker="20.6", title="Le RAG vocal", sub="quand la réponse doit venir en moins d’une seconde", scene="voix", body="""
    <p class="lede">Un <b>assistant vocal</b> enchaîne détection de fin de parole, reconnaissance, recherche, modèle, synthèse vocale. Le tout doit commencer à répondre en moins d’une seconde environ.</p>
    <ul class="rules">
      <li><b>Flux partout</b> : reconnaissance, LLM et synthèse fonctionnent en continu, sans attendre la fin de l’étape précédente.</li>
      <li><b>Recherche en parallèle</b> ou en cache, souvent démarrée avant la fin de la phrase.</li>
      <li><b>Interruption</b> (<i>barge-in</i>) : si l’utilisateur reprend la parole, la synthèse s’arrête aussitôt.</li>
      <li><b>Mesurer le percentile 95</b>, pas la moyenne : une réponse lente sur vingt casse l’impression de naturel.</li>
    </ul>"""),
  dict(kicker="20.7", title="Industrialiser", sub="ce qui reste après la démonstration", scene="prod", body="""
    <p class="lede">Six chantiers font la différence entre un prototype et un service.</p>
    <ul class="rules">
      <li><b>Évaluation continue</b> sur le jeu de référence, à chaque changement.</li>
      <li><b>Droits d’accès</b> : filtrer les passages <b>à la recherche</b> selon l’utilisateur ; filtrer après la réponse est trop tard.</li>
      <li><b>Fraîcheur</b> : réindexer ce qui change, supprimer ce qui disparaît.</li>
      <li><b>Observabilité</b> : tracer chaque requête (question, passages, réponse, durée, coût) pour comprendre les échecs.</li>
      <li><b>Coût</b> : cache, modèle plus petit pour la réécriture, reclassement limité.</li>
      <li><b>Sécurité</b> : un document peut contenir des consignes cachées (chapitre 22) ; traiter le contenu retrouvé comme une donnée.</li>
    </ul>"""),
 ],
 practice={1:[dict(q="Pourquoi découpe-t-on les documents en passages avant de les indexer ?", choices=["pour réduire la taille du disque", "pour retrouver des unités précises et tenir dans le contexte du modèle", "pour supprimer les doublons", "pour chiffrer les données"], answer=1, why="<p>Un passage ciblé est plus facile à retrouver et laisse de la place dans le contexte.</p>")],
           2:[dict(q="Pourquoi combiner recherche vectorielle et par mots-clés ?", choices=["pour économiser de la mémoire", "parce que chacune rate des cas que l’autre trouve (références exactes, sens)", "pour éviter le reclassement", "parce que le vectoriel est interdit"], answer=1, why="<p>Les vecteurs captent le sens, les mots-clés captent les termes exacts : elles se complètent.</p>")],
           3:[dict(q="Quel est le rôle d’un jeu de référence ?", choices=["entraîner le modèle", "rejouer des questions connues pour détecter une régression", "remplacer l’index", "chiffrer les réponses"], answer=1, why="<p>Il permet de mesurer l’effet de chaque changement sur des cas connus.</p>")],
           6:[dict(q="Où faut-il appliquer les droits d’accès dans un RAG d’entreprise ?", choices=["après la génération de la réponse", "au moment de la recherche, avant de donner les passages au modèle", "uniquement à l’ingestion", "nulle part"], answer=1, why="<p>Un passage interdit ne doit jamais atteindre le contexte du modèle.</p>")]}
),
dict(dir="onprem", no=21, title="Une infrastructure IA sur site", sub="cadrer, dimensionner, construire, exploiter", cnt="Les étapes pour passer d’un serveur à un service", alt="Les étapes de construction d’une infrastructure d’IA sur site",
 scenes=[
  dict(key="etapes", title="Neuf étapes", sub="du besoin à l’exploitation", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Cadrer", s="usages, données, volumes", pal="blue"), dict(n="Dimensionner", s="mémoire, débit, marge", pal="blue"), dict(n="Matériel", s="GPU, serveurs, alimentation"), dict(n="Réseau et stockage", s="modèles, données"), dict(n="Plateforme", s="conteneurs, orchestrateur", pal="red"), dict(n="Service d’inférence", s="moteur + passerelle", pal="red"), dict(n="Sécurité", s="accès, journaux, cloisonnement", pal="red"), dict(n="Observabilité", s="métriques, alertes"), dict(n="Exploitation", s="mises à jour, capacité")],
       plate="Une infrastructure d’IA sur site se construit dans cet ordre : cadrer les usages, dimensionner, acquérir et installer, relier au réseau et au stockage, bâtir la plateforme, exposer le service, sécuriser, observer, puis exploiter dans la durée.",
       facts=[["délai typique", "des mois : le matériel est souvent l’attente"], ["erreur courante", "acheter avant de cadrer"]]),
  dict(key="dimension", title="Un exemple de dimensionnement", sub="un modèle de 70 milliards pour 20 utilisateurs", kind="mem", scale=0.03, limit=160, limitLabel="2 GPU de 80 Go",
       configs=[dict(n="Besoin total", segs=[["Poids 70B en 4 bits", 43, "blue"], ["Cache : 20 × 8 000 jetons", 50, "red"], ["Marge 10 %", 9, "paper"]])],
       info="cache de 320 Ko par jeton (80 couches, 8 têtes KV de 128, 16 bits)",
       plate="Un modèle de 70 milliards de paramètres en 4 bits pèse environ 43 Go. Vingt utilisateurs avec 8 000 jetons de contexte chacun ajoutent environ 50 Go de cache KV. Avec une marge, le besoin approche 100 Go : deux GPU de 80 Go, en prévoyant de la redondance en plus.",
       facts=[["cache par jeton", "≈ 320 Ko"], ["20 × 8 000 jetons", "≈ 50 Go"], ["redondance", "un GPU ou un nœud de plus (N+1)"]], cam=dict(az=4, el=4)),
  dict(key="plateforme", title="La plateforme en couches", sub="du GPU à l’application", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Applications", s="chat, RAG, agents"), dict(n="Passerelle API", s="authentification, quotas, journaux", pal="red"), dict(n="Routage de modèles", s="le bon modèle pour chaque usage", pal="blue"), dict(n="Moteurs d’inférence", s="vLLM, llama.cpp…", pal="blue"), dict(n="Orchestrateur", s="Kubernetes + pilotes GPU"), dict(n="GPU et stockage", s="poids, cache, données", pal="red")],
       plate="Les applications ne parlent jamais directement aux GPU : une passerelle gère authentification, quotas et journaux ; un routeur choisit le modèle ; des moteurs d’inférence servent les requêtes ; un orchestrateur place les charges sur les GPU.",
       facts=[["passerelle", "un point d’entrée unique"], ["moteur", "par lots continus"], ["orchestrateur", "plugin GPU, files d’attente"]]),
  dict(key="rentabilite", title="Sur site ou cloud ?", sub="un exemple de point d’équilibre", kind="curve", fn="breakeven",
       plate="Le cloud n’a pas de coût d’entrée mais un coût mensuel élevé ; le matériel sur site demande un investissement puis des frais d’exploitation modestes. Selon l’usage, les courbes se croisent après quelques années. Chiffres d’exemple, à remplacer par les vôtres.",
       facts=[["point d’équilibre ici", "≈ 30 mois"], ["inconnues", "taux d’occupation, personnel, énergie"]]),
 ],
 pages=[
  dict(kicker="Chapitre 21 · avancé", title="Une infrastructure IA sur site", sub="posséder ses modèles et ses données", scene="etapes", body="""
    <p class="lede">Faire tourner ses modèles <b>chez soi</b> répond à trois besoins : garder des <b>données confidentielles</b> chez soi, maîtriser la <b>latence</b> et les <b>coûts</b> quand l’usage est constant, et ne pas dépendre d’un fournisseur.</p>
    <p>Le prix : on devient responsable du matériel, des mises à jour, de la sécurité et de la disponibilité. Une machine qui fait tourner un modèle n’est pas un <b>service</b> ; ce chapitre décrit les neuf étapes pour passer de l’un à l’autre.</p>"""),
  dict(kicker="21.1", title="Cadrer le besoin", sub="avant d’acheter quoi que ce soit", scene="etapes", body="""
    <p class="lede">Les questions qui décident de tout le reste :</p>
    <ul class="rules">
      <li><b>Qui</b> utilise, combien en même temps (pointe, pas moyenne) ?</li>
      <li><b>Quoi</b> : chat, RAG, code, voix, images ? quelle taille de modèle, quelle longueur de contexte ?</li>
      <li><b>Quel niveau de qualité</b> : un modèle plus petit suffit-il ? On le vérifie avec un jeu d’essais réels.</li>
      <li><b>Quelles données</b> : lesquelles ne doivent jamais sortir ? quelles obligations (conservation, journalisation, droit d’accès) ?</li>
      <li><b>Quelle disponibilité</b> : acceptable d’être indisponible une nuit ? un week-end ?</li>
    </ul>"""),
  dict(kicker="21.2", title="Dimensionner", sub="mémoire d’abord, puis débit", scene="dimension", body="""
    <p class="lede">La contrainte de départ est la <b>mémoire des GPU</b> (chapitre 16) : poids + cache KV de tous les utilisateurs + marge.</p>
    <p>Pour un modèle de 70 milliards en 4 bits (≈ 43 Go) et 20 utilisateurs à 8 000 jetons (≈ 50 Go de cache), il faut près de 100 Go : deux GPU de 80 Go. Ensuite le <b>débit</b> : jetons par seconde et par utilisateur attendus, sachant que la vitesse de décodage est bornée par la bande passante mémoire (chapitre 17).</p>
    <p>Prévoir une <b>redondance</b> (un GPU ou un nœud de plus) pour tenir une panne ou une maintenance sans coupure.</p>"""),
  dict(kicker="21.3", title="Construire la plateforme", sub="matériel, réseau, logiciels", scene="plateforme", body="""
    <ul class="rules">
      <li><b>Matériel</b> : serveurs GPU, alimentation et refroidissement dimensionnés pour la puissance (chapitre 18), prise de courant et climatisation de la salle.</li>
      <li><b>Réseau</b> : réseau rapide entre nœuds si plusieurs serveurs servent un même modèle ; réseau séparé pour l’administration.</li>
      <li><b>Stockage</b> : un dépôt de poids de modèles (plusieurs dizaines à centaines de Go chacun), les index de RAG, les journaux.</li>
      <li><b>Logiciels</b> : pilotes GPU, conteneurs, un orchestrateur (souvent Kubernetes avec le plugin GPU), un moteur d’inférence (vLLM pour la production, Ollama pour les essais), une passerelle API.</li>
      <li><b>Registre de modèles</b> : versions, licences, empreintes de fichiers.</li>
    </ul>"""),
  dict(kicker="21.4", title="Sécuriser et gouverner", sub="la partie qui se négocie avec la direction", scene="etapes", body="""
    <ul class="rules">
      <li><b>Accès</b> : authentification forte, droits par équipe, clés par application, quotas.</li>
      <li><b>Cloisonnement</b> : réseau dédié, pas d’accès sortant non contrôlé depuis les moteurs.</li>
      <li><b>Journaux</b> : qui a demandé quoi, quand, avec quel modèle ; conservés selon la politique de l’organisation.</li>
      <li><b>Données</b> : durée de conservation des conversations, anonymisation, droit à l’effacement.</li>
      <li><b>Modèles</b> : vérifier la licence de chaque modèle et la provenance des fichiers.</li>
      <li><b>Cadre légal</b> : protection des données personnelles et obligations propres au secteur ; à valider avec le juriste.</li>
    </ul>"""),
  dict(kicker="21.5", title="Exploiter", sub="surveiller, mettre à jour, ajuster", scene="plateforme", body="""
    <p class="lede">Un service d’IA se surveille par des mesures spécifiques.</p>
    <ul class="rules">
      <li><b>Utilisateur</b> : temps avant le premier jeton, jetons par seconde, taux d’erreurs.</li>
      <li><b>Moteur</b> : longueur de la file, occupation du cache KV, taille des lots.</li>
      <li><b>GPU</b> : utilisation, mémoire, température, erreurs matérielles.</li>
    </ul>
    <p>On fixe des <b>objectifs de service</b> (par exemple le temps du premier jeton), on teste un nouveau modèle sur le jeu d’essais avant de basculer, et on garde un retour arrière. On suit aussi la <b>capacité</b> : quand la file s’allonge aux heures de pointe, on ajoute des GPU avant que les utilisateurs ne s’en plaignent.</p>"""),
  dict(kicker="21.6", title="Sur site ou cloud", sub="un calcul, pas une idéologie", scene="rentabilite", body="""
    <p class="lede">Le choix dépend du <b>taux d’occupation</b> des GPU.</p>
    <p>Un GPU occupé en permanence revient moins cher sur site au bout de quelques années ; un GPU utilisé quelques heures par semaine revient moins cher à louer. Le calcul doit inclure l’énergie, le local, le personnel, le renouvellement du matériel (les GPU vieillissent vite) et le coût du risque.</p>
    <p>Une voie courante : <b>hybride</b>. Sur site, les données et les usages stables ; dans le cloud, les pointes, les essais de nouveaux modèles et l’entraînement ponctuel.</p>"""),
 ],
 practice={2:[dict(q="Quelles deux consommations de mémoire additionner pour dimensionner un serveur d’inférence ?", choices=["les poids et le cache KV de tous les utilisateurs", "les images et le son", "le disque et l’écran", "les journaux et les sauvegardes"], answer=0, why="<p>Les poids sont fixes ; le cache grandit avec les utilisateurs et les contextes.</p>")],
           5:[dict(q="Dans quel cas l’achat de GPU sur site est-il le plus rentable ?", choices=["usage occasionnel", "GPU occupés en permanence pendant des années", "essais ponctuels", "jamais"], answer=1, why="<p>L’investissement s’amortit si le matériel travaille presque tout le temps.</p>")]}
),
dict(dir="securite", no=22, title="Jailbreaks et défenses", sub="pourquoi un modèle se laisse détourner, comment s’en protéger", cnt="Défense en profondeur avec des garde-fous open source", alt="Plusieurs couches de protection autour d’un modèle",
 scenes=[
  dict(key="couches", title="Défense en profondeur", sub="aucune couche ne suffit seule", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Entrée", s="requête + contexte"), dict(n="Filtre d’entrée", s="classifieur de risques", pal="red"), dict(n="Modèle", s="aligné, consignes claires", pal="blue"), dict(n="Filtre de sortie", s="contenu, fuites", pal="red"), dict(n="Outils", s="permissions minimales", pal="red"), dict(n="Journal", s="trace et alerte", pal="blue")],
       plate="Les protections se superposent : un filtre à l’entrée, un modèle entraîné à refuser, un filtre à la sortie, des outils aux droits minimaux, et une trace de tout. Chaque couche arrête une partie des attaques ; aucune ne les arrête toutes.",
       facts=[["principe", "plusieurs barrières indépendantes"], ["à ne pas faire", "tout confier au prompt système"]]),
  dict(key="canal", title="Le problème de fond : un seul canal", sub="instructions et données se mélangent", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Consignes du système", s="fiables", pal="blue"), dict(n="Demande de l’utilisateur", s="à vérifier"), dict(n="Documents, pages, courriels", s="non fiables", pal="red"), dict(n="Contexte unique", s="tout est du texte"), dict(n="Le modèle", s="ne distingue pas parfaitement", pal="red"), dict(n="Actions", s="si des outils sont branchés", pal="red")],
       plate="Pour un modèle, consignes, question et documents sont du texte dans le même contexte. Un contenu extérieur (page web, courriel, fichier) peut donc contenir des ordres que le modèle prend pour légitimes : c’est l’injection de consignes, directe ou indirecte.",
       facts=[["injection directe", "dans la demande"], ["injection indirecte", "dans un contenu lu par le modèle"], ["risque max", "quand des outils agissent"]]),
  dict(key="redteam", title="La boucle de l’équipe rouge", sub="attaquer pour mieux défendre", kind="cycle", unit="temps", speed=0.5,
       nodes=[dict(n="Attaquer (autorisé)", pal="red"), dict(n="Mesurer", pal="blue"), dict(n="Corriger"), dict(n="Retester", pal="blue")], center="en continu",
       plate="Tester ses défenses est un travail régulier : une équipe, ou un outil, tente de détourner le système avec des attaques connues ; on mesure le taux de réussite ; on corrige (consignes, filtres, droits des outils) ; on retest, y compris les cas anciens.",
       facts=[["mesure principale", "taux de réussite des attaques"], ["à surveiller aussi", "les refus injustifiés"]]),
 ],
 pages=[
  dict(kicker="Chapitre 22 · avancé", title="Jailbreaks et défenses", sub="un modèle n’obéit pas à une règle, il suit une tendance", scene="couches", body="""
    <p class="lede">Un modèle n’a pas de règle de sécurité gravée : il a appris, par entraînement, à <b>refuser</b> certaines demandes. Ce comportement peut être contourné ; on parle de <b>jailbreak</b>.</p>
    <p>Ce chapitre explique <b>pourquoi</b> cela arrive et <b>comment s’en protéger</b>, y compris avec des modèles ouverts. Il décrit les attaques à un niveau général pour mieux se défendre ; il ne donne pas de méthode détaillée pour en monter.</p>"""),
  dict(kicker="22.1", title="Pourquoi ça arrive", sub="trois causes de fond", scene="canal", body="""
    <ul class="rules">
      <li><b>Objectifs concurrents</b> : le modèle est entraîné à être utile <b>et</b> à refuser ; une formulation qui fait pencher vers l’utilité peut l’emporter.</li>
      <li><b>Généralisation incomplète</b> : le refus est appris sur des exemples ; une demande formulée autrement (langue rare, codage, mise en scène) peut sortir du domaine couvert.</li>
      <li><b>Un seul canal</b> : consignes, question et documents sont du texte dans le même contexte ; le modèle ne sépare pas parfaitement ce qu’on lui demande de ce qu’il lit.</li>
    </ul>
    <p>Conséquence : on ne peut pas « corriger » définitivement un modèle. Il faut des protections <b>autour</b> de lui.</p>"""),
  dict(kicker="22.2", title="Les familles d’attaques", sub="un aperçu, côté défense", scene="canal", body="""
    <ul class="rules">
      <li><b>Injection directe</b> : l’utilisateur demande au modèle d’ignorer ses consignes.</li>
      <li><b>Injection indirecte</b> : des instructions cachées dans un document, une page web ou un courriel que le système lit.</li>
      <li><b>Mise en scène</b> : faire jouer un rôle, un récit ou une hypothèse pour obtenir ce que la demande directe n’obtiendrait pas.</li>
      <li><b>Brouillage</b> : changer de langue, coder, fragmenter ou masquer le contenu pour échapper aux filtres.</li>
      <li><b>Conversations longues</b> : avancer par petites étapes, ou saturer le contexte d’exemples.</li>
      <li><b>Attaques automatisées</b> : des programmes cherchent des formulations qui marchent.</li>
    </ul>"""),
  dict(kicker="22.3", title="Se protéger", sub="défense en profondeur", scene="couches", body="""
    <p class="lede">La règle de base : <b>ne jamais compter sur le modèle seul</b> pour protéger quelque chose d’important.</p>
    <ul class="rules">
      <li><b>Droits minimaux</b> : un agent ne reçoit que les outils et les données dont il a besoin ; les actions sensibles demandent la confirmation d’un humain.</li>
      <li><b>Séparer instructions et données</b> : marquer clairement le contenu extérieur comme une donnée, ne pas lui obéir.</li>
      <li><b>Filtrer l’entrée et la sortie</b> avec des classifieurs, et vérifier les actions demandées avant de les exécuter.</li>
      <li><b>Isoler et tracer</b> : code en bac à sable ; tout comportement inhabituel doit se voir.</li>
    </ul>"""),
  dict(kicker="22.4", title="Les garde-fous ouverts", sub="des modèles et des outils à brancher", scene="couches", body="""
    <p class="lede">Des classifieurs de sécurité à poids ouverts existent, que l’on branche avant et après le modèle principal.</p>
    <ul class="rules">
      <li><b>Llama Guard</b> (Meta) et <b>ShieldGemma</b> (Google) : classent une requête ou une réponse selon des catégories de risques.</li>
      <li><b>Granite Guardian</b> (IBM) : modèle de garde, y compris pour des contrôles de fidélité d’un RAG.</li>
      <li><b>NeMo Guardrails</b> (NVIDIA) : cadre pour définir des règles de dialogue autour d’un modèle.</li>
      <li><b>LLM Guard</b> et d’autres bibliothèques : filtres déterministes (données personnelles, secrets, formats).</li>
    </ul>
    <p>Aucun n’est infaillible : des études montrent qu’ils peuvent eux-mêmes être contournés. On les <b>combine</b> et on les <b>reteste</b>.</p>"""),
  dict(kicker="22.5", title="Tester et mesurer", sub="red teaming et jeux d’évaluation", scene="redteam", body="""
    <p class="lede">Une défense non testée est une hypothèse.</p>
    <ul class="rules">
      <li><b>Équipe rouge</b> : des personnes autorisées essaient de détourner le système, avec un périmètre et des règles écrits.</li>
      <li><b>Jeux d’évaluation publics</b> (par exemple HarmBench, JailbreakBench) : mesurent le taux de réussite d’attaques connues.</li>
      <li><b>Deux mesures</b> : le taux d’attaques qui réussissent, <b>et</b> le taux de refus injustifiés (un système trop prudent est inutilisable).</li>
      <li><b>En continu</b> : rejouer à chaque changement de modèle ou de consigne, et ajouter chaque incident réel au jeu d’essais.</li>
    </ul>"""),
 ],
 practice={1:[dict(q="Pourquoi un contenu lu par un agent (page web, courriel) est-il dangereux ?", choices=["il est trop long", "il peut contenir des consignes que le modèle prend pour des ordres légitimes", "il utilise trop de jetons", "il ralentit le GPU"], answer=1, why="<p>Consignes et données partagent le même contexte : c’est l’injection indirecte.</p>")],
           3:[dict(q="Quelle est la meilleure défense pour limiter les dégâts d’un agent détourné ?", choices=["un prompt système plus long", "lui donner des droits minimaux et exiger une confirmation pour les actions sensibles", "augmenter la température", "supprimer les journaux"], answer=1, why="<p>Les droits minimaux limitent ce qu’une attaque réussie peut faire.</p>")],
           4:[dict(q="Pourquoi mesurer aussi le taux de refus injustifiés ?", choices=["pour économiser des jetons", "parce qu’un système qui refuse trop est inutilisable", "parce que les refus sont gratuits", "pour réduire la température"], answer=1, why="<p>La sécurité se juge sur les deux erreurs : laisser passer, et bloquer à tort.</p>")]}
)]
