(function(){var svg=document.getElementById('map');if(!svg)return;
var W=600,H=680,vb={x:0,y:0,w:W,h:H},PH=window.__PH||{},NS='http://www.w3.org/2000/svg',MAXZ=4,FULLZ=3.4,MINZ=.62,MARG=26;
function E(n,a,p){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
var pins=[],lim=1e9,bgl=svg.querySelector('.bgl'),mdots=svg.querySelectorAll('.mdot'),stdots=svg.querySelectorAll('.stdot'),stbars=svg.querySelectorAll('.stbar');
stbars.forEach(function(r){var mm=/rotate\((-?[\d.]+) (-?[\d.]+) (-?[\d.]+)\)/.exec(r.getAttribute('transform')||'');if(mm){r.dataset.a=mm[1];r.dataset.cx=mm[2];r.dataset.cy=mm[3]}});
var dcl=E('g',{class:'decl'},svg);svg.insertBefore(dcl,svg.querySelector('.pin'));
document.querySelectorAll('#map .pin').forEach(function(a){
 var c=a.querySelector('circle'),t=a.querySelector('text'),lt=a.querySelector('.lbl text');if(!c||!t)return;
 var n=a.getAttribute('data-n'),fill=c.getAttribute('fill'),tf=t.getAttribute('fill'),nm=lt?lt.textContent:'',cx=+c.getAttribute('cx'),cy=+c.getAttribute('cy'),ph=PH[n];
 while(a.firstChild)a.removeChild(a.firstChild);
 var g=E('g',{},a);E('circle',{r:20,fill:'#fff',opacity:0},g);var m=E('g',{class:'mini'},g);
 E('rect',{x:-13.5,y:-13.5,width:27,height:27,rx:4,fill:fill,stroke:fill==='#121212'?'#fff':'#121212','stroke-width':2},m);
 var mt=E('text',{y:5,'text-anchor':'middle','font-size':14,'font-weight':900,fill:tf},m);mt.textContent=n;
 if(ph){a.classList.add('hp');var f=E('g',{class:'full'},g);
  E('polygon',{points:'-6,-8 6,-8 0,0',fill:fill},f);
  E('rect',{x:-23,y:-64,width:46,height:56,rx:3,fill:fill,stroke:'#fff','stroke-width':1.5},f);
  var ft=E('text',{y:-52,'text-anchor':'middle','font-size':11,'font-weight':900,fill:'#fff'},f);ft.textContent=n;
  var fo=E('foreignObject',{x:-21,y:-48,width:42,height:38},f),im=document.createElement('img');
  im.src=ph;im.setAttribute('referrerpolicy','no-referrer');im.setAttribute('draggable','false');im.alt='';im.style.cssText='display:block;width:100%;height:100%;object-fit:cover;pointer-events:none';fo.appendChild(im)}
 var w=Math.round(nm.length*7+16),l=E('g',{class:'lbl'},g);
 E('rect',{x:-w/2,y:-26,width:w,height:24,fill:'#121212'},l);var lx=E('text',{y:-9,'text-anchor':'middle','font-size':12,'font-weight':800,fill:'#fff'},l);lx.textContent=nm;
 var dl=E('line',{stroke:'#121212','stroke-opacity':.5,'stroke-width':1.25,'vector-effect':'non-scaling-stroke',style:'display:none'},dcl),dc=E('circle',{fill:'#121212',style:'display:none'},dcl);
 pins.push({a:a,g:g,l:l,x:cx,y:cy,hp:!!ph,hero:false,dl:dl,dc:dc})});
var wrap=document.createElement('div');wrap.style.cssText='position:relative';svg.parentNode.insertBefore(wrap,svg);wrap.appendChild(svg);
var st=document.createElement('style');st.textContent='#map .full{display:none}#map .pin.hero .full{display:inline}#map .pin.hero .mini{display:none}#map .bgl{pointer-events:none}#map .pin .lbl{display:none}#map .pin:hover .lbl,#map .pin.on .lbl{display:block}.mz{position:absolute;right:8px;top:8px;display:flex;flex-direction:column;gap:4px;z-index:3}.mz button{width:36px;height:36px;border:0;background:#121212;color:#fff;font:900 20px/1 Archivo,sans-serif;cursor:pointer;padding:0;-webkit-tap-highlight-color:transparent}.mz button:active{background:#444}.mz button[hidden]{display:none}';document.head.appendChild(st);
var bx=document.createElement('div');bx.className='mz';bx.innerHTML='<button type="button" data-z="in" aria-label="Zoom in">+</button><button type="button" data-z="out" aria-label="Zoom out">&minus;</button><button type="button" data-z="reset" aria-label="Reset map" hidden style="font-size:13px">1×</button>';wrap.appendChild(bx);
function zoom(){return W/vb.w}
var soft=false,bnc=null;
function fitW(){var col=wrap?wrap.parentNode:null;if(!col)return;var cs=getComputedStyle(col),pw=col.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight),nh=pw*H/W,ah=window.innerHeight-12;
 if(nh>ah){wrap.style.width=Math.max(280,Math.round(ah*W/H))+'px';wrap.style.margin='0 auto'}else{wrap.style.width='';wrap.style.margin=''}}
function clamp(m){vb.w=Math.min(W/MINZ,Math.max(W/MAXZ,vb.w));vb.h=vb.w*H/W;var mg=m||0;
 if(vb.w>=W)vb.x=(W-vb.w)/2;else vb.x=Math.min(W-vb.w+mg,Math.max(-mg,vb.x));
 if(vb.h>=H)vb.y=(H-vb.h)/2;else vb.y=Math.min(H-vb.h+mg,Math.max(-mg,vb.y))}
function bounce(){var x0=vb.x,y0=vb.y;clamp(0);var gx=vb.x,gy=vb.y;vb.x=x0;vb.y=y0;
 if(Math.abs(gx-x0)<.5&&Math.abs(gy-y0)<.5){ui();return}
 var t0=performance.now();if(bnc)cancelAnimationFrame(bnc);
 (function f(n){var k=Math.min(1,(n-t0)/180);vb.x=x0+(gx-x0)*k;vb.y=y0+(gy-y0)*k;ui();if(k<1)bnc=requestAnimationFrame(f)})(t0)}
function ui(){fitW();clamp(soft?MARG:0);svg.setAttribute('viewBox',vb.x+' '+vb.y+' '+vb.w+' '+vb.h);var cw=svg.clientWidth||390,s=vb.w/cw,z=zoom();svg.classList.toggle('zm',z>1.25);
 var ch=svg.clientHeight||442,all=z>=FULLZ,pk=[],chg=false,ix=0;
 pins.forEach(function(p){p.ox=0;p.oy=0;var h=false;
  if(p.hp){var sx=(p.x-vb.x)/vb.w*cw,sy=(p.y-vb.y)/vb.h*ch;
   if(all)h=sx>-24&&sx<cw+24&&sy>70&&sy<ch+40&&ix++<lim;
   else if(sx>-8&&sx<cw+8&&sy>68&&sy<ch+10){h=true;for(var i=0;i<pk.length;i++)if(Math.abs(pk[i][0]-sx)<54&&Math.abs(pk[i][1]-sy)<70){h=false;break}if(h)pk.push([sx,sy])}}
  if(h!==p.hero){p.hero=h;p.a.classList.toggle('hero',h);chg=true}});
 for(var ps=0;ps<3;ps++)for(var i=0;i<pins.length;i++)for(var j=i+1;j<pins.length;j++){var a=pins[i],b=pins[j];if(a.hero&&b.hero)continue;
  var cx2=a.hero||b.hero?52:34,cy2=a.hero||b.hero?66:34,
  ax=(a.x-vb.x)/vb.w*cw+a.ox,ay=(a.y-vb.y)/vb.h*ch+a.oy+(a.hero?-28:0),bx2=(b.x-vb.x)/vb.w*cw+b.ox,by2=(b.y-vb.y)/vb.h*ch+b.oy+(b.hero?-28:0),dx=bx2-ax,dy=by2-ay;
  if(Math.abs(dx)<cx2&&Math.abs(dy)<cy2){var px2=cx2-Math.abs(dx),py2=cy2-Math.abs(dy),fa=a.hero?0:(b.hero?1:.5),fb=1-fa,mv;
   if(px2<py2){mv=px2*(dx<0?-1:1);b.ox+=mv*fb;a.ox-=mv*fa}else{mv=py2*(dy<0?-1:1);b.oy+=mv*fb;a.oy-=mv*fa}}}
 pins.forEach(function(p){if(!p.hero){var m2=Math.hypot(p.ox,p.oy);if(m2>20){p.ox*=20/m2;p.oy*=20/m2}
   var sx3=(p.x-vb.x)/vb.w*cw+p.ox,sy3=(p.y-vb.y)/vb.h*ch+p.oy;
   if(sx3<14)p.ox+=14-sx3;else if(sx3>cw-14)p.ox-=sx3-(cw-14);
   if(sy3<14)p.oy+=14-sy3;else if(sy3>ch-14)p.oy-=sy3-(ch-14)}});
 pins.forEach(function(p){
  p.g.setAttribute('transform','translate('+(p.x+p.ox*s)+' '+(p.y+p.oy*s)+') scale('+s+')');p.l.setAttribute('transform','translate(0 '+(p.hero?-62:-12)+')');
  var off=!p.hero&&Math.hypot(p.ox,p.oy)>3;
  if(p.dl){p.dl.setAttribute('x1',p.x);p.dl.setAttribute('y1',p.y);p.dl.setAttribute('x2',p.x+p.ox*s);p.dl.setAttribute('y2',p.y+p.oy*s);p.dl.style.display=off?'':'none'}
  if(p.dc){p.dc.setAttribute('cx',p.x);p.dc.setAttribute('cy',p.y);p.dc.setAttribute('r',3.4*s);p.dc.style.display=off?'':'none'}});
 if(chg)pins.forEach(function(p){if(p.hero)p.a.parentNode.appendChild(p.a)});
 if(bgl)svg.appendChild(bgl);
 for(var i2=0;i2<mdots.length;i2++)mdots[i2].setAttribute('r',3.4*s);
 for(var i3=0;i3<stdots.length;i3++)stdots[i3].setAttribute('r',6.5*s);
 var bk=Math.min(1,1/z);for(var i4=0;i4<stbars.length;i4++){var r4=stbars[i4];if(r4.dataset.a)r4.setAttribute('transform','translate('+r4.dataset.cx+' '+r4.dataset.cy+') scale('+bk+') rotate('+r4.dataset.a+') translate('+(-r4.dataset.cx)+' '+(-r4.dataset.cy)+')')}
 bx.querySelector('[data-z=reset]').hidden=Math.abs(z-1)<.01;bx.querySelector('[data-z=in]').disabled=z>=MAXZ-.01}
function at(f,px,py){soft=false;var r=svg.getBoundingClientRect(),ux=vb.x+(px-r.left)/r.width*vb.w,uy=vb.y+(py-r.top)/r.height*vb.h;var nz=Math.min(MAXZ,Math.max(MINZ,zoom()*f));vb.w=W/nz;vb.h=H/nz;vb.x=ux-(px-r.left)/r.width*vb.w;vb.y=uy-(py-r.top)/r.height*vb.h;ui()}
function mid(){var r=svg.getBoundingClientRect();return[r.left+r.width/2,r.top+r.height/2]}
bx.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var k=b.getAttribute('data-z'),c=mid();if(k==='in')at(1.6,c[0],c[1]);else if(k==='out')at(1/1.6,c[0],c[1]);else{vb={x:0,y:0,w:W,h:H};ui()}});
svg.addEventListener('wheel',function(e){if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();at(e.deltaY<0?1.15:1/1.15,e.clientX,e.clientY)},{passive:false});
svg.addEventListener('dblclick',function(e){if(e.target.closest('.pin'))return;at(2,e.clientX,e.clientY)});
var moved=0,last=null,pd=0;
function pan(dx,dy){var r=svg.getBoundingClientRect();vb.x-=dx/r.width*vb.w;vb.y-=dy/r.height*vb.h;ui()}
svg.addEventListener('touchstart',function(e){moved=0;if(e.touches.length===1)soft=true;if(e.touches.length===2){pd=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);e.preventDefault()}last=e.touches.length===1?[e.touches[0].clientX,e.touches[0].clientY]:null},{passive:false});
svg.addEventListener('touchmove',function(e){if(e.touches.length===2){e.preventDefault();var d=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);if(pd>0)at(d/pd,(e.touches[0].clientX+e.touches[1].clientX)/2,(e.touches[0].clientY+e.touches[1].clientY)/2);pd=d;moved=99}
 else if(e.touches.length===1&&last&&zoom()>1.01){e.preventDefault();var x=e.touches[0].clientX,y=e.touches[0].clientY;moved+=Math.abs(x-last[0])+Math.abs(y-last[1]);pan(x-last[0],y-last[1]);last=[x,y]}},{passive:false});
