#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-27.html (ticket-restaurant) et article-50.html (tarif EDF)
À lancer depuis ~/Desktop/mon site

1. article-27 : exonération ticket-restaurant 2026 confirmée entre 12,20€
   et 14,64€ de valeur faciale (selon participation employeur 50-60%),
   pas un chiffre unique de 13,09€. Plafond part patronale exonérée :
   7,32€/titre en 2026 (confirmé officiel, service-public.gouv.fr).

2. article-50 : tarif réglementé EDF (Tarif Bleu, option Base) confirmé
   à 0,194€/kWh en juin 2026 — bien inférieur au "0,25€/kWh" cité,
   suite à plusieurs baisses successives en 2025-2026.

Idempotent. Sauvegardes en .bak_art27 et .bak_art50.

Usage :
    python3 corriger_article27_50.py
"""

import os

REMPLACEMENTS = {
    "article-27.html": [
        (
            "Les tickets restaurant (ou carte Swile/Edenred) sont exonérés d'impôt et de charges sociales jusqu'à 13,09€ par titre en 2025 (dont 60% payés par l'employeur). Si votre employeur les propose et que vous ne les utilisez pas systématiquement, vous perdez de l'argent. À l'inverse, ne les utilisez pas uniquement dans des restaurants — ils sont acceptés en grande surface, boulangeries et épiceries pour composer un repas moins cher.",
            "Les tickets restaurant (ou carte Swile/Edenred) sont exonérés d'impôt et de charges sociales pour une valeur faciale comprise entre 12,20€ et 14,64€ par titre en 2026, selon que l'employeur participe à 60% ou 50% (plafond de part patronale exonérée : 7,32€/titre). Si votre employeur les propose et que vous ne les utilisez pas systématiquement, vous perdez de l'argent. À l'inverse, ne les utilisez pas uniquement dans des restaurants — ils sont acceptés en grande surface, boulangeries et épiceries pour composer un repas moins cher.",
        ),
    ],
    "article-50.html": [
        (
            "Les chiffres ci-dessous sont basés sur une utilisation moyenne française et un tarif réglementé EDF 2025 (environ 0,25 €/kWh).",
            "Les chiffres ci-dessous sont basés sur une utilisation moyenne française et un tarif réglementé EDF 2026 (environ 0,194 €/kWh en option Base, après plusieurs baisses successives).",
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
