#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-492.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

Tarifs commerciaux précis (Revolut Premium 9,99€/mois, frais retrait
1,7%, etc.) NON modifiés — hors périmètre vérifiable sans recherche
dédiée par établissement. Le rebranding Lydia->Sumeria est déjà
correctement noté. Seules les dates sont corrigées.

Idempotent. Sauvegarde en .bak_art492.

Usage :
    python3 corriger_article492.py
"""

import os

FICHIER = "article-492.html"

REMPLACEMENTS = [
    (
        "Revolut, N26, Lydia : quelle néobanque en 2025 — Zéro frais, cashback, lounge. Guide complet sur Economya.fr",
        "Revolut, N26, Lydia : quelle néobanque en 2026 — Zéro frais, cashback, lounge. Guide complet sur Economya.fr",
    ),
    (
        "<title>Revolut, N26, Lydia : quelle néobanque en 2025 — Economya.fr</title>",
        "<title>Revolut, N26, Lydia : quelle néobanque en 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Revolut, N26, Lydia : quelle néobanque en 2025",',
        '"headline": "Revolut, N26, Lydia : quelle néobanque en 2026",',
    ),
    (
        '<meta property="og:title" content="Revolut, N26, Lydia : quelle néobanque en 2025">',
        '<meta property="og:title" content="Revolut, N26, Lydia : quelle néobanque en 2026">',
    ),
    (
        '<meta name="twitter:title" content="Revolut, N26, Lydia : quelle néobanque en 2025">',
        '<meta name="twitter:title" content="Revolut, N26, Lydia : quelle néobanque en 2026">',
    ),
    (
        "<h1>Revolut, N26, Lydia :<br><em>quelle néobanque en 2025</em></h1>",
        "<h1>Revolut, N26, Lydia :<br><em>quelle néobanque en 2026</em></h1>",
    ),
    (
        "En 2025, Revolut, N26, Sumeria (ex-Lydia) et les banques en ligne françaises se disputent le marché.",
        "En 2026, Revolut, N26, Sumeria (ex-Lydia) et les banques en ligne françaises se disputent le marché.",
    ),
    (
        "⚖️ Le comparatif néobanques 2025",
        "⚖️ Le comparatif néobanques 2026",
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

    with open(FICHIER + ".bak_art492", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026 (tarifs commerciaux non verifies - hors perimetre)")


if __name__ == "__main__":
    main()
