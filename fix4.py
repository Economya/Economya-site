import os

css = "@media(max-width:768px){.hamburger{display:flex}nav .nav-links,nav>a:not(.logo){display:none}nav ul{display:none}}"

count = 0
for f in os.listdir('.'):
    if not f.endswith('.html') or f == 'index.html':
        continue
    content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    if '@media(max-width:768px){.hamburger{display:flex}nav .nav-links' not in content:
        content = content.replace('@media(max-width:768px){.hamburger{display:flex}nav ul{display:none}}', css)
        open(f, 'w', encoding='utf-8').write(content)
        count += 1

print(str(count) + ' fichiers corriges')