from pathlib import Path
from html.parser import HTMLParser
import concurrent.futures as cf
import hashlib, json, re, time, urllib.request, urllib.error

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'research' / 'sources'
SOURCES.mkdir(parents=True, exist_ok=True)
class Reader(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0; self.math=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in ('script','style'): self.skip+=1
        if tag=='math':
            self.math+=1
            if self.math==1: self.parts.append(' '+a.get('alttext','[math]')+' ')
        if not self.skip and not self.math:
            if tag in ('p','h1','h2','h3','h4','h5','h6','section','tr','li','figcaption'): self.parts.append('\n')
            if tag in ('td','th'): self.parts.append(' | ')
    def handle_endtag(self,tag):
        if tag in ('script','style'): self.skip=max(0,self.skip-1)
        if tag=='math': self.math=max(0,self.math-1)
        if tag in ('p','h1','h2','h3','h4','h5','h6','tr','li','figcaption'): self.parts.append('\n')
    def handle_data(self,d):
        if not self.skip and not self.math: self.parts.append(d)
    def text(self):
        return '\n'.join(re.sub(r'\s+',' ',x).strip() for x in ''.join(self.parts).split('\n') if x.strip())

md=next(ROOT.glob('Feed-Forward*2026-10-24.md')).read_text(encoding='utf-8')
entries=[]
for ln in md.splitlines():
    if not re.match(r'^\| [A-H]\d\d ·',ln): continue
    cells=[x.strip() for x in ln.strip('|').split('|')]
    link=re.search(r'\[([^]]+)\]\(([^)]+)\)',cells[1])
    aid=re.search(r'arxiv.org/(?:abs|html)/(\d{4}\.\d+)',link[2])
    entries.append(dict(id=cells[0].split()[0],priority=cells[0].split()[-1],name=link[1],url=link[2],arxiv=aid[1] if aid else None,original_meta=cells[1],original_idea=cells[2],original_boundary=cells[3]))
for e in entries:
    if e['id']=='D01': e['arxiv']='2312.04563'
new=[('N01','MVSNet','1804.02505'),('N02','CroCo','2210.10716'),('N03','CroCo v2','2211.10408'),('N04','Light3R-SfM','2501.14914'),('N05','TTT3R','2509.26645'),('N06','Gekko','2609.01530'),('S01','Feed-Forward 3D Scene Modeling: A Problem-Driven Perspective','2604.14025')]
entries += [dict(id=i,name=n,arxiv=a,url='https://arxiv.org/abs/'+a,priority='P1',addition_candidate=True) for i,n,a in new]
(ROOT/'research'/'catalogue-seed.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (personal academic literature review)'})
    with urllib.request.urlopen(req,timeout=40) as r: return r.read(),r.geturl()
def fetch(e):
    key=e['arxiv'] or e['id']; tp=SOURCES/(key+'.txt'); hp=SOURCES/(key+'.html')
    result={'id':e['id'],'name':e['name'],'arxiv':e['arxiv'],'checked':'2026-10-24'}
    if tp.exists() and tp.stat().st_size>4000:
        result.update(status='cached',text_file=str(tp.relative_to(ROOT)),characters=len(tp.read_text(encoding='utf-8'))); return result
    try:
        url='https://arxiv.org/html/'+e['arxiv'] if e['arxiv'] else 'https://raw.githubusercontent.com/yyfz/Pi3/main/README.md'
        b,final=get(url)
        if e['arxiv']:
            p=Reader(); p.feed(b.decode('utf-8','replace')); text=p.text()
            if len(text)<7000: raise ValueError('HTML not a full paper')
            hp.write_bytes(b)
        else: text=b.decode('utf-8','replace')
        tp.write_text(text,encoding='utf-8'); result.update(status='fulltext-html' if e['arxiv'] else 'official-readme',url=final,text_file=str(tp.relative_to(ROOT)),characters=len(text),sha256=hashlib.sha256(b).hexdigest())
    except Exception as ex:
        result['html_error']=str(ex)
        if e['arxiv']:
            try:
                from pypdf import PdfReader
                b,final=get('https://arxiv.org/pdf/'+e['arxiv']); pp=SOURCES/(key+'.pdf'); pp.write_bytes(b)
                reader=PdfReader(pp); text='\n\n'.join(f'[PDF page {i+1}]\n'+(p.extract_text() or '') for i,p in enumerate(reader.pages))
                tp.write_text(text,encoding='utf-8'); result.update(status='fulltext-pdf',url=final,text_file=str(tp.relative_to(ROOT)),characters=len(text),pages=len(reader.pages),sha256=hashlib.sha256(b).hexdigest())
            except Exception as exc: result.update(status='unavailable',error=str(exc))
        else: result.update(status='unavailable',error=str(ex))
    return result
results=[]
with cf.ThreadPoolExecutor(max_workers=3) as pool:
    for r in pool.map(fetch,entries):
        results.append(r)
        (ROOT/'research'/'source-manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
        print(r['id'],r['status'],r.get('characters',0),flush=True)
print('DONE',len(results),flush=True)
