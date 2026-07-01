#!/usr/bin/env python3
"""
Intègre 2 nouveaux outils dans outils-gratuits.html :
1. "Coût réel d'un appartement" -> nouvelle section "🏘️ Propriétaire & Copropriété"
   (insérée entre la section Immobilier & Logement et Emploi/Fiscalité/Transport)
2. "Budget vacances" -> section "🎯 Profil, Habitudes & Voyage"
   (insérée après le quiz voyageur, avant Pouvoir d'achat réel)
3. Compteur 28 -> 30 outils disponibles.

Idempotent : si déjà fait, ne fait rien.
Sauvegarde .bak_ajout2outils avant modification.
"""

import os
import shutil

FICHIER = "outils-gratuits.html"

# --- 1. Nouvelle section Propriétaire & Copropriété ---
ANCRE_IMMO = '''    </a>
  </div>

  <div class="section-title">💼 Emploi, Fiscalité & Transport</div>'''

NOUVELLE_SECTION_IMMO = '''    </a>
  </div>

  <div class="section-title">🏘️ Propriétaire & Copropriété</div>
  <div class="tools-grid">
    <a href="calculateur-cout-appartement.html" class="tool-card featured">
      <span class="new-badge">🆕 Nouveau</span>
      <span class="tool-icon">🏢</span>
      <div class="tool-cat">Calculateur</div>
      <div class="tool-name">Coût réel d'un appartement</div>
      <div class="tool-desc">Au-delà du crédit : charges de copropriété, taxe foncière, assurance, entretien.</div>
      <span class="tool-btn">Calculer →</span>
    </a>
  </div>

  <div class="section-title">💼 Emploi, Fiscalité & Transport</div>'''

# --- 2. Carte Budget vacances ---
ANCRE_VOYAGE = '''      <span class="tool-btn">Faire le quiz →</span>
    </a>
    <a href="calculateur-pouvoir-achat.html" class="tool-card">'''

NOUVELLE_CARTE_VOYAGE = '''      <span class="tool-btn">Faire le quiz →</span>
    </a>
    <a href="calculateur-budget-vacances.html" class="tool-card">
      <span class="new-badge">🆕 Nouveau</span>
      <span class="tool-icon">🧳</span>
      <div class="tool-cat">Calculateur</div>
      <div class="tool-name">Budget vacances</div>
      <div class="tool-desc">Combien va coûter votre voyage ? Budget chiffré par poste et épargne mensuelle nécessaire.</div>
      <span class="tool-btn">Calculer →</span>
    </a>
    <a href="calculateur-pouvoir-achat.html" class="tool-card">'''

# --- 3. Compteur ---
COMPTEUR_ANCIEN = '<div class="stat"><span class="stat-num">28</span><div class="stat-lbl">Outils disponibles</div></div>'
COMPTEUR_NOUVEAU = '<div class="stat"><span class="stat-num">30</span><div class="stat-lbl">Outils disponibles</div></div>'


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    corrections = 0

    if 'calculateur-cout-appartement.html' in contenu_modifie:
        print("ℹ️  Section 'Propriétaire & Copropriété' déjà présente (idempotent)")
    elif ANCRE_IMMO in contenu_modifie:
        contenu_modifie = contenu_modifie.replace(ANCRE_IMMO, NOUVELLE_SECTION_IMMO, 1)
        corrections += 1
        print("✅ Nouvelle section 'Propriétaire & Copropriété' ajoutée")
    else:
        print("⚠️  Ancre Immobilier non trouvée — vérifiez manuellement")

    if 'calculateur-budget-vacances.html' in contenu_modifie:
        print("ℹ️  Carte 'Budget vacances' déjà présente (idempotent)")
    elif ANCRE_VOYAGE in contenu_modifie:
        contenu_modifie = contenu_modifie.replace(ANCRE_VOYAGE, NOUVELLE_CARTE_VOYAGE, 1)
        corrections += 1
        print("✅ Carte 'Budget vacances' ajoutée")
    else:
        print("⚠️  Ancre Voyage non trouvée — vérifiez manuellement")

    if COMPTEUR_ANCIEN in contenu_modifie:
        contenu_modifie = contenu_modifie.replace(COMPTEUR_ANCIEN, COMPTEUR_NOUVEAU, 1)
        corrections += 1
        print("✅ Compteur mis à jour : 28 -> 30")
    elif COMPTEUR_NOUVEAU in contenu_modifie:
        print("ℹ️  Compteur déjà à jour (idempotent)")
    else:
        print("⚠️  Compteur non trouvé — vérifiez manuellement")

    if corrections == 0:
        print("✅ Rien à faire — le fichier est déjà à jour.")
        return

    shutil.copy2(FICHIER, FICHIER + ".bak_ajout2outils")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"\n✅ {corrections} modification(s) écrite(s) dans {FICHIER}")
    print(f"   Sauvegarde créée : {FICHIER}.bak_ajout2outils")


if __name__ == "__main__":
    main()
