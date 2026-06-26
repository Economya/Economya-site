#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-463.html — dates des exemples illustratifs (méthode
SMART)
À lancer depuis ~/Desktop/mon site

Contenu pédagogique (exemples d'objectifs SMART), pas de chiffre
réglementé. Les dates sont avancées d'un an pour rester pertinentes.

Idempotent. Sauvegarde en .bak_art463.

Usage :
    python3 corriger_article463.py
"""

import os

FICHIER = "article-463.html"

REMPLACEMENTS = [
    (
        '<div class="si-desc">Une date limite précise. "D\'ici au 31 décembre 2025".</div>',
        '<div class="si-desc">Une date limite précise. "D\'ici au 31 décembre 2026".</div>',
    ),
    (
        '<div class="ex-good">"Constituer 4 200 € sur Livret A d\'ici le 31 décembre 2025 via virement automatique de 350 €/mois dès le 1er du mois"</div>',
        '<div class="ex-good">"Constituer 4 200 € sur Livret A d\'ici le 31 décembre 2026 via virement automatique de 350 €/mois dès le 1er du mois"</div>',
    ),
    (
        '<div class="ex-good">"Ouvrir un PEA avant le 30 juin 2025, y déposer 100 € initialement, puis 100 €/mois sur un ETF MSCI World"</div>',
        '<div class="ex-good">"Ouvrir un PEA avant le 30 juin 2026, y déposer 100 € initialement, puis 100 €/mois sur un ETF MSCI World"</div>',
    ),
    (
        '<div class="ex-plan">Plan : 3 600 € ÷ 12 = 300 €/mois supplémentaires dès janvier 2025</div>',
        '<div class="ex-plan">Plan : 3 600 € ÷ 12 = 300 €/mois supplémentaires dès janvier 2026</div>',
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

    with open(FICHIER + ".bak_art463", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")


if __name__ == "__main__":
    main()
