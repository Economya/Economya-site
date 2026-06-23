#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-306.html — montants allocations familiales obsolètes
À lancer depuis ~/Desktop/mon site

Les montants actuels (176€/401€/627€) sont nettement supérieurs aux vrais
montants CAF 2026 (vérifiés via plusieurs sources convergentes, barème
post-revalorisation du 1er avril 2026) : ~152€/349€/545€. Incohérence
interne également détectée : le badge disait "350€" alors que le tableau
allait jusqu'à 627€.

⚠️ La ligne "par enfant supplémentaire" n'a pas pu être vérifiée avec
confiance — laissée inchangée, à vérifier manuellement sur caf.fr.

Idempotent. Sauvegarde en .bak_art306.

Usage :
    python3 corriger_article306.py
"""

import os

FICHIER = "article-306.html"

REMPLACEMENTS = [
    (
        "Allocations familiales 2025 : montants et conditions — Jusqu'à 350€/mois. Guide complet sur Economya.fr",
        "Allocations familiales 2026 : montants et conditions — Jusqu'à 545€/mois. Guide complet sur Economya.fr",
    ),
    (
        "💰 Jusqu'à 350 €/mois",
        "💰 Jusqu'à 545 €/mois",
    ),
    (
        "Les allocations familiales sont versées par la CAF à toutes les familles ayant au moins 2 enfants de moins de 20 ans. Leur montant dépend du nombre d'enfants et des revenus du foyer depuis la modulation mise en place en 2015. Voici les montants 2025 et toutes les conditions.",
        "Les allocations familiales sont versées par la CAF à toutes les familles ayant au moins 2 enfants de moins de 20 ans. Leur montant dépend du nombre d'enfants et des revenus du foyer depuis la modulation mise en place en 2015. Voici les montants 2026 et toutes les conditions.",
    ),
    (
        "💶 Montants des allocations familiales 2025",
        "💶 Montants des allocations familiales 2026",
    ),
    (
        '<tr><td>2 enfants</td><td class="g">176 €/mois</td><td class="o">88 €/mois</td><td>44 €/mois</td></tr>',
        '<tr><td>2 enfants</td><td class="g">152 €/mois</td><td class="o">76 €/mois</td><td>38 €/mois</td></tr>',
    ),
    (
        '<tr><td>3 enfants</td><td class="g">401 €/mois</td><td class="o">201 €/mois</td><td>100 €/mois</td></tr>',
        '<tr><td>3 enfants</td><td class="g">349 €/mois</td><td class="o">174 €/mois</td><td>87 €/mois</td></tr>',
    ),
    (
        '<tr><td>4 enfants</td><td class="g">627 €/mois</td><td class="o">313 €/mois</td><td>157 €/mois</td></tr>',
        '<tr><td>4 enfants</td><td class="g">545 €/mois</td><td class="o">272 €/mois</td><td>136 €/mois</td></tr>',
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
        if nouveau in contenu:
            continue
        if ancien in contenu:
            contenu = contenu.replace(ancien, nouveau)
            nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou textes attendus non trouvés.")
        return

    with open(FICHIER + ".bak_art306", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   ⚠️  Ligne 'par enfant supplémentaire' non vérifiée — à contrôler sur caf.fr")


if __name__ == "__main__":
    main()
