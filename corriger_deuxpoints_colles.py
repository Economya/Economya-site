#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du bug de formatage "Titre :sous-titre" sans espace après les
deux-points — bug répandu trouvé sur 480 occurrences à travers le site
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Le motif " :X" (espace, deux-points, lettre directement collée, sans
espace) est corrigé en " : X" (espace ajouté après les deux-points).

Sécurité : ne touche QUE le motif [lettre/espace] + espace + : + lettre
(pas de chiffres autour, donc les heures comme "12:30" ne sont jamais
concernées puisqu'il n'y a pas d'espace avant le ":" dans ce cas).

Idempotent. Une seule sauvegarde globale en .bak_colonfix par fichier
modifié.

Usage :
    python3 corriger_deuxpoints_colles.py
"""

import os
import re
import glob

# Motif : espace + ':' + lettre (sans espace) -> espace + ':' + espace + lettre
PATTERN = re.compile(r' :([a-zà-ÿA-ZÀ-Ÿ])')


def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    nouveau_contenu, nb_remplacements = PATTERN.subn(r' : \1', contenu)

    if nb_remplacements == 0:
        return 0

    with open(chemin + ".bak_colonfix", 'w', encoding='utf-8') as f:
        f.write(contenu)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    return nb_remplacements


def main():
    fichiers = sorted(glob.glob("article-*.html"))
    total_fichiers = 0
    total_remplacements = 0

    for fichier in fichiers:
        nb = traiter_fichier(fichier)
        if nb > 0:
            total_fichiers += 1
            total_remplacements += nb

    print(f"=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Espaces ajoutés après ':' : {total_remplacements}")


if __name__ == "__main__":
    main()
