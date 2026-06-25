#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-427.html — dates 2025->2026 + ajout surtaxe avril 2026
À lancer depuis ~/Desktop/mon site

La commission de 15% (confirmée stable depuis des années) et les frais
FBA estimés (4,50€) restent dans les fourchettes confirmées pour 2026,
non modifiés. Ajout d'un fait précis manquant : une surtaxe logistique
de 1,5% sur les frais d'expédition FBA (pas sur le prix de vente) est
entrée en vigueur le 17 avril 2026 dans plusieurs pays européens dont
la France.

Idempotent. Sauvegarde en .bak_art427.

Usage :
    python3 corriger_article427.py
"""

import os

FICHIER = "article-427.html"

REMPLACEMENTS = [
    (
        "Amazon FBA en 2025 : encore rentable ? — Le vrai calcul de rentabilité. Guide complet sur Economya.fr",
        "Amazon FBA en 2026 : encore rentable ? — Le vrai calcul de rentabilité. Guide complet sur Economya.fr",
    ),
    (
        "<title>Amazon FBA en 2025 : encore rentable ? — Economya.fr</title>",
        "<title>Amazon FBA en 2026 : encore rentable ? — Economya.fr</title>",
    ),
    (
        '"headline": "Amazon FBA en 2025 : encore rentable ?",',
        '"headline": "Amazon FBA en 2026 : encore rentable ?",',
    ),
    (
        '<meta property="og:title" content="Amazon FBA en 2025 : encore rentable ?">',
        '<meta property="og:title" content="Amazon FBA en 2026 : encore rentable ?">',
    ),
    (
        '<meta name="twitter:title" content="Amazon FBA en 2025 : encore rentable ?">',
        '<meta name="twitter:title" content="Amazon FBA en 2026 : encore rentable ?">',
    ),
    (
        "<h1>Amazon FBA en 2025 :<br><em>encore rentable ?</em></h1>",
        "<h1>Amazon FBA en 2026 :<br><em>encore rentable ?</em></h1>",
    ),
    (
        "Amazon FBA (Fulfilled By Amazon) consiste à envoyer vos stocks à Amazon qui gère le stockage, l'expédition et le service client. En 2025, la concurrence est intense et les frais d'Amazon ont augmenté. Est-ce encore rentable ? La réponse honnête : oui, mais les marges sont serrées et le capital initial est important.",
        "Amazon FBA (Fulfilled By Amazon) consiste à envoyer vos stocks à Amazon qui gère le stockage, l'expédition et le service client. La concurrence est intense et, depuis le 17 avril 2026, une surtaxe logistique de 1,5% s'applique sur les frais d'expédition FBA en Europe (pas sur le prix de vente — un impact réel mais limité sur la marge). Est-ce encore rentable ? La réponse honnête : oui, mais les marges sont serrées et le capital initial est important.",
    ),
    (
        "⚖️ Amazon FBA en 2025 : avantages vs défis réels",
        "⚖️ Amazon FBA en 2026 : avantages vs défis réels",
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

    with open(FICHIER + ".bak_art427", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026, surtaxe logistique 1,5% (avril 2026) ajoutee")


if __name__ == "__main__":
    main()
