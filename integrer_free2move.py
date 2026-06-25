#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du partenaire d'affiliation Free2Move (location/autopartage
de véhicules) sur l'article dédié à la location de voiture
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Lien Awin vérifié : awinmid=124140, awinaffid=2926395

Insertion juste avant <footer>, même ancrage fiable que pour
SeDomicilier.

Idempotent. Sauvegarde en .bak_free2move avant modification.

Usage :
    python3 integrer_free2move.py
"""

import os

FICHIER = "article-68.html"

LIEN_AWIN = "https://www.awin1.com/cread.php?awinmid=124140&awinaffid=2926395&ued=https%3A%2F%2Fwww.free2move.com%2Ffr-FR%2F"

BLOC_FREE2MOVE = f'''
  <div class="tip" style="background:#E8F4F8;border-left:4px solid #2E86AB;color:#0D3A4D">
    <strong>🚗 Pas besoin d'acheter une voiture pour en avoir une quand il faut</strong>
    Pour un usage occasionnel, l'autopartage et la location courte durée via des services comme <a href="{LIEN_AWIN}" target="_blank" rel="noopener sponsored">Free2Move</a> permettent de louer un véhicule à l'heure, à la journée ou pour un trajet ponctuel, sans les coûts fixes d'une voiture personnelle (assurance, entretien, stationnement, dépréciation). Une solution flexible pour les citadins qui n'ont besoin d'un véhicule que de temps en temps. Economya peut percevoir une commission sur ce lien, sans coût supplémentaire pour vous.
  </div>
'''


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "Free2Move" in contenu:
        print("✅ Déjà présent.")
        return

    if "<footer>" not in contenu:
        print("❌ Pas de footer trouvé.")
        return

    contenu_original = contenu
    nouveau_contenu = contenu.replace("<footer>", BLOC_FREE2MOVE + "\n<footer>", 1)

    with open(FICHIER + ".bak_free2move", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    print(f"✅ Encart Free2Move ajouté sur {FICHIER}")


if __name__ == "__main__":
    main()
