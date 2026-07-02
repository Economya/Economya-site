#!/usr/bin/env python3
"""
Corrige 2 problemes sur les boutons de partage des articles Economya.fr :

1. 455 articles ont un bloc de partage avec des placeholders litteraux
   "URL_PAGE" et "TITRE_PAGE" jamais remplaces -> les boutons Facebook,
   Twitter, LinkedIn, WhatsApp, Pinterest sont casses (pointent vers un
   lien invalide au lieu du vrai article).

2. 74 articles n'ont AUCUN bloc de partage -> on en ajoute un, complet,
   avec les bonnes valeurs directement (pas de placeholder).

Le vrai titre de chaque article est extrait de sa balise <title>
(tout ce qui precede " — Economya.fr"). L'URL reelle est reconstruite
depuis le nom de fichier : https://economya.fr/{fichier}

Idempotent. Sauvegardes .bak_partage avant modification.
"""

import glob
import re
import shutil
from urllib.parse import quote

SITE = "https://economya.fr"

BLOC_PARTAGE_TEMPLATE = '''
<!-- Boutons partage -->
<div style="background:#fff;border-radius:16px;border:1px solid rgba(0,0,0,0.08);padding:1.2rem 1.5rem;margin:2rem auto;max-width:680px;text-align:center">
  <p style="font-size:.82rem;font-weight:600;color:#5F5E5A;margin-bottom:.8rem;text-transform:uppercase;letter-spacing:.05em">Partager cet article</p>
  <div style="display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap">
    <a href="https://www.facebook.com/sharer/sharer.php?u={url}" target="_blank" rel="noopener" style="background:#1877F2;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">📘 Facebook</a>
    <a href="https://twitter.com/intent/tweet?url={url}&text={titre}" target="_blank" rel="noopener" style="background:#000;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">𝕏 Twitter</a>
    <a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener" style="background:#0A66C2;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">💼 LinkedIn</a>
    <a href="whatsapp://send?text={titre}%20-%20{url}" target="_blank" rel="noopener" style="background:#25D366;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">💬 WhatsApp</a>
    <a href="https://pinterest.com/pin/create/button/?url={url}&description={titre}" target="_blank" rel="noopener" style="background:#E60023;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">📌 Pinterest</a>
  </div>
</div>
'''


def get_title(contenu):
    m = re.search(r'<title>(.*?)</title>', contenu, re.DOTALL)
    if not m:
        return "Economya.fr"
    titre = m.group(1)
    titre = re.sub(r'\s*—\s*Economya\.fr\s*$', '', titre).strip()
    return titre


def main():
    fichiers = sorted(glob.glob('article-*.html'))
    total_placeholders = 0
    total_ajouts = 0
    total_rien = 0

    for f in fichiers:
        with open(f, 'r', encoding='utf-8') as fh:
            contenu = fh.read()

        titre_reel = get_title(contenu)
        url_reelle = f"{SITE}/{f}"
        url_encoded = quote(url_reelle, safe=':/')
        titre_encoded = quote(titre_reel)

        modifie = False
        contenu_new = contenu

        if 'URL_PAGE' in contenu_new or 'TITRE_PAGE' in contenu_new:
            contenu_new = contenu_new.replace('URL_PAGE', url_encoded)
            contenu_new = contenu_new.replace('TITRE_PAGE', titre_encoded)
            modifie = True
            total_placeholders += 1

        elif 'Partager cet article' not in contenu_new:
            bloc = BLOC_PARTAGE_TEMPLATE.format(url=url_encoded, titre=titre_encoded)
            if '<footer>' in contenu_new:
                contenu_new = contenu_new.replace('<footer>', bloc + '\n<footer>', 1)
                modifie = True
                total_ajouts += 1
            else:
                print(f"  ATTENTION {f}: pas de <footer> trouve, bloc non ajoute")

        else:
            total_rien += 1

        if modifie:
            shutil.copy2(f, f + '.bak_partage')
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(contenu_new)

    print(f"Placeholders corriges : {total_placeholders}")
    print(f"Blocs de partage ajoutes : {total_ajouts}")
    print(f"Deja bons, rien fait : {total_rien}")
    print(f"Total traite : {len(fichiers)}")


if __name__ == '__main__':
    main()
