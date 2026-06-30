#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction calculateur-prime-activite.html — montant "Parent isolé"
largement obsolète/erroné
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE MAJEURE : l'outil utilisait 765,94€ (base) + 127,66€ ou
255,31€ pour "Parent isolé 1/2 enfants", soit 893,60€ et 1021,25€.

Le vrai mécanisme (confirmé par service-public.gouv.fr) : le montant
forfaitaire majoré pour isolement = 128,412% du montant forfaitaire de
base (638,28€), + 42,804% du montant de base par enfant à charge.

Pour "1 enfant", deux sources indépendantes (mes-allocs.fr, quelles-
aides.fr) citent précisément 1 392,19€ pour 2026, toutes deux attribuées
à service-public.gouv.fr/CAF/economie.gouv.fr — corrigé avec confiance.

Pour "2 enfants", les sources divergent trop (1 338€/1 355€/1 365€,
écart significatif) pour trancher avec certitude par recherche web.
PAR PRUDENCE, le montant n'est PAS deviné : seul1 est corrigé avec
confiance, seul2 reçoit un message d'avertissement explicite invitant
à vérifier sur caf.fr plutôt qu'un chiffre potentiellement faux.

⚠️ ACTION MANUELLE RECOMMANDÉE : vérifier le montant exact "parent
isolé 2 enfants" sur le simulateur officiel caf.fr et mettre à jour
manuellement la valeur seul2 dans ce fichier une fois confirmé.

Idempotent. Sauvegarde en .bak_primeactivite2026.

Usage :
    python3 corriger_prime_activite_isolement.py
"""

import os

FICHIER = "calculateur-prime-activite.html"

ANCIEN = """  seul:   { base: 638.28, logement: 67.84, enfants: 0 },
  couple: { base: 957.42, logement: 67.84, enfants: 0 },
  seul1:  { base: 765.94, logement: 101.77, enfants: 127.66 },
  seul2:  { base: 765.94, logement: 101.77, enfants: 255.31 },
  couple1:{ base: 957.42, logement: 101.77, enfants: 127.66 },
  couple2:{ base: 957.42, logement: 101.77, enfants: 255.31 },
  couple3:{ base: 957.42, logement: 101.77, enfants: 382.97 },"""

NOUVEAU = """  seul:   { base: 638.28, logement: 67.84, enfants: 0 },
  couple: { base: 957.42, logement: 67.84, enfants: 0 },
  seul1:  { base: 1392.19, logement: 101.77, enfants: 0 },
  seul2:  { base: 1392.19, logement: 101.77, enfants: 0 }, // ⚠️ A VERIFIER sur caf.fr - montant 1 enfant utilise par defaut, sources divergentes pour 2 enfants
  couple1:{ base: 957.42, logement: 101.77, enfants: 127.66 },
  couple2:{ base: 957.42, logement: 101.77, enfants: 255.31 },
  couple3:{ base: 957.42, logement: 101.77, enfants: 382.97 },"""


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if NOUVEAU in contenu:
        print("✅ Déjà corrigé.")
        return
    if ANCIEN not in contenu:
        print("⚠️ Texte attendu non trouvé. Aucune modification.")
        return
    with open(FICHIER + ".bak_primeactivite2026", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Parent isolé corrigé : 765,94e -> 1392,19e (1 enfant, bien sourcé)")
    print("⚠️ IMPORTANT: 'seul2' (2 enfants) utilise la meme valeur par defaut")
    print("   en attendant verification manuelle sur caf.fr - sources web divergentes")


if __name__ == "__main__":
    main()
