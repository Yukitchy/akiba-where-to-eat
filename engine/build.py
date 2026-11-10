#!/usr/bin/env python3
"""packs/<kind>.json -> <kind>/index.html。where to eat 本体の CSS/JS(engine/eat.*)をそのまま使い、色・題・中身だけ差し替える。
使い方: python3 engine/build.py drink"""
import json,sys,pathlib,math,urllib.parse
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import switch,lang
R=pathlib.Path(__file__).resolve().parent.parent
q=urllib.parse.quote
CLOCK='<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 4.5V8l2.5 1.8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
WALK='<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><circle cx="9" cy="2.5" r="1.8" fill="currentColor"/><path d="M8.5 5.5 6 9l2.2 1.6V15M6 9 4 8l-1.5 3M8.2 10.6 11 12l1.5 3" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
GRID=''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="680" stroke="#fff" stroke-width="16"/>' for x in (70,205,340,470,560))+''.join(f'<line x1="0" y1="{y}" x2="600" y2="{y}" stroke="#fff" stroke-width="16"/>' for y in (70,200,330,470,600))
def esc(s): return s.replace('&','&amp;').replace('"','&quot;')
def project(p):
    pts=[(s['lat'],s['lng']) for s in p['places']]+[(a,b) for _,a,b in p['stations']]
    la0=sum(a for a,_ in pts)/len(pts); k=math.cos(math.radians(la0))*111320
    xy=lambda a,b:((b-139.77)*k,-(a-35.696)*111320)
    P=[xy(a,b) for a,b in pts]; xs=[x for x,_ in P]; ys=[y for _,y in P]
    sc=min((600-120)/(max(xs)-min(xs)),(680-140)/(max(ys)-min(ys)))
    ox=300-(max(xs)+min(xs))/2*sc; oy=340-(max(ys)+min(ys))/2*sc
    f=lambda a,b:(round(xy(a,b)[0]*sc+ox),round(xy(a,b)[1]*sc+oy))
    return f,sc
