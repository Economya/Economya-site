import glob

fichiers = glob.glob('article-*.html')
count = 0
examples = []
for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if 'URL_PAGE' in c or 'TITRE_PAGE' in c:
        count += 1
        examples.append(f)
print(f'{count} articles avec URL_PAGE/TITRE_PAGE non remplace')
print(examples[:10])
