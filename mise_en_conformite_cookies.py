#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de mise en conformité RGPD (cookies + GA conditionnel)
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Ce script :
1. Sauvegarde chaque fichier modifié en .bak_cookies avant toute modification
2. Remplace l'ancien bloc Google Analytics (chargement automatique) par le script conditionnel
3. Insère le bandeau cookies avant </body> (si pas déjà présent)
4. Est SANS DANGER à relancer plusieurs fois (idempotent) : il ne modifie pas un fichier déjà à jour
5. N'IMPORTE PAS index.html (déjà fait manuellement)

Usage :
    python3 mise_en_conformite_cookies.py
"""

import os
import re
import glob

# Le nouveau script GA conditionnel (remplace l'ancien bloc)
NOUVEAU_GA = '''<script>
window.dataLayer = window.dataLayer || [];
function gtag(){ window.dataLayer.push(arguments); }
window.gtag = gtag;
window.economyaLoadGA = function() {
  if (window.economyaGALoaded) return;
  window.economyaGALoaded = true;
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=G-YBK8GHCDT5";
  document.head.appendChild(s);
  gtag("js", new Date());
  gtag("config", "G-YBK8GHCDT5");
};
</script>'''

# Le bandeau cookies complet
BANDEAU_COOKIES = '''<div id="economya-cookie-banner" style="display:none;position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#085041;color:#ffffff;padding:18px 20px;box-shadow:0 -2px 10px rgba(0,0,0,0.15);">
<div style="max-width:1100px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;">
<p style="margin:0;font-size:0.9rem;line-height:1.5;flex:1;min-width:240px;">Nous utilisons des cookies pour mesurer l'audience du site. Vous pouvez accepter ou refuser les cookies non essentiels. <a href="/politique-confidentialite.html" style="color:#EF9F27;text-decoration:underline;">En savoir plus</a></p>
<div style="display:flex;gap:10px;flex-shrink:0;">
<button id="economya-cookie-refuse" style="background:transparent;border:1px solid #ffffff;color:#ffffff;padding:8px 18px;border-radius:4px;cursor:pointer;font-size:0.85rem;">Refuser</button>
<button id="economya-cookie-accept" style="background:#EF9F27;border:none;color:#2C2C2A;padding:8px 18px;border-radius:4px;cursor:pointer;font-weight:600;font-size:0.85rem;">Accepter</button>
</div></div></div>
<script>
(function(){
var K="economya_cookie_consent";
var D=180;
function getC(){try{var r=localStorage.getItem(K);if(!r)return null;var d=JSON.parse(r);var e=new Date(d.timestamp);e.setDate(e.getDate()+D);if(new Date()>e)return null;return d.value;}catch(e){return null;}}
function setC(v){try{localStorage.setItem(K,JSON.stringify({value:v,timestamp:new Date().toISOString()}));}catch(e){}}
function apply(v){if(v==="accepted"){if(typeof window.economyaLoadGA==="function"){window.economyaLoadGA();}}}
var existing=getC();
var banner=document.getElementById("economya-cookie-banner");
if(existing){apply(existing);}else if(banner){banner.style.display="block";}
var a=document.getElementById("economya-cookie-accept");
var r=document.getElementById("economya-cookie-refuse");
if(a){a.addEventListener("click",function(){setC("accepted");apply("accepted");banner.style.display="none";});}
if(r){r.addEventListener("click",function(){setC("refused");banner.style.display="none";});}
})();
</script>'''

# Regex pour repérer l'ancien bloc GA (du commentaire jusqu'au </script> qui ferme le 2e script)
ANCIEN_GA_PATTERN = re.compile(
    r"<!--\s*Google Analytics\s*-->\s*"
    r"<script async src=\"https://www\.googletagmanager\.com/gtag/js\?id=G-YBK8GHCDT5\"></script>\s*"
    r"<script>\s*"
    r"window\.dataLayer = window\.dataLayer \|\| \[\];\s*"
    r"function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*"
    r"gtag\('js', new Date\(\)\);\s*"
    r"gtag\('config', 'G-YBK8GHCDT5'\);\s*"
    r"</script>",
    re.MULTILINE
)

def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    modifications = []

    # 1. Remplacer l'ancien bloc GA si présent et pas déjà fait
    if "economyaLoadGA" not in contenu and ANCIEN_GA_PATTERN.search(contenu):
        contenu = ANCIEN_GA_PATTERN.sub(NOUVEAU_GA, contenu, count=1)
        modifications.append("GA conditionnel ajouté")

    # 2. Insérer le bandeau cookies avant </body> si pas déjà présent
    if "economya-cookie-banner" not in contenu and "</body>" in contenu:
        contenu = contenu.replace("</body>", BANDEAU_COOKIES + "\n</body>", 1)
        modifications.append("Bandeau cookies ajouté")

    # Si rien à changer, on ne touche pas au fichier
    if contenu == contenu_original:
        return None

    # Sauvegarde avant modification
    chemin_bak = chemin + ".bak_cookies"
    if not os.path.exists(chemin_bak):
        with open(chemin_bak, 'w', encoding='utf-8') as f:
            f.write(contenu_original)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu)

    return modifications


def main():
    fichiers = sorted(glob.glob("*.html"))
    fichiers = [f for f in fichiers if f != "index.html"]  # déjà fait manuellement

    total_modifies = 0
    total_ga = 0
    total_bandeau = 0
    erreurs = []

    for fichier in fichiers:
        try:
            resultat = traiter_fichier(fichier)
            if resultat:
                total_modifies += 1
                if "GA conditionnel ajouté" in resultat:
                    total_ga += 1
                if "Bandeau cookies ajouté" in resultat:
                    total_bandeau += 1
        except Exception as e:
            erreurs.append(f"{fichier} : {e}")

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers traités : {len(fichiers)}")
    print(f"Fichiers modifiés : {total_modifies}")
    print(f"  - avec GA conditionnel ajouté : {total_ga}")
    print(f"  - avec bandeau cookies ajouté : {total_bandeau}")
    print(f"Erreurs : {len(erreurs)}")
    for e in erreurs:
        print(f"  ⚠️  {e}")
    print(f"\nSauvegardes créées avec l'extension .bak_cookies")
    print(f"Pour annuler une modification sur un fichier : mv fichier.html.bak_cookies fichier.html")


if __name__ == "__main__":
    main()
