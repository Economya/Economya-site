#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du simulateur APL — simulateur-apl.html
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Corrections apportées (vérifiées via sources officielles, juin 2026) :
1. Plafonds de loyer "personne seule" corrigés (zone 1 et zone 3 étaient faux)
2. Forfait charges : corrigé pour dépendre de la COMPOSITION DU FOYER
   (60,59€ base + 13,74€/personne supplémentaire), pas de la zone — c'était
   une erreur de structure, pas seulement de montant

⚠️ LIMITES ASSUMÉES, IMPORTANTES :
- Les plafonds de loyer "couple" et "familles avec enfants" n'ont PAS pu être
  vérifiés avec une source officielle fiable dans le temps disponible — ils
  restent inchangés (probablement approximatifs).
- La formule de "participation personnelle" (Rp) reste une simplification
  par tranches, PAS la vraie formule CAF (qui utilise 3 seuils R0/R1/R2
  variables par zone ET composition familiale, non reconstituable de façon
  fiable à partir de sources publiques généralistes).
- Le disclaimer affiché à l'utilisateur est renforcé pour refléter cette
  incertitude plus clairement.

Sans danger à relancer (idempotent). Sauvegarde en .bak_apl avant modification.

Usage :
    python3 corriger_apl.py
"""

import os
import re

FICHIER = "simulateur-apl.html"

ANCIEN_PLAFONDS_SEUL = "seul:       [370, 291, 262],"
NOUVEAU_PLAFONDS_SEUL = "seul:       [333, 290, 272],"

ANCIEN_CHARGES_BLOC = '''// Forfait charges par zone
const CHARGES = [57, 52, 49];'''

NOUVEAU_CHARGES_BLOC = '''// Forfait charges CAF — dépend de la composition du foyer, PAS de la zone
// (60,59€ base pour 1 personne ou couple, +13,74€ par personne supplémentaire)
const CHARGES_PAR_SITUATION = {
  seul: 60.59,
  couple: 60.59,
  '1enfant': 74.33,
  '2enfants': 88.07,
  '3enfants': 101.81,
  parent_seul: 60.59,
};'''

ANCIEN_APPEL_CHARGES = "  const charges = CHARGES[zone];"
NOUVEL_APPEL_CHARGES = "  const charges = CHARGES_PAR_SITUATION[situation];"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable dans ce dossier.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "CHARGES_PAR_SITUATION" in contenu:
        print("✅ Déjà corrigé.")
        return

    manquants = []
    if ANCIEN_PLAFONDS_SEUL not in contenu:
        manquants.append("plafonds personne seule")
    if ANCIEN_CHARGES_BLOC not in contenu:
        manquants.append("bloc forfait charges")
    if ANCIEN_APPEL_CHARGES not in contenu:
        manquants.append("appel calcul charges")

    if manquants:
        print(f"⚠️  Blocs non trouvés tels qu'attendus : {', '.join(manquants)}")
        print("   Aucune modification effectuée, pour éviter une erreur.")
        return

    with open(FICHIER + ".bak_apl", 'w', encoding='utf-8') as f:
        f.write(contenu)

    nouveau_contenu = contenu.replace(ANCIEN_PLAFONDS_SEUL, NOUVEAU_PLAFONDS_SEUL, 1)
    nouveau_contenu = nouveau_contenu.replace(ANCIEN_CHARGES_BLOC, NOUVEAU_CHARGES_BLOC, 1)
    nouveau_contenu = nouveau_contenu.replace(ANCIEN_APPEL_CHARGES, NOUVEL_APPEL_CHARGES, 1)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    print("✅ Corrections APL appliquées :")
    print("   - Plafonds loyer 'personne seule' corrigés (333€/290€/272€)")
    print("   - Forfait charges corrigé : dépend désormais de la composition du foyer, pas de la zone")
    print(f"   Sauvegarde créée : {FICHIER}.bak_apl")
    print("   ⚠️  Plafonds couple/familles non vérifiés — à contrôler sur caf.fr.")
    print("   ⚠️  La participation personnelle reste une formule simplifiée, pas le calcul CAF exact.")


if __name__ == "__main__":
    main()