var md=null;svg.addEventListener('touchend',function(){if(soft){soft=false;bounce()}},{passive:true});
svg.addEventListener('mousedown',function(e){if(zoom()>1.01||zoom()<0.99){md=[e.clientX,e.clientY];moved=0;soft=true}});
window.addEventListener('mousemove',function(e){if(!md)return;moved+=Math.abs(e.clientX-md[0])+Math.abs(e.clientY-md[1]);pan(e.clientX-md[0],e.clientY-md[1]);md=[e.clientX,e.clientY]});
window.addEventListener('mouseup',function(){if(md){md=null;soft=false;bounce()}});
svg.addEventListener('click',function(e){if(moved>8){e.stopPropagation();e.preventDefault();moved=0}},true);
window.addEventListener('resize',ui);
try{var q=new URLSearchParams(location.search).get('pz');if(q){var a=q.split(',').map(Number);vb.w=W/a[0];vb.h=H/a[0];vb.x=a[1]-vb.w/2;vb.y=a[2]-vb.h/2}}catch(_){}
ui();
/* 初回だけ：地図が画面に入ったら1回、寄った状態から引いて全体になる（写真ピンが数字ピンへ戻る）。触れたら止める */
var demoOn=false,raf=0,home=null;
function ez(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2}
function cl01(v){return Math.min(1,Math.max(0,v))}
function frame(t){var z=t<300?2.3:t<1100?2.3-.3*ez((t-300)/800):t<2700?2-ez((t-1100)/1600):1,w=W/z;
 vb.w=w;vb.h=w*H/W;vb.x=hx-vb.w/2;vb.y=hy-vb.h/2;lim=Math.ceil((1-cl01((t-300)/800))*pins.length);if(t>=1100)lim=0;ui()}
