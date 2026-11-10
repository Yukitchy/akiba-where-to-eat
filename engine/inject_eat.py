"""eat 本体(~/where-to-eat/akihabara/index.html)に言語ボタンと辞書を差し込む（何度実行しても同じ結果）。"""
import re,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
import lang,mapbg,switch
P=pathlib.Path('/Users/yuki/where-to-eat/akihabara/index.html')
t=P.read_text(encoding='utf-8')
t=re.sub(r'<style id="langcss">.*?</style>','',t,flags=re.S)
t=re.sub(r'<style id="tightcss">.*?</style>','',t,flags=re.S)
t=re.sub(r'<script id="langjs">.*?</script>','',t,flags=re.S)
t=re.sub(r'<script id="pinzoomjs">.*?</script>','',t,flags=re.S)
t=re.sub(r'<details class="langsw">.*?</details>','{{LANGBTN}}',t,flags=re.S)
t=re.sub(r'<button type="button" class="langsw".*?</button>','{{LANGBTN}}',t,flags=re.S)
t=re.sub(r'<span>TOKYO · \d+ PLACES</span>','{{LANGBTN}}',t)
assert '{{LANGBTN}}' in t
# 地図の背景を黄×黒の絵地図に（駅4点の位置から投影を合わせてある。ピン・引き出し線(<g data-k)はそのまま）
_f,_sc=mapbg.affine(23130.85,-3232681.39,-32262.40,1151948.68)
_st=[('AKIHABARA',35.69838,139.77313),('SUEHIROCHO',35.7022,139.7716),('KANDA',35.69169,139.77088),('OCHANOMIZU',35.69962,139.7653)]
_m=re.search(r'(<svg id="map"[^>]*>).*?(?=<g data-k=)',t,flags=re.S)
assert _m
t=t[:_m.end(1)]+mapbg.bg(_f,_sc,_st)+t[_m.end():]
t=t.replace('{{LANGBTN}}',lang.button())
keys=set(json.loads((lang.R/'packs'/'i18nkeys_eat.json').read_text(encoding='utf-8')))
t=t.replace('</head>','<style id="langcss">'+lang.CSS+'</style><style id="tightcss">'+switch.TIGHT+'</style></head>',1)
t=t.replace('</body>','<script id="langjs">'+lang.js(keys)+'</script></body>',1)
ph={}
for m in re.finditer(r'<article class="card[^"]*" id="p(\d+)".*?</article>',t,flags=re.S):
    u=re.search(r'<img src="([^"]+)"[^>]*data-l="Dish"',m.group(0))
    if u: ph[int(m.group(1))]=u.group(1)
t=t.replace('</body>','<script id="pinzoomjs">window.__PH='+json.dumps(ph)+';\n'+(lang.R/'engine'/'pinzoom.js').read_text(encoding='utf-8')+'</script></body>',1)
print('eat photos',len(ph))
P.write_text(t,encoding='utf-8');print('ok',len(t))
