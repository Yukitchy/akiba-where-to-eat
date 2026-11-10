"""言語切り替え（EN主・ja/zh/es/de/ko）。ページ内の英語テキストを辞書(packs/i18n.json)で差し替える。
drink/buy は build.py から、eat は engine/inject_eat.py から差し込む。"""
import json,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
LANGS=[('en','English'),('ja','日本語'),('zh','中文'),('es','Español'),('de','Deutsch'),('ko','한국어')]
GLOBE='<svg class="gl" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>'
CHEV='<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8l8 8 8-8" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FLAGS={
'en':'<svg viewBox="0 0 24 16"><rect width="24" height="16" fill="#fff"/><rect y="0.00" width="24" height="1.23" fill="#B22234"/><rect y="2.46" width="24" height="1.23" fill="#B22234"/><rect y="4.92" width="24" height="1.23" fill="#B22234"/><rect y="7.38" width="24" height="1.23" fill="#B22234"/><rect y="9.85" width="24" height="1.23" fill="#B22234"/><rect y="12.31" width="24" height="1.23" fill="#B22234"/><rect y="14.77" width="24" height="1.23" fill="#B22234"/><rect width="10" height="8.6" fill="#3C3B6E"/></svg>',
'ja':'<svg viewBox="0 0 24 16"><rect width="24" height="16" fill="#fff"/><circle cx="12" cy="8" r="4.6" fill="#BC002D"/></svg>',
'zh':'<svg viewBox="0 0 24 16"><rect width="24" height="16" fill="#DE2910"/><polygon points="5,2.2 5.9,4.9 8.7,4.9 6.4,6.5 7.3,9.2 5,7.5 2.7,9.2 3.6,6.5 1.3,4.9 4.1,4.9" fill="#FFDE00"/></svg>',
'es':'<svg viewBox="0 0 24 16"><rect width="24" height="16" fill="#AA151B"/><rect y="4" width="24" height="8" fill="#F1BF00"/></svg>',
'de':'<svg viewBox="0 0 24 16"><rect width="24" height="16" fill="#FFCE00"/><rect width="24" height="5.34" fill="#000"/><rect y="5.33" width="24" height="5.34" fill="#DD0000"/></svg>',
'ko':'<svg viewBox="0 0 24 16"><rect width="24" height="16" fill="#fff"/><circle cx="12" cy="8" r="3.6" fill="#CD2E3A"/><path d="M8.4 8a3.6 3.6 0 0 0 7.2 0a1.8 1.8 0 0 0-3.6 0a1.8 1.8 0 0 1-3.6 0z" fill="#0047A0"/><g stroke="#000" stroke-width="1"><path d="M3 3.3l2.6-1.6M3.6 4.5l2.6-1.6M3 5.7l2.6-1.6"/><path d="M18.4 12.6l2.6-1.6M17.8 13.8l2.6-1.6M18.4 14.5l2.6-1.6" opacity=".0"/></g></svg>',
}
def button():
    fl=''.join(v.replace('<svg ',f'<svg class="f{" on" if k=="en" else ""}" data-l="{k}" aria-hidden="true" ',1) for k,v in FLAGS.items())
    return f'<button type="button" class="langsw" aria-label="Change language"><span class="fl">{fl}</span><b class="lc">EN</b></button>'
CSS='''.langsw{margin-left:auto;align-self:flex-end;margin-bottom:4px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;border:0;padding:8px 11px;font:900 15px/1 Archivo,sans-serif;letter-spacing:.08em;color:var(--ls-t,#fff);background:var(--ac,#1F8A4C);-webkit-tap-highlight-color:transparent}.langsw:active{filter:brightness(.88)}.langsw .fl{display:block;width:24px;height:16px;flex:none;box-shadow:0 0 0 1px rgba(0,0,0,.25)}.langsw .fl svg{display:none;width:24px;height:16px}.langsw .fl svg.on{display:block}.langsw .lc{display:block;min-width:1.6em;text-align:left}
'''
def js(keys):
    T=json.loads((R/'packs'/'i18n.json').read_text(encoding='utf-8'))
    sub={k:v for k,v in T.items() if keys is None or k in keys}
    return 'window.__T='+json.dumps(sub,ensure_ascii=False,separators=(',',':'))+';\n'+(R/'engine'/'lang.js').read_text(encoding='utf-8')
