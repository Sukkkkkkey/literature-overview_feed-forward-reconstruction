from pathlib import Path
import json,re,sys
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'research/contacts';O.mkdir(exist_ok=True)
items=json.loads((R/'research/additional-study-sources.json').read_text(encoding='utf-8'))
for e in items:
 if len(sys.argv)>2 and e['slug'] not in sys.argv[2:]:continue
 pdf=R/e['pdf'];reader=PdfReader(pdf);doc=pdfium.PdfDocument(pdf)
 if '--report' in sys.argv:
  print('\n'+e['slug'])
  for i,p in enumerate(reader.pages):
   text=p.extract_text() or ''
   caps=re.findall(r'(?:Figure|Table)\s+\d+\s*[:.][^\n]{0,140}',text)
   if caps:print('p'+str(i+1),'; '.join(caps)[:400])
  continue
 sheet=Image.new('RGB',(1240,1200),'#dce3e7');d=ImageDraw.Draw(sheet)
 for i in range(min(12,len(doc))):
  im=doc[i].render(scale=.5).to_pil().convert('RGB');im.thumbnail((300,370))
  x=(i%4)*310;y=(i//4)*400;sheet.paste(im,(x+(310-im.width)//2,y+25));d.text((x+8,y+7),e['slug']+' / p'+str(i+1),fill='black')
 sheet.save(O/(e['slug']+'.png'))
 print(e['slug'],flush=True)
