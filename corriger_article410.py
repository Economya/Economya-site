#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-410.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

Les tarifs commerciaux précis par néobanque (0-15€/mois, 0-17,99€/mois,
etc.) ne sont PAS modifiés ici — ce sont des prix qui évoluent fréquemment
par établissement, hors périmètre vérifiable dans cette session sans
recherche dédiée par banque. La garantie FGDR (100 000€) est un montant
réglementé stable au niveau européen, inchangé. Seules les dates sont
corrigées.

Idempotent. Sauvegarde en .bak_art410.

Usage :
    python3 corriger_article410.py
"""

import os

FICHIER = "article-410.html"

REMPLACEMENTS = [
    (
        "Néobanques 2025 : le comparatif complet — Zéro frais, cashback, assurances. Guide complet sur Economya.fr",
        "Néobanques 2026 : le comparatif complet — Zéro frais, cashback, assurances. Guide complet sur Economya.fr",
    ),
    (
        "<title>Néobanques 2025 : le comparatif complet — Economya.fr</title>",
        "<title>Néobanques 2026 : le comparatif complet — Economya.fr</title>",
    ),
    (
        '"headline": "Néobanques 2025 : le comparatif complet",',
        '"headline": "Néobanques 2026 : le comparatif complet",',
    ),
    (
        '<meta property="og:title" content="Néobanques 2025 : le comparatif complet">',
        '<meta property="og:title" content="Néobanques 2026 : le comparatif complet">',
    ),
    (
        '<meta name="twitter:title" content="Néobanques 2025 : le comparatif complet">',
        '<meta name="twitter:title" content="Néobanques 2026 : le comparatif complet">',
    ),
    (
        "<h1>Néobanques 2025 :<br><em>le comparatif complet</em></h1>",
        "<h1>Néobanques 2026 :<br><em>le comparatif complet</em></h1>",
    ),
    (
        "Voici le comparatif 2025 pour choisir celle qui vous correspond.",
        "Voici le comparatif 2026 pour choisir celle qui vous correspond.",
    ),
    (
        "Moins riche fonctionnellement en 2025 qu'auparavant suite à des refontes.",
        "Moins riche fonctionnellement en 2026 qu'auparavant suite à des refontes.",
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

    with open(FICHIER + ".bak_art410", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026 (tarifs neobanques non verifies - hors perimetre)")


if __name__ == "__main__":
    main()
