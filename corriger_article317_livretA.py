#!/usr/bin/env python3
"""
Corrige article-317.html (Études supérieures des enfants : épargner tôt) :
le Livret A est annoncé à "2,4 % en 2025" — obsolète sur les deux points
(taux ET année). Le taux réel 2026, déjà confirmé ailleurs sur le site
(ex: article-88.html), est de 1,5 %.

Idempotent. Sauvegarde .bak_livretA avant modification.
"""

import os
import shutil

FICHIER = "article-317.html"

ANCIEN = "Simple, 100 % sécurisé, disponible à tout moment. Taux 2,4 % en 2025. Plafond 22 950 €."
NOUVEAU = "Simple, 100 % sécurisé, disponible à tout moment. Taux 1,5 % en 2026. Plafond 22 950 €."

ANCIEN_BADGE = "2,4 %/an garanti"
NOUVEAU_BADGE = "1,5 %/an garanti"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    total = 0

    for ancien, nouveau in [(ANCIEN, NOUVEAU), (ANCIEN_BADGE, NOUVEAU_BADGE)]:
        if ancien in contenu_modifie:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau, 1)
            print(f"✅ Corrigé : {ancien[:50]}...")
            total += 1
        elif nouveau in contenu_modifie:
            print(f"ℹ️  Déjà corrigé (idempotent) : {nouveau[:50]}...")
        else:
            print(f"⚠️  Chaîne non trouvée : {ancien[:50]}...")

    if total == 0:
        print("✅ Rien à faire.")
        return

    shutil.copy2(FICHIER, FICHIER + ".bak_livretA")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"\n✅ {total} correction(s) appliquée(s) dans {FICHIER}")
    print(f"   Sauvegarde créée : {FICHIER}.bak_livretA")


if __name__ == "__main__":
    main()
