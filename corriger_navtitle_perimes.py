#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction de 2 liens "nav-title" périmés (navigation article précédent/
suivant) — hors du périmètre de synchroniser_liens_croises.py qui ne
cible que les sim-card-title
À lancer depuis ~/Desktop/mon site

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_navtitle_perimes.py
"""

import os

REMPLACEMENTS = {
    "article-1.html": [
        (
            '<span class="nav-title">Quel fournisseur d\'électricité choisir en 2025 ?</span>',
            '<span class="nav-title">Quel fournisseur d\'électricité choisir en 2026 ?</span>',
        ),
    ],
    "article-33.html": [
        (
            '<span class="nav-title">Jouer aux jeux vidéo sans se ruiner en 2025</span>',
            '<span class="nav-title">Jouer aux jeux vidéo sans se ruiner en 2026</span>',
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
