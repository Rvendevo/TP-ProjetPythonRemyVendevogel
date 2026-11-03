"""Opérations matricielles implémentées avec les listes Python.

Convention :
- les points sont des vecteurs-colonnes ;
- la rotation d'un objet est R = Rz @ Ry @ Rx ;
- T transforme les coordonnées locales en coordonnées mondiales ;
- le point mondial est converti en local avec T^-1.
"""

import math

Matrice = list[list[float]]


def identite(taille: int) -> Matrice:
    return [
        [1.0 if ligne == colonne else 0.0 for colonne in range(taille)]
        for ligne in range(taille)
    ]


def multiplier_matrices(a: Matrice, b: Matrice) -> Matrice:
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("Dimensions de matrices incompatibles.")
    if any(len(ligne) != len(a[0]) for ligne in a):
        raise ValueError("La première matrice n'est pas rectangulaire.")
    if any(len(ligne) != len(b[0]) for ligne in b):
        raise ValueError("La deuxième matrice n'est pas rectangulaire.")
    lignes, colonnes, commun = len(a), len(b[0]), len(b)
    resultat = [[0.0] * colonnes for _ in range(lignes)]
    for i in range(lignes):
        for j in range(colonnes):
            for k in range(commun):
                resultat[i][j] += a[i][k] * b[k][j]
    return resultat


def multiplier_matrice_vecteur(a: Matrice, v: list[float]) -> list[float]:
    if any(len(ligne) != len(v) for ligne in a):
        raise ValueError("Dimensions incompatibles entre matrice et vecteur.")
    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]


def rotation_x(angle_degres: float) -> Matrice:
    angle = math.radians(angle_degres)
    c, s = math.cos(angle), math.sin(angle)
    return [
        [1.0, 0.0, 0.0],
        [0.0, c, -s],
        [0.0, s, c],
    ]


def rotation_y(angle_degres: float) -> Matrice:
    angle = math.radians(angle_degres)
    c, s = math.cos(angle), math.sin(angle)
    return [
        [c, 0.0, s],
        [0.0, 1.0, 0.0],
        [-s, 0.0, c],
    ]


def rotation_z(angle_degres: float) -> Matrice:
    angle = math.radians(angle_degres)
    c, s = math.cos(angle), math.sin(angle)
    return [
        [c, -s, 0.0],
        [s, c, 0.0],
        [0.0, 0.0, 1.0],
    ]


def rotation_totale(angle_x: float, angle_y: float, angle_z: float) -> Matrice:
    # L'ordre compte : les rotations ne commutent généralement pas.
    rx = rotation_x(angle_x)
    ry = rotation_y(angle_y)
    rz = rotation_z(angle_z)
    return multiplier_matrices(multiplier_matrices(rz, ry), rx)


def transposer(a: Matrice) -> Matrice:
    return [list(colonne) for colonne in zip(*a)]


def inverser_matrice(a: Matrice) -> Matrice:
    """Inverse une matrice carrée par élimination de Gauss-Jordan."""
    n = len(a)
    if n == 0 or any(len(ligne) != n for ligne in a):
        raise ValueError("La matrice doit être carrée et non vide.")

    gauche = [[float(valeur) for valeur in ligne] for ligne in a]
    droite = identite(n)
    epsilon = 1e-12

    for colonne in range(n):
        pivot = max(range(colonne, n), key=lambda ligne: abs(gauche[ligne][colonne]))
        if abs(gauche[pivot][colonne]) < epsilon:
            raise ValueError("Matrice singulière ou trop proche de l'être.")

        gauche[colonne], gauche[pivot] = gauche[pivot], gauche[colonne]
        droite[colonne], droite[pivot] = droite[pivot], droite[colonne]

        valeur_pivot = gauche[colonne][colonne]
        gauche[colonne] = [valeur / valeur_pivot for valeur in gauche[colonne]]
        droite[colonne] = [valeur / valeur_pivot for valeur in droite[colonne]]

        for ligne in range(n):
            if ligne == colonne:
                continue
            facteur = gauche[ligne][colonne]
            gauche[ligne] = [
                gauche[ligne][j] - facteur * gauche[colonne][j]
                for j in range(n)
            ]
            droite[ligne] = [
                droite[ligne][j] - facteur * droite[colonne][j]
                for j in range(n)
            ]

    return droite


def matrice_homogene(rotation: Matrice, centre: tuple[float, float, float]) -> Matrice:
    """Construit T, transformation des coordonnées locales vers mondiales."""
    if len(rotation) != 3 or any(len(ligne) != 3 for ligne in rotation):
        raise ValueError("La rotation doit être une matrice 3x3.")
    cx, cy, cz = centre
    return [
        [rotation[0][0], rotation[0][1], rotation[0][2], cx],
        [rotation[1][0], rotation[1][1], rotation[1][2], cy],
        [rotation[2][0], rotation[2][1], rotation[2][2], cz],
        [0.0, 0.0, 0.0, 1.0],
    ]


def transformer_point(t: Matrice, point: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = point
    resultat = multiplier_matrice_vecteur(t, [x, y, z, 1.0])
    if abs(resultat[3]) < 1e-12:
        raise ValueError("Coordonnée homogène invalide.")
    return (
        resultat[0] / resultat[3],
        resultat[1] / resultat[3],
        resultat[2] / resultat[3],
    )
