#!/usr/bin/env python3
"""Génère les feuilles d'équations en français des trois atlas : maths, chimie, compléments de physique.
Balisage dans les données : {x} italique · _{..} indice · ^{..} exposant · !{..} vecteur."""
import os, re, html
SITE = os.path.expanduser("~/vault/atlas_of_physics_local/atlas-of-physics.vercel.app/")
def md(s):
    s = re.sub(r"!\{([^{}]*)\}", r'<i class="vec">\1</i>', s)
    s = re.sub(r"(?<![_^])\{([^{}]*)\}", r"<i>\1</i>", s)
    p = None
    while p != s:
        p = s
        s = re.sub(r"_\{([^{}]*)\}", r"<sub>\1</sub>", s); s = re.sub(r"\^\{([^{}]*)\}", r"<sup>\1</sup>", s)
    return s
MATHS = ("Maths", "Atlas des maths", "Collège · lycée · MPSI", [
 ("Algèbre", [
  ("Identités remarquables", "({a}+{b})^{2} = {a}^{2} + 2{ab} + {b}^{2} ;  ({a}−{b})^{2} = {a}^{2} − 2{ab} + {b}^{2}", "{a}^{2} − {b}^{2} = ({a}−{b})({a}+{b})"),
  ("Second degré : discriminant", "Δ = {b}^{2} − 4{ac}", "pour {ax}^{2}+{bx}+{c} = 0, {a} ≠ 0"),
  ("Racines", "{x} = (−{b} ± √Δ) / 2{a}", "si Δ > 0 ; une racine double −{b}/2{a} si Δ = 0 ; aucune racine réelle si Δ < 0"),
  ("Somme et produit des racines", "{x}_{1}+{x}_{2} = −{b}/{a} ;  {x}_{1}{x}_{2} = {c}/{a}", ""),
  ("Forme canonique", "{a}({x}−α)^{2} + β", "α = −{b}/2{a}, β = {f}(α)"),
  ("Inégalité des moyennes", "({a}+{b})/2 ≥ √({ab})", "pour {a}, {b} ≥ 0, égalité si {a} = {b}"),
  ("Suite arithmétique", "{u}_{n} = {u}_{0} + {nr} ;  Σ = (n+1)({u}_{0}+{u}_{n})/2", "{r} : raison ; somme des termes de 0 à {n}"),
  ("Suite géométrique", "{u}_{n} = {u}_{0}{q}^{n} ;  Σ = {u}_{0}(1−{q}^{n+1})/(1−{q})", "{q} ≠ 1 ; converge vers 0 si |{q}| < 1"),
  ("Binôme de Newton", "({a}+{b})^{n} = Σ_{k=0}^{n} C({n},{k}) {a}^{k}{b}^{n−k}", ""),
 ]),
 ("Géométrie", [
  ("Pythagore", "{a}^{2} + {b}^{2} = {c}^{2}", "triangle rectangle d’hypoténuse {c} ; la réciproque donne la rectangularité"),
  ("Thalès", "AM/AB = AN/AC = MN/BC", "(MN) parallèle à (BC), M sur (AB), N sur (AC)"),
  ("Aires usuelles", "triangle ½{bh} ;  disque π{r}^{2} ;  trapèze ½({B}+{b}){h}", "périmètre du cercle 2π{r}"),
  ("Volumes usuels", "cylindre π{r}^{2}{h} ;  cône ⅓π{r}^{2}{h} ;  pyramide ⅓{B}{h}", "{B} : aire de la base"),
  ("Sphère", "{V} = 4π{r}^{3}/3 ;  {A} = 4π{r}^{2}", ""),
  ("Distance de deux points", "AB = √(({x}_{B}−{x}_{A})^{2} + ({y}_{B}−{y}_{A})^{2})", "dans l’espace, on ajoute le terme en {z}"),
  ("Équation d’un cercle", "({x}−{a})^{2} + ({y}−{b})^{2} = {r}^{2}", "centre ({a}, {b}), rayon {r}"),
  ("Angle inscrit", "angle au centre = 2 × angle inscrit", "interceptant le même arc"),
 ]),
 ("Trigonométrie", [
  ("Relation fondamentale", "cos^{2}θ + sin^{2}θ = 1", ""),
  ("Tangente", "tan θ = sin θ / cos θ", "cos θ ≠ 0"),
  ("Addition", "cos({a}+{b}) = cos {a} cos {b} − sin {a} sin {b}", "sin({a}+{b}) = sin {a} cos {b} + cos {a} sin {b}"),
  ("Duplication", "sin 2{a} = 2 sin {a} cos {a}", "cos 2{a} = cos^{2}{a} − sin^{2}{a} = 2cos^{2}{a} − 1 = 1 − 2sin^{2}{a}"),
  ("Angles", "π rad = 180°", "longueur d’arc {s} = {r}θ (θ en radians)"),
  ("Loi des cosinus", "{a}^{2} = {b}^{2} + {c}^{2} − 2{bc} cos Â", "généralise Pythagore"),
  ("Loi des sinus", "{a}/sin Â = {b}/sin B̂ = {c}/sin Ĉ", ""),
 ]),
 ("Fonctions, dérivées", [
  ("Dérivées usuelles", "({x}^{n})′ = {n}{x}^{n−1} ;  (√{x})′ = 1/(2√{x}) ;  (1/{x})′ = −1/{x}^{2}", ""),
  ("Exponentielle, logarithme", "(e^{x})′ = e^{x} ;  (ln {x})′ = 1/{x}", "pour {x} > 0 avec le logarithme"),
  ("Trigonométrie", "(sin {x})′ = cos {x} ;  (cos {x})′ = −sin {x} ;  (tan {x})′ = 1 + tan^{2}{x}", ""),
  ("Produit, quotient", "({uv})′ = {u}′{v} + {uv}′ ;  ({u}/{v})′ = ({u}′{v} − {uv}′)/{v}^{2}", ""),
  ("Composée", "({v}∘{u})′ = {u}′ × {v}′∘{u} ;  (e^{u})′ = {u}′e^{u} ;  (ln {u})′ = {u}′/{u}", ""),
  ("Tangente en {a}", "{y} = {f}({a}) + {f}′({a})({x}−{a})", ""),
 ]),
 ("Exponentielle et logarithme", [
  ("Propriétés de l’exponentielle", "e^{a+b} = e^{a}e^{b} ;  e^{−a} = 1/e^{a} ;  (e^{a})^{n} = e^{na}", ""),
  ("Propriétés du logarithme", "ln({ab}) = ln {a} + ln {b} ;  ln({a}/{b}) = ln {a} − ln {b} ;  ln({a}^{n}) = {n} ln {a}", "{a}, {b} > 0"),
  ("Puissance réelle", "{a}^{x} = e^{x ln {a}}", "{a} > 0"),
  ("Croissances comparées", "ln {x}/{x} → 0 ;  e^{x}/{x} → +∞", "quand {x} → +∞"),
  ("Logarithme décimal", "log {x} = ln {x} / ln 10", ""),
 ]),
 ("Intégrales", [
  ("Primitives usuelles", "∫{x}^{n} d{x} = {x}^{n+1}/(n+1) + C ;  ∫ d{x}/{x} = ln|{x}| + C", "{n} ≠ −1"),
  ("Exponentielle, trigonométrie", "∫e^{x} d{x} = e^{x} + C ;  ∫cos {x} d{x} = sin {x} + C ;  ∫sin {x} d{x} = −cos {x} + C", ""),
  ("Intégrale et primitive", "∫_{a}^{b} {f}({x}) d{x} = F({b}) − F({a})", "F : une primitive de {f}"),
  ("Valeur moyenne", "{μ} = 1/({b}−{a}) ∫_{a}^{b} {f}({x}) d{x}", ""),
  ("Intégration par parties", "∫_{a}^{b} {u}′{v} = [{uv}]_{a}^{b} − ∫_{a}^{b} {uv}′", ""),
 ]),
 ("Développements limités en 0", [
  ("Exponentielle", "e^{x} = 1 + {x} + {x}^{2}/2! + … + {x}^{n}/{n}! + o({x}^{n})", ""),
  ("Sinus, cosinus", "sin {x} = {x} − {x}^{3}/3! + {x}^{5}/5! − … ;  cos {x} = 1 − {x}^{2}/2! + {x}^{4}/4! − …", ""),
  ("Logarithme", "ln(1+{x}) = {x} − {x}^{2}/2 + {x}^{3}/3 − …", ""),
  ("Série géométrique", "1/(1−{x}) = 1 + {x} + {x}^{2} + … + {x}^{n} + o({x}^{n})", ""),
  ("Puissance", "(1+{x})^{α} = 1 + α{x} + α(α−1){x}^{2}/2 + …", ""),
 ]),
 ("Nombres complexes", [
  ("Définition", "i^{2} = −1 ;  {z} = {a} + i{b}", "partie réelle {a}, partie imaginaire {b}"),
  ("Conjugué et module", "{z̄} = {a} − i{b} ;  |{z}|^{2} = {z}{z̄} = {a}^{2} + {b}^{2}", ""),
  ("Forme exponentielle", "{z} = {r}e^{iθ} = {r}(cos θ + i sin θ)", "{r} = |{z}|, θ = arg {z}"),
  ("Euler", "e^{iθ} = cos θ + i sin θ ;  e^{iπ} + 1 = 0", ""),
  ("Moivre", "(cos θ + i sin θ)^{n} = cos {n}θ + i sin {n}θ", ""),
  ("Racines {n}-ièmes de l’unité", "ω_{k} = e^{2iπ{k}/{n}},  {k} = 0, …, {n}−1", ""),
 ]),
 ("Dénombrement, probabilités", [
  ("Factorielle, arrangements", "{n}! = 1×2×…×{n} ;  A({n},{p}) = {n}!/({n}−{p})!", "listes ordonnées de {p} éléments distincts"),
  ("Combinaisons", "C({n},{p}) = {n}! / ({p}!({n}−{p})!)", "parties à {p} éléments d’un ensemble à {n} éléments"),
  ("Probabilité d’une réunion", "P({A}∪{B}) = P({A}) + P({B}) − P({A}∩{B})", ""),
  ("Probabilité conditionnelle", "P_{B}({A}) = P({A}∩{B}) / P({B})", ""),
  ("Probabilités totales, Bayes", "P({B}) = Σ P({A}_{i})P_{A_{i}}({B}) ;  P_{B}({A}) = P_{A}({B})P({A})/P({B})", "{A}_{i} : partition de l’univers"),
  ("Espérance, variance", "E({X}) = Σ {x}_{i}{p}_{i} ;  V({X}) = E({X}^{2}) − E({X})^{2}", "écart type σ = √V"),
  ("Loi binomiale", "P({X}={k}) = C({n},{k}){p}^{k}(1−{p})^{n−k} ;  E = {np} ;  V = {np}(1−{p})", ""),
 ]),
 ("Espace, algèbre linéaire", [
  ("Produit scalaire", "!{u}·!{v} = {xx}′ + {yy}′ + {zz}′ = ‖!{u}‖‖!{v}‖ cos θ", "orthogonaux si le produit est nul"),
  ("Norme", "‖!{u}‖ = √({x}^{2} + {y}^{2} + {z}^{2})", ""),
  ("Plan", "{ax} + {by} + {cz} + {d} = 0", "(a, b, c) : vecteur normal"),
  ("Distance d’un point à un plan", "|{ax}_{0}+{by}_{0}+{cz}_{0}+{d}| / √({a}^{2}+{b}^{2}+{c}^{2})", ""),
  ("Déterminant 2 × 2", "det [[{a},{b}],[{c},{d}]] = {ad} − {bc}", "la matrice est inversible si le déterminant est non nul"),
  ("Inverse 2 × 2", "M^{−1} = (1/({ad}−{bc})) [[{d},−{b}],[−{c},{a}]]", ""),
 ]),
 ("Coniques", [
  ("Ellipse", "{x}^{2}/{a}^{2} + {y}^{2}/{b}^{2} = 1 ;  {c}^{2} = {a}^{2} − {b}^{2}", "foyers (±{c}, 0), {a} ≥ {b}"),
  ("Hyperbole", "{x}^{2}/{a}^{2} − {y}^{2}/{b}^{2} = 1 ;  {c}^{2} = {a}^{2} + {b}^{2}", "asymptotes {y} = ±({b}/{a}){x}"),
  ("Parabole", "{y}^{2} = 2{p}{x}", "foyer ({p}/2, 0), directrice {x} = −{p}/2"),
  ("Excentricité", "{e} = {c}/{a}", "< 1 ellipse, = 1 parabole, > 1 hyperbole"),
 ]),
])
CHIMIE = ("Chimie", "Atlas de chimie", "Collège · lycée · MPSI-PCSI", [
 ("Quantité de matière", [
  ("Masse", "{n} = {m} / {M}", "{n} en mol, {m} en g, {M} masse molaire en g·mol^{−1}"),
  ("Nombre d’entités", "{n} = {N} / {N}_{A}", "{N}_{A} = 6,022 × 10^{23} mol^{−1}"),
  ("Gaz", "{n} = {V} / {V}_{m}", "{V}_{m} ≈ 24 L·mol^{−1} à 20 °C et 1 atm"),
  ("Masse volumique, densité", "ρ = {m}/{V} ;  {d} = ρ / ρ_{eau}", "ρ_{eau} = 1,00 g·mL^{−1}"),
 ]),
 ("Solutions", [
  ("Concentration molaire", "{C} = {n} / {V}", "en mol·L^{−1}"),
  ("Concentration massique", "{C}_{m} = {m} / {V} = {C}{M}", "en g·L^{−1}"),
  ("Dilution", "{C}_{i}{V}_{i} = {C}_{f}{V}_{f}", "la quantité de soluté se conserve ; facteur de dilution {F} = {C}_{i}/{C}_{f}"),
  ("Fraction massique", "{w} = {m}_{soluté} / {m}_{solution}", ""),
 ]),
 ("Gaz parfaits", [
  ("Équation d’état", "{PV} = {nRT}", "{R} = 8,314 J·K^{−1}·mol^{−1} ; {P} en Pa, {V} en m^{3}, {T} en K"),
  ("Température", "{T} (K) = θ (°C) + 273,15", ""),
  ("Pression partielle (Dalton)", "{P} = Σ {P}_{i} ;  {P}_{i} = {x}_{i}{P}", "{x}_{i} : fraction molaire"),
 ]),
 ("Réaction chimique", [
  ("Tableau d’avancement", "{n}_{i} = {n}_{i,0} + ν_{i}{x}", "ν_{i} < 0 pour un réactif, > 0 pour un produit"),
  ("Réactif limitant", "{x}_{max} = min({n}_{i,0} / |ν_{i}|)", ""),
  ("Rendement", "η = {n}_{exp} / {n}_{max}", "ou {m}_{exp} / {m}_{max}"),
 ]),
 ("Acides et bases", [
  ("pH", "pH = −log [H_{3}O^{+}] ;  [H_{3}O^{+}] = 10^{−pH}", "concentration en mol·L^{−1}"),
  ("Produit ionique de l’eau", "{K}_{e} = [H_{3}O^{+}][HO^{−}] = 10^{−14}", "à 25 °C ; pH + pOH = 14"),
  ("Constante d’acidité", "{K}_{a} = [H_{3}O^{+}][A^{−}] / [HA] ;  p{K}_{a} = −log {K}_{a}", ""),
  ("Relation de Henderson", "pH = p{K}_{a} + log([A^{−}]/[HA])", "pH = p{K}_{a} quand [A^{−}] = [HA]"),
  ("Acide fort, base forte", "pH = −log {C} ;  pH = 14 + log {C}", "solutions diluées"),
  ("Acide faible", "pH = ½(p{K}_{a} − log {C})", "si l’acide est peu dissocié"),
  ("Dosage", "{C}_{A}{V}_{A} = {C}_{B}{V}_{B}", "à l’équivalence, pour une stœchiométrie 1 : 1"),
 ]),
 ("Énergie des réactions", [
  ("Quantité de chaleur", "{Q} = {mc}Δ{T}", "{c} capacité thermique massique ; eau : 4,18 J·g^{−1}·K^{−1}"),
  ("Loi de Hess", "Δ_{r}{H}° = Σ ν Δ_{f}{H}°(produits) − Σ ν Δ_{f}{H}°(réactifs)", ""),
  ("Enthalpie libre", "Δ{G} = Δ{H} − {T}Δ{S}", "réaction spontanée si Δ{G} < 0"),
  ("Constante d’équilibre", "Δ{G}° = −{RT} ln {K}", ""),
  ("Quotient de réaction", "Δ{G} = Δ{G}° + {RT} ln {Q}", ""),
 ]),
 ("Cinétique", [
  ("Vitesse de réaction", "{v} = (1/ν) d[X]/d{t}", "ν : nombre stœchiométrique en valeur absolue"),
  ("Ordre 0", "[A] = [A]_{0} − {kt} ;  {t}_{1/2} = [A]_{0} / 2{k}", ""),
  ("Ordre 1", "[A] = [A]_{0}e^{−kt} ;  {t}_{1/2} = ln 2 / {k}", "ln[A] est une droite en fonction de {t}"),
  ("Ordre 2", "1/[A] = 1/[A]_{0} + {kt}", ""),
  ("Loi d’Arrhenius", "{k} = {A}e^{−E_{a}/{RT}}", "ln {k} = ln {A} − {E}_{a}/{RT}"),
 ]),
 ("Équilibre chimique", [
  ("Constante d’équilibre", "{K} = [C]^{c}[D]^{d} / ([A]^{a}[B]^{b})", "pour {a}A + {b}B ⇌ {c}C + {d}D, concentrations à l’équilibre"),
  ("Sens d’évolution", "{Q} < {K} : sens direct ;  {Q} > {K} : sens inverse", ""),
  ("Van ’t Hoff", "d ln {K} / d{T} = Δ{H}° / ({R}{T}^{2})", "exothermique : {K} diminue quand {T} augmente"),
  ("Produit de solubilité", "{K}_{s} = [Ag^{+}][Cl^{−}]", "exemple : AgCl, {s} = √{K}_{s}"),
 ]),
 ("Oxydoréduction, piles", [
  ("Formule de Nernst", "{E} = {E}° + (0,059 / {n}) log([Ox]/[Red])", "à 25 °C ; général : {E}° + ({RT}/{nF}) ln([Ox]/[Red])"),
  ("Force électromotrice", "{E} = {E}_{cathode} − {E}_{anode}", "la cathode est le pôle +"),
  ("Enthalpie libre et potentiel", "Δ{G}° = −{nF}{E}°", "{F} = 96 485 C·mol^{−1}"),
  ("Électrolyse (Faraday)", "{m} = {M}{I}{t} / ({nF})", "{n} : électrons échangés"),
  ("Quantité d’électricité", "{Q} = {I}{t} = {n}_{e}{F}", ""),
 ]),
 ("Atome et spectroscopie", [
  ("Nombres quantiques", "{n} ≥ 1 ;  0 ≤ ℓ ≤ {n}−1 ;  −ℓ ≤ {m}_{ℓ} ≤ ℓ ;  {m}_{s} = ±½", "une couche {n} contient au plus 2{n}^{2} électrons"),
  ("Niveaux de l’hydrogène", "{E}_{n} = −13,6 eV / {n}^{2}", "1 eV = 1,602 × 10^{−19} J"),
  ("Photon", "{E} = {hν} = {hc}/λ", "{h} = 6,626 × 10^{−34} J·s ; {c} = 2,998 × 10^{8} m·s^{−1}"),
  ("Loi de Beer–Lambert", "{A} = ε ℓ {C}", "{A} = log({I}_{0}/{I}) ; ℓ : épaisseur de la cuve"),
 ]),
])
COMPL = ("Compléments", "Physique, compléments", "Leviers · ondes · lumière · atome", [
 ("Leviers et poulies", [
  ("Moment d’une force", "ℳ = {F} × {d}", "{d} : distance de l’axe à la ligne d’action de la force (N·m)"),
  ("Équilibre d’un levier", "{F}_{1}{l}_{1} = {F}_{2}{l}_{2}", "la balance romaine (杆秤) en est une application"),
  ("Avantage mécanique", "AM = {F}_{charge} / {F}_{effort} = {l}_{effort} / {l}_{charge}", ""),
  ("Palan idéal", "{F} = {P} / {n}", "{n} brins portant la charge ; la corde se déplace {n} fois plus"),
  ("Travail, puissance", "{W} = {F}{s} ;  {P} = {W} / {t}", ""),
  ("Rendement", "η = {W}_{utile} / {W}_{moteur} × 100 %", ""),
 ]),
 ("Ondes", [
  ("Célérité", "{v} = λ{f} = λ / {T}", "{f} = 1/{T}"),
  ("Interférences", "Δ = {k}λ (constructives) ;  Δ = ({k}+½)λ (destructives)", "Δ : différence de marche"),
  ("Corde vibrante", "{v} = √({F}/μ) ;  {L} = {n}λ/2", "ondes stationnaires, {n} entier"),
  ("Effet Doppler", "{f}′ = {f} {v} / ({v} − {v}_{s})", "source qui s’approche ; observateur qui s’approche : {f}′ = {f}({v}+{v}_{o})/{v}"),
  ("Niveau sonore", "{L} = 10 log({I}/{I}_{0})", "{I}_{0} = 10^{−12} W·m^{−2}, en décibels"),
 ]),
 ("Lumière", [
  ("Indice de réfraction", "{n} = {c} / {v}", "{c} = 3,00 × 10^{8} m·s^{−1}"),
  ("Loi de Snell–Descartes", "{n}_{1} sin θ_{1} = {n}_{2} sin θ_{2}", ""),
  ("Réflexion totale", "sin θ_{c} = {n}_{2} / {n}_{1}", "{n}_{1} > {n}_{2} ; principe de la fibre optique"),
  ("Lentille mince", "1/{f} = 1/{p} + 1/{p}′ ;  γ = −{p}′/{p}", "{p}, {p}′ : distances objet et image, positives pour un objet et une image réels"),
  ("Fentes d’Young", "{i} = λ{D} / {a}", "interfrange ; {a} : écart des fentes, {D} : distance à l’écran"),
  ("Réseau", "{d} sin θ = {k}λ", ""),
 ]),
 ("Force de Lorentz", [
  ("Force magnétique", "{F} = {qvB} sin θ", "θ : angle entre !{v} et !{B}"),
  ("Mouvement circulaire", "{r} = {mv} / ({qB}) ;  {T} = 2π{m} / ({qB})", "la période ne dépend pas de la vitesse"),
  ("Hélice", "pas = {v}_{∥}{T}", ""),
  ("Sélecteur de vitesse", "{v} = {E} / {B}", "force électrique = force magnétique"),
  ("Spectromètre de masse", "{r} = (1/{B}) √(2{mU}/{q})", ""),
  ("Cyclotron", "{E}_{c,max} = {q}^{2}{B}^{2}{R}^{2} / (2{m})", ""),
  ("Force de Laplace", "{F} = {BIL} sin θ", "conducteur de longueur {L}"),
 ]),
 ("Courant alternatif", [
  ("Tension sinusoïdale", "{u}({t}) = {U}_{m} cos(ω{t}) ;  ω = 2π{f}", ""),
  ("Valeur efficace", "{U}_{eff} = {U}_{m} / √2", "220 V efficaces ↔ {U}_{m} ≈ 311 V"),
  ("Force électromotrice", "{e} = −{N} Δ Φ / Δ{t} ;  {e}_{m} = {NBS}ω", "alternateur : bobine de {N} spires tournant dans un champ"),
  ("Transformateur idéal", "{U}_{2} / {U}_{1} = {N}_{2} / {N}_{1} = {I}_{1} / {I}_{2}", ""),
  ("Transport de l’énergie", "{I} = {P} / {U} ;  {P}_{perdue} = {R}{I}^{2}", "haute tension : moins de pertes en ligne"),
  ("Réactances", "{X}_{L} = ω{L} ;  {X}_{C} = 1 / (ω{C})", "résonance : {f}_{0} = 1 / (2π√({LC}))"),
 ]),
 ("Gaz et thermodynamique", [
  ("Gaz parfait", "{PV} = {nRT}", "{R} = 8,314 J·K^{−1}·mol^{−1}"),
  ("Transformations", "{P}_{1}{V}_{1} = {P}_{2}{V}_{2} (T const.) ;  {V}/{T} const. ({P} const.)", "{P}/{T} const. ({V} const.)"),
  ("Énergie cinétique moyenne", "⟨{E}_{c}⟩ = (3/2) {k}_{B}{T}", "{k}_{B} = 1,381 × 10^{−23} J·K^{−1}"),
  ("Vitesse quadratique", "{v}_{rms} = √(3{RT}/{M})", ""),
  ("Premier principe", "ΔU = {Q} + {W}", "{W} = −{P}Δ{V} à pression constante"),
  ("Rendement de Carnot", "η = 1 − {T}_{f} / {T}_{c}", "températures en kelvins"),
 ]),
 ("Atome et noyau", [
  ("Énergie d’un photon", "{E} = {hf} = {hc}/λ", "{h} = 6,626 × 10^{−34} J·s"),
  ("Effet photoélectrique", "{hf} = {W}_{0} + {E}_{c,max}", "{E}_{c,max} = {eU}_{a} (tension d’arrêt)"),
  ("Longueur d’onde de de Broglie", "λ = {h} / {p}", ""),
  ("Niveaux de Bohr", "{E}_{n} = −13,6 eV / {n}^{2} ;  {hf} = {E}_{m} − {E}_{n}", ""),
  ("Décroissance radioactive", "{N} = {N}_{0}e^{−λ{t}} = {N}_{0}(½)^{t/T} ;  λ = ln 2 / {T}", "activité {A} = λ{N}"),
  ("Datation au carbone 14", "{t} = ({T}/ln 2) ln({N}_{0}/{N})", "{T} ≈ 5 730 ans"),
  ("Énergie de masse", "{E} = Δ{m}{c}^{2}", "fission et fusion : défaut de masse"),
 ]),
])

