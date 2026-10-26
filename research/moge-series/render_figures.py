from pathlib import Path
import json,hashlib
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2]
# Boxes were selected from rendered PDF pages, in top-left normalized coordinates.
PLAN=[
 ('moge-2','2507.02546v1','architecture',4,[.165,.085,.84,.29],'Figure 2'),
 ('moge-2','2507.02546v1','data',5,[.165,.085,.84,.33],'Figure 4'),
 ('moge-2','2507.02546v1','experiment',9,[.16,.08,.85,.255],'Table 4'),
 ('moge-3','2607.17967v2','architecture',4,[.16,.08,.85,.415],'Figure 2'),
 ('moge-3','2607.17967v2','experiment',9,[.16,.74,.85,.925],'Table 3'),
 ('moge-3','2607.17967v2','iterations',9,[.16,.08,.85,.395],'Figure 4'),
]
manifest=[]
for slug,version,key,page,box,label in PLAN:
 p=R/'research/sources'/f'{version}.pdf';doc=pdfium.PdfDocument(p)
 im=doc[page-1].render(scale=3).to_pil().convert('RGB');w,h=im.size
 crop=im.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(box)))
 out=R/'assets/figures'/slug/f'{key}.png';out.parent.mkdir(parents=True,exist_ok=True);crop.save(out)
 manifest.append(dict(slug=slug,key=key,image=out.relative_to(R).as_posix(),version=version,page=page,label=label,box=box,width=crop.width,height=crop.height,source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),image_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),url=f'https://arxiv.org/pdf/{version}#page={page}',operation='Original PDF crop'))
(R/'research/moge-series/figures.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Rendered',len(manifest),'original figures')
