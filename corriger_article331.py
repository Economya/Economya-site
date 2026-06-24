#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réécriture article-331.html — exclusion des chaudières biomasse du
parcours "par geste" MaPrimeRénov' depuis le 1er janvier 2026
À lancer depuis ~/Desktop/mon site

Changement de fond (pas juste un chiffre) : depuis le 1er janvier 2026
(décret n°2025-956 du 8 septembre 2025), les chaudières biomasse
automatiques et manuelles — donc les chaudières à granulés — ne sont
PLUS éligibles au parcours "par geste" de MaPrimeRénov'. Elles restent
finançables uniquement via le parcours "rénovation d'ampleur" (projet
combinant au moins 2 gestes d'isolation).

Le poêle à granulés (insert), différent d'une chaudière, reste éligible
au parcours "par geste".

Modifications :
1. Intro : retire la promesse "jusqu'à 10 000€ via MaPrimeRénov'" sans
   nuance, ajoute la distinction chaudière/poêle
2. Carte "types" : ajoute un badge d'avertissement sur les 2 types
   "chaudière" (automatique et avec ballon ECS)
3. Carte aide MaPrimeRénov' : réécrite pour expliquer la double situation
4. Exemple de rentabilité : remplacé par un encart honnête plutôt qu'un
   chiffre inventé pour un scénario de rénovation d'ampleur trop complexe
   à simuler avec confiance
5. Dates 2025 -> 2026

Idempotent. Sauvegarde en .bak_art331.

Usage :
    python3 corriger_article331.py
"""

import os

FICHIER = "article-331.html"

REMPLACEMENTS = [
    (
        "Chaudière à granulés : prix et subventions — Jusqu'à 10 000€ d'aide. Guide complet sur Economya.fr",
        "Chaudière à granulés : prix et subventions 2026 — aides selon parcours. Guide complet sur Economya.fr",
    ),
    (
        '<div class="savings-badge">💰 Jusqu\'à 10 000 € d\'aide</div>',
        '<div class="savings-badge">💰 Aides selon le parcours choisi</div>',
    ),
    (
        '<div class="stat-cell"><span class="stat-num">10 000 €</span><span class="stat-lbl">d\'aides MaPrimeRénov\' possibles</span></div>',
        '<div class="stat-cell"><span class="stat-num">Variable</span><span class="stat-lbl">selon parcours (geste ou ampleur)</span></div>',
    ),
    (
        "La chaudière à granulés (ou pellets) est l'une des solutions de chauffage les plus rentables pour remplacer une chaudière fioul ou gaz : carbone neutre, coût du combustible stable et bas, et jusqu'à 10 000 € d'aides disponibles via MaPrimeRénov'.",
        "La chaudière à granulés (ou pellets) est l'une des solutions de chauffage les plus rentables pour remplacer une chaudière fioul ou gaz : carbone neutre et coût du combustible stable et bas. ⚠️ Depuis le 1er janvier 2026, les chaudières à granulés ne sont plus finançables via le parcours MaPrimeRénov' \"par geste\" — elles doivent désormais s'inscrire dans une rénovation d'ampleur (projet combinant au moins 2 gestes d'isolation). Le poêle à granulés (insert), lui, reste éligible au parcours simple.",
    ),
    (
        '<div class="type top">\n      <span class="top-badge">⭐ La plus populaire</span>\n      <div class="type-icon">🏠</div>\n      <div class="type-name">Chaudière à granulés automatique</div>\n      <div class="type-prix">8 000–18 000 €</div>\n      <div class="type-desc">Alimentation automatique depuis un silo. Très confortable, quasi-autonome. Entretien annuel par un professionnel. Idéale pour remplacer une chaudière fioul centrale.</div>\n    </div>',
        '<div class="type top">\n      <span class="top-badge">⚠️ Non éligible au parcours simple depuis 2026</span>\n      <div class="type-icon">🏠</div>\n      <div class="type-name">Chaudière à granulés automatique</div>\n      <div class="type-prix">8 000–18 000 €</div>\n      <div class="type-desc">Alimentation automatique depuis un silo. Très confortable, quasi-autonome. Entretien annuel par un professionnel. Depuis le 1er janvier 2026, finançable uniquement via une rénovation d\'ampleur (avec au moins 2 gestes d\'isolation), plus via le parcours simple.</div>\n    </div>',
    ),
    (
        '<div class="type-name">Chaudière à granulés avec ballon ECS</div>\n      <div class="type-prix">10 000–20 000 €</div>\n      <div class="type-desc">Alimente le chauffage central ET l\'eau chaude sanitaire. Solution complète pour remplacer totalement la chaudière fioul ou gaz.</div>',
        '<div class="type-name">Chaudière à granulés avec ballon ECS</div>\n      <div class="type-prix">10 000–20 000 €</div>\n      <div class="type-desc">Alimente le chauffage central ET l\'eau chaude sanitaire. Comme la chaudière simple, non éligible au parcours \"par geste\" depuis 2026 — uniquement via rénovation d\'ampleur.</div>',
    ),
    (
        "💶 Les aides disponibles en 2025",
        "💶 Les aides disponibles en 2026",
    ),
    (
        '<div class="aide top">\n      <div class="aide-icon">🏛️</div>\n      <div class="aide-body">\n        <h3>MaPrimeRénov\' (ANAH)</h3>\n        <p>Aide principale calculée selon les revenus. Les ménages très modestes remplaçant une chaudière fioul par une chaudière granulés peuvent atteindre 10 000 € d\'aide. Demande obligatoire avant les travaux sur maprimerenov.gouv.fr.</p>\n      </div>\n      <div class="aide-right"><span class="aide-amt">5 000–10 000 €</span><span class="aide-sub">selon revenus</span></div>\n    </div>',
        '<div class="aide top">\n      <div class="aide-icon">🏛️</div>\n      <div class="aide-body">\n        <h3>MaPrimeRénov\' (ANAH) — selon l\'équipement</h3>\n        <p>⚠️ Depuis le 1er janvier 2026, une chaudière à granulés seule n\'est plus finançable via le parcours \"par geste\". Elle reste éligible si le projet s\'inscrit dans une rénovation d\'ampleur (au moins 2 gestes d\'isolation, accompagnement obligatoire). Le poêle à granulés (insert), en revanche, reste finançable au parcours simple, à un montant plus modeste. Demande obligatoire avant les travaux sur maprimerenov.gouv.fr.</p>\n      </div>\n      <div class="aide-right"><span class="aide-amt">Variable</span><span class="aide-sub">selon parcours et équipement</span></div>\n    </div>',
    ),
    (
        '<h2>📊 Exemple de rentabilité</h2>\n  <div class="renta">\n    <h3>💡 Maison 120 m² — Remplacement chaudière fioul</h3>\n    <div class="renta-grid">\n      <div class="renta-item"><div class="renta-label">Coût installation</div><div class="renta-val">14 000 €</div></div>\n      <div class="renta-item"><div class="renta-label">MaPrimeRénov\' (mod.)</div><div class="renta-val">−6 000 €</div></div>\n      <div class="renta-item"><div class="renta-label">CEE estimés</div><div class="renta-val">−1 500 €</div></div>\n      <div class="renta-item"><div class="renta-label">Reste à charge</div><div class="renta-val">6 500 €</div></div>\n      <div class="renta-item"><div class="renta-label">Économies/an (vs fioul)</div><div class="renta-val">~900 €/an</div></div>\n      <div class="renta-item"><div class="renta-label">Retour investissement</div><div class="renta-val">~7 ans</div></div>\n    </div>\n  </div>',
        '<h2>📊 Coût réel selon votre situation</h2>\n  <div class="renta">\n    <h3>💡 Maison 120 m² — Remplacement chaudière fioul</h3>\n    <p style="margin-bottom:1rem">Le coût final dépend désormais fortement du parcours suivi : une chaudière seule (sans MaPrimeRénov\' depuis 2026) coûte environ <strong>14 000 €</strong>, financée seulement par les CEE (environ −1 500 €) et la TVA réduite, soit un reste à charge proche de <strong>12 000 €</strong>. En revanche, intégrée à une rénovation d\'ampleur avec isolation, le taux de prise en charge MaPrimeRénov\' peut atteindre 45 à 80 % du coût global selon vos revenus — mais le projet est alors plus vaste et plus coûteux dans l\'absolu. Demandez un devis personnalisé via un Accompagnateur Rénov\' agréé pour connaître votre reste à charge exact.</p>\n  </div>',
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
        print("✅ Déjà corrigé ou textes attendus non trouvés.")
        return

    with open(FICHIER + ".bak_art331", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Réécriture complète : exclusion chaudière granulés du parcours")
    print("   'par geste' depuis 2026, distinction avec le poêle à granulés.")


if __name__ == "__main__":
    main()
