from pathlib import Path
from pypdf import PdfReader
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1]
items=json.loads((R/'research/additional-study-sources.json').read_text(encoding='utf-8'))
for arg in sys.argv[1:]:
 slug,nums=arg.split(':');e=next(x for x in items if x['slug']==slug);doc=PdfReader(R/e['pdf'])
 for n in nums.split(','):
  print('\n###',slug,'PDF PAGE',n,'###\n'+doc.pages[int(n)-1].extract_text())
