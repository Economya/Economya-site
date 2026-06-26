#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des dates 2025->2026 sur 4 fichiers (lot 306-325)
À lancer depuis ~/Desktop/mon site

article-308 : incohérence interne corrigée — le montant PreParE majoré
était déjà étiqueté "(2026)" juste au-dessus, mais le titre de section
disait encore "2025".

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot306_325.py
"""

import os

REMPLACEMENTS = {
    "article-306.html": [
        (
            "* Montants indicatifs 2025. Vérifiez les montants exacts sur caf.fr selon votre situation.",
            "* Montants indicatifs 2026. Vérifiez les montants exacts sur caf.fr selon votre situation.",
        ),
    ],
    "article-308.html": [
        (
            "📊 Récapitulatif PreParE 2025",
            "📊 Récapitulatif PreParE 2026",
        ),
    ],
    "article-318.html": [
        (
            "💶 Les montants par tranche d'âge (2025)",
            "💶 Les montants par tranche d'âge (2026)",
        ),
    ],
    "article-325.html": [
        (
            "🔧 Les appareils éligibles et les montants 2025",
            "🔧 Les appareils éligibles et les montants 2026",
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
