import glob, re

# on cherche un article qui a "article-nav" DEFINI dans son <style> (pas juste utilise dans le body)
for f in sorted(glob.glob('article-*.html')):
    c = open(f, encoding='utf-8').read()
    if '.article-nav' in c and 'data-nav-styled' not in c:
        # verifier que c'est bien dans une balise <style>
        style_idx = c.find('<style')
        style_end = c.find('</style>')
        if style_idx != -1 and style_end != -1:
            style_content = c[style_idx:style_end]
            if '.article-nav' in style_content or '.art-nav-btn' in style_content:
                print(f"=== CSS trouve dans : {f} ===")
                # afficher les regles pertinentes
                for motif in ['.article-nav', '.art-nav-btn', '.nav-label', '.nav-title']:
                    m = re.search(re.escape(motif) + r'\s*\{[^}]*\}', style_content)
                    if m:
                        print(m.group())
                print()
                print("=== Utilisation dans le body ===")
                idx = c.find('class="article-nav"')
                print(c[max(0,idx-20):idx+500])
                break
else:
    print("Aucun CSS .article-nav trouve dans les balises <style> d'aucun article")
