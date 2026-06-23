#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du footer de index.html — liens manquants
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Problème : "Mentions légales" et "Contact" étaient du texte brut, pas des
liens cliquables. "Politique de confidentialité" était absente du footer.
Seules les autres pages du site avaient ces liens fonctionnels.

Idempotent. Sauvegarde en .bak_footer avant modification.

Usage :
    python3 corriger_footer_index.py
"""

import os

FICHIER = "index.html"

ANCIEN = "© 2026 · Mentions légales · Contact · Economya peut percevoir une commission sur certains liens présents sur ce site, sans coût supplémentaire pour vous."

NOUVEAU = '© 2026 · <a href="mentions-legales.html" style="color:rgba(255,255,255,.7)">Mentions légales</a> · <a href="politique-confidentialite.html" style="color:rgba(255,255,255,.7)">Politique de confidentialité</a> · <a href="mailto:contact@economya.fr" style="color:rgba(255,255,255,.7)">Contact</a> · Economya peut percevoir une commission sur certains liens présents sur ce site, sans coût supplémentaire pour vous.'


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
    with open(FICHIER + ".bak_footer", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    print("✅ Footer corrigé : liens 'Mentions légales' et 'Contact' fonctionnels,")
    print("   'Politique de confidentialité' ajoutée.")


if __name__ == "__main__":
    main()
