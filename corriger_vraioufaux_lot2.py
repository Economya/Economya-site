#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction vrai-ou-faux.html — lot 2 (2 erreurs supplémentaires)
À lancer depuis ~/Desktop/mon site

1. Crypto "flat tax à 30%" -> incohérent avec la correction déjà
   appliquée aujourd'hui sur la flat tax générale (PS 2026 = 18,6%,
   total réel 31,4%). Confirmé par sources spécialisées crypto
   convergentes (Kraken, Ramify, Waltio) pour 2026.
2. LEP "plafond de revenus environ 21 000€" -> confirmé FAUX par
   sources multiples et concordantes (service-public.gouv.fr,
   Meilleurtaux, Moneyvox) : le vrai plafond 2026 pour une personne
   seule est de 23 028€ de revenu fiscal de référence.

Le seuil d'exonération crypto de 305€/an est resté inchangé (confirmé
exact par 5 sources sur 6, non modifié).

Idempotent. Sauvegarde en .bak_vraioufaux2 avant modification.

Usage :
    python3 corriger_vraioufaux_lot2.py
"""

import os

FICHIER = "vrai-ou-faux.html"

REMPLACEMENTS = [
    (
        "{cat:'💰 Crypto',text:'Les gains sur cryptomonnaies sont imposables en France.',answer:true,expl:'Exact ! Les plus-values sur cryptomonnaies sont taxées à 30% (flat tax) depuis 2023.',fact:'Seules les cessions inférieures à 305€/an sont exonérées. Au-delà, déclaration obligatoire.'},",
        "{cat:'💰 Crypto',text:'Les gains sur cryptomonnaies sont imposables en France.',answer:true,expl:'Exact ! Les plus-values sur cryptomonnaies sont taxées à 31,4% (flat tax 2026 : 12,8% IR + 18,6% PS).',fact:'Seules les cessions inférieures à 305€/an sont exonérées. Au-delà, déclaration obligatoire.'},",
    ),
    (
        "{cat:'🏦 Épargne',text:'Le LEP (Livret d\\'Épargne Populaire) est accessible à tous les Français.',answer:false,expl:'FAUX ! Le LEP est réservé aux personnes dont les revenus fiscaux ne dépassent pas un certain plafond.',fact:'En 2026, le plafond de revenus pour le LEP est d\\'environ 21 000€ pour une personne seule.'},",
        "{cat:'🏦 Épargne',text:'Le LEP (Livret d\\'Épargne Populaire) est accessible à tous les Français.',answer:false,expl:'FAUX ! Le LEP est réservé aux personnes dont les revenus fiscaux ne dépassent pas un certain plafond.',fact:'En 2026, le plafond de revenus pour le LEP est de 23 028€ de revenu fiscal de référence pour une personne seule.'},",
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
            contenu = contenu.replace(ancien, nouveau, 1)
            nb_modifs += 1
        else:
            print(f"⚠️  Texte non trouvé (ignoré) : {ancien[:70]}...")

    if nb_modifs == 0:
        print("✅ Déjà corrigé.")
        return

    with open(FICHIER + ".bak_vraioufaux2", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs}/2 erreur(s) corrigée(s) dans vrai-ou-faux.html (lot 2) :")
    print("   1. Crypto flat tax: 30% -> 31,4%")
    print("   2. Plafond revenus LEP: ~21 000e -> 23 028e")


if __name__ == "__main__":
    main()
