"""buy/ の準備中ページ。drink のビルド結果から head/CSS を借りて、色・題・本文だけ差し替える。店が揃ったら packs/buy.json から build.py buy で置き換える。"""
import pathlib,sys,re
R=pathlib.Path(__file__).resolve().parent.parent; sys.path.insert(0,str(R/'engine')); import switch
t=(R/'drink/index.html').read_text(encoding='utf-8')
head=t[:t.index('<div class="col"><div class="top">')]
for a,b in (('F4B223','2F6FDB'),('F5B454','8DB4F0'),('A86A00','1F4FA8')): head=head.replace(a,b).replace(a.lower(),b.lower())
head=re.sub(r'<link rel="icon"[^>]*>','<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 fill=%22%232F6FDB%22/%3E%3C/svg%3E">',head,count=1)
head=re.sub(r'<title>.*?</title>','<title>Where to buy in Akihabara</title>',head)
head=re.sub(r'(name="description" content=")[^"]*',r'\1Shopping places in Akihabara, coming soon.',head)
head=re.sub(r'(og:title" content=")[^"]*',r'\1Where to buy in Akihabara',head)
head=re.sub(r'(og:description" content=")[^"]*',r'\1Shopping places in Akihabara, coming soon.',head)
body=f'''<div class="col"><div class="top">{switch.logo('buy','../')}<span>TOKYO · COMING SOON</span></div>
<h1>Where to {switch.dropdown('buy')} in<em>Akihabara</em></h1>
<p class="gp" style="margin:22px 0 40px">We are checking shops one by one. Real places, with hours and how to pay, will be here soon. Meanwhile, see <a href="../">where to eat</a> and <a href="../drink/">where to drink</a>.</p></div>
</body>'''
(R/'buy').mkdir(exist_ok=True); (R/'buy/index.html').write_text(head.replace('</style>',switch.CSS+'</style>',1)+body+'<script>'+switch.JS+'</script>',encoding='utf-8'); print('ok')
