#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-351.html — reste à charge CPF obsolète
À lancer depuis ~/Desktop/mon site

Le reste à charge CPF est passé de 100€ (mai 2024) à 150€ (depuis le
2 avril 2026, décret n° 2026-234 du 30 mars 2026). Le plafond de 5 000€
du compte CPF reste inchangé et correct.

Idempotent. Sauvegarde en .bak_art351.

Usage :
    python3 corriger_article351.py
"""

import os

FICHIER = "article-351.html"

REMPLACEMENTS = [
    (
        "📅 Vérifié mai 2025",
        "📅 Vérifié juin 2026",
    ),
    (
        "Depuis mai 2024, les formations CPF nécessitent un reste à charge de 100 € (sauf exceptions). Malgré cette évolution, le CPF reste un outil puissant pour financer des formations qualifiantes, des bilans de compétences ou des préparations aux concours. Voici ce qui reste accessible en 2025.",
        "Depuis le 2 avril 2026, les formations CPF nécessitent un reste à charge de 150 € (sauf exceptions). Malgré cette évolution, le CPF reste un outil puissant pour financer des formations qualifiantes, des bilans de compétences ou des préparations aux concours. Voici ce qui reste accessible en 2026.",
    ),
    (
        '<span class="stat-num">100 €</span><span class="stat-lbl">reste à charge minimum depuis mai 2024</span>',
        '<span class="stat-num">150 €</span><span class="stat-lbl">reste à charge minimum depuis avril 2026</span>',
    ),
    (
        "<strong>Reste à charge de 100 € obligatoire (depuis mai 2024)</strong><span>Chaque formation CPF nécessite désormais un minimum de 100 € de participation personnelle, sauf exceptions. Objectif : lutter contre les arnaques et valoriser l'investissement personnel dans la formation.</span>",
        "<strong>Reste à charge de 150 € obligatoire (depuis avril 2026)</strong><span>Chaque formation CPF nécessite désormais un minimum de 150 € de participation personnelle, sauf exceptions. Objectif : lutter contre les arnaques et valoriser l'investissement personnel dans la formation.</span>",
    ),
    (
        "Les demandeurs d'emploi, personnes en invalidité et salariés dont l'employeur cofinance n'ont pas à payer les 100 €. Le CPF abondement entreprise efface aussi ce reste à charge.",
        "Les demandeurs d'emploi, personnes en invalidité et salariés dont l'employeur cofinance n'ont pas à payer les 150 €. Le CPF abondement entreprise efface aussi ce reste à charge.",
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

    with open(FICHIER + ".bak_art351", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")


if __name__ == "__main__":
    main()