MATHS[3].extend([
 ("Sommes et équivalents", [
  ("Sommes classiques", "Σ_{k=1}^{n} {k} = {n}({n}+1)/2 ;  Σ {k}^{2} = {n}({n}+1)(2{n}+1)/6 ;  Σ {k}^{3} = [{n}({n}+1)/2]^{2}", ""),
  ("Équivalents usuels en 0", "sin {x} ~ {x} ;  tan {x} ~ {x} ;  e^{x} − 1 ~ {x} ;  ln(1+{x}) ~ {x} ;  1 − cos {x} ~ {x}^{2}/2 ;  (1+{x})^{α} − 1 ~ α{x}", ""),
  ("Limites usuelles", "sin {x}/{x} → 1 ;  (e^{x}−1)/{x} → 1 ;  ln(1+{x})/{x} → 1", "quand {x} → 0"),
  ("Formule de Stirling", "{n}! ~ √(2π{n}) ({n}/e)^{n}", "quand {n} → +∞"),
  ("Inégalités classiques", "e^{x} ≥ 1 + {x} ;  ln(1+{x}) ≤ {x} ;  |sin {x}| ≤ |{x}|", "convexité et concavité"),
  ("Cauchy–Schwarz", "|⟨{u}, {v}⟩| ≤ ‖{u}‖ ‖{v}‖ ;  Σ {a}_{i}{b}_{i} ≤ √(Σ{a}_{i}^{2}) √(Σ{b}_{i}^{2})", "égalité si les vecteurs sont colinéaires"),
  ("Inégalité triangulaire", "|{a}+{b}| ≤ |{a}| + |{b}| ;  ||{a}|−|{b}|| ≤ |{a}−{b}|", ""),
 ]),
 ("Analyse (prépa)", [
  ("Taylor–Young", "{f}({a}+{h}) = Σ_{k=0}^{n} {f}^{(k)}({a}) {h}^{k}/{k}! + o({h}^{n})", ""),
  ("Taylor avec reste intégral", "{f}({b}) = Σ_{k=0}^{n} {f}^{(k)}({a})({b}−{a})^{k}/{k}! + ∫_{a}^{b} ({b}−{t})^{n}/{n}! {f}^{(n+1)}({t}) d{t}", "{f} de classe C^{n+1}"),
  ("Inégalité de Taylor–Lagrange", "|{f}({b}) − Σ_{k=0}^{n} {f}^{(k)}({a})({b}−{a})^{k}/{k}!| ≤ {M}|{b}−{a}|^{n+1}/({n}+1)!", "{M} = sup|{f}^{(n+1)}|"),
  ("Accroissements finis", "{f}({b}) − {f}({a}) = {f}′({c})({b}−{a})", "pour un {c} dans ]{a}, {b}["),
  ("Fonctions hyperboliques", "ch {x} = (e^{x}+e^{−x})/2 ;  sh {x} = (e^{x}−e^{−x})/2 ;  ch^{2}{x} − sh^{2}{x} = 1", "(sh)′ = ch ; (ch)′ = sh"),
  ("Fonctions réciproques", "(arcsin)′ = 1/√(1−{x}^{2}) ;  (arccos)′ = −1/√(1−{x}^{2}) ;  (arctan)′ = 1/(1+{x}^{2})", "arcsin et arccos sur ]−1, 1[ ; arctan sur ℝ"),
  ("Dérivée d’une réciproque", "({f}^{−1})′ = 1 / ({f}′∘{f}^{−1})", "si {f}′ ne s’annule pas"),
  ("Primitives supplémentaires", "∫ d{x}/(1+{x}^{2}) = arctan {x} ;  ∫ d{x}/√(1−{x}^{2}) = arcsin {x} ;  ∫ tan {x} d{x} = −ln|cos {x}|", ""),
  ("Changement de variable", "∫_{a}^{b} {f}({φ}({t})){φ}′({t}) d{t} = ∫_{φ(a)}^{φ(b)} {f}({x}) d{x}", "{φ} de classe C¹"),
  ("Intégrales de Wallis", "W_{n} = ∫_{0}^{π/2} sin^{n}{t} d{t} ;  W_{n+2} = ({n}+1)/({n}+2) W_{n}", "W_{0} = π/2, W_{1} = 1"),
  ("Intégrale de Gauss", "∫_{−∞}^{+∞} e^{−{x}^{2}} d{x} = √π", ""),
 ]),
 ("Séries, équations différentielles", [
  ("Séries de référence", "Σ 1/{n}^{α} converge ⟺ α > 1 ;  Σ {q}^{n} converge ⟺ |{q}| < 1", "séries de Riemann et séries géométriques"),
  ("Somme de Bâle", "Σ_{n=1}^{∞} 1/{n}^{2} = π^{2}/6", ""),
  ("Critère de d’Alembert", "{u}_{n+1}/{u}_{n} → ℓ :  ℓ < 1 converge, ℓ > 1 diverge", "termes {u}_{n} > 0"),
  ("Séries entières usuelles", "e^{x} = Σ {x}^{n}/{n}! ;  1/(1−{x}) = Σ {x}^{n} ;  ln(1+{x}) = Σ (−1)^{n+1}{x}^{n}/{n}", "rayons de convergence respectifs : ∞, 1, 1"),
  ("Équation linéaire d’ordre 1", "{y}′ + {a}{y} = {b} :  {y} = {λ}e^{−ax} + {b}/{a}", "{a} et {b} constants, {a} ≠ 0"),
  ("Équation d’ordre 2 à coefficients constants", "{y}″ + {ay}′ + {by} = 0 ;  {r}^{2} + {ar} + {b} = 0", "Δ > 0 : {λ}e^{r_{1}x} + {μ}e^{r_{2}x} ; Δ = 0 : ({λ}+{μ}{x})e^{rx} ; Δ < 0 : e^{αx}({λ}cos β{x} + {μ}sin β{x})"),
  ("Oscillateur harmonique", "{y}″ + ω^{2}{y} = 0 :  {y} = {A}cos(ω{x}) + {B}sin(ω{x})", ""),
 ]),
 ("Algèbre linéaire, polynômes (prépa)", [
  ("Théorème du rang", "dim {E} = dim Ker {u} + dim Im {u}", "{E} de dimension finie, {u} linéaire"),
  ("Formule de Grassmann", "dim({F}+{G}) = dim {F} + dim {G} − dim({F}∩{G})", ""),
  ("Déterminant", "det({AB}) = det {A} det {B} ;  det({A}^{T}) = det {A}", "{A} est inversible si et seulement si det {A} ≠ 0"),
  ("Polynôme caractéristique", "χ_{A}({λ}) = det({λ}{I} − {A})", "valeurs propres = racines"),
  ("Trace et déterminant", "tr {A} = Σ {λ}_{i} ;  det {A} = Π {λ}_{i}", "valeurs propres comptées avec multiplicité"),
  ("Cayley–Hamilton", "χ_{A}({A}) = 0", ""),
  ("Relations de Viète", "Σ {x}_{i} = −{a}_{n−1}/{a}_{n} ;  Π {x}_{i} = (−1)^{n}{a}_{0}/{a}_{n}", "racines d’un polynôme de degré {n}"),
  ("Projection orthogonale sur une droite", "proj_{u}({v}) = ⟨{u},{v}⟩/‖{u}‖^{2} {u}", ""),
  ("Produit vectoriel", "‖!{u}∧!{v}‖ = ‖!{u}‖‖!{v}‖ sin θ", "aire du parallélogramme construit sur !{u} et !{v}"),
 ]),
 ("Probabilités (prépa)", [
  ("Loi de Poisson", "P({X}={k}) = e^{−λ} λ^{k} / {k}! ;  E({X}) = V({X}) = λ", ""),
  ("Loi géométrique", "P({X}={k}) = {p}(1−{p})^{k−1} ;  E = 1/{p} ;  V = (1−{p})/{p}^{2}", "{k} ≥ 1"),
  ("Loi uniforme sur ⟦1, n⟧", "E = ({n}+1)/2 ;  V = ({n}^{2}−1)/12", ""),
  ("Covariance", "Cov({X},{Y}) = E({XY}) − E({X})E({Y}) ;  V({X}+{Y}) = V({X}) + V({Y}) + 2 Cov({X},{Y})", "indépendantes ⇒ covariance nulle"),
  ("Inégalité de Markov", "P({X} ≥ {a}) ≤ E({X}) / {a}", "{X} ≥ 0 et {a} > 0"),
  ("Bienaymé–Tchebychev", "P(|{X} − E({X})| ≥ ε) ≤ V({X}) / ε^{2}", ""),
  ("Probabilités composées", "P({A}_{1}∩…∩{A}_{n}) = P({A}_{1}) P_{A_{1}}({A}_{2}) … P_{A_{1}∩…∩A_{n−1}}({A}_{n})", ""),
 ]),
 ("Nombres complexes (prépa)", [
  ("Formules d’Euler", "cos θ = (e^{iθ}+e^{−iθ})/2 ;  sin θ = (e^{iθ}−e^{−iθ})/(2i)", "pour linéariser"),
  ("Racines {n}-ièmes d’un complexe", "{z}^{n} = {r}e^{iθ} ⟹ {z}_{k} = {r}^{1/n}e^{i(θ+2kπ)/n}", "{k} = 0, …, {n}−1 ; leur somme est nulle"),
  ("Factorisation trigonométrique", "cos {p} + cos {q} = 2 cos(({p}+{q})/2) cos(({p}−{q})/2)", "sin {p} + sin {q} = 2 sin(({p}+{q})/2) cos(({p}−{q})/2)"),
  ("Transformations du plan", "{z}′ = {az} + {b}", "{a} = 1 : translation ; |{a}| = 1 : rotation ; {a} réel ≠ 1 : homothétie"),
  ("Inégalité triangulaire", "|{z}+{w}| ≤ |{z}| + |{w}|", "égalité si les arguments sont égaux"),
 ]),
 ("Arithmétique", [
  ("Bézout", "{a}∧{b} = {d} ⟹ il existe {u}, {v} entiers : {au} + {bv} = {d}", ""),
  ("Petit théorème de Fermat", "{a}^{p} ≡ {a} [{p}]", "{p} premier ; si {p} ne divise pas {a} : {a}^{p−1} ≡ 1 [{p}]"),
  ("Indicatrice d’Euler", "φ({n}) = {n} Π (1 − 1/{p})", "produit sur les diviseurs premiers {p} de {n}"),
 ]),
])
CHIMIE[3].extend([
 ("Thermodynamique chimique (prépa)", [
  ("Potentiel chimique, activité", "μ_{i} = μ_{i}° + {RT} ln {a}_{i}", "gaz parfait : {a}_{i} = {P}_{i}/{P}° ; soluté : {a}_{i} = [i]/{C}° ; solide et solvant : {a}_{i} = 1"),
  ("Enthalpie libre de réaction", "Δ_{r}{G} = Δ_{r}{G}° + {RT} ln {Q}_{r} ;  Δ_{r}{G}° = −{RT} ln {K}°", "à l’équilibre : Δ_{r}{G} = 0 et {Q}_{r} = {K}°"),
  ("Évolution d’un système", "{Q}_{r} < {K}° : sens direct ;  {Q}_{r} > {K}° : sens inverse", ""),
  ("Gibbs–Helmholtz, Ellingham", "Δ_{r}{G}° = Δ_{r}{H}° − {T}Δ_{r}{S}°", "approximation d’Ellingham : Δ_{r}{H}° et Δ_{r}{S}° indépendants de {T}"),
  ("Loi de Kirchhoff", "Δ_{r}{H}°({T}_{2}) = Δ_{r}{H}°({T}_{1}) + ∫_{T_{1}}^{T_{2}} Δ_{r}{C}_{p}° d{T}", ""),
  ("Loi de Van’t Hoff", "d ln {K}° / d{T} = Δ_{r}{H}° / ({R}{T}^{2})", "intégrée : ln({K}_{2}/{K}_{1}) = −(Δ_{r}{H}°/{R})(1/{T}_{2} − 1/{T}_{1})"),
  ("Variance (règle des phases)", "{v} = {N} − {r} − {k} + 2 − φ", "{N} constituants, {r} équilibres, {k} relations supplémentaires, φ phases"),
  ("Lois de Raoult et de Henry", "{P}_{i} = {x}_{i}{P}_{i}^{*} ;  {P}_{i} = {k}_{H}{x}_{i}", "mélange idéal ; soluté dilué"),
  ("Théorème des moments chimiques", "{n}_{liq} × ML = {n}_{vap} × MV", "point M dans le fuseau d’un diagramme binaire, L et V sur l’horizontale passant par M"),
 ]),
 ("Solutions aqueuses (prépa)", [
  ("Condition de précipitation", "précipite si {Q} = Π [i]^{ν_{i}} > {K}_{s}", "début de précipitation : {Q} = {K}_{s}"),
  ("Complexation", "{β}_{n} = [ML_{n}] / ([M][L]^{n})", "constante globale de formation de M + {n}L ⇌ ML_{n}"),
  ("Domaines de prédominance", "pH > p{K}_{a} : base prédominante ;  pH < p{K}_{a} : acide prédominant", ""),
  ("Demi-équivalence d’un dosage", "pH = p{K}_{a}", "acide faible dosé par une base forte"),
  ("Conductivité de la solution", "σ = Σ λ_{i}[X_{i}]", "λ_{i} : conductivité molaire ionique ; σ en S·m^{−1}"),
  ("Force ionique", "{I} = ½ Σ {c}_{i}{z}_{i}^{2}", "{z}_{i} : charge de l’ion {i}"),
  ("Constante d’équilibre d’une réaction redox", "log {K}° = {n}({E}°_{1} − {E}°_{2}) / 0,059", "25 °C ; l’oxydant du couple 1 réagit avec le réducteur du couple 2"),
  ("Charge d’une pile", "{Q} = {n}{F} ;  {Q} = {I}{t}", "{Q} en coulombs"),
 ]),
 ("Cinétique (prépa)", [
  ("Loi de vitesse", "{v} = {k}[A]^{α}[B]^{β}", "ordres partiels α et β ; ordre global α + β"),
  ("Temps de demi-réaction", "ordre 0 : [A]_{0}/2{k} ;  ordre 1 : ln 2/{k} ;  ordre 2 : 1/({k}[A]_{0})", ""),
  ("Quasi-stationnarité", "d[I]/d{t} ≈ 0", "AEQS : intermédiaire réactionnel très réactif"),
  ("Énergie d’activation", "ln({k}_{2}/{k}_{1}) = −({E}_{a}/{R})(1/{T}_{2} − 1/{T}_{1})", ""),
  ("Substitution et élimination", "SN1 et E1 : {v} = {k}[RX] ;  SN2 et E2 : {v} = {k}[RX][Nu]", "Nu : nucléophile ou base"),
  ("Stéréoisomères", "au plus 2^{n} stéréoisomères", "pour {n} centres stéréogènes ; moins en présence de symétrie (composés méso)"),
 ]),
 ("Cristallographie", [
  ("Compacité", "{C} = {Z} × (4/3)π{R}^{3} / {a}^{3}", "{Z} atomes par maille cubique de côté {a}"),
  ("Masse volumique", "ρ = {Z}{M} / ({N}_{A}{a}^{3})", ""),
  ("Cubique à faces centrées", "{Z} = 4 ;  {a}√2 = 4{R} ;  {C} = π√2/6 ≈ 0,74", "contact le long de la diagonale d’une face ; coordinence 12"),
  ("Cubique centré", "{Z} = 2 ;  {a}√3 = 4{R} ;  {C} = π√3/8 ≈ 0,68", "contact le long de la grande diagonale ; coordinence 8"),
  ("Cubique simple", "{Z} = 1 ;  {a} = 2{R} ;  {C} = π/6 ≈ 0,52", "coordinence 6"),
  ("Sites interstitiels (CFC)", "octaédriques : 4 par maille, {r}/{R} ≤ √2 − 1 ≈ 0,414 ;  tétraédriques : 8 par maille, {r}/{R} ≤ √(3/2) − 1 ≈ 0,225", ""),
 ]),
 ("Structure de la matière (prépa)", [
  ("Remplissage des orbitales", "Klechkowski : {n}+ℓ croissant, puis {n} croissant ;  Pauli ;  Hund", ""),
  ("Moment dipolaire", "μ = δ × {d}", "δ : charge partielle, {d} : longueur de liaison ; 1 D = 3,336 × 10^{−30} C·m"),
  ("Géométrie (VSEPR)", "AX_{n}E_{m} :  {n}+{m} = 2 linéaire ; 3 trigonale plane ; 4 tétraédrique", "angles 180°, 120°, 109,5°"),
  ("Charge formelle", "CF = {N}_{valence} − {N}_{non liants} − ½{N}_{liants}", ""),
  ("Nombre d’onde (IR)", "σ = 1/λ", "en cm^{−1}"),
  ("RMN du proton", "{n} + 1 pics pour {n} protons voisins équivalents", "déplacement chimique δ = 10^{6}(ν − ν_{réf})/ν_{réf}, en ppm"),
 ]),
])

