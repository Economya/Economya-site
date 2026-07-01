#!/usr/bin/env python3
"""
Corrige 2 erreurs factuelles trouvées lors de l'audit qualité (lot 4) :

1. article-220.html (Démission reconversion) :
   La condition "5 ans chez le même employeur" est fausse. Confirmé
   France Travail/Transitions Pro : les 5 ans (1300 jours) d'activité
   salariée continue peuvent être acquis chez un OU PLUSIEURS employeurs.

2. article-339.html (PEA) :
   - "17,2 %" de prélèvements sociaux après 5 ans -> obsolète, le taux réel
     est 18,6 % (déjà harmonisé ailleurs sur le site). Incohérence interne :
     le "12,8 % d'économie" cité juste après ne fonctionne mathématiquement
     qu'avec 18,6 % (31,4 - 18,6 = 12,8), pas avec 17,2 %.
   - "30 % en compte-titres ordinaire" -> la flat tax CTO réelle est 31,4 %
     (12,8 % IR + 18,6 % PS), déjà harmonisée ailleurs sur le site.

Idempotent. Sauvegardes .bak_auditqualite_lot4 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-220.html": [
        (
            '<div class="cond-titre">5 ans d\'ancienneté chez le même employeur</div>',
            '<div class="cond-titre">5 ans d\'activité salariée continue</div>',
        ),
        (
            "Vous devez justifier de 5 années continues de contrat de travail chez votre employeur actuel au moment de la démission. Les contrats précédents ne comptent pas, sauf s'ils n'ont pas été interrompus plus d'une période normale entre deux contrats.",
            "Vous devez justifier d'au moins 5 ans (1 300 jours) d'activité salariée continue au cours des 60 derniers mois, chez un ou plusieurs employeurs — l'ancienneté n'a pas besoin d'être chez le même employeur. Les congés sans solde, sabbatiques ou périodes de disponibilité ne sont pas pris en compte.",
        ),
    ],
    "article-339.html": [
        (
            "Après 5 ans, vos plus-values ne sont taxées qu'à 17,2 % (prélèvements sociaux seulement) au lieu de 30 % en compte-titres ordinaire.",
            "Après 5 ans, vos plus-values ne sont taxées qu'à 18,6 % (prélèvements sociaux seulement) au lieu de 31,4 % en compte-titres ordinaire.",
        ),
        (
            "Plus-values soumises uniquement aux prélèvements sociaux (17,2 %) — soit 12,8 % d'économie vs un CTO.",
            "Plus-values soumises uniquement aux prélèvements sociaux (18,6 %) — soit 12,8 % d'économie vs un CTO.",
        ),
    ],
}


def corriger_fichier(fichier, remplacements):
    if not os.path.exists(fichier):
        print(f"❌ Fichier introuvable : {fichier} (ignoré)")
        return

    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    total = 0

    for ancien, nouveau in remplacements:
        if ancien in contenu_modifie:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau, 1)
            print(f"  ✅ Corrigé : {ancien[:55]}...")
            total += 1
        elif nouveau in contenu_modifie:
            print(f"  ℹ️  Déjà corrigé (idempotent) : {nouveau[:55]}...")
        else:
            print(f"  ⚠️  Chaîne non trouvée : {ancien[:55]}...")

    if total == 0:
        print(f"  → Rien à faire pour {fichier}.")
        return

    shutil.copy2(fichier, fichier + ".bak_auditqualite_lot4")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  → {total} correction(s) écrite(s) dans {fichier} (sauvegarde créée)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
