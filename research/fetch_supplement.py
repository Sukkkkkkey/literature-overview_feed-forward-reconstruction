from pathlib import Path
from html.parser import HTMLParser
import ast,urllib.request,re,json,hashlib,concurrent.futures as cf
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
tree=ast.parse((ROOT/'research/fetch_sources.py').read_text(encoding='utf-8'))
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.ClassDef)],type_ignores=[]),'reader','exec'))
cp=ROOT/'research/catalogue-seed.json';mp=ROOT/'research/source-manifest.json'
entries=json.loads(cp.read_text(encoding='utf-8')); manifest=json.loads(mp.read_text(encoding='utf-8'))
new=[('N07','StreamVGGT','2507.11539'),('N08','VGGT-Long','2507.16443'),('N09','D4RT','2512.08924'),('N10','Depth Anything V2','2406.09414'),('N11','TripoSR','2403.02151'),('N12','InstantMesh','2404.07191')]
for i,n,a in new:
 if not any(e['id']==i for e in entries): entries.append(dict(id=i,name=n,arxiv=a,url='https://arxiv.org/abs/'+a,priority='P1',addition_candidate=True))
cp.write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
def fetch(e):
 pdf=e['id'] in ['A02','E03']
 url='https://arxiv.org/'+('pdf/' if pdf else 'html/')+e['arxiv']
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 with urllib.request.urlopen(req,timeout=75) as r: b=r.read();url=r.geturl()
 out=ROOT/'research/sources'/e['arxiv']
 out.with_suffix('.pdf' if pdf else '.html') # arxiv IDs contain a dot: do not replace their suffix
 (Path(str(out)+('.pdf' if pdf else '.html'))).write_bytes(b)
 if pdf:
  reader=PdfReader(str(out)+'.pdf');s='\n\n'.join(f'[PDF page {i+1}]\n'+(p.extract_text() or '') for i,p in enumerate(reader.pages))
 else:
  p=Reader();p.feed(b.decode('utf-8','replace'));s=p.text()
 Path(str(out)+'.txt').write_text(s,encoding='utf-8')
 return dict(id=e['id'],name=e['name'],arxiv=e['arxiv'],checked='2026-10-24',status='fulltext-pdf' if pdf else 'fulltext-html',url=url,text_file='research/sources/'+e['arxiv']+'.txt',characters=len(s),sha256=hashlib.sha256(b).hexdigest())
selected=[e for e in entries if e['id'] in ['A02','E03']+[x[0] for x in new]]
with cf.ThreadPoolExecutor(max_workers=3) as pool:
 for r in pool.map(fetch,selected):
  manifest=[m for m in manifest if m['id']!=r['id']]+[r]
  mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
  print(r['id'],r['status'],r['characters'],flush=True)