CSS = """
  html { scroll-padding-top: 76px; }
  body { min-height: 100vh; padding: 0 16px 80px; }
  header { max-width: 1120px; margin: 0 auto; padding: 22px 12px; display: flex; justify-content: space-between; gap: 12px; font: 500 12px var(--mono); letter-spacing: .06em; color: var(--muted); text-transform: uppercase; }
  header a { font: 500 19px var(--serif); letter-spacing: 0; text-transform: none; color: var(--strong); text-decoration: none; }
  header span { padding-top: 5px; margin-left: auto; text-align: right; }
  .hero { text-align: center; margin: 48px auto 36px; max-width: 760px; }
  .hero h1 { font: 400 clamp(42px, 7vw, 76px)/1 var(--serif); color: var(--strong); letter-spacing: -.015em; }
  .hero p { font: italic 400 clamp(19px, 2.2vw, 24px)/1.4 var(--serif); color: var(--muted); margin-top: 14px; }
  nav { position: sticky; top: 0; z-index: 2; margin: 0 -16px; padding: 10px 16px; background: color-mix(in srgb, var(--page) 92%, transparent); backdrop-filter: blur(8px); border-bottom: 1px solid var(--faint); }
  nav .in { max-width: 1120px; margin: 0 auto; display: flex; align-items: center; gap: 6px 20px; flex-wrap: wrap; }
  nav a { font: 500 12px var(--mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); text-decoration: none; padding: 8px 0; }
  nav a:hover { color: var(--strong); }
  nav input { margin-left: auto; width: min(100%, 260px); font: 14px var(--sans); color: var(--strong); background: var(--card); border: 1px solid var(--faint); border-radius: 999px; padding: 8px 14px; }
  nav input:focus { outline: none; border-color: var(--mid); }
  main { max-width: 1120px; margin: 0 auto; }
  .group { background: var(--card); border-radius: 14px; box-shadow: var(--lift); padding: 18px 22px 8px; margin-top: 22px; }
  .group h2 { font: 400 clamp(26px, 3.4vw, 34px)/1.1 var(--serif); color: var(--strong); padding-bottom: 8px; }
  ul { list-style: none; padding: 0; }
  li { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.4fr); gap: 4px 24px; align-items: baseline; padding: 11px 0; border-top: 1px solid var(--faint); }
  .n { font-size: 14px; color: var(--text); } .n small { display: block; font-size: 12.5px; color: var(--muted); margin-top: 2px; }
  .e { font: 400 20px/1.4 var(--serif); color: var(--strong); overflow-x: auto; overflow-y: hidden; padding-left: 14px; border-left: 1px solid var(--mid); }
  .e sub, .e sup, .n sub, .n sup, small sub, small sup { font-size: .68em; line-height: 0; }
  small i, .n i { font-family: var(--serif); font-size: 1.1em; color: var(--hi); }
  .vec { position: relative; display: inline-block; }
  .vec::before { content: '→'; position: absolute; left: 50%; transform: translateX(-50%); top: -.42em; font-size: .7em; font-style: normal; line-height: 1; }
  li[hidden], .group[hidden] { display: none; }
  .empty { text-align: center; color: var(--muted); padding: 40px 0; }
  @media (max-width: 700px) { li { grid-template-columns: 1fr; } header span { display: none; } }
"""
def page(slug, data, back_label, back_href, repo=False):
    short, brand, sub, groups = data
    FONTS = ('<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">' if repo
             else '<link href="/vendor/fonts/fonts.css" rel="stylesheet">')
    ATLASCSS = "../atlas.css" if repo else "/atlas.css"
    HOME = "" if repo else '<span><a href="/" style="font:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit">Accueil</a></span>'
    nav = "".join(f'<a href="#g{i}">{html.escape(g)}</a>' for i, (g, _) in enumerate(groups))
    body = ""
    for i, (g, rows) in enumerate(groups):
        lis = "".join(f'<li><div class="n">{md(html.escape(n, quote=False))}' + (f'<small>{md(html.escape(c, quote=False))}</small>' if c else "") + f'</div><div class="e">{md(html.escape(e, quote=False))}</div></li>' for n, e, c in rows)
        body += f'<section class="group" id="g{i}"><h2>{html.escape(g)}</h2><ul>{lis}</ul></section>\n'
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Feuille d’équations · {html.escape(brand)}</title>
<link rel="icon" href="data:,">
{FONTS}
<link rel="stylesheet" href="{ATLASCSS}">
<!-- Généré par make-equations.py (VPS) : modifier les données dans ce script puis le relancer. -->
<style>{CSS}</style>
</head>
<body>
<header><a href="{back_href}">{html.escape(brand)}</a>{HOME}</header>
<section class="hero"><h1>Feuille d’équations</h1><p>{html.escape(sub)}. Les formules du programme, sans démonstration.</p></section>
<nav><div class="in">{nav}<input type="search" id="q" placeholder="Rechercher une formule" aria-label="Rechercher une formule"></div></nav>
<main>
{body}<p class="empty" id="none" hidden>Aucune formule ne correspond.</p>
</main>
<script>
(function () {{
  var q = document.getElementById('q'), none = document.getElementById('none');
  q.addEventListener('input', function () {{
    var t = q.value.trim().toLowerCase(), any = false;
    document.querySelectorAll('.group').forEach(function (g) {{
      var shown = 0;
      g.querySelectorAll('li').forEach(function (li) {{ var ok = !t || li.textContent.toLowerCase().indexOf(t) >= 0; li.hidden = !ok; if (ok) shown++; }});
      g.hidden = !shown; if (shown) any = true;
    }});
    none.hidden = any;
  }});
}})();
</script>
</body>
</html>
"""
def repo_sheet(slug):
    """version « dépôt GitHub » : chemins relatifs, polices Google, sans lien vers l'accueil du VPS"""
    data = {"maths": MATHS, "chimie": CHIMIE, "complements": COMPL}[slug]
    return page_compl(repo=True) if slug == "complements" else page(slug, data, "", "../", repo=True)

