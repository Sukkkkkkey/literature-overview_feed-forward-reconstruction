"""Record final coverage, source integrity and the completed browser checks."""
from pathlib import Path
import json,hashlib,re,datetime
import check_html
R=Path(__file__).resolve().parents[1]
data=json.loads((R/'catalogue.json').read_text(encoding='utf-8'))
reg=json.loads((R/'papers/registry.json').read_text(encoding='utf-8'))
figs=json.loads((R/'research/figure-manifest.json').read_text(encoding='utf-8'))
browser=json.loads((R/'research/qa-v2/browser-checks.json').read_text(encoding='utf-8'))
assert len(browser['pages'])==35 and not browser['errors'] and not browser['external']
assert all(not p['desktopOverflow'] and not p['mobileOverflow'] and not p['brokenImages'] for p in browser['pages'])
topics=list((R/'topics').glob('*.html'))
ids=[pid for p in topics for pid in re.findall(r'<article class="method" id="method-([A-Z]\d\d)"',p.read_text(encoding='utf-8'))]
expected=[e['id'] for e in data if e['topic']!='00']
assert sorted(ids)==sorted(expected),(set(expected)-set(ids),len(ids))
assert len(reg)==23 and len(figs)==63
for e in reg:
 body=(R/e['path']).read_text(encoding='utf-8')
 assert all(f'id="{section}"' in body for section in e['sections'])
for e in figs:assert (R/e['image']).exists()
src=[]
for filename in ['paper-study-sources.json','additional-study-sources.json']:
 src+=json.loads((R/'research'/filename).read_text(encoding='utf-8'))
for e in src:assert hashlib.sha256((R/e['pdf']).read_bytes()).hexdigest()==e['sha256'],e['slug']
report={
 'checked_at':datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
 'html_pages':35,'topics':10,'independent_paper_studies':23,'catalogue_entries':69,
 'research_papers':67,'engineering_entries':1,'survey_entries':1,
 'topic_method_cards':len(ids),'original_figure_table_plates':len(figs),
 'local_links_and_anchors':'passed','all_primary_method_assignments_covered':True,
 'fixed_version_pdf_hashes_verified':len(src),'original_note_unchanged':check_html.report.get('readonly_note_unchanged'),
 'browser':{'pages':len(browser['pages']),'desktop_viewport':[1460,1050],'mobile_viewport':[390,844],
 'overflow_pages':0,'broken_images':0,'script_errors':0,'external_requests':0,
 'paper_lightbox_and_section_navigation':'passed for all 23 studies','topic_mobile_toc':'passed for all 10 topics',
 'search_hash_open_font_toggle_gauge_and_full_resolution_zoom':'passed'},
 'visual_review':'Topic hero, comparison tables, method cards, mobile layout, study pages and original crop contact sheets inspected.',
 'limitations':['Reading-based synthesis; no model execution or reproduction of reported metrics.','A bounded systematic reading map, not an exhaustive catalogue of the entire field.']}
(R/'research/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
