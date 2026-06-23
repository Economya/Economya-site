#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du taux DMTO "ancien" dans calculateur-frais-notaire.html
À lancer depuis ~/Desktop/mon site

Depuis la loi de finances 2025, la majorité des départements ont relevé
leur taux de DMTO de 4,5% à 5%, faisant passer le taux global de 5,80%
à 6,32% dans ces départements (qui sont majoritaires en 2026).
Le fichier utilisait encore l'ancien taux à 5,80%.

On utilise 6,32% (taux majoré, désormais le plus répandu) comme valeur
par défaut la plus représentative, avec ajustement du taux total affiché.

Idempotent. Sauvegarde en .bak_notaire.
"""
import os

FICHIER = "calculateur-frais-notaire.html"
ANCIEN = """  if(typeActuel === 'ancien') {
    taxes = base * 0.0580; // ~5.80% droits mutation ancien
    tauxTotal = 7.5;
    typeLabel = 'Ancien';
  } else if(typeActuel === 'neuf') {"""
NOUVEAU = """  if(typeActuel === 'ancien') {
    taxes = base * 0.0632; // ~6,32% droits mutation ancien (taux majore 2026, majorite des departements)
    tauxTotal = 8;
    typeLabel = 'Ancien';
  } else if(typeActuel === 'neuf') {"""

def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if "0.0632" in contenu:
        print("✅ Déjà corrigé.")
        return
    if ANCIEN not in contenu:
        print("⚠️ Bloc attendu non trouvé. Aucune modification.")
        return
    with open(FICHIER + ".bak_notaire", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    print("✅ Taux DMTO ancien corrigé : 5,80% -> 6,32% (taux majoré 2026, majoritaire)")
    print("   ⚠️ Certains départements (minoritaires) sont restés à 5,81% — l'outil indique une estimation, pas un calcul garanti par département.")

if __name__ == "__main__":
    main()
