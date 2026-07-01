#!/usr/bin/env python3
"""
Corrige le lien cassé de la carte 'Banque en ligne vs traditionnelle'
dans comparateurs.html : pointait vers article-182.html (jardinage),
doit pointer vers article-187.html (Changer de banque et économiser,
qui compare bien Boursobank / Fortuneo / Hello bank).

Idempotent : si le lien est déjà correct, ne fait rien.
Fait une sauvegarde .bak_lienbanque avant modification.
"""

import os
import shutil

FICHIER = "comparateurs.html"

ANCIEN = '<a href="article-182.html" class="comp-card">'
NOUVEAU = '<a href="article-187.html" class="comp-card">'


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    # Lecture
    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    if NOUVEAU in contenu:
        print("✅ Rien à faire — le lien pointe déjà vers article-187.html.")
        return

    if ANCIEN not in contenu:
        print(f"⚠️  Chaîne attendue non trouvée : {ANCIEN}")
        print("   Le fichier a peut-être déjà changé. Vérifiez manuellement.")
        return

    contenu_modifie = contenu.replace(ANCIEN, NOUVEAU, 1)

    # Sauvegarde avant écriture
    shutil.copy2(FICHIER, FICHIER + ".bak_lienbanque")

    # Écriture (opération séparée de la lecture)
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"✅ 1 correction appliquée dans {FICHIER}")
    print(f"   article-182.html (jardinage) -> article-187.html (banques)")
    print(f"   Sauvegarde créée : {FICHIER}.bak_lienbanque")


if __name__ == "__main__":
    main()
