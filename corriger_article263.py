#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-263.html — malus écologique obsolète
À lancer depuis ~/Desktop/mon site

Corrections vérifiées via source officielle (service-public.gouv.fr, fiche F35947,
et economie.gouv.fr), pour le barème en vigueur au 1er janvier 2026 :
1. Année 2025 -> 2026 (titre, meta, intro, h2)
2. Plafond malus CO2 : 60 000€ -> 80 000€ (au-delà de 192 g/km)
3. Seuil malus masse : 1 600 kg -> 1 500 kg

⚠️ LIMITE ASSUMÉE : les valeurs précises ligne par ligne du tableau gramme par
gramme (118g, 119-122g, etc.) n'ont pas pu être vérifiées avec une confiance
suffisante pour être réécrites sans risque de remplacer une erreur par une autre.
Une mention est ajoutée pour renvoyer vers le simulateur officiel.

Idempotent. Sauvegarde en .bak_art263.

Usage :
    python3 corriger_article263.py
"""

import os

FICHIER = "article-263.html"

REMPLACEMENTS = [
    (
        "Malus écologique 2025 : barème complet — Évitez jusqu'à 60 000€ de malus. Guide complet sur Economya.fr",
        "Malus écologique 2026 : barème complet — Évitez jusqu'à 80 000€ de malus. Guide complet sur Economya.fr",
    ),
    (
        "⚠️ Évitez jusqu'à 60 000 € de malus",
        "⚠️ Évitez jusqu'à 80 000 € de malus",
    ),
    (
        "Le malus écologique a été drastiquement durci depuis 2024. Un SUV diesel émettant 160 g de CO₂/km peut aujourd'hui coûter plus de 10 000 € de malus. Les seuils baissent chaque année. Voici le barème 2025 complet pour anticiper avant d'acheter.",
        "Le malus écologique a été drastiquement durci depuis 2024. Un SUV diesel émettant 160 g de CO₂/km peut aujourd'hui coûter plus de 10 000 € de malus. Les seuils baissent chaque année. Voici le barème 2026 complet pour anticiper avant d'acheter. Pour un calcul exact gramme par gramme, vérifiez le simulateur officiel sur service-public.fr.",
    ),
    (
        "📊 Barème malus CO₂ 2025 (véhicules neufs)",
        "📊 Barème malus CO₂ 2026 (véhicules neufs)",
    ),
    (
        '<tr><td>175 g et plus</td><td class="rr">Plafonné à 60 000 €</td><td class="rr">60 000 €</td></tr>',
        '<tr><td>192 g et plus</td><td class="rr">Plafonné à 80 000 €</td><td class="rr">80 000 €</td></tr>',
    ),
    (
        "Depuis 2022, un malus sur le poids s'applique aux véhicules dépassant 1 600 kg : 10 € par kg supplémentaire. Un SUV de 2 tonnes peut ainsi cumuler malus CO₂ + malus poids. Les véhicules électriques sont exonérés du malus masse jusqu'à 2 300 kg.",
        "Depuis 2022, un malus sur le poids s'applique aux véhicules dépassant 1 500 kg : à partir de 10 € par kg supplémentaire (taux progressif par tranches). Un SUV de 2 tonnes peut ainsi cumuler malus CO₂ + malus poids. Les véhicules électriques restent exonérés du malus masse en 2026.",
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

    with open(FICHIER + ".bak_art263", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   ⚠️  Tableau détaillé gramme par gramme non réécrit (valeurs intermédiaires")
    print("      non vérifiables avec confiance) — mention du simulateur officiel ajoutée.")


if __name__ == "__main__":
    main()
