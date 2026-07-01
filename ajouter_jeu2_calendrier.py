#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajoute la carte du nouveau jeu "Le Calendrier des Bons Plans 2026"
dans jeux.html
À lancer depuis ~/Desktop/mon site, APRÈS avoir placé le fichier
calendrier-bons-plans.html dans ce même dossier ET après avoir déjà
ajouté la carte "Où vivre mieux ?" (ajouter_jeu1_ouvivremieux.py).

Insertion juste après la carte "Où vivre mieux ?".

Idempotent. Sauvegarde en .bak_ajoutjeu2 avant modification.

Usage :
    python3 ajouter_jeu2_calendrier.py
"""

import os

FICHIER = "jeux.html"

ANCRE = """    <a class="game-card" href="ou-vivre-mieux.html">
      <div class="game-thumb" style="background:linear-gradient(135deg,#082f49,#0c4a6e,#0891b2)">🏙️<div class="game-badge new">Nouveau</div></div>
      <div class="game-info">
        <div class="game-cat">Comparateur</div>
        <div class="game-title">Où vivre mieux ?</div>
        <div class="game-desc">Comparez votre pouvoir d'achat réel entre 13 grandes villes françaises selon votre salaire.</div>
        <div class="game-meta"><span class="game-tag">📍 13 villes</span><span class="game-tag">⏱️ 1 min</span></div>
        <span class="game-btn">▶ Jouer</span>
      </div>
    </a>"""

NOUVELLE_CARTE = """    <a class="game-card" href="ou-vivre-mieux.html">
      <div class="game-thumb" style="background:linear-gradient(135deg,#082f49,#0c4a6e,#0891b2)">🏙️<div class="game-badge new">Nouveau</div></div>
      <div class="game-info">
        <div class="game-cat">Comparateur</div>
        <div class="game-title">Où vivre mieux ?</div>
        <div class="game-desc">Comparez votre pouvoir d'achat réel entre 13 grandes villes françaises selon votre salaire.</div>
        <div class="game-meta"><span class="game-tag">📍 13 villes</span><span class="game-tag">⏱️ 1 min</span></div>
        <span class="game-btn">▶ Jouer</span>
      </div>
    </a>

    <a class="game-card" href="calendrier-bons-plans.html">
      <div class="game-thumb" style="background:linear-gradient(135deg,#4a1d96,#7c3aed,#a855f7)">📅<div class="game-badge new">Nouveau</div></div>
      <div class="game-info">
        <div class="game-cat">Calendrier</div>
        <div class="game-title">Calendrier des Bons Plans</div>
        <div class="game-desc">La meilleure astuce pour économiser chaque mois de l'année 2026 : soldes, impôts, Black Friday...</div>
        <div class="game-meta"><span class="game-tag">📅 12 mois</span><span class="game-tag">⏱️ 1 min</span></div>
        <span class="game-btn">▶ Jouer</span>
      </div>
    </a>"""


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if 'href="calendrier-bons-plans.html"' in contenu:
        print("✅ Déjà ajouté.")
        return
    if ANCRE not in contenu:
        print("⚠️ Ancre non trouvée (le jeu 1 a-t-il bien été ajouté avant ?). Aucune modification.")
        return
    with open(FICHIER + ".bak_ajoutjeu2", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCRE, NOUVELLE_CARTE, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Carte 'Calendrier des Bons Plans' ajoutée dans jeux.html")


if __name__ == "__main__":
    main()
