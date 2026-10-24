from pathlib import Path
import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parents[1]
for e in json.loads((root/'research/catalogue-seed.json').read_text(encoding='utf-8')):
 if e['id'] not in sys.argv[1:]: continue
 lines=(root/'research/sources'/((e['arxiv'] or e['id'])+'.txt')).read_text(encoding='utf-8').splitlines()
 starts=[i for i,l in enumerate(lines) if re.match(r'^1\.?\s+Introduction\s*$',l,re.I)]
 start=starts[-1] if starts else 50
 hs=[(i,l) for i,l in enumerate(lines) if i>start and re.match(r'^\d\.?\d?\s+[A-Z]',l) and len(l)<105]
 print('\n##',e['id'],e['name']);print('SECTIONS',hs[:25])
 for kind,pat,budget in [('METHOD','method|approach|framework|architecture',2800),('EVIDENCE','experiment|evaluation|result|ablation',2200)]:
  hits=[i for i,l in hs if re.search(pat,l,re.I)]
  begin=hits[0] if hits else start+20
  end=next((i for i,l in hs if i>begin+3 and re.match(r'^\d\s',l)),min(begin+250,len(lines)))
  out=[]
  for i in range(begin,end):
   l=lines[i]
   if len(l)>100 and not l.startswith('|') and not re.match(r'^\\',l):
    out.append(str(i+1)+': '+l[:850])
  # Include later quantitative / ablation findings instead of raw table cells.
  if kind=='EVIDENCE':
   later=[(i,l) for i,l in enumerate(lines) if i>end and len(l)>150 and re.search(r'we (evaluate|report|observe|compare)|ablation|Table \d+ shows',l,re.I) and not l.startswith('|')]
   out=out[:2]+[str(i+1)+': '+l[:700] for i,l in later[:5]]
  print(kind+'\n'+'\n'.join(out)[:budget])
