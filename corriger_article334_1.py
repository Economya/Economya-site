#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-334.html — TVA photovoltaïque, prime autoconsommation, lien croisé
À lancer depuis ~/Desktop/mon site

1. TVA 10% pour le photovoltaïque -> obsolète depuis le 1er janvier 2026
   (remplacée par 5,5% sous conditions strictes, ou 20% sinon)
2. Prime autoconsommation "jusqu'à 500€/kWc" -> formulation prudente
   (montant et statut même du dispositif incertains à la date de
   rédaction, sources contradictoires sur une possible suppression
   en 2026 — renvoi vers vérification officielle)
3. Lien croisé daté vers article-322 : 2025 -> 2026

Idempotent. Sauvegarde en .bak_art334.

Usage :
    python3 corriger_article334.py
"""

import os

FICHIER = "article-334.html"

REMPLACEMENTS = [
    (
        "MaPrimeRénov' (panneaux solaires thermiques), TVA à 10 % pour les installations photovoltaïques, prime à l'autoconsommation (jusqu'à 500 €/kWc). Vérifiez votre éligibilité sur maprimerenov.gouv.fr avant de signer.",
        "MaPrimeRénov' (panneaux solaires thermiques uniquement, pas le photovoltaïque). Pour le photovoltaïque : TVA réduite à 5,5 % sous conditions strictes depuis 2026 (20 % sinon, le taux de 10 % n'existe plus), et prime à l'autoconsommation dont le montant évolue chaque trimestre — vérifiez le taux actuel et l'existence du dispositif sur le site officiel EDF OA avant de signer.",
    ),
    (
        '<div class="sim-card-title">Pompe à chaleur :aides et rentabilité 2025</div>',
        '<div class="sim-card-title">Pompe à chaleur :aides et rentabilité 2026</div>',
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

    with open(FICHIER + ".bak_art334", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   TVA 10%->5,5%/20%, prime autoconso prudente, lien croise 2026")


if __name__ == "__main__":
    main()
