from pathlib import Path
import json,hashlib
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
Q=R/'research/qa/moge';Q.mkdir(parents=True,exist_ok=True)
records=[]
for version in ['2410.19115v3','2507.02546v1','2607.17967v2']:
 p=R/'research/sources'/f'{version}.pdf'
 reader=PdfReader(p);texts=[page.extract_text(extraction_mode='layout') for page in reader.pages]
 (R/'research/sources'/f'{version}-pages.txt').write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n{t}' for i,t in enumerate(texts)),encoding='utf-8')
 records.append(dict(version=version,url=f'https://arxiv.org/pdf/{version}',pdf=str(p.relative_to(R)).replace('\\','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pages=len(texts),checked='2026-10-26'))
 doc=pdfium.PdfDocument(p)
 for start in range(0,min(len(doc),16),4):
  sheet=Image.new('RGB',(1200,850),'#dce3e7')
  for j in range(4):
   n=start+j
   if n>=len(doc):break
   im=doc[n].render(scale=1).to_pil().convert('RGB');im.thumbnail((295,810))
   sheet.paste(im,(j*300,25));ImageDraw.Draw(sheet).text((j*300+5,5),f'{version} p{n+1}',fill='black')
  sheet.save(Q/f'{version}-contact-{start+1}.jpg')
(R/'research/moge-series/sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print([(r['version'],r['pages']) for r in records])
