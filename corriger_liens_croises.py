#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des liens croisés datés (texte "APL 2025" etc. dans les grilles
de liens en bas d'articles, désynchronisé des articles déjà corrigés)
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Cible précisément : "(APL|RSA|CPF|Allocations familiales|Prime naissance|
Congé parental|Chômage ARE|Prime d'activité|Bonus écologique|Malus
écologique) 2025" -> "... 2026"

Ne touche PAS aux autres mentions de "2025" sans rapport avec ces 10
dispositifs (dates dans d'autres contextes, autres sujets).

Idempotent. Sauvegarde en .bak_liens_croises avant modification.

Usage :
    python3 corriger_liens_croises.py
"""

import os
import re
import glob

PATTERN = re.compile(
    r"(APL|RSA|CPF|Allocations familiales|Prime naissance|Congé parental|"
    r"Chômage ARE|Prime d'activité|Bonus écologique|Malus écologique) 2025"
)


def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    nb_matches = len(PATTERN.findall(contenu))
    if nb_matches == 0:
        return None

    contenu_corrige = PATTERN.sub(r"\1 2026", contenu)

    with open(chemin + ".bak_liens_croises", 'w', encoding='utf-8') as f:
        f.write(contenu)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu_corrige)

    return nb_matches


def main():
    fichiers = sorted(glob.glob("article-*.html"))
    total_fichiers = 0
    total_remplacements = 0

    for fichier in fichiers:
        resultat = traiter_fichier(fichier)
        if resultat:
            total_fichiers += 1
            total_remplacements += resultat

    print(f"=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Liens corrigés au total : {total_remplacements}")
    print(f"Sauvegardes créées avec l'extension .bak_liens_croises")


if __name__ == "__main__":
    main()
