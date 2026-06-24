#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-329.html — lien croisé daté vers article-322
À lancer depuis ~/Desktop/mon site

"Pompe à chaleur :aides et rentabilité 2025" -> "...2026" (le titre réel
de l'article-322 cible a déjà été corrigé, ce lien-texte avait été oublié
car non couvert par le script de liens croisés du premier passage).

Idempotent. Sauvegarde en .bak_art329.

Usage :
    python3 corriger_article329.py
"""

import os

FICHIER = "article-329.html"

ANCIEN = '<div class="sim-card-title">Pompe à chaleur :aides et rentabilité 2025</div>'
NOUVEAU = '<div class="sim-card-title">Pompe à chaleur :aides et rentabilité 2026</div>'


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
    with open(FICHIER + ".bak_art329", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Lien croisé corrigé : 2025 -> 2026")


if __name__ == "__main__":
    main()
