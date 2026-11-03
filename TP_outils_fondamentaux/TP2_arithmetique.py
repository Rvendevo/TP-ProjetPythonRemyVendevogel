import math
import time


def diviseurs(n):
    if n <= 0:
        raise ValueError("L'entier doit être strictement positif.")
    resultat = []
    for diviseur in range(1, math.isqrt(n) + 1):
        if n % diviseur == 0:
            resultat.append(diviseur)
            if diviseur != n // diviseur:
                resultat.append(n // diviseur)
    return sorted(resultat)


def est_parfait(n):
    if n < 2:
        return False
    return sum(diviseurs(n)[:-1]) == n


def pgcd_naif(a, b):
    a, b = abs(a), abs(b)
    if a == 0 and b == 0:
        return 0
    meilleur = 1
    for diviseur in range(1, min(a, b) + 1):
        if a % diviseur == 0 and b % diviseur == 0:
            meilleur = diviseur
    return meilleur


def pgcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def est_premier_naif(n):
    if n < 2:
        return False
    for diviseur in range(2, n):
        if n % diviseur == 0:
            return False
    return True


def est_premier(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    diviseur = 3
    while diviseur * diviseur <= n:
        if n % diviseur == 0:
            return False
        diviseur += 2
    return True


def duree(fonction, argument):
    debut = time.perf_counter()
    resultat = fonction(argument)
    return resultat, time.perf_counter() - debut


def crible(limite):
    if limite < 0:
        raise ValueError("La limite doit être positive ou nulle.")
    tableau = [True] * (limite + 1)
    if limite >= 0:
        tableau[0] = False
    if limite >= 1:
        tableau[1] = False
    diviseur = 2
    while diviseur * diviseur <= limite:
        if tableau[diviseur]:
            for multiple in range(diviseur * diviseur, limite + 1, diviseur):
                tableau[multiple] = False
        diviseur += 1
    return [n for n, premier in enumerate(tableau) if premier]


def facteurs(n):
    if n < 1:
        raise ValueError("L'entier doit être strictement positif.")
    resultat = []
    diviseur = 2
    reste = n
    while diviseur * diviseur <= reste:
        while reste % diviseur == 0:
            resultat.append(diviseur)
            reste //= diviseur
        diviseur += 1
    if reste > 1:
        resultat.append(reste)
    return resultat


def fibonacci_recursif(n):
    if n < 0:
        raise ValueError("Le rang doit être positif ou nul.")
    if n < 2:
        return n
    return fibonacci_recursif(n - 1) + fibonacci_recursif(n - 2)


def fibonacci_compte(n, appels=None):
    if n < 0:
        raise ValueError("Le rang doit être positif ou nul.")
    if appels is None:
        appels = {}
    appels[n] = appels.get(n, 0) + 1
    if n < 2:
        return n
    return fibonacci_compte(n - 1, appels) + fibonacci_compte(n - 2, appels)


def fibonacci(n):
    if n < 0:
        raise ValueError("Le rang doit être positif ou nul.")
    precedent, courant = 0, 1
    for _ in range(n):
        precedent, courant = courant, precedent + courant
    return precedent


def temps_de_vol(n, plafond=100000):
    if n < 1:
        raise ValueError("Le départ doit être un entier strictement positif.")
    if plafond < 0:
        raise ValueError("Le plafond doit être positif ou nul.")
    tours = 0
    while n != 1 and tours < plafond:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        tours += 1
    if n != 1:
        raise RuntimeError("Le plafond d'itérations a été atteint.")
    return tours


def euclide_etendu(a, b):
    if b == 0:
        if a < 0:
            return -a, -1, 0
        return a, 1, 0
    pgcd_resultat, u, v = euclide_etendu(b, a % b)
    return pgcd_resultat, v, u - (a // b) * v


def puissance_mod_naive(a, e, n):
    if e < 0 or n <= 0:
        raise ValueError("L'exposant doit être positif ou nul et le modulo positif.")
    resultat = 1
    for _ in range(e):
        resultat = resultat * a % n
    return resultat


def puissance_mod(a, e, n):
    if e < 0 or n <= 0:
        raise ValueError("L'exposant doit être positif ou nul et le modulo positif.")
    resultat = 1
    base = a % n
    while e > 0:
        if e % 2 == 1:
            resultat = resultat * base % n
        base = base * base % n
        e //= 2
    return resultat


def tests():
    assert diviseurs(28) == [1, 2, 4, 7, 14, 28]
    assert diviseurs(1) == [1]
    assert diviseurs(36) == [1, 2, 3, 4, 6, 9, 12, 18, 36]
    assert [n for n in range(2, 10000) if est_parfait(n)] == [6, 28, 496, 8128]
    assert pgcd_naif(1071, 462) == pgcd(1071, 462) == 21
    assert pgcd(-48, 18) == 6
    assert pgcd(0, 7) == 7
    assert not est_premier(1) and not est_premier(0) and not est_premier(-7)
    assert est_premier(2) and est_premier(97) and not est_premier(91)
    assert crible(100) == [n for n in range(101) if est_premier(n)]
    assert len(crible(100000)) == 9592
    decomposition = facteurs(360)
    assert decomposition == [2, 2, 2, 3, 3, 5]
    assert math.prod(decomposition) == 360
    assert facteurs(1) == []
    assert facteurs(97) == [97]
    assert fibonacci(0) == 0 and fibonacci(1) == 1
    assert all(fibonacci(n) == fibonacci_recursif(n) for n in range(26))
    assert len(str(fibonacci(10000))) == 2090
    assert temps_de_vol(27) == 111
    assert euclide_etendu(1071, 462) == (21, -3, 7)
    assert 1071 * -3 + 462 * 7 == 21
    assert puissance_mod(7, 10**7, 1_000_003) == pow(7, 10**7, 1_000_003)
    assert puissance_mod_naive(7, 100, 97) == puissance_mod(7, 100, 97)
    for fonction in (lambda: diviseurs(0), lambda: facteurs(0), lambda: temps_de_vol(0),
                     lambda: puissance_mod(2, -1, 5), lambda: crible(-1)):
        try:
            fonction()
        except ValueError:
            pass
        else:
            raise AssertionError("Une entrée invalide aurait dû provoquer une erreur.")


if __name__ == "__main__":
    print("Diviseurs de 28 :", diviseurs(28))
    print("Nombres parfaits sous 10 000 :", [n for n in range(2, 10000) if est_parfait(n)])
    print("PGCD naïf et Euclide :", pgcd_naif(1071, 462), pgcd(1071, 462))
    print("Primalité :", est_premier_naif(97), est_premier(97), est_premier(91))
    for nombre in (10_007, 100_003, 1_000_003):
        _, temps_naif = duree(est_premier_naif, nombre)
        _, temps_optimise = duree(est_premier, nombre)
        print(f"{nombre}: naïf {temps_naif:.6f} s | optimisé {temps_optimise:.6f} s")
    debut = time.perf_counter()
    premiers = crible(100_000)
    print("Crible :", len(premiers), "premiers en", time.perf_counter() - debut, "s")
    print("Facteurs de 360 :", facteurs(360))
    compteurs = {}
    print("Fibonacci récursif F(30) :", fibonacci_compte(30, compteurs))
    print("Appels à F(1) :", compteurs.get(1, 0), "| total :", sum(compteurs.values()))
    print("Fibonacci itératif F(10 000), nombre de chiffres :", len(str(fibonacci(10_000))))
    print("Temps de vol de 27 :", temps_de_vol(27))
    print("Euclide étendu :", euclide_etendu(1071, 462))
    print("Puissance modulaire :", puissance_mod(7, 10**7, 1_000_003))
    tests()
    print("Tous les tests du TP2 sont réussis.")
