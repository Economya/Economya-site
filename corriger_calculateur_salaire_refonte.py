#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction STRUCTURELLE complète de calculateur-salaire.html — refonte du
calcul des cotisations salariales avec la vraie logique de tranchement
T1/T2 (PMSS)
À lancer depuis ~/Desktop/mon site

DÉCOUVERTES CONFIRMÉES (sources convergentes : bulletin-paie.com,
salaireclair.fr, l-expert-comptable.com, légisocial.fr) :
1. Cotisation maladie salariale (0,75%) : SUPPRIMÉE depuis le 1er janvier
   2018 — n'existe plus du tout sur les bulletins de paie.
2. Retraite complémentaire AGIRC-ARRCO : depuis la fusion de 2019, le
   taux T1 (3,15%) est identique pour cadres ET non-cadres — la
   distinction de taux par statut que faisait l'outil n'existe plus.
3. Le vrai mécanisme est un système de TRANCHES : T1 s'applique sur la
   part du salaire ≤ PMSS (4 005€/mois en 2026), T2 (8,64%, cadres
   essentiellement) sur la part > PMSS. L'outil appliquait un taux
   "tranche 2" de façon non tranchée (sur tout le salaire), ce qui
   aurait aggravé l'erreur si on avait juste remplacé le chiffre sans
   corriger la logique — d'où cette refonte complète.
4. Vieillesse de base : 6,90% (plafonnée, ≤ PMSS) + 0,40% (déplafonnée,
   sur tout le salaire) — l'outil n'avait que la part plafonnée.
5. CSG/CRDS : 9,70% (pas 9,68%), sur une assiette de 98,25% du brut
   (abattement de 1,75% pour frais professionnels), pas sur 100%.
6. Prévoyance cadre obligatoire : 1,5% — confirmé correct, gardé tel quel.

Pour le mode "net → brut" (calcul inverse), une résolution itérative
simple est utilisée car le taux global n'est plus un taux fixe unique
(il dépend désormais du dépassement ou non du PMSS).

Idempotent. Sauvegarde en .bak_salaire2026refonte.

Usage :
    python3 corriger_calculateur_salaire_refonte.py
