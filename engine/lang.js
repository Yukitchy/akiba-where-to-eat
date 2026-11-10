(function(){
var T=window.__T||{},L='en',store=new WeakMap(),busy=false;
var D={ja:['月','火','水','木','金','土','日'],zh:['周一','周二','周三','周四','周五','周六','周日'],ko:['월','화','수','목','금','토','일'],es:['lun','mar','mié','jue','vie','sáb','dom'],de:['Mo','Di','Mi','Do','Fr','Sa','So']};
var EN=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],LB={en:'EN',ja:'JA',zh:'ZH',es:'ES',de:'DE',ko:'KO'};
function tr(s){var k=s.replace(/\s+/g,' ').trim();if(!k)return null;var v=T[k];if(v&&v[L])return v[L];
 var m=k.match(/^(\d+) min walk$/);if(m&&T['{n} min walk']&&T['{n} min walk'][L])return T['{n} min walk'][L].replace('{n}',m[1]);
 var p=['Open right now: ','Closed: ','Pay: '];for(var i=0;i<p.length;i++){if(k.indexOf(p[i])===0){var q=T[p[i].trim()];if(q&&q[L])return q[L]+' '+k.slice(p[i].length)}}
 if(D[L]&&/\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b/.test(k)){return k.replace(/\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b/g,function(d){return D[L][EN.indexOf(d)]})}
 return null}
function skip(n){for(var e=n.parentNode;e&&e!==document.body;e=e.parentNode){var t=e.nodeName;if(t==='SCRIPT'||t==='STYLE'||t==='svg'||t==='SVG'||t==='NOSCRIPT'||(e.classList&&(e.classList.contains('langsw')||e.classList.contains('big')||e.classList.contains('no'))))return true}return false}
function node(n){if(skip(n))return;var o=store.get(n);if(o===undefined||(n.nodeValue!==o.t&&n.nodeValue!==o.o)){o={o:n.nodeValue,t:null};store.set(n,o)}
 if(L==='en'){if(o.t!==null){if(n.nodeValue!==o.o)n.nodeValue=o.o;o.t=null}return}
 var r=tr(o.o);if(r===null){if(o.t!==null){if(n.nodeValue!==o.o)n.nodeValue=o.o;o.t=null}return}
 var w=o.o.match(/^\s*/)[0],x=o.o.match(/\s*$/)[0],nv=w+r+x;o.t=nv;if(n.nodeValue!==nv)n.nodeValue=nv}
function walk(root){busy=true;try{var w=document.createTreeWalker(root,4,null),n,a=[];while(n=w.nextNode())a.push(n);a.forEach(node)}finally{busy=false}}
function apply(l){L=l;document.documentElement.lang=l;walk(document.body);
 var b=document.querySelector('.langsw .lc');if(b)b.textContent=LB[l];
}
var obs=new MutationObserver(function(ms){if(busy||L==='en')return;busy=true;try{ms.forEach(function(m){if(m.type==='characterData')node(m.target);else m.addedNodes.forEach(function(a){if(a.nodeType===3)node(a);else if(a.nodeType===1)walk(a)})})}finally{busy=false}});
function init(){var sw=document.querySelector('button.langsw');if(!sw)return;var O=['en','ja','zh','es','de','ko'];
 sw.addEventListener('click',function(){var l=O[(O.indexOf(L)+1)%O.length];try{localStorage.setItem('eatmap_lang',l)}catch(_){}apply(l)});
 var l=null;try{l=new URLSearchParams(location.search).get('lang')||localStorage.getItem('eatmap_lang')}catch(_){}
 if(!l||!LB[l])l='en';obs.observe(document.body,{childList:true,subtree:true,characterData:true});apply(l)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init()})();
