#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du dernier lot article-63/71/82/85/87 — clôture du balayage
systématique des 527 articles
À lancer depuis ~/Desktop/mon site

article-71 : prix Amazon Prime (69,90€/an) confirmé EXACT et inchangé
pour 2026 (source officielle amazon.fr) — seule l'année est mise à jour.
Les autres fichiers : dates génériques uniquement.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot63_87.py
"""

import os

REMPLACEMENTS = {
    "article-63.html": [
        (
            "Les meilleures plateformes last minute en 2025",
            "Les meilleures plateformes last minute en 2026",
        ),
    ],
    "article-71.html": [
        (
            "L'abonnement Amazon Prime coûte <strong>69,90 € par an</strong> en 2025.",
            "L'abonnement Amazon Prime coûte <strong>69,90 € par an</strong> en 2026.",
        ),
    ],
    "article-82.html": [
        (
            "Les assureurs les moins chers en 2025",
            "Les assureurs les moins chers en 2026",
        ),
    ],
    "article-85.html": [
        (
            "Les offres les moins chères du marché en 2025",
            "Les offres les moins chères du marché en 2026",
        ),
    ],
    "article-87.html": [
        (
            "alors que les ressources gratuites disponibles en 2025 permettent d'atteindre un niveau B2",
            "alors que les ressources gratuites disponibles permettent d'atteindre un niveau B2",
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
    print(f"🎉 Balayage systematique des 527 articles TERMINE")


if __name__ == "__main__":
    main()
