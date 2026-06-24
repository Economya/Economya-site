#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réécriture article-185.html — confusion fondamentale MaPrimeRénov'/photovoltaïque
À lancer depuis ~/Desktop/mon site

ERREUR DE FOND identifiée (confirmée par de nombreuses sources convergentes,
décrite comme "la confusion la plus répandue sur le web") : MaPrimeRénov'
NE FINANCE PAS les panneaux photovoltaïques (production d'électricité) —
uniquement le solaire thermique (chauffe-eau). L'article, consacré à la
PRODUCTION D'ÉLECTRICITÉ, citait à tort MaPrimeRénov' comme une aide
disponible.

Autres corrections :
- TVA : 10% n'est plus applicable au photovoltaïque depuis le 1er janvier
  2026 (remplacée par 5,5% sous conditions strictes, ou 20% sinon)
- Prime autoconsommation : montant et existence même incertains à la date
  de rédaction (sources contradictoires sur une suppression début juin
  2026) — formulation prudente avec renvoi vers EDF OA pour vérification
- Dates 2025 -> 2026

Idempotent. Sauvegarde en .bak_art185.

Usage :
    python3 corriger_article185.py
"""

import os

FICHIER = "article-185.html"

REMPLACEMENTS = [
    (
        "En 2025, le prix des panneaux solaires a chuté de plus de 70 % en dix ans. Ce qui coûtait 15 000 euros il y a une décennie pour une installation de 3 kWc s'obtient aujourd'hui pour moins de 6 000 euros — avant aides. Et les aides, justement, n'ont jamais été aussi généreuses : MaPrimeRénov', prime autoconsommation, TVA réduite, éco-PTZ. Pour un propriétaire avec un toit bien exposé, l'investissement peut être rentabilisé en 6 à 10 ans et générer de l'électricité gratuite pendant 25 ans. Même pour les locataires ou ceux qui ne peuvent pas installer sur leur toit, des solutions accessibles existent désormais.",
        "Le prix des panneaux solaires a chuté de plus de 70 % en dix ans. Ce qui coûtait 15 000 euros il y a une décennie pour une installation de 3 kWc s'obtient aujourd'hui pour moins de 6 000 euros — avant aides. ⚠️ Attention à une confusion très répandue : MaPrimeRénov' ne finance PAS les panneaux photovoltaïques (production d'électricité) — uniquement le solaire thermique (chauffe-eau). Pour le photovoltaïque, les dispositifs concernés sont la prime à l'autoconsommation, la TVA réduite et l'éco-PTZ. Pour un propriétaire avec un toit bien exposé, l'investissement peut être rentabilisé en 6 à 10 ans et générer de l'électricité gratuite pendant 25 ans. Même pour les locataires ou ceux qui ne peuvent pas installer sur leur toit, des solutions accessibles existent désormais.",
    ),
    (
        "Les aides disponibles en 2025",
        "Les aides disponibles en 2026",
    ),
    (
        '<div class="aide">\n      <div class="aide-emoji">🏛️</div>\n      <div class="aide-nom">Prime autoconsommation (EDF OA)</div>\n      <div class="aide-desc">Prime versée sur 5 ans pour toute installation en autoconsommation avec vente du surplus. Montant variable selon la puissance installée.</div>\n      <div class="aide-montant">230 à 580€/kWc selon puissance</div>\n    </div>\n    <div class="aide">\n      <div class="aide-emoji">🏠</div>\n      <div class="aide-nom">MaPrimeRénov\' Sérénité</div>\n      <div class="aide-desc">Pour les ménages modestes, couvre une partie de l\'installation solaire dans le cadre d\'une rénovation globale du logement.</div>\n      <div class="aide-montant">Jusqu\'à 50% du coût travaux</div>\n    </div>\n    <div class="aide">\n      <div class="aide-emoji">📊</div>\n      <div class="aide-nom">TVA à 10% (au lieu de 20%)</div>\n      <div class="aide-desc">Toute installation solaire sur résidence principale bénéficie d\'une TVA réduite à 10% — un avantage immédiat sur la facture installateur.</div>\n      <div class="aide-montant">jusqu\'à -10% sur le montant HT</div>\n    </div>',
        '<div class="aide">\n      <div class="aide-emoji">🏛️</div>\n      <div class="aide-nom">Prime à l\'autoconsommation (EDF OA)</div>\n      <div class="aide-desc">⚠️ Ce dispositif évolue fréquemment (montant révisé chaque trimestre, statut même incertain selon les périodes en 2026). Versée en une seule fois après mise en service. Vérifiez le montant et l\'existence actuelle du dispositif directement sur le site officiel EDF OA avant tout projet.</div>\n      <div class="aide-montant">Variable selon puissance — à vérifier sur edf-oa.fr</div>\n    </div>\n    <div class="aide">\n      <div class="aide-emoji">🚫</div>\n      <div class="aide-nom">MaPrimeRénov\' — NON applicable au photovoltaïque</div>\n      <div class="aide-desc">MaPrimeRénov\' ne finance que le solaire thermique (chauffe-eau solaire, système solaire combiné), jamais les panneaux produisant de l\'électricité. Si vous installez des panneaux hybrides, seule la partie thermique de l\'installation peut y être éligible.</div>\n      <div class="aide-montant">Non éligible pour le photovoltaïque</div>\n    </div>\n    <div class="aide">\n      <div class="aide-emoji">📊</div>\n      <div class="aide-nom">TVA réduite (depuis janvier 2026)</div>\n      <div class="aide-desc">Depuis le 1er janvier 2026, la TVA à 10% n\'est plus applicable au photovoltaïque. Seules deux options existent désormais : 5,5% sous conditions strictes (installations ≤ 9 kWc avec critères de performance environnementale), ou TVA normale à 20% sinon.</div>\n      <div class="aide-montant">5,5% (conditions strictes) ou 20%</div>\n    </div>',
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

    with open(FICHIER + ".bak_art185", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   ERREUR DE FOND corrigée : MaPrimeRénov' ne finance PAS le")
    print("   photovoltaïque (confusion très répandue). TVA et autoconso mises à jour.")


if __name__ == "__main__":
    main()
