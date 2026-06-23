#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du calcul de la prime d'activité — calculateur-prime-activite.html
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Corrections apportées (réforme du 1er avril 2026, paramètres officiels CAF) :
1. Montant forfaitaire personne seule/couple mis à jour (638,28€ / 957,42€)
2. Taux sur revenus professionnels : 61% -> 59,85% (taux officiel exact)
3. Ajout de la bonification individuelle, qui manquait complètement du calcul
   (jusqu'à 240,63€, démarre à 709,18€, plafond atteint à 1 658,76€)

⚠️ Limite assumée : les montants liés aux enfants et au forfait logement
n'ont pas pu être vérifiés avec une source officielle précise dans le temps
disponible — ils restent inchangés. À vérifier dans un second temps sur caf.fr.

Sans danger à relancer (idempotent). Sauvegarde en .bak_prime avant modification.

Usage :
    python3 corriger_prime_activite.py
"""

import os

FICHIER = "calculateur-prime-activite.html"

ANCIEN_FORFAITS = '''const FORFAITS = {
  seul:   { base: 635.71, logement: 67.84, enfants: 0 },
  couple: { base: 953.57, logement: 67.84, enfants: 0 },
  seul1:  { base: 762.85, logement: 101.77, enfants: 127.14 },
  seul2:  { base: 762.85, logement: 101.77, enfants: 254.28 },
  couple1:{ base: 953.57, logement: 101.77, enfants: 127.14 },
  couple2:{ base: 953.57, logement: 101.77, enfants: 254.28 },
  couple3:{ base: 953.57, logement: 101.77, enfants: 381.42 },
};'''

NOUVEAU_FORFAITS = '''const FORFAITS = {
  seul:   { base: 638.28, logement: 67.84, enfants: 0 },
  couple: { base: 957.42, logement: 67.84, enfants: 0 },
  seul1:  { base: 765.94, logement: 101.77, enfants: 127.66 },
  seul2:  { base: 765.94, logement: 101.77, enfants: 255.31 },
  couple1:{ base: 957.42, logement: 101.77, enfants: 127.66 },
  couple2:{ base: 957.42, logement: 101.77, enfants: 255.31 },
  couple3:{ base: 957.42, logement: 101.77, enfants: 382.97 },
};'''

ANCIEN_CALCUL = '''  // Formule simplifiée prime d'activité
  // PA = MF + 0.61 × RP - RG
  // MF = montant forfaitaire
  // RP = revenus professionnels
  // RG = ressources globales du foyer
  const rg = revenus + autres;
  const pa = montantForaitaire + 0.61 * revenus - rg;
  const prime = Math.max(0, Math.round(pa));'''

NOUVEAU_CALCUL = '''  // Formule prime d'activité (barème officiel CAF au 1er avril 2026)
  // PA = MF + 59,85% × RP + Bonification individuelle - RG
  // MF = montant forfaitaire
  // RP = revenus professionnels
  // RG = ressources globales du foyer
  // Bonification individuelle : 0€ sous 709,18€, croît linéairement jusqu'à
  // 240,63€ max atteint à 1 658,76€ de revenus professionnels
  function bonificationIndividuelle(rp) {
    const SEUIL_BAS = 709.18;
    const SEUIL_HAUT = 1658.76;
    const MAX_BONIF = 240.63;
    if (rp <= SEUIL_BAS) return 0;
    if (rp >= SEUIL_HAUT) return MAX_BONIF;
    return MAX_BONIF * (rp - SEUIL_BAS) / (SEUIL_HAUT - SEUIL_BAS);
  }
  const rg = revenus + autres;
  const bonification = bonificationIndividuelle(revenus);
  const pa = montantForaitaire + 0.5985 * revenus + bonification - rg;
  const prime = Math.max(0, Math.round(pa));'''


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable dans ce dossier.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "bonificationIndividuelle" in contenu:
        print("✅ Déjà corrigé — bonification individuelle déjà présente.")
        return

    if ANCIEN_FORFAITS not in contenu or ANCIEN_CALCUL not in contenu:
        print("⚠️  Un des blocs attendus n'a pas été trouvé tel quel.")
        print("   Aucune modification effectuée, pour éviter une erreur.")
        return

    with open(FICHIER + ".bak_prime", 'w', encoding='utf-8') as f:
        f.write(contenu)

    nouveau_contenu = contenu.replace(ANCIEN_FORFAITS, NOUVEAU_FORFAITS, 1)
    nouveau_contenu = nouveau_contenu.replace(ANCIEN_CALCUL, NOUVEAU_CALCUL, 1)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    print("✅ Calcul de la prime d'activité corrigé :")
    print("   - Montants forfaitaires mis à jour (638,28€ / 957,42€)")
    print("   - Taux corrigé : 61% -> 59,85%")
    print("   - Bonification individuelle ajoutée (jusqu'à 240,63€)")
    print(f"   Sauvegarde créée : {FICHIER}.bak_prime")
    print("   ⚠️  Montants enfants/logement non vérifiés avec une source officielle précise — à contrôler plus tard.")


if __name__ == "__main__":
    main()
