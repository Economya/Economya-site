#!/usr/bin/env python3
"""
Corrige les liens de partage (Twitter/X, WhatsApp, Pinterest) dont le paramètre
text= ou description= contient un caractère "/" non encodé (ex: "150€/mois").
Ce "/" brut fait croire à certains outils qu'il s'agit d'un chemin d'URL,
ce qui génère des pages fantômes en 404 dans Google Search Console
(economya.fr/mois, economya.fr/litre, economya.fr/5, economya.fr/10...).

Le script :
- Cherche les <a href="..."> de partage Twitter/X, WhatsApp, Pinterest
- Repère uniquement la portion text=... ou description=... de l'URL
- Remplace les "/" bruts dans CETTE portion par %2F (encodage correct)
- Ne touche à RIEN d'autre (le lien réel vers l'article n'est jamais modifié)
- Fait une sauvegarde .bak_shareencode de chaque fichier modifié
- Est idempotent : relancer le script sur des fichiers déjà corrigés ne change rien
"""
import re
import glob
import sys

# Repère le bloc text=... ou description=... jusqu'à sa fin naturelle :
# - pour WhatsApp : s'arrête avant " - https://..."
# - pour Twitter/Pinterest : s'arrête à la fin de l'attribut href (avant le ")
PARAM_PATTERN = re.compile(
    r'((?:text|description)=)(.*?)((?:\s-\shttps?://|"))'
)

def fix_param_value(match):
    prefix, value, suffix = match.groups()
    if '/' in value:
        value = value.replace('/', '%2F')
    return prefix + value + suffix

def process_file(path):
    with open(path, encoding='utf-8') as f:
        original = f.read()

    fixed = PARAM_PATTERN.sub(fix_param_value, original)

    if fixed != original:
        backup_path = path + '.bak_shareencode'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        return True
    return False

def main():
    files = sorted(glob.glob('article-*.html'))
    if not files:
        print("Aucun fichier article-*.html trouvé dans ce dossier.")
        sys.exit(1)

    modified = []
    for path in files:
        try:
            if process_file(path):
                modified.append(path)
        except Exception as e:
            print(f"⚠️  Erreur sur {path} : {e}")

    print(f"\n{len(modified)} fichier(s) corrigé(s) sur {len(files)} analysé(s).")
    if modified:
        print("Fichiers modifiés :")
        for m in modified[:30]:
            print(f"  - {m}")
        if len(modified) > 30:
            print(f"  ... et {len(modified)-30} autres.")
        print("\nUne sauvegarde .bak_shareencode a été créée pour chaque fichier modifié.")

if __name__ == '__main__':
    main()
