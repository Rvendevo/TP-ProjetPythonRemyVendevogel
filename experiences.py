"""Expériences comparatives reproductibles pour le projet."""

import math
import random
import time

from geometrie import Boite, Point, distance_point_boite, classifier_distance
from matrices import inverser_matrice, matrice_homogene, rotation_totale, transformer_point


def experience_validation() -> None:
    print("\nEXPÉRIENCE 1 — Validation géométrique")
    boite = Boite("boite_test", Point(0, 0, 0), 2, 2, 2)
    cas = [
        ("centre", Point(0, 0, 0), 0.0),
        ("intérieur", Point(0.5, 0.5, 0.5), 0.0),
        ("sur une face", Point(1, 0, 0), 0.0),
        ("à 0.5 m d'une face", Point(1.5, 0, 0), 0.5),
        ("à 1 m d'une arête", Point(1.5, 1.5, 0), math.sqrt(0.5)),
        ("à l'extérieur en diagonale", Point(2, 2, 2), math.sqrt(3)),
    ]
    erreurs = 0
    for nom, point, attendu in cas:
        obtenu = distance_point_boite(point, boite)
        correct = math.isclose(obtenu, attendu, rel_tol=1e-9, abs_tol=1e-9)
        erreurs += not correct
        print(
            f"- {nom:28} distance attendue={attendu:.6f}, "
            f"obtenue={obtenu:.6f} : {'OK' if correct else 'ÉCHEC'}"
        )
    print(f"Bilan : {len(cas) - erreurs}/{len(cas)} tests réussis.")


def experience_marge() -> None:
    print("\nEXPÉRIENCE 2 — Effet de la marge de sécurité")
    boite = Boite("boite", Point(0, 0, 0), 2, 2, 2)
    points = [
        ("contact", Point(1, 0, 0)),
        ("proche", Point(1.08, 0, 0)),
        ("moyennement loin", Point(1.2, 0, 0)),
        ("loin", Point(2, 0, 0)),
    ]
    for marge in (0.05, 0.10, 0.30):
        print(f"\nMarge = {marge:.2f} m")
        for nom, point in points:
            distance = distance_point_boite(point, boite)
            print(
                f"  {nom:20} d={distance:.4f} m -> "
                f"{classifier_distance(distance, marge)}"
            )


def experience_rotation() -> None:
    print("\nEXPÉRIENCE 3 — Effet de la rotation")
    print("La référence est la distance au volume orienté, calculée dans son repère local.")
    angles = (0, 15, 30, 45, 60, 90)
    point = Point(1.5, 0.0, 0.0)
    for angle in angles:
        boite = Boite("test", Point(0, 0, 0), 2, 1, 1, 0, 0, angle)
        distance = distance_point_boite(point, boite)
        print(f"  rotation Z={angle:>3}° -> distance = {distance:.6f} m")
    print("Interprétation : la distance peut changer car le volume tourne,")
    print("alors que le point du contrôleur reste fixe dans le repère mondial.")


def experience_flottants() -> None:
    print("\nEXPÉRIENCE 4 — Précision numérique près d'une limite")
    limite = 1.0
    valeurs = [
        1.0,
        1.0 - 1e-12,
        1.0 + 1e-12,
        1.0 - 1e-9,
        1.0 + 1e-9,
        0.1 + 0.2,
    ]
    print(f"Limite de face : x = {limite:.17f}")
    for x in valeurs:
        ecart = x - limite
        print(f"  x={x:.17f} ; écart={ecart:+.17g}")
    print("\nExemple classique : 0.1 + 0.2 n'est généralement pas exactement 0.3")
    print(f"  0.1 + 0.2 = {0.1 + 0.2:.17f}")
    print(f"  différence avec 0.3 = {(0.1 + 0.2) - 0.3:+.17g}")
    print("À discuter : une tolérance epsilon stabilise la décision près d'une limite,")
    print("mais sa valeur doit être choisie et justifiée selon l'échelle du problème.")


def experience_matrices() -> None:
    print("\nEXPÉRIENCE 5 — Vérification d'une transformation matricielle")
    rotation = rotation_totale(15, 25, 40)
    transformation = matrice_homogene(rotation, (2.0, -1.0, 0.5))
    inverse = inverser_matrice(transformation)
    point_local = (0.4, -0.2, 0.7)
    point_monde = transformer_point(transformation, point_local)
    retour_local = transformer_point(inverse, point_monde)
    erreurs = [abs(a - b) for a, b in zip(point_local, retour_local)]
    print(f"Point local initial : {point_local}")
    print(f"Point transformé    : {tuple(round(v, 8) for v in point_monde)}")
    print(f"Retour au local     : {tuple(round(v, 8) for v in retour_local)}")
    print(f"Erreur maximale     : {max(erreurs):.3e}")
    print("Une erreur très petite est attendue, mais pas nécessairement zéro exact.")


def experience_performance() -> None:
    print("\nEXPÉRIENCE 6 — Temps de calcul selon le nombre de boîtes")
    generateur = random.Random(2026)  # Graine fixe : expérience reproductible.
    point = Point(0.2, -0.3, 0.4)
    for nombre in (10, 100, 500, 1000):
        boites = [
            Boite(
                f"b{i}",
                Point(
                    generateur.uniform(-10, 10),
                    generateur.uniform(-10, 10),
                    generateur.uniform(-10, 10),
                ),
                generateur.uniform(0.2, 2.0),
                generateur.uniform(0.2, 2.0),
                generateur.uniform(0.2, 2.0),
                0,
                0,
                generateur.uniform(0, 180),
            )
            for i in range(nombre)
        ]
        debut = time.perf_counter()
        for boite in boites:
            distance_point_boite(point, boite)
        duree = time.perf_counter() - debut
        print(f"  {nombre:4} boîtes : {duree:.6f} seconde(s)")
    print("Les temps dépendent de la machine et de l'environnement d'exécution.")
    print("Répète plusieurs fois et compare plutôt les tendances que des valeurs isolées.")


def lancer_menu_experiences() -> None:
    while True:
        print("\n=== EXPÉRIENCES COMPARATIVES ===")
        print("1. Validation de la géométrie")
        print("2. Effet de la marge de sécurité")
        print("3. Effet de la rotation")
        print("4. Précision des flottants")
        print("5. Vérification des matrices")
        print("6. Temps de calcul selon le nombre de boîtes")
        print("7. Toutes les expériences")
        print("0. Retour au menu principal")
        choix = input("Ton choix : ").strip()
        actions = {
            "1": experience_validation,
            "2": experience_marge,
            "3": experience_rotation,
            "4": experience_flottants,
            "5": experience_matrices,
            "6": experience_performance,
        }
        if choix in actions:
            actions[choix]()
        elif choix == "7":
            for action in actions.values():
                action()
        elif choix == "0":
            break
        else:
            print("Choix inconnu.")
