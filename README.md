# Détecteur de collision et de proximité VR en 3D

## Présentation

Ce projet simule un point `controller` dans un espace tridimensionnel et détecte sa relation avec des cubes et des boîtes rectangulaires, y compris des boîtes tournées.

Il est réalisé en Python et fonctionne dans le terminal. Aucun casque VR ni bibliothèque externe n'est nécessaire.

## Problématique

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

```text
dx = max(abs(x) - hx, 0)
dy = max(abs(y) - hy, 0)
dz = max(abs(z) - hz, 0)
distance = sqrt(dx*dx + dy*dy + dz*dz)
```

La classification est :
- `COLLISION` si la distance est considérée nulle selon la tolérance choisie ;
- `PROXIMITÉ` si la distance est positive et inférieure ou égale à la marge ;
- `SÛR` au-delà de la marge.

Le modèle traite le contrôleur comme un point sans rayon. Il ne s'agit pas d'un système certifié de sécurité physique.

## Installation et lancement

Python 3.10 ou plus récent recommandé. Aucun paquet externe n'est requis.

Dans un terminal, place-toi dans le dossier du projet puis lance :

```bash
python main.py
```

Sur certains systèmes, la commande peut être `python3 main.py`.

## Menu principal

1. Ajouter une boîte
2. Afficher les boîtes
3. Analyser la position du contrôleur
4. Lancer les expériences comparatives
5. Charger une scène de démonstration
0. Quitter

## Tests automatiques

Lance :

```bash
python -m unittest -v
```

Les tests vérifient les distances connues, les états, les rotations et le retour des coordonnées après transformation inverse.

## Expériences à réaliser pour le rapport

1. **Validation géométrique** : tester des points à l'intérieur, sur la surface, près d'une face et en diagonale.
2. **Marge de sécurité** : comparer plusieurs marges sur les mêmes points.
3. **Rotation** : faire tourner une boîte sans déplacer le contrôleur.
4. **Flottants** : observer des valeurs très proches d'une limite et discuter le choix de la tolérance.
5. **Matrices** : transformer un point vers le repère mondial puis revenir au repère local ; mesurer l'erreur maximale.
6. **Performance** : mesurer plusieurs tailles de scène. Les résultats varient selon l'ordinateur ; répéter les mesures et comparer les tendances.

Pour un rapport solide, noter les paramètres, les résultats observés et une interprétation. Ne pas inventer de résultats : exécuter le programme et compléter le compte rendu avec ses propres mesures.

## Limites

- Le contrôleur est un point, pas une sphère ayant un rayon.
- Les objets sont des boîtes rectangulaires ; les maillages complexes ne sont pas traités.
- Les angles suivent la convention `Rz @ Ry @ Rx` (rotation X, puis Y, puis Z appliquées au vecteur colonne).
- La tolérance numérique est un paramètre de modélisation à justifier.
- Les mesures de performance dépendent de l'environnement.
- Le programme est un projet pédagogique, pas un système de sécurité certifié.

## Plan d'amélioration possible

- Ajouter un rayon au contrôleur.
- Enregistrer les scènes dans un fichier JSON.
- Ajouter des tests aléatoires reproductibles.
- Comparer l'inversion générale de la matrice à une inversion spécialisée des transformations rigides.
