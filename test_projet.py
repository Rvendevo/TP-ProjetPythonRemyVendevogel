"""Tests automatisés du projet. Lancer avec : python -m unittest."""

import math
import unittest

from geometrie import Boite, Point, distance_point_boite, classifier_distance
from matrices import inverser_matrice, matrice_homogene, rotation_totale, transformer_point


class TestsGeometrie(unittest.TestCase):
    def setUp(self):
        self.boite = Boite("test", Point(0, 0, 0), 2, 2, 2)

    def test_point_dans_boite(self):
        self.assertAlmostEqual(distance_point_boite(Point(0.2, 0.3, 0.4), self.boite), 0.0)

    def test_point_sur_surface(self):
        self.assertAlmostEqual(distance_point_boite(Point(1, 0, 0), self.boite), 0.0)

    def test_distance_face(self):
        self.assertAlmostEqual(distance_point_boite(Point(1.5, 0, 0), self.boite), 0.5)

    def test_distance_diagonale(self):
        self.assertAlmostEqual(
            distance_point_boite(Point(2, 2, 0), self.boite), math.sqrt(2)
        )

    def test_classification(self):
        self.assertEqual(classifier_distance(0.0, 0.2), "COLLISION")
        self.assertEqual(classifier_distance(0.1, 0.2), "PROXIMITÉ")
        self.assertEqual(classifier_distance(0.5, 0.2), "SÛR")

    def test_rotation_90_degres(self):
        boite = Boite("tournee", Point(0, 0, 0), 2, 1, 1, 0, 0, 90)
        self.assertAlmostEqual(distance_point_boite(Point(0, 0.75, 0), boite), 0.0, places=8)

    def test_transformation_inverse(self):
        t = matrice_homogene(rotation_totale(10, 20, 30), (1, 2, 3))
        inverse = inverser_matrice(t)
        point = (0.3, -0.4, 0.8)
        monde = transformer_point(t, point)
        retour = transformer_point(inverse, monde)
        for a, b in zip(point, retour):
            self.assertAlmostEqual(a, b, places=9)


if __name__ == "__main__":
    unittest.main()
