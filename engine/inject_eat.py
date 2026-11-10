"""eat 本体(~/where-to-eat/akihabara/index.html)に言語ボタンと辞書を差し込む（何度実行しても同じ結果）。"""
import re,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
import lang
P=pathlib.Path('/Users/yuki/where-to-eat/akihabara/index.html')
t=P.read_text(encoding='utf-8')
t=re.sub(r'<style id="langcss">.*?</style>','',t,flags=re.S)
t=re.sub(r'<script id="langjs">.*?</script>','',t,flags=re.S)
t=re.sub(r'<script id="pinzoomjs">.*?</script>','',t,flags=re.S)
t=re.sub(r'<details class="langsw">.*?</details>','{{LANGBTN}}',t,flags=re.S)
t=re.sub(r'<button type="button" class="langsw".*?</button>','{{LANGBTN}}',t,flags=re.S)
t=re.sub(r'<span>TOKYO · \d+ PLACES</span>','{{LANGBTN}}',t)
assert '{{LANGBTN}}' in t
t=t.replace('{{LANGBTN}}',lang.button())
keys=set(json.loads((lang.R/'packs'/'i18nkeys_eat.json').read_text(encoding='utf-8')))
t=t.replace('</head>','<style id="langcss">'+lang.CSS+'</style></head>',1)
t=t.replace('</body>','<script id="langjs">'+lang.js(keys)+'</script></body>',1)
ph={}
for m in re.finditer(r'<article class="card[^"]*" id="p(\d+)".*?</article>',t,flags=re.S):
    u=re.search(r'<img src="([^"]+)"[^>]*data-l="Dish"',m.group(0))
    if u: ph[int(m.group(1))]=u.group(1)
t=t.replace('</body>','<script id="pinzoomjs">window.__PH='+json.dumps(ph)+';\n'+(lang.R/'engine'/'pinzoom.js').read_text(encoding='utf-8')+'</script></body>',1)
print('eat photos',len(ph))
P.write_text(t,encoding='utf-8');print('ok',len(t))
