#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suppression de la ligne "Salto" (service fermé en mars 2023) dans checklist-abonnements.html
À lancer depuis ~/Desktop/mon site

Salto a définitivement fermé le 27 mars 2023 (TF1, M6, France Télévisions).
Le proposer comme abonnement à suivre/couper est une erreur factuelle.

Idempotent. Sauvegarde en .bak_salto.
"""
import os

FICHIER = "checklist-abonnements.html"
ANCIEN = "    { nom: 'Salto', detail: 'TV française', prix: 6.99 },\n"
NOUVEAU = ""

def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if ANCIEN not in contenu:
        if "'Salto'" not in contenu:
            print("✅ Déjà corrigé (Salto absent).")
        else:
            print("⚠️ Ligne Salto trouvée sous une forme différente. Vérifie manuellement.")
        return
    with open(FICHIER + ".bak_salto", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    print("✅ Ligne 'Salto' supprimée (service fermé depuis mars 2023)")

if __name__ == "__main__":
    main()
