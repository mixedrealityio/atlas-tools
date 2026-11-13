# Atlas de l'IA : chapitres 14 à 19 (voir l'IA en 3D, paramétrage, matériel)
GROUPS = [("Voir l’IA en 3D", ["reseau3d", "modele3d"]), ("Paramétrer et dimensionner", ["parametres", "puce", "cluster", "egpu"])]
CHAPTERS = [
dict(dir="reseau3d", no=14, title="Voir un réseau de neurones en 3D", sub="neurones, cartes, tenseurs, paysage de la perte", cnt="Rendre visible ce qui n’est que nombres", alt="Un réseau de neurones et un bloc de nombres en trois dimensions",
 scenes=[
  dict(key="mlp", title="Un petit réseau", sub="4 → 6 → 6 → 3 neurones", kind="net", layers=[4, 6, 6, 3], names=["Entrée", "Couche cachée 1", "Couche cachée 2", "Sortie"], params="93 paramètres : 78 poids + 15 biais",
       plate="Chaque neurone calcule une somme pondérée de ses entrées puis applique une fonction non linéaire. Chaque trait est un poids. Ce petit réseau a 78 poids et 15 biais : 93 paramètres. Un grand modèle de langage en a des dizaines de milliards, mais l’ossature est la même.",
       facts=[["poids", "4×6 + 6×6 + 6×3 = 78"], ["biais", "6 + 6 + 3 = 15"], ["total", "93 paramètres"]]),
  dict(key="cnn", title="Un réseau convolutif en cartes", sub="de 28 × 28 pixels à 10 classes", kind="fmaps",
       layers=[dict(n="Entrée", size=28, depth=1, dim="28×28×1"), dict(n="Convolution", size=24, depth=6, dim="24×24×6"), dict(n="Mise en commun", size=12, depth=6, dim="12×12×6"), dict(n="Convolution", size=8, depth=16, dim="8×8×16"), dict(n="Mise en commun", size=4, depth=16, dim="4×4×16"), dict(n="Dense", size=1, depth=1, vec=120, dim="120"), dict(n="Sortie", size=1, depth=1, vec=10, dim="10 classes")],
       plate="C’est la manière de TensorSpace : chaque couche d’un réseau convolutif est une pile de cartes. La largeur diminue (mise en commun) pendant que le nombre de cartes augmente, jusqu’aux couches denses et à la sortie.",
       facts=[["cartes", "une par filtre"], ["réduction", "la taille baisse, la profondeur monte"]], cam=dict(az=14, el=8)),
  dict(key="bloc", title="Le bloc de nombres d’un transformeur", sub="jetons × dimensions × couches", kind="tensor", tokens=6, dims=6, depth=5,
       plate="Pendant un calcul, un transformeur manipule un bloc de nombres : une ligne par jeton, une colonne par dimension, et une tranche par couche. Chaque couche transforme la tranche précédente. Avec 1 000 jetons, 4 096 dimensions et 32 couches, cela fait 131 millions de valeurs.",
       facts=[["exemple réel", "1 000 × 4 096 × 32 ≈ 1,3 × 10⁸ valeurs"], ["activations", "ce qu’on garde pour la rétropropagation"]], cam=dict(az=28, el=16)),
  dict(key="paysage", title="Le paysage de la perte", sub="trois façons de descendre", kind="landscape",
       plate="La perte est une altitude : chaque position est un réglage possible des poids. Entraîner, c’est descendre. Avec un taux trop faible, on avance à peine ; avec un taux adapté, on rejoint la vallée ; avec un taux trop fort, on rebondit d’un versant à l’autre. Ici 2 poids : un vrai modèle en a des milliards.",
       facts=[["dimensions", "2 ici ; des milliards en vrai"], ["méthode", "descente de gradient"]], cam=dict(az=20, el=24)),
 ],
 pages=[
  dict(kicker="Chapitre 14 · tous niveaux", title="Voir un réseau de neurones en 3D", sub="rendre visible ce qui n’est que nombres", scene="mlp", body="""
    <p class="lede">Un modèle d’IA est un tableau de nombres et des opérations. Rien de cela ne se voit : c’est pourquoi on a inventé des manières de le <b>dessiner en 3D</b>.</p>
    <p>L’idée n’est pas neuve. <b>TensorSpace</b>, un cadre libre né en Chine vers 2018 sur Three.js et TensorFlow.js, affiche dans un navigateur chaque couche d’un réseau convolutif sous forme d’une pile de cartes, que l’on peut tourner et inspecter. Cet atlas reprend ce principe pour tous les types de modèles.</p>
    <p>Ce chapitre montre quatre vues : le <b>réseau de neurones</b>, les <b>cartes</b> d’un réseau convolutif, le <b>bloc de nombres</b> d’un transformeur et le <b>paysage de la perte</b>.</p>"""),
  dict(kicker="14.1", title="Neurones et couches", sub="la brique de base", scene="mlp", body="""
    <p class="lede">Un <b>neurone</b> artificiel fait deux choses : une somme pondérée de ses entrées, puis une fonction non linéaire (par exemple « ne garder que le positif »).</p>
    <div class="eq"><i>y</i> = σ( Σ <i>w</i><sub>i</sub> <i>x</i><sub>i</sub> + <i>b</i> )</div>
    <p>Les <i>w</i> sont les <b>poids</b>, <i>b</i> le <b>biais</b> : ce sont les paramètres appris. Une <b>couche</b> regroupe des neurones qui lisent les mêmes entrées ; le réseau en enchaîne plusieurs.</p>
    <p>La figure compte : 4 × 6 + 6 × 6 + 6 × 3 = 78 poids, plus 15 biais, soit 93 paramètres. La couleur indique la couche active à l’instant : l’information avance couche après couche.</p>"""),
  dict(kicker="14.2", title="Les cartes d’un réseau convolutif", sub="la vue TensorSpace", scene="cnn", body="""
    <p class="lede">Dans un réseau convolutif (chapitre 8), chaque couche produit plusieurs <b>cartes</b> de la taille de l’image ou de moins.</p>
    <p>Ici : une image de 28 × 28 pixels, six filtres 5 × 5 (six cartes de 24 × 24), une réduction à 12 × 12, seize filtres (cartes de 8 × 8), une nouvelle réduction à 4 × 4, puis une couche dense de 120 valeurs et dix scores de sortie. C’est l’architecture d’un lecteur de chiffres manuscrits, de la famille de LeNet.</p>
    <p>La largeur de chaque pile se lit d’un coup d’œil : <b>moins de pixels, plus de cartes</b>.</p>"""),
  dict(kicker="14.3", title="Le bloc de nombres du transformeur", sub="ce qui circule vraiment", scene="bloc", body="""
    <p class="lede">Un transformeur n’a pas de neurones visibles : il manipule un <b>bloc de nombres</b> à trois axes.</p>
    <ul class="rules">
      <li>un axe pour les <b>jetons</b> de la séquence ;</li>
      <li>un axe pour les <b>dimensions</b> du modèle (4 096 pour un modèle de 7 milliards) ;</li>
      <li>un axe pour les <b>couches</b> : chacune lit la tranche précédente et en écrit une nouvelle.</li>
    </ul>
    <p>Ces nombres sont les <b>activations</b>. Pour 1 000 jetons, 4 096 dimensions et 32 couches : environ 131 millions de valeurs, stockées pendant l’entraînement pour la rétropropagation, d’où l’importance du recalcul d’activations (chapitre 6).</p>"""),
  dict(kicker="14.4", title="Le paysage de la perte", sub="descendre en 3D", scene="paysage", body="""
    <p class="lede">Imaginez que chaque réglage possible des poids soit un point d’un terrain, et que la <b>perte</b> en soit l’altitude. Entraîner un modèle, c’est <b>descendre</b> vers une vallée.</p>
    <p>La figure en montre trois descentes depuis le même point, avec trois taux d’apprentissage : trop faible (la boule avance à peine), adapté (elle rejoint la vallée), trop fort (elle rebondit d’un versant à l’autre). Le chapitre 6 en donne les ordres de grandeur.</p>
    <p>Attention : ce terrain a <b>deux dimensions</b>. Celui d’un vrai modèle en a des milliards, et ses « pièges » sont surtout des cols plutôt que des cuvettes, ce qui facilite la descente.</p>"""),
  dict(kicker="14.5", title="Voir soi-même", sub="outils pour inspecter un modèle", scene="mlp", body="""
    <p class="lede">Plusieurs outils permettent d’explorer un modèle sans écrire de visualisation.</p>
    <ul class="rules">
      <li><b>TensorSpace</b> : réseaux convolutifs en 3D dans le navigateur (projet libre, plus ancien, centré sur les CNN).</li>
      <li><b>Netron</b> : affiche le graphe d’opérations d’un fichier de modèle (ONNX et autres).</li>
      <li><b>TensorBoard</b> : suit les courbes de perte, les distributions de poids et les graphes pendant l’entraînement.</li>
      <li><b>Projecteurs de plongements</b> : placent des vecteurs en 2D ou 3D pour voir quels mots se regroupent (chapitre 1).</li>
      <li><b>Visualisations pédagogiques de transformeurs</b> : certaines déroulent en 3D, couche par couche, le calcul d’un petit modèle de langage.</li>
    </ul>"""),
 ],
 practice={1:[dict(q="Combien de paramètres a un réseau 4 → 6 → 3 (poids et biais) ?", choices=["24", "42", "51", "72"], answer=2, why="<p>Poids : 4×6 + 6×3 = 42 ; biais : 6 + 3 = 9 ; total 51.</p>")],
           2:[dict(q="Quand on avance dans un réseau convolutif, en général…", choices=["la taille des cartes augmente et leur nombre baisse", "la taille des cartes diminue et leur nombre augmente", "tout reste identique", "les cartes disparaissent"], answer=1, why="<p>La mise en commun réduit la taille, les couches suivantes ajoutent des filtres.</p>")],
           4:[dict(q="Pour 2 000 jetons, 4 096 dimensions et 32 couches, combien de valeurs d’activation, environ ?", choices=["≈ 26 millions", "≈ 260 millions", "≈ 2,6 milliards", "≈ 26 milliards"], answer=1, why="<p>2 000 × 4 096 × 32 ≈ 2,6 × 10⁸.</p>")]}
),
dict(dir="modele3d", no=15, title="L’IA et la modélisation 3D", sub="NeRF, gaussiennes, génération d’objets", cnt="Reconstruire et fabriquer des objets en 3D", alt="Un nuage de gaussiennes qui forme un objet en 3D",
 scenes=[
  dict(key="reps", title="Les représentations 3D", sub="cinq façons de décrire un objet", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4,
       stages=[dict(n="Nuage de points", s="des points dans l’espace"), dict(n="Voxels", s="des cubes, comme des pixels 3D"), dict(n="Maillage", s="sommets + triangles", pal="blue"), dict(n="Champ de distance (SDF)", s="une fonction : dedans / dehors", pal="red"), dict(n="Radiance (NeRF)", s="densité + couleur partout", pal="red"), dict(n="Gaussiennes", s="des taches 3D qui se projettent", pal="blue")],
       plate="Il n’existe pas une seule manière de décrire un objet 3D. Les jeux et la CAO utilisent des maillages ; les réseaux de neurones aiment les champs continus (SDF, NeRF) ; les gaussiennes offrent un rendu rapide. On passe de l’un à l’autre par des algorithmes (par exemple marching cubes pour extraire un maillage d’un champ).",
       facts=[["maillage", "standard des jeux et de la CAO"], ["NeRF", "continu, lent à rendre"], ["gaussiennes", "explicite, rapide"]]),
  dict(key="nerf", title="Le principe de NeRF", sub="un réseau qui prédit densité et couleur", kind="pipeline", per=4, bw=1.9, gap=0.65, y=1.4, loop="ajuster le réseau",
       stages=[dict(n="Photos", s="plusieurs angles"), dict(n="Un rayon par pixel", s="depuis la caméra"), dict(n="Échantillons", s="points sur le rayon", pal="blue"), dict(n="Réseau", s="(x, y, z, vue) → densité, couleur", pal="red"), dict(n="Rendu volumique", s="cumule le long du rayon"), dict(n="Comparer", s="à la vraie photo", pal="blue")],
       plate="NeRF apprend une fonction qui, pour un point de l’espace et une direction de vue, donne une densité et une couleur. On génère l’image en cumulant ces valeurs le long de chaque rayon, on la compare à la photo, et on ajuste le réseau.",
       facts=[["entrée", "position 3D + direction"], ["sortie", "densité + couleur"], ["défaut", "entraînement et rendu lents"]]),
  dict(key="gauss", title="Les gaussiennes 3D", sub="un nuage qui s’ajuste aux photos", kind="cloud",
       plate="Le gaussian splatting représente la scène par des millions de gaussiennes 3D (position, taille, orientation, couleur, opacité). On les projette sur l’image, on compare à la photo, et on ajuste chaque gaussienne. Le rendu est assez rapide pour du temps réel.",
       facts=[["primitives", "gaussiennes 3D explicites"], ["rendu", "temps réel (≥ 30 images/s)"], ["optimisation", "descente de gradient"]], cam=dict(az=18, el=16)),
  dict(key="gen3d", title="Générer un objet", sub="d’un texte ou d’une image au maillage texturé", kind="pipeline", per=4, bw=1.9, gap=0.65, y=1.4,
       stages=[dict(n="Texte ou image", s="la demande"), dict(n="Diffusion de forme", s="dans un espace latent", pal="blue"), dict(n="Surface", s="marching cubes", pal="red"), dict(n="Maillage", s="sans texture"), dict(n="Textures", s="vues multiples, puis fusion", pal="blue"), dict(n="Objet 3D", s="matériaux prêts à l’emploi", pal="red")],
       plate="Les générateurs 3D récents séparent deux étapes : d’abord la forme (un modèle de diffusion produit un champ de distance, dont on extrait un maillage), puis la texture (un modèle de diffusion peint l’objet depuis plusieurs vues, fusionnées en une carte de texture).",
       facts=[["étape 1", "géométrie"], ["étape 2", "texture et matériaux"], ["exemple libre", "Hunyuan3D (Tencent)"]]),
 ],
 pages=[
  dict(kicker="Chapitre 15 · tous niveaux", title="L’IA et la modélisation 3D", sub="reconstruire et fabriquer des objets", scene="reps", body="""
    <p class="lede">Modéliser en 3D, c’est décrire la forme et l’apparence d’un objet. Longtemps l’affaire d’artistes et de capteurs, c’est aujourd’hui aussi celle de modèles d’IA.</p>
    <p>Deux problèmes : la <b>reconstruction</b> (à partir de photos d’un objet réel, retrouver sa forme) et la <b>génération</b> (inventer un objet à partir d’un texte ou d’une image). Ils reposent sur les mêmes idées que le reste de cet atlas : une fonction apprise, une comparaison, une descente de gradient.</p>"""),
  dict(kicker="15.1", title="Représenter un objet", sub="points, voxels, maillages, champs", scene="reps", body="""
    <p class="lede">Le choix de la <b>représentation</b> décide de ce qu’on peut faire.</p>
    <ul class="rules">
      <li><b>Maillage</b> : sommets et triangles. Le format des jeux, de la CAO et de l’impression 3D.</li>
      <li><b>Nuage de points, voxels</b> : simples, mais lourds ou grossiers.</li>
      <li><b>Champ implicite</b> (SDF) : une fonction dit si un point est dedans ou dehors. On en extrait un maillage par <i>marching cubes</i>.</li>
      <li><b>Champ de radiance</b> (NeRF) et <b>gaussiennes</b> : pensés pour reproduire des images, pas pour être modifiés par un artiste.</li>
    </ul>"""),
  dict(kicker="15.2", title="NeRF", sub="un champ de lumière appris", scene="nerf", body="""
    <p class="lede">En 2020, <b>NeRF</b> (<i>neural radiance field</i>) a montré qu’un petit réseau pouvait mémoriser une scène entière.</p>
    <p>On lui donne un point de l’espace et une direction de vue ; il renvoie une <b>densité</b> (y a-t-il de la matière ?) et une <b>couleur</b>. Pour obtenir un pixel, on lance un rayon, on cumule densités et couleurs le long du rayon (le <b>rendu volumique</b>), et on compare le résultat à la vraie photo. Quelques dizaines de photos suffisent.</p>
    <p>Défaut : l’entraînement dure longtemps et chaque image coûte beaucoup de calcul.</p>"""),
  dict(kicker="15.3", title="Les gaussiennes 3D", sub="le « splatting »", scene="gauss", body="""
    <p class="lede">Le <b>3D Gaussian Splatting</b> (2023) remplace le réseau par des millions de petites <b>gaussiennes 3D</b> explicites.</p>
    <p>Chacune a une position, une taille, une orientation, une couleur et une opacité. Pour faire une image, on les projette (« éclabousse ») sur l’écran ; on compare aux photos et on ajuste chaque gaussienne par descente de gradient, comme les poids d’un réseau. La figure rejoue cette optimisation : le nuage désordonné se resserre en un tore.</p>
    <p>Le gain majeur est la <b>vitesse de rendu</b>, assez grande pour afficher la scène en temps réel. Le défaut : on obtient un nuage, pas un maillage propre.</p>"""),
  dict(kicker="15.4", title="Générer des objets", sub="forme, puis texture", scene="gen3d", body="""
    <p class="lede">Pour <b>fabriquer</b> un objet à partir d’un texte ou d’une image, les modèles récents procèdent en deux temps.</p>
    <ol class="rules">
      <li><b>La forme</b> : un modèle de diffusion (chapitre 8) travaille dans un espace latent de formes et produit un champ de distance ; on en extrait un maillage.</li>
      <li><b>La texture</b> : un second modèle de diffusion peint l’objet vu de plusieurs angles, en s’appuyant sur la géométrie ; les vues sont fusionnées en une carte de texture, parfois avec des matériaux réalistes.</li>
    </ol>
    <p>Des laboratoires chinois comme Tencent (<b>Hunyuan3D</b>) ont publié ce type de modèles en libre accès, ce qui permet de les faire tourner chez soi sur un GPU.</p>"""),
  dict(kicker="15.5", title="De l’objet généré à l’objet utilisable", sub="ce qui reste à faire", scene="reps", body="""
    <p class="lede">Un objet généré est impressionnant en image, moins en production.</p>
    <ul class="rules">
      <li><b>Topologie</b> : les maillages générés sont souvent trop denses ou irréguliers ; on les simplifie et on les « retopologise ».</li>
      <li><b>Dépliage UV et matériaux</b> : pour que la texture s’applique proprement, avec des matériaux physiques (PBR).</li>
      <li><b>Échelle et précision</b> : un objet beau n’est pas un objet aux bonnes cotes, ce qui compte en CAO ou en impression 3D.</li>
      <li><b>Usages</b> : jeux et effets visuels, jumeaux numériques, simulation pour la robotique (chapitre 12), commerce en ligne.</li>
    </ul>"""),
 ],
 practice={1:[dict(q="Quelle représentation est la plus utilisée dans les jeux vidéo ?", choices=["le maillage de triangles", "le champ de radiance NeRF", "les voxels", "le nuage de points"], answer=0, why="<p>Les cartes graphiques sont optimisées pour dessiner des triangles texturés.</p>")],
           2:[dict(q="Que renvoie le réseau NeRF pour un point de l’espace vu sous une direction ?", choices=["un maillage", "une densité et une couleur", "une photo entière", "un identifiant d’objet"], answer=1, why="<p>On cumule ensuite ces valeurs le long du rayon pour obtenir la couleur du pixel.</p>")],
           3:[dict(q="Quel est le principal avantage du gaussian splatting sur NeRF ?", choices=["il produit directement un maillage propre", "il se rend beaucoup plus vite", "il n’a pas besoin de photos", "il n’a aucun paramètre"], answer=1, why="<p>Projeter des gaussiennes explicites est bien plus rapide que de questionner un réseau le long de chaque rayon.</p>")]}
),
dict(dir="parametres", no=16, title="Le tableau de bord des paramètres", sub="quantification, contexte, serveur", cnt="Ce que chaque réglage change en mémoire, en vitesse, en qualité", alt="La mémoire d’une carte graphique répartie entre poids et cache",
 scenes=[
  dict(key="panneau", title="Quatre familles de réglages", sub="du bouton au gigaoctet", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Entraînement", s="taux, lot, époques, rang", pal="blue"), dict(n="Échantillonnage", s="T, top-p, min-p, graine", pal="red"), dict(n="Mémoire", s="quantification, contexte, lot", pal="blue"), dict(n="Serveur", s="GPU, parallélisme, file", pal="red")],
       plate="Les réglages d’un modèle ouvert tiennent en quatre familles. Les deux premières changent le comportement (chapitres 4 et 6). Les deux dernières changent ce qui tient dans la machine et la vitesse : c’est l’objet de ce chapitre.",
       facts=[["comportement", "entraînement, échantillonnage"], ["ressources", "mémoire, serveur"]]),
  dict(key="quant", title="La quantification", sub="un modèle de 8 milliards en gigaoctets", kind="mem", scale=0.15, limit=24, limitLabel="GPU 24 Go",
       configs=[dict(n="16 bits", segs=[["Poids", 16, "blue"]]), dict(n="Q8_0", segs=[["Poids", 8.5, "blue"]]), dict(n="Q5_K_M", segs=[["Poids", 5.7, "blue"]]), dict(n="Q4_K_M", segs=[["Poids", 4.9, "blue"]])],
       plate="Les poids d’un modèle de 8 milliards pèsent 16 Go en 16 bits. Les formats de quantification de llama.cpp (Q8, Q5, Q4) les réduisent à 8,5, 5,7 et 4,9 Go environ, au prix d’une perte de qualité d’autant plus petite que le nombre de bits est élevé.",
       facts=[["Q4_K_M", "≈ 4,9 bits par poids"], ["Q5_K_M", "≈ 5,7 bits par poids"], ["Q8_0", "≈ 8,5 bits par poids"]]),
  dict(key="ctx", title="Le contexte coûte de la mémoire", sub="cache KV selon la longueur", kind="mem", scale=0.15, limit=24, limitLabel="GPU 24 Go",
       configs=[dict(n="Poids Q4", segs=[["Poids", 4.9, "blue"]]), dict(n="Cache 8k", segs=[["Cache KV", 1, "red"]]), dict(n="Cache 32k", segs=[["Cache KV", 4, "red"]]), dict(n="Cache 128k", segs=[["Cache KV", 16, "red"]])],
       info="8 milliards, 32 couches, 8 têtes KV de 128 : 128 Ko par jeton",
       plate="Le cache KV grossit avec la longueur du contexte : 128 Ko par jeton pour ce modèle, soit 1 Go pour 8 000 jetons, 4 Go pour 32 000 et 16 Go pour 128 000. Un grand contexte peut peser plus que les poids quantifiés.",
       facts=[["formule", "2 × couches × têtes KV × dim × octets"], ["par jeton", "128 Ko ici"], ["×  utilisateurs", "le cache se multiplie"]]),
  dict(key="serveur", title="Un serveur d’inférence réglé", sub="gpu_memory_utilization sur une carte de 24 Go", kind="mem", scale=0.15, limit=24, limitLabel="GPU 24 Go",
       configs=[dict(n="0,85", segs=[["Poids", 16, "blue"], ["Contexte CUDA", 1, "dark"], ["Cache KV", 3.4, "red"], ["Réserve", 3.6, "paper"]]), dict(n="0,95", segs=[["Poids", 16, "blue"], ["Contexte CUDA", 1, "dark"], ["Cache KV", 5.8, "red"], ["Réserve", 1.2, "paper"]])],
       info="chiffres illustratifs pour un modèle de 8 milliards en 16 bits",
       plate="Un serveur comme vLLM réserve une fraction de la mémoire du GPU : il charge les poids, garde un peu pour le contexte CUDA, et consacre le reste au cache KV. Monter la fraction de 0,85 à 0,95 agrandit le cache, donc le nombre de requêtes simultanées, mais réduit la marge.",
       facts=[["valeur courante", "0,85 à 0,90"], ["à éviter", "1,0 : aucune marge"]]),
 ],
 pages=[
  dict(kicker="Chapitre 16 · intermédiaire", title="Le tableau de bord des paramètres", sub="tout ce qui se règle, et ce que ça change", scene="panneau", body="""
    <p class="lede">Un modèle à poids ouverts s’accompagne d’un tableau de bord de réglages. Mieux vaut savoir ce que chacun fait que les essayer au hasard.</p>
    <p>On peut les ranger en quatre familles : ceux qui règlent l’<b>entraînement</b> (chapitre 6), ceux qui règlent l’<b>échantillonnage</b> (chapitre 4), ceux qui règlent la <b>mémoire</b> (quantification, longueur de contexte, taille de lot), et ceux du <b>serveur</b> (répartition sur les GPU, file d’attente).</p>
    <p>Ce chapitre traite des deux dernières, qui décident de ce qu’on peut faire tourner chez soi.</p>"""),
  dict(kicker="16.1", title="Quantifier les poids", sub="moins de bits par nombre", scene="quant", body="""
    <p class="lede">Un poids stocké sur 16 bits peut l’être sur 8, 5 ou 4 bits : le fichier rétrécit presque proportionnellement.</p>
    <div class="eq">taille ≈ paramètres × bits par poids ÷ 8</div>
    <p>Exemple : 8 milliards × 4,9 ÷ 8 ≈ 4,9 Go en <b>Q4_K_M</b> (format de llama.cpp, le plus répandu), contre 16 Go en 16 bits. Les formats « K » mélangent plusieurs précisions, avec plus de bits pour les parties sensibles.</p>
    <p>La perte de qualité est faible vers 5 à 8 bits, mesurable vers 4 bits, et nette en dessous de 3. Les sources divergent sur les chiffres exacts : testez sur vos propres tâches.</p>"""),
  dict(kicker="16.2", title="Le contexte et le cache KV", sub="la mémoire qui grandit", scene="ctx", body="""
    <p class="lede">Les poids sont fixes ; le <b>cache KV</b> grandit avec chaque jeton lu ou écrit.</p>
    <div class="eq">cache = 2 × couches × têtes KV × dim. de tête × jetons × lots × octets</div>
    <p>Pour notre modèle de 8 milliards (32 couches, 8 têtes KV de 128), cela fait 128 Ko par jeton : 4 Go pour 32 000 jetons, 16 Go pour 128 000. Avec plusieurs utilisateurs en parallèle, tout se multiplie.</p>
    <p>On le réduit en <b>quantifiant le cache</b> (8 bits au lieu de 16), en choisissant des modèles à peu de têtes KV (GQA), ou en limitant le contexte au nécessaire.</p>"""),
  dict(kicker="16.3", title="Régler un serveur", sub="vLLM, llama.cpp, Ollama", scene="serveur", body="""
    <p class="lede">Chaque moteur expose ses boutons. Les plus utiles :</p>
    <table class="data">
      <tr><th>réglage</th><th>effet</th></tr>
      <tr><td>vLLM · <i>gpu_memory_utilization</i></td><td>part de la mémoire du GPU utilisée (0,85 à 0,9)</td></tr>
      <tr><td>vLLM · <i>max_model_len</i></td><td>contexte maximal, donc taille du cache</td></tr>
      <tr><td>vLLM · <i>max_num_seqs</i>, <i>tensor_parallel_size</i></td><td>requêtes simultanées ; nombre de GPU</td></tr>
      <tr><td>llama.cpp · <i>-ngl</i></td><td>couches placées sur le GPU, le reste en RAM</td></tr>
    </table>"""),
  dict(kicker="16.4", title="Ce qui change quoi", sub="mémoire, vitesse, qualité", scene="panneau", body="""
    <p class="lede">Chaque réglage déplace trois curseurs à la fois.</p>
    <table class="data">
      <tr><th>on augmente…</th><th>mémoire</th><th>vitesse</th><th>qualité</th></tr>
      <tr><td>les bits par poids</td><td>plus</td><td>plus lent</td><td>meilleure</td></tr>
      <tr><td>la longueur de contexte</td><td>plus (cache)</td><td>plus lent</td><td>plus de contexte utile</td></tr>
      <tr><td>le nombre de requêtes simultanées</td><td>plus (cache)</td><td>meilleur débit total</td><td>inchangée</td></tr>
      <tr><td>la température</td><td>—</td><td>—</td><td>plus variée, moins fiable</td></tr>
      <tr><td>le taux d’apprentissage (affinage)</td><td>—</td><td>—</td><td>trop fort : oubli</td></tr>
    </table>
    <p>Règle pratique : fixer d’abord le modèle et la quantification qui <b>tiennent</b>, puis le contexte nécessaire, puis régler la vitesse.</p>"""),
 ],
 practice={1:[dict(q="Combien pèse environ un modèle de 14 milliards de paramètres quantifié à 4,9 bits par poids ?", choices=["≈ 4,3 Go", "≈ 8,6 Go", "≈ 14 Go", "≈ 28 Go"], answer=1, why="<p>14 × 4,9 ÷ 8 ≈ 8,6 Go.</p>")],
           2:[dict(q="Avec 128 Ko de cache par jeton, combien de mémoire pour 64 000 jetons ?", choices=["≈ 1 Go", "≈ 4 Go", "≈ 8 Go", "≈ 16 Go"], answer=2, why="<p>64 000 × 128 Ko ≈ 8,2 Go (soit 8 Go environ).</p>")],
           3:[dict(q="Pourquoi déconseille-t-on gpu_memory_utilization = 1,0 ?", choices=["le modèle devient plus lent", "il ne reste aucune marge de mémoire", "il désactive le cache", "il change la température"], answer=1, why="<p>Sans marge, un pic d’utilisation fait planter le serveur.</p>")]}
),
dict(dir="puce", no=17, title="Dans un GPU", sub="calcul, mémoire, précisions, débits", cnt="Pourquoi la mémoire compte autant que le calcul", alt="Une puce de GPU avec ses unités de calcul et sa mémoire",
 scenes=[
  dict(key="puce", title="Une puce de GPU", sub="des milliers d’unités et de la mémoire proche", kind="chip",
       plate="Un GPU contient plusieurs dizaines à plus d’une centaine de multiprocesseurs (SM), chacun avec des cœurs de calcul et des cœurs tenseur dédiés aux produits de matrices. Autour de la puce, des piles de mémoire HBM fournissent des milliers de gigaoctets par seconde.",
       facts=[["SM", "plus de 100 sur un H100"], ["HBM", "mémoire empilée, très large"], ["cœurs tenseur", "produits de matrices"]]),
  dict(key="roofline", title="Calcul ou mémoire : qui limite ?", sub="le modèle du toit (roofline)", kind="curve", fn="roofline",
       plate="Pour chaque octet lu en mémoire, on effectue un certain nombre d’opérations : c’est l’intensité arithmétique. Si elle est faible, la mémoire limite (montée en pente) ; si elle est élevée, c’est le calcul (plateau). Le décodage d’un modèle de langage, à une requête, est tout à gauche.",
       facts=[["décodage, 1 requête", "≈ 1 opération par octet"], ["prefill, gros lots", "des centaines"], ["conséquence", "la mémoire limite le décodage"]]),
  dict(key="prec", title="Les précisions", sub="chaque étage divise la mémoire", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="FP32", s="4 octets", pal="dark"), dict(n="BF16 / FP16", s="2 octets", pal="blue"), dict(n="FP8", s="1 octet", pal="blue"), dict(n="INT4 / FP4", s="0,5 octet", pal="red")],
       plate="Moins de bits, c’est moins de mémoire et moins de données à lire, donc un modèle plus rapide. L’entraînement utilise BF16 (et de plus en plus FP8), l’inférence descend souvent à 8 ou 4 bits.",
       facts=[["entraînement", "BF16, parfois FP8"], ["inférence", "16, 8 ou 4 bits"], ["coût", "perte de précision"]]),
  dict(key="debits", title="L’échelle des débits", sub="de l’SSD à la mémoire HBM", kind="logbars", unit="Go/s", axis="échelle logarithmique : chaque graduation est 10 fois plus grande",
       items=[dict(n="SSD NVMe", v=7, pal="dark"), dict(n="PCIe 4 ×16", v=32, pal="dark"), dict(n="DDR5 (PC)", v=90, pal="paper"), dict(n="Mac M3 Max", v=400, pal="blue"), dict(n="RTX 4090", v=1008, pal="blue"), dict(n="A100", v=2039, pal="red"), dict(n="H100", v=3350, pal="red")],
       plate="Chaque niveau de mémoire est environ dix fois plus rapide que le précédent. C’est la raison de tous les compromis : plus un poids est loin du calcul, plus il coûte cher à lire. Débits théoriques en gigaoctets par seconde, ordres de grandeur.",
       facts=[["SSD → GPU", "quelques Go/s"], ["HBM d’un H100", "3 350 Go/s"], ["rapport", "≈ 500 ×"]]),
 ],
 pages=[
  dict(kicker="Chapitre 17 · intermédiaire", title="Dans un GPU", sub="la machine qui calcule le modèle", scene="puce", body="""
    <p class="lede">Un GPU n’est pas un « gros processeur » : c’est une machine à faire des <b>produits de matrices en parallèle</b>, avec une mémoire très rapide autour.</p>
    <p>La puce contient des dizaines à des centaines de <b>multiprocesseurs</b> (SM), chacun avec ses cœurs et ses <b>cœurs tenseur</b>, spécialisés dans la multiplication-accumulation de petites matrices. Tout autour, des piles de mémoire <b>HBM</b> collées à la puce, avec un bus très large.</p>
    <p>Les chapitres précédents ont montré qu’un modèle, c’est surtout cela : des produits de matrices. Ce chapitre explique pourquoi le matériel qui les fait décide de la vitesse.</p>"""),
  dict(kicker="17.1", title="Calcul et mémoire", sub="deux ressources distinctes", scene="puce", body="""
    <p class="lede">Un GPU a deux limites indépendantes : <b>combien d’opérations il fait par seconde</b>, et <b>combien d’octets il lit par seconde</b>.</p>
    <table class="data">
      <tr><th>GPU</th><th>calcul BF16</th><th>mémoire</th><th>capacité</th></tr>
      <tr><td>A100</td><td>≈ 312 TFLOPs</td><td>≈ 2 To/s</td><td>80 Go</td></tr>
      <tr><td>H100 SXM</td><td>≈ 989 TFLOPs</td><td>≈ 3,35 To/s</td><td>80 Go</td></tr>
      <tr><td>RTX 4090</td><td>≈ 10² TFLOPs</td><td>≈ 1 To/s</td><td>24 Go</td></tr>
    </table>
    <p>Valeurs des constructeurs, en ordres de grandeur (dense, sans « sparsité »).</p>"""),
  dict(kicker="17.2", title="Le mur de la mémoire", sub="pourquoi le décodage est lent", scene="roofline", body="""
    <p class="lede">Pour produire un jeton, le modèle lit <b>chaque poids une fois</b> et fait environ deux opérations dessus : une multiplication, une addition.</p>
    <p>Cela fait de l’ordre d’une opération par octet lu, très loin du seuil où le calcul devient la limite (près de 300 sur un H100). Le GPU attend donc la mémoire, comme le montre la pente de la figure.</p>
    <div class="eq">jetons par seconde ≲ bande passante ÷ taille des poids</div>
    <p>Exemple : 3 350 Go/s ÷ 14 Go ≈ 240 jetons par seconde pour un modèle de 7 milliards en 16 bits, sur un H100, <b>pour une seule requête</b>. Servir plusieurs requêtes à la fois réutilise les poids lus et fait monter l’intensité.</p>"""),
  dict(kicker="17.3", title="Les précisions", sub="moins de bits, plus de vitesse", scene="prec", body="""
    <p class="lede">Chaque nombre peut être stocké sur 32, 16, 8 ou 4 bits.</p>
    <p>Diviser les bits par deux divise par deux la mémoire occupée <b>et</b> la quantité à lire, donc <b>double à peu près la vitesse de décodage</b>. Les GPU récents ont même des unités dédiées aux formats courts (FP8, FP4).</p>
    <p>L’entraînement exige plus de précision pour accumuler de petites corrections (BF16 pour les poids, FP32 pour les cumuls). L’inférence supporte mieux les formats courts, surtout avec des méthodes de quantification qui protègent les poids les plus sensibles.</p>"""),
  dict(kicker="17.4", title="L’échelle des débits", sub="chaque niveau, dix fois plus rapide", scene="debits", body="""
    <p class="lede">Entre le disque et le cœur de calcul, la donnée traverse plusieurs niveaux, chacun environ <b>dix fois plus rapide</b> que le précédent.</p>
    <p>Un SSD donne quelques Go/s, un bus PCIe 4.0 ×16 une trentaine, la mémoire d’un PC une centaine, celle d’un Mac haut de gamme quelques centaines, celle d’un GPU de bureau environ un To/s, celle d’un GPU de centre de données plus de trois.</p>
    <p>La conséquence pratique : un modèle qui <b>tient entièrement dans la mémoire du GPU</b> va vite ; dès qu’une partie est ailleurs, elle est lue par un chemin 10 à 100 fois plus lent.</p>"""),
  dict(kicker="17.5", title="Au-delà d’un seul fournisseur", sub="le paysage du matériel d’IA", scene="puce", body="""
    <p class="lede">Un GPU de centre de données n’est pas un produit unique. Plusieurs fabricants proposent des accélérateurs d’IA, avec des architectures voisines.</p>
    <p>En Chine, des acteurs comme Huawei (série Ascend), Cambricon ou Moore Threads développent leurs propres puces. La difficulté tient moins à la puce qu’au <b>logiciel</b> : pilotes, bibliothèques de calcul, compilateurs, outils d’entraînement. C’est ce socle qui décide qu’un modèle tourne facilement sur une puce, ou non.</p>
    <p>Les grands principes de ce chapitre (calcul, mémoire, débits, précisions) s’appliquent à tous.</p>"""),
 ],
 practice={1:[dict(q="Pourquoi le décodage d’un LLM à une requête est-il limité par la mémoire ?", choices=["il fait trop de calculs", "il lit tous les poids pour très peu d’opérations par octet", "le GPU manque de cœurs", "l’image est trop grande"], answer=1, why="<p>Intensité arithmétique d’environ 1 opération par octet, très en dessous du seuil de calcul.</p>")],
           2:[dict(q="Un modèle pèse 28 Go et la bande passante est 1 To/s. Borne de vitesse à une requête ?", choices=["≈ 3,6 jetons/s", "≈ 36 jetons/s", "≈ 360 jetons/s", "≈ 3 600 jetons/s"], answer=1, why="<p>1 000 Go/s ÷ 28 Go ≈ 36 jetons/s.</p>")],
           3:[dict(q="Passer de 16 à 8 bits par poids, à qualité acceptable, fait en gros…", choices=["doubler la mémoire", "diviser par deux la mémoire et la lecture", "ne rien changer", "multiplier par 4 la précision"], answer=1, why="<p>Moitié moins d’octets à stocker et à lire.</p>")]}
),
dict(dir="cluster", no=18, title="Du GPU au centre de données", sub="nœuds, réseaux, énergie, pannes", cnt="Comment des milliers de GPU travaillent ensemble", alt="Des serveurs de huit GPU reliés par un commutateur réseau",
 scenes=[
  dict(key="grappe", title="Une grappe de GPU", sub="quatre nœuds de huit GPU", kind="cluster", nodes=4, gpus=8,
       plate="Un nœud réunit huit GPU reliés entre eux par NVLink, très rapide. Les nœuds sont reliés par un réseau (InfiniBand ou Ethernet) environ dix à vingt fois plus lent. Pour entraîner, les GPU échangent sans cesse leurs gradients ; la topologie décide de ce qui est possible.",
       facts=[["NVLink (H100)", "900 Go/s par GPU"], ["InfiniBand NDR", "400 Gbit/s ≈ 50 Go/s par port"], ["rapport", "≈ 18 ×"]]),
  dict(key="para", title="Placer le parallélisme", sub="chaque type de découpage à sa place", kind="pipeline", per=2, bw=3.4, gap=0.9, y=1.4,
       stages=[dict(n="Tenseurs", s="dans un nœud : NVLink", pal="red"), dict(n="Experts", s="souvent dans un nœud", pal="red"), dict(n="Pipeline", s="entre nœuds voisins", pal="blue"), dict(n="Données", s="sur tout le cluster", pal="blue")],
       plate="Le découpage des matrices (parallélisme de tenseurs) échange beaucoup de données à chaque couche : on le garde dans un nœud, sur NVLink. Le pipeline échange peu, entre étages ; les copies de données n’échangent qu’à la fin d’une étape : elles peuvent s’étendre sur tout le réseau.",
       facts=[["règle", "le plus bavard au plus près"], ["tenseurs", "NVLink"], ["données", "réseau entre nœuds"]]),
  dict(key="watts", title="L’échelle de la puissance", sub="du GPU à la salle", kind="logbars", unit="kW", axis="échelle logarithmique, ordres de grandeur",
       items=[dict(n="GPU H100", v=0.7, pal="blue"), dict(n="Serveur 8 GPU", v=10, pal="blue"), dict(n="Armoire de 72 GPU", v=120, pal="red"), dict(n="10 000 GPU", v=14000, pal="red")],
       plate="Un GPU de centre de données consomme environ 700 W, un serveur de huit GPU une dizaine de kilowatts, une armoire de 72 GPU à refroidissement liquide plus de 100 kW, et un cluster de dix mille GPU de l’ordre de dix mégawatts avec refroidissement et réseau.",
       facts=[["GPU", "≈ 0,7 kW"], ["serveur 8 GPU", "≈ 10 kW"], ["cluster de 10 000", "≈ 10 MW ou plus"]]),
  dict(key="pannes", title="Tenir en cas de panne", sub="sauvegarder pour reprendre", kind="pipeline", per=3, bw=2.3, gap=0.8, y=1.4, loop="dernier point de contrôle",
       stages=[dict(n="Entraîner", s="des milliers de GPU", pal="blue"), dict(n="Point de contrôle", s="sauvegarde régulière", pal="red"), dict(n="Panne", s="un GPU, un câble…"), dict(n="Détecter", s="et isoler le matériel"), dict(n="Redémarrer", s="depuis le point de contrôle", pal="blue")],
       plate="Avec des dizaines de milliers de composants, une panne arrive en heures, parfois en minutes. On sauvegarde régulièrement l’état complet (points de contrôle) et on repart du dernier après avoir isolé le matériel défaillant.",
       facts=[["fréquence", "une panne toutes les quelques heures à grande échelle"], ["remède", "points de contrôle fréquents"]]),
 ],
 pages=[
  dict(kicker="Chapitre 18 · avancé", title="Du GPU au centre de données", sub="quand un GPU ne suffit plus", scene="grappe", body="""
    <p class="lede">Un modèle de plusieurs centaines de milliards de paramètres ne tient pas dans un GPU, et mettrait des siècles à s’entraîner sur un seul. On en associe des milliers.</p>
    <p>Mais deux GPU ne font pas simplement deux fois plus : ils doivent <b>échanger des données</b>, et ces échanges passent par des fils de vitesses très différentes. Tout l’art d’un cluster consiste à faire circuler peu de données sur les fils lents.</p>
    <p>On appelle parfois <b>« clusters de dix mille cartes »</b> (万卡集群, en chinois) ces grappes à très grande échelle, où le réseau et les pannes deviennent le problème principal.</p>"""),
  dict(kicker="18.1", title="Le nœud de huit GPU", sub="NVLink, le réseau interne", scene="grappe", body="""
    <p class="lede">Un <b>nœud</b> est un serveur qui réunit typiquement <b>huit GPU</b>.</p>
    <p>Ils sont reliés par <b>NVLink</b> et des commutateurs NVSwitch, qui donnent à chaque GPU environ <b>900 Go/s</b> vers les autres (génération H100). C’est presque la vitesse de leur propre mémoire : les huit GPU se comportent comme un grand GPU.</p>
    <p>Des machines récentes étendent ce domaine : une armoire de 72 GPU reliés par NVLink forme un seul « super-nœud », refroidi par liquide.</p>"""),
  dict(kicker="18.2", title="Relier les nœuds", sub="InfiniBand, Ethernet, topologies", scene="grappe", body="""
    <p class="lede">Entre les nœuds, le réseau offre de l’ordre de <b>400 Gbit/s par port</b> (environ 50 Go/s), soit dix-huit fois moins qu’au sein d’un nœud.</p>
    <p>Les technologies courantes sont <b>InfiniBand</b> et les variantes d’<b>Ethernet</b> conçues pour l’IA. La topologie la plus courante est l’<b>arbre épais</b> (<i>fat-tree</i>), où deux nœuds quelconques disposent de la même bande passante ; des options moins chères existent, mais peuvent se congestionner.</p>
    <p>À grande échelle, le réseau est souvent la limite : quand il sature, les GPU attendent et les calculs perdent en efficacité.</p>"""),
  dict(kicker="18.3", title="Placer les parallélismes", sub="le plus bavard au plus près", scene="para", body="""
    <p class="lede">Les quatre découpages du chapitre 6 n’ont pas les mêmes besoins en communication.</p>
    <ul class="rules">
      <li><b>Tenseurs</b> : échanges à chaque couche, donc dans un nœud, sur NVLink.</li>
      <li><b>Experts</b> : chaque jeton va à son expert, dans un nœud ou des nœuds proches.</li>
      <li><b>Pipeline</b> : seules les activations d’une frontière circulent, entre nœuds voisins.</li>
      <li><b>Données</b> : on moyenne les gradients en fin d’étape, sur tout le cluster.</li>
    </ul>
    <p><b>MFU</b> : part du calcul théorique réellement utilisée, souvent 30 à 50 %.</p>"""),
  dict(kicker="18.4", title="Énergie, chaleur, pannes", sub="le côté physique", scene="watts", body="""
    <p class="lede">Concevoir un cluster, c’est aussi gérer des mégawatts.</p>
    <ul class="rules">
      <li><b>Puissance</b> : un GPU 700 W, un serveur ≈ 10 kW, une armoire dense plus de 100 kW. Un cluster de dix mille GPU demande de l’ordre de dix mégawatts.</li>
      <li><b>Refroidissement</b> : au-delà d’une trentaine de kilowatts par armoire, l’air ne suffit plus ; on passe au <b>refroidissement liquide</b>.</li>
      <li><b>Pannes</b> : plus on a de composants, plus il y en a qui cassent. On sauvegarde régulièrement l’état de l’entraînement (points de contrôle) et on reprend après la panne.</li>
      <li><b>Coût</b> : l’énergie et le temps de GPU font partie du prix de chaque jeton.</li>
    </ul>"""),
 ],
 practice={1:[dict(q="Pourquoi garde-t-on le parallélisme de tenseurs à l’intérieur d’un nœud ?", choices=["parce qu’il utilise peu de mémoire", "parce qu’il échange des données à chaque couche et a besoin du lien le plus rapide", "parce qu’il n’a pas besoin de GPU", "parce qu’il est plus facile à programmer"], answer=1, why="<p>Les échanges fréquents exigent NVLink ; le réseau entre nœuds est trop lent.</p>")],
           2:[dict(q="NVLink à 900 Go/s et InfiniBand à 50 Go/s : le rapport est d’environ…", choices=["2", "18", "180", "1 800"], answer=1, why="<p>900 ÷ 50 = 18.</p>")],
           3:[dict(q="Que sauvegarde-t-on avec un point de contrôle ?", choices=["uniquement la dernière réponse", "l’état complet de l’entraînement pour pouvoir reprendre après une panne", "le fichier du tokenizer", "la température"], answer=1, why="<p>Poids, états de l’optimiseur et position dans les données.</p>")]}
),
dict(dir="egpu", no=19, title="GPU externes et matériel local", sub="Thunderbolt, OCuLink, mémoire, dimensionnement", cnt="Faire tourner un modèle ouvert chez soi", alt="Un ordinateur portable relié à un GPU externe",
 scenes=[
  dict(key="liens", title="Le lien compte moins que la mémoire", sub="débits en Go/s, échelle logarithmique", kind="logbars", unit="Go/s", axis="échelle logarithmique : ordres de grandeur",
       items=[dict(n="Thunderbolt 4", v=3.5, pal="dark"), dict(n="OCuLink ×4", v=7.9, pal="blue"), dict(n="PCIe 4 ×16", v=31.5, pal="blue"), dict(n="PCIe 5 ×16", v=63, pal="blue"), dict(n="VRAM RTX 4090", v=1008, pal="red")],
       plate="Le lien entre l’ordinateur et le GPU externe (Thunderbolt, OCuLink) est bien plus lent que la mémoire du GPU. Peu importe tant que tout le modèle est dans la mémoire du GPU : le lien ne sert qu’à charger les poids et à échanger quelques jetons.",
       facts=[["Thunderbolt 4", "40 Gbit/s, dont une part en PCIe (≈ 3 à 4 Go/s utiles)"], ["OCuLink ×4", "PCIe 4.0 ×4 ≈ 7,9 Go/s théoriques"], ["VRAM", "≈ 1 000 Go/s"]]),
  dict(key="chaine", title="Un GPU en boîtier", sub="de l’ordinateur à la carte", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Ordinateur", s="portable ou mini-PC"), dict(n="Câble", s="Thunderbolt ou OCuLink", pal="blue"), dict(n="Boîtier eGPU", s="alimentation dédiée", pal="red"), dict(n="GPU", s="mémoire vive : 16 à 24 Go", pal="red")],
       plate="Un GPU externe est une vraie carte graphique de bureau dans un boîtier avec son alimentation, relié à l’ordinateur par un câble. On gagne la mémoire et la puissance de calcul d’une carte de bureau sans changer d’ordinateur.",
       facts=[["boîtier", "alimentation 300 à 750 W"], ["câble", "court et blindé (OCuLink)"]]),
  dict(key="choix", title="Quel modèle sur quelle carte ?", sub="poids en 4 bits, carte de 24 Go", kind="mem", scale=0.15, limit=24, limitLabel="carte 24 Go",
       configs=[dict(n="8B Q4", segs=[["Poids", 4.9, "blue"]]), dict(n="14B Q4", segs=[["Poids", 8.6, "blue"]]), dict(n="32B Q4", segs=[["Poids", 19.6, "blue"]]), dict(n="70B Q4", segs=[["Poids", 42.9, "red"]])],
       info="sans le cache KV ni la marge (à ajouter)",
       plate="En 4 bits, un modèle de 8 milliards tient dans moins de 5 Go, un de 14 milliards dans moins de 9, un de 32 milliards dans environ 20 Go : tout juste sur une carte de 24 Go, avec peu de place pour le cache. Un modèle de 70 milliards (43 Go) déborde.",
       facts=[["formule", "poids + cache KV + marge ≤ mémoire"], ["marge", "1 à 2 Go"]]),
  dict(key="debord", title="Quand le modèle déborde", sub="une partie des couches en RAM", kind="pipeline", per=4, bw=1.9, gap=0.7, y=1.4,
       stages=[dict(n="Couches en VRAM", s="1 000 Go/s", pal="blue"), dict(n="Couches en RAM", s="≈ 90 Go/s", pal="dark"), dict(n="Par le bus PCIe", s="≈ 32 Go/s", pal="red"), dict(n="Chaque jeton", s="attend le maillon lent", pal="red")],
       plate="Quand le modèle ne tient pas, des couches restent en RAM et sont lues à chaque jeton par le bus PCIe, de dix à trente fois plus lent que la mémoire du GPU. La vitesse s’effondre dès que quelques couches débordent.",
       facts=[["effet", "vitesse divisée par plusieurs fois"], ["remèdes", "quantifier, réduire le contexte, plus de VRAM"]]),
 ],
 pages=[
  dict(kicker="Chapitre 19 · pratique", title="GPU externes et matériel local", sub="faire tourner un modèle ouvert chez soi", scene="liens", body="""
    <p class="lede">Faire tourner un modèle ouvert chez soi demande une chose avant tout : de la <b>mémoire vive de carte graphique</b> (VRAM).</p>
    <p>Un portable n’en a presque pas ; un <b>GPU externe</b> (eGPU) lui en ajoute : une carte de bureau dans un boîtier, reliée par un câble Thunderbolt ou OCuLink. Il devient populaire en Chine, où les mini-PC avec port OCuLink sont répandus.</p>
    <p>Ce chapitre répond à trois questions : le <b>câble</b> ralentit-il le modèle ? <b>quel modèle</b> tient dans quelle carte ? et que se passe-t-il quand il <b>déborde</b> ?</p>"""),
  dict(kicker="19.1", title="Brancher un GPU", sub="boîtier, alimentation, câble", scene="chaine", body="""
    <p class="lede">Un eGPU, ce sont trois choses : une <b>carte</b>, un <b>boîtier avec alimentation</b>, un <b>câble</b>.</p>
    <ul class="rules">
      <li><b>Thunderbolt 3, 4</b> : un seul câble, avec charge et données ; le débit total est de 40 Gbit/s, dont seule une partie sert au PCIe.</li>
      <li><b>OCuLink</b> : une liaison PCIe directe, sans la couche Thunderbolt ; elle offre près de deux fois plus de débit utile, mais nécessite un port sur la machine et un câble court et blindé.</li>
      <li>La <b>carte</b> décide de la mémoire et de la vitesse : 16 à 24 Go sont le minimum confortable pour des modèles de 8 à 32 milliards en 4 bits.</li>
    </ul>"""),
  dict(kicker="19.2", title="Le câble ralentit-il le modèle ?", sub="peu, tant que tout tient en VRAM", scene="liens", body="""
    <p class="lede">Le lien sert à <b>charger les poids</b> au début, puis à faire passer le texte entrant et sortant.</p>
    <p>Charger 20 Go à 3,5 Go/s prend environ 6 secondes ; à 7,9 Go/s, 2,5 secondes. Ensuite, <b>tout le calcul se fait dans la carte</b>, à la vitesse de sa mémoire (autour de 1 To/s). Des mesures de blogs rapportent une perte de quelques pour cent avec OCuLink et plus nette avec Thunderbolt : sources isolées, à vérifier sur votre machine.</p>
    <p>En affinage, les échanges avec l’ordinateur sont plus fréquents : le lien pèse davantage.</p>"""),
  dict(kicker="19.3", title="Quel modèle sur quelle carte", sub="poids + cache + marge", scene="choix", body="""
    <p class="lede">Règle : <b>poids + cache KV + marge ≤ mémoire de la carte</b>.</p>
    <p>Poids = paramètres × bits ÷ 8 (chapitre 16). Pour une carte de 24 Go : un modèle de 8 milliards en 4 bits (≈ 5 Go) laisse beaucoup de place au cache ; un de 32 milliards (≈ 20 Go) la limite à 2 ou 3 Go, soit un contexte court ; un de 70 milliards (≈ 43 Go) exige deux cartes.</p>
    <p>Choisissez le plus gros modèle qui tienne avec le contexte voulu : un petit modèle bien quantifié vaut mieux qu’un grand modèle qui déborde.</p>"""),
  dict(kicker="19.4", title="Quand ça déborde", sub="la RAM, le bus, la chute de vitesse", scene="debord", body="""
    <p class="lede">Si le modèle ne tient pas dans la carte, certains moteurs placent quelques couches en RAM.</p>
    <p>Chaque jeton doit alors lire ces couches par le bus PCIe (≈ 32 Go/s pour un ×16) et la RAM (≈ 90 Go/s), bien plus lents que la mémoire du GPU (≈ 1 000 Go/s). <b>Une seule couche qui déborde</b> impose son rythme à toute la génération.</p>
    <p>Mieux vaut d’abord réduire la quantification, raccourcir le contexte ou quantifier le cache KV. Le déport sur la RAM reste un dernier recours : il permet d’exécuter un modèle, pas de l’exécuter vite.</p>"""),
  dict(kicker="19.5", title="Pièges et alternatives", sub="alimentation, Mac, cloud", scene="chaine", body="""
    <p class="lede">Avant d’acheter, quelques vérifications.</p>
    <ul class="rules">
      <li><b>Compatibilité</b> : un Mac à puce Apple <b>n’accepte pas</b> de GPU externe. Sa force est la <b>mémoire unifiée</b> : jusqu’à plusieurs centaines de Go, avec une bande passante de 400 à 800 Go/s, ce qui convient bien à de gros modèles quantifiés, mais pas aux outils CUDA.</li>
      <li><b>Alimentation</b> : une carte de bureau demande 300 à 450 W et une alimentation à la hauteur ; prévoyez aussi le refroidissement.</li>
      <li><b>Câble</b> : court et blindé, sinon pertes de débit ou déconnexions.</li>
      <li><b>Logiciel</b> : pilotes et bibliothèques (CUDA sur NVIDIA, ROCm sur AMD) ; la même carte n’offre pas la même facilité d’un système à l’autre.</li>
      <li><b>Alternative</b> : louer des heures de GPU dans le cloud pour les besoins ponctuels, plutôt que d’acheter du matériel peu utilisé.</li>
    </ul>"""),
 ],
 practice={1:[dict(q="Combien de temps pour charger 24 Go à 3 Go/s ?", choices=["≈ 1 s", "≈ 8 s", "≈ 72 s", "≈ 8 min"], answer=1, why="<p>24 ÷ 3 = 8 secondes.</p>")],
           2:[dict(q="Un modèle de 32 milliards en 4,9 bits par poids tient-il dans 24 Go avec 4 Go de cache ?", choices=["oui, avec de la marge", "non : 19,6 + 4 dépasse presque la carte, il reste peu de marge", "oui, il n’y a que 5 Go de poids", "non, jamais"], answer=1, why="<p>32 × 4,9 ÷ 8 ≈ 19,6 Go ; avec 4 Go de cache on atteint 23,6 Go sur 24, sans marge.</p>")],
           3:[dict(q="Quelle est la conséquence d’un modèle qui déborde en RAM ?", choices=["rien de notable", "la vitesse chute, car chaque jeton lit des couches par un chemin bien plus lent", "la qualité augmente", "la mémoire du GPU double"], answer=1, why="<p>Les couches en RAM sont lues à chaque jeton par le bus PCIe, dix à trente fois plus lent.</p>")]}
)]