# ---------- feuille des compléments : même mise en page que la feuille de l'atlas de physique d'origine, avec des puces vers les pages ----------
COMPL_CH = {"Leviers et poulies": "leviers", "Ondes": "ondes", "Lumière": "lumiere", "Force de Lorentz": "lorentz",
            "Courant alternatif": "alternatif", "Gaz et thermodynamique": "gaz", "Atome et noyau": "noyau"}
COMPL_PAGES = {  # nom de la ligne -> numéros de pages du chapitre (0 = ouverture du chapitre) ; absent = pas encore dessiné
 "Moment d’une force": [0], "Équilibre d’un levier": [0, 1], "Avantage mécanique": [1], "Palan idéal": [3], "Rendement": [4],
 "Célérité": [0, 1], "Interférences": [2], "Effet Doppler": [3],
 "Indice de réfraction": [0], "Loi de Snell–Descartes": [0], "Réflexion totale": [1], "Lentille mince": [2], "Fentes d’Young": [3],
 "Force magnétique": [0], "Mouvement circulaire": [0, 1], "Hélice": [2], "Spectromètre de masse": [3], "Cyclotron": [4],
 "Tension sinusoïdale": [0], "Valeur efficace": [1], "Force électromotrice": [0], "Transformateur idéal": [2], "Transport de l’énergie": [3],
 "Gaz parfait": [0], "Transformations": [1, 2], "Énergie cinétique moyenne": [0], "Vitesse quadratique": [0], "Premier principe": [3],
 "Énergie d’un photon": [0], "Effet photoélectrique": [0], "Niveaux de Bohr": [2], "Décroissance radioactive": [3], "Datation au carbone 14": [3], "Énergie de masse": [4],
}
def _titles(ch):
    import re as _re
    src = open(SITE + "complements/" + ch + "/pages.js", encoding="utf8").read()
    out = []
    for k, t in _re.findall(r"kicker:\s*'([^']*)',\s*title:\s*'([^']*)'", src):
        out.append(("Ch. " + k.split(" ")[1] if k.startswith("Chapitre") else k.split(" ")[0], t))
    return out
