"""Compact source reader for manual method/experiment checking."""
from pathlib import Path
import sys,json,re
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1]
E={e['id']:e for e in json.loads((R/'catalogue.json').read_text(encoding='utf-8'))}
for pid in sys.argv[1:]:
 e=E[pid];lines=(R/e['source_local']).read_text(encoding='utf-8').splitlines()
 candidates=[i for i,s in enumerate(lines) if re.match(r'^[234](?:\s|\.\s).*(?:Method|Approach|Framework|Our|Pre-training|Analysis|Reliab)',s,re.I)]
 start=candidates[-1] if candidates else 80
 end=next((i for i in range(start+1,len(lines)) if lines[i]=='References'),len(lines))
 body=[s for s in lines[start:end] if not s.startswith('|') and (len(s)>85 or re.match(r'^\d',s) or re.match(r'^(?:Figure|Table) \d',s))]
 print('\n###',pid,e['name'],e['version'],'###\n')
 print('\n'.join(body)[:18000])
