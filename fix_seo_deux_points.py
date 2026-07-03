import os, shutil

# 1. Corriger le robots.txt (retirer le www pour matcher le reste du site)
print("=== Correction robots.txt ===")
if os.path.exists('robots.txt'):
    c = open('robots.txt', encoding='utf-8').read()
    ancien = 'https://www.economya.fr/sitemap.xml'
    nouveau = 'https://economya.fr/sitemap.xml'
    if nouveau in c and ancien not in c:
        print("Deja corrige (idempotent).")
    elif ancien in c:
        c_new = c.replace(ancien, nouveau, 1)
        shutil.copy2('robots.txt', 'robots.txt.bak_www')
        open('robots.txt', 'w', encoding='utf-8').write(c_new)
        print("OK : www retire du robots.txt")
    else:
        print("Chaine non trouvee, verifier manuellement")
else:
    print("robots.txt introuvable")

print()

# 2. Supprimer les 2 fichiers de test
print("=== Suppression des fichiers de test ===")
for f in ['article-218-test.html', 'article-484-test.html']:
    if os.path.exists(f):
        os.remove(f)
        print(f"Supprime : {f}")
    else:
        print(f"Deja absent : {f}")
