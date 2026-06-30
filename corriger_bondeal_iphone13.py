#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction le-bon-deal.html — prix réparation Apple iPhone 13 obsolète
À lancer depuis ~/Desktop/mon site

Confirmé par source citant directement les tarifs officiels Apple FR
(forum communautaire Apple, 2026) : remplacement écran iPhone 13 sans
AppleCare+ = 338,99€ (arrondi 339€), pas 329€. Économie et pourcentage
recalculés en conséquence (219€ au lieu de 209€, -65% au lieu de -64%).

Idempotent. Sauvegarde en .bak_bondealiphone.

Usage :
    python3 corriger_bondeal_iphone13.py
"""

import os

FICHIER = "le-bon-deal.html"

ANCIEN = "{cat:'📱 Réparation',q:'Quelle option est moins chère pour un écran cassé ?',a:{icon:'📱',name:'Apple Store officiel',detail:'Remplacement écran iPhone 13',price:'329€',sub:'réparation',val:32900},b:{icon:'🔧',name:'Réparateur indépendant',detail:'Même pièce • Même qualité',price:'120€',sub:'réparation',val:12000,badge:'✅ -64%'},correct:'b',economy:209,explication:'Les réparateurs indépendants agréés proposent des prix 3x moins chers pour la même qualité !'},"

NOUVEAU = "{cat:'📱 Réparation',q:'Quelle option est moins chère pour un écran cassé ?',a:{icon:'📱',name:'Apple Store officiel',detail:'Remplacement écran iPhone 13',price:'339€',sub:'réparation',val:33900},b:{icon:'🔧',name:'Réparateur indépendant',detail:'Même pièce • Même qualité',price:'120€',sub:'réparation',val:12000,badge:'✅ -65%'},correct:'b',economy:219,explication:'Les réparateurs indépendants agréés proposent des prix nettement moins chers pour la même qualité !'},"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if NOUVEAU in contenu:
        print("✅ Déjà corrigé.")
        return
    if ANCIEN not in contenu:
        print("⚠️ Texte attendu non trouvé. Aucune modification.")
        return
    with open(FICHIER + ".bak_bondealiphone", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Prix iPhone 13 corrigé : 329€ -> 339€ (économie et % recalculés : 219€, -65%)")


if __name__ == "__main__":
    main()
