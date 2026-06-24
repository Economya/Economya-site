#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-431.html — plafond PER obsolète + taux MaPrimeRénov'
À lancer depuis ~/Desktop/mon site

1. Plafond PER : 32 909€ (donnée très ancienne, ~2021) -> 37 680€
   (plafond maximum 2026 pour un salarié, confirmé par service-public.fr
   et sources convergentes : 10% × 8 PASS 2025, PASS 2025 = 47 100€)
2. Dates 2025 -> 2026
3. MaPrimeRénov "30 à 70%" -> "30 à 80%" (cohérent avec les corrections
   déjà appliquées ailleurs sur le site)

Idempotent. Sauvegarde en .bak_art431.

Usage :
    python3 corriger_article431.py
"""

import os

FICHIER = "article-431.html"

REMPLACEMENTS = [
    (
        "💰 Les 10 niches fiscales méconnues à utiliser en 2025",
        "💰 Les 10 niches fiscales méconnues à utiliser en 2026",
    ),
    (
        "Les versements sur un PER individuel sont déductibles du revenu imposable dans la limite de 10 % des revenus professionnels nets (plafond 2025 : environ 32 909 €). Pour un contribuable à 30 % de TMI versant 5 000 €, c'est 1 500 € d'impôt économisés immédiatement.",
        "Les versements sur un PER individuel sont déductibles du revenu imposable dans la limite de 10 % des revenus professionnels nets (plafond 2026 pour un salarié : 37 680 €, ou 4 710 € minimum si vos revenus sont faibles). Pour un contribuable à 30 % de TMI versant 5 000 €, c'est 1 500 € d'impôt économisés immédiatement.",
    ),
    (
        "Les travaux d'isolation, de chauffage et de ventilation dans votre résidence principale ouvrent droit à MaPrimeRénov (subvention) ET à une TVA réduite à 5,5 %. L'ensemble peut couvrir 30 à 70 % du coût total selon les travaux et votre revenu.",
        "Les travaux d'isolation, de chauffage et de ventilation dans votre résidence principale ouvrent droit à MaPrimeRénov (subvention) ET à une TVA réduite à 5,5 %. L'ensemble peut couvrir 30 à 80 % du coût total selon les travaux et votre revenu. ⚠️ Depuis 2026, certains travaux (isolation des murs, chaudières biomasse) ne sont finançables qu'en rénovation d'ampleur, pas en geste isolé.",
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

    with open(FICHIER + ".bak_art431", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Plafond PER 32 909€->37 680€, taux MPR 70%->80%, dates 2026")


if __name__ == "__main__":
    main()
