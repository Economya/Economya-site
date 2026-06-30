#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du lien d'affiliation Flightright dans article-276.html
(Flying Blue, Miles&More)
À lancer depuis ~/Desktop/mon site

Ajoute un nouveau bloc <div class="tip"> juste avant la newsletter,
mentionnant Flightright dans le contexte naturel d'un vol annulé ou
retardé (situation où les miles ne servent à rien, mais où une
indemnisation légale est due).

Lien tracké Awin confirmé :
https://www.awin1.com/cread.php?awinmid=13334&awinaffid=2926395&ued=https%3A%2F%2Fwww.flightright.fr

Idempotent. Sauvegarde en .bak_flightright.

Usage :
    python3 integrer_flightright_article276.py
"""

import os

FICHIER = "article-276.html"

ANCIEN = """  <div class="warn">
    <strong>⚠️ Attention à la dépréciation des miles</strong>
    Les compagnies réévaluent régulièrement leurs barèmes à la hausse (plus de miles requis pour les mêmes vols). Utilisez vos miles dans les 12 à 24 mois suivant leur accumulation plutôt que d'attendre. Les miles "dormants" perdent de la valeur chaque année.
  </div>

  <div class="cta">
    <h3>📬 Voyages malins dans votre boîte mail</h3>"""

NOUVEAU = """  <div class="warn">
    <strong>⚠️ Attention à la dépréciation des miles</strong>
    Les compagnies réévaluent régulièrement leurs barèmes à la hausse (plus de miles requis pour les mêmes vols). Utilisez vos miles dans les 12 à 24 mois suivant leur accumulation plutôt que d'attendre. Les miles "dormants" perdent de la valeur chaque année.
  </div>

  <div class="tip">
    <strong>✈️ Vol annulé ou retardé ? Vos miles ne suffisent pas, mais la loi vous protège</strong>
    Un vol annulé ou retardé de plus de 3 heures au départ ou à l'arrivée de l'UE ouvre droit à une indemnisation pouvant atteindre 600€ par passager, indépendamment de vos points de fidélité. <a href="https://www.awin1.com/cread.php?awinmid=13334&awinaffid=2926395&ued=https%3A%2F%2Fwww.flightright.fr" rel="sponsored noopener" target="_blank">Flightright</a> vérifie gratuitement votre éligibilité et gère la procédure de réclamation auprès de la compagnie à votre place.
  </div>

  <div class="cta">
    <h3>📬 Voyages malins dans votre boîte mail</h3>"""


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if NOUVEAU in contenu:
        print("✅ Déjà intégré.")
        return
    if ANCIEN not in contenu:
        print("⚠️ Texte attendu non trouvé. Aucune modification.")
        return
    with open(FICHIER + ".bak_flightright", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Lien Flightright intégré dans article-276.html")


if __name__ == "__main__":
    main()
