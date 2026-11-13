# Atlas de l'IA : chapitre 77, Qwen 3.6 35B-A3B, un modèle à mélange d'experts (MoE), même démarche que le chapitre 76
GROUPS = [("Voir l’IA en 3D", ["qwenmoe"])]
P = lambda q, ch, a, w: dict(q=q, choices=ch, answer=a, why=f"<p>{w}</p>")
Z = lambda x, y, d, az=8, el=7: dict(target=[x, y, 0], dist=d, az=az, el=el, auto=False)
LEG = '<p><b>Code couleur</b> (comme au chapitre 76) : blanc = <b>4 bits</b>, bleu = <b>8 bits</b>, rouge = <b>16 bits</b> ; gris = pas de poids.</p>'

CHAPTERS = [dict(dir="qwenmoe", no=77, title="Qwen 3.6 35B-A3B", sub="un mélange d’experts : 35 milliards de poids, 3 au travail",
 cnt="Routeur, 256 experts par couche, 8 actifs par token : pourquoi un MoE va si vite", alt="Une pile de 40 couches et une grille de 256 experts dont 8 s’allument",
 scenes=[
  dict(key="moe", title="Le trajet d’une requête", sub="blanc 4 bits · bleu 8 bits · rouge 16 bits", kind="qwenmoe",
       plate="Même chemin qu’au chapitre 76 : tokeniseur et embeddings, puis 40 couches, puis la tête de sortie et la tête MTP. Mais la partie « réflexion » de chaque couche n’est plus un seul MLP : c’est un bloc de 256 petits experts. Le routeur (rouge) en choisit 8 pour le token en cours, la grille de droite montre lesquels ; l’expert partagé (bleu) travaille toujours. D’une couche à l’autre, les 8 experts changent. La quantification affichée est une recette typique pour un MoE, pas celle d’un fichier précis.",
       facts=[["couches", "40 (30 GDN + 10 attention)"], ["experts", "256 par couche, 8 + 1 partagé actifs"], ["poids", "35 Md, ~3 Md par token"]], cam=dict(az=5, el=6)),
  dict(key="lu", title="Stocker n’est pas lire", sub="milliards de poids", kind="qbars", sp=2.8,
       bars=[dict(n="27B dense : stockés", v=27, pal="paper", s="27 Md"), dict(n="27B dense : lus par token", v=27, pal="blue", s="27 Md"), dict(n="35B-A3B : stockés", v=35, pal="paper", s="35 Md"), dict(n="35B-A3B : lus par token", v=3, pal="blue", s="~3 Md")],
       info="un MoE garde tout en mémoire, mais n’en lit qu’une petite partie par token",
       plate="Un modèle dense lit tous ses poids pour chaque token. Un MoE les garde tous en mémoire, mais ne lit que ceux des experts choisis : ~3 milliards sur 35. Sur un Mac, la génération est limitée par la vitesse de lecture de la mémoire : lire moins, c’est aller plus vite.",
       facts=[["dense 27B", "27 Md lus par token"], ["MoE 35B-A3B", "~3 Md lus par token"], ["mémoire", "il faut quand même tout stocker"]]),
  dict(key="go", title="La taille en mémoire", sub="selon la quantification (ordres de grandeur)", kind="qbars", sp=2.8,
       bars=[dict(n="16 bits", v=70, pal="red", s="~70 Go"), dict(n="8 bits", v=37, pal="blue", s="~37 Go"), dict(n="4 bits (+ échelles)", v=20, pal="paper", s="~20 Go")],
       info="35 milliards × bits ÷ 8, plus les échelles des groupes",
       plate="La taille se calcule simplement : nombre de poids × bits par poids ÷ 8. En 16 bits, ~70 Go ; en 8 bits, ~37 Go ; en 4 bits avec une échelle par groupe de 32 poids (~4,5 bits en moyenne), ~20 Go, à peu près comme le 27B dense en quantification dynamique.",
       facts=[["16 bits", "~70 Go"], ["4 bits", "~20 Go"], ["calcul", "poids × bits ÷ 8"]]),
 ],
 pages=[
  dict(kicker="Chapitre 77 · un modèle réel", title="Qwen 3.6 35B-A3B", sub="35 milliards de poids, 3 au travail", scene="moe", body="""
    <p class="lede">Le nom dit tout : <b>35B</b>, 35 milliards de poids au total ; <b>A3B</b>, environ 3 milliards <b>actifs</b> pour chaque token.</p>
    <p>C’est un <b>mélange d’experts</b> (<i>mixture of experts</i>, MoE, chapitre 27). Le chemin d’une requête est le même que pour le Qwen 3.8 27B dense du chapitre 76 : tokenisation, embeddings, couches, tête de sortie, échantillonnage, tête MTP. Ce qui change est à l’intérieur de chaque couche.</p>
    """ + LEG + """
    <p>L’architecture vient de la fiche du modèle (Qwen/Qwen3.6-35B-A3B sur Hugging Face) ; la répartition des bits est une recette typique, pas celle d’un fichier précis.</p>"""),
  dict(kicker="77.1", title="40 couches hybrides", sub="3 GDN, puis 1 attention, dix fois", scene="moe", cam=Z(-4.2, 4.6, 30, 6, 6), body="""
    <p class="lede">Le motif est le même que dans le 27B : <b>trois couches GDN</b> (Gated DeltaNet, le résumé compact) puis <b>une couche d’attention complète</b>, répété <b>10 fois</b>.</p>
    <ul class="rules">
      <li><b>30 couches GDN</b> : une attention linéaire, à mémoire de taille fixe.</li>
      <li><b>10 couches d’attention</b> (une sur quatre, les blocs larges) : elles seules ont un cache KV qui grandit avec le texte.</li>
    </ul>
    <p>Le modèle est moins profond (40 couches contre 64) et plus étroit (vecteurs de 2 048 nombres) : toute la capacité supplémentaire est dans les experts.</p>"""),
  dict(kicker="77.2", title="Le routeur et les experts", sub="8 experts sur 256, à chaque couche", scene="moe", cam=Z(5.2, 4.2, 30, 4, 6), body="""
    <p class="lede">Dans chaque couche, la partie « réflexion » est découpée en <b>256 experts</b> : 256 petits MLP indépendants.</p>
    <ol class="rules">
      <li>Le <b>routeur</b>, une toute petite couche, donne un score à chaque expert pour le token en cours.</li>
      <li>Les <b>8 meilleurs</b> travaillent ; leurs résultats sont additionnés, pondérés par leurs scores.</li>
      <li>Un <b>expert partagé</b> travaille pour tous les tokens : il porte ce qui est commun à tout.</li>
    </ol>
    <p>La grille montre les experts choisis à chaque couche : ils changent d’une couche à l’autre et d’un token à l’autre. Un « expert » n’est pas un spécialiste lisible (« la chimie ») : la spécialisation est apprise, souvent par types de tokens.</p>
    <p>À l’entraînement, une pénalité d’<b>équilibrage</b> évite que le routeur envoie tout aux mêmes experts.</p>"""),
  dict(kicker="77.3", title="Pourquoi un MoE va vite", sub="stocker n’est pas lire", scene="lu", body="""
    <p class="lede">Pour produire un token, un modèle relit ses poids en mémoire. Sur un Mac, c’est la vitesse de cette lecture qui limite la génération.</p>
    <table class="data">
      <tr><th>modèle</th><th>stockés</th><th>lus par token</th></tr>
      <tr><td>Qwen 3.8 27B (dense)</td><td>27 Md</td><td>27 Md</td></tr>
      <tr><td>Qwen 3.6 35B-A3B (MoE)</td><td>35 Md</td><td>~3 Md</td></tr>
    </table>
    <p>Le MoE lit environ <b>9 fois moins de poids</b> par token : la génération est bien plus rapide. Le prix : il faut quand même <b>tout garder en mémoire</b>, car le token suivant choisira d’autres experts.</p>"""),
  dict(kicker="77.4", title="Quantifier un MoE", sub="où mettre les bits", scene="moe", body="""
    <p class="lede">Le principe du chapitre 76 s’applique : compresser là où les erreurs se moyennent, épargner les goulots. Recette typique :</p>
    <table class="data">
      <tr><th>bits</th><th>parties</th></tr>
      <tr><td>4</td><td>les 256 experts de chaque couche (l’essentiel des poids), la plupart des parties mélange</td></tr>
      <tr><td>8</td><td>l’expert partagé, les embeddings, la tête de sortie, les projections de sortie</td></tr>
      <tr><td>16</td><td>les routeurs, les normalisations, la convolution et l’état des GDN, la tête MTP</td></tr>
    </table>
    <p>Le <b>routeur</b> est minuscule mais décisif : une petite erreur envoie le token vers d’autres experts, et toute la couche change. L’<b>expert partagé</b> sert à chaque token : ses erreurs ne se diluent pas. Chaque expert ordinaire, lui, ne sert qu’à une petite partie des tokens : on peut le compresser fort.</p>"""),
  dict(kicker="77.5", title="La mémoire", sub="~20 Go en 4 bits, contexte long", scene="go", body="""
    <p class="lede">35 milliards de poids × bits ÷ 8 : ~70 Go en 16 bits, ~37 Go en 8 bits, ~20 Go en 4 bits.</p>
    <p>En 4 bits, il tient donc dans la même enveloppe que le 27B dense du chapitre 76 (la limite de 28 Go du serveur). Le cache KV ne concerne que les <b>10 couches d’attention</b> ; les 30 couches GDN gardent un état de taille fixe. La fiche annonce un contexte natif de <b>262 144 tokens</b> ; en pratique, la fenêtre est réglée pour tenir en mémoire (65 536 tokens sur le Mac pour le 27B).</p>"""),
  dict(kicker="77.6", title="Dense ou MoE ?", sub="ce qu’on gagne, ce qu’on perd", scene="lu", body="""
    <table class="data">
      <tr><th></th><th>27B dense</th><th>35B-A3B MoE</th></tr>
      <tr><td>mémoire (4 bits)</td><td>~15 à 20 Go</td><td>~20 Go</td></tr>
      <tr><td>poids lus par token</td><td>27 Md</td><td>~3 Md</td></tr>
      <tr><td>vitesse de génération</td><td>correcte</td><td>bien plus rapide</td></tr>
      <tr><td>finesse par token</td><td>tous les poids travaillent</td><td>3 Md seulement travaillent</td></tr>
    </table>
    <p>À mémoire égale, le dense met <b>tous</b> ses poids au service de chaque token : il est souvent plus fin sur les tâches difficiles. Le MoE répond beaucoup plus vite, ce qui compte pour un agent qui enchaîne les appels. Les deux tournent avec le même type de serveur (mtplx, mlx-lm, llama.cpp) : seul le fichier du modèle change.</p>
    <p>Pour l’affiner (chapitre 78), le MoE pose un problème de plus : modifier les experts sans dérégler le routeur.</p>"""),
 ],
 practice={
  2: [P("Combien d’experts travaillent pour un token, dans une couche ?", ["les 256", "8, plus l’expert partagé", "un seul", "aucun, seul le routeur calcule"], 1, "Le routeur garde les 8 meilleurs scores ; l’expert partagé travaille toujours.")],
  3: [P("Pourquoi le MoE génère-t-il plus vite que le 27B dense ?", ["il a moins de poids en mémoire", "il lit ~3 Md de poids par token au lieu de 27", "il n’a pas de tête de sortie", "il ignore le contexte"], 1, "La génération est limitée par la lecture de la mémoire : lire moins, c’est aller plus vite.")],
  4: [P("Pourquoi garder le routeur en 16 bits ?", ["il est énorme", "une petite erreur change les experts choisis, donc toute la couche", "il n’est jamais utilisé", "pour le cache KV"], 1, "Il est minuscule, le garder précis ne coûte presque rien.")],
 }),
]
