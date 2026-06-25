#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-497.html (2e passage) — 3e occurrence du plafond PER
obsolète + dates restantes
À lancer depuis ~/Desktop/mon site

Le plafond cité ("35 194€") correspondait exactement au calcul avec le
PASS 2023 (43 992€ × 8 × 10%) — une 3e version obsolète du même chiffre
déjà corrigée 2 fois ailleurs aujourd'hui. Plafond 2026 confirmé : 37 680€.
Réduction IR maximale recalculée à TMI 45% : 37 680 × 45% = 16 956€
(au lieu de 14 478€, qui ne correspondait à aucun calcul cohérent avec
l'ancien plafond non plus).

Idempotent. Sauvegarde en .bak_art497v2.

Usage :
    python3 corriger_article497_v2.py
"""

import os

FICHIER = "article-497.html"

REMPLACEMENTS = [
    (
        "Défiscalisation : toutes les niches légales 2025 — Réduisez votre impôt de 30%. Guide complet sur Economya.fr",
        "Défiscalisation : toutes les niches légales 2026 — Réduisez votre impôt de 30%. Guide complet sur Economya.fr",
    ),
    (
        "<title>Défiscalisation : toutes les niches légales 2025 — Economya.fr</title>",
        "<title>Défiscalisation : toutes les niches légales 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Défiscalisation : toutes les niches légales 2025",',
        '"headline": "Défiscalisation : toutes les niches légales 2026",',
    ),
    (
        '<meta property="og:title" content="Défiscalisation : toutes les niches légales 2025">',
        '<meta property="og:title" content="Défiscalisation : toutes les niches légales 2026">',
    ),
    (
        '<meta name="twitter:title" content="Défiscalisation : toutes les niches légales 2025">',
        '<meta name="twitter:title" content="Défiscalisation : toutes les niches légales 2026">',
    ),
    (
        "<h1>Défiscalisation :<br><em>toutes les niches légales 2025</em></h1>",
        "<h1>Défiscalisation :<br><em>toutes les niches légales 2026</em></h1>",
    ),
    (
        "💰 Les niches fiscales les plus accessibles en 2025",
        "💰 Les niches fiscales les plus accessibles en 2026",
    ),
    (
        "Les versements sur un PER individuel ou collectif sont déductibles du revenu imposable dans la limite de 10 % des revenus professionnels nets N-1 (plafond 2025 : 35 194 €). À TMI 30 %, chaque 1 000 € versé réduit l'impôt de 300 €. Pour les TNS (indépendants), le plafond est encore plus élevé (loi Madelin).",
        "Les versements sur un PER individuel ou collectif sont déductibles du revenu imposable dans la limite de 10 % des revenus professionnels nets N-1 (plafond 2026 : 37 680 €). À TMI 30 %, chaque 1 000 € versé réduit l'impôt de 300 €. Pour les TNS (indépendants), le plafond est encore plus élevé (loi Madelin).",
    ),
    (
        '<span class="ntag g">Déduction immédiate</span><span class="ntag">TMI 30 % → −30 % d\'impôt</span><span class="ntag g">Plafond 35 194 €</span>',
        '<span class="ntag g">Déduction immédiate</span><span class="ntag">TMI 30 % → −30 % d\'impôt</span><span class="ntag g">Plafond 37 680 €</span>',
    ),
    (
        '<span class="n-gain">Jusqu\'à 14 478 €</span><span class="n-sub">de réduction IR/an</span>',
        '<span class="n-gain">Jusqu\'à 16 956 €</span><span class="n-sub">de réduction IR/an</span>',
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

    with open(FICHIER + ".bak_art497v2", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Plafond PER 35194e->37680e, reduction max recalculee 16956e, dates 2026")


if __name__ == "__main__":
    main()
