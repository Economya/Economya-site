#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-357.html — recalcul complet du tableau des salaires
apprenti (base SMIC obsolète)
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE : la note de bas de tableau avait déjà été mise à jour
("SMIC brut 2026 : ~1 867€") mais TOUTES les valeurs en euros du tableau
restaient calculées sur l'ancien SMIC (1752€) — confirmé par recalcul
exact (27%×1752=473€, 39%×1752=683€, etc., correspondant pile aux
anciennes valeurs). Tout le tableau est recalculé avec le SMIC 2026
(1867€).

Idempotent. Sauvegarde en .bak_art357smic.

Usage :
    python3 corriger_article357_smic.py
"""

import os

FICHIER = "article-357.html"

REMPLACEMENTS = [
    (
        "💶 Les salaires de l'apprenti en 2025",
        "💶 Les salaires de l'apprenti en 2026",
    ),
    (
        '<tr><td>CAP / BEP (jusqu\'à 17 ans)</td><td>—</td><td class="g">27 % SMIC (~473 €)</td><td class="g">39 % SMIC (~683 €)</td><td>—</td></tr>',
        '<tr><td>CAP / BEP (jusqu\'à 17 ans)</td><td>—</td><td class="g">27 % SMIC (~504 €)</td><td class="g">39 % SMIC (~728 €)</td><td>—</td></tr>',
    ),
    (
        '<tr><td>CAP / BEP (18–20 ans)</td><td>—</td><td class="g">43 % SMIC (~754 €)</td><td class="g">51 % SMIC (~893 €)</td><td>—</td></tr>',
        '<tr><td>CAP / BEP (18–20 ans)</td><td>—</td><td class="g">43 % SMIC (~803 €)</td><td class="g">51 % SMIC (~952 €)</td><td>—</td></tr>',
    ),
    (
        '<tr><td>Bac Pro / BTS (21–25 ans)</td><td>—</td><td class="g">53 % SMIC (~929 €)</td><td class="g">61 % SMIC (~1 069 €)</td><td class="g">78 % SMIC (~1 367 €)</td></tr>',
        '<tr><td>Bac Pro / BTS (21–25 ans)</td><td>—</td><td class="g">53 % SMIC (~990 €)</td><td class="g">61 % SMIC (~1 139 €)</td><td class="g">78 % SMIC (~1 456 €)</td></tr>',
    ),
    (
        '<tr><td>Master / Ingénieur (25 ans +)</td><td>100 % SMIC min.</td><td class="g">100 % SMIC (~1 752 €)</td><td class="g">100 % SMIC</td><td>—</td></tr>',
        '<tr><td>Master / Ingénieur (25 ans +)</td><td>100 % SMIC min.</td><td class="g">100 % SMIC (~1 867 €)</td><td class="g">100 % SMIC</td><td>—</td></tr>',
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

    with open(FICHIER + ".bak_art357smic", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Tableau SMIC apprenti entierement recalcule sur base 1867e")


if __name__ == "__main__":
    main()
