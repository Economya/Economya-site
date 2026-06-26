#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des dates 2025->2026 sur 6 fichiers (lot 151-200)
À lancer depuis ~/Desktop/mon site

Contenu générique sans chiffre substantiel verifiable (tendances deco,
avertissement crypto, prix concert, comparatif box fibre, LED, cout
electromenager). Seules les dates sont corrigees.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot151_200.py
"""

import os

REMPLACEMENTS = {
    "article-151.html": [
        (
            "Les tendances 2025 faciles à reproduire soi-même",
            "Les tendances 2026 faciles à reproduire soi-même",
        ),
    ],
    "article-158.html": [
        (
            "ignorer complètement ce marché en 2025 est une position aussi risquée qu'y plonger les yeux fermés.",
            "ignorer complètement ce marché en 2026 est une position aussi risquée qu'y plonger les yeux fermés.",
        ),
    ],
    "article-184.html": [
        (
            "Un billet pour un grand concert pop ou rock dépasse régulièrement les 80 à 120 euros en 2025 — sans compter le transport, la restauration sur place et l'hébergement pour les festivals.",
            "Un billet pour un grand concert pop ou rock dépasse régulièrement les 80 à 120 euros en 2026 — sans compter le transport, la restauration sur place et l'hébergement pour les festivals.",
        ),
    ],
    "article-192.html": [
        (
            "Comparatif des offres box fibre en 2025",
            "Comparatif des offres box fibre en 2026",
        ),
        (
            "Tarifs indicatifs mai 2025 — vérifiez les offres du moment sur les sites des opérateurs ou sur comparateurs.",
            "Tarifs indicatifs juin 2026 — vérifiez les offres du moment sur les sites des opérateurs ou sur comparateurs.",
        ),
    ],
    "article-194.html": [
        (
            "LED haute efficacité (2025)",
            "LED haute efficacité (2026)",
        ),
    ],
    "article-198.html": [
        (
            'Prix moyen France 2025',
            'Prix moyen France 2026',
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
