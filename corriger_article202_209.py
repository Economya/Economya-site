#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-202.html (taux immobilier obsolète) et article-209.html
(date)
À lancer depuis ~/Desktop/mon site

article-202 : "3,4 à 3,8%" était déjà identifié comme obsolète ce matin
et corrigé dans article-201 en "3,3 à 3,7%" (taux 2026 confirmé). Même
correction appliquée ici pour cohérence inter-articles.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_article202_209.py
"""

import os

REMPLACEMENTS = {
    "article-202.html": [
        (
            "Des millions de Français ont souscrit un crédit immobilier entre 2016 et 2022, à des taux compris entre 1 % et 2,5 %. Depuis, les taux ont grimpé puis redescendu — et se stabilisent en 2025 autour de 3,4 à 3,8 %.",
            "Des millions de Français ont souscrit un crédit immobilier entre 2016 et 2022, à des taux compris entre 1 % et 2,5 %. Depuis, les taux ont grimpé puis redescendu — et se stabilisent en 2026 autour de 3,3 à 3,7 %.",
        ),
    ],
    "article-209.html": [
        (
            "Les photos : le vrai levier en 2025",
            "Les photos : le vrai levier en 2026",
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
