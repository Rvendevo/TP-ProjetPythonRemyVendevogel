from collections import Counter
import math
import unicodedata


def nettoyer(texte):
    texte = unicodedata.normalize("NFD", texte.upper())
    resultat = []
    for caractere in texte:
        if unicodedata.category(caractere) == "Mn":
            continue
        if "A" <= caractere <= "Z":
            resultat.append(caractere)
    return "".join(resultat)


def lettre_vers_nombre(c):
    if len(c) != 1 or not "A" <= c <= "Z":
        raise ValueError("Une lettre majuscule de A à Z est attendue.")
    return ord(c) - ord("A")


def nombre_vers_lettre(n):
    return chr(n % 26 + ord("A"))


def pgcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def euclide_etendu(a, b):
    if b == 0:
        if a < 0:
            return -a, -1, 0
        return a, 1, 0
    resultat, u, v = euclide_etendu(b, a % b)
    return resultat, v, u - (a // b) * v


def inverse_modulaire(a, modulo):
    resultat, coefficient, _ = euclide_etendu(a, modulo)
    if resultat != 1:
        raise ValueError("La clé ne possède pas d'inverse modulo 26.")
    return coefficient % modulo


def cles_valides():
    return [a for a in range(1, 26) if pgcd(a, 26) == 1]


def chiffrer(texte, a, b):
    if a not in cles_valides():
        raise ValueError("Le paramètre a doit être premier avec 26.")
    resultat = []
    for caractere in nettoyer(texte):
        nombre = lettre_vers_nombre(caractere)
        resultat.append(nombre_vers_lettre((a * nombre + b) % 26))
    return "".join(resultat)


def dechiffrer(texte, a, b):
    inverse = inverse_modulaire(a, 26)
    resultat = []
    for caractere in nettoyer(texte):
        nombre = lettre_vers_nombre(caractere)
        resultat.append(nombre_vers_lettre(inverse * (nombre - b) % 26))
    return "".join(resultat)


def toutes_les_clefs(secret):
    return [(a, b, dechiffrer(secret, a, b)) for a in cles_valides() for b in range(26)]


def candidats_frequences(secret, nombre_lettres=3):
    texte = nettoyer(secret)
    if not texte:
        return []
    frequences = Counter(texte).most_common(nombre_lettres)
    lettres_francaises = "EASINTR"
    candidats = []
    for lettre_chiffree, _ in frequences:
        cible = lettre_vers_nombre(lettre_chiffree)
        for lettre_claire in lettres_francaises:
            numero_clair = lettre_vers_nombre(lettre_claire)
            for a in cles_valides():
                b = (cible - a * numero_clair) % 26
                cle = (a, b)
                if cle not in [(c[0], c[1]) for c in candidats]:
                    candidats.append((a, b, dechiffrer(texte, a, b)))
    return candidats


def score_francais(texte):
    frequences = {
        "E": 0.147, "A": 0.076, "S": 0.079, "I": 0.075, "N": 0.071,
        "T": 0.072, "R": 0.066, "U": 0.063, "L": 0.055, "O": 0.053,
        "D": 0.036, "C": 0.032, "M": 0.026, "P": 0.030, "V": 0.016,
        "Q": 0.013, "F": 0.011, "B": 0.009, "G": 0.010, "H": 0.010,
        "J": 0.003, "X": 0.004, "Y": 0.003, "Z": 0.003, "K": 0.001,
        "W": 0.001
    }
    texte = nettoyer(texte)
    if not texte:
        return float("-inf")
    comptes = Counter(texte)
    return sum((comptes[lettre] / len(texte)) * math.log(probabilite)
               for lettre, probabilite in frequences.items())


def casser_par_frequences(secret):
    candidats = candidats_frequences(secret, 5)
    if not candidats:
        return None
    return max(candidats, key=lambda candidat: score_francais(candidat[2]))



def indice_coincidence(texte):
    texte = nettoyer(texte)
    longueur = len(texte)
    if longueur < 2:
        return 0.0
    comptes = Counter(texte)
    return sum(nombre * (nombre - 1) for nombre in comptes.values()) / (longueur * (longueur - 1))


def vigenere(texte, cle):
    texte = nettoyer(texte)
    cle = nettoyer(cle)
    if not cle:
        raise ValueError("La clé doit contenir au moins une lettre.")
    resultat = []
    for indice, caractere in enumerate(texte):
        decalage = lettre_vers_nombre(cle[indice % len(cle)])
        resultat.append(nombre_vers_lettre(lettre_vers_nombre(caractere) + decalage))
    return "".join(resultat)


def indices_par_longueur(texte, longueur_max=7):
    texte = nettoyer(texte)
    resultats = {}
    for longueur in range(1, longueur_max + 1):
        colonnes = [texte[indice::longueur] for indice in range(longueur)]
        resultats[longueur] = sum(indice_coincidence(colonne) for colonne in colonnes) / longueur
    return resultats


def tests():
    assert lettre_vers_nombre("C") == 2
    assert nombre_vers_lettre(2) == "C"
    assert all(nombre_vers_lettre(lettre_vers_nombre(c)) == c for c in "ABCXYZ")
    assert nettoyer("À l'été, déjà !") == "ALETEDEJA"
    assert len(cles_valides()) == 12
    assert chiffrer("ATTAQUEALAUBE", 5, 8) == "IZZIKECILIENC"
    message = nettoyer("Attaque à l'aube")
    secret = chiffrer(message, 5, 8)
    assert dechiffrer(secret, 5, 8) == message
    assert len(toutes_les_clefs(secret)) == 312
    texte_long = nettoyer("Le chiffrement affine est un chiffrement par substitution monoalphabetique. Chaque lettre du message est remplacee par une autre lettre, toujours la meme, ce qui laisse intactes les frequences relatives des lettres et permet de casser le code sans essayer toutes les clefs possibles.")
    secret_long = chiffrer(texte_long, 7, 12)
    assert math.isclose(indice_coincidence(texte_long), indice_coincidence(secret_long), abs_tol=1e-12)
    secret_vigenere = vigenere(texte_long, "CLE")
    assert len(secret_vigenere) == len(texte_long)
    assert len(indices_par_longueur(secret_vigenere, 7)) == 7
    assert inverse_modulaire(5, 26) == 21
    assert casser_par_frequences(chiffrer(
        "Le chiffrement affine est un chiffrement par substitution monoalphabetique. "
        "Chaque lettre du message est remplacee par une autre lettre, toujours la meme, "
        "ce qui laisse intactes les frequences relatives des lettres et permet de casser "
        "le code sans essayer toutes les clefs possibles.", 7, 12
    ))[:2] == (7, 12)
    for fonction in (
        lambda: lettre_vers_nombre("AB"),
        lambda: chiffrer("TEST", 4, 7),
        lambda: dechiffrer("TEST", 4, 7),
    ):
        try:
            fonction()
        except ValueError:
            pass
        else:
            raise AssertionError("Une entrée invalide aurait dû provoquer une erreur.")


if __name__ == "__main__":
    message = nettoyer("Attaque à l'aube")
    cle_a, cle_b = 5, 8
    secret = chiffrer(message, cle_a, cle_b)
    print("Message nettoyé :", message)
    print("Message chiffré :", secret)
    print("Clés valides pour a :", cles_valides())
    print("Inverse de 5 modulo 26 :", inverse_modulaire(5, 26))
    print("Message déchiffré :", dechiffrer(secret, cle_a, cle_b))
    essais = toutes_les_clefs(secret)
    print("Nombre de clés essayées :", len(essais))
    print("Clé retrouvée par comparaison :", [(a, b) for a, b, texte in essais if texte == message])
    texte_long = nettoyer(
        "Le chiffrement affine est un chiffrement par substitution monoalphabetique. "
        "Chaque lettre du message est remplacee par une autre lettre, toujours la meme, "
        "ce qui laisse intactes les frequences relatives des lettres et permet de casser "
        "le code sans essayer toutes les clefs possibles."
    )
    secret_long = chiffrer(texte_long, 7, 12)
    print("Candidat par fréquences :", casser_par_frequences(secret_long))
    hasard = "".join(__import__("random").choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(len(texte_long)))
    print("Indice de coïncidence clair/chiffré/hasard :", indice_coincidence(texte_long), indice_coincidence(secret_long), indice_coincidence(hasard))
    secret_vigenere = vigenere(texte_long, "CLE")
    print("Vigenère, début du texte :", secret_vigenere[:40])
    print("Indice de coïncidence Vigenère :", indice_coincidence(secret_vigenere))
    print("Indices selon les longueurs possibles :", indices_par_longueur(secret_vigenere, 7))
    tests()
    print("Tous les tests du TP5 sont réussis.")
