#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-322.html — dates obsolètes + erreur montant MaPrimeRénov
À lancer depuis ~/Desktop/mon site

1. Dates 2025 -> 2026 (titre, meta, h1)
2. Erreur corrigée : l'exemple disait "MaPrimeRénov' (revenus moyens) : −5 000€"
   alors que 5 000€ correspond aux revenus TRÈS MODESTES pour une PAC air/eau
   (source officielle economie.gouv.fr 2026). Pour "revenus moyens"
   (intermédiaire), le bon montant est 3 000€. Cascade recalculée :
   reste à charge 5 500€ -> 7 500€, ROI ~6 ans -> ~8 ans.

Le chiffre "4 000-11 000€ selon revenus et type" (badge général) reste
correct et n'est pas modifié — il couvre bien la fourchette PAC air/eau
(jusqu'à 5 000€) à PAC géothermique (jusqu'à 11 000€).

Idempotent. Sauvegarde en .bak_art322.

Usage :
    python3 corriger_article322.py
"""

import os

FICHIER = "article-322.html"

REMPLACEMENTS = [
    (
        "Pompe à chaleur : aides et rentabilité 2025 — MaPrimeRénov' jusqu'à 11 000€. Guide complet sur Economya.fr",
        "Pompe à chaleur : aides et rentabilité 2026 — MaPrimeRénov' jusqu'à 11 000€. Guide complet sur Economya.fr",
    ),
    (
        "Pompe à chaleur : aides et rentabilité 2025 — Economya.fr",
        "Pompe à chaleur : aides et rentabilité 2026 — Economya.fr",
    ),
    (
        '"headline": "Pompe à chaleur : aides et rentabilité 2025",',
        '"headline": "Pompe à chaleur : aides et rentabilité 2026",',
    ),
    (
        '<h1>Pompe à chaleur :<br><em>aides et rentabilité 2025</em></h1>',
        '<h1>Pompe à chaleur :<br><em>aides et rentabilité 2026</em></h1>',
    ),
    (
        '<meta property="og:title" content="Pompe à chaleur : aides et rentabilité 2025">',
        '<meta property="og:title" content="Pompe à chaleur : aides et rentabilité 2026">',
    ),
    (
        '<meta name="twitter:title" content="Pompe à chaleur : aides et rentabilité 2025">',
        '<meta name="twitter:title" content="Pompe à chaleur : aides et rentabilité 2026">',
    ),
    (
        "💶 Les aides financières disponibles en 2025",
        "💶 Les aides financières disponibles en 2026",
    ),
    (
        '<div class="renta-label">MaPrimeRénov\' (revenus moyens)</div><div class="renta-val">−5 000 €</div>',
        '<div class="renta-label">MaPrimeRénov\' (revenus moyens)</div><div class="renta-val">−3 000 €</div>',
    ),
    (
        '<div class="renta-label">Reste à charge</div><div class="renta-val">5 500 €</div>',
        '<div class="renta-label">Reste à charge</div><div class="renta-val">7 500 €</div>',
    ),
    (
        '<div class="renta-label">Retour sur investissement</div><div class="renta-val">~6 ans</div>',
        '<div class="renta-label">Retour sur investissement</div><div class="renta-val">~8 ans</div>',
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

    with open(FICHIER + ".bak_art322", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2025->2026, et erreur MaPrimeRénov corrigée :")
    print("   5 000€ -> 3 000€ (revenus moyens), cascade recalculée")


if __name__ == "__main__":
    main()
