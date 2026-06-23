#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du taux DMTO "terrain" dans calculateur-frais-notaire.html
À lancer APRÈS corriger_notaire.py, depuis ~/Desktop/mon site

Le bloc "Terrain" utilisait encore l'ancien taux 5,80%, non corrigé par
le script précédent qui ne ciblait que le bloc "ancien". Les terrains
suivent le même régime DMTO que l'ancien -> même correction (6,32%).

Idempotent. Sauvegarde en .bak_notaire_terrain.
"""
import os

FICHIER = "calculateur-frais-notaire.html"
ANCIEN = """  } else {
    taxes = base * 0.0580;
    tauxTotal = 8;
    typeLabel = 'Terrain';
  }"""
NOUVEAU = """  } else {
    taxes = base * 0.0632; // taux majore 2026, meme regime DMTO que l'ancien
    tauxTotal = 8.5;
    typeLabel = 'Terrain';
  }"""

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
        print("⚠️ Bloc attendu non trouvé. Vérifie manuellement.")
        return
    with open(FICHIER + ".bak_notaire_terrain", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    print("✅ Taux DMTO terrain corrigé : 5,80% -> 6,32%")

if __name__ == "__main__":
    main()
