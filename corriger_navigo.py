#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du prix du Pass Navigo dans calculateur-cout-voiture.html
À lancer depuis ~/Desktop/mon site

Le prix mensuel officiel 2026 du Pass Navigo (source : Île-de-France Mobilités,
Service Public, janvier 2026) est de 90,80€, pas 88€ (ancien tarif 2025: 88,80€).

Idempotent. Sauvegarde en .bak_navigo.
"""
import os

FICHIER = "calculateur-cout-voiture.html"
ANCIEN = "Pass Navigo : 88 €/mois"
NOUVEAU = "Pass Navigo : 90,80 €/mois"

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
    with open(FICHIER + ".bak_navigo", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    print("✅ Prix Pass Navigo corrigé : 88€ -> 90,80€/mois (tarif officiel 2026)")

if __name__ == "__main__":
    main()
