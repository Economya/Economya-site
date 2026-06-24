#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction SMIC obsolète — article-218.html et article-357.html
À lancer depuis ~/Desktop/mon site

SMIC actuel (depuis le 1er juin 2026) : 1 867,02 € brut mensuel
(au lieu de 1 801€, valeur novembre 2024 ; ou 1 766€, valeur début 2024).

1. article-218.html : exemple de calcul ARE recalculé en cascade
   (SMIC -> SJR -> ARE) : 1 801€ -> 1 867,02€, SJR 59,40€ -> 61,56€,
   résultat ~1 120€/mois -> ~1 141€/mois
2. article-357.html : SMIC brut 2025 ~1 766€ -> 2026 ~1 867€

Idempotent. Sauvegarde en .bak_smic.

Usage :
    python3 corriger_smic.py
"""

import os

REMPLACEMENTS = {
    "article-218.html": [
        (
            '<div class="simul-row"><span class="simul-lab">SMIC (1 801 € brut) — SJR = 59,40 €</span><span class="simul-val">≈ 1 120 €/mois</span></div>',
            '<div class="simul-row"><span class="simul-lab">SMIC (1 867 € brut) — SJR = 61,56 €</span><span class="simul-val">≈ 1 141 €/mois</span></div>',
        ),
    ],
    "article-357.html": [
        (
            "* SMIC brut 2025 : ~1 766 €. Les entreprises peuvent payer au-delà du minimum légal. Les salaires affichés sont les minimums.",
            "* SMIC brut 2026 : ~1 867 €. Les entreprises peuvent payer au-delà du minimum légal. Les salaires affichés sont les minimums.",
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

        with open(fichier + ".bak_smic", 'w', encoding='utf-8') as f:
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
