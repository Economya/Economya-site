#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nettoyage final — derniers articles "génériques" du tout début (lot 1-33)
jamais réellement corrigés
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE : article-2 est lui-même une source non corrigée (titre/h1/
meta encore "2025") — même schéma qu'article-201/353/354. Après ce
script, RELANCER synchroniser_liens_croises.py pour propager partout
(corrigera automatiquement article-1 et le nav-title d'article-33 qui
pointent vers article-2 et article-34).

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_nettoyage_final_1_33.py
"""

import os

REMPLACEMENTS = {
    "article-2.html": [
        (
            '<meta property="og:title" content="Quel fournisseur d\'électricité choisir en 2025 ?">',
            '<meta property="og:title" content="Quel fournisseur d\'électricité choisir en 2026 ?">',
        ),
        (
            '<meta name="twitter:title" content="Quel fournisseur d\'électricité choisir en 2025 ?">',
            '<meta name="twitter:title" content="Quel fournisseur d\'électricité choisir en 2026 ?">',
        ),
        (
            '<meta name="description" content="Quel fournisseur d\'électricité choisir en 2025 ? — Economya.fr" />',
            '<meta name="description" content="Quel fournisseur d\'électricité choisir en 2026 ? — Economya.fr" />',
        ),
        (
            '<span style="color:var(--t,#2C2C2A)">Quel fournisseur d\'électricité choisir en 2025 ?</span>',
            '<span style="color:var(--t,#2C2C2A)">Quel fournisseur d\'électricité choisir en 2026 ?</span>',
        ),
        (
            '"name": "Quel fournisseur d\'électricité choisir en 2025 ?", "item": "https://economya.fr/article-2.html"',
            '"name": "Quel fournisseur d\'électricité choisir en 2026 ?", "item": "https://economya.fr/article-2.html"',
        ),
        (
            "<h1>Quel fournisseur d'électricité choisir <em>en 2025 ?</em></h1>",
            "<h1>Quel fournisseur d'électricité choisir <em>en 2026 ?</em></h1>",
        ),
        (
            "<h2>Les principaux fournisseurs en 2025</h2>",
            "<h2>Les principaux fournisseurs en 2026</h2>",
        ),
    ],
    "article-3.html": [
        (
            "Voici le classement des meilleures en 2025.",
            "Voici le classement des meilleures en 2026.",
        ),
        (
            "<h2>Le classement 2025</h2>",
            "<h2>Le classement 2026</h2>",
        ),
    ],
    "article-7.html": [
        (
            "Les meilleurs forfaits à moins de 10€/mois en 2025",
            "Les meilleurs forfaits à moins de 10€/mois en 2026",
        ),
    ],
    "article-11.html": [
        (
            "En 2025, un smartphone sur cinq vendu en France est reconditionné.",
            "Un smartphone sur cinq vendu en France est reconditionné.",
        ),
        (
            "Les meilleures plateformes en 2025",
            "Les meilleures plateformes en 2026",
        ),
    ],
    "article-23.html": [
        (
            "Les aides à l'achat d'un vélo électrique en 2025",
            "Les aides à l'achat d'un vélo électrique en 2026",
        ),
    ],
    "article-33.html": [
        (
            "<h2>Les meilleures plateformes en 2025</h2>",
            "<h2>Les meilleures plateformes en 2026</h2>",
        ),
        (
            "La RAM est suffisante pour votre usage (8 Go minimum en 2025)",
            "La RAM est suffisante pour votre usage (8 Go minimum en 2026)",
        ),
        (
            "qui soit en 2025. <strong>Back Market",
            "qui soit en 2026. <strong>Back Market",
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
    print(f"IMPORTANT: relancer synchroniser_liens_croises.py ensuite")


if __name__ == "__main__":
    main()
