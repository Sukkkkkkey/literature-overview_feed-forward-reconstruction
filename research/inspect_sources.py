from pathlib import Path
import argparse,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('ids',nargs='+');p.add_argument('--limit',type=int,default=6500);p.add_argument('--pattern');p.add_argument('--context',type=int,default=1);p.add_argument('--lines');a=p.parse_args()
catalog=json.loads((ROOT/'research/catalogue-seed.json').read_text(encoding='utf-8'))
for entry in catalog:
 if entry['id'] not in a.ids: continue
 path=ROOT/'research/sources'/((entry['arxiv'] or entry['id'])+'.txt')
 print('\n###',entry['id'],entry['name'])
 if not path.exists(): print('NOT ACQUIRED');continue
 lines=path.read_text(encoding='utf-8').splitlines()
 if a.lines:
  lo,hi=map(int,a.lines.split(':')); print('\n'.join(f'{i+1}: {lines[i]}' for i in range(lo-1,min(hi,len(lines))))[:a.limit]);continue
 if a.pattern:
  out=[]; seen=set()
  for i,l in enumerate(lines):
   if re.search(a.pattern,l,re.I):
    for j in range(max(0,i-a.context),min(len(lines),i+a.context+1)):
     if j not in seen: out.append(f'{j+1}: {lines[j]}');seen.add(j)
  print('\n'.join(out)[:a.limit]);continue
 starts=[i for i,l in enumerate(lines) if re.match(r'^1\.?\s+Introduction\s*$',l,re.I)]
 body=starts[-1] if starts else 60
 headings=[(i,l) for i,l in enumerate(lines) if i>body and re.match(r'^(?:[2-7](?:\.|\s)|[A-Z]\.\d|\d+\.\d\s)',l) and len(l)<125]
 print('HEADINGS:', '; '.join(f'{i+1}:{l}' for i,l in headings)[:2000])
 method=[i for i,l in headings if i>60 and re.search('method|approach|framework|architecture|model|preliminar',l,re.I)]
 experiments=[i for i,l in headings if i>60 and re.search('experiment|evaluation|result|benchmark',l,re.I)]
 selected=[]
 for label,loc,amount in [('METHOD',method, int(a.limit*.58)),('EXPERIMENT',experiments,int(a.limit*.42))]:
  start=loc[0] if loc else (max(65,len(lines)//5) if label=='METHOD' else max(100,len(lines)//2))
  s='\n'.join(f'{j+1}: {lines[j]}' for j in range(start,min(len(lines),start+170)) if not lines[j].startswith('|'))
  selected.append(label+'\n'+s[:amount])
 print('\n'.join(selected))