def page_compl(repo=False):
    short, brand, sub, groups = COMPL
    up = open(os.path.expanduser("~/atlas-upstream/equations/index.html"), encoding="utf8").read()
    style = up[up.index("<style>"):up.index("</style>") + 8]
    style = style.replace("</style>", "  .n small { display: block; font-size: 12.5px; color: var(--muted); margin-top: 2px; }\n  .n small i, .n i { font-family: var(--serif); color: var(--hi); }\n</style>")
    FONTS = ('<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">' if repo else '<link href="/vendor/fonts/fonts.css" rel="stylesheet">')
    ATLASCSS = "../atlas.css" if repo else "/atlas.css"
    titles = {ch: _titles(ch) for ch in COMPL_CH.values()}
    nav = "".join(f'<a href="#{COMPL_CH[g]}">{html.escape(g)}</a>' for g, _ in groups)
    body = ""
    for g, rows in groups:
        ch = COMPL_CH[g]; lis = ""
        for n, e, c in rows:
            pg = COMPL_PAGES.get(n)
            chips = ('<span class="chips">' + "".join(f'<a href="../{ch}/#{i}">{html.escape(titles[ch][i][0])} {html.escape(titles[ch][i][1])}</a>' for i in pg if i < len(titles[ch])) + "</span>") if pg else '<span class="chips"><span class="none">pas encore dessiné</span></span>'
            cls = "" if pg else ' class="unshown"'
            note = f"<small>{md(html.escape(c, quote=False))}</small>" if c else ""
            lis += f'<li{cls}><div class="e">{md(html.escape(e, quote=False))}</div><div class="m"><span class="n">{md(html.escape(n, quote=False))}{note}</span>{chips}</div></li>\n          '
        body += f'<section class="sheet" id="{ch}">\n      <div class="shead"><h2>{html.escape(g)}</h2><span>chapitre {list(COMPL_CH.values()).index(ch) + 1}</span></div>\n      <div class="group"><ul>\n          {lis}</ul></div>\n    </section>\n    '
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Feuille d’équations · {html.escape(brand)}</title>
<link rel="icon" href="data:,">
{FONTS}
<link rel="stylesheet" href="{ATLASCSS}">
<!-- Généré par make-equations.py (VPS), mise en page de l'atlas de physique d'origine : modifier les données dans ce script puis le relancer. -->
{style}
</head>
<body>
  <header><a href="../">{html.escape(brand)}</a><span>Les formules, liées aux pages</span></header>
  <section class="hero">
    <h1>Feuille d’équations</h1>
    <p>Les formules des sept chapitres de compléments. Chacune renvoie vers les pages de l’atlas qui la montrent ou l’utilisent.</p>
  </section>
  <nav aria-label="Chapitres"><div class="in">
    {nav}
    <input type="search" id="q" placeholder="Filtrer : moment, Lorentz, Snell…" aria-label="Filtrer les équations" autocomplete="off">
  </div></nav>
  <main>
    {body}<p class="empty" id="empty">Aucune équation ne correspond.</p>
  </main>
  <footer>Formules du programme de physique (manuels 人教版 et programmes français), regroupées par chapitre de l’atlas. Les noms à côté de chaque équation sont ceux de l’atlas. Les puces donnent le numéro et le titre de la page ; les lignes en gris ne sont pas encore dessinées dans l’atlas.</footer>
<script>
  const q = document.getElementById('q'), norm = s => s.normalize('NFKD').toLowerCase();
  const items = [...document.querySelectorAll('.group li')].map(el => [el, norm(el.textContent)]);
  q.addEventListener('input', () => {{
    const t = norm(q.value.trim());
    for (const [el, txt] of items) el.classList.toggle('hidden', !!t && !txt.includes(t));
    for (const g of document.querySelectorAll('.group')) g.classList.toggle('hidden', !!t && !g.querySelector('li:not(.hidden)'));
    for (const s of document.querySelectorAll('.sheet')) s.classList.toggle('hidden', !!t && !s.querySelector('.group:not(.hidden)'));
    document.getElementById('empty').style.display = t && !document.querySelector('.sheet:not(.hidden)') ? 'block' : 'none';
  }});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    for slug, data, back in (("maths", MATHS, "../"), ("chimie", CHIMIE, "../"), ("complements", COMPL, "../")):
        d = SITE + slug + "/equations/"; os.makedirs(d, exist_ok=True)
        open(d + "index.html", "w", encoding="utf8").write(page_compl() if slug == "complements" else page(slug, data, "", back))
        print(slug, sum(len(r) for _, r in data[3]), "formules")
