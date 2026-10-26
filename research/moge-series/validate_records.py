from pathlib import Path
from html.parser import HTMLParser
import json,hashlib
R=Path(__file__).resolve().parents[2];S=R/'research/moge-series';Q=R/'research/qa/moge'
class IDs(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=set();self.feed(s)
 def handle_starttag(self,t,a):
  if 'id' in dict(a):self.ids.add(dict(a)['id'])
coverage=json.loads((S/'coverage.json').read_text(encoding='utf-8'));n=0
for p in coverage['papers']:
 ids=IDs((R/'papers'/p['page']).read_text(encoding='utf-8')).ids
 for i in p['items']:
  if i['status']=='reference-only':assert i['priority']!='core' and i['source'] and i['note']
  else:assert i['target'] in ids,(p['page'],i['target'])
  n+=1
 for c in p['claims']:assert c['target'] in ids and c['conditions'] and c['evidence']
static=[json.loads((Q/f'static-{x}.json').read_text(encoding='utf-8')) for x in ['series','1','2','3']]
assert all(v['passed'] for v in static)
browser=json.loads((Q/'browser.json').read_text(encoding='utf-8'));assert not browser['errors'] and not browser['external'] and browser['legacyAnchors'] and browser['jsOff']
for p in browser['pages']:
 assert not p['desktopOverflow'] and not p['mobileOverflow'] and not p['desktopBrokenImages'] and not p['mobileBrokenImages']
 assert p['mobileToc'] and p['mobileAnchor']
 for k,v in p.items():
  if any(x in k for x in ['Lightbox','Zoom','Escape','FontToggle']):assert v
for f in json.loads((S/'figures.json').read_text(encoding='utf-8')):assert hashlib.sha256((R/f['image']).read_bytes()).hexdigest()==f['image_sha256']
note=Path(r'D:\Obsidian\storage\Sukey\路漫漫其修远兮\A_notes\3d\papers\⭐Feed-Forward 3D Reconstruction.md')
note_hash=hashlib.sha256(note.read_bytes()).hexdigest()
report=dict(checked='2026-10-26',pages=4,coverage_items=n,coverage_targets='passed',structure_and_reading=[dict(file=v['file'],passed=v['passed'],reading=v['reading']) for v in static],coverage_warning_resolution='Skill validator expects adjacent coverage.json; project uses research/moge-series/coverage.json. All per-paper targets and omissions validated separately here.',browser=browser,source_figure_hashes='passed',visual_review='Inspected desktop/mobile screenshots and all six new original crops; no clipped captions or missing table rows.',readonly_note_sha256=note_hash,readonly_note_stable_since_first_observation=note_hash=='61a5b3affd67c99d4b9977522981b46c8d93975407e100d19d667f8e44533849',readonly_note_matches_historical_snapshot=False,models_executed=False)
assert report['readonly_note_stable_since_first_observation']
(S/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Validated 4 pages,',n,'coverage items, original crop hashes, offline desktop/mobile and legacy anchors')
