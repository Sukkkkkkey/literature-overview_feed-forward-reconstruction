from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
import json,hashlib
R=Path(__file__).resolve().parents[1]
class Scan(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.assets=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id'in d:self.ids.append(d['id'])
  if 'href'in d:self.links.append(d['href'])
  if 'src'in d:self.assets.append(d['src'])
pages=[R/'index.html',R/'review.html']+list((R/'topics').glob('*.html'))+list((R/'papers').glob('*.html'));scans={};errors=[]
for p in pages:
 s=Scan();s.feed(p.read_text(encoding='utf-8'));scans[p]=s
 if len(s.ids)!=len(set(s.ids)):errors.append(f'Duplicate IDs {p.name}')
 if '{{' in p.read_text(encoding='utf-8'):errors.append(f'Unexpanded template {p.name}')
for p,s in scans.items():
 for h in s.links+s.assets:
  u=urlsplit(h)
  if u.scheme:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if not target.exists():errors.append(f'Missing {p.name}: {h}')
  elif u.fragment and target in scans and u.fragment not in scans[target].ids:errors.append(f'Missing anchor {p.name}: {h}')
data=json.loads((R/'catalogue.json').read_text(encoding='utf-8'))
for e in data:
 if not (R/e['source_local']).exists():errors.append('No source '+e['id'])
 if not e['source_sha256']:errors.append('No hash '+e['id'])
report={'pages':len(pages),'entries':len(data),'papers':sum(e['type']=='论文' for e in data),'local_checks':errors}
note=Path(r'D:\Obsidian\storage\Sukey\路漫漫其修远兮\A_notes\3d\papers\⭐Feed-Forward 3D Reconstruction.md')
if note.exists():
 report['readonly_note_sha256']=hashlib.sha256(note.read_bytes()).hexdigest()
 report['readonly_note_unchanged']=report['readonly_note_sha256'].upper()=='89AF9576D17CC9CDDE050D8BA7203B5EF4B684AC45FA945101FEFE1D72E548D0'
 if not report['readonly_note_unchanged']:errors.append('Original note changed')
(R/'research/qa').mkdir(exist_ok=True)
(R/'research/qa/link-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2));assert not errors
