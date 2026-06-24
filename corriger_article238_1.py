#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-238.html — montant AAH obsolète + dates
À lancer depuis ~/Desktop/mon site

Le montant AAH était à 1 016,05€/mois (avant avril 2025) — le montant
actuel (depuis le 1er avril 2026, décret n°2026-229 du 30 mars 2026) est
1 041,59€/mois, confirmé par de nombreuses sources convergentes officielles.

Idempotent. Sauvegarde en .bak_art238.

Usage :
    python3 corriger_article238.py
"""

import os

FICHIER = "article-238.html"

REMPLACEMENTS = [
    (
        "Allocation adulte handicapé (AAH) 2025 — Jusqu'à 1 016€/mois. Guide complet sur Economya.fr",
        "Allocation adulte handicapé (AAH) 2026 — Jusqu'à 1 041€/mois. Guide complet sur Economya.fr",
    ),
    (
        "Allocation adulte handicapé (AAH) 2025",
        "Allocation adulte handicapé (AAH) 2026",
    ),
    (
        "<h1>Allocation adulte handicapé :<br><em>vos droits en 2025</em></h1>",
        "<h1>Allocation adulte handicapé :<br><em>vos droits en 2026</em></h1>",
    ),
    (
        "💰 Jusqu'à 1 016 €/mois",
        "💰 Jusqu'à 1 041 €/mois",
    ),
    (
        "📅 Vérifié mai 2025",
        "📅 Vérifié juin 2026",
    ),
    (
        "L'AAH est l'une des aides les plus importantes du système social français — et l'une des moins bien connues. En 2025, son montant maximal atteint 1 016,05 € par mois. Voici comment savoir si vous y avez droit et comment la demander.",
        "L'AAH est l'une des aides les plus importantes du système social français — et l'une des moins bien connues. En 2026, son montant maximal atteint 1 041,59 € par mois. Voici comment savoir si vous y avez droit et comment la demander.",
    ),
    (
        '<span class="stat-num">1 016 €</span><span class="stat-lbl">montant maximum/mois</span>',
        '<span class="stat-num">1 041 €</span><span class="stat-lbl">montant maximum/mois</span>',
    ),
    (
        "<th>Montant 2025</th>",
        "<th>Montant 2026</th>",
    ),
    (
        '<td class="g">1 016,05 €/mois</td>',
        '<td class="g">1 041,59 €/mois</td>',
    ),
    (
        '<td class="o">jusqu\'à 1 016,05 €/mois</td>',
        '<td class="o">jusqu\'à 1 041,59 €/mois</td>',
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

    with open(FICHIER + ".bak_art238", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Montant AAH corrigé : 1 016,05€ -> 1 041,59€/mois")


if __name__ == "__main__":
    main()
