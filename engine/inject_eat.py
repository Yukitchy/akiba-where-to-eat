"""eat 本体(~/where-to-eat/akihabara/index.html)に言語ボタンと辞書を差し込む（何度実行しても同じ結果）。"""
import re,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
import lang
P=pathlib.Path('/Users/yuki/where-to-eat/akihabara/index.html')
t=P.read_text(encoding='utf-8')
t=re.sub(r'<style id="langcss">.*?</style>','',t,flags=re.S)
t=re.sub(r'<script id="langjs">.*?</script>','',t,flags=re.S)
t=re.sub(r'<details class="langsw">.*?</details>','{{LANGBTN}}',t,flags=re.S)
t=re.sub(r'<button type="button" class="langsw".*?</button>','{{LANGBTN}}',t,flags=re.S)
t=re.sub(r'<span>TOKYO · \d+ PLACES</span>','{{LANGBTN}}',t)
assert '{{LANGBTN}}' in t
t=t.replace('{{LANGBTN}}',lang.button())
keys=set(json.loads((lang.R/'packs'/'i18nkeys_eat.json').read_text(encoding='utf-8')))
t=t.replace('</head>','<style id="langcss">'+lang.CSS+'</style></head>',1)
t=t.replace('</body>','<script id="langjs">'+lang.js(keys)+'</script></body>',1)
P.write_text(t,encoding='utf-8');print('ok',len(t))
