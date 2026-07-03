import re
c = open('article-123.html', encoding='utf-8').read()
style_idx = c.find('<style')
style_end = c.find('</style>')
style_content = c[style_idx:style_end]

m = re.search(r'footer\s*\{[^}]*\}', style_content)
print("Regle CSS footer trouvee:", m.group() if m else "AUCUNE REGLE FOOTER DANS LE STYLE")

# verifier aussi si le footer a un style en ligne
idx_footer = c.find('<footer')
print()
print("Balise footer telle qu'ecrite dans le HTML:")
print(repr(c[idx_footer:idx_footer+60]))
