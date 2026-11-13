# Pages ajoutées à des chapitres existants, d'après « Atlas des Technologies 3D » (édition novembre 2026)
from common import P, pg

ADDITIONS = {
 "matrices": {"pages": [
   pg("Transformer les normales", "la matrice de normale", "trs",
      "Une normale n’est pas un point : si l’objet est étiré de façon non uniforme, la transformer par la matrice modèle la rend fausse (elle n’est plus perpendiculaire à la surface).",
      "=N = (M₃ₓ₃⁻¹)ᵀ",
      "On utilise la <b>transposée de l’inverse</b> du bloc 3×3 de la matrice modèle, puis on renormalise. Oublier cette règle donne un éclairage qui « glisse » sur un objet mis à l’échelle. Pour une rotation pure, les deux matrices sont identiques.")],
   "practice": {0: [P("Pourquoi utilise-t-on une matrice spéciale pour les normales ?", ["une mise à l’échelle non uniforme ne les garderait pas perpendiculaires à la surface", "pour les colorier", "pour la perspective", "parce que les normales ont w = 1"], 0, "On utilise la transposée de l’inverse de la matrice modèle.")]}},
 "surfaces": {"pages": [
   pg("Topologie et subdivision", "quads, boucles d’arêtes, Catmull-Clark", "buffers",
      "Le GPU dessine des triangles (toujours plans), mais les modeleurs travaillent en <b>quadrilatères</b> : ils guident les boucles d’arêtes, la subdivision et le dépliage UV.",
      ["Une bonne topologie anticipe la <b>déformation</b> : des boucles d’arêtes autour des coudes et des articulations valent mieux qu’un maillage dense et aléatoire.", "<b>Normales de sommets</b> : moyenne des normales des faces voisines, pour un aspect lisse ; des faces inversées créent des taches sombres.",
       "<b>Subdivision de Catmull-Clark</b> (1978) : lisse un maillage de contrôle grossier ; c’est le modificateur Subdivision Surface de Blender.", "<b>Retopologie</b> : reconstruire un maillage propre par-dessus une sculpture ou un scan très dense ; <b>décimation</b> : réduire les triangles."],
      "Nanite (chapitre 51) automatise les niveaux de détail, mais ne dispense pas de comprendre la topologie de départ.")]},
 "courbes": {"pages": [
   pg("Courbes, temps et subdivision", "Bézier dans l’animation", "casteljau",
      "Les courbes de Bézier sont nées dans l’automobile française des années 1960 : Pierre Bézier chez Renault, Paul de Casteljau chez Citroën.",
      ["En animation, les courbes de Bézier décrivent le <b>temps</b> : dans l’éditeur de graphes de Blender ou d’Unreal, leurs poignées règlent l’accélération, l’amortissement et le rebond entre deux images clés.", "Les <b>surfaces de subdivision</b> complètent les NURBS : partir d’un maillage de contrôle et le raffiner. Ce sont les standards des personnages et des formes organiques, les NURBS restant ceux des pièces mécaniques.",
       "En procédural, les courbes guident routes, câbles et tuyaux générés par Geometry Nodes (chapitre 53)."])]},
 "pbr": {"pages": [
   pg("Avant le PBR : Phong et Blinn-Phong", "l’éclairage classique", "brdf",
      "Le modèle de <b>Phong</b> (1975) découpe la lumière en trois termes : <b>ambiant</b> (une constante d’appoint), <b>diffus</b> (loi de Lambert : n·l) et <b>spéculaire</b> (un reflet autour de la direction miroir, élevé à une puissance).",
      "=I = k_a + k_d (n·l) + k_s (r·v)^α",
      "<b>Blinn-Phong</b> remplace r·v par n·h (le vecteur médian entre lumière et vue), plus rapide et plus réaliste. Ces modèles restent utiles pour un rendu stylisé, mais ne conservent pas l’énergie et ignorent Fresnel : le PBR (GGX, popularisé par le modèle de Disney en 2012) les a remplacés.")],
   "practice": {0: [P("Quel terme du modèle de Phong utilise la loi de Lambert ?", ["le terme diffus", "le terme spéculaire", "le terme ambiant", "aucun"], 0, "Il est proportionnel au produit scalaire de la normale et de la direction de la lumière.")]}},
 "guides": {"pages": [
   pg("Toutes les optiques AR comparées", "guides diffractifs, géométriques, birdbath, rétinien", "types",
      (("technologie", "atouts", "limites", "exemples"), ("guide diffractif", "lame fine, industrialisable", "efficacité, arcs-en-ciel, coût", "HoloLens 2, Magic Leap 2"), ("guide géométrique (miroirs)", "efficacité lumineuse, image nette", "épaisseur, fabrication", "Lumus, Epson Moverio"), ("birdbath", "bonne image, coût modéré", "épaisseur, transparence moyenne", "Xreal, lunettes vidéo"), ("rétinien (balayage laser)", "netteté, contraste", "puissance, sécurité, champ", "North Focals (arrêté)"), ("passthrough vidéo", "occlusion, champ large", "pas de transparence, poids", "Quest 3, Vision Pro")),
      "Aucune ne domine : le marché explore tout en même temps, selon quatre axes d’arbitrage : champ de vision, luminosité à l’œil (plusieurs milliers de nits pour l’extérieur), transparence et poids.")]},
 "microoled": {"pages": [
   pg("Micro-OLED et micro-LED sur silicium", "OLEDoS et LEDoS", "ppd",
      ["<b>Micro-OLED</b> (OLED-on-silicon) : 2 000 à 4 000 pixels par pouce ; la logique de pilotage est sous les pixels ; dalles limitées à environ un pouce, luminosité limitée par les matériaux organiques.", "<b>Micro-LED sur silicium</b> (LEDoS) : diodes inorganiques, des dizaines de milliers de nits, longue durée de vie. Déjà en version monochrome (verte) ou couleur dans des lunettes AR légères (JBD, Vuzix, TCL RayNeo).",
       "Le verrou du micro-LED couleur : le <b>rouge</b> à haute densité (rendement des diodes AlGaInP) et le transfert de millions de diodes sans défaut."],
      "La course micro-OLED / micro-LED structure la feuille de route des casques : densité, luminance et efficacité décideront du prochain saut de qualité (chapitre 68).")]},
 "fibres": {"pages": [
   pg("Écrans à fibres et holographie", "d’autres pistes de laboratoire", "chaine",
      "Au-delà de la fibre qui balaie, des équipes universitaires étudient des <b>écrans à fibres</b> : la lumière de micro-LED est injectée dans des fibres de quelques micromètres, dont les extrémités, agencées en matrice, forment les pixels.",
      "Promesses : une densité extrême et une grande souplesse mécanique (un écran courbé autour de l’œil). D’autres travaux combinent fibres et modulateurs de phase pour approcher de vrais hologrammes (chapitre 15). Ces pistes visent les afficheurs rétiniens et les casques ultra-compacts ; elles restent au stade de la recherche.")]},
 "latence": {"pages": [
   pg("La stabilité avant tout", "gigue, encodage, sans-fil", "m2p",
      ["Une cadence <b>stable</b> compte plus qu’une moyenne élevée : la gigue (images irrégulières) est plus nauséeuse qu’une baisse ponctuelle de résolution, d’où la résolution dynamique.", "Les centrales inertielles sont lues à environ 1 000 Hz et fusionnées avec les caméras.",
       "Pour un casque relié sans fil à un PC (Air Link, Virtual Desktop, Steam Link), l’encodage et le décodage vidéo ajoutent environ 10 ms, compensés par la reprojection locale.", "Wi-Fi 6/6E dédié ou câble DisplayPort pour réduire le délai."])]},
 "mains": {"pages": [
   pg("Gants, EMG et corps entier", "au-delà des caméras", "chaine",
      (("capteur", "principe", "exemples"), ("caméras", "réseau sur les images, 21 points par main", "Quest, Vision Pro, MediaPipe, Ultraleap"), ("gants instrumentés", "capteurs de flexion et IMU", "Manus, StretchSense"), ("EMG au poignet", "lire les signaux des muscles et des nerfs", "bracelet de Meta (Orion, 2024)"), ("corps entier", "estimation par caméra ou IA", "BlazePose (33 points), OpenPose, suivi du corps Quest")),
      "L’EMG promet un contrôle discret, sans lever la main ni être vu par une caméra. Les standards de geste se fixent : pincer pour sélectionner, fermer le poing pour saisir, regard + geste pour lever les ambiguïtés.")]},
 "regard": {"pages": [
   pg("Fixations, saccades, poursuites", "le vocabulaire du regard", "chaine",
      ["<b>Fixations</b> : environ 200 à 300 ms, là où l’attention se pose.", "<b>Saccades</b> : sauts très rapides de 20 à 100 ms, pendant lesquels la vision est en partie coupée (suppression saccadique) ; certains moteurs en profitent pour corriger l’image sans que l’on s’en aperçoive.",
       "<b>Poursuites</b> : suivre un objet en mouvement."],
      "Usages en XR : rendu fovéal et compression du flux ; <b>interaction</b> (regarder puis pincer, fixation prolongée) ; <b>avatars</b> dont les yeux vivent ; <b>analyse</b> (recherche UX, formation des pilotes, signatures oculaires étudiées pour certaines maladies neurologiques). La précision des casques (0,5 à 2°) suffit au rendu et à l’interaction ; les analyses fines demandent des appareils dédiés à 250 Hz ou plus.")]},
 "haptique": {"pages": [
   pg("Concevoir l’haptique", "une question d’expérience", "familles",
      "Le retour haptique doit être calibré, synchronisé avec l’image et le son, et jamais envahissant. Les études montrent qu’un retour même approximatif améliore la précision des gestes et la présence lors des manipulations fines.",
      "Pistes de recherche : <b>redirection haptique</b> (faire croire que la main touche un objet virtuel en la guidant vers un vrai objet), peau électronique, retour de chaleur, gants à micro-fluides.")]},
 "blender": {"pages": [
   pg("Blender et les autres logiciels DCC", "une grammaire commune", "entrees",
      "Maya, 3ds Max, Houdini, Cinema 4D et Blender partagent une même grammaire : <b>navigation orbitale</b> autour d’un pivot, vues orthographiques standard, <b>gizmos</b> de transformation, modes (objet, édition, sculpture, UV), éditeurs spécialisés (courbes, nœuds, hiérarchie), et un travail <b>non destructif</b> par modificateurs.",
      "La création immersive se développe à côté : Gravity Sketch (dessin et modélisation en VR), ShapesXR (maquettes d’interfaces), Adobe Substance Modeler (sculpture). Les échanges avec Blender passent par USD, glTF et OpenXR (chapitres 35 et 58).")]},
 "photogrammetrie": {"pages": [
   pg("Photogrammétrie ou gaussiennes ?", "mesurer ou représenter", "chaine",
      "Le Gaussian Splatting part du même résultat SfM (COLMAP), mais saute le MVS et le maillage : il produit directement une scène photoréaliste, en une demi-heure environ.",
      (("besoin", "méthode"), ("mesurer, exporter en CAO, imprimer", "photogrammétrie : maillage et texture"), ("visite immersive, rendu photoréaliste", "gaussiennes (chapitre 40)"), ("les deux", "gaussiennes, puis extraction de surface (2DGS, SuGaR)")),
      "Outils : RealityCapture (RealityScan), Metashape, Meshroom (libre), 3DF Zephyr ; Postshot, Polycam et nerfstudio pour les gaussiennes.")]},
 "nerf": {"pages": [
   pg("Les variantes", "BARF, D-NeRF, et le reste", "entrain",
      ["<b>Poses inconnues</b> : BARF optimise les poses des caméras en même temps que la scène.", "<b>Scènes dynamiques</b> : D-NeRF ajoute le temps en entrée.", "<b>Anticrénelage</b> : Mip-NeRF, Zip-NeRF.",
       "<b>Édition et éclairage</b> : segmentation, relighting."],
      "NeRF reste le choix des scènes statiques à qualité maximale hors temps réel (patrimoine, effets visuels, recherche), et le socle scientifique des méthodes suivantes : la scène comme une fonction dérivable, optimisée par gradient.")]},
 "gaussiennes": {"pages": [
   pg("Usages et défis", "le standard de la capture immersive", "nuage",
      "En deux ans, les gaussiennes sont devenues le standard de fait de la capture immersive : visites virtuelles, objets pour la XR, ralentis sportifs en 3D, décors de fond dans les moteurs de jeu.",
      ["Défis : reflets parfaits et transparence, mémoire (des centaines de Mo par scène), pas de maillage propre pour la CAO ou l’impression, contrôle artistique.", "Réponses : Mip-Splatting (anticrénelage), compression, extraction de surfaces, gaussiennes animées et 4D, génération de gaussiennes par texte."])]},
 "generation": {"pages": [
   pg("La génération en production", "ce qui change pour les artistes", "direct",
      "Entre les deux vagues (SDS puis générateurs natifs), d’autres familles ont marqué l’histoire : Point-E et Shap-E (OpenAI) génèrent des nuages de points ou des champs implicites ; les grands modèles de reconstruction (LRM) passent d’une image à la 3D en un seul passage.",
      ["Enjeux de production : topologie propre et UV automatiques pour l’animation, cohérence entre vues, contrôle fin (style, proportions, articulations).", "Enjeux juridiques : licences des données d’entraînement et droits des artistes."],
      "Le scénario le plus probable n’est pas la fin des artistes 3D mais un changement de métier : générer, évaluer, retopologiser, intégrer, comme la photographie numérique a transformé le métier de l’image sans le supprimer.")]},
 "datasets": {"pages": [
   pg("Données synthétiques et gouvernance", "fabriquer la vérité terrain", "prep",
      "Le réel ne fournit jamais une vérité terrain parfaite. Les <b>données synthétiques</b> (scènes rendues par un moteur, avec randomisation des matériaux, des lumières et des caméras) donnent une profondeur, des normales et des segmentations exactes : Hypersim (intérieurs photoréalistes) pour l’estimation de profondeur, simulateurs pour la robotique.",
      "La <b>gouvernance</b> devient centrale : les corpus agrégés du web ont des licences hétérogènes ; la communauté construit des corpus aux licences ouvertes et respecte le refus des créateurs (opt-out). L’évaluation des modèles 3D (qualité géométrique, fidélité au texte, topologie utilisable) reste largement humaine.")]},
 "avenir": {"pages": [
   pg("Les modèles du monde", "de la 3D implicite à la 3D explicite", "convergence",
      "Les générateurs vidéo (Sora et ses successeurs) montrent une compréhension implicite de la 3D : perspective, occlusion, parallaxe. Les modèles interactifs (Genie, agents incarnés) apprennent des environnements où l’on agit.",
      "La question ouverte : ces représentations implicites deviendront-elles des scènes 3D <b>explicites</b>, éditables, utilisables dans les moteurs et les casques ? Trois chantiers sont déjà en marche : des <b>jumeaux numériques</b> vivants (capture, gaussiennes, capteurs), des <b>assistants visuels</b> dans des lunettes, et la <b>création augmentée</b>, du texte à la scène animée.",
      "Plus la 3D devient automatique, plus comprendre ce qu’elle fait (où est la caméra, comment la lumière interagit, quelle latence le corps tolère) devient décisif pour la diriger.")]},
}
CHAPTERS = []
