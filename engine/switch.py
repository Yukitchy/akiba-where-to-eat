"""h1 の「EAT / DRINK / BUY」をタップで切り替えるドロップダウン（where to eat の AKIHABARA エリア切替と同じ作り）。
eat 本体(~/where-to-eat/akihabara)・drink・buy に同じ部品を差し込む。"""
URL={'eat':'https://yukitchy.github.io/where-to-eat/akihabara/','drink':'https://yukitchy.github.io/akiba-where-to-eat/drink/','buy':'https://yukitchy.github.io/akiba-where-to-eat/buy/'}
LAB={'eat':'Eat','drink':'Drink','buy':'Buy'}
CHEV='<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8l8 8 8-8" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CSS='''.kindsw{display:inline-block;position:relative}.kindsw summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:.08em;color:var(--ac,var(--red));text-decoration:underline;text-decoration-thickness:.06em;text-underline-offset:.1em}.kindsw summary::-webkit-details-marker{display:none}
.kindsw .chev{width:.3em;height:.3em;margin-left:.04em}.kindsw[open] .chev{transform:rotate(180deg)}.kindsw ul{list-style:none;margin:6px 0 0;padding:6px 0;background:var(--ink);position:absolute;left:0;top:100%;z-index:6;min-width:min(78vw,240px);text-transform:uppercase}.kindsw li a{display:block;padding:12px 18px;color:#fff;text-decoration:none;font:900 .55em/1 Archivo,sans-serif;font-stretch:62%;letter-spacing:.02em}.kindsw li a:hover,.kindsw li a:focus{background:var(--ac,var(--red))}.kindsw li a i{font-style:normal;margin-left:.4em;opacity:.7}.kindsw li a[aria-current]{opacity:.55;pointer-events:none}
.top{align-items:flex-end}.klg{display:flex;align-items:flex-end;width:190px;min-height:39.5px;padding-bottom:4px;margin-top:8px}.klg img{display:block;width:100%;height:auto;mix-blend-mode:multiply}
'''
JS='''(function(){var k=document.querySelector('details.kindsw');if(!k)return;document.addEventListener('click',function(e){if(k.open&&!e.target.closest('details.kindsw'))k.open=false});var a=document.querySelector('details.areasw');if(a){k.addEventListener('toggle',function(){if(k.open)a.open=false});a.addEventListener('toggle',function(){if(a.open)k.open=false})}})();'''
def dropdown(cur):
    li=''.join(f'<li><a href="{URL[k]}"{" aria-current=page" if k==cur else ""}>{LAB[k]} {"" if k==cur else "<i>&rarr;</i>"}</a></li>' for k in ('eat','drink','buy'))
    return f'<details class="kindsw"><summary>{LAB[cur]}{CHEV}</summary><ul>{li}</ul></details>'
def logo(cur,up):
    return f'<a class="klg" href="{URL[cur]}" aria-label="{LAB[cur].upper()}MAP"><img src="{up}brand/logo-{cur}-1line.png" alt="{LAB[cur].upper()}MAP" width="190"></a>'