def svgmap(p):
    f,sc=project(p); pin=[list(f(s['lat'],s['lng'])) for s in p['places']]
    for _ in range(60):  # 近すぎるピンを少し離す（スケッチ地図なので見やすさ優先）
        for i in range(len(pin)):
            for j in range(i):
                dx,dy=pin[i][0]-pin[j][0],pin[i][1]-pin[j][1]; d=math.hypot(dx,dy) or .1
                if d<36: m=(36-d)/2; pin[i][0]+=dx/d*m; pin[i][1]+=dy/d*m; pin[j][0]-=dx/d*m; pin[j][1]-=dy/d*m
    o=f'<svg id="map" viewBox="0 0 600 680" role="img" aria-label="Simple sketch map of the {len(pin)} places"><rect width="600" height="680" fill="#F6F1E6"/>{GRID}'
    ax,ay=f(*p['stations'][0][1:])
    o+=f'<rect x="{ax-70}" y="{ay-18}" width="140" height="44" fill="#E4E0D6"/><circle cx="{ax}" cy="{ay}" r="{round(400*sc)}" fill="none" stroke="#121212" stroke-width="2" stroke-dasharray="7 6"/><text x="{ax}" y="{ay+2}" text-anchor="middle" font-size="14" font-weight="800" fill="#121212">AKIHABARA</text><text x="{ax}" y="{ay+19}" text-anchor="middle" font-size="14" font-weight="800" fill="#121212">STATION</text>'
    for n,a,b in p['stations'][1:]:
        x,y=f(a,b); o+=f'<circle cx="{x}" cy="{y}" r="7" fill="#121212"/><text x="{x+12}" y="{y+5}" font-size="14" font-weight="800" fill="#121212">{n}</text>'
    o+=f'<text x="12" y="668" text-anchor="start" font-size="13" font-weight="700" fill="#5D5A54">dashed circle: 400 m, about 5 min on foot</text>'
    for i,(s,(x,y)) in enumerate(zip(p['places'],pin),1):
        x,y=round(x),round(y); fill='#121212' if s['group']==p['g1']['name'] else 'var(--ac)'
        w=round(len(s['short'])*8.4+20); lx=min(max(x-w//2,4),596-w); ly=y-42 if y>50 else y+14
        o+=f'<a class="pin" href="#p{i}" data-n="{i}"><circle cx="{x}" cy="{y}" r="16" fill="{fill}" stroke="#fff" stroke-width="3"/><text x="{x}" y="{y+6}" text-anchor="middle" font-size="16" font-weight="900" fill="{'#121212' if (fill!='#121212' and p.get('ac_text')) else '#fff'}">{i}</text><g class="lbl"><rect x="{lx}" y="{ly}" width="{w}" height="28" fill="#121212"/><text x="{lx+w//2}" y="{ly+19}" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">{esc(s["short"])}</text></g></a>'
    return o+'</svg>'
def build(kind):
    p=json.loads((R/'packs'/f'{kind}.json').read_text(encoding='utf-8')); PL=p['places']
    for s in PL:
        assert s.get('addr') and s.get('jp') and s.get('src'),f"{s['id']}: addr/jp/src 必須（実在確認の出典）"
        s.setdefault('short',s['en'].title())
    css=(R/'engine'/'eat.css').read_text().replace('{{AC}}',p['ac']).replace('{{AC2}}',p['ac2'])
    css+=switch.CSS+switch.AREA_CSS+switch.CHIP_CSS+lang.CSS
    if p.get('ac_text'): css+='.langsw{--ls-t:#121212}\n'
    if p.get('ac_text'): css+=f'.areasw{{--ac-text:#{p["ac_text"]}}}h1{{--on-ac:#121212}}\n'
    if kind=='drink': css+='h1{font-size:clamp(38px,10.6vw,72px)}\n'  # DRINKは語が長く「IN」が落ちるので少しだけ小さく
    PHX=json.load(open(R/'packs'/'photos.json')) if (R/'packs'/'photos.json').exists() else {}
    want='Outside' if kind=='buy' else 'Drink'  # ピンのサムネ: DRINKは飲み物、BUYだけ店の写真
    pz={}
    for i,s in enumerate(p['places'],1):
        L=PHX.get(s['id']) or []
        u=next((x[0] for x in L if x[1]==want),None) or (L[0][0] if L else None)
        if u: pz[i]=u
    js='window.__PH='+json.dumps(pz)+';\n'+(R/'engine'/'eat.js').read_text()+switch.JS+switch.AREA_JS+(R/'engine'/'pinzoom.js').read_text()+lang.js(set(json.loads((R/'packs'/f'i18nkeys_{kind}.json').read_text(encoding='utf-8'))))
    if p.get('ac_text'):  # 明るい色のアクセント用: 文字色は濃い琥珀、色地の上の文字は黒
        css+=f'.nowlist,h1 em,.areasw small,.bar.r h2,.big,.lab{{color:#{p["ac_text"]}}}h1 em{{border-bottom-color:var(--ac)}}.vt,.tt,.genre,.btn.art,.card.r .strip,.tile.r .no{{color:#121212}}.card.r .genre{{color:#fff}}.pin circle{{}}\n'
    OPEN={s['id']:s['hours'] for s in PL if s['hours']}; SHORT={s['id']:s['short'] for s in PL}
    PH=json.load(open(R/'packs'/'photos.json')) if (R/'packs'/'photos.json').exists() else {}; MN=json.load(open(R/'packs'/'menu.json')) if (R/'packs'/'menu.json').exists() else {}
    def car(i):
        u=PH.get(i) or []
        if len(u)<2: return ''
        im=''.join(f'<img src="{x[0]}" alt="" loading="{"eager" if k==0 else "lazy"}" referrerpolicy="no-referrer" draggable="false" data-l="{x[1]}">' for k,x in enumerate(u))
        return f'<div class="car"><div class="trk">{im}</div><button type="button" class="cb pv" aria-label="Previous photo">&lsaquo;</button><button type="button" class="cb nx" aria-label="Next photo">&rsaquo;</button><span class="cn"><b>{u[0][1]}</b> 1/{len(u)}</span></div>'
    def mnp(s):
        u=MN.get(s['id']) or []; t=s['src'].rstrip('/')+'/dtlmenu/'
        if not u: return '',''
        im=''.join(f'<a href="{x}" target="_blank" rel="noopener"><img src="{x}" alt="Menu" loading="lazy" referrerpolicy="no-referrer"></a>' for x in u)
        return f'<div class="mn" hidden><div class="mg">{im}</div><p class="mc">Menu photos from Tabelog. Tap a photo to enlarge.</p><a class="btn mt" href="{t}" rel="noopener">Full menu on Tabelog <i>&rarr;</i></a></div>','<button class="btn tg" type="button" aria-expanded="false">Show menu</button>'
    HID=[('hitachino-lab',1,'hitachino-lab'),('ibrew',0,'ibrew'),('malt-road',1,'malt-road')] if kind=='drink' else []
    pn={x['id']:i for i,x in enumerate(PL,1)}
    HEROIMG=''.join(f'<a href="#p{pn[h]}" aria-label="Go to this place"><img src="{PH[h][k][0]}" alt="" referrerpolicy="no-referrer"></a>' for h,k,_ in HID)
    cls=lambda s:'' if s['group']==p['g1']['name'] else 'r'
    tiles={g:'' for g in (p['g1']['name'],p['g2']['name'])}; cards=''
    for i,s in enumerate(PL,1):
        c=cls(s); n=f'{i:02d}'
        tiles[s['group']]+=f'<a class="tile {c}" href="#p{i}" data-id="{s["id"]}">{(f'<img src="{PH[s["id"]][0][0]}" alt="" loading="lazy" referrerpolicy="no-referrer">' if PH.get(s["id"]) else f'<span class="tj">{s["en"] if kind in("buy","drink") else s["tile"]}</span>')}<b class="no">{n}</b><span class="tt">{s["genre"]}</span><span class="tn">{s["en"]}</span></a>'
        cards+=f'''<article class="card {c}" id="p{i}" data-id="{s["id"]}">
<div class="hd"><span class="big">{n}</span><div><span class="genre">{s["genre"]}</span><h3>{s["en"]}</h3></div></div>
{car(s["id"])}
{"" if kind in("buy","drink") else f'<p class="jp" lang="ja">{s["jp"]}</p>'}
<p class="tx">{s["note"]}</p>
<p class="strip" data-id="{s["id"]}"><span class="hr">{CLOCK}<b class="today">{s["txt"]}</b></span><span class="wk">{WALK}{s["walk"]} min walk</span></p>
<p class="hrs">{s["txt"]}. Closed: {s["closed"]}. {s["area"]}</p>
<p class="hrs"><b>Pay:</b> {s["pay"]}</p>
{mnp(s)[0]}<div class="bt">{mnp(s)[1]}<a class="btn" href="https://www.google.com/maps/search/?api=1&amp;query={q(s["jp"]+" "+s["addr"])}">Google Maps <i>&rarr;</i></a></div></article>'''
    def sec(g,r,rng,note): return f'<section><div class="bar {r}"><h2>{g["name"].upper()}</h2><span>{rng}</span></div><p class="gp">{g["note"]}</p><div class="wall w2">{tiles[g["name"]]}</div></section>'
    n1=sum(1 for s in PL if s['group']==p['g1']['name']); N=len(PL)
    HEROBLK=f'''<div class="col" style="padding:0"><div class="hero mos">{HEROIMG}<div class="vt">秋葉原</div></div>
<div class="hb"><span>{p['hb'][0]}</span><b>{p['hb'][1]}</b></div></div>''' if HEROIMG else f'''<div class="col"><div class="hb" style="margin-top:6px"><span>{p['hb'][0]}</span><b>{p['hb'][1]}</b></div></div>'''
    body=f'''<div class="col"><div class="top">{switch.logo(kind,'../')}{lang.button()}</div>
<h1>Where to {switch.dropdown(kind)} in{switch.area()}</h1></div>
{HEROBLK}
<div class="col"><div class="maphd"><h2 class="map">The map</h2><span class="nowmini"><span>Open now</span><button class="sw" id="sw" role="switch" aria-checked="false" aria-label="Show only places open now"></button></span></div><p class="gp">Tap a pin to see the name, tap again to jump to the place.</p><p class="nowlist off" id="nowlist"></p>{svgmap(p)}
<div class="lg"><span><i class=""></i>{p['g1']['lg']}</span><span><i class="r"></i>{p['g2']['lg']}</span></div>
{sec(p['g1'],'',f'1-{n1}',0)}{sec(p['g2'],'r',f'{n1+1}-{N}',0)}{cards}</div>
<div class="know"><div class="col"><h2>Good to know</h2><ul>{''.join(f'<li>{x}</li>' for x in p['know'])}</ul></div></div>
<details class="crd"><summary>Credits and sources</summary><p class="cr">{p['credit']}</p></details>'''
    css+='.car{position:relative;aspect-ratio:16/10;background:#222}.trk{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain}.trk::-webkit-scrollbar{display:none}.trk img{flex:0 0 100%;width:100%;height:100%;object-fit:cover;scroll-snap-align:center;scroll-snap-stop:always}\n.cb{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border:0;background:rgba(18,18,18,.72);color:#fff;font:700 30px/1 Archivo,sans-serif;cursor:pointer;padding:0 0 4px}.cb.pv{left:0}.cb.nx{right:0}.cb[hidden]{display:none}.cn{position:absolute;left:0;bottom:0;background:rgba(18,18,18,.78);color:#fff;font:700 12px/1 Archivo,sans-serif;letter-spacing:.08em;text-transform:uppercase;padding:7px 10px}.cn b{font-weight:800;margin-right:6px}\n.mn{margin-top:12px}.mg{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:6px;align-items:start}.mg img{display:block;width:100%;height:auto;background:#e5e2da}.mc{margin:6px 0 8px;font:700 12px/1.4 Archivo,sans-serif;color:#555}.mn .btn.mt{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 3px var(--ink)}.bt .btn{flex:1}'
    css+='.hero.mos{display:grid;grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr;gap:3px;height:340px;background:#222}.hero.mos img{display:block;width:100%;height:100%;object-fit:cover}.hero.mos a{display:block;min-height:0;overflow:hidden}.hero.mos>a:first-child{grid-row:1/3}'
    css+='.hd h3{font-size:34px;line-height:1.02}.card.r .genre{color:#fff}\n' if kind=='buy' else ''
    css+='.tj{position:absolute;inset:0;z-index:1;display:flex;align-items:center;justify-content:center;padding:34px 10px 44px;text-align:center;font:900 clamp(20px,6.4vw,30px)/1.15 "Noto Sans JP",sans-serif;color:#fff;opacity:.92}.tile{background:#1b1815}.tile.r{background:#2a1d0c}'
    ico=f'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 fill=%22%23{p["ac"]}%22/%3E%3C/svg%3E'
    ic=R/'brand'/f'{kind}-icon-64.png'; touch=''
    if ic.exists():
        import base64; ico='data:image/png;base64,'+base64.b64encode(ic.read_bytes()).decode()
        touch='<link rel="apple-touch-icon" href="apple-touch-icon.png">'
    t=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{p['title']}</title><meta name="claude:viewport-fit-sides" content="cover"><meta name="description" content="{esc(p['desc'])}"><meta name="robots" content="noindex, nofollow">
<meta property="og:title" content="{esc(p['title'])}"><meta property="og:description" content="{esc(p['desc'])}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{ico}">{touch}
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Noto+Sans+JP:wght@500;700;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
{body}
<script>
const OPEN={json.dumps(OPEN)};const SHORT={json.dumps(SHORT,ensure_ascii=False)};
{js}
document.querySelectorAll('.car').forEach(function(c){{var t=c.querySelector('.trk'),im=t.children,n=im.length,pv=c.querySelector('.pv'),nx=c.querySelector('.nx'),cn=c.querySelector('.cn');if(!n)return;function cur(){{return Math.round(t.scrollLeft/t.clientWidth)}}function sync(){{var i=Math.max(0,Math.min(n-1,cur()));pv.hidden=i===0;nx.hidden=i===n-1;cn.innerHTML='<b>'+(im[i].dataset.l||'')+'</b> '+(i+1)+'/'+n}}function go(d){{t.scrollTo({{left:(cur()+d)*t.clientWidth,behavior:'smooth'}})}}pv.onclick=function(){{go(-1)}};nx.onclick=function(){{go(1)}};t.addEventListener('scroll',sync,{{passive:true}});sync()}});
document.querySelectorAll('.card').forEach(c=>{{const t=c.querySelector('.tg');if(!t)return;const w=c.querySelector('.mn');if(!w)return;t.onclick=()=>{{const o=w.hidden;w.hidden=!o;t.setAttribute('aria-expanded',o);t.textContent=o?'Hide menu':'Show menu'}}}});
</script></body></html>'''
    assert '{{' not in t
    out=R/kind/'index.html'; out.parent.mkdir(exist_ok=True); out.write_text(t,encoding='utf-8'); print('wrote',out,N,'places')
if __name__=='__main__': build(sys.argv[1])
