#!/usr/bin/env python3
"""
Corrige le compteur d'outils obsolète dans a-propos.html : 27 -> 30
(mis à jour après l'ajout de calculateur-pouvoir-achat, calculateur-cout-appartement
et calculateur-budget-vacances).

Idempotent : si déjà corrigé, ne fait rien.
Sauvegarde .bak_compteuroutils avant modification.
"""

import os
import shutil

FICHIER = "a-propos.html"

ANCIEN = '''    <div class="stat">
      <span class="stat-num">27</span>
      <div class="stat-lbl">Outils interactifs gratuits</div>
    </div>'''

NOUVEAU = '''    <div class="stat">
      <span class="stat-num">30</span>
      <div class="stat-lbl">Outils interactifs gratuits</div>
    </div>'''


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    if NOUVEAU in contenu:
        print("✅ Rien à faire — le compteur affiche déjà 30.")
        return

    if ANCIEN not in contenu:
        print(f"⚠️  Chaîne attendue non trouvée. Vérifiez manuellement.")
        return

    contenu_modifie = contenu.replace(ANCIEN, NOUVEAU, 1)

    shutil.copy2(FICHIER, FICHIER + ".bak_compteuroutils")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"✅ 1 correction appliquée dans {FICHIER} : 27 -> 30 outils")
    print(f"   Sauvegarde créée : {FICHIER}.bak_compteuroutils")


if __name__ == "__main__":
    main()
