#!/usr/bin/env python3
"""
Intègre le nouvel outil "Calculateur pouvoir d'achat réel" dans outils-gratuits.html :
1. Ajoute une carte dans la section "🎯 Profil, Habitudes & Voyage" (avant ADN Financier).
2. Met à jour le compteur 27 -> 28 outils disponibles.

Idempotent : si déjà fait, ne fait rien.
Sauvegarde .bak_ajoutpouvoirachat avant modification.
"""

import os
import shutil

FICHIER = "outils-gratuits.html"

ANCRE = '''      <span class="tool-btn">Faire le quiz →</span>
    </a>
    <a href="adn-financier.html" class="tool-card featured">'''

NOUVELLE_CARTE = '''      <span class="tool-btn">Faire le quiz →</span>
    </a>
    <a href="calculateur-pouvoir-achat.html" class="tool-card">
      <span class="viral-badge">🆕 Nouveau</span>
      <span class="tool-icon">📉</span>
      <div class="tool-cat">Calculateur</div>
      <div class="tool-name">Pouvoir d'achat réel</div>
      <div class="tool-desc">Votre salaire a-t-il vraiment augmenté ? Comparez à l'inflation réelle INSEE.</div>
      <span class="tool-btn">Calculer →</span>
    </a>
    <a href="adn-financier.html" class="tool-card featured">'''

COMPTEUR_ANCIEN = '<div class="stat"><span class="stat-num">27</span><div class="stat-lbl">Outils disponibles</div></div>'
COMPTEUR_NOUVEAU = '<div class="stat"><span class="stat-num">28</span><div class="stat-lbl">Outils disponibles</div></div>'


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    corrections = 0

    if ANCRE in contenu_modifie:
        contenu_modifie = contenu_modifie.replace(ANCRE, NOUVELLE_CARTE, 1)
        corrections += 1
        print("✅ Carte 'Pouvoir d'achat réel' ajoutée")
    elif 'calculateur-pouvoir-achat.html' in contenu_modifie:
        print("ℹ️  Carte déjà présente (idempotent)")
    else:
        print("⚠️  Ancre non trouvée pour l'ajout de la carte — vérifiez manuellement")

    if COMPTEUR_ANCIEN in contenu_modifie:
        contenu_modifie = contenu_modifie.replace(COMPTEUR_ANCIEN, COMPTEUR_NOUVEAU, 1)
        corrections += 1
        print("✅ Compteur mis à jour : 27 -> 28")
    elif COMPTEUR_NOUVEAU in contenu_modifie:
        print("ℹ️  Compteur déjà à jour (idempotent)")
    else:
        print("⚠️  Compteur non trouvé — vérifiez manuellement")

    if corrections == 0:
        print("✅ Rien à faire — le fichier est déjà à jour.")
        return

    shutil.copy2(FICHIER, FICHIER + ".bak_ajoutpouvoirachat")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"\n✅ {corrections} modification(s) écrite(s) dans {FICHIER}")
    print(f"   Sauvegarde créée : {FICHIER}.bak_ajoutpouvoirachat")


if __name__ == "__main__":
    main()
