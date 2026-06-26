#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des dates 2025->2026 sur 3 fichiers (lot 481-500)
À lancer depuis ~/Desktop/mon site

Contenu générique (comparaison salariale, visas nomades digitaux,
badge de fraîcheur), pas de chiffre substantiel à vérifier.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot481_500.py
"""

import os

REMPLACEMENTS = {
    "article-481.html": [
        (
            "Équivalent France 2025",
            "Équivalent France 2026",
        ),
    ],
    "article-494.html": [
        (
            "+50 pays en 2025",
            "+50 pays en 2026",
        ),
    ],
    "article-500.html": [
        (
            "📅 Mai 2025",
            "📅 Juin 2026",
        ),
    ],
}


def main():
    total_fichiers = 0
    total_remplacements = 0

    for fichier, paires in REMPLACEMENTS.items():
        if not os.path.exists(fichier):
            print(f"❌ {fichier} introuvable, ignoré.")
            continue

        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()

        contenu_original = contenu
        nb_modifs_fichier = 0

        for ancien, nouveau in paires:
            if nouveau in contenu and ancien not in contenu:
                continue
            if ancien in contenu:
                contenu = contenu.replace(ancien, nouveau)
                nb_modifs_fichier += 1

        if nb_modifs_fichier == 0:
            print(f"✅ {fichier} : déjà corrigé ou texte non trouvé")
            continue

        ext = fichier.replace("article-", "").replace(".html", "")
        with open(fichier + f".bak_art{ext}", 'w', encoding='utf-8') as f:
            f.write(contenu_original)

        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)

        print(f"✅ {fichier} : {nb_modifs_fichier} remplacement(s)")
        total_fichiers += 1
        total_remplacements += nb_modifs_fichier

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Remplacements totaux : {total_remplacements}")


if __name__ == "__main__":
    main()
