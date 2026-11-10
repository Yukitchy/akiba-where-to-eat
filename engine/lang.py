"""言語切り替え（EN主・ja/zh/es/de/ko）。ページ内の英語テキストを辞書(packs/i18n.json)で差し替える。
drink/buy は build.py から、eat は engine/inject_eat.py から差し込む。"""
import json,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
LANGS=[('en','English'),('ja','日本語'),('zh','中文'),('es','Español'),('de','Deutsch'),('ko','한국어')]
GLOBE='<svg class="gl" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>'
CHEV='<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8l8 8 8-8" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def button():
    return f'<button type="button" class="langsw" aria-label="Change language">{GLOBE}<b class="lc">EN</b></button>'
CSS='''.langsw{margin-left:auto;align-self:flex-end;margin-bottom:4px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;border:3px solid var(--ink);padding:8px 11px;font:900 15px/1 Archivo,sans-serif;letter-spacing:.08em;color:var(--ink);background:transparent;-webkit-tap-highlight-color:transparent}.langsw:active{background:var(--ink);color:#fff}.langsw .gl{width:19px;height:19px}.langsw .lc{display:block;min-width:1.6em;text-align:left}
'''
def js(keys):
    T=json.loads((R/'packs'/'i18n.json').read_text(encoding='utf-8'))
    sub={k:v for k,v in T.items() if keys is None or k in keys}
    return 'window.__T='+json.dumps(sub,ensure_ascii=False,separators=(',',':'))+';\n'+(R/'engine'/'lang.js').read_text(encoding='utf-8')
