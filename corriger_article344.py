#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-344.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

La ligne sur la flat tax crypto (31,4% depuis 2026) est déjà correcte
(corrigée plus tôt dans la session). Seules les dates du titre/meta/h1/
lead restent à mettre à jour. Les frais de plateforme (Binance, Coinbase,
etc.) sont des taux commerciaux propres à chaque service, non vérifiés
ici (hors périmètre de cette correction).

Idempotent. Sauvegarde en .bak_art344.

Usage :
    python3 corriger_article344.py
"""

import os

FICHIER = "article-344.html"

REMPLACEMENTS = [
    (
        "Bitcoin en 2025 : acheter, stocker, sécuriser — Guide sans jargon. Guide complet sur Economya.fr",
        "Bitcoin en 2026 : acheter, stocker, sécuriser — Guide sans jargon. Guide complet sur Economya.fr",
    ),
    (
        "<title>Bitcoin en 2025 : acheter, stocker, sécuriser — Economya.fr</title>",
        "<title>Bitcoin en 2026 : acheter, stocker, sécuriser — Economya.fr</title>",
    ),
    (
        '"headline": "Bitcoin en 2025 : acheter, stocker, sécuriser",',
        '"headline": "Bitcoin en 2026 : acheter, stocker, sécuriser",',
    ),
    (
        '<meta property="og:title" content="Bitcoin en 2025 : acheter, stocker, sécuriser">',
        '<meta property="og:title" content="Bitcoin en 2026 : acheter, stocker, sécuriser">',
    ),
    (
        '<meta name="twitter:title" content="Bitcoin en 2025 : acheter, stocker, sécuriser">',
        '<meta name="twitter:title" content="Bitcoin en 2026 : acheter, stocker, sécuriser">',
    ),
    (
        "<h1>Bitcoin en 2025 :<br><em>acheter, stocker, sécuriser</em></h1>",
        "<h1>Bitcoin en 2026 :<br><em>acheter, stocker, sécuriser</em></h1>",
    ),
    (
        "Le Bitcoin est l'actif le plus performant de la décennie 2010–2020, mais aussi l'un des plus volatils. En 2025, il est plus accessible que jamais via des plateformes régulées françaises. Mais la sécurité reste l'enjeu majeur : perdre sa clé privée, c'est perdre ses bitcoins définitivement.",
        "Le Bitcoin est l'actif le plus performant de la décennie 2010–2020, mais aussi l'un des plus volatils. En 2026, il est plus accessible que jamais via des plateformes régulées françaises. Mais la sécurité reste l'enjeu majeur : perdre sa clé privée, c'est perdre ses bitcoins définitivement.",
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

    with open(FICHIER + ".bak_art344", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026 (flat tax deja correcte)")


if __name__ == "__main__":
    main()
