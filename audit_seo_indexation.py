import os, glob, re

print("=== 1. SITEMAP.XML ===")
if os.path.exists('sitemap.xml'):
    c = open('sitemap.xml', encoding='utf-8').read()
    urls = re.findall(r'<loc>(.*?)</loc>', c)
    print(f"Sitemap trouve, {len(urls)} URLs listees")
    # verifier les doublons de test dans le sitemap
    test_urls = [u for u in urls if 'test' in u.lower()]
    print(f"URLs suspectes (contenant 'test') dans le sitemap : {test_urls}")
else:
    print("AUCUN sitemap.xml trouve a la racine !")

print()
print("=== 2. ROBOTS.TXT ===")
if os.path.exists('robots.txt'):
    c = open('robots.txt', encoding='utf-8').read()
    print(c)
else:
    print("AUCUN robots.txt trouve a la racine !")

print()
print("=== 3. FICHIERS DE TEST EN DOUBLE ===")
test_files = glob.glob('*-test.html')
print(f"{len(test_files)} fichiers de test trouves : {test_files}")

print()
print("=== 4. BALISES NOINDEX ACCIDENTELLES ===")
fichiers = glob.glob('article-*.html')
noindex_files = []
for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if 'noindex' in c.lower():
        noindex_files.append(f)
print(f"Articles avec 'noindex' quelque part : {len(noindex_files)}")
print(noindex_files[:20])

print()
print("=== 5. BALISES CANONICAL ===")
sans_canonical = []
for f in fichiers[:50]:  # echantillon rapide
    c = open(f, encoding='utf-8').read()
    if 'rel="canonical"' not in c:
        sans_canonical.append(f)
print(f"Sur un echantillon de 50 : {len(sans_canonical)} sans balise canonical")
print(sans_canonical[:10])
