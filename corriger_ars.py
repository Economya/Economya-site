#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-309.html et article-53.html — montant ARS obsolète
À lancer depuis ~/Desktop/mon site

Allocation de Rentrée Scolaire (ARS) 2026 (revalorisée le 1er avril 2026,
confirmé par service-public.gouv.fr) : de 426,87€ (6-10 ans) à 466,02€
(15-18 ans) selon l'âge. Les deux articles citaient des montants obsolètes
(406€ et 416€) qui ne correspondent à aucune année récente réelle.

Idempotent. Sauvegarde en .bak_ars.

Usage :
    python3 corriger_ars.py
"""

import os

REMPLACEMENTS = {
    "article-309.html": [
        (
            "L'Allocation de Rentrée Scolaire (ARS) de la CAF peut atteindre 406 € par enfant scolarisé entre 6 et 18 ans (sous conditions de revenus). Renseignez-vous aussi auprès de votre mairie pour des aides complémentaires.",
            "L'Allocation de Rentrée Scolaire (ARS) de la CAF va de 426,87 € à 466,02 € par enfant selon son âge (6-18 ans, sous conditions de revenus). Renseignez-vous aussi auprès de votre mairie pour des aides complémentaires.",
        ),
        (
            '<span class="s-eco">jusqu\'à 406 €</span><span class="s-sub">ARS par enfant</span>',
            '<span class="s-eco">jusqu\'à 466 €</span><span class="s-sub">ARS par enfant</span>',
        ),
    ],
    "article-53.html": [
        (
            "L'Allocation de Rentrée Scolaire (ARS)</strong> — versée automatiquement par la CAF en août aux familles éligibles. Elle peut atteindre 416 € par enfant en 2025 selon l'âge et les revenus.",
            "L'Allocation de Rentrée Scolaire (ARS)</strong> — versée automatiquement par la CAF en août aux familles éligibles. Elle peut atteindre 466 € par enfant en 2026 selon l'âge et les revenus.",
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

        with open(fichier + ".bak_ars", 'w', encoding='utf-8') as f:
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
