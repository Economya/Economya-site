#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-207.html — réforme LMNP majeure (réintégration des
amortissements dans la plus-value) jamais mentionnée + plafond obsolète
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE IMPORTANTE : depuis le 15 février 2025 (loi n°2025-127, art. 84),
les amortissements déduits pendant la location sont réintégrés dans le
calcul de la plus-value à la revente (sauf résidences étudiantes/seniors/
EHPAD). L'article présentait le LMNP comme un double avantage fiscal
(loyers ET revente non imposés) sans jamais mentionner cette réforme —
lacune corrigée par l'ajout d'un encart d'avertissement dédié.

Plafond micro-BIC : 77 700€ (revenus 2025) -> mention des deux seuils,
77 700€ actuel et 83 600€ pour les revenus 2026.

Idempotent. Sauvegarde en .bak_art207.

Usage :
    python3 corriger_article207.py
"""

import os

FICHIER = "article-207.html"

ANCIEN_INTRO = "Le statut de Loueur en Meublé Non Professionnel (LMNP) est l'un des placements immobiliers les plus avantageux fiscalement en France. Il permet de percevoir des loyers largement défiscalisés grâce à l'amortissement comptable du bien — une mécanique que 90 % des propriétaires ignorent. Résultat : des revenus locatifs quasiment non imposés pendant 10 à 20 ans, tout en se constituant un patrimoine. Voici comment ça fonctionne concrètement."

NOUVEAU_INTRO = """Le statut de Loueur en Meublé Non Professionnel (LMNP) est l'un des placements immobiliers les plus avantageux fiscalement en France. Il permet de percevoir des loyers largement défiscalisés grâce à l'amortissement comptable du bien — une mécanique que 90 % des propriétaires ignorent. Résultat : des revenus locatifs quasiment non imposés pendant 10 à 20 ans. ⚠️ Attention cependant : depuis une réforme de 2025, cet avantage n'est plus "gratuit" à la revente (voir l'encart dédié plus bas). Voici comment ça fonctionne concrètement.</p>

  <div class="warn">
    <strong>⚠️ Réforme 2025 : les amortissements sont désormais repris à la revente</strong>
    Depuis le 15 février 2025 (loi n°2025-127, article 84), les amortissements déduits pendant la location sont réintégrés dans le calcul de la plus-value lors de la revente du bien (sauf résidences étudiantes, seniors et EHPAD, qui restent exemptées). Concrètement, l'avantage fiscal n'est plus définitif : ce qui n'a pas été imposé sur les loyers chaque année peut désormais être rattrapé par l'impôt au moment de la vente. L'imposition à la revente peut être multipliée par 2 à 5 selon la durée de détention et le montant cumulé d'amortissements. Le LMNP reste avantageux, mais ce n'est plus le "double cadeau fiscal" qu'il était avant 2025 — anticipez cet impact avant toute décision de revente."""

ANCIEN_PLAFOND = '<div class="reg-row"><span class="reg-label">Plafond de revenus</span><span class="reg-val">77 700 €/an</span></div>'
NOUVEAU_PLAFOND = '<div class="reg-row"><span class="reg-label">Plafond de revenus</span><span class="reg-val">77 700 €/an (revenus 2025) · 83 600 €/an (revenus 2026)</span></div>'


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    ancien_intro_complet = f'<p>{ANCIEN_INTRO}</p>'
    if ancien_intro_complet in contenu:
        contenu = contenu.replace(ancien_intro_complet, f'<p>{NOUVEAU_INTRO}\n  </div>', 1)
        nb_modifs += 1

    if ANCIEN_PLAFOND in contenu:
        contenu = contenu.replace(ANCIEN_PLAFOND, NOUVEAU_PLAFOND, 1)
        nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou textes attendus non trouvés.")
        return

    with open(FICHIER + ".bak_art207", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Encart reforme plus-value 2025 ajoute, plafond micro-BIC mis a jour")


if __name__ == "__main__":
    main()
