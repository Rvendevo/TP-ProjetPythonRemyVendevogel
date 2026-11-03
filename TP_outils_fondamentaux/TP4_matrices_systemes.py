import math
import random
from fractions import Fraction
import time


def verifier_matrice(matrice):
    if not matrice or not matrice[0]:
        raise ValueError("La matrice ne doit pas être vide.")
    largeur = len(matrice[0])
    if any(len(ligne) != largeur for ligne in matrice):
        raise ValueError("Toutes les lignes doivent avoir la même longueur.")


def transposee(A):
    verifier_matrice(A)
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def produit(A, B):
    verifier_matrice(A)
    verifier_matrice(B)
    if len(A[0]) != len(B):
        raise ValueError("Les dimensions des matrices ne sont pas compatibles.")
    resultat = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                resultat[i][j] += A[i][k] * B[k][j]
    return resultat


def matrice_aleatoire(n):
    if n < 1:
        raise ValueError("La taille doit être positive.")
    return [[random.random() for _ in range(n)] for _ in range(n)]


def resoudre(A, b, tolerance=1e-14):
    verifier_matrice(A)
    n = len(A)
    if len(A[0]) != n or len(b) != n:
        raise ValueError("Le système doit être carré et le second membre de taille adaptée.")
    if tolerance < 0:
        raise ValueError("La tolérance doit être positive ou nulle.")
    matrice = [list(A[i]) + [b[i]] for i in range(n)]
    for colonne in range(n):
        ligne_pivot = max(range(colonne, n), key=lambda i: abs(matrice[i][colonne]))
        if abs(matrice[ligne_pivot][colonne]) <= tolerance:
            raise ValueError("Le système est singulier ou trop mal conditionné.")
        matrice[colonne], matrice[ligne_pivot] = matrice[ligne_pivot], matrice[colonne]
        for ligne in range(colonne + 1, n):
            facteur = matrice[ligne][colonne] / matrice[colonne][colonne]
            matrice[ligne][colonne] = 0.0
            for indice in range(colonne + 1, n + 1):
                matrice[ligne][indice] -= facteur * matrice[colonne][indice]
    solution = [0.0] * n
    for ligne in range(n - 1, -1, -1):
        somme = matrice[ligne][n]
        for colonne in range(ligne + 1, n):
            somme -= matrice[ligne][colonne] * solution[colonne]
        solution[ligne] = somme / matrice[ligne][ligne]
    return solution


def appliquer_matrice(A, vecteur):
    verifier_matrice(A)
    if len(A[0]) != len(vecteur):
        raise ValueError("La dimension du vecteur est incompatible.")
    return [sum(coefficient * valeur for coefficient, valeur in zip(ligne, vecteur)) for ligne in A]


def matrice_hilbert(n):
    if n < 1:
        raise ValueError("La taille doit être positive.")
    return [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]


def matrice_rotation(angle_degres):
    angle = math.radians(angle_degres)
    return [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]


def transformer_point(matrice, point):
    resultat = appliquer_matrice(matrice, point)
    return tuple(resultat)



def determinant(A, tolerance=1e-14):
    verifier_matrice(A)
    n = len(A)
    if len(A[0]) != n:
        raise ValueError("Le déterminant exige une matrice carrée.")
    matrice = [list(ligne) for ligne in A]
    resultat = 1
    for colonne in range(n):
        ligne_pivot = max(range(colonne, n), key=lambda i: abs(matrice[i][colonne]))
        if abs(matrice[ligne_pivot][colonne]) <= tolerance:
            return 0
        if ligne_pivot != colonne:
            matrice[colonne], matrice[ligne_pivot] = matrice[ligne_pivot], matrice[colonne]
            resultat = -resultat
        pivot = matrice[colonne][colonne]
        resultat *= pivot
        for ligne in range(colonne + 1, n):
            facteur = matrice[ligne][colonne] / pivot
            for indice in range(colonne, n):
                matrice[ligne][indice] -= facteur * matrice[colonne][indice]
    return resultat


def hilbert_exacte(n):
    if n < 1:
        raise ValueError("La taille doit être positive.")
    return [[Fraction(1, i + j + 1) for j in range(n)] for i in range(n)]


