#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction le-bon-deal.html — prix Netflix et Xbox Game Pass Ultimate
obsolètes
À lancer depuis ~/Desktop/mon site

Mêmes erreurs déjà confirmées et corrigées ailleurs aujourd'hui dans
cette session :
- Netflix Standard : 13,49€ -> 14,99€ (économie/an recalculée : 81€ -> 90€)
- Xbox Game Pass Ultimate : 14,99€ -> 20,99€ (prix actuel confirmé
  aujourd'hui via article-34 ; économie/an recalculée : 780€ -> 708€)

Idempotent. Sauvegarde en .bak_bondeallot2.

Usage :
    python3 corriger_bondeal_lot2.py
"""

import os

FICHIER = "le-bon-deal.html"

REMPLACEMENTS = [
    (
        "{cat:'📺 Streaming',q:'Quelle offre de streaming est la moins chère ?',a:{icon:'🔴',name:'Netflix Standard solo',detail:'2 écrans HD • 1 compte',price:'13,49€',sub:'/mois',val:1349},b:{icon:'🔴',name:'Netflix partagé',detail:'2 écrans HD • Partagé via Sharesub',price:'6,75€',sub:'/mois partagé',val:675,badge:'✅ Partagé'},correct:'b',economy:81,explication:'Partager son compte Netflix divise la facture par 2. Économie : 81€/an !'},",
        "{cat:'📺 Streaming',q:'Quelle offre de streaming est la moins chère ?',a:{icon:'🔴',name:'Netflix Standard solo',detail:'2 écrans HD • 1 compte',price:'14,99€',sub:'/mois',val:1499},b:{icon:'🔴',name:'Netflix partagé',detail:'2 écrans HD • Partagé via Sharesub',price:'7,50€',sub:'/mois partagé',val:750,badge:'✅ Partagé'},correct:'b',economy:90,explication:'Partager son compte Netflix divise la facture par 2. Économie : 90€/an !'},",
    ),
    (
        "{cat:'🎮 Gaming',q:'Quelle option est la moins chère pour jouer ?',a:{icon:'🎮',name:'Jeu neuf PS5',detail:'Nouveau titre AAA • Disque',price:'79,99€',sub:'le jeu',val:7999},b:{icon:'🎮',name:'Xbox Game Pass',detail:'Centaines de jeux • Illimité',price:'14,99€',sub:'/mois',val:1499,badge:'✅ Illimité'},correct:'b',economy:780,explication:'Xbox Game Pass = centaines de jeux pour 15€/mois vs 80€ par jeu. 780€/an économisés !'},",
        "{cat:'🎮 Gaming',q:'Quelle option est la moins chère pour jouer ?',a:{icon:'🎮',name:'Jeu neuf PS5',detail:'Nouveau titre AAA • Disque',price:'79,99€',sub:'le jeu',val:7999},b:{icon:'🎮',name:'Xbox Game Pass Ultimate',detail:'Centaines de jeux • Illimité',price:'20,99€',sub:'/mois',val:2099,badge:'✅ Illimité'},correct:'b',economy:708,explication:'Xbox Game Pass Ultimate = centaines de jeux pour 21€/mois vs 80€ par jeu. 708€/an économisés !'},",
    ),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    for ancien, nouveau in REMPLACEMENTS:
        if nouveau in contenu and ancien not in contenu:
            continue
        if ancien in contenu:
            contenu = contenu.replace(ancien, nouveau)
            nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou texte non trouvé.")
        return

    with open(FICHIER + ".bak_bondeallot2", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} question(s) corrigée(s) : Netflix 13,49€->14,99€, Game Pass 14,99€->20,99€")


if __name__ == "__main__":
    main()
