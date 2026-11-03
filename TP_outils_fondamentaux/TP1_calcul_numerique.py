import math
import sys
from fractions import Fraction


def division_euclidienne(nombre, diviseur):
    if diviseur == 0:
        raise ZeroDivisionError("Le diviseur ne peut pas être nul.")
    return nombre // diviseur, nombre % diviseur


def presque_egaux(a, b, tolerance=1e-9):
    if tolerance < 0:
        raise ValueError("La tolérance doit être positive ou nulle.")
    return math.isclose(a, b, rel_tol=tolerance, abs_tol=tolerance)


def nombre_de_chiffres(n):
    n = abs(n)
    compte = 1
    while n >= 10:
        n //= 10
        compte += 1
    return compte


def heron(a, tolerance=1e-12, tours_max=1000, avec_tours=False):
    if a < 0:
        raise ValueError("La racine carrée réelle d'un nombre négatif n'existe pas.")
    if tolerance <= 0:
        raise ValueError("La tolérance doit être strictement positive.")
    if tours_max < 1:
        raise ValueError("Le nombre maximal de tours doit être positif.")
    if a == 0:
        return (0.0, 0) if avec_tours else 0.0
    estimation = float(a) if a >= 1 else 1.0
    for tour in range(1, tours_max + 1):
        suivante = 0.5 * (estimation + a / estimation)
        if abs(suivante - estimation) <= tolerance * abs(suivante):
            return (suivante, tour) if avec_tours else suivante
        estimation = suivante
    raise RuntimeError("La méthode de Héron n'a pas convergé.")


def vers_binaire(n):
    if n < 0:
        raise ValueError("L'entier doit être positif ou nul.")
    if n == 0:
        return "0"
    chiffres = ""
    while n > 0:
        chiffres = str(n % 2) + chiffres
        n //= 2
    return chiffres


def epsilon_machine():
    epsilon = 1.0
    while 1.0 + epsilon / 2 != 1.0:
        epsilon /= 2
    return epsilon


def racines_naif(a, b, c):
    if a == 0:
        raise ValueError("Le coefficient a doit être non nul.")
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("L'équation ne possède pas de racines réelles.")
    racine_delta = math.sqrt(delta)
    return (-b - racine_delta) / (2 * a), (-b + racine_delta) / (2 * a)


def racines(a, b, c):
    if a == 0:
        raise ValueError("Le coefficient a doit être non nul.")
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("L'équation ne possède pas de racines réelles.")
    if delta == 0:
        racine = -b / (2 * a)
        return racine, racine
    racine_delta = math.sqrt(delta)
    if b >= 0:
        racine_sure = (-b - racine_delta) / (2 * a)
    else:
        racine_sure = (-b + racine_delta) / (2 * a)
    autre_racine = c / (a * racine_sure) if racine_sure != 0 else (-b - racine_delta) / (2 * a)
    return tuple(sorted((racine_sure, autre_racine)))


def tests():
    quotient, reste = division_euclidienne(2026, 7)
    assert (quotient, reste) == (289, 3)
    assert quotient * 7 + reste == 2026
    assert division_euclidienne(10, 5) == (2, 0)
    assert presque_egaux(0.1 + 0.2, 0.3)
    assert not presque_egaux(1.0, 1.5)
    total = 0.0
    for _ in range(1000):
        total += 0.1
    assert abs(total - 100) < 1e-10
    assert nombre_de_chiffres(2026) == 4
    assert nombre_de_chiffres(7) == 1
    assert nombre_de_chiffres(0) == 1
    assert nombre_de_chiffres(-12345) == 5
    assert abs(heron(2) - math.sqrt(2)) < 1e-12
    assert heron(0) == 0.0
    assert abs(heron(1e-20) - 1e-10) < 1e-20
    assert vers_binaire(37) == "100101"
    assert vers_binaire(0) == "0"
    assert all(vers_binaire(n) == bin(n)[2:] for n in range(2000))
    assert epsilon_machine() == sys.float_info.epsilon
    petite, grande = racines(1.0, -1e8, 1.0)
    assert math.isclose(petite, 1e-8, rel_tol=1e-12)
    assert math.isclose(grande, 1e8, rel_tol=1e-12)
    assert math.isclose(petite * grande, 1.0, rel_tol=1e-12)
    assert racines(1, 2, 1) == (-1.0, -1.0)
    rationnel = sum((Fraction(1, 10) for _ in range(1000)), Fraction(0))
    assert rationnel == 100
    assert Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10)
    for fonction, arguments in (
        (lambda: division_euclidienne(1, 0), ()),
        (lambda: heron(-1), ()),
        (lambda: vers_binaire(-1), ()),
        (lambda: racines(0, 1, 1), ()),
        (lambda: racines(1, 0, 1), ()),
    ):
        try:
            fonction()
        except (ValueError, ZeroDivisionError):
            pass
        else:
            raise AssertionError("Une entrée invalide aurait dû provoquer une erreur.")


if __name__ == "__main__":
    print("Division euclidienne :", division_euclidienne(2026, 7))
    print("Dernier chiffre et nombre tronqué :", 123456789 % 10, 123456789 // 10)
    print("0.1 + 0.2 :", 0.1 + 0.2)
    print("Comparaison tolérante :", presque_egaux(0.1 + 0.2, 0.3))
    total = 0.0
    for _ in range(1000):
        total += 0.1
    print("Accumulation :", total, "écart :", total - 100)
    print("Table de 7 :")
    for multiplicateur in range(1, 11):
        print(f"7 x {multiplicateur} = {7 * multiplicateur}")
    somme = 0
    for entier in range(1, 101):
        somme += entier
    print("Somme par boucle et formule :", somme, 100 * 101 // 2)
    print("Nombre de chiffres :", nombre_de_chiffres(2026), nombre_de_chiffres(10**60))
    print("Racine de 2 par Héron :", heron(2), "Tours :", heron(2, avec_tours=True)[1])
    print("Binaire de 37 :", vers_binaire(37))
    print("Epsilon machine :", epsilon_machine())
    print("Racines naïves :", racines_naif(1.0, -1e8, 1.0))
    print("Racines stables :", racines(1.0, -1e8, 1.0))
    print("Somme exacte de fractions :", sum((Fraction(1, 10) for _ in range(1000)), Fraction(0)))
    tests()
    print("Tous les tests du TP1 sont réussis.")