"""

import os

FICHIER = "calculateur-salaire.html"

ANCIEN = """function calculate() {
  let valeur = +document.getElementById('salaire').value || 0;
  const periode = document.getElementById('periode').value;
  const statut = document.getElementById('statut').value;

  if(periode === 'annuel') valeur = valeur / 12;

  // Taux cotisations salariales 2026 (approximatifs)
  const tauxSecu = 0.0075;
  const tauxRetraite = 0.0690;
  const tauxRetraite2 = statut === 'cadre' ? 0.0387 : 0.0270;
  const tauxCSG = 0.0968;
  const tauxPrev = statut === 'cadre' ? 0.015 : 0.005;
  const tauxTotal = tauxSecu + tauxRetraite + tauxRetraite2 + tauxCSG + tauxPrev;

  let brutMensuel, netAvantImpot;

  if(mode === 'brut') {
    brutMensuel = valeur;
    netAvantImpot = brutMensuel * (1 - tauxTotal);
  } else {
    netAvantImpot = valeur;
    brutMensuel = netAvantImpot / (1 - tauxTotal);
  }

  // Prélèvement à la source estimé (taux moyen ~10% pour salaire médian)
  const tauxPAS = netAvantImpot < 1500 ? 0.02 : netAvantImpot < 2500 ? 0.07 : netAvantImpot < 4000 ? 0.12 : 0.17;
  const pas = netAvantImpot * tauxPAS;
  const netApresImpot = netAvantImpot - pas;

  document.getElementById('r-net-mensuel').textContent = fmt(netApresImpot);
  document.getElementById('r-brut-mensuel').textContent = fmt(brutMensuel);
  document.getElementById('r-net-annuel').textContent = fmt(netApresImpot * 12);
  document.getElementById('r-pas').textContent = fmt(pas);

  document.getElementById('d-brut').textContent = fmt(brutMensuel);
  document.getElementById('d-secu').textContent = '- ' + fmt(brutMensuel * tauxSecu);
  document.getElementById('d-retraite').textContent = '- ' + fmt(brutMensuel * tauxRetraite);
  document.getElementById('d-retraite2').textContent = '- ' + fmt(brutMensuel * tauxRetraite2);
  document.getElementById('d-chomage').textContent = '- ' + fmt(brutMensuel * tauxCSG);
  document.getElementById('d-prev').textContent = '- ' + fmt(brutMensuel * tauxPrev);
  document.getElementById('d-net-avant').textContent = fmt(netAvantImpot);
  document.getElementById('d-pas2').textContent = '- ' + fmt(pas);
  document.getElementById('d-net-apres').textContent = fmt(netApresImpot);

  const ratio = (netApresImpot / brutMensuel * 100).toFixed(0);
  const tip = document.getElementById('tip-text');
  tip.innerHTML = `<strong>💡 Info :</strong> Votre salaire net représente <strong>${ratio}%</strong> de votre brut. La règle générale : le net avant impôt est environ 78-80% du brut pour un non-cadre, 75-77% pour un cadre.`;"""

NOUVEAU = """function calculerCotisations(brutMensuel, statut) {
  // Barème 2026 confirmé (sources convergentes URSSAF/AGIRC-ARRCO) :
  // PMSS (Plafond Mensuel de la Sécurité Sociale) = 4005€ en 2026
  const PMSS = 4005;
  const trancheT1 = Math.min(brutMensuel, PMSS);
  const trancheT2 = Math.max(0, brutMensuel - PMSS);

  // Maladie salariale : SUPPRIMÉE depuis 2018 (0%)
  const secu = 0;

  // Vieillesse de base : plafonnée 6,90% (T1) + déplafonnée 0,40% (totalité)
  const vieillessePlafonnee = trancheT1 * 0.0690;
  const vieillesseDeplafonnee = brutMensuel * 0.0040;
  const retraite = vieillessePlafonnee + vieillesseDeplafonnee;

  // Retraite complémentaire AGIRC-ARRCO : 3,15% (T1, identique cadre/non-cadre
  // depuis la fusion 2019) + 8,64% (T2, part au-delà du PMSS)
  const retraite2 = trancheT1 * 0.0315 + trancheT2 * 0.0864;

  // CSG/CRDS : 9,70% sur 98,25% du brut (abattement frais professionnels)
  const csg = brutMensuel * 0.9825 * 0.0970;

  // Prévoyance obligatoire cadre (1,5% sur T1) ; facultative non-cadre (~0,5%, variable)
  const prev = statut === 'cadre' ? trancheT1 * 0.015 : brutMensuel * 0.005;

  const total = secu + retraite + retraite2 + csg + prev;
  return { secu, retraite, retraite2, csg, prev, total };
}

function calculate() {
  let valeur = +document.getElementById('salaire').value || 0;
  const periode = document.getElementById('periode').value;
  const statut = document.getElementById('statut').value;

  if(periode === 'annuel') valeur = valeur / 12;

  let brutMensuel, netAvantImpot, cot;

  if(mode === 'brut') {
    brutMensuel = valeur;
    cot = calculerCotisations(brutMensuel, statut);
    netAvantImpot = brutMensuel - cot.total;
  } else {
    netAvantImpot = valeur;
    // Résolution itérative (le taux n'est plus fixe à cause du tranchement PMSS)
    brutMensuel = netAvantImpot / 0.78; // estimation initiale
    for (let i = 0; i < 8; i++) {
      cot = calculerCotisations(brutMensuel, statut);
      const netEstime = brutMensuel - cot.total;
      const ecart = netAvantImpot - netEstime;
      brutMensuel += ecart; // ajustement direct, converge en quelques itérations
    }
    cot = calculerCotisations(brutMensuel, statut);
  }

  // Prélèvement à la source estimé (taux moyen ~10% pour salaire médian)
  const tauxPAS = netAvantImpot < 1500 ? 0.02 : netAvantImpot < 2500 ? 0.07 : netAvantImpot < 4000 ? 0.12 : 0.17;
  const pas = netAvantImpot * tauxPAS;
  const netApresImpot = netAvantImpot - pas;

  document.getElementById('r-net-mensuel').textContent = fmt(netApresImpot);
  document.getElementById('r-brut-mensuel').textContent = fmt(brutMensuel);
  document.getElementById('r-net-annuel').textContent = fmt(netApresImpot * 12);
  document.getElementById('r-pas').textContent = fmt(pas);

  document.getElementById('d-brut').textContent = fmt(brutMensuel);
  document.getElementById('d-secu').textContent = '- ' + fmt(cot.secu);
  document.getElementById('d-retraite').textContent = '- ' + fmt(cot.retraite);
  document.getElementById('d-retraite2').textContent = '- ' + fmt(cot.retraite2);
  document.getElementById('d-chomage').textContent = '- ' + fmt(cot.csg);
  document.getElementById('d-prev').textContent = '- ' + fmt(cot.prev);
  document.getElementById('d-net-avant').textContent = fmt(netAvantImpot);
  document.getElementById('d-pas2').textContent = '- ' + fmt(pas);
  document.getElementById('d-net-apres').textContent = fmt(netApresImpot);

  const ratio = (netApresImpot / brutMensuel * 100).toFixed(0);
  const tip = document.getElementById('tip-text');
  tip.innerHTML = `<strong>💡 Info :</strong> Votre salaire net représente <strong>${ratio}%</strong> de votre brut. La règle générale : le net avant impôt est environ 76-78% du brut (cotisations salariales ~22-25% selon le statut et le dépassement du plafond de la Sécurité sociale).`;"""


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
    with open(FICHIER + ".bak_salaire2026refonte", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Refonte complète du calcul de cotisations appliquée")
    print("   - Maladie salariale: 0,75% -> 0% (supprimee depuis 2018)")
    print("   - Retraite T1: identique cadre/non-cadre desormais (3,15%)")
    print("   - Retraite T2 (8,64%): appliquee SEULEMENT sur la part > PMSS (4005e/mois)")
    print("   - Vieillesse deplafonnee 0,40% ajoutee")
    print("   - CSG/CRDS: 9,70% sur assiette 98,25% (au lieu de 9,68% sur 100%)")


if __name__ == "__main__":
    main()
