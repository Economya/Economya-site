#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-164.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

Les prix de vols et budgets voyage sont intrinsèquement volatils et déjà
présentés en fourchettes (60-120€, 30-50€/jour, etc.) — plus robustes
face à l'obsolescence que des prix fixes. Pas de chiffre réglementé à
vérifier ici. Seules les dates sont corrigées.

Idempotent. Sauvegarde en .bak_art164.

Usage :
    python3 corriger_article164.py
"""

import os

FICHIER = "article-164.html"

REMPLACEMENTS = [
    (
        "<title>Maroc, Tunisie, Portugal : destinations low cost 2025 — Economya.fr</title>",
        "<title>Maroc, Tunisie, Portugal : destinations low cost 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Maroc, Tunisie, Portugal : destinations low cost 2025",',
        '"headline": "Maroc, Tunisie, Portugal : destinations low cost 2026",',
    ),
    (
        '<meta property="og:title" content="Maroc, Tunisie, Portugal : destinations low cost 2025">',
        '<meta property="og:title" content="Maroc, Tunisie, Portugal : destinations low cost 2026">',
    ),
    (
        '<meta name="twitter:title" content="Maroc, Tunisie, Portugal : destinations low cost 2025">',
        '<meta name="twitter:title" content="Maroc, Tunisie, Portugal : destinations low cost 2026">',
    ),
    (
        '<meta name="description" content="Maroc, Tunisie, Portugal : destinations low cost 2025 — Economya.fr" />',
        '<meta name="description" content="Maroc, Tunisie, Portugal : destinations low cost 2026 — Economya.fr" />',
    ),
    (
        "<h1>Maroc, Tunisie, Portugal : destinations low cost 2025</h1>",
        "<h1>Maroc, Tunisie, Portugal : destinations low cost 2026</h1>",
    ),
    (
        "c'est encore possible en 2025 — à condition de choisir les bonnes destinations",
        "c'est encore possible — à condition de choisir les bonnes destinations",
    ),
    (
        "Le Portugal est la destination européenne qui offre le meilleur rapport qualité-prix en 2025.",
        "Le Portugal est la destination européenne qui offre le meilleur rapport qualité-prix.",
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

    with open(FICHIER + ".bak_art164", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026 (prix voyage non modifies, deja en fourchettes)")


if __name__ == "__main__":
    main()
