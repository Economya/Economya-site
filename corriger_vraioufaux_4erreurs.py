#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction vrai-ou-faux.html — 4 erreurs/incohérences trouvées
À lancer depuis ~/Desktop/mon site

1. LEP plafonné à 7 700€ -> 10 000€ (même erreur confirmée et corrigée
   ce matin dans comparateur-livrets.html et plusieurs articles).
2. Flat tax "30% : 12,8% IR + 17,2% PS" -> incohérent avec la
   correction déjà appliquée aujourd'hui (PS = 18,6% en 2026, total
   réel 31,4%, pas 30%).
3. "Taux d'endettement max recommandé 33%" marqué vrai, alors que le
   propre "fact" de la question dit "le HCSF recommande 35%" -
   contradiction interne. Le vrai chiffre confirmé aujourd'hui est
   35% (HCSF) : la question est reformulée pour être cohérente et
   exacte.
4. Consultation généraliste "26,50€" : confirmé par sources multiples
   (Ameli, service-public.gouv.fr, etc.) que le tarif est passé à 30€
   depuis le 22 décembre 2024, stable en 2026. La question d'origine
   était confuse (auto-contradictoire : "FAUX... attendez, c'est
   vrai !"). Reformulée clairement.

Idempotent. Sauvegarde en .bak_vraioufaux avant modification.

Usage :
    python3 corriger_vraioufaux_4erreurs.py
"""

import os

FICHIER = "vrai-ou-faux.html"

REMPLACEMENTS = [
    (
        "{cat:'💰 Épargne',text:'Le Livret A est plafonné à 22 950€.',answer:true,expl:'Exact ! Le plafond du Livret A est de 22 950€ depuis 2013.',fact:'Le LEP (Livret d\\'Épargne Populaire) est plafonné à 7 700€ avec un taux plus avantageux.'},",
        "{cat:'💰 Épargne',text:'Le Livret A est plafonné à 22 950€.',answer:true,expl:'Exact ! Le plafond du Livret A est de 22 950€ depuis 2013.',fact:'Le LEP (Livret d\\'Épargne Populaire) est plafonné à 10 000€ avec un taux plus avantageux.'},",
    ),
    (
        "{cat:'💰 Fiscalité',text:'En France, la flat tax sur les revenus du capital est de 30%.',answer:true,expl:'Correct ! Le PFU (Prélèvement Forfaitaire Unique) est de 30% : 12,8% IR + 17,2% prélèvements sociaux.',fact:'Vous pouvez opter pour l\\'imposition au barème progressif si votre TMI est inférieure à 12,8%.'},",
        "{cat:'💰 Fiscalité',text:'En France, la flat tax sur les revenus du capital est de 31,4%.',answer:true,expl:'Correct ! Le PFU (Prélèvement Forfaitaire Unique) est de 31,4% : 12,8% IR + 18,6% prélèvements sociaux (taux 2026).',fact:'Vous pouvez opter pour l\\'imposition au barème progressif si votre TMI est inférieure à 12,8%.'},",
    ),
    (
        "{cat:'🏦 Crédit',text:'Le taux d\\'endettement maximum recommandé pour un crédit est de 33%.',answer:true,expl:'Correct ! La règle des 33% signifie que vos mensualités ne doivent pas dépasser 1/3 de vos revenus.',fact:'Depuis 2022, le HCSF recommande un taux d\\'endettement maximal de 35% charges incluses.'},",
        "{cat:'🏦 Crédit',text:'Le taux d\\'endettement maximum recommandé pour un crédit est de 35%.',answer:true,expl:'Correct ! Depuis 2022, le HCSF (Haut Conseil de Stabilité Financière) recommande un taux d\\'endettement maximal de 35%, charges incluses.',fact:'L\\'ancienne règle des 33% (1/3 des revenus) a été remplacée par ce seuil de 35% plus précis.'},",
    ),
    (
        "{cat:'🏥 Médecin',text:'En France, la consultation chez un médecin généraliste coûte 26,50€.',answer:false,expl:'FAUX ! Depuis mai 2023, le tarif de la consultation chez un généraliste est de 26,50€... attendez, c\\'est vrai !',fact:'Bien que le tarif soit 26,50€, après remboursement Sécu (70%) et mutuelle, votre reste à charge peut être nul.'},",
        "{cat:'🏥 Médecin',text:'En France, la consultation chez un médecin généraliste coûte 30€.',answer:true,expl:'Vrai ! Depuis le 22 décembre 2024, le tarif conventionné d\\'une consultation généraliste secteur 1 est passé à 30€.',fact:'Avec le médecin traitant, l\\'Assurance Maladie rembourse 70% (19€), une bonne mutuelle peut couvrir le reste à charge.'},",
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

    with open(FICHIER + ".bak_vraioufaux", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs}/4 erreur(s) corrigée(s) dans vrai-ou-faux.html :")
    print("   1. LEP: 7700e -> 10000e")
    print("   2. Flat tax: 30% -> 31,4% (PS 2026 = 18,6%)")
    print("   3. Taux endettement: 33% -> 35% (HCSF, coherence interne)")
    print("   4. Consultation generaliste: 26,50e -> 30e (depuis dec 2024)")


if __name__ == "__main__":
    main()
