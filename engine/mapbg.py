"""絵地図(黄×黒)の背景SVG。ピンは build.py / pinzoom.js が上に載せる。f=緯度経度→SVG座標、sc=px/m"""
import math,random
XS=[0,70,205,340,470,560,600];YS=[0,70,200,330,470,600,680]
K='#121212';Y='#F4B223'
def _blds(seed=5,pad=14):
    r=random.Random(seed);out=[]
    for i in range(6):
        for j in range(6):
            x0,y0,x1,y1=XS[i]+pad,YS[j]+pad,XS[i+1]-pad,YS[j+1]-pad
            if x1-x0<20 or y1-y0<20:continue
            nx=3 if x1-x0>150 else 2 if x1-x0>70 else 1;ny=2 if y1-y0>70 else 1
            w=(x1-x0)/nx;h=(y1-y0)/ny
            for a in range(nx):
                for b in range(ny):
                    if r.random()<.1:continue
                    g=3+r.random()*2;r.choice((12,18,26,34,44))
                    out.append((x0+a*w+g,y0+b*h+g,w-2*g,h-2*g,r.random()))
    return out
def _path(pl):return 'M'+' L'.join(f'{x} {y}' for x,y in pl)
def _halo(t,x,y,anchor='middle',size=11,fill=K,halo=Y,w=4):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="800" fill="{fill}" stroke="{halo}" stroke-width="{w}" stroke-linejoin="round" paint-order="stroke">{t}</text>'
def affine(ax,bx,ay,by):
    """EAT用: 緯度経度→SVG座標（x=ax*lng+bx, y=ay*lat+by）。x方向の縮尺(px/m)も返す"""
    return (lambda a,b:(round(ax*b+bx),round(ay*a+by))),ax/(math.cos(math.radians(35.696))*111320)
def bg(f,sc,stations):
    ST={n:f(a,b) for n,a,b in stations}
    ak=ST.get('AKIHABARA') or next(iter(ST.values()))
    OK=f(35.7076,139.7745);KD=f(35.6890,139.7698)
    JR=[OK,ak,KD]
    CHUO=[f(35.7040,139.7716),f(35.6975,139.7712),f(35.6920,139.7706)]
    s=f'<rect width="600" height="680" fill="{Y}"/>'
    g=''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="680" stroke="{K}" stroke-width="14"/>' for x in range(70,620,135))
    g+=''.join(f'<line x1="0" y1="{y}" x2="600" y2="{y}" stroke="{K}" stroke-width="14"/>' for y in range(70,700,130))
    s+=g
    for x,y,w,h,r in _blds():s+=f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{"#FFD25E" if r<.5 else "#F7C233"}"/>'
    s+=f'<path d="{_path(CHUO)}" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round"/>'
    a=CHUO[0];b=CHUO[1];ang=math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))
    L=''
    L+=f'<text transform="translate({(a[0]+b[0])/2+14:.0f} {(a[1]+b[1])/2:.0f}) rotate({ang:.0f})" font-size="11" font-weight="900" letter-spacing="3" fill="{K}" stroke="#fff" stroke-width="3" paint-order="stroke">CHUO-DORI</text>'
    s+=f'<path d="{_path(JR)}" fill="none" stroke="{K}" stroke-width="18"/><path d="{_path(JR)}" fill="none" stroke="#fff" stroke-width="10"/><path d="{_path(JR)}" fill="none" stroke="{K}" stroke-width="2.5" stroke-dasharray="12 12"/>'
    # landmarks
    x,y=f(35.6997,139.7744);L+=f'<rect x="{x+2}" y="{y-46}" width="56" height="46" fill="#fff" stroke="{K}" stroke-width="3"/>'+''.join(f'<rect x="{x+9+i*11}" y="{y-38}" width="5" height="5" fill="{Y}"/>' for i in range(4))+_halo('Yodobashi Akiba',x+30,y+14)
    x,y=f(35.69899,139.77135);L+=f'<rect x="{x-50}" y="{y-56}" width="32" height="56" fill="#fff" stroke="{K}" stroke-width="3"/>'+''.join(f'<rect x="{x-43+i*11}" y="{y-48}" width="5" height="5" fill="{Y}"/>' for i in range(2))+_halo('Radio Kaikan',x-34,y+14)
    x,y=f(35.70195,139.76788);L+=f'<g stroke="{K}" stroke-width="5" fill="none" stroke-linecap="square"><path d="M{x-16} {y} V{y-26} M{x+16} {y} V{y-26} M{x-23} {y-30} H{x+23} M{x-18} {y-23} H{x+18}"/></g>'+_halo('Kanda Myojin',x,y+16)
    ra=math.degrees(math.atan2(JR[2][1]-JR[1][1],JR[2][0]-JR[1][0]))
    for n,(x,y) in ST.items():
        s+=f'<rect x="{x-22}" y="{y-8}" width="44" height="16" rx="2" fill="{K}" transform="rotate({ra:.0f} {x} {y})"/><circle cx="{x}" cy="{y}" r="6" fill="{Y}"/>';L+=_halo(n,x+28,y+5,'start',14,K,Y,4).replace('font-weight="800"','font-weight="900"')
    s+=f'<g class="bgl">{L}</g>'
    s+=f'<g transform="translate(40 56)"><circle r="19" fill="none" stroke="{K}" stroke-width="2"/><path d="M0 -15 L6 4 L0 0 L-6 4Z" fill="{K}"/><text y="-23" text-anchor="middle" font-size="12" font-weight="900" fill="{K}">N</text></g>'
    L=200*sc;s+=f'<g transform="translate(24 652)"><path d="M0 0H{L:.0f}M0 -5V5M{L:.0f} -5V5M{L/2:.0f} -3V3" stroke="{K}" stroke-width="2.5" fill="none"/><text x="{L/2:.0f}" y="-9" text-anchor="middle" font-size="11" font-weight="800" fill="{K}">200 m</text></g>'
    return s
