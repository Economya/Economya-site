#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du lot article-351/353/354/360/369 — sources des liens
croisés répétés + montants ASPA/AAH obsolètes
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE (même schéma qu'article-201 plus tôt) : article-353 et
article-354 sont eux-mêmes encore datés "2025" dans leur titre/h1/meta
— ce qui explique la répétition de "2025" dans une dizaine de liens
croisés (351,352,355,356,358,360,361,362,363,364,365). Après ce script,
RELANCER synchroniser_liens_croises.py pour propager partout.

article-369 : ASPA 1 012€ -> 1 043,59€ (déjà confirmé aujourd'hui),
AAH 1 016€ -> 1 041,59€ (confirmé service-public.gouv.fr, avril 2026).

article-351/360 : dates uniquement.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot351_369.py
"""

import os

REMPLACEMENTS = {
    "article-353.html": [
        (
            "MOOC gratuits : les 20 meilleurs en 2025 — Harvard, MIT, Polytechnique gratuit. Guide complet sur Economya.fr",
            "MOOC gratuits : les 20 meilleurs en 2026 — Harvard, MIT, Polytechnique gratuit. Guide complet sur Economya.fr",
        ),
        (
            '"name": "MOOC gratuits : les 20 meilleurs en 2025", "item": "https://economya.fr/article-353.html"',
            '"name": "MOOC gratuits : les 20 meilleurs en 2026", "item": "https://economya.fr/article-353.html"',
        ),
        (
            "<h1>MOOC gratuits :<br><em>les 20 meilleurs en 2025</em></h1>",
            "<h1>MOOC gratuits :<br><em>les 20 meilleurs en 2026</em></h1>",
        ),
        (
            "Voici la sélection des 20 meilleures plateformes et cours gratuits en 2025.",
            "Voici la sélection des 20 meilleures plateformes et cours gratuits en 2026.",
        ),
    ],
    "article-354.html": [
        (
            "Apprendre à coder gratuitement : parcours complet 2025 — Développeur sans école à 10 000€. Guide complet sur Economya.fr",
            "Apprendre à coder gratuitement : parcours complet 2026 — Développeur sans école à 10 000€. Guide complet sur Economya.fr",
        ),
        (
            '"name": "Apprendre à coder gratuitement : parcours complet 2025", "item": "https://economya.fr/article-354.html"',
            '"name": "Apprendre à coder gratuitement : parcours complet 2026", "item": "https://economya.fr/article-354.html"',
        ),
        (
            "<h1>Apprendre à coder gratuitement :<br><em>parcours complet 2025</em></h1>",
            "<h1>Apprendre à coder gratuitement :<br><em>parcours complet 2026</em></h1>",
        ),
    ],
    "article-351.html": [
        (
            "🏆 Les meilleures formations à financer avec le CPF en 2025",
            "🏆 Les meilleures formations à financer avec le CPF en 2026",
        ),
    ],
    "article-360.html": [
        (
            "💶 Les montants Erasmus+ 2024–2025 par groupe de pays",
            "💶 Les montants Erasmus+ 2025–2026 par groupe de pays",
        ),
    ],
    "article-369.html": [
        (
            '<span class="a-montant">jusqu\'à 1 012 €/mois</span><span class="a-sub">personne seule (2025)</span>',
            '<span class="a-montant">jusqu\'à 1 043,59 €/mois</span><span class="a-sub">personne seule (2026)</span>',
        ),
        (
            '<span class="a-montant">jusqu\'à 1 016 €/mois</span><span class="a-sub">taux plein 2025</span>',
            '<span class="a-montant">jusqu\'à 1 041,59 €/mois</span><span class="a-sub">taux plein 2026</span>',
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
