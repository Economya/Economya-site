#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-246.html — modèle gratuit obsolète, prix Plus obsolète
À lancer depuis ~/Desktop/mon site

Confirmé par de nombreuses sources convergentes (2026) :
1. Le modèle gratuit n'est plus GPT-4o mini — c'est désormais un modèle
   de la gamme GPT-5.x (numéro exact volatil selon la date, formulé de
   façon générique pour éviter une nouvelle obsolescence rapide)
2. ChatGPT Plus est passé de 20€ à 23€/mois
3. Nouveauté non mentionnée : un palier "Go" à 8€/mois existe désormais
   entre le gratuit et le Plus

Idempotent. Sauvegarde en .bak_art246.

Usage :
    python3 corriger_article246.py
"""

import os

FICHIER = "article-246.html"

REMPLACEMENTS = [
    (
        "ChatGPT gratuit : tout ce qu'on peut faire en 2025 — IA gratuite au quotidien. Guide complet sur Economya.fr",
        "ChatGPT gratuit : tout ce qu'on peut faire en 2026 — IA gratuite au quotidien. Guide complet sur Economya.fr",
    ),
    (
        "<title>ChatGPT gratuit : tout ce qu'on peut faire en 2025 — Economya.fr</title>",
        "<title>ChatGPT gratuit : tout ce qu'on peut faire en 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "ChatGPT gratuit : tout ce qu\'on peut faire en 2025",',
        '"headline": "ChatGPT gratuit : tout ce qu\'on peut faire en 2026",',
    ),
    (
        '<meta property="og:title" content="ChatGPT gratuit : tout ce qu\'on peut faire en 2025">',
        '<meta property="og:title" content="ChatGPT gratuit : tout ce qu\'on peut faire en 2026">',
    ),
    (
        '<meta name="twitter:title" content="ChatGPT gratuit : tout ce qu\'on peut faire en 2025">',
        '<meta name="twitter:title" content="ChatGPT gratuit : tout ce qu\'on peut faire en 2026">',
    ),
    (
        "<h1>ChatGPT gratuit :<br><em>tout ce qu'on peut faire en 2025</em></h1>",
        "<h1>ChatGPT gratuit :<br><em>tout ce qu'on peut faire en 2026</em></h1>",
    ),
    (
        "ChatGPT version gratuite reste en 2025 l'un des outils les plus puissants accessibles sans débourser un centime. Rédaction, recherche, code, résumés, traduction, conseils… Voici ce que vous pouvez vraiment en tirer — et où la version payante devient utile.",
        "ChatGPT version gratuite reste l'un des outils les plus puissants accessibles sans débourser un centime (notez qu'un palier intermédiaire \"Go\" à 8€/mois existe désormais entre le gratuit et le Plus). Rédaction, recherche, code, résumés, traduction, conseils… Voici ce que vous pouvez vraiment en tirer — et où la version payante devient utile.",
    ),
    (
        "<th>Gratuit (GPT-4o mini)</th>",
        "<th>Gratuit (modèle de base, dernière génération GPT-5)</th>",
    ),
    (
        "<th>Plus (20 €/mois)</th>",
        "<th>Plus (23 €/mois)</th>",
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

    with open(FICHIER + ".bak_art246", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Modele GPT-5.x, Plus 23e/mois, mention palier Go ajoutee")


if __name__ == "__main__":
    main()
