# Atlas de l'IA : chapitres 35 à 37 (demande et élasticité, atrophie des compétences, fossé de l'ingénieur logiciel)
GROUPS = [("L’IA et le travail", ["elasticite", "atrophie", "fosse"])]
P = lambda q, ch, a, w: dict(q=q, choices=ch, answer=a, why=f"<p>{w}</p>")
def pipe(key, title, sub, stages, plate, facts, per=3, bw=2.3, gap=0.8, **kw):
    return dict(key=key, title=title, sub=sub, kind="pipeline", per=per, bw=bw, gap=gap, y=1.4, stages=[dict(n=a, s=b, **({"pal": c} if c else {})) for a, b, c in stages], plate=plate, facts=facts, **kw)

CHAPTERS = [
dict(dir="elasticite", no=35, title="Demande, élasticité et emploi", sub="si l’IA baisse le coût d’une tâche, que devient la demande ?", cnt="Le raisonnement économique derrière « l’IA va-t-elle prendre nos emplois ? »", alt="Des droites de demande plus ou moins élastiques",
 scenes=[
  dict(key="elast", title="Trois élasticités", sub="quand le prix baisse", kind="curve", fn="elasticite",
       plate="L’élasticité-prix ε est le rapport entre la variation relative de la quantité demandée et celle du prix. Si ε est supérieur à 1, une baisse de prix fait augmenter la dépense totale : la demande est « élastique ». Si ε est inférieur à 1, elle la fait baisser. Courbes illustratives (approximation linéaire).",
       facts=[["définition", "ε = % de variation de Q / % de variation de P"], ["ε > 1", "la dépense totale augmente"], ["ε < 1", "la dépense totale diminue"]]),
  pipe("jevons", "Le paradoxe de Jevons", "plus efficace, donc plus utilisé", [("Coût unitaire baisse", "la ressource devient efficace", "blue"), ("Usages nouveaux", "devenus rentables", "blue"), ("Demande élastique", "ε > 1", "red"), ("Consommation totale monte", "malgré l’efficacité", "red"), ("Demande inélastique", "ε < 1", None), ("Consommation totale baisse", "l’efficacité suffit", None)],
       "Jevons (1865) a observé que des machines à vapeur plus économes en charbon ont fait augmenter la consommation totale de charbon. L’effet n’est pas automatique : il dépend de l’élasticité de la demande. Appliqué à une tâche rendue moins chère par l’IA, tout dépend de la façon dont la demande de cette tâche réagit.",
       [["Jevons", "1865, charbon"], ["condition", "demande élastique"], ["à ne pas faire", "en faire une loi"]]),
  pipe("taches", "Des tâches, pas des métiers", "ce que l’IA touche vraiment", [("Un métier", "un faisceau de tâches", None), ("Tâches automatisées", "l’IA les fait seule", "red"), ("Tâches augmentées", "l’humain va plus vite", "blue"), ("Tâches nouvelles", "créées autour de l’outil", "blue"), ("Tâches intactes", "relation, décision, responsabilité", None), ("Résultat", "le métier se recompose", "red")],
       "Les économistes analysent le travail par tâches. L’IA automatise certaines, en augmente d’autres, en crée de nouvelles. Ce qui arrive à l’emploi dépend de la part de chaque catégorie dans le métier et de la façon dont la demande du produit final réagit.",
       [["approche", "analyse par tâches (Autor et d’autres)"], ["effets", "substitution, complément, création"]]),
  pipe("facteurs", "Ce qui fait pencher la balance", "cinq facteurs", [("Élasticité du produit", "plus de demande si moins cher ?", "blue"), ("Part de la tâche", "dans la valeur du produit", "blue"), ("Substitut ou complément", "l’IA remplace-t-elle ou aide ?", "red"), ("Goulots restants", "vérification, régulation, confiance", "blue"), ("Vitesse de diffusion", "adoption et réorganisation", None), ("Concurrence", "gains gardés ou rendus aux clients", None)],
       "Cinq facteurs décident si une baisse du coût d’une tâche réduit ou augmente l’emploi qui lui est lié : l’élasticité du produit, la part de la tâche dans sa valeur, le caractère substituable ou complémentaire, les goulots restants, la vitesse de diffusion.",
       [["clé", "aucun facteur seul ne suffit"], ["conséquence", "réponses différentes selon les secteurs"]]),
 ],
 pages=[
  dict(kicker="Chapitre 35 · économie", title="Demande, élasticité et emploi", sub="un cadre pour raisonner sans slogan", scene="elast", body="""
    <p class="lede">« L’IA va supprimer des emplois » et « l’IA va en créer » sont deux slogans. Un cadre d’économiste aide à raisonner sur un cas précis.</p>
    <p>Question centrale : quand une tâche devient beaucoup moins chère, la <b>demande de ce qu’elle produit</b> augmente-t-elle assez pour compenser ? Ce chapitre donne les outils, puis les résultats d’études, avec leurs limites.</p>"""),
  dict(kicker="35.1", title="L’élasticité de la demande", sub="la réaction de la quantité au prix", scene="elast", body="""
    <div class="eq">ε = (ΔQ / Q) ÷ (ΔP / P)</div>
    <p>Si ε &gt; 1, la demande est <b>élastique</b> : une baisse de prix de 10 % fait monter les quantités de plus de 10 % et la dépense totale augmente. Si ε &lt; 1, elle est <b>inélastique</b> : les quantités montent moins que le prix ne baisse.</p>
    <p>Exemples : le sel (très inélastique : on n’en consomme pas plus s’il est moins cher), les voyages ou les vidéos en ligne (beaucoup plus élastiques).</p>"""),
  dict(kicker="35.2", title="Le paradoxe de Jevons", sub="et son application à une tâche", scene="jevons", body="""
    <p class="lede">En 1865, Jevons constate que des machines à vapeur plus économes en charbon ont fait <b>augmenter</b> la consommation de charbon : des usages nouveaux sont devenus rentables.</p>
    <p>Pour une tâche rendue moins chère par l’IA (traduire, rédiger un contrat type, écrire une fonction), l’effet sur la demande de travail dépend de ε : si la demande de ce que produit la tâche est élastique, on en <b>fait davantage</b> et l’emploi peut tenir ; si elle est saturée, on en fait pareil avec moins de monde.</p>
    <p>C’est une condition à vérifier, pas une loi.</p>"""),
  dict(kicker="35.3", title="Tâches et métiers", sub="un exemple historique", scene="taches", body="""
    <p class="lede">Un métier est un faisceau de tâches. L’IA en automatise, en augmente, en crée.</p>
    <p>Exemple souvent cité : l’arrivée des <b>distributeurs de billets</b> aux États-Unis. Pendant plusieurs décennies, le nombre d’employés de banque a continué d’augmenter, car les agences, moins chères à ouvrir, se sont multipliées et le métier s’est déplacé vers le conseil ; l’emploi a ensuite reculé avec la banque en ligne.</p>
    <p>La leçon : l’effet dépend du temps, de la <b>recomposition</b> des tâches et des autres changements en cours.</p>"""),
  dict(kicker="35.4", title="Les facteurs qui décident", sub="cinq questions à poser", scene="facteurs", body="""
    <ul class="rules">
      <li><b>Le produit</b> est-il à demande élastique (logiciel, contenu) ou saturée ?</li>
      <li><b>La tâche</b> pèse-t-elle beaucoup dans le coût final ?</li>
      <li>L’IA <b>remplace</b> ou <b>complète</b> l’humain ? Un complément augmente la valeur du travail restant.</li>
      <li>Quels <b>goulots</b> subsistent (vérification, responsabilité, réglementation) ?</li>
      <li>Qui garde les gains : les <b>clients</b> (prix en baisse) ou les <b>entreprises</b> (marges) ?</li>
    </ul>"""),
  dict(kicker="35.5", title="Ce que montrent les études", sub="premiers résultats, prudence", scene="taches", body="""
    <ul class="rules">
      <li><b>Support client</b> : une étude (Brynjolfsson, Li, Raymond, 2023) mesure en moyenne environ <b>14 %</b> de productivité en plus avec un assistant, davantage pour les débutants.</li>
      <li><b>Développeurs expérimentés</b> : un essai contrôlé de METR (2025) sur leurs propres dépôts trouve des tâches environ <b>19 %</b> plus lentes avec l’IA, alors que les participants se croyaient plus rapides.</li>
      <li><b>Jeunes diplômés</b> : des analyses de données d’emploi (Brynjolfsson et collègues, 2025) relèvent un recul relatif de l’emploi des plus jeunes dans les métiers les plus exposés.</li>
    </ul>
    <p>Chaque résultat a un contexte étroit : à relire à la source avant de généraliser.</p>"""),
 ],
 practice={1:[P("Si ε = 2, que fait une baisse de prix de 10 % ?", ["la quantité demandée monte d’environ 20 %, la dépense totale augmente", "la quantité ne change pas", "la dépense totale baisse", "le prix remonte"], 0, "ε = 2 signifie +2 % de quantité par −1 % de prix : demande élastique.")],
           2:[P("Le paradoxe de Jevons se produit quand…", ["la demande est élastique : l’efficacité fait augmenter l’usage total", "la demande est nulle", "l’outil est interdit", "le prix monte"], 0, "Des usages nouveaux, devenus rentables, dépassent l’économie réalisée.")],
           3:[P("Pourquoi analyse-t-on l’effet de l’IA par tâches ?", ["un métier regroupe des tâches affectées différemment", "pour éviter de compter", "parce que les métiers n’existent pas", "pour simplifier la loi"], 0, "Automatisation, augmentation et création coexistent dans un même métier.")]}
),
dict(dir="atrophie", no=36, title="L’atrophie des compétences", sub="quand l’IA fait à notre place, que reste-t-il ?", cnt="Le risque de perdre ce qu’on ne pratique plus", alt="Une courbe de performance qui monte pendant que la compétence propre baisse",
 scenes=[
  dict(key="atro", title="Deux courbes", sub="performance assistée et compétence propre", kind="curve", fn="atrophie",
       plate="Avec l’IA, la performance apparente monte vite. Si l’on délègue sans s’exercer, la compétence propre, celle qui reste quand l’outil est absent ou se trompe, peut baisser. Un usage actif (essayer d’abord, comprendre, corriger) la maintient. Courbes illustratives, pas des mesures.",
       facts=[["performance avec l’IA", "monte"], ["compétence passive", "peut baisser"], ["usage actif", "la préserve"]]),
  pipe("meca", "Le mécanisme", "déléguer, ne plus pratiquer, ne plus savoir", [("Tâche difficile", "effort nécessaire", None), ("Délégation à l’IA", "réponse immédiate", "blue"), ("Illusion de maîtrise", "on a l’impression de savoir", "red"), ("Moins de pratique", "pas de répétition", "red"), ("Compétence en baisse", "sans l’outil, on bute", "red"), ("Dépendance", "on délègue davantage", "red")],
       "Apprendre demande un effort : essayer, se tromper, corriger. Quand l’outil fournit directement la réponse, l’effort disparaît et l’impression d’avoir compris peut rester : c’est l’illusion de maîtrise. Moins de pratique, donc moins de compétence, donc plus de délégation : une boucle.",
       [["effort", "condition de l’apprentissage"], ["illusion", "lire n’est pas savoir faire"], ["effet GPS", "comparable à l’orientation"]]),
  pipe("etudes", "Ce que disent les études", "des résultats partiels", [("Lycéens et maths", "PNAS 2025", "blue"), ("Avec assistant libre", "meilleur pendant, moins bon après", "red"), ("Avec assistant guidé", "l’écart disparaît en partie", "blue"), ("Développeurs", "se jugent plus rapides que mesuré", "red"), ("Enquête de travailleurs", "confiance en l’IA ↔ moins de pensée critique", None), ("Limites", "contextes étroits, durées courtes", "red")],
       "Une étude contrôlée sur des lycéens (Bastani et collègues, 2025) trouve de meilleurs résultats pendant l’usage d’un assistant libre, mais de moins bons à l’examen sans l’outil ; un assistant conçu pour guider limite l’écart. Une enquête de chercheurs de Microsoft et Carnegie Mellon (2025) associe une plus grande confiance dans l’IA à moins d’effort de pensée critique déclaré. Contextes étroits, durées courtes : à lire avec prudence.",
       [["étude 1", "lycéens, mathématiques"], ["étude 2", "enquête sur le travail du savoir"], ["limite", "pas de consensus définitif"]]),
  pipe("dev", "Chez les ingénieurs", "ce qui s’use en premier", [("Écrire du code", "moins de pratique", "red"), ("Relire du code", "devient la tâche principale", "blue"), ("Déboguer", "plus rare, plus difficile", "red"), ("Comprendre l’architecture", "se délègue", "red"), ("Juniors", "moins d’occasions d’apprendre", "red"), ("Parade", "pratique délibérée", "blue")],
       "Chez les ingénieurs, ce qui risque de s’user : écrire sans assistance, déboguer, comprendre le système dans son ensemble. Un junior qui n’écrit plus jamais le code risque de ne pas devenir un relecteur capable. La parade est de garder du temps de pratique non assistée.",
       [["risque", "relecteur sans expérience"], ["parade", "pratique délibérée"]]),
  pipe("parades", "Rester compétent", "usage actif plutôt que passif", [("Essayer d’abord", "puis comparer", "blue"), ("Demander pourquoi", "pas seulement quoi", "blue"), ("Expliquer à voix haute", "test de compréhension", "blue"), ("Sessions sans IA", "régulières", "red"), ("Revue approfondie", "lire pour de vrai", "red"), ("Évaluer sans outil", "former et recruter", None)],
       "Quelques pratiques : essayer avant de demander, se faire expliquer les raisons, expliquer soi-même la solution, garder des sessions sans assistance, relire vraiment ce qui est produit, évaluer et former sans l’outil.",
       [["principe", "l’outil assiste, il ne remplace pas la pratique"], ["organisation", "former les juniors sans raccourci"]]),
 ],
 pages=[
  dict(kicker="Chapitre 36 · compétences", title="L’atrophie des compétences", sub="le prix caché de la délégation", scene="atro", body="""
    <p class="lede">Une compétence qu’on ne pratique plus s’affaiblit. Avec une IA qui fait vite et bien, la tentation de ne plus pratiquer est forte.</p>
    <p>Ce chapitre distingue deux courbes : la <b>performance avec l’outil</b>, qui monte, et la <b>compétence sans l’outil</b>, qui compte quand il se trompe, est indisponible, ou qu’il faut juger son résultat.</p>"""),
  dict(kicker="36.1", title="Le mécanisme", sub="délégation et illusion de maîtrise", scene="meca", body="""
    <p class="lede">Apprendre exige un effort : chercher, se tromper, corriger. L’IA le supprime.</p>
    <ul class="rules">
      <li><b>Illusion de maîtrise</b> : lire une solution correcte donne l’impression de la savoir produire.</li>
      <li><b>Déchargement cognitif</b> : on confie à l’outil ce qu’on ne retient plus, comme avec un GPS.</li>
      <li><b>Boucle</b> : moins de pratique, moins de compétence, plus de délégation.</li>
    </ul>
    <p>Déléguer n’est pas un mal : calculatrices et correcteurs ont déjà déplacé nos compétences. La question est de savoir <b>lesquelles on veut garder</b>.</p>"""),
  dict(kicker="36.2", title="Ce que disent les études", sub="résultats partiels", scene="etudes", body="""
    <ul class="rules">
      <li><b>Lycéens</b> (Bastani et collègues, 2025) : un assistant libre améliore les exercices pendant l’usage, mais les résultats à l’examen <b>sans outil</b> sont moins bons ; un assistant guidé limite l’écart.</li>
      <li><b>Travailleurs du savoir</b> (Microsoft et Carnegie Mellon, 2025) : plus de confiance dans l’IA va avec moins d’effort de pensée critique déclaré (enquête, auto-évaluations).</li>
      <li><b>Développeurs</b> (METR, 2025) : ils se croyaient plus rapides qu’ils ne l’étaient.</li>
    </ul>
    <p>Aucune de ces études ne prouve une perte durable de compétence à long terme ; elles montrent des risques à surveiller.</p>"""),
  dict(kicker="36.3", title="Chez les ingénieurs", sub="écrire, relire, déboguer", scene="dev", body="""
    <ul class="rules">
      <li><b>Écrire</b> : moins de pratique du clavier, des algorithmes, des API.</li>
      <li><b>Relire</b> : devient l’essentiel, mais relire exige d’avoir déjà écrit et débogué.</li>
      <li><b>Déboguer</b> : quand l’IA échoue, c’est à l’humain de trouver pourquoi, souvent dans du code qu’il n’a pas écrit.</li>
      <li><b>Juniors</b> : les tâches simples, où l’on apprenait, sont celles que l’IA fait le mieux.</li>
    </ul>"""),
  dict(kicker="36.4", title="Garder la main", sub="usage actif et pratique délibérée", scene="parades", body="""
    <ul class="rules">
      <li><b>Essayer d’abord</b>, puis comparer avec la réponse de l’IA.</li>
      <li>Demander les <b>raisons</b>, expliquer la solution soi-même.</li>
      <li>Garder des <b>sessions sans assistance</b> (un kata, un petit projet).</li>
      <li>Relire <b>vraiment</b> : tester, chercher la faille, refuser ce qu’on ne comprend pas.</li>
    </ul>
    <p>L’objectif n’est pas de refuser l’outil, mais d’éviter que sa facilité n’épuise la compétence qui permet de le superviser.</p>"""),
  dict(kicker="36.5", title="Pour les organisations", sub="former, recruter, évaluer", scene="parades", body="""
    <ul class="rules">
      <li><b>Former les juniors</b> avec du travail réel et de la relecture exigeante, pas seulement des tâches déléguées.</li>
      <li><b>Évaluer sans l’outil</b> une partie des compétences clés, puis avec l’outil.</li>
      <li><b>Conserver des experts</b> capables de reprendre la main en cas de panne ou d’erreur.</li>
      <li><b>Mesurer</b> : qualité réelle, erreurs détectées, temps de compréhension, pas seulement la vitesse.</li>
    </ul>"""),
 ],
 practice={1:[P("Qu’est-ce que l’illusion de maîtrise ?", ["croire savoir faire parce qu’on a lu une solution correcte", "maîtriser trop d’outils", "ne pas avoir d’illusion", "avoir un modèle trop gros"], 0, "Lire n’est pas savoir produire : sans effort, l’apprentissage manque.")],
           2:[P("Que montre l’étude sur les lycéens (2025) ?", ["de meilleurs résultats avec l’outil, moins bons sans lui après un usage libre", "aucun effet", "que l’IA est interdite", "que les maths sont faciles"], 0, "Un assistant libre aide pendant, mais peut nuire à ce qui reste sans lui ; un assistant guidé limite l’écart.")],
           4:[P("Quelle pratique protège le mieux une compétence ?", ["essayer d’abord, puis comparer avec l’IA", "tout déléguer", "ne jamais utiliser l’outil", "lire en diagonale"], 0, "L’usage actif préserve l’effort qui construit la compétence.")]}
),
dict(dir="fosse", no=37, title="Le fossé de l’ingénieur logiciel", sub="ce que l’IA banalise et ce qui reste rare", cnt="Où se déplace la valeur quand écrire du code devient bon marché", alt="Une chaîne de valeur de l’intention à l’exploitation",
 scenes=[
  pipe("banal", "Ce qui se banalise", "ce que l’IA fait déjà bien", [("Code standard", "CRUD, formulaires, glue", "red"), ("Tests simples", "cas évidents", "red"), ("Traduction de code", "d’un langage à un autre", "red"), ("Documentation", "premier jet", "red"), ("Exemples connus", "problèmes bien documentés", "red"), ("Conséquence", "le coût d’écrire baisse", "blue")],
       "Plus une tâche ressemble à ce qui existe en grande quantité dans les données d’entraînement, mieux l’IA la fait. Écrire du code standard, des tests simples, traduire ou documenter devient bon marché : ce n’est plus un avantage durable.",
       [["indice", "abondance dans les données"], ["effet", "le code devient bon marché"]]),
  pipe("rare", "Ce qui reste rare", "où la valeur se déplace", [("Comprendre le besoin", "le vrai problème", "blue"), ("Spécifier", "intention précise, cas limites", "blue"), ("Arbitrer", "architecture, coûts, risques", "blue"), ("Vérifier", "tests, revue, sécurité", "red"), ("Exploiter", "fiabilité, pannes, données réelles", "red"), ("Répondre de", "responsabilité, confiance", "red")],
       "Ce qui reste difficile à automatiser : comprendre le besoin réel, le spécifier sans ambiguïté, arbitrer entre des contraintes contradictoires, vérifier, faire tourner un système réel et en répondre. La valeur se déplace de « écrire » vers « décider, vérifier, assumer ».",
       [["déplacement", "écrire → décider et vérifier"], ["clé", "responsabilité"]]),
  pipe("chaine", "La nouvelle chaîne", "de l’intention à l’exploitation", [("Intention", "ce qu’on veut vraiment", "blue"), ("Spécification", "contraintes, critères", "blue"), ("Agent", "génère et teste", "red"), ("Vérification", "revue, tests, sécurité", "blue"), ("Mise en production", "déploiement, observabilité", None), ("Retour", "incidents, usage réel", "red")],
       "L’ingénieur passe progressivement de l’écriture directe à une chaîne : formuler l’intention, spécifier, faire générer par des agents (chapitres 9 à 11), vérifier, déployer, observer. Chaque étape demande du jugement, et le goulot se déplace vers la vérification.",
       [["agents", "chapitres 9 à 11"], ["vérification", "chapitre 31"], ["sécurité", "chapitre 22"]], loop="itérer"),
  pipe("goulot", "Le goulot de la vérification", "générer vite, vérifier lentement", [("Génération", "quasi instantanée", "blue"), ("Volume de code", "explose", "red"), ("Relecture", "limitée par l’attention humaine", "red"), ("Dette cachée", "code non compris", "red"), ("Parades", "tests, types, revues ciblées", "blue"), ("Compétence rare", "juger vite et juste", "red")],
       "Quand le code coûte peu à produire, le volume augmente, mais la capacité humaine de relecture ne suit pas. Le risque est une dette cachée : du code que personne ne comprend. Les parades sont les tests, les types, la revue ciblée et la maîtrise du domaine.",
       [["goulot", "la relecture"], ["risque", "code non compris"], ["parade", "automatiser la vérification"]]),
  dict(key="emploi", title="Emploi et élasticité", sub="un modèle volontairement simple", kind="curve", fn="emploi",
       plate="Modèle jouet : si la productivité est multipliée par m, le prix du logiciel baisse d’autant, la quantité demandée est multipliée par m^ε, et l’emploi nécessaire par m^(ε−1). Avec ε = 1 l’emploi est stable, au-dessus il augmente, au-dessous il baisse. Courbes illustratives, hypothèses fortes (voir la page).",
       facts=[["formule", "emploi ∝ m^(ε−1)"], ["ε < 1", "moins d’ingénieurs"], ["ε > 1", "plus d’ingénieurs"]]),
  dict(key="amdahl", title="La loi d’Amdahl du développement", sub="seule une partie du travail accélère", kind="curve", fn="amdahl",
       plate="Si l’IA accélère fortement l’écriture du code mais pas la compréhension du besoin, la spécification, la revue ou la mise en production, le gain global est borné par la part non accélérée : avec 60 % de travail automatisable, même une accélération infinie ne dépasse pas 2,5 fois. Courbes illustratives.",
       facts=[["loi d’Amdahl", "gain = 1 / ((1−f) + f/m)"], ["plafond", "1 / (1−f)"]]),
  pipe("confond", "Pourquoi les chiffres actuels sont ambigus", "plusieurs causes en même temps", [("Fin de l’argent bon marché", "hausse des taux, 2022–2024", "red"), ("Sur-embauche post-2020", "correction", "red"), ("Réorientation des budgets", "vers l’IA elle-même", "blue"), ("Effet réel de l’IA", "tâches automatisées", "blue"), ("Cycle du secteur", "se répète", None), ("Conclusion", "difficile d’isoler l’IA", "red")],
       "Le recul de certaines embauches de développeurs depuis 2022 coïncide avec la hausse des taux d’intérêt, la correction de la sur-embauche de 2020–2021 et le déplacement des budgets vers l’IA. Isoler l’effet propre des assistants de code est difficile, et les études sérieuses divergent.",
       [["difficulté", "causes multiples et simultanées"], ["prudence", "ne pas attribuer tout à l’IA"]]),
  pipe("fossesdurables", "Des fossés durables", "ce qui protège un ingénieur", [("Connaissance du domaine", "métier, réglementation", "blue"), ("Confiance", "relation, réputation", "blue"), ("Systèmes réels", "contraintes, héritage, données", "blue"), ("Sécurité et fiabilité", "enjeu critique", "red"), ("Coordination", "équipes, parties prenantes", "blue"), ("Apprendre vite", "outils et domaines nouveaux", "red")],
       "Les atouts durables ne sont pas des langages mais des combinaisons : connaissance profonde d’un domaine, confiance de clients et d’équipes, maîtrise de systèmes réels et critiques, capacité de coordination et d’apprentissage rapide.",
       [["profil", "en T : large et profond"], ["valeur", "domaine + jugement + confiance"]]),
 ],
 pages=[
  dict(kicker="Chapitre 37 · carrière", title="Le fossé de l’ingénieur logiciel", sub="où va la valeur quand le code devient bon marché", scene="banal", body="""
    <p class="lede">Un <b>fossé</b> (<i>moat</i>) est ce qui protège une position : une rareté que les autres ne peuvent pas copier facilement.</p>
    <p>Pendant des décennies, savoir écrire du code correct était rare. Si l’IA en baisse le coût, où se déplace la rareté ? Ce chapitre propose une analyse, <b>sans prétendre prédire</b> : l’incertitude est grande.</p>"""),
  dict(kicker="37.1", title="Ce qui se banalise", sub="ce que l’IA fait déjà bien", scene="banal", body="""
    <ul class="rules">
      <li><b>Code standard</b> : formulaires, accès aux données, assemblage de bibliothèques.</li>
      <li><b>Tâches bien documentées</b> : algorithmes classiques, exemples fréquents.</li>
      <li><b>Traduction</b> de code d’un langage à l’autre, <b>premiers jets</b> de tests et de documentation.</li>
    </ul>
    <p>La règle empirique : plus un problème ressemble à ce qui est <b>abondant</b> en ligne, mieux l’IA le traite, et moins il protège celui qui le résout.</p>"""),
  dict(kicker="37.2", title="Ce qui reste rare", sub="décider, vérifier, assumer", scene="rare", body="""
    <ul class="rules">
      <li><b>Comprendre le besoin</b> : ce que l’utilisateur veut vraiment, rarement ce qu’il dit.</li>
      <li><b>Spécifier</b> et prévoir les cas limites.</li>
      <li><b>Arbitrer</b> : coût, délai, risque, maintenabilité.</li>
      <li><b>Vérifier</b> et sécuriser ce qui est produit.</li>
      <li><b>Exploiter</b> et <b>répondre</b> du système devant des utilisateurs réels.</li>
    </ul>"""),
  dict(kicker="37.3", title="La nouvelle chaîne de travail", sub="de l’intention à l’exploitation", scene="chaine", body="""
    <p class="lede">Le travail glisse de « écrire le code » vers « conduire une chaîne » : intention, spécification, génération par des agents, vérification, déploiement, observation.</p>
    <p>Les chapitres 9 à 11 expliquent les harnais, agents et boucles qui exécutent la génération ; c’est <b>l’humain qui fixe l’objectif, les critères et les limites</b>. Les compétences qui comptent : spécifier clairement, structurer un problème, choisir les bons garde-fous (chapitre 22).</p>"""),
  dict(kicker="37.4", title="Le goulot de la vérification", sub="le code bon marché a un coût caché", scene="goulot", body="""
    <p class="lede">Générer du code est presque gratuit, <b>le comprendre et le vérifier ne l’est pas</b>.</p>
    <ul class="rules">
      <li>Le volume de code augmente plus vite que la capacité humaine de relecture.</li>
      <li>Une dette cachée s’accumule : du code qui marche mais que personne ne comprend.</li>
      <li>Parades : <b>tests automatisés</b>, typage, revues ciblées sur les zones à risque, évaluations (chapitre 31).</li>
    </ul>
    <p>Savoir juger vite et juste devient donc une compétence centrale, liée au chapitre 36 : on ne juge bien que ce qu’on sait faire.</p>"""),
  dict(kicker="37.5", title="Des fossés durables", sub="ce qui protège", scene="fossesdurables", body="""
    <ul class="rules">
      <li><b>Le domaine</b> : finance, santé, industrie, droit… connaître le métier de ses utilisateurs.</li>
      <li><b>La confiance</b> : relations, réputation, capacité à s’engager.</li>
      <li><b>Les systèmes réels</b> : héritage, contraintes, données sales, exigences de sécurité.</li>
      <li><b>L’apprentissage rapide</b> : changer d’outil, de langage, de domaine.</li>
    </ul>
    <p>Un langage ou un framework n’est pas un fossé. Une <b>combinaison</b> de domaine, de jugement et de confiance en est un.</p>"""),
  dict(kicker="37.6", title="Pourquoi l’issue est incertaine", sub="un modèle simple et ses limites", scene="emploi", body="""
    <p class="lede">Ma remarque « tout dépend de l’élasticité de la demande de logiciel » est un <b>résumé</b>, pas une explication. Voici ce qu’elle veut dire.</p>
    <div class="eq">emploi ∝ m<sup>ε−1</sup></div>
    <p>Si l’IA multiplie la productivité par <i>m</i>, le logiciel coûte moins cher, on en demande plus (<i>m</i><sup>ε</sup>) mais il faut moins de travail par unité (1/<i>m</i>). Si ε &gt; 1, on en demande tellement plus que l’emploi augmente ; si ε &lt; 1, il baisse. Mais ε <b>n’est connu pour aucun segment</b> du logiciel, et il n’est pas constant.</p>"""),
  dict(kicker="37.7", title="Les hypothèses cachées", sub="ce que le modèle simple suppose", scene="amdahl", body="""
    <ul class="rules">
      <li><b>Report complet sur les prix</b> : on suppose que les gains font baisser les prix. Si les entreprises gardent les marges, la demande ne bouge pas.</li>
      <li><b>Une productivité uniforme</b> : en réalité seule une part <i>f</i> du travail accélère (loi d’Amdahl, figure) ; comprendre, spécifier, vérifier et exploiter ne vont pas plus vite.</li>
      <li><b>Un ε constant</b> : la demande peut être très élastique pour le logiciel sur mesure des petites structures, qui n’existait pas faute de moyens, et saturée pour les produits de masse.</li>
      <li><b>Des ingénieurs homogènes</b> : l’emploi total peut tenir pendant que la composition change, avec moins de postes juniors d’exécution et plus de postes de vérification et de domaine.</li>
      <li><b>Un équilibre de long terme</b> : la transition peut être longue et douloureuse même si le point d’arrivée est favorable.</li>
    </ul>"""),
  dict(kicker="37.8", title="Ce que disent les chiffres actuels", sub="un signal difficile à lire", scene="confond", body="""
    <p class="lede">Des embauches de développeurs ont reculé depuis 2022. Est-ce l’IA ?</p>
    <p>Pas forcément : la <b>hausse des taux</b> a réduit le financement des entreprises technologiques, la <b>sur-embauche de 2020–2021</b> a été corrigée, et une partie des budgets est passée vers l’IA elle-même. Les études qui isolent l’effet des assistants de code (recul relatif des plus jeunes dans les métiers exposés, par exemple) existent mais ne font pas consensus et portent sur des périodes courtes.</p>
    <p>Conclusion honnête : <b>on ne sait pas encore</b>, et il faut se méfier de ceux qui l’affirment dans un sens ou dans l’autre.</p>"""),
  dict(kicker="37.9", title="Les indicateurs à suivre", sub="ce qui réduirait l’incertitude", scene="emploi", body="""
    <ul class="rules">
      <li><b>Le prix et le volume</b> de logiciel livré : le nombre d’applications créées, l’usage de logiciel sur mesure par les petites entreprises (signe d’une demande élastique).</li>
      <li><b>Les offres d’emploi par ancienneté</b> et par domaine : où baissent-elles, où montent-elles ?</li>
      <li><b>Le coût de vérification</b> : temps de revue, défauts échappés, incidents.</li>
      <li><b>Les salaires par compétence</b> : le domaine et la sécurité montent-ils pendant que le code standard baisse ?</li>
    </ul>
    <p>Ce qui <b>changerait mon analyse</b> : des signes durables que les gains de productivité se transforment en plus de logiciel livré (élasticité haute), ou au contraire en moins de projets avec les mêmes équipes réduites (élasticité basse).</p>"""),
  dict(kicker="37.10", title="Se préparer sans prédire", sub="trois scénarios et des gestes utiles", scene="rare", body="""
    <ul class="rules">
      <li><b>Scénario 1</b> : demande de logiciel très élastique (ε &gt; 1, chapitre 35) ; on en produit beaucoup plus et les ingénieurs se déplacent vers la vérification et le domaine.</li>
      <li><b>Scénario 2</b> : demande saturée sur certains segments ; moins de postes d’exécution, plus de postes de supervision.</li>
      <li><b>Scénario 3</b> : progrès continus des agents ; la frontière entre exécution et jugement recule.</li>
    </ul>
    <p><b>Gestes utiles quel que soit le scénario</b> : maîtriser un domaine, pratiquer sans l’IA (chapitre 36), apprendre à spécifier et à vérifier, construire de la confiance, suivre ses résultats avec des mesures réelles.</p>"""),
 ],
 practice={1:[P("Quelle tâche logicielle est la plus exposée à la banalisation ?", ["le code standard bien documenté en ligne", "la négociation avec un client", "l’arbitrage d’architecture sous contraintes", "la responsabilité d’un incident"], 0, "Plus la tâche est abondante dans les données, mieux l’IA la fait.")],
           4:[P("Pourquoi la vérification devient-elle un goulot ?", ["le code se génère plus vite que l’humain ne peut le relire", "les tests sont interdits", "les ordinateurs sont lents", "le code est trop court"], 0, "Le volume augmente ; l’attention humaine reste limitée.")],
           6:[P("Si ε = 0,5 et que la productivité est multipliée par 4, que prédit le modèle simple pour l’emploi ?", ["il baisse de moitié (4^(−0,5) = 0,5)", "il double", "il ne change pas", "il est multiplié par 4"], 0, "Emploi ∝ m^(ε−1) = 4^(−0,5) = 0,5 : la demande ne suit pas assez la baisse de prix. Hypothèses fortes, à lire avec la page.")],
           7:[P("Pourquoi la loi d’Amdahl limite-t-elle le gain global ?", ["la part du travail non accélérée reste inchangée", "l’IA est trop lente", "les ingénieurs refusent l’outil", "le code est trop court"], 0, "Avec 60 % de travail automatisable, le gain maximal est 1/(1−0,6) = 2,5.")],
           5:[P("Qu’est-ce qui constitue un fossé durable pour un ingénieur ?", ["une combinaison de domaine, de jugement et de confiance", "la maîtrise d’un seul framework", "la vitesse de frappe", "le nombre de lignes écrites"], 0, "Les outils changent ; domaine, jugement et confiance sont plus difficiles à copier.")]}
),
]
