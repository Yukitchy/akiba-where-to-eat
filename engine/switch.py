"""EAT / DRINK / BUY の切り替えバー＋ロゴ。build.py と eat 本体(index.html)の両方に差し込む。"""
KINDS=[('eat','EAT','D9342B','fff',''),('drink','DRINK','F4B223','121212','drink/'),('buy','BUY','2F6FDB','fff','buy/')]
LOGO={'eat':'EATMAP','drink':'DRINKMAP','buy':'BUYMAP'}
CSS='''.klogo{display:block;margin:14px auto 0;width:min(70%,300px)}.klogo img{display:block;width:100%;height:auto;mix-blend-mode:multiply}
.kinds{display:flex;margin:14px 0 0;border:3px solid #121212;background:#fff}.kinds a{flex:1;text-align:center;padding:13px 0 12px;font:900 15px/1 Archivo,sans-serif;letter-spacing:.14em;color:#121212;text-decoration:none;border-left:3px solid #121212}.kinds a:first-child{border-left:0}
.kinds a.on{background:var(--c);color:var(--t);pointer-events:none}.kinds a:not(.on):hover,.kinds a:not(.on):focus-visible{background:#121212;color:#fff}
'''
def html(cur,up):
    """cur=今のページ種別 / up='' (eat本体) か '../' (drink,buy)"""
    tabs=''.join(f'<a href="{up}{path}" style="--c:#{c};--t:#{t}"{" class=on aria-current=page" if k==cur else ""}>{lab}</a>' for k,lab,c,t,path in KINDS)
    return f'<a class="klogo" href="{up or "./"}{dict((k,p) for k,_,_,_,p in KINDS)[cur]}"><img src="{up}brand/logo-{cur}.png" alt="{LOGO[cur]}" width="300"></a><nav class="kinds" aria-label="Guides">{tabs}</nav>'
