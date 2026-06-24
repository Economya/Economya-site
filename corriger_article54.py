#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réécriture article-54.html — confusion MaPrimeRénov'/photovoltaïque (bis)
À lancer depuis ~/Desktop/mon site

Même erreur de fond que sur article-185 : cet article concerne le
photovoltaïque (autoconsommation, 3 kWc) — MaPrimeRénov' ne le finance
PAS. La TVA à 10% est aussi obsolète depuis le 1er janvier 2026.

Le coût "après aides" et le calcul de ROI reposaient en partie sur les
4 000€ de MaPrimeRénov' à tort attribués — ces chiffres dérivés sont
désormais incertains sans connaître le taux actuel de la prime à
l'autoconsommation (dispositif dont le montant et même l'existence sont
sujets à débat à cette période). Formulation prudente plutôt qu'un
nouveau chiffre inventé.

Idempotent. Sauvegarde en .bak_art54.

Usage :
    python3 corriger_article54.py
"""

import os

FICHIER = "article-54.html"

REMPLACEMENTS = [
    (
        "Une installation résidentielle de 3 kWc (suffisante pour une famille de 4 personnes) coûte entre 8 000 et 12 000 € après aides. Sans aides : 12 000 à 18 000 €. La durée de vie est de 25 à 30 ans.",
        "Une installation résidentielle de 3 kWc (suffisante pour une famille de 4 personnes) coûte entre 12 000 et 18 000 € avant aides. Le coût net dépend fortement des aides obtenues (voir ci-dessous) — comptez un reste à charge variable selon votre situation et le dispositif en vigueur au moment de votre projet. La durée de vie est de 25 à 30 ans.",
    ),
    (
        "MaPrimeRénov' peut couvrir jusqu'à 4 000 €. La TVA est réduite à 10%. Certaines régions proposent des aides complémentaires. Au total, les aides peuvent représenter 30 à 40% du coût.",
        "⚠️ MaPrimeRénov' ne finance PAS les panneaux photovoltaïques (production d'électricité) — uniquement le solaire thermique (chauffe-eau). Pour le photovoltaïque, les aides réelles sont : la prime à l'autoconsommation (EDF OA, montant révisé chaque trimestre — vérifiez le taux et l'existence actuelle du dispositif sur edf-oa.fr) et la TVA réduite (5,5% sous conditions strictes depuis 2026, 20% sinon — le taux de 10% n'existe plus). Certaines régions proposent des aides complémentaires.",
    ),
    (
        "En autoconsommation totale, avec une installation de 3 kWc et un coût net de 8 000 €, les économies annuelles sont de 600 à 900 €. Le retour sur investissement se situe entre 9 et 13 ans.",
        "En autoconsommation totale, avec une installation de 3 kWc, les économies annuelles sont de 600 à 900 €. Le retour sur investissement exact dépend du coût net après les aides réellement applicables (voir ci-dessus) — simulez votre cas précis avec un installateur RGE plutôt que de vous fier à un délai générique.",
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

    with open(FICHIER + ".bak_art54", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   ERREUR DE FOND corrigée : MaPrimeRénov' ne finance pas le")
    print("   photovoltaïque. TVA corrigée. Chiffres dérivés rendus prudents.")


if __name__ == "__main__":
    main()
