# Atlas de l'IA : chapitres 1 à 3 (texte, attention, inférence)
eq = lambda s: f'<div class="eq">{s}</div>'
GROUPS = [("Les modèles de langage", ["texte", "attention", "inference"])]
CHAPTERS = [
dict(dir="texte", no=1, title="Du texte aux nombres", sub="jetons, vocabulaire, plongements", cnt="Ce que le modèle lit vraiment", alt="Une phrase découpée en jetons numérotés",
 scenes=[
  dict(key="tok", title="Le texte en jetons", sub="une phrase découpée en morceaux", kind="tokens", y=2.2, info="exemple illustratif : les identifiants varient selon le modèle",
       items=[dict(t="L", id=43), dict(t="’", id=6), dict(t="intelligence", id=9120), dict(t=" artificielle", id=18011), dict(t=" apprend", id=5521), dict(t=" à", id=311), dict(t=" prédire", id=21874), dict(t=" la", id=264), dict(t=" suite", id=7312), dict(t=".", id=13)],
       plate="Un modèle ne lit pas des lettres mais des jetons : des morceaux de mots, d’espaces et de ponctuation. Chaque jeton a un numéro dans un vocabulaire fixé avant l’entraînement.",
       facts=[["jetons", "10"], ["vocabulaire typique", "32 000 à 260 000"], ["caractères", "46"]], cam=dict(dx=0, y=2.2, dist=26, az=4, el=6, radius=7)),
  dict(key="bpe", title="Fusionner les paires fréquentes", sub="le principe du BPE", kind="pipeline", per=3, bw=2.4, gap=0.9, y=1.6,
       stages=[dict(n="l·o·w·e·r", s="départ : lettres"), dict(n="lo·w·e·r", s="« l o » fréquent"), dict(n="low·e·r", s="« lo w » fréquent"), dict(n="low·er", s="« e r » fréquent"), dict(n="lower", s="un seul jeton", pal="red")],
       plate="L’encodage par paires d’octets (BPE) part des caractères et fusionne à chaque étape la paire qui revient le plus souvent dans le corpus d’entraînement du tokenizer. Après quelques dizaines de milliers de fusions, les mots courants sont un seul jeton, les rares sont découpés.",
       facts=[["fusions", "≈ taille du vocabulaire"], ["mot rare", "plusieurs jetons"], ["mot courant", "un seul jeton"]], cam=dict(dx=0, y=2.0, dist=25, az=4, el=6, radius=7)),
  dict(key="emb", title="L’espace des sens", sub="un point par jeton, des directions pour les relations", kind="scatter", by=2.6,
       points=[dict(n="homme", x=-3.6, y=-0.8, c="blue"), dict(n="femme", x=-3.6, y=0.8, c="blue"), dict(n="roi", x=-1.2, y=-0.5), dict(n="reine", x=-1.2, y=1.1), dict(n="France", x=1.4, y=-1.4, c="red"), dict(n="Paris", x=1.4, y=0.2, c="red"), dict(n="Italie", x=3.6, y=-1.4, c="red"), dict(n="Rome", x=3.6, y=0.2, c="red")],
       arrows=[["homme", "femme", ""], ["roi", "reine", "même direction"], ["France", "Paris", ""], ["Italie", "Rome", "capitale de"]], walk=["roi", "reine", "France", "Paris"],
       info="projection en 2 dimensions (le vrai espace en a des milliers)",
       plate="Chaque jeton est transformé en un vecteur de plusieurs milliers de nombres, le plongement. Des jetons de sens proches ont des vecteurs proches, et certaines relations (féminin, capitale) correspondent à des directions presque parallèles. Ici, projetées en 2 dimensions.",
       facts=[["dimension réelle", "512 à 16 000"], ["distance", "cosinus des angles"], ["appris par", "l’entraînement"]], cam=dict(dx=0, y=2.4, dist=24, az=2, el=4, radius=6)),
  dict(key="flow", title="De la phrase au mot suivant", sub="le trajet complet", kind="pipeline", per=3, bw=2.2, gap=0.8, y=1.6,
       stages=[dict(n="Texte"), dict(n="Jetons", s="découpage"), dict(n="Identifiants", s="vocabulaire"), dict(n="Plongements", s="vecteurs"), dict(n="Transformeur", s="N couches", pal="blue"), dict(n="Scores", s="un par mot", pal="red")],
       plate="Tout modèle de langage suit le même trajet : texte, jetons, identifiants, vecteurs, calcul par les couches, puis un score par mot du vocabulaire. Le mot choisi est ajouté au texte et le trajet recommence.",
       facts=[["entrée", "texte"], ["sortie", "scores sur le vocabulaire"]], cam=dict(dx=0, y=2.0, dist=25, az=4, el=6, radius=7)),
 ],
 pages=[
  dict(kicker="Chapitre 1 · tous niveaux", title="Du texte aux nombres", sub="ce que le modèle lit vraiment", scene="tok", body="""
    <p class="lede">Un modèle de langage ne voit ni lettres ni mots : il voit des <b>nombres</b>. Avant toute chose, il faut transformer le texte en suite d’entiers.</p>
    <p>La phrase de la figure est découpée en <b>jetons</b> (<i>tokens</i>) : des morceaux de mot, des espaces, des signes. Chaque jeton est un numéro dans un <b>vocabulaire</b> fixé une fois pour toutes, avant l’entraînement. Les identifiants de la figure sont inventés pour l’exemple.</p>
    <p>Tout ce qui suit dans cet atlas, de l’attention à l’inférence, travaille sur ces suites de nombres.</p>"""),
  dict(kicker="1.1", title="Apprendre à découper", sub="l’encodage par paires d’octets", scene="bpe", body="""
    <p class="lede">Découper par mots échoue sur les mots rares ; découper par lettres allonge tout. Le <b>BPE</b> (<i>byte pair encoding</i>) prend un compromis appris sur un gros corpus.</p>
    <p>On part des caractères (ou des octets), puis on <b>fusionne à répétition la paire la plus fréquente</b>. Chaque fusion crée un jeton. On s’arrête quand le vocabulaire atteint la taille voulue : de 32 000 à plus de 250 000 jetons selon les modèles.</p>
    <p>Résultat : les mots courants sont un jeton, les mots rares se découpent en morceaux, et <b>tout texte reste codable</b>, car les octets de départ sont toujours là.</p>"""),
  dict(kicker="1.2", title="Ce que le découpage change", sub="coût, langues, chiffres", scene="tok", body="""
    <p class="lede">Le découpage n’est pas neutre : il décide de ce que le modèle perçoit facilement.</p>
    <ul class="rules">
      <li><b>Coût et mémoire</b> : on paie, on limite le contexte et on mesure la vitesse en <b>jetons</b>, pas en mots. En anglais, un mot vaut environ 1,3 jeton ; dans d’autres langues, souvent davantage.</li>
      <li><b>Chiffres</b> : un nombre est souvent coupé en morceaux, ce qui explique en partie les erreurs d’arithmétique.</li>
      <li><b>Espaces et casse</b> : « artificielle » et « Artificielle » sont des jetons différents.</li>
      <li><b>Mots inventés</b> : « drôlissime » devient plusieurs jetons, que le modèle devine en les recombinant.</li>
    </ul>"""),
  dict(kicker="1.3", title="Des identifiants aux vecteurs", sub="la matrice de plongement", scene="emb", body="""
    <p class="lede">Un numéro ne dit rien du sens. Chaque identifiant sert donc d’<b>indice de ligne</b> dans une grande table : la <b>matrice de plongement</b>.</p>
    <p>Cette matrice a une ligne par jeton et une colonne par dimension du modèle. Avec 128 000 jetons et 4 096 dimensions, elle contient environ 0,5 milliard de nombres. Ils ne sont pas écrits à la main : ils sont <b>appris</b> avec le reste du modèle.</p>
    <p>On compare deux vecteurs par l’angle qu’ils forment (<b>similarité cosinus</b>). Des jetons proches par le sens deviennent proches dans l’espace, et des relations régulières y prennent la forme de directions : de « roi » à « reine », comme de « homme » à « femme ».</p>"""),
  dict(kicker="1.4", title="Le trajet complet", sub="du texte au score", scene="flow", body="""
    <p class="lede">Après les plongements, les vecteurs traversent les couches du transformeur (chapitre suivant), qui produisent à la fin <b>un score par jeton du vocabulaire</b>.</p>
    <p>Ces scores s’appellent <b>logits</b>. Les réglages d’échantillonnage (chapitre 4) en tirent le mot suivant, qui est ajouté au texte. Le modèle repart alors du début avec un jeton de plus : c’est ainsi qu’il écrit, mot après mot.</p>
    <p>Retenez la forme générale : <b>texte → jetons → vecteurs → calcul → scores → un jeton</b>, répétée autant de fois qu’il y a de jetons à produire.</p>"""),
 ],
 practice={0:[dict(q="Un modèle de langage reçoit en entrée…", choices=["des mots tels quels", "des suites de numéros de jetons", "des images de texte", "des phrases entières"], answer=1, why="<p>Le texte est converti en identifiants de jetons avant d’entrer dans le modèle.</p>")],
           1:[dict(q="Que fait l’algorithme BPE à chaque étape ?", choices=["il supprime les mots rares", "il fusionne la paire de symboles la plus fréquente", "il traduit le texte", "il trie le vocabulaire par ordre alphabétique"], answer=1, why="<p>Il crée un nouveau jeton à partir de la paire la plus fréquente dans le corpus, et recommence jusqu’à la taille de vocabulaire voulue.</p>")],
           3:[dict(q="La matrice de plongement a 100 000 lignes et 4 096 colonnes. Combien de nombres contient-elle ?", choices=["≈ 4 millions", "≈ 41 millions", "≈ 410 millions", "≈ 4 milliards"], answer=2, why="<p>100 000 × 4 096 ≈ 4,1 × 10⁸, soit environ 410 millions.</p>")]}
),
dict(dir="attention", no=2, title="Attention et transformeur", sub="requêtes, clés, valeurs, couches", cnt="Le calcul au cœur de tous les modèles de langage", alt="Une matrice d’attention entre des mots d’une phrase",
 scenes=[
  dict(key="att", title="La matrice d’attention", sub="qui regarde qui", kind="attn", causal=True, tokens=["Le", "chat", "dort", "car", "il", "est", "fatigué"],
       scores=[[1, 0, 0, 0, 0, 0, 0], [1.2, 1.5, 0, 0, 0, 0, 0], [0.4, 2.2, 1.2, 0, 0, 0, 0], [0.2, 1.0, 1.3, 1.0, 0, 0, 0], [0.1, 2.9, 0.8, 0.3, 0.9, 0, 0], [0.2, 1.7, 0.4, 0.2, 1.8, 0.7, 0], [0.1, 1.6, 0.9, 0.2, 1.5, 0.8, 0.9]],
       plate="Chaque ligne est un jeton qui interroge tous les jetons précédents : la hauteur de la barre est le poids qu’il leur accorde. Ici, « il » regarde surtout « chat ». Les cases sombres sont masquées : un jeton ne peut pas lire le futur.",
       facts=[["somme d’une ligne", "100 %"], ["masque causal", "ne regarde que le passé"], ["valeurs ici", "illustratives"]], cam=dict(dx=0, y=2.3, dist=21, az=2, el=3, radius=5)),
  dict(key="qkv", title="Requête, clé, valeur", sub="les trois projections", kind="pipeline", per=4, bw=1.9, gap=0.65, y=1.6,
       stages=[dict(n="Jeton", s="vecteur x"), dict(n="Q = x·Wq", s="que cherché-je ?", pal="blue"), dict(n="K = x·Wk", s="qu’ai-je à offrir ?", pal="blue"), dict(n="V = x·Wv", s="mon contenu", pal="red"), dict(n="Q·Kᵀ/√d", s="scores"), dict(n="softmax", s="poids (somme 1)"), dict(n="Σ poids·V", s="mélange des valeurs", pal="red")],
       plate="À partir du vecteur de chaque jeton, trois matrices apprises fabriquent une requête Q, une clé K et une valeur V. Q·K donne un score de pertinence, le softmax le transforme en poids, et ces poids mélangent les valeurs V.",
       facts=[["matrices apprises", "Wq, Wk, Wv"], ["division par √d", "garde les scores raisonnables"]], cam=dict(dx=0, y=2.4, dist=28, az=4, el=7, radius=8)),
  dict(key="bloc", title="Un bloc de transformeur", sub="attention, puis réseau dense, avec des raccourcis", kind="pipeline", per=5, bw=1.7, gap=0.6, y=1.4, loop="× N couches",
       stages=[dict(n="Entrée", s="x"), dict(n="Attention", s="entre jetons", pal="blue"), dict(n="+ Norme", s="raccourci"), dict(n="MLP", s="par jeton", pal="red"), dict(n="+ Norme", s="raccourci")],
       plate="Un bloc enchaîne une attention (les jetons s’échangent de l’information) et un petit réseau dense (chaque jeton est transformé seul), chacun suivi d’un raccourci résiduel et d’une normalisation. Le modèle empile des dizaines de ces blocs.",
       facts=[["attention", "mélange entre jetons"], ["MLP", "calcul sur chaque jeton"], ["raccourcis", "facilitent l’entraînement"]], cam=dict(dx=0, y=1.9, dist=24, az=4, el=6, radius=6)),
  dict(key="pile", title="L’empilement", sub="de l’entrée aux scores", kind="pipeline", per=3, bw=2.1, gap=0.8, y=1.6,
       stages=[dict(n="Plongements"), dict(n="Bloc 1", s="", pal="blue"), dict(n="Bloc 2", pal="blue"), dict(n="…", pal="blue"), dict(n="Bloc N", pal="blue"), dict(n="Logits", s="un score par mot", pal="red")],
       plate="Les blocs sont empilés : la sortie de l’un est l’entrée du suivant. Un modèle de 7 milliards de paramètres a typiquement une trentaine de blocs de 4 096 dimensions ; les plus gros en ont plus de cent.",
       facts=[["7 Md de paramètres", "≈ 32 blocs × 4 096 dim."], ["règle approchée", "≈ 12 d² paramètres par bloc"]], cam=dict(dx=0, y=2.0, dist=24, az=4, el=6, radius=6)),
 ],
 pages=[
  dict(kicker="Chapitre 2 · tous niveaux", title="Attention et transformeur", sub="le calcul au cœur du modèle", scene="att", body="""
    <p class="lede">Dans « Le chat dort car il est fatigué », qui est « il » ? Pour répondre, le modèle doit relier un jeton à un autre, parfois loin. Le <b>mécanisme d’attention</b> fait exactement cela.</p>
    <p>Chaque jeton calcule un <b>poids</b> pour chacun des jetons qu’il peut lire. Plus le poids est grand, plus l’information de ce jeton influence le sien. La figure montre ces poids : une ligne par jeton qui interroge, une colonne par jeton interrogé.</p>
    <p>Le <b>transformeur</b> (2017) est l’architecture bâtie autour de cette idée. Il a remplacé les réseaux récurrents parce qu’il traite tous les jetons en parallèle, ce qui s’entraîne bien mieux sur des GPU.</p>"""),
  dict(kicker="2.1", title="Requête, clé, valeur", sub="trois rôles, trois matrices", scene="qkv", body="""
    <p class="lede">Chaque jeton joue trois rôles à la fois, avec trois projections apprises de son vecteur <i>x</i>.</p>
    <ul class="rules">
      <li>la <b>requête</b> <i>Q</i> : ce que ce jeton cherche ;</li>
      <li>la <b>clé</b> <i>K</i> : ce que ce jeton offre à ceux qui cherchent ;</li>
      <li>la <b>valeur</b> <i>V</i> : l’information qu’il transmet s’il est choisi.</li>
    </ul>
    <div class="eq">Attention(<i>Q</i>, <i>K</i>, <i>V</i>) = softmax( <i>Q</i><i>K</i><sup>T</sup> / √<i>d</i> ) <i>V</i></div>
    <p>Le produit <i>Q</i>·<i>K</i> mesure la pertinence ; le softmax en fait des poids de somme 1 ; la sortie est la moyenne pondérée des valeurs.</p>"""),
  dict(kicker="2.2", title="Ne pas lire le futur", sub="le masque causal", scene="att", body="""
    <p class="lede">Un modèle de langage est entraîné à prédire le jeton suivant. Il ne doit donc pas pouvoir lire les jetons qui viennent après.</p>
    <p>Le <b>masque causal</b> met à −∞ les scores des jetons futurs avant le softmax : leurs poids deviennent nuls (les cases sombres de la figure). Chaque ligne ne distribue donc sa probabilité que sur le passé et sur elle-même.</p>
    <p>Grâce à ce masque, une seule passe sur un texte de <i>n</i> jetons apprend <i>n</i> prédictions à la fois : c’est ce qui rend l’entraînement efficace. À l’inférence, le même masque justifie le <b>cache KV</b> (chapitre 3).</p>"""),
  dict(kicker="2.3", title="Plusieurs têtes, des positions", sub="têtes d’attention, RoPE, GQA", scene="att", body="""
    <p class="lede">Une seule attention ne suffit pas : le modèle en calcule <b>plusieurs en parallèle</b>, les <b>têtes</b>, chacune sur une tranche différente du vecteur.</p>
    <p>Une tête peut suivre la syntaxe, une autre les références (« il » → « chat »), une autre la position. Leurs sorties sont recollées puis mélangées par une dernière matrice.</p>
    <p>L’attention ne sait pas où est chaque jeton : on injecte l’<b>ordre</b>. Les modèles récents utilisent les <b>positions rotatives</b> (RoPE), qui font tourner Q et K selon la position. Pour économiser la mémoire, beaucoup partagent les clés et valeurs entre plusieurs têtes (<b>GQA</b>), ce qui réduit le cache KV.</p>"""),
  dict(kicker="2.4", title="Le bloc complet", sub="attention, MLP, raccourcis", scene="bloc", body="""
    <p class="lede">Un bloc de transformeur combine deux sous-couches.</p>
    <ul class="rules">
      <li><b>Attention</b> : les jetons s’échangent de l’information.</li>
      <li><b>MLP</b> (réseau dense) : chaque jeton est transformé seul, avec une couche qui élargit puis une qui resserre. C’est là que se trouve la plus grande part des paramètres.</li>
    </ul>
    <p>Autour de chacune : une <b>normalisation</b> et un <b>raccourci résiduel</b> (on ajoute l’entrée à la sortie). Ces raccourcis laissent le signal et le gradient traverser des dizaines de blocs sans s’éteindre.</p>
    <p>Dans un modèle à <b>mélange d’experts</b>, le MLP est remplacé par plusieurs MLP « experts » dont seuls quelques-uns travaillent sur chaque jeton.</p>"""),
  dict(kicker="2.5", title="Empiler et compter", sub="d’où viennent les milliards de paramètres", scene="pile", body="""
    <p class="lede">Le modèle empile <i>N</i> blocs identiques en forme, mais aux poids différents.</p>
    <p>Pour une dimension <i>d</i>, un bloc standard a environ 4<i>d</i>² paramètres pour l’attention et 8<i>d</i>² pour le MLP, soit <b>≈ 12 <i>d</i>²</b>.</p>
    <div class="eq">paramètres ≈ 12 · <i>N</i> · <i>d</i>² + (vocabulaire × <i>d</i>)</div>
    <p>Avec <i>d</i> = 4 096 et <i>N</i> = 32 : 12 × 32 × 4 096² ≈ 6,4 milliards, plus 0,5 milliard pour les plongements : un modèle « de 7 milliards ». Ce nombre de paramètres décide de la mémoire (chapitre 3) et du coût d’entraînement (chapitre 6).</p>"""),
 ],
 practice={0:[dict(q="Dans la matrice d’attention d’un modèle de langage causal, un jeton peut regarder…", choices=["tous les jetons, passés et futurs", "seulement les jetons passés et lui-même", "seulement le jeton suivant", "seulement le premier jeton"], answer=1, why="<p>Le masque causal met à zéro le poids des jetons futurs.</p>")],
           1:[dict(q="Dans l’attention, les poids appliqués aux valeurs sont obtenus…", choices=["en additionnant les clés", "par un softmax appliqué aux scores Q·K", "en prenant le maximum des valeurs", "au hasard"], answer=1, why="<p>Les scores Q·K/√d passent par un softmax : des poids positifs de somme 1, qui pondèrent les valeurs.</p>")],
           4:[dict(q="Combien de paramètres, environ, pour N = 32 blocs et d = 4 096 (hors plongements) ?", choices=["≈ 640 millions", "≈ 6,4 milliards", "≈ 64 milliards", "≈ 640 milliards"], answer=1, why="<p>12 × 32 × 4 096² ≈ 12 × 32 × 1,68 × 10⁷ ≈ 6,4 × 10⁹.</p>")]}
),
dict(dir="inference", no=3, title="Ce qui se passe pendant une inférence", sub="prefill, décodage, cache KV, mémoire", cnt="Du prompt au premier mot, puis aux suivants", alt="Une génération pas à pas avec un cache de clés et de valeurs",
 scenes=[
  dict(key="phase", title="Deux phases", sub="lire l’invite, puis écrire", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.6, loop="un jeton de plus",
       stages=[dict(n="Invite", s="tout le prompt"), dict(n="Prefill", s="en parallèle", pal="blue"), dict(n="Cache KV", s="rempli", pal="red"), dict(n="Décodage", s="1 jeton à la fois", pal="blue"), dict(n="Échantillonnage", s="choisit un mot"), dict(n="Jeton ajouté", s="au cache")],
       plate="L’inférence a deux temps : le prefill traite toute l’invite d’un coup (calcul intense, parallèle), puis le décodage produit les jetons un par un (chaque pas relit le cache et les poids).",
       facts=[["prefill", "limité par le calcul"], ["décodage", "limité par la bande passante mémoire"]], cam=dict(dx=0, y=2.4, dist=26, az=4, el=7, radius=7)),
  dict(key="cache", title="Le cache clé-valeur", sub="ne pas tout recalculer", kind="kv", tokens=["Paris", "est", "la", "capitale", "de", "la", "France"], cy=3.0,
       plate="À chaque pas, seul le nouveau jeton est calculé. Les clés et valeurs de tous les jetons précédents ont déjà été calculées et sont relues dans le cache. Sans cache, on referait tout le calcul de l’invite à chaque nouveau mot.",
       facts=[["sans cache", "coût ∝ n² par réponse"], ["avec cache", "coût ∝ n"], ["prix", "de la mémoire"]], cam=dict(dx=0, y=2.7, dist=25, az=4, el=5, radius=6)),
  dict(key="memoire", title="La mémoire d’un modèle de 7 milliards", sub="poids et cache en gigaoctets", kind="mem", scale=0.18, limit=24, limitLabel="GPU 24 Go",
       configs=[dict(n="Poids fp16", segs=[["Poids", 14, "blue"]]), dict(n="Poids 4 bits", segs=[["Poids", 4, "blue"]]), dict(n="Cache 32k", segs=[["Cache KV", 4, "red"]]), dict(n="Cache sans GQA", segs=[["Cache KV", 16, "red"]])],
       info="exemple : 32 couches, 8 têtes KV de 128, 32 000 jetons de contexte",
       plate="Pour un modèle de 7 milliards de paramètres : 14 Go en 16 bits, environ 4 Go quantifié en 4 bits. Le cache KV s’y ajoute et croît avec le contexte et le nombre de requêtes simultanées. Le partage des têtes (GQA) le divise par quatre ici.",
       facts=[["poids fp16", "2 octets × 7 Md = 14 Go"], ["cache par jeton (GQA)", "128 Ko"], ["32 000 jetons", "≈ 4 Go"]], cam=dict(dx=0, y=2.6, dist=23, az=5, el=5, radius=6)),
  dict(key="spec", title="Le décodage spéculatif", sub="un petit modèle propose, un gros vérifie", kind="pipeline", per=2, bw=3.2, gap=0.9, y=1.6, loop="on recommence",
       stages=[dict(n="Petit modèle", s="propose 4 jetons vite", pal="blue"), dict(n="Gros modèle", s="vérifie les 4 d’un coup", pal="red"), dict(n="Accepter", s="les jetons corrects"), dict(n="Corriger", s="le premier faux")],
       plate="Le gros modèle est lent parce qu’il relit tous ses poids à chaque jeton. Pour en tirer plusieurs par lecture, on laisse un petit modèle proposer quelques jetons, et le gros les vérifie en une seule passe. Le résultat est identique à celui du gros modèle seul.",
       facts=[["gain typique", "×2 à ×3"], ["qualité", "inchangée"]], cam=dict(dx=0, y=2.4, dist=24, az=4, el=6, radius=6)),
 ],
 pages=[
  dict(kicker="Chapitre 3 · tous niveaux", title="Ce qui se passe pendant une inférence", sub="de l’invite au dernier mot", scene="phase", body="""
    <p class="lede">Vous envoyez une question. Que fait la machine entre l’appui sur « envoyer » et le dernier mot ?</p>
    <p>L’<b>inférence</b> (<i>serving</i>) se déroule en deux phases très différentes. Le <b>prefill</b> lit toute l’invite d’un coup. Le <b>décodage</b> écrit ensuite la réponse <b>un jeton à la fois</b>, car chaque jeton dépend du précédent.</p>
    <p>Presque tout ce que l’on règle en production (latence, débit, coût, mémoire) vient de cette asymétrie.</p>"""),
  dict(kicker="3.1", title="Prefill et décodage", sub="deux goulots d’étranglement", scene="phase", body="""
    <p class="lede">Le <b>prefill</b> traite des milliers de jetons en parallèle : c’est du calcul intense, le GPU est occupé. Il détermine le <b>temps avant le premier jeton</b>.</p>
    <p>Le <b>décodage</b> produit un jeton par passe, mais chaque passe doit relire <b>tous les poids</b> depuis la mémoire. Le GPU passe son temps à attendre les données : on est limité par la <b>bande passante mémoire</b>.</p>
    <div class="eq">vitesse maximale ≈ bande passante / taille des poids</div>
    <p>Avec 14 Go de poids et 2 To/s de bande passante, la borne théorique à une requête est d’environ 140 jetons par seconde. Plus de requêtes servies ensemble amortissent cette lecture.</p>"""),
  dict(kicker="3.2", title="Le cache KV", sub="relire au lieu de recalculer", scene="cache", body="""
    <p class="lede">Pour écrire le jeton <i>n</i>, l’attention a besoin des clés et des valeurs des <i>n</i>−1 jetons précédents. Elles ne changent pas : on les <b>garde en mémoire</b>.</p>
    <p>À chaque pas, le modèle calcule Q, K et V du <b>seul nouveau jeton</b>, ajoute K et V au cache, et relit le cache pour son attention. Sans cache, le coût de la réponse grandirait comme le carré de la longueur.</p>
    <p>Le prix est la mémoire : le cache grossit avec la longueur du contexte et le nombre de conversations en cours.</p>"""),
  dict(kicker="3.3", title="Combien de mémoire ?", sub="poids, cache, quantification", scene="memoire", body="""
    <p class="lede">Deux postes pèsent sur la mémoire : les <b>poids</b> et le <b>cache KV</b>.</p>
    <p><b>Poids</b> : nombre de paramètres × octets par paramètre. En 16 bits (2 octets) : 14 Go pour 7 milliards. La <b>quantification</b> (8 bits, 4 bits) divise ce chiffre, au prix d’une petite perte de qualité.</p>
    <div class="eq">cache par jeton = 2 × couches × têtes KV × dim. de tête × octets</div>
    <p>Pour 32 couches, 8 têtes KV de 128 dimensions et 2 octets : 131 072 octets, soit 128 Ko par jeton ; 4 Go pour 32 000 jetons. Avec 32 têtes KV (sans GQA), ce serait 16 Go. Une carte de 24 Go n’accueille donc pas les deux sans compromis.</p>"""),
  dict(kicker="3.4", title="Débit, latence et astuces", sub="batching, pagination, décodage spéculatif", scene="spec", body="""
    <p class="lede">Un serveur d’inférence arbitre entre <b>latence</b> (vitesse perçue par un utilisateur) et <b>débit</b> (jetons produits par seconde au total).</p>
    <ul class="rules">
      <li><b>Batching continu</b> : traiter plusieurs requêtes ensemble, en y faisant entrer de nouvelles dès qu’une se termine.</li>
      <li><b>Cache paginé</b> : découper le cache en pages pour ne pas gaspiller la mémoire.</li>
      <li><b>Cache de préfixe</b> : réutiliser le prefill d’un prompt système identique d’une requête à l’autre.</li>
      <li><b>Décodage spéculatif</b> (figure) : un petit modèle propose, le gros vérifie ; même résultat, souvent deux à trois fois plus vite.</li>
    </ul>"""),
 ],
 practice={1:[dict(q="Pourquoi la phase de décodage est-elle limitée par la bande passante mémoire ?", choices=["elle calcule des matrices immenses", "chaque jeton oblige à relire tous les poids du modèle", "elle écrit beaucoup sur le disque", "elle utilise Internet"], answer=1, why="<p>Un jeton par passe, mais toute la matrice de poids doit être lue à chaque passe : la mémoire, pas le calcul, limite.</p>")],
           2:[dict(q="À quoi sert le cache KV ?", choices=["à stocker les réponses déjà données", "à ne pas recalculer les clés et valeurs des jetons précédents", "à accélérer l’entraînement", "à compresser le vocabulaire"], answer=1, why="<p>Les K et V des jetons déjà traités sont réutilisés à chaque nouveau jeton.</p>")],
           3:[dict(q="Un modèle de 7 milliards de paramètres en 4 bits (0,5 octet par paramètre) pèse environ…", choices=["3,5 Go", "7 Go", "14 Go", "28 Go"], answer=0, why="<p>7 × 10⁹ × 0,5 octet = 3,5 Go (un peu plus en pratique avec les métadonnées).</p>")]}
)]
