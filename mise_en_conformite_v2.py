#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de mise en conformité RGPD v2 — AdSense + disclaimer + année
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site
APRÈS avoir lancé mise_en_conformite_cookies.py (script v1)

Ce script fait 4 choses, chacune indépendante et idempotente :
1. Remplace le chargement automatique d'AdSense par un chargement conditionnel
2. Met à jour la fonction apply() du bandeau cookies pour charger aussi les pubs
3. Corrige le disclaimer en footer ("Cet article contient..." -> texte générique)
4. Met à jour "© 2025" en "© 2026"

Sauvegarde chaque fichier modifié en .bak_v2 avant modification.
Sans danger à relancer plusieurs fois.

Usage :
    python3 mise_en_conformite_v2.py
"""

import os
import re
import glob

# --- 1. Nouveau script AdSense conditionnel (remplace le chargement direct) ---
ANCIEN_ADSENSE_PATTERN = re.compile(
    r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-3051071564398795"\s*'
    r'crossorigin="anonymous"></script>',
    re.MULTILINE
)

NOUVEAU_ADSENSE = '''<script>
window.economyaLoadAds = function() {
  if (window.economyaAdsLoaded) return;
  window.economyaAdsLoaded = true;
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3051071564398795";
  s.crossOrigin = "anonymous";
  document.head.appendChild(s);
};
</script>'''

# --- 2. Mise à jour de la fonction apply() dans le bandeau déjà inséré ---
ANCIEN_APPLY = 'function apply(v){if(v==="accepted"){if(typeof window.economyaLoadGA==="function"){window.economyaLoadGA();}}}'
NOUVEAU_APPLY = 'function apply(v){if(v==="accepted"){if(typeof window.economyaLoadGA==="function"){window.economyaLoadGA();}if(typeof window.economyaLoadAds==="function"){window.economyaLoadAds();}}}'

# --- 3. Disclaimer footer ---
ANCIEN_DISCLAIMER = "Cet article contient des liens partenaires."
NOUVEAU_DISCLAIMER = "Economya peut percevoir une commission sur certains liens présents sur ce site, sans coût supplémentaire pour vous."

# --- 4. Année ---
ANCIENNE_ANNEE = "© 2025"
NOUVELLE_ANNEE = "© 2026"


def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    modifications = []

    # 1. AdSense conditionnel
    if "economyaLoadAds" not in contenu and ANCIEN_ADSENSE_PATTERN.search(contenu):
        contenu = ANCIEN_ADSENSE_PATTERN.sub(NOUVEAU_ADSENSE, contenu, count=1)
        modifications.append("AdSense conditionnel")

    # 2. Mise à jour fonction apply() du bandeau
    if ANCIEN_APPLY in contenu:
        contenu = contenu.replace(ANCIEN_APPLY, NOUVEAU_APPLY)
        modifications.append("Bandeau mis à jour (pubs incluses)")

    # 3. Disclaimer footer
    if ANCIEN_DISCLAIMER in contenu:
        contenu = contenu.replace(ANCIEN_DISCLAIMER, NOUVEAU_DISCLAIMER)
        modifications.append("Disclaimer corrigé")

    # 4. Année
    if ANCIENNE_ANNEE in contenu:
        contenu = contenu.replace(ANCIENNE_ANNEE, NOUVELLE_ANNEE)
        modifications.append("Année mise à jour")

    if contenu == contenu_original:
        return None

    chemin_bak = chemin + ".bak_v2"
    if not os.path.exists(chemin_bak):
        with open(chemin_bak, 'w', encoding='utf-8') as f:
            f.write(contenu_original)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu)

    return modifications


def main():
    fichiers = sorted(glob.glob("*.html"))

    total_modifies = 0
    compteurs = {"AdSense conditionnel": 0, "Bandeau mis à jour (pubs incluses)": 0,
                 "Disclaimer corrigé": 0, "Année mise à jour": 0}
    erreurs = []

    for fichier in fichiers:
        try:
            resultat = traiter_fichier(fichier)
            if resultat:
                total_modifies += 1
                for r in resultat:
                    compteurs[r] += 1
        except Exception as e:
            erreurs.append(f"{fichier} : {e}")

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers traités : {len(fichiers)}")
    print(f"Fichiers modifiés : {total_modifies}")
    for k, v in compteurs.items():
        print(f"  - {k} : {v}")
    print(f"Erreurs : {len(erreurs)}")
    for e in erreurs:
        print(f"  ⚠️  {e}")
    print(f"\nSauvegardes créées avec l'extension .bak_v2")


if __name__ == "__main__":
    main()
