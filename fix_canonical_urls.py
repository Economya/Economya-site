#!/usr/bin/env python3
"""
Corrige les URLs déclarées dans les balises canonical, og:url, twitter:url
et JSON-LD ("url" et "mainEntityOfPage") pour qu'elles pointent vers la
version SANS .html — cohérente avec ce que le site sert et lie réellement
partout (menus, navigation, fils d'Ariane).

Avant : <link rel="canonical" href="https://economya.fr/article-1.html">
Après : <link rel="canonical" href="https://economya.fr/article-1">

Ne touche à AUCUN autre lien du contenu (les liens internes .html dans le
corps de la page ne sont pas modifiés par ce script — c'est volontaire,
ils fonctionneront quand même une fois la redirection Netlify en place).

- Fait une sauvegarde .bak_canonical de chaque fichier modifié
- Idempotent : relancer sur des fichiers déjà corrigés ne change rien
"""
import re
import glob
import sys

# Ne cible que : www.economya.fr ou economya.fr, suivi d'un chemin se
# terminant par .html, à l'intérieur des attributs canonical/og:url/twitter:url
# et des champs "url"/"mainEntityOfPage" du JSON-LD.
URL_PATTERN = re.compile(
    r'(https?://(?:www\.)?economya\.fr/[^"\s]*?)\.html\b'
)

TARGET_CONTEXT_PATTERNS = [
    re.compile(r'(<link\s+rel=["\']canonical["\']\s+href=")([^"]+)(")'),
    re.compile(r'(<meta\s+property=["\']og:url["\']\s+content=")([^"]+)(")'),
    re.compile(r'(<meta\s+name=["\']twitter:url["\']\s+content=")([^"]+)(")'),
    re.compile(r'("url"\s*:\s*")([^"]+)(")'),
    re.compile(r'("mainEntityOfPage"\s*:\s*")([^"]+)(")'),
]

def strip_html_extension(url):
    return URL_PATTERN.sub(r'\1', url)

def process_file(path):
    with open(path, encoding='utf-8') as f:
        original = f.read()

    content = original
    for pattern in TARGET_CONTEXT_PATTERNS:
        def repl(m):
            prefix, url, suffix = m.groups()
            return prefix + strip_html_extension(url) + suffix
        content = pattern.sub(repl, content)

    if content != original:
        backup_path = path + '.bak_canonical'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = sorted(glob.glob('*.html'))
    if not files:
        print("Aucun fichier .html trouvé dans ce dossier.")
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
        print("Exemples de fichiers modifiés :")
        for m in modified[:20]:
            print(f"  - {m}")
        if len(modified) > 20:
            print(f"  ... et {len(modified)-20} autres.")
        print("\nUne sauvegarde .bak_canonical a été créée pour chaque fichier modifié.")

if __name__ == '__main__':
    main()
