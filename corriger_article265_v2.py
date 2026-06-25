#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-265.html (2e passage) — 3 points manqués au 1er passage
À lancer depuis ~/Desktop/mon site

1. Fil d'Ariane (breadcrumb visuel + JSON-LD) : "2025" -> "2026"
2. Prix Carte Liberté "399 €" -> "349 €" (le 1er script avait un motif
   trop spécifique qui ne correspondait pas exactement au fichier réel)
3. Titre de l'encart "L'abonnement TGV Max : pour les moins de 30 ans"
   -> corrigé pour refléter les deux vrais abonnements (MAX JEUNE 16-27
   ans ET MAX SENIOR 60 ans+, pas juste "moins de 30 ans")

Idempotent. Sauvegarde en .bak_art265v2.

Usage :
    python3 corriger_article265_v2.py
"""

import os

FICHIER = "article-265.html"

REMPLACEMENTS = [
    (
        '<span style="color:var(--t,#2C2C2A)">Train pas cher : cartes SNCF et astuces 2025</span>',
        '<span style="color:var(--t,#2C2C2A)">Train pas cher : cartes SNCF et astuces 2026</span>',
    ),
    (
        '"name": "Train pas cher : cartes SNCF et astuces 2025", "item": "https://economya.fr/article-265.html"',
        '"name": "Train pas cher : cartes SNCF et astuces 2026", "item": "https://economya.fr/article-265.html"',
    ),
    (
        '<div class="carte-price">399 €</div>',
        '<div class="carte-price">349 €</div>',
    ),
    (
        "💡 L'abonnement TGV Max : pour les moins de 30 ans",
        "💡 Les abonnements MAX JEUNE et MAX SENIOR : voyager illimité à -30%",
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

    with open(FICHIER + ".bak_art265v2", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Fil d'Ariane 2026, prix Liberte 349e, titre encart corrige")


if __name__ == "__main__":
    main()
