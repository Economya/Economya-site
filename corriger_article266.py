#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-266.html — leasing social VE : seuil obsolète + nuance
sur le fonctionnement par éditions
À lancer depuis ~/Desktop/mon site

Le seuil de revenu fiscal de référence est passé de 15 400€ (1ère édition,
2024) à 16 880€ pour l'édition 2026 (confirmé par plusieurs sources
détaillées citant le dossier de presse officiel d'avril 2026, montrant
une progression 15 400€->16 300€ (2025)->16 880€ (2026)).

⚠️ Point important ajouté : ce dispositif fonctionne par ÉDITIONS limitées
dans le temps (pas en continu) — la 3e édition rouvre le 16 juillet 2026,
avec un nombre de contrats plafonné (50 000) généralement épuisé en
quelques semaines.

Idempotent. Sauvegarde en .bak_art266.

Usage :
    python3 corriger_article266.py
"""

import os

FICHIER = "article-266.html"

REMPLACEMENTS = [
    (
        "Leasing social VE 2025 : conditions et dossier — VE dès 100€/mois. Guide complet sur Economya.fr",
        "Leasing social VE 2026 : conditions et dossier — VE dès 100€/mois. Guide complet sur Economya.fr",
    ),
    (
        "<title>Leasing social VE 2025 : conditions et dossier — Economya.fr</title>",
        "<title>Leasing social VE 2026 : conditions et dossier — Economya.fr</title>",
    ),
    (
        '"headline": "Leasing social VE 2025 : conditions et dossier",',
        '"headline": "Leasing social VE 2026 : conditions et dossier",',
    ),
    (
        '<meta property="og:title" content="Leasing social VE 2025 : conditions et dossier">',
        '<meta property="og:title" content="Leasing social VE 2026 : conditions et dossier">',
    ),
    (
        '<meta name="twitter:title" content="Leasing social VE 2025 : conditions et dossier">',
        '<meta name="twitter:title" content="Leasing social VE 2026 : conditions et dossier">',
    ),
    (
        "<h1>Leasing social VE 2025 :<br><em>conditions et dossier</em></h1>",
        "<h1>Leasing social VE 2026 :<br><em>conditions et dossier</em></h1>",
    ),
    (
        "Le leasing social permet aux ménages modestes de louer un véhicule électrique neuf à partir de 100 €/mois — assurance et entretien inclus. Un dispositif exceptionnel remis en place par le gouvernement après le succès de la première édition. Voici tout ce qu'il faut savoir pour préparer votre dossier.",
        "Le leasing social permet aux ménages modestes de louer un véhicule électrique neuf à partir de 100 €/mois — assurance et entretien inclus. ⚠️ Ce dispositif fonctionne par éditions limitées dans le temps (3e édition : réouverture le 16 juillet 2026, 50 000 contrats disponibles, généralement épuisés en quelques semaines) — vérifiez les dates d'ouverture actuelles avant de monter votre dossier. Voici tout ce qu'il faut savoir pour préparer votre dossier.",
    ),
    (
        '<span class="stat-num">15 400 €</span><span class="stat-lbl">revenu fiscal max pour éligibilité</span>',
        '<span class="stat-num">16 880 €</span><span class="stat-lbl">revenu fiscal max pour éligibilité (2026)</span>',
    ),
    (
        "<li>Revenu fiscal ≤ 15 400 €/an</li>",
        "<li>Revenu fiscal ≤ 16 880 €/an</li>",
    ),
    (
        "<li>Revenu fiscal > 15 400 €</li>",
        "<li>Revenu fiscal > 16 880 €</li>",
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

    with open(FICHIER + ".bak_art266", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Seuil 15400e->16880e, nuance editions limitees ajoutee, dates 2026")


if __name__ == "__main__":
    main()
