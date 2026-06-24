#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-484.html — date obsolète + avertissement réforme ACRE
À lancer depuis ~/Desktop/mon site

Cas particulier : les chiffres actuels (50%, taux 12,3/21,2/23,2%) sont
TOUJOURS CORRECTS aujourd'hui (24 juin 2026). Mais une réforme entre en
vigueur le 1er juillet 2026 (décret n°2026-69) qui réduira ce taux de
50% à 25%. On ajoute un avertissement clair plutôt que de modifier des
chiffres qui ne sont pas encore faux.

1. "Vérifié mai 2025" -> "Vérifié juin 2026"
2. Ajout d'un avertissement sur la réforme du 1er juillet 2026

Idempotent. Sauvegarde en .bak_art484.

Usage :
    python3 corriger_article484.py
"""

import os

FICHIER = "article-484.html"

ANCIEN_VERIFIE = "📅 Vérifié mai 2025"
NOUVEAU_VERIFIE = "📅 Vérifié juin 2026"

ANCIEN_LEAD = "L'ACRE (Aide à la Création ou Reprise d'une Entreprise) divise par deux vos cotisations sociales pendant les 12 premiers mois d'activité. Accessible à la plupart des créateurs d'entreprise, elle peut représenter une économie de plusieurs milliers d'euros et faciliter considérablement le démarrage. Voici tout ce qu'il faut savoir."

NOUVEAU_LEAD_AVEC_AVERTISSEMENT = """L'ACRE (Aide à la Création ou Reprise d'une Entreprise) divise par deux vos cotisations sociales pendant les 12 premiers mois d'activité. Accessible à la plupart des créateurs d'entreprise, elle peut représenter une économie de plusieurs milliers d'euros et faciliter considérablement le démarrage. Voici tout ce qu'il faut savoir.</p>

  <div style="background:#FEF3C7;border-left:4px solid #F59E0B;border-radius:8px;padding:1rem 1.4rem;margin:1.5rem 0;font-size:.9rem;color:#633806;">
    <strong>⚠️ Changement important au 1er juillet 2026 :</strong> le taux d'exonération ACRE passe de 50 % à 25 % pour les créations d'entreprise à partir de cette date (décret n°2026-69). Les chiffres ci-dessous restent valables pour les entreprises créées avant le 1er juillet 2026. Si vous créez après cette date, l'économie réelle sera deux fois moins importante.
  </div>

  <p class="lead"></p"""


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu

    if "1er juillet 2026" in contenu and "2025" not in contenu:
        print("✅ Déjà corrigé.")
        return

    nb_modifs = 0

    if ANCIEN_VERIFIE in contenu:
        contenu = contenu.replace(ANCIEN_VERIFIE, NOUVEAU_VERIFIE)
        nb_modifs += 1

    if ANCIEN_LEAD in contenu:
        # Remplace le texte + ajoute l'avertissement juste après le </p> existant
        ancien_complet = f'<p class="lead">{ANCIEN_LEAD}</p>'
        nouveau_complet = NOUVEAU_LEAD_AVEC_AVERTISSEMENT.replace(
            ANCIEN_LEAD, ANCIEN_LEAD
        )
        if ancien_complet in contenu:
            contenu = contenu.replace(
                ancien_complet,
                f'<p class="lead">{ANCIEN_LEAD}</p>\n\n'
                f'  <div style="background:#FEF3C7;border-left:4px solid #F59E0B;'
                f'border-radius:8px;padding:1rem 1.4rem;margin:1.5rem 0;'
                f'font-size:.9rem;color:#633806;">\n'
                f'    <strong>⚠️ Changement important au 1er juillet 2026 :</strong> '
                f'le taux d\'exonération ACRE passe de 50 % à 25 % pour les créations '
                f'd\'entreprise à partir de cette date (décret n°2026-69). Les chiffres '
                f'ci-dessous restent valables pour les entreprises créées avant le '
                f'1er juillet 2026. Si vous créez après cette date, l\'économie réelle '
                f'sera deux fois moins importante.\n'
                f'  </div>'
            )
            nb_modifs += 1

    if nb_modifs == 0:
        print("⚠️ Textes attendus non trouvés. Aucune modification.")
        return

    with open(FICHIER + ".bak_art484", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} modification(s) appliquée(s) sur {FICHIER}")
    print("   - Date mise à jour (juin 2026)")
    print("   - Avertissement ajouté sur la réforme ACRE du 1er juillet 2026")


if __name__ == "__main__":
    main()
