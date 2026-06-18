open('index.html','w').write(open('index.html','r').read().replace('&lt;','<').replace('&gt;','>').replace('&quot;','"'))
print('done')

