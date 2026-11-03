import math
import time


def evaluer_naif(P, x):
    total = 0
    for indice, coefficient in enumerate(P):
        total += coefficient * x ** indice
    return total


def evaluer(P, x):
    total = 0
    for coefficient in reversed(P):
        total = total * x + coefficient
    return total


def deriver(P):
    return [indice * P[indice] for indice in range(1, len(P))]


def dichotomie(fonction, a, b, tolerance=1e-12, tours_max=1000):
    if tolerance <= 0 or tours_max < 1:
        raise ValueError("La tolérance et le nombre de tours doivent être positifs.")
    valeur_a, valeur_b = fonction(a), fonction(b)
    if valeur_a == 0:
        return a
    if valeur_b == 0:
        return b
    if valeur_a * valeur_b > 0:
        raise ValueError("Les bornes doivent encadrer un changement de signe.")
    for _ in range(tours_max):
        milieu = (a + b) / 2
        valeur_milieu = fonction(milieu)
        if valeur_milieu == 0 or abs(b - a) <= tolerance:
            return milieu
        if valeur_a * valeur_milieu < 0:
            b, valeur_b = milieu, valeur_milieu
        else:
            a, valeur_a = milieu, valeur_milieu
    raise RuntimeError("La dichotomie n'a pas atteint la tolérance demandée.")


def newton(P, depart, tolerance=1e-12, tours_max=100):
    if tolerance <= 0 or tours_max < 1:
        raise ValueError("La tolérance et le nombre de tours doivent être positifs.")
    derivee = deriver(P)
    x = float(depart)
    for tour in range(1, tours_max + 1):
        valeur = evaluer(P, x)
        pente = evaluer(derivee, x)
        if math.isclose(pente, 0.0, abs_tol=1e-15):
            raise ZeroDivisionError("La dérivée est trop proche de zéro.")
        suivant = x - valeur / pente
        if abs(suivant - x) <= tolerance * max(1.0, abs(suivant)):
            return suivant, tour
        x = suivant
    raise RuntimeError("La méthode de Newton n'a pas convergé.")


def newton_trace(P, depart, tours):
    derivee = deriver(P)
    x = float(depart)
    trajet = [x]
    for _ in range(tours):
        pente = evaluer(derivee, x)
        if math.isclose(pente, 0.0, abs_tol=1e-15):
            break
        x -= evaluer(P, x) / pente
        trajet.append(x)
    return trajet


def integrer_rectangles(fonction, a, b, subdivisions=10000):
    if subdivisions <= 0:
        raise ValueError("Le nombre de subdivisions doit être positif.")
    largeur = (b - a) / subdivisions
    return sum(fonction(a + indice * largeur) for indice in range(subdivisions)) * largeur



def somme(P, Q):
    longueur = max(len(P), len(Q))
    return [(P[i] if i < len(P) else 0) + (Q[i] if i < len(Q) else 0) for i in range(longueur)]


def produit_poly(P, Q):
    if not P or not Q:
        return []
    resultat = [0] * (len(P) + len(Q) - 1)
    for indice_p, coefficient_p in enumerate(P):
        for indice_q, coefficient_q in enumerate(Q):
            resultat[indice_p + indice_q] += coefficient_p * coefficient_q
    return resultat


def derivee_avant(fonction, x, h):
    if h == 0:
        raise ValueError("Le pas doit être non nul.")
    return (fonction(x + h) - fonction(x)) / h


def derivee_centree(fonction, x, h):
    if h == 0:
        raise ValueError("Le pas doit être non nul.")
    return (fonction(x + h) - fonction(x - h)) / (2 * h)


def rectangles(fonction, a, b, n):
    if n <= 0:
        raise ValueError("Le nombre de subdivisions doit être positif.")
    largeur = (b - a) / n
    return largeur * sum(fonction(a + i * largeur) for i in range(n))


def trapezes(fonction, a, b, n):
    if n <= 0:
        raise ValueError("Le nombre de subdivisions doit être positif.")
    largeur = (b - a) / n
    interieur = sum(fonction(a + i * largeur) for i in range(1, n))
    return largeur * ((fonction(a) + fonction(b)) / 2 + interieur)


def simpson(fonction, a, b, n):
    if n <= 0:
        raise ValueError("Le nombre de subdivisions doit être positif.")
    if n % 2 == 1:
        n += 1
    largeur = (b - a) / n
    impairs = sum(fonction(a + i * largeur) for i in range(1, n, 2))
    pairs = sum(fonction(a + i * largeur) for i in range(2, n, 2))
    return largeur / 3 * (fonction(a) + fonction(b) + 4 * impairs + 2 * pairs)


def newton_general(fonction, depart, tolerance=1e-12, tours_max=100):
    x = float(depart)
    for tour in range(1, tours_max + 1):
        pente = derivee_centree(fonction, x, 1e-6)
        if math.isclose(pente, 0.0, abs_tol=1e-14):
            raise ZeroDivisionError("La dérivée est trop proche de zéro.")
        suivant = x - fonction(x) / pente
        if abs(suivant - x) <= tolerance * max(1.0, abs(suivant)):
            return suivant, tour
        x = suivant
    raise RuntimeError("La méthode de Newton n'a pas convergé.")


def tests():
    polynome = [2, 3, 0, 5]
    assert evaluer_naif(polynome, 2) == 48
    assert evaluer(polynome, 2) == 48
    assert evaluer(polynome, 0) == 2
    assert evaluer([], 3) == 0
    assert all(math.isclose(evaluer_naif(polynome, x), evaluer(polynome, x), rel_tol=1e-12, abs_tol=1e-12)
               for x in (-2, 0, 1, 2, 10))
    assert deriver(polynome) == [3, 0, 15]
    assert deriver([7]) == []
    assert deriver([]) == []
    racine = dichotomie(lambda x: x * x - 2, 0, 2)
    assert abs(racine - math.sqrt(2)) < 1e-10
    assert math.isclose(dichotomie(lambda x: x - 3, 0, 5), 3, abs_tol=1e-12)
    racine_newton, tours = newton([-2, 0, 1], 1)
    assert abs(racine_newton - math.sqrt(2)) < 1e-10
    assert tours < 10
    assert newton_trace([2, -2, 0, 1], 0, 6) == [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
    assert abs(integrer_rectangles(lambda x: x, 0, 1, 10000) - 0.5) < 1e-4
    assert somme([1, 2], [0, 0, 3]) == [1, 2, 3]
    assert produit_poly([1, 1], [1, 1]) == [1, 2, 1]
    assert produit_poly([-1, 1], [1, 1]) == [-1, 0, 1]
    binome = [1]
    for _ in range(10):
        binome = produit_poly(binome, [1, 1])
    assert binome == [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]
    assert abs(derivee_centree(math.sin, 1, 1e-5) - math.cos(1)) < 1e-9
    assert abs(rectangles(lambda x: x*x, 0, 1, 1000) - 1/3) < 0.001
    assert abs(trapezes(lambda x: x*x, 0, 1, 1000) - 1/3) < 1e-6
    assert abs(simpson(lambda x: x*x, 0, 1, 10) - 1/3) < 1e-14
    assert abs(simpson(lambda x: 4/(1+x*x), 0, 1, 1000) - math.pi) < 1e-12
    assert abs(newton_general(lambda x: math.cos(x)-x, 0.5)[0] - 0.7390851332) < 1e-9
    for fonction in (
        lambda: dichotomie(lambda x: x * x + 1, -1, 1),
        lambda: newton([1, 0, 1], 0),
        lambda: integrer_rectangles(lambda x: x, 0, 1, 0),
    ):
        try:
            fonction()
        except (ValueError, ZeroDivisionError):
            pass
        else:
            raise AssertionError("Une entrée invalide aurait dû provoquer une erreur.")


if __name__ == "__main__":
    polynome = [2, 3, 0, 5]
    print("Évaluation naïve et Horner :")
    for valeur in (-2, 0, 1, 2, 10):
        print(valeur, evaluer_naif(polynome, valeur), evaluer(polynome, valeur))
    print("Dérivée :", deriver(polynome))
    for degre in (1000, 5000, 20000):
        polynome_test = [1] * (degre + 1)
        debut = time.perf_counter()
        valeur_naive = evaluer_naif(polynome_test, 1.0001)
        temps_naif = time.perf_counter() - debut
        debut = time.perf_counter()
        valeur_horner = evaluer(polynome_test, 1.0001)
        temps_horner = time.perf_counter() - debut
        print(f"Degré {degre}: naïf {temps_naif:.6f} s | Horner {temps_horner:.6f} s | écart {abs(valeur_naive-valeur_horner):.3e}")
    print("Dichotomie de x² - 2 :", dichotomie(lambda x: x * x - 2, 0, 2))
    print("Newton pour x³ - 2x - 5 :", newton([-5, -2, 0, 1], 2))
    print("Trajet de Newton dans le cas cyclique :", newton_trace([2, -2, 0, 1], 0, 8))
    print("Somme et produit de polynômes :", somme([1, 2], [0, 0, 3]), produit_poly([1, 1], [1, 1]))
    print("Dérivée numérique centrée de sin en 1 :", derivee_centree(math.sin, 1, 1e-6))
    for subdivisions in (10, 100, 1000):
        print(f"n={subdivisions}: rectangles={rectangles(lambda x: x*x, 0, 1, subdivisions):.10f} | trapèzes={trapezes(lambda x: x*x, 0, 1, subdivisions):.10f} | Simpson={simpson(lambda x: x*x, 0, 1, subdivisions):.10f}")
    print("Approximation de pi par Simpson :", simpson(lambda x: 4/(1+x*x), 0, 1, 1000))
    print("Newton général pour cos(x)-x :", newton_general(lambda x: math.cos(x)-x, 0.5))
    try:
        import matplotlib.pyplot as plt
        valeurs_x = [indice / 100 for indice in range(-300, 301)]
        valeurs_y = [evaluer(polynome, x) for x in valeurs_x]
        plt.plot(valeurs_x, valeurs_y)
        plt.axhline(0)
        plt.grid(True)
        plt.title("Représentation du polynôme")
        plt.xlabel("x")
        plt.ylabel("P(x)")
        plt.show()
    except ImportError:
        print("Matplotlib n'est pas installé : le tracé est ignoré.")
    tests()
    print("Tous les tests du TP3 sont réussis.")