var hx=W/2,hy=H/2;
function stop(){if(!demoOn)return;demoOn=false;cancelAnimationFrame(raf);lim=1e9;if(home){vb={x:home.x,y:home.y,w:home.w,h:home.h};ui()}}
function play(){if(demoOn||sessionStorage.getItem('pzdemo'))return;
 var xs=[],ys=[];pins.forEach(function(p){if(p.hp){xs.push(p.x);ys.push(p.y)}});if(xs.length<3)return;
 xs.sort(function(a,b){return a-b});ys.sort(function(a,b){return a-b});hx=xs[xs.length>>1];hy=ys[ys.length>>1];
 home={x:vb.x,y:vb.y,w:vb.w,h:vb.h};demoOn=true;try{sessionStorage.setItem('pzdemo','1')}catch(_){}
 var t0=performance.now();(function f(n){if(!demoOn)return;var t=n-t0;if(t>=2700){demoOn=false;lim=1e9;vb={x:home.x,y:home.y,w:home.w,h:home.h};ui();return}frame(t);raf=requestAnimationFrame(f)})(t0)}
['touchstart','mousedown','wheel','keydown'].forEach(function(ev){svg.addEventListener(ev,stop,{passive:true})});bx.addEventListener('click',stop,true);
try{var dm=new URLSearchParams(location.search).get('dm');
 if(dm!==null){var xs0=pins.filter(function(p){return p.hp});xs0.sort(function(a,b){return a.x-b.x});hx=xs0.length?xs0[xs0.length>>1].x:W/2;xs0.sort(function(a,b){return a.y-b.y});hy=xs0.length?xs0[xs0.length>>1].y:H/2;frame(+dm)}
 else if(!new URLSearchParams(location.search).get('pz')&&!matchMedia('(prefers-reduced-motion:reduce)').matches&&'IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){io.disconnect();setTimeout(play,150)}},{threshold:.6});io.observe(svg)}}catch(_){}
})();
