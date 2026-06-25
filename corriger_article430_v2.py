#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-430.html — incohérence interne du barème + dates
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE : le tableau du barème IR était INCOHÉRENT en interne — une
ligne avait déjà le bon seuil 2026 (29 579-84 577€) pendant que les lignes
voisines avaient encore d'anciens seuils (11 497€, 29 315€, 83 823€,
180 294€), créant un trou non couvert entre 29 315€ et 29 579€.

Barème 2026 correct et cohérent (déjà confirmé ailleurs sur le site) :
0-11 600 (0%) / 11 600-29 579 (11%) / 29 579-84 577 (30%) /
84 577-181 917 (41%) / au-delà de 181 917 (45%).

Idempotent. Sauvegarde en .bak_art430v2.

Usage :
    python3 corriger_article430_v2.py
"""

import os

FICHIER = "article-430.html"

REMPLACEMENTS = [
    (
        "Seuils de revenus : impôts et aides en 2025 — Ne dépassez pas les plafonds clés. Guide complet sur Economya.fr",
        "Seuils de revenus : impôts et aides en 2026 — Ne dépassez pas les plafonds clés. Guide complet sur Economya.fr",
    ),
    (
        "<title>Seuils de revenus : impôts et aides en 2025 — Economya.fr</title>",
        "<title>Seuils de revenus : impôts et aides en 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Seuils de revenus : impôts et aides en 2025",',
        '"headline": "Seuils de revenus : impôts et aides en 2026",',
    ),
    (
        '<meta property="og:title" content="Seuils de revenus : impôts et aides en 2025">',
        '<meta property="og:title" content="Seuils de revenus : impôts et aides en 2026">',
    ),
    (
        '<meta name="twitter:title" content="Seuils de revenus : impôts et aides en 2025">',
        '<meta name="twitter:title" content="Seuils de revenus : impôts et aides en 2026">',
    ),
    (
        "<h1>Seuils de revenus :<br><em>impôts et aides en 2025</em></h1>",
        "<h1>Seuils de revenus :<br><em>impôts et aides en 2026</em></h1>",
    ),
    (
        "📊 Les seuils d'imposition 2025 (barème IR)",
        "📊 Les seuils d'imposition 2026 (barème IR)",
    ),
    (
        '<tr><td>0 à 11 497 €</td><td class="g">0 %</td><td>Non imposable — aucun IR à payer</td></tr>',
        '<tr><td>0 à 11 600 €</td><td class="g">0 %</td><td>Non imposable — aucun IR à payer</td></tr>',
    ),
    (
        '<tr><td>11 497 à 29 315 €</td><td class="o">11 %</td><td>1ère tranche imposable</td></tr>',
        '<tr><td>11 600 à 29 579 €</td><td class="o">11 %</td><td>1ère tranche imposable</td></tr>',
    ),
    (
        '<tr><td>83 823 à 180 294 €</td><td class="r">41 %</td><td>Hauts revenus</td></tr>',
        '<tr><td>84 577 à 181 917 €</td><td class="r">41 %</td><td>Hauts revenus</td></tr>',
    ),
    (
        '<tr><td>Au-delà de 180 294 €</td><td class="r">45 %</td><td>Très hauts revenus</td></tr>',
        '<tr><td>Au-delà de 181 917 €</td><td class="r">45 %</td><td>Très hauts revenus</td></tr>',
    ),
    (
        "Les seuils fiscaux changent chaque année au moment de la loi de finances. Les montants indiqués sont ceux de 2025 mais peuvent être révisés.",
        "Les seuils fiscaux changent chaque année au moment de la loi de finances. Les montants indiqués sont ceux de 2026 mais peuvent être révisés.",
    ),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    for ancien, nouveau in REMPLACEMENTS:
        if nouveau in contenu and ancien not in contenu:
            continue
        if ancien in contenu:
            contenu = contenu.replace(ancien, nouveau)
            nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou textes attendus non trouvés.")
        return

    with open(FICHIER + ".bak_art430v2", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Bareme IR rendu coherent (11600/29579/84577/181917), dates 2026")


if __name__ == "__main__":
    main()
