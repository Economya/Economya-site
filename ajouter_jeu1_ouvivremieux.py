#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajoute la carte du nouveau jeu "Où vivre mieux avec votre salaire ?"
dans jeux.html
À lancer depuis ~/Desktop/mon site, APRÈS avoir placé le fichier
ou-vivre-mieux.html dans ce même dossier.

Insertion juste après la carte "Inflation Run" (premier jeu de la
grille), même structure HTML que les cartes existantes.

Idempotent. Sauvegarde en .bak_ajoutjeu1 avant modification.

Usage :
    python3 ajouter_jeu1_ouvivremieux.py
"""

import os

FICHIER = "jeux.html"

ANCRE = """    <a class="game-card" href="inflation-run.html">
      <div class="game-thumb dark">🏃<div class="game-badge hot">🔥 Addictif</div></div>
      <div class="game-info">
        <div class="game-cat">Runner</div>
        <div class="game-title">Inflation Run</div>
        <div class="game-desc">Esquivez les dépenses inutiles et récupérez des économies ! Un runner addictif où chaque décision compte.</div>
        <div class="game-meta"><span class="game-tag">⌨️ Espace / Clic</span><span class="game-tag">⏱️ 2-5 min</span></div>
        <span class="game-btn">▶ Jouer</span>
      </div>
    </a>"""

NOUVELLE_CARTE = """    <a class="game-card" href="inflation-run.html">
      <div class="game-thumb dark">🏃<div class="game-badge hot">🔥 Addictif</div></div>
      <div class="game-info">
        <div class="game-cat">Runner</div>
        <div class="game-title">Inflation Run</div>
        <div class="game-desc">Esquivez les dépenses inutiles et récupérez des économies ! Un runner addictif où chaque décision compte.</div>
        <div class="game-meta"><span class="game-tag">⌨️ Espace / Clic</span><span class="game-tag">⏱️ 2-5 min</span></div>
        <span class="game-btn">▶ Jouer</span>
      </div>
    </a>

    <a class="game-card" href="ou-vivre-mieux.html">
      <div class="game-thumb" style="background:linear-gradient(135deg,#082f49,#0c4a6e,#0891b2)">🏙️<div class="game-badge new">Nouveau</div></div>
      <div class="game-info">
        <div class="game-cat">Comparateur</div>
        <div class="game-title">Où vivre mieux ?</div>
        <div class="game-desc">Comparez votre pouvoir d'achat réel entre 13 grandes villes françaises selon votre salaire.</div>
        <div class="game-meta"><span class="game-tag">📍 13 villes</span><span class="game-tag">⏱️ 1 min</span></div>
        <span class="game-btn">▶ Jouer</span>
      </div>
    </a>"""


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if 'href="ou-vivre-mieux.html"' in contenu:
        print("✅ Déjà ajouté.")
        return
    if ANCRE not in contenu:
        print("⚠️ Ancre non trouvée. Aucune modification.")
        return
    with open(FICHIER + ".bak_ajoutjeu1", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCRE, NOUVELLE_CARTE, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Carte 'Où vivre mieux ?' ajoutée dans jeux.html")


if __name__ == "__main__":
    main()
