#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-229.html (CPF) et article-242.html (forfait hospitalier)
À lancer depuis ~/Desktop/mon site

article-229 : montants annuels CPF (500/800€, plafond 5000/8000€) déjà
confirmés CORRECTS et inchangés pour 2026, non modifiés. Le "reste à
charge" est en revanche largement obsolète : passé de 100€ à 150€
(depuis le 1er avril 2026, +45%, décret application loi de finances 2026).

article-242 : DEUX réformes santé majeures depuis 2026 (sources
officielles, Légifrance) :
- Forfait journalier hospitalier : 20€ -> 23€/jour (depuis le 01/03/2026)
- Participation forfaitaire (actes >120€) : 24€ -> 32€ (depuis le 01/04/2026)

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_article229_242.py
"""

import os

REMPLACEMENTS = {
    "article-229.html": [
        (
            "En 2025, un reste à charge de 100 € est demandé pour les financements directs, sauf prise en charge par l'employeur ou France Travail.",
            "Depuis avril 2026, un reste à charge de 150 € est demandé pour les financements directs (contre 100€ auparavant), sauf prise en charge par l'employeur ou France Travail.",
        ),
    ],
    "article-242.html": [
        (
            '<div class="famount"><span class="amt red">22 €/jour</span><span class="sub">en 2025</span></div>',
            '<div class="famount"><span class="amt red">23 €/jour</span><span class="sub">depuis mars 2026</span></div>',
        ),
        (
            "Depuis 2024, une participation forfaitaire de 24 € s'applique pour toute hospitalisation de moins de 30 jours (hors ALD, maternité, accidents du travail).",
            "Depuis avril 2026, une participation forfaitaire de 32 € s'applique pour tout acte médical supérieur à 120€, y compris en hospitalisation de moins de 30 jours (hors ALD, maternité, accidents du travail).",
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
