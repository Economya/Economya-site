#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-62.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

Contenu structurel et stable (réforme 100% Santé de 2021, prix d'entrée
opticiens en ligne) — pas de chiffre réglementé daté à vérifier. Seules
les dates sont corrigées.

Idempotent. Sauvegarde en .bak_art62.

Usage :
    python3 corriger_article62.py
"""

import os

FICHIER = "article-62.html"

REMPLACEMENTS = [
    (
        "<title>Lunettes pas chères : où acheter en 2025 — Economya.fr</title>",
        "<title>Lunettes pas chères : où acheter en 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Lunettes pas chères : où acheter en 2025",',
        '"headline": "Lunettes pas chères : où acheter en 2026",',
    ),
    (
        '<meta property="og:title" content="Lunettes pas chères : où acheter en 2025">',
        '<meta property="og:title" content="Lunettes pas chères : où acheter en 2026">',
    ),
    (
        '<meta name="twitter:title" content="Lunettes pas chères : où acheter en 2025">',
        '<meta name="twitter:title" content="Lunettes pas chères : où acheter en 2026">',
    ),
    (
        '<meta name="description" content="Lunettes pas chères : où acheter en 2025 — Economya.fr" />',
        '<meta name="description" content="Lunettes pas chères : où acheter en 2026 — Economya.fr" />',
    ),
    (
        "<h1>Lunettes pas chères :<br><em>où acheter en 2025</em></h1>",
        "<h1>Lunettes pas chères :<br><em>où acheter en 2026</em></h1>",
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

    with open(FICHIER + ".bak_art62", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026")


if __name__ == "__main__":
    main()
