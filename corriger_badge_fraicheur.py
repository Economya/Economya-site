#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mise à jour du badge de fraîcheur "Vérifié [mois] 2025" -> "Vérifié juin 2026"
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Cible les 3 variantes trouvées : "Vérifié mai 2025", "Vérifié juin 2025",
"Vérifié en 2025" -> toutes remplacées par "Vérifié juin 2026".

Remplacement simple de texte, aucun chiffre/donnée factuelle touché —
risque minimal.

Idempotent. Sauvegarde en .bak_badge avant modification.

Usage :
    python3 corriger_badge_fraicheur.py
"""

import os
import glob

VARIANTES = [
    "Vérifié mai 2025",
    "Vérifié juin 2025",
    "Vérifié en 2025",
]

NOUVEAU = "Vérifié juin 2026"


def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    modifie = False

    for variante in VARIANTES:
        if variante in contenu:
            contenu = contenu.replace(variante, NOUVEAU)
            modifie = True

    if not modifie:
        return False

    with open(chemin + ".bak_badge", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu)

    return True


def main():
    fichiers = sorted(glob.glob("article-*.html"))
    total_modifies = 0

    for fichier in fichiers:
        if traiter_fichier(fichier):
            total_modifies += 1

    print(f"=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_modifies}")
    print(f"Sauvegardes créées avec l'extension .bak_badge")


if __name__ == "__main__":
    main()
