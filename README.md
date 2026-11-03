# Détecteur de collision et de proximité VR en 3D

## Présentation

Ce projet simule un point `controller` dans un espace tridimensionnel et détecte sa relation avec des cubes et des boîtes rectangulaires, y compris des boîtes tournées.

Il fonctionne dans le terminal. Aucun casque VR ni bibliothèque externe n'est nécessaire.

Ce projet est personnel : au départ de ces vacances, j'ai préparé un jeu en VR pour un événement communautaire. Le suivi de mes manettes a fait défaut et, en fin de soirée, je n'ai pas pu jouer en réalité virtuelle, mais simplement sur ordinateur. Le lendemain, j'ai décidé que cela serait mon projet Python, dû au fait qu'il m'a causé un grand trauma (exagération).

La nature du projet étant plutôt compliquée, j'ai créé un programme qui regarde simplement si un point (la manette dans ce contexte) est en contact avec un objet, s'il est proche avec une certaine tolérance donnée ou s'il est suffisamment éloigné. Quelques tests sont préprogrammés, avec un environnement préfait, quelques exemples de tests dans ce Markdown et un affichage pour faire ces propres tests.

L'intelligence artificielle a été utilisée dans l'orientation du projet (ce qui est pertinent et ce qui ne l'est pas, suggestions, conseille mineur), la vérification du code (intégration mineure de code réparé/correction) et quelques réexplications sur certaines notions comme les matrices.

## Sujet

**Comment les transformations matricielles et la précision des nombres flottants influencent-elles la fiabilité d'un détecteur de collision et de proximité dans un espace 3D ?**

## Notions mathématiques étudiées

### Nombres flottants et calcul numérique
- Coordonnées, dimensions, angles et distances sont stockés en `float`.
- Les calculs de distance impliquent des additions, multiplications et racines carrées.
- Les expériences testent les valeurs proches d'une limite et le rôle d'une tolérance numérique.

### Matrices et transformations linéaires
- Les matrices de rotation représentent l'orientation d'une boîte.
- Une matrice homogène 4×4 combine rotation et translation.
- L'inverse transforme les coordonnées mondiales en coordonnées locales.
- L'inversion est implémentée par élimination de Gauss-Jordan.

## Modèle géométrique

Une boîte est définie par son centre, ses dimensions et ses angles de rotation. Le point du contrôleur est transformé dans le repère local de la boîte, puis on calcule la distance minimale à la boîte alignée sur les axes.

Pour les demi-dimensions `hx`, `hy`, `hz` et le point local `(x, y, z)` :


dx = max(abs(x) - hx, 0)
dy = max(abs(y) - hy, 0)
dz = max(abs(z) - hz, 0)
distance = sqrt(dx*dx + dy*dy + dz*dz)


La classification est :
- `COLLISION` si la distance est considérée nulle selon la tolérance choisie ;
- `PROXIMITÉ` si la distance est positive et inférieure ou égale à la marge ;
- `SÛR` au-delà de la marge.

Le modèle traite le contrôleur comme un point sans rayon. Il ne s'agit pas d'un système certifié de sécurité physique.

## Installation et lancement

Python 3.10 ou plus récent recommandé. Aucun paquet externe n'est requis.

Dans un terminal, placez-vous dans le dossier du projet puis lancez :

```bash
python main.py
```

## Menu principal

1. Ajouter une boîte
2. Afficher les boîtes
3. Analyser la position du contrôleur
4. Lancer les expériences comparatives
5. Charger une scène de démonstration
0. Quitter

## Tests automatiques

Lancez :
test_projet.py

Les tests vérifient les distances connues, les états, les rotations et le retour des coordonnées après transformation inverse.

## Expériences pertinentes à réaliser 

1. **Validation géométrique** : tester des points à l'intérieur, sur la surface, près d'une face et en diagonale.
2. **Marge de sécurité** : comparer plusieurs marges sur les mêmes points.
3. **Rotation** : faire tourner une boîte sans déplacer le contrôleur.
4. **Flottants** : observer des valeurs très proches d'une limite et discuter le choix de la tolérance.
5. **Matrices** : transformer un point vers le repère mondial puis revenir au repère local ; mesurer l'erreur maximale.
6. **Performance** : mesurer plusieurs tailles de scène. Les résultats varient selon l'ordinateur ; répéter les mesures et comparer les tendances.

## Limites

- Le contrôleur est un point, pas une sphère ayant un rayon.
- Les objets sont des boîtes rectangulaires ; les structures complexes ne sont pas traités.
- Les angles suivent la convention `Rz @ Ry @ Rx` (rotation X, puis Y, puis Z appliquées au vecteur colonne).
- La tolérance numérique est un paramètre de modélisation à justifier.
- Les mesures de performance dépendent de l'environnement.

## Plan d'amélioration possible

- Ajouter un rayon au contrôleur.
- Enregistrer les scènes dans un fichier.
- Ajouter des tests aléatoires reproductibles.
