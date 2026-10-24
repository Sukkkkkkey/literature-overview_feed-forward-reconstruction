"""Download and verify the fixed PDF versions used by the added studies."""
from pathlib import Path
import json,sys,importlib.util,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prepare',R/'research/prepare_paper_studies.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
items=json.loads((R/'research/additional-studies.json').read_text(encoding='utf-8'))
mod.SLUGS={x['id']:x['slug'] for x in items}
entries=[e for e in json.loads((R/'catalogue.json').read_text(encoding='utf-8')) if e['id'] in mod.SLUGS]
reports=[];errors=[]
def prepare(e):
 pdf=R/'research/sources'/(e['version']+'.pdf')
 if not pdf.exists():
  part=pdf.with_suffix('.download')
  subprocess.run(['curl.exe','-L','--fail','--silent','--show-error','--max-time','180','--connect-timeout','20','--retry','2','--output',str(part),'https://arxiv.org/pdf/'+e['version']],check=True,timeout=600)
  if not part.read_bytes().startswith(b'%PDF'):raise ValueError('Not PDF')
  part.replace(pdf)
 return mod.prepare(e)
with ThreadPoolExecutor(max_workers=3) as pool:
 futures={pool.submit(prepare,e):e for e in entries}
 for f in as_completed(futures):
  try:reports.append(f.result())
  except Exception as ex:errors.append({'id':futures[f]['id'],'error':str(ex)});print(errors[-1],flush=True)
(R/'research/additional-study-sources.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared',len(reports),'errors',len(errors))
if errors:sys.exit(1)
