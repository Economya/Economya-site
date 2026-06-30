#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction calculateur-frais-notaire.html — barème des émoluments du
notaire légèrement décalé
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE : source officielle confirmée (arrêté du 28 février 2020,
prorogé pour 2026-2028, C. com. art. A444-53) — les 4 taux par tranche
utilisés par l'outil étaient systématiquement trop élevés d'environ 2%
en relatif (probablement un ancien barème ou une confusion de source) :

| Tranche              | Outil (ancien) | Vrai taux officiel |
|-----------------------|----------------|---------------------|
| 0 - 6 500€            | 3,945%         | 3,870%              |
| 6 501 - 17 000€       | 1,627%         | 1,596%              |
| 17 001 - 60 000€      | 1,085%         | 1,064%              |
| Au-delà de 60 000€    | 0,814%         | 0,799%              |

Le taux DMTO de 6,32% utilisé ailleurs dans l'outil est confirmé EXACT
(taux majoré 2025, applicable dans 88 départements sur 101) — non
modifié.

Idempotent. Sauvegarde en .bak_baremenotaire2026.

Usage :
    python3 corriger_frais_notaire_bareme.py
"""

import os

FICHIER = "calculateur-frais-notaire.html"

ANCIEN = """  if(base <= 6500) e = base * 0.03945;
  else if(base <= 17000) e = 6500*0.03945 + (base-6500)*0.01627;
  else if(base <= 60000) e = 6500*0.03945 + 10500*0.01627 + (base-17000)*0.01085;
  else e = 6500*0.03945 + 10500*0.01627 + 43000*0.01085 + (base-60000)*0.00814;"""

NOUVEAU = """  if(base <= 6500) e = base * 0.03870;
  else if(base <= 17000) e = 6500*0.03870 + (base-6500)*0.01596;
  else if(base <= 60000) e = 6500*0.03870 + 10500*0.01596 + (base-17000)*0.01064;
  else e = 6500*0.03870 + 10500*0.01596 + 43000*0.01064 + (base-60000)*0.00799;"""


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
    with open(FICHIER + ".bak_baremenotaire2026", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Barème émoluments notaire corrigé (4 tranches, source: arrêté 28/02/2020 prorogé)")
    print("   DMTO 6,32% confirme deja exact, non modifie")


if __name__ == "__main__":
    main()
