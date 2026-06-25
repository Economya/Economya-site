#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-252.html — prix Netflix obsolètes
À lancer depuis ~/Desktop/mon site

Confirmé par très nombreuses sources convergentes (juin 2026), après la
hausse de janvier 2026 :
- Standard avec pub : 4,99€ -> 7,99€/mois
- Standard (sans pub) : 13,49€ -> 14,99€/mois
- Premium : 19,99€ -> 21,99€/mois
- Membre supplémentaire : 4,99€ -> 5,99€/mois (hors foyer)

Idempotent. Sauvegarde en .bak_art252.

Usage :
    python3 corriger_article252.py
"""

import os

FICHIER = "article-252.html"

REMPLACEMENTS = [
    (
        "Netflix 2025 : partage de compte, règles, prix — Compte légal dès 4,99€/mois. Guide complet sur Economya.fr",
        "Netflix 2026 : partage de compte, règles, prix — Compte légal dès 7,99€/mois. Guide complet sur Economya.fr",
    ),
    (
        "<title>Netflix 2025 : partage de compte, règles, prix — Economya.fr</title>",
        "<title>Netflix 2026 : partage de compte, règles, prix — Economya.fr</title>",
    ),
    (
        '"headline": "Netflix 2025 : partage de compte, règles, prix",',
        '"headline": "Netflix 2026 : partage de compte, règles, prix",',
    ),
    (
        '<meta property="og:title" content="Netflix 2025 : partage de compte, règles, prix">',
        '<meta property="og:title" content="Netflix 2026 : partage de compte, règles, prix">',
    ),
    (
        '<meta name="twitter:title" content="Netflix 2025 : partage de compte, règles, prix">',
        '<meta name="twitter:title" content="Netflix 2026 : partage de compte, règles, prix">',
    ),
    (
        "<h1>Netflix 2025 :<br><em>partage de compte, règles, prix</em></h1>",
        "<h1>Netflix 2026 :<br><em>partage de compte, règles, prix</em></h1>",
    ),
    (
        '<div class="savings-badge">💰 Compte légal dès 4,99 €/mois</div>',
        '<div class="savings-badge">💰 Compte légal dès 7,99 €/mois</div>',
    ),
    (
        "Depuis 2023, Netflix a mis fin au partage de compte gratuit entre foyers différents. En 2025, les règles sont claires : chaque foyer doit avoir son propre abonnement. Mais Netflix propose des solutions légales accessibles dès 4,99 €/mois. Voici tout ce qu'il faut savoir pour payer le juste prix.",
        "Depuis 2023, Netflix a mis fin au partage de compte gratuit entre foyers différents. Les règles sont claires : chaque foyer doit avoir son propre abonnement. Mais Netflix propose des solutions légales accessibles dès 7,99 €/mois. Voici tout ce qu'il faut savoir pour payer le juste prix.",
    ),
    (
        "💶 Les offres Netflix en France en 2025",
        "💶 Les offres Netflix en France en 2026",
    ),
    (
        '<div class="p-prix">4,99 €</div>',
        '<div class="p-prix">7,99 €</div>',
    ),
    (
        '<div class="p-prix">13,49 €</div>\n      <div class="p-desc">HD 1080p, 2 écrans simultanés, sans pub. Option membre supplémentaire : +4,99 €/mois.</div>',
        '<div class="p-prix">14,99 €</div>\n      <div class="p-desc">HD 1080p, 2 écrans simultanés, sans pub. Option membre supplémentaire : +5,99 €/mois.</div>',
    ),
    (
        '<div class="p-prix">19,99 €</div>\n      <div class="p-desc">4K Ultra HD, 4 écrans simultanés, son Spatial Audio. Option membre supplémentaire : +4,99 €/mois.</div>',
        '<div class="p-prix">21,99 €</div>\n      <div class="p-desc">4K Ultra HD, 4 écrans simultanés, son Spatial Audio. Option membre supplémentaire : +5,99 €/mois.</div>',
    ),
    (
        "👥 Le partage de compte en 2025 — ce qui est légal",
        "👥 Le partage de compte en 2026 — ce qui est légal",
    ),
    (
        "La solution légale pour partager avec quelqu'un hors de chez vous : l'option <strong>Membre supplémentaire</strong> à 4,99 €/mois (disponible sur Standard et Premium). Cette personne a son propre profil et ses propres identifiants.",
        "La solution légale pour partager avec quelqu'un hors de chez vous : l'option <strong>Membre supplémentaire</strong> à 5,99 €/mois (disponible sur Standard et Premium). Cette personne a son propre profil et ses propres identifiants.",
    ),
    (
        "💡 L'offre avec pub à 4,99 €/mois : la meilleure option pour les petits budgets",
        "💡 L'offre avec pub à 7,99 €/mois : la meilleure option pour les petits budgets",
    ),
    (
        "Pour 4,99 €/mois, vous avez accès à l'essentiel du catalogue (quelques contenus exclus), en HD 1080p, sur 2 écrans. Si vous regardez Netflix 2 à 3 heures par semaine, c'est le meilleur rapport qualité/prix.",
        "Pour 7,99 €/mois, vous avez accès à l'essentiel du catalogue (quelques contenus exclus, environ 85% du catalogue total), en HD 1080p, sur 2 écrans. Si vous regardez Netflix 2 à 3 heures par semaine, c'est le meilleur rapport qualité/prix.",
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

    with open(FICHIER + ".bak_art252", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Prix Netflix 2026: 7,99/14,99/21,99e, membre sup 5,99e")


if __name__ == "__main__":
    main()
