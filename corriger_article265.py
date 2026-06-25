#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-265.html — prix carte Liberté + nom erroné + dates
À lancer depuis ~/Desktop/mon site

Confirmé par SNCF Voyageurs (source officielle) :
1. Carte Liberté : 349€/an (l'article disait 399€, erreur)
2. "TGV Max (anciennement OuiGo Max)" : aucune trace de ce renommage —
   les vrais noms sont "MAX JEUNE" et "MAX SENIOR" (79€/mois chacun,
   confirmé exact). Le terme "TGV Max" et l'historique "anciennement
   OuiGo Max" semblent erronés, corrigés ici.
3. Dates 2025->2026

Note : Carte Avantage (49€, -30%/-60%) déjà exacte, non modifiée.

Idempotent. Sauvegarde en .bak_art265.

Usage :
    python3 corriger_article265.py
"""

import os

FICHIER = "article-265.html"

REMPLACEMENTS = [
    (
        "Train pas cher : cartes SNCF et astuces 2025 — jusqu'à -50% sur chaque billet. Guide complet sur Economya.fr",
        "Train pas cher : cartes SNCF et astuces 2026 — jusqu'à -50% sur chaque billet. Guide complet sur Economya.fr",
    ),
    (
        "<title>Train pas cher : cartes SNCF et astuces 2025 — Economya.fr</title>",
        "<title>Train pas cher : cartes SNCF et astuces 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Train pas cher : cartes SNCF et astuces 2025",',
        '"headline": "Train pas cher : cartes SNCF et astuces 2026",',
    ),
    (
        '<meta property="og:title" content="Train pas cher : cartes SNCF et astuces 2025">',
        '<meta property="og:title" content="Train pas cher : cartes SNCF et astuces 2026">',
    ),
    (
        '<meta name="twitter:title" content="Train pas cher : cartes SNCF et astuces 2025">',
        '<meta name="twitter:title" content="Train pas cher : cartes SNCF et astuces 2026">',
    ),
    (
        "<h1>Train pas cher :<br><em>cartes SNCF et astuces 2025</em></h1>",
        "<h1>Train pas cher :<br><em>cartes SNCF et astuces 2026</em></h1>",
    ),
    (
        "🎫 Les cartes de réduction SNCF 2025",
        "🎫 Les cartes de réduction SNCF 2026",
    ),
    (
        '<div class="carte-price">399 €</div>\n      <div class="carte-remise">−50 % sur trajet choisi</div>',
        '<div class="carte-price">349 €</div>\n      <div class="carte-remise">−50 % sur trajet choisi</div>',
    ),
    (
        "TGV Max (anciennement OuiGo Max) à 79 €/mois permet de voyager en TGV et Intercités illimité sous réserve de disponibilité. Rentable dès 2 à 3 voyages par mois. Idéal pour les étudiants ou jeunes actifs qui voyagent fréquemment.",
        "Les abonnements MAX JEUNE (16-27 ans) et MAX SENIOR (60 ans et +) à 79 €/mois donnent -30% garantis toute l'année sur TGV INOUI et Intercités, avec des réservations à 0€ selon disponibilité. Rentable dès 2 à 3 voyages par mois. Idéal pour les étudiants ou jeunes actifs qui voyagent fréquemment.",
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

    with open(FICHIER + ".bak_art265", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Carte Liberte 399e->349e, nom MAX JEUNE/SENIOR corrige, dates 2026")


if __name__ == "__main__":
    main()
