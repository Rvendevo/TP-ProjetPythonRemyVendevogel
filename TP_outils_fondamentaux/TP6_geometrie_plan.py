import math
import random


def vecteur(A, B):
    return B[0] - A[0], B[1] - A[1]


def produit_scalaire(u, v):
    return u[0] * v[0] + u[1] * v[1]


def norme(u):
    return math.sqrt(produit_scalaire(u, u))


def angle(u, v):
    norme_u, norme_v = norme(u), norme(v)
    if math.isclose(norme_u, 0.0) or math.isclose(norme_v, 0.0):
        raise ValueError("L'angle d'un vecteur nul n'est pas défini.")
    cosinus = produit_scalaire(u, v) / (norme_u * norme_v)
    cosinus = max(-1.0, min(1.0, cosinus))
    return math.degrees(math.acos(cosinus))


def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]


def orientation(A, B, C, tolerance=1e-12):
    valeur = determinant(vecteur(A, B), vecteur(A, C))
    if math.isclose(valeur, 0.0, abs_tol=tolerance):
        return 0
    return 1 if valeur > 0 else -1


def aire(polygone):
    if len(polygone) < 3:
        return 0.0
    somme = 0
    for indice in range(len(polygone)):
        x1, y1 = polygone[indice]
        x2, y2 = polygone[(indice + 1) % len(polygone)]
        somme += x1 * y2 - x2 * y1
    return abs(somme) / 2


def sur_segment(A, B, P, tolerance=1e-12):
    if orientation(A, B, P, tolerance) != 0:
        return False
    return (min(A[0], B[0]) - tolerance <= P[0] <= max(A[0], B[0]) + tolerance
            and min(A[1], B[1]) - tolerance <= P[1] <= max(A[1], B[1]) + tolerance)


def se_coupent(A, B, C, D):
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return (
        (o1 == 0 and sur_segment(A, B, C))
        or (o2 == 0 and sur_segment(A, B, D))
        or (o3 == 0 and sur_segment(C, D, A))
        or (o4 == 0 and sur_segment(C, D, B))
    )


def intersection(A, B, C, D):
    ab = vecteur(A, B)
    cd = vecteur(C, D)
    denominateur = determinant(ab, cd)
    if math.isclose(denominateur, 0.0, abs_tol=1e-12):
        if se_coupent(A, B, C, D):
            return "segments colinéaires ou parallèles confondus"
        return None
    ac = vecteur(A, C)
    t = determinant(ac, cd) / denominateur
    u = determinant(ac, ab) / denominateur
    if -1e-12 <= t <= 1 + 1e-12 and -1e-12 <= u <= 1 + 1e-12:
        return A[0] + t * ab[0], A[1] + t * ab[1]
    return None


def dedans(P, polygone, inclure_bord=True):
    if len(polygone) < 3:
        return False
    x, y = P
    interieur = False
    for indice in range(len(polygone)):
        premier = polygone[indice]
        suivant = polygone[(indice + 1) % len(polygone)]
        if inclure_bord and sur_segment(premier, suivant, P):
            return True
        x1, y1 = premier
        x2, y2 = suivant
        if (y1 > y) != (y2 > y):
            x_croisement = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_croisement:
                interieur = not interieur
    return interieur


def aire_monte_carlo(polygone, xmin, xmax, ymin, ymax, tirages=200000, graine=None):
    if tirages <= 0 or xmin >= xmax or ymin >= ymax:
        raise ValueError("Les bornes et le nombre de tirages sont invalides.")
    generateur = random.Random(graine)
    touches = 0
    for _ in range(tirages):
        point = (generateur.uniform(xmin, xmax), generateur.uniform(ymin, ymax))
        if dedans(point, polygone):
            touches += 1
    return (xmax - xmin) * (ymax - ymin) * touches / tirages


def tests():
    assert vecteur((1, 2), (4, 6)) == (3, 4)
    assert produit_scalaire((1, 2), (3, 4)) == 11
    assert norme((3, 4)) == 5
    assert math.isclose(angle((1, 0), (1, 1)), 45.0)
    assert math.isclose(angle((1, 0), (0, 1)), 90.0)
    assert determinant((1, 0), (0, 1)) == 1
    assert orientation((0, 0), (1, 0), (1, 1)) == 1
    assert orientation((0, 0), (1, 0), (1, -1)) == -1
    assert orientation((0, 0), (1, 1), (2, 2)) == 0
    carre = [(0, 0), (1, 0), (1, 1), (0, 1)]
    triangle = [(0, 0), (4, 0), (0, 3)]
    maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
    assert aire(carre) == 1.0
    assert aire(triangle) == 6.0
    assert aire(maison) == 4.0
    assert math.isclose(aire(maison), aire(maison[::-1]))
    assert se_coupent((0, 0), (2, 2), (0, 2), (2, 0))
    assert not se_coupent((0, 0), (1, 0), (0, 1), (1, 1))
    assert se_coupent((0, 0), (2, 0), (1, 0), (3, 0))
    assert intersection((0, 0), (2, 2), (0, 2), (2, 0)) == (1.0, 1.0)
    assert intersection((0, 0), (1, 0), (0, 1), (1, 1)) is None
    assert dedans((1, 1), maison)
    assert dedans((1, 2.4), maison)
    assert not dedans((3, 1), maison)
    assert not dedans((0.2, 2.2), maison)
    assert dedans((0, 0), carre)
    assert math.isclose(aire_monte_carlo(maison, 0, 2, 0, 2.5, 200000, 0), 4.0, abs_tol=0.04)
    try:
        angle((0, 0), (1, 0))
    except ValueError:
        pass
    else:
        raise AssertionError("Un vecteur nul ne définit pas d'angle.")
    try:
        aire_monte_carlo(maison, 0, 2, 0, 2.5, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("Un nombre de tirages nul doit être refusé.")


if __name__ == "__main__":
    point_a, point_b = (1, 2), (4, 6)
    vecteur_ab = vecteur(point_a, point_b)
    print("Vecteur AB :", vecteur_ab)
    print("Produit scalaire :", produit_scalaire((1, 2), (3, 4)))
    print("Norme :", norme(vecteur_ab))
    print("Angle :", angle((1, 0), (1, 1)))
    maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
    print("Aire de la maison :", aire(maison))
    print("Orientation gauche/droite/aligné :",
          orientation((0, 0), (1, 0), (1, 1)),
          orientation((0, 0), (1, 0), (1, -1)),
          orientation((0, 0), (1, 1), (2, 2)))
    print("Intersection des diagonales :", intersection((0, 0), (2, 2), (0, 2), (2, 0)))
    for point in ((1, 1), (1, 2.4), (3, 1), (0.2, 2.2)):
        print("Point", point, "dans la maison :", dedans(point, maison))
    print("Aire estimée par Monte-Carlo :", aire_monte_carlo(maison, 0, 2, 0, 2.5, 200000))
    tests()
    print("Tous les tests du TP6 sont réussis.")
