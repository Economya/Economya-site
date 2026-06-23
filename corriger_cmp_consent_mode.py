#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mise en place d'une CMP catégorisée + Google Consent Mode v2
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Remplace le bandeau cookies simple (Accepter/Refuser) par une CMP complète :
- Bouton "Tout accepter"
- Bouton "Tout refuser"
- Bouton "Personnaliser" avec catégories séparées (Analytics / Publicité)
- Déclaration Google Consent Mode v2 (consent default + update)
- Stockage du consentement par catégorie (pas juste accepté/refusé en bloc)

Idempotent. Sauvegarde en .bak_cmp avant modification.

Usage :
    python3 corriger_cmp_consent_mode.py
"""

import os
import re
import glob

# --- 1. Déclaration Consent Mode v2 par défaut, à insérer juste après dataLayer init ---
ANCIEN_DATALAYER_INIT = '''window.dataLayer = window.dataLayer || [];
function gtag(){ window.dataLayer.push(arguments); }
window.gtag = gtag;'''

NOUVEAU_DATALAYER_INIT = '''window.dataLayer = window.dataLayer || [];
function gtag(){ window.dataLayer.push(arguments); }
window.gtag = gtag;
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'wait_for_update': 500
});'''

# --- 2. Remplacement complet du bandeau + script (Accepter/Refuser simple) ---
ANCIEN_BANNER_BLOC_PATTERN = re.compile(
    r'<div id="economya-cookie-banner".*?</script>\s*',
    re.DOTALL
)

NOUVEAU_BANNER_BLOC = '''<div id="economya-cookie-banner" style="display:none;position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#085041;color:#ffffff;padding:18px 20px;box-shadow:0 -2px 10px rgba(0,0,0,0.15);">
<div style="max-width:1100px;margin:0 auto;">
<div id="economya-cmp-simple" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;">
<p style="margin:0;font-size:0.9rem;line-height:1.5;flex:1;min-width:240px;">Nous utilisons des cookies pour mesurer l'audience du site et diffuser des publicités. Vous pouvez choisir les catégories que vous acceptez. <a href="/politique-confidentialite.html" style="color:#EF9F27;text-decoration:underline;">En savoir plus</a></p>
<div style="display:flex;gap:10px;flex-shrink:0;flex-wrap:wrap;">
<button id="economya-cmp-personnaliser" style="background:transparent;border:1px solid #ffffff;color:#ffffff;padding:8px 16px;border-radius:4px;cursor:pointer;font-size:0.85rem;">Personnaliser</button>
<button id="economya-cookie-refuse" style="background:transparent;border:1px solid #ffffff;color:#ffffff;padding:8px 16px;border-radius:4px;cursor:pointer;font-size:0.85rem;">Tout refuser</button>
<button id="economya-cookie-accept" style="background:#EF9F27;border:none;color:#2C2C2A;padding:8px 16px;border-radius:4px;cursor:pointer;font-weight:600;font-size:0.85rem;">Tout accepter</button>
</div>
</div>
<div id="economya-cmp-categories" style="display:none;margin-top:14px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.2);">
<label style="display:flex;align-items:center;gap:8px;margin-bottom:10px;font-size:0.85rem;cursor:default;">
<input type="checkbox" checked disabled style="width:16px;height:16px;">
Cookies essentiels (toujours actifs — fonctionnement du site)
</label>
<label style="display:flex;align-items:center;gap:8px;margin-bottom:10px;font-size:0.85rem;cursor:pointer;">
<input type="checkbox" id="economya-cat-analytics" style="width:16px;height:16px;cursor:pointer;">
Mesure d'audience (Google Analytics)
</label>
<label style="display:flex;align-items:center;gap:8px;margin-bottom:14px;font-size:0.85rem;cursor:pointer;">
<input type="checkbox" id="economya-cat-publicite" style="width:16px;height:16px;cursor:pointer;">
Publicité personnalisée (Google AdSense)
</label>
<button id="economya-cmp-valider" style="background:#EF9F27;border:none;color:#2C2C2A;padding:8px 16px;border-radius:4px;cursor:pointer;font-weight:600;font-size:0.85rem;">Valider mes choix</button>
</div>
</div>
</div>
<script>
(function(){
var K = "economya_cookie_consent_v2";
var D = 180;

function getC(){
  try{
    var r = localStorage.getItem(K);
    if(!r) return null;
    var d = JSON.parse(r);
    var e = new Date(d.timestamp);
    e.setDate(e.getDate() + D);
    if(new Date() > e) return null;
    return d;
  }catch(e){ return null; }
}

function setC(analytics, publicite){
  try{
    localStorage.setItem(K, JSON.stringify({
      analytics: analytics,
      publicite: publicite,
      timestamp: new Date().toISOString()
    }));
  }catch(e){}
}

function applyConsent(analytics, publicite){
  if(typeof window.gtag === "function"){
    window.gtag('consent', 'update', {
      'analytics_storage': analytics ? 'granted' : 'denied',
      'ad_storage': publicite ? 'granted' : 'denied',
      'ad_user_data': publicite ? 'granted' : 'denied',
      'ad_personalization': publicite ? 'granted' : 'denied'
    });
  }
  if(analytics && typeof window.economyaLoadGA === "function"){
    window.economyaLoadGA();
  }
  if(publicite && typeof window.economyaLoadAds === "function"){
    window.economyaLoadAds();
  }
}

var banner = document.getElementById("economya-cookie-banner");
var existing = getC();

if(existing){
  applyConsent(existing.analytics, existing.publicite);
}else if(banner){
  banner.style.display = "block";
}

var btnAccept = document.getElementById("economya-cookie-accept");
var btnRefuse = document.getElementById("economya-cookie-refuse");
var btnPersonnaliser = document.getElementById("economya-cmp-personnaliser");
var btnValider = document.getElementById("economya-cmp-valider");
var divCategories = document.getElementById("economya-cmp-categories");
var divSimple = document.getElementById("economya-cmp-simple");
var checkAnalytics = document.getElementById("economya-cat-analytics");
var checkPublicite = document.getElementById("economya-cat-publicite");

if(btnAccept){
  btnAccept.addEventListener("click", function(){
    setC(true, true);
    applyConsent(true, true);
    banner.style.display = "none";
  });
}
if(btnRefuse){
  btnRefuse.addEventListener("click", function(){
    setC(false, false);
    applyConsent(false, false);
    banner.style.display = "none";
  });
}
if(btnPersonnaliser){
  btnPersonnaliser.addEventListener("click", function(){
    divCategories.style.display = "block";
    divSimple.style.display = "none";
  });
}
if(btnValider){
  btnValider.addEventListener("click", function(){
    var a = checkAnalytics ? checkAnalytics.checked : false;
    var p = checkPublicite ? checkPublicite.checked : false;
    setC(a, p);
    applyConsent(a, p);
    banner.style.display = "none";
  });
}
})();
</script>
'''


def traiter_fichier(chemin):
    if not os.path.exists(chemin):
        return "introuvable"

    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "economya_cookie_consent_v2" in contenu:
        return "déjà à jour"

    if 'id="economya-cookie-banner"' not in contenu:
        return "pas de bandeau (ignoré)"

    contenu_original = contenu

    # 1. Consent Mode v2 default
    if ANCIEN_DATALAYER_INIT in contenu and "gtag('consent', 'default'" not in contenu:
        contenu = contenu.replace(ANCIEN_DATALAYER_INIT, NOUVEAU_DATALAYER_INIT, 1)

    # 2. Remplacement du bandeau
    if not ANCIEN_BANNER_BLOC_PATTERN.search(contenu):
        return "bandeau non reconnu (structure differente)"

    contenu = ANCIEN_BANNER_BLOC_PATTERN.sub(NOUVEAU_BANNER_BLOC, contenu, count=1)

    if contenu == contenu_original:
        return "aucun changement"

    with open(chemin + ".bak_cmp", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu)

    return "mis a jour"


def main():
    fichiers = sorted(glob.glob("*.html")) + sorted(glob.glob("article-*.html"))
    fichiers = sorted(set(fichiers))

    resultats = {}
    for fichier in fichiers:
        statut = traiter_fichier(fichier)
        resultats[statut] = resultats.get(statut, 0) + 1

    print("=== RÉSUMÉ ===")
    for statut, count in resultats.items():
        print(f"{statut} : {count}")


if __name__ == "__main__":
    main()
