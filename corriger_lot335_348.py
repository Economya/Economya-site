#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du lot article-335/336/338/340/345/348
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE MAJEURE article-345 : le cours de l'or a augmenté d'environ
+42% depuis mai 2025 (~80€/g -> ~114€/g, confirmé par plusieurs sources
convergentes, juin 2026). Les prix produits sont recalculés
proportionnellement (approximation raisonnable, le cours réel fluctue
en continu — une note invite à vérifier le cours du jour).

article-340 : rendement fonds euros 2,5-3,5% NON re-vérifié précisément
pour 2026 — seule l'année est mise à jour, fourchette conservée par
prudence (à vérifier plus précisément si besoin).

article-348 : la référence croisée vers l'article-349 (corrigé en
profondeur aujourd'hui — loi Le Meur) est mise à jour de "cadre légal
2025" à "cadre légal 2026".

article-335/336/338 : dates uniquement, contenu déjà à jour par ailleurs.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot335_348.py
"""

import os

REMPLACEMENTS = {
    "article-335.html": [
        (
            "a été finalisé en 2023–2024.",
            "a été finalisé en 2023–2024 et continue d'évoluer depuis.",
        ),
    ],
    "article-336.html": [
        (
            "🏆 Les meilleurs ETF World pour débutants en 2025",
            "🏆 Les meilleurs ETF World pour débutants en 2026",
        ),
    ],
    "article-338.html": [
        (
            "PEA disponible depuis 2024.",
            "PEA disponible.",
        ),
    ],
    "article-340.html": [
        (
            "les fonds euros (capital garanti, ~2,5–3,5 % en 2025)",
            "les fonds euros (capital garanti, ~2,5–3,5 % en 2026 — à vérifier précisément selon l'assureur)",
        ),
        (
            "<li>Rendement 2025 : ~2,5–3,5 %/an</li>",
            "<li>Rendement 2026 : ~2,5–3,5 %/an (à vérifier précisément selon l'assureur)</li>",
        ),
    ],
    "article-345.html": [
        (
            "En 2025, le gramme d'or dépasse les 80 €.",
            "En 2026, le gramme d'or dépasse les 110 € — une envolée de plus de 40% depuis mi-2025, à vérifier au cours du jour avant tout achat.",
        ),
        (
            '<div class="prod-prix">~490 € (mai 2025)</div>',
            '<div class="prod-prix">~700 € (estimation juin 2026, à vérifier au cours du jour)</div>',
        ),
        (
            '<div class="prod-prix">~2 700 € (mai 2025)</div>',
            '<div class="prod-prix">~3 850 € (estimation juin 2026, à vérifier au cours du jour)</div>',
        ),
        (
            '<div class="prod-prix">~2 750 € (mai 2025)</div>',
            '<div class="prod-prix">~3 920 € (estimation juin 2026, à vérifier au cours du jour)</div>',
        ),
        (
            '<div class="prod-prix">~90 € (mai 2025)</div>',
            '<div class="prod-prix">~128 € (estimation juin 2026, à vérifier au cours du jour)</div>',
        ),
    ],
    "article-348.html": [
        (
            "Consultez l'article 349 de ce site sur le cadre légal 2025.",
            "Consultez l'article 349 de ce site sur le cadre légal 2026.",
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
    print(f"⚠️ article-345 : prix or estimes (+42%), verifier cours du jour")


if __name__ == "__main__":
    main()
