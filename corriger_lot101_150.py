#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des dates 2025->2026 sur 4 fichiers (lot 101-150)
À lancer depuis ~/Desktop/mon site

Contenu générique sans chiffre substantiel à vérifier (outils gratuits,
forfaits mobiles, conseils CV, arnaques courantes). article-114 n'est
PAS modifié : sa statistique "200 milliards d'euros en 2024" est une
référence historique correctement datée, pas une erreur.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot101_150.py
"""

import os

REMPLACEMENTS = {
    "article-108.html": [
        (
            "Les meilleurs outils gratuits en 2025",
            "Les meilleurs outils gratuits en 2026",
        ),
    ],
    "article-113.html": [
        (
            "Comparatif des meilleurs forfaits à moins de 10 € (2025)",
            "Comparatif des meilleurs forfaits à moins de 10 € (2026)",
        ),
    ],
    "article-124.html": [
        (
            "C'est le budget nécessaire pour créer un CV professionnel et une lettre de motivation percutante en 2025 — à condition de savoir quels outils utiliser et quelles règles appliquer.",
            "C'est le budget nécessaire pour créer un CV professionnel et une lettre de motivation percutante en 2026 — à condition de savoir quels outils utiliser et quelles règles appliquer.",
        ),
    ],
    "article-147.html": [
        (
            "Les arnaques les plus répandues en 2025",
            "Les arnaques les plus répandues en 2026",
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
