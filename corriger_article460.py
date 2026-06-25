#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-460.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

Contenu de recommandation pure (pas de chiffre à vérifier). Seules les
dates sont corrigées.

Idempotent. Sauvegarde en .bak_art460.

Usage :
    python3 corriger_article460.py
"""

import os

FICHIER = "article-460.html"

REMPLACEMENTS = [
    (
        "Podcasts finances personnelles : les meilleurs en 2025 — S'enrichir en écoutant. Guide complet sur Economya.fr",
        "Podcasts finances personnelles : les meilleurs en 2026 — S'enrichir en écoutant. Guide complet sur Economya.fr",
    ),
    (
        "<title>Podcasts finances personnelles : les meilleurs en 2025 — Economya.fr</title>",
        "<title>Podcasts finances personnelles : les meilleurs en 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Podcasts finances personnelles : les meilleurs en 2025",',
        '"headline": "Podcasts finances personnelles : les meilleurs en 2026",',
    ),
    (
        '<meta property="og:title" content="Podcasts finances personnelles : les meilleurs en 2025">',
        '<meta property="og:title" content="Podcasts finances personnelles : les meilleurs en 2026">',
    ),
    (
        '<meta name="twitter:title" content="Podcasts finances personnelles : les meilleurs en 2025">',
        '<meta name="twitter:title" content="Podcasts finances personnelles : les meilleurs en 2026">',
    ),
    (
        "<h1>Podcasts finances personnelles :<br><em>les meilleurs en 2025</em></h1>",
        "<h1>Podcasts finances personnelles :<br><em>les meilleurs en 2026</em></h1>",
    ),
    (
        "Les podcasts sont le format idéal pour se former en finance pendant les transports, le sport ou les tâches ménagères. En 2025, l'offre francophone s'est considérablement étoffée.",
        "Les podcasts sont le format idéal pour se former en finance pendant les transports, le sport ou les tâches ménagères. L'offre francophone s'est considérablement étoffée ces dernières années.",
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

    with open(FICHIER + ".bak_art460", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026")


if __name__ == "__main__":
    main()
