c = open('article-52.html', encoding='utf-8').read()

print("=== HEADER ===")
idx_hero = c.find('class="hero')
if idx_hero == -1:
    idx_hero = c.find('class="ah')
print(c[max(0,idx_hero-20):idx_hero+600])

print()
print("=== FOOTER ===")
idx_footer = c.find('<footer')
print(c[idx_footer:idx_footer+700])
