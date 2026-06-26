#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des dates 2025->2026 sur 8 fichiers (lot 253-272)
À lancer depuis ~/Desktop/mon site

Contenu générique (apps gratuites, MacBook, cloud, IA, ZFE, vélo cargo)
sans chiffre substantiel à vérifier — déjà confirmé correct ailleurs
(bonus/malus écologique vérifié dans une session précédente). Seules
les dates sont corrigées, y compris une incohérence interne dans
article-263 ("seuil 2025" alors que l'article annonce "barème 2026").

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot253_272.py
"""

import os

REMPLACEMENTS = {
    "article-253.html": [
        (
            "En 2025, plusieurs applications gratuites font ce travail à votre place",
            "Plusieurs applications gratuites font ce travail à votre place",
        ),
    ],
    "article-255.html": [
        (
            "Le MacBook M1 reconditionné est l'un des meilleurs achats tech de 2025.",
            "Le MacBook M1 reconditionné est l'un des meilleurs achats tech de 2026.",
        ),
        (
            "Pour un usage confortable en 2025 : 16 Go de RAM",
            "Pour un usage confortable en 2026 : 16 Go de RAM",
        ),
    ],
    "article-256.html": [
        (
            '<span style="color:var(--t,#2C2C2A)">Cloud gratuit : comparer les offres 2025</span>',
            '<span style="color:var(--t,#2C2C2A)">Cloud gratuit : comparer les offres 2026</span>',
        ),
        (
            '"name": "Cloud gratuit : comparer les offres 2025", "item": "https://economya.fr/article-256.html"',
            '"name": "Cloud gratuit : comparer les offres 2026", "item": "https://economya.fr/article-256.html"',
        ),
        (
            "<h1>Cloud gratuit :<br><em>comparer les offres 2025</em></h1>",
            "<h1>Cloud gratuit :<br><em>comparer les offres 2026</em></h1>",
        ),
        (
            "☁️ Les meilleures offres gratuites en 2025",
            "☁️ Les meilleures offres gratuites en 2026",
        ),
    ],
    "article-258.html": [
        (
            "ChatGPT n'est plus seul. En 2025, Deepseek, Mistral Le Chat, Google Gemini et Perplexity rivalisent avec des versions gratuites très capables.",
            "ChatGPT n'est plus seul. Deepseek, Mistral Le Chat, Google Gemini et Perplexity rivalisent avec des versions gratuites très capables.",
        ),
        (
            "🏆 Les meilleurs IA gratuits en 2025",
            "🏆 Les meilleurs IA gratuits en 2026",
        ),
        (
            "Le grand choc de 2025. L'IA chinoise open source rivalise avec GPT-4 en raisonnement mathématique et en code, gratuitement.",
            "L'IA chinoise open source rivalise avec les meilleurs modèles occidentaux en raisonnement mathématique et en code, gratuitement.",
        ),
    ],
    "article-261.html": [
        (
            "💶 Les aides disponibles en 2025",
            "💶 Les aides disponibles en 2026",
        ),
    ],
    "article-263.html": [
        (
            '<div style="font-size:.72rem;color:var(--m)">Sous le seuil 2025</div>',
            '<div style="font-size:.72rem;color:var(--m)">Sous le seuil 2026</div>',
        ),
    ],
    "article-270.html": [
        (
            "🏙️ Les ZFE et leurs restrictions en 2025",
            "🏙️ Les ZFE et leurs restrictions en 2026",
        ),
    ],
    "article-272.html": [
        (
            "Voici toutes les aides disponibles en 2025.",
            "Voici toutes les aides disponibles en 2026.",
        ),
    ],
}


def main():
    total_fichiers = 0
    total_remplacements = 0

    for fichier, paires in REMPLACEMENTS.items():
        if not os.path.exists(fichier):
            print(f"❌ {fichier} introuvable, ignoré.")
            continue

        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()

        contenu_original = contenu
        nb_modifs_fichier = 0

        for ancien, nouveau in paires:
            if nouveau in contenu and ancien not in contenu:
                continue
            if ancien in contenu:
                contenu = contenu.replace(ancien, nouveau)
                nb_modifs_fichier += 1

        if nb_modifs_fichier == 0:
            print(f"✅ {fichier} : déjà corrigé ou texte non trouvé")
            continue

        ext = fichier.replace("article-", "").replace(".html", "")
        with open(fichier + f".bak_art{ext}", 'w', encoding='utf-8') as f:
            f.write(contenu_original)

        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)

        print(f"✅ {fichier} : {nb_modifs_fichier} remplacement(s)")
        total_fichiers += 1
        total_remplacements += nb_modifs_fichier

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Remplacements totaux : {total_remplacements}")


if __name__ == "__main__":
    main()
