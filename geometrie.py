"""Modèle géométrique et détection des collisions."""

from dataclasses import dataclass
import math

from matrices import (
    inverser_matrice,
    matrice_homogene,
    rotation_totale,
    transformer_point,
)


@dataclass(frozen=True)
class Point:
    x: float
    y: float
    z: float

    def __str__(self) -> str:
        return f"({self.x:.4g}, {self.y:.4g}, {self.z:.4g})"


@dataclass(frozen=True)
class Boite:
    nom: str
    centre: Point
    largeur: float
    profondeur: float
    hauteur: float
    angle_x: float = 0.0
    angle_y: float = 0.0
    angle_z: float = 0.0

    def __post_init__(self) -> None:
        if min(self.largeur, self.profondeur, self.hauteur) <= 0:
            raise ValueError("Les dimensions de la boîte doivent être positives.")

    @property
    def demi_dimensions(self) -> tuple[float, float, float]:
        return self.largeur / 2, self.profondeur / 2, self.hauteur / 2

    def matrice_locale_vers_monde(self) -> list[list[float]]:
        rotation = rotation_totale(self.angle_x, self.angle_y, self.angle_z)
        return matrice_homogene(
            rotation, (self.centre.x, self.centre.y, self.centre.z)
        )


def distance_boite_alignee(
    point: tuple[float, float, float],
    demi_dimensions: tuple[float, float, float],
) -> float:
    """Distance minimale d'un point à une boîte centrée sur l'origine."""
    dx = max(abs(point[0]) - demi_dimensions[0], 0.0)
    dy = max(abs(point[1]) - demi_dimensions[1], 0.0)
    dz = max(abs(point[2]) - demi_dimensions[2], 0.0)
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def distance_point_boite(point: Point, boite: Boite) -> float:
    """Convertit le point mondial en local, puis calcule la distance."""
    transformation = boite.matrice_locale_vers_monde()
    inverse = inverser_matrice(transformation)
    local = transformer_point(inverse, (point.x, point.y, point.z))
    return distance_boite_alignee(local, boite.demi_dimensions)


def classifier_distance(distance: float, marge: float, epsilon: float = 1e-9) -> str:
    """Classe un résultat selon une tolérance numérique explicite."""
    if distance <= epsilon:
        return "COLLISION"
    if distance <= marge + epsilon:
        return "PROXIMITÉ"
    return "SÛR"


def analyser_point(point: Point, boites: list[Boite], marge: float) -> list[dict]:
    if marge < 0:
        raise ValueError("La marge de sécurité ne peut pas être négative.")
    resultats = []
    for boite in boites:
        distance = distance_point_boite(point, boite)
        resultats.append(
            {
                "nom": boite.nom,
                "distance": distance,
                "etat": classifier_distance(distance, marge),
            }
        )
    return resultats
