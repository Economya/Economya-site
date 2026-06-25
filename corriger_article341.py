#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-341.html — SCPI : dates 2025->2026
À lancer depuis ~/Desktop/mon site

Rendement moyen SCPI confirmé stable en 2026 (ASPIM officiel : 4,91% en
2025, projections 2026 dans la même fourchette 4,5-5%) — le "4-5%" de
l'article reste globalement exact, seules les dates sont mises à jour.
Les rendements SCPI nommés (étiquetés "(2024)") sont déjà correctement
datés et inchangés.

Idempotent. Sauvegarde en .bak_art341.

Usage :
    python3 corriger_article341.py
"""

import os

FICHIER = "article-341.html"

REMPLACEMENTS = [
    (
        "SCPI : guide complet 2025 — Immobilier dès 200€. Guide complet sur Economya.fr",
        "SCPI : guide complet 2026 — Immobilier dès 200€. Guide complet sur Economya.fr",
    ),
    (
        "<title>SCPI : guide complet 2025 — Economya.fr</title>",
        "<title>SCPI : guide complet 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "SCPI : guide complet 2025",',
        '"headline": "SCPI : guide complet 2026",',
    ),
    (
        '<meta property="og:title" content="SCPI : guide complet 2025">',
        '<meta property="og:title" content="SCPI : guide complet 2026">',
    ),
    (
        '<meta name="twitter:title" content="SCPI : guide complet 2025">',
        '<meta name="twitter:title" content="SCPI : guide complet 2026">',
    ),
    (
        "<h1>SCPI :<br><em>guide complet 2025</em></h1>",
        "<h1>SCPI :<br><em>guide complet 2026</em></h1>",
    ),
    (
        "Les SCPI (Sociétés Civiles de Placement Immobilier) permettent d'investir dans l'immobilier professionnel (bureaux, commerces, entrepôts, santé) dès 200 €, sans gérer de locataires. Avec un rendement moyen de 4 à 5 % en 2025, elles offrent une alternative solide entre le Livret A et la Bourse.",
        "Les SCPI (Sociétés Civiles de Placement Immobilier) permettent d'investir dans l'immobilier professionnel (bureaux, commerces, entrepôts, santé) dès 200 €, sans gérer de locataires. Avec un rendement moyen de 4,5 à 5 % en 2026 (4,91% en moyenne selon l'ASPIM en 2025), elles offrent une alternative solide entre le Livret A et la Bourse.",
    ),
    (
        '<span class="stat-num">4–5 %</span><span class="stat-lbl">rendement moyen SCPI 2025</span>',
        '<span class="stat-num">4,5–5 %</span><span class="stat-lbl">rendement moyen SCPI 2026</span>',
    ),
    (
        "🏆 Les SCPI les plus recommandées en 2025",
        "🏆 Les SCPI les plus recommandées en 2026",
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

    with open(FICHIER + ".bak_art341", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026, rendement affine a 4,5-5% (ASPIM 4,91% 2025)")


if __name__ == "__main__":
    main()
