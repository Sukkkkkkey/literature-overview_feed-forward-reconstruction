from pathlib import Path
import json, re, urllib.request, hashlib
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader

R=Path(__file__).resolve().parents[1]
SLUGS={'A01':'dust3r','A06':'vggt','A08':'pi3','A09':'mapanything','A10':'depth-anything-3','A12':'vggt-omega'}
entries=[e for e in json.loads((R/'catalogue.json').read_text(encoding='utf-8')) if e['id'] in SLUGS]
class Figures(HTMLParser):
 def __init__(self): super().__init__();self.items=[];self.current=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='figure':self.current={'id':a.get('id'),'text':[],'images':[]}
  if self.current is not None and tag=='img':self.current['images'].append(a)
 def handle_data(self,s):
  if self.current is not None:self.current['text'].append(s)
 def handle_endtag(self,tag):
  if tag=='figure' and self.current is not None:
   self.current['text']=re.sub(r'\s+',' ',' '.join(self.current['text'])).strip();self.items.append(self.current);self.current=None

def prepare(e):
 slug=SLUGS[e['id']];pdf=R/'research/sources'/(e['version']+'.pdf')
 if not pdf.exists():
  req=urllib.request.Request('https://arxiv.org/pdf/'+e['version'],headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=90) as response:data=response.read()
  if not data.startswith(b'%PDF'):raise ValueError('Not PDF: '+e['name'])
  pdf.write_bytes(data)
 reader=PdfReader(pdf);pages=[p.extract_text() or '' for p in reader.pages]
 (R/'research/sources'/(e['version']+'-pages.txt')).write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n'+p for i,p in enumerate(pages)),encoding='utf-8')
 p=Figures();p.feed((R/'research/sources'/(e['arxiv']+'.html')).read_text(encoding='utf-8'))
 report={'id':e['id'],'slug':slug,'name':e['name'],'version':e['version'],'pdf':str(pdf.relative_to(R)).replace('\\','/'),'url':'https://arxiv.org/pdf/'+e['version'],'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(pages),'figures':p.items}
 (R/'research'/('figures-'+slug+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(slug, len(pages),'pages',flush=True)
 return report

if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=3) as pool:reports=list(pool.map(prepare,entries))
 (R/'research/paper-study-sources.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