def inverse(A, tolerance=1e-14):
    verifier_matrice(A)
    n = len(A)
    if len(A[0]) != n:
        raise ValueError("L'inverse exige une matrice carrée.")
    matrice = [list(map(float, A[i])) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for colonne in range(n):
        ligne_pivot = max(range(colonne, n), key=lambda i: abs(matrice[i][colonne]))
        if abs(matrice[ligne_pivot][colonne]) <= tolerance:
            raise ValueError("La matrice est singulière.")
        matrice[colonne], matrice[ligne_pivot] = matrice[ligne_pivot], matrice[colonne]
        pivot = matrice[colonne][colonne]
        matrice[colonne] = [valeur / pivot for valeur in matrice[colonne]]
        for ligne in range(n):
            if ligne != colonne:
                facteur = matrice[ligne][colonne]
                matrice[ligne] = [matrice[ligne][indice] - facteur * matrice[colonne][indice] for indice in range(2*n)]
    return [ligne[n:] for ligne in matrice]


def translation(tx, ty):
    return [[1.0, 0.0, tx], [0.0, 1.0, ty], [0.0, 0.0, 1.0]]


def rotation_h(angle_radians):
    cosinus, sinus = math.cos(angle_radians), math.sin(angle_radians)
    return [[cosinus, -sinus, 0.0], [sinus, cosinus, 0.0], [0.0, 0.0, 1.0]]


def produit_matrice_vecteur(A, vecteur):
    return [sum(coefficient * valeur for coefficient, valeur in zip(ligne, vecteur)) for ligne in A]


def tests():
    assert transposee([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transposee([[1]]) == [[1]]
    assert produit([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]
    assert produit([[1, 2, 3]], [[1], [2], [3]]) == [[14]]
    matrice = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
    second_membre = [2, -1, 8]
    solution = resoudre(matrice, second_membre)
    assert all(math.isclose(a, b, abs_tol=1e-10) for a, b in zip(solution, [3, -1, 0.5]))
    assert all(math.isclose(a, b, abs_tol=1e-10)
               for a, b in zip(appliquer_matrice(matrice, solution), second_membre))
    assert resoudre([[2, 1], [1, 1]], [5, 3]) == [2.0, 1.0]
    assert math.isclose(transformer_point(matrice_rotation(90), (1, 0))[0], 0, abs_tol=1e-12)
    assert math.isclose(transformer_point(matrice_rotation(90), (1, 0))[1], 1, abs_tol=1e-12)
    assert math.isclose(determinant([[1, 2, 2], [1, 3, -2], [3, 5, 8]]), -2, abs_tol=1e-12)
    assert determinant([[1, 2], [2, 4]]) == 0
    hilbert = hilbert_exacte(12)
    second_membre_exact = [sum(ligne) for ligne in hilbert]
    solution_exacte = resoudre(hilbert, second_membre_exact, tolerance=0)
    assert solution_exacte == [Fraction(1)] * 12
    matrice_inverse = inverse([[1, 2], [3, 4]])
    identite = produit([[1, 2], [3, 4]], matrice_inverse)
    assert all(math.isclose(identite[i][j], 1.0 if i == j else 0.0, abs_tol=1e-12) for i in range(2) for j in range(2))
    point_homogene = [1.0, 0.0, 1.0]
    resultat_premier = produit_matrice_vecteur(rotation_h(math.pi/2), produit_matrice_vecteur(translation(3, 1), point_homogene))
    resultat_second = produit_matrice_vecteur(translation(3, 1), produit_matrice_vecteur(rotation_h(math.pi/2), point_homogene))
    assert all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(resultat_premier, [-1, 4, 1]))
    assert all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(resultat_second, [3, 2, 1]))
    for fonction in (
        lambda: transposee([[1, 2], [3]]),
        lambda: produit([[1, 2]], [[1, 2]]),
        lambda: resoudre([[1, 2], [2, 4]], [3, 6]),
        lambda: resoudre([[1, 2]], [3]),
    ):
        try:
            fonction()
        except ValueError:
            pass
        else:
            raise AssertionError("Une matrice invalide aurait dû provoquer une erreur.")


if __name__ == "__main__":
    A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
    b = [2, -1, 8]
    print("Transposée :", transposee(A))
    print("Produit matriciel :", produit(A, A))
    print("Solution du système :", resoudre(A, b))
    print("Vérification Ax :", appliquer_matrice(A, resoudre(A, b)))
    random.seed(42)
    for taille in (40, 80, 120):
        premiere = matrice_aleatoire(taille)
        seconde = matrice_aleatoire(taille)
        debut = time.perf_counter()
        produit(premiere, seconde)
        print(f"Produit Python, taille {taille}: {time.perf_counter() - debut:.4f} s")
    try:
        import numpy as np
        taille = 120
        premiere = matrice_aleatoire(taille)
        seconde = matrice_aleatoire(taille)
        debut = time.perf_counter()
        produit(premiere, seconde)
        temps_python = time.perf_counter() - debut
        debut = time.perf_counter()
        np.array(premiere) @ np.array(seconde)
        temps_numpy = time.perf_counter() - debut
        print(f"Python pur : {temps_python:.6f} s | NumPy : {temps_numpy:.6f} s")
        random.seed(7)
        taille = 50
        premiere = matrice_aleatoire(taille)
        second_membre = [random.random() for _ in range(taille)]
        solution_python = resoudre(premiere, second_membre)
        solution_numpy = np.linalg.solve(np.array(premiere), np.array(second_membre))
        print("Écart maximal avec NumPy :", max(abs(a - b) for a, b in zip(solution_python, solution_numpy)))
        hilbert = np.array(matrice_hilbert(12))
        solution_vraie = np.ones(12)
        second_membre = hilbert @ solution_vraie
        solution_directe = np.linalg.solve(hilbert, second_membre)
        solution_inverse = np.linalg.inv(hilbert) @ second_membre
        print("Erreur solve :", float(np.max(np.abs(solution_directe - solution_vraie))))
        print("Erreur inverse :", float(np.max(np.abs(solution_inverse - solution_vraie))))
        print("Conditionnement :", float(np.linalg.cond(hilbert)))
    except ImportError:
        print("NumPy n'est pas installé : les comparaisons NumPy sont ignorées.")
    print("Rotation de 90 degrés :", transformer_point(matrice_rotation(90), (1, 0)))
    print("Déterminant :", determinant(A))
    hilbert_exact = hilbert_exacte(12)
    second_membre_exact = [sum(ligne) for ligne in hilbert_exact]
    print("Solution exacte de Hilbert :", resoudre(hilbert_exact, second_membre_exact, tolerance=0))
    print("Inverse de la matrice :", inverse([[1, 2], [3, 4]]))
    point_homogene = [1.0, 0.0, 1.0]
    print("Translation puis rotation :", produit_matrice_vecteur(rotation_h(math.pi/2), produit_matrice_vecteur(translation(3, 1), point_homogene)))
    print("Rotation puis translation :", produit_matrice_vecteur(translation(3, 1), produit_matrice_vecteur(rotation_h(math.pi/2), point_homogene)))
    tests()
    print("Tous les tests du TP4 sont réussis.")
