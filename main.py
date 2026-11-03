"""Point d'entrée du projet Détecteur VR 3D."""

from geometrie import Boite, Point, analyser_point
from experiences import lancer_menu_experiences


def lire_nombre(message: str) -> float:
    """Lit un nombre flottant, en acceptant la virgule décimale."""
    while True:
        texte = input(message).strip().replace(",", ".")
        try:
            valeur = float(texte)
            if not math_is_finite(valeur):
                print("Entre une valeur numérique finie.")
                continue
            return valeur
        except ValueError:
            print("Valeur invalide. Exemple : 1.25")


def math_is_finite(valeur: float) -> bool:
    # Évite d'accepter NaN et les infinis dans les coordonnées.
    return valeur == valeur and valeur not in (float("inf"), float("-inf"))


def lire_entier(message: str, minimum: int = 0) -> int:
    while True:
        texte = input(message).strip()
        try:
            valeur = int(texte)
            if valeur < minimum:
                print(f"Entre un entier supérieur ou égal à {minimum}.")
                continue
            return valeur
        except ValueError:
            print("Entre un nombre entier valide.")


def creer_boite_interactive(numero: int) -> Boite:
    print(f"\n--- Création de la boîte {numero} ---")
    nom = input("Nom de l'objet : ").strip() or f"boite_{numero}"
    print("Position du centre (en mètres) :")
    centre = Point(
        lire_nombre("  x = "),
        lire_nombre("  y = "),
        lire_nombre("  z = "),
    )
    print("Dimensions complètes (largeur, profondeur, hauteur) en mètres :")
    while True:
        largeur = lire_nombre("  largeur = ")
        profondeur = lire_nombre("  profondeur = ")
        hauteur = lire_nombre("  hauteur = ")
        if largeur > 0 and profondeur > 0 and hauteur > 0:
            break
        print("Les trois dimensions doivent être strictement positives.")
    print("Rotation en degrés autour des axes X, Y et Z :")
    rx = lire_nombre("  angle X = ")
    ry = lire_nombre("  angle Y = ")
    rz = lire_nombre("  angle Z = ")
    return Boite(nom, centre, largeur, profondeur, hauteur, rx, ry, rz)


def afficher_boites(boites: list[Boite]) -> None:
    if not boites:
        print("Aucune boîte n'est définie.")
        return
    print("\nObjets de l'espace :")
    for boite in boites:
        print(
            f"- {boite.nom} : centre={boite.centre}, "
            f"dimensions=({boite.largeur:g}, {boite.profondeur:g}, "
            f"{boite.hauteur:g}) m, "
            f"rotation=({boite.angle_x:g}°, {boite.angle_y:g}°, "
            f"{boite.angle_z:g}°)"
        )


def analyser_interactif(boites: list[Boite]) -> None:
    if not boites:
        print("Crée d'abord au moins une boîte.")
        return
    print("\nPosition du contrôleur (en mètres) :")
    controleur = Point(
        lire_nombre("  x = "),
        lire_nombre("  y = "),
        lire_nombre("  z = "),
    )
    marge = lire_nombre("Marge de sécurité en mètres (ex. 0.25) : ")
    while marge < 0:
        print("La marge doit être positive ou nulle.")
        marge = lire_nombre("Marge de sécurité en mètres : ")

    resultats = analyser_point(controleur, boites, marge)
    print("\n=== Analyse du contrôleur ===")
    print(f"Position : {controleur}")
    print(f"Marge de sécurité : {marge:.6g} m")
    for resultat in resultats:
        distance = resultat["distance"]
        distance_texte = "0" if distance == 0 else f"{distance:.8g}"
        print(
            f"- {resultat['nom']}: {resultat['etat']} "
            f"(distance à la surface = {distance_texte} m)"
        )
    if resultats:
        plus_proche = min(resultats, key=lambda resultat: resultat["distance"])
        print(
            f"\nObjet le plus proche : {plus_proche['nom']} "
            f"({plus_proche['distance']:.8g} m)"
        )


def main() -> None:
    boites: list[Boite] = []
    while True:
        print("\n" + "=" * 52)
        print(" DÉTECTEUR DE COLLISION ET DE PROXIMITÉ VR — 3D")
        print("=" * 52)
        print("1. Ajouter une boîte")
        print("2. Afficher les boîtes")
        print("3. Analyser la position du contrôleur")
        print("4. Lancer les expériences comparatives")
        print("5. Charger une scène de démonstration")
        print("0. Quitter")
        choix = input("Ton choix : ").strip()

        if choix == "1":
            boites.append(creer_boite_interactive(len(boites) + 1))
            print("Boîte ajoutée.")
        elif choix == "2":
            afficher_boites(boites)
        elif choix == "3":
            analyser_interactif(boites)
        elif choix == "4":
            lancer_menu_experiences()
        elif choix == "5":
            boites = [
                Boite("cube_central", Point(0, 0, 0), 2, 2, 2),
                Boite("boite_tournee", Point(3, 0, 0), 2.5, 1.2, 2, 0, 0, 30),
                Boite("obstacle_haut", Point(0, 0, 3), 1, 1.5, 1.5, 0, 20, 0),
            ]
            print("Scène de démonstration chargée.")
        elif choix == "0":
            print("Fin du programme.")
            break
        else:
            print("Choix inconnu. Réessaie.")


if __name__ == "__main__":
    main()
