from pathlib import Path
import json,re,html,importlib.util
R=Path(__file__).resolve().parents[1]
META=[
 ('A01','dust3r','DUSt3R','Geometric 3D Vision Made Easy','共同坐标系中的 pointmap，重写两图几何接口。','2023.12 · CVPR 2024','两张 RGB；无需相机参数','两张共同参考系点图 + 置信度','两图前馈；多图另需全局对齐','从两图回归理解 pointmap'),
 ('A06','vggt','VGGT','Visual Geometry Grounded Transformer','把整组图像放进一个网络，共享几何推理。','2025.03 · CVPR 2025','单张或多张 RGB','相机、深度、点图、跟踪特征','联合前馈；可选 BA 与查询跟踪','从成对几何走向多视骨干'),
 ('A08','pi3','π³','Permutation-Equivariant Visual Geometry Learning','让每张图平等地参与几何推断。','2025.07 · ICLR 2026','无序 RGB 图像集合','局部点图、相机、置信度','前馈；整体坐标与尺度有自由度','取消固定参考视图的特权'),
 ('A09','mapanything','MapAnything','Universal Feed-Forward Metric 3D Reconstruction','将部分已知的几何，变成统一重建的条件。','2025.09 · arXiv','RGB + 可选射线／位姿／深度','射线、ray-depth、相机、metric scale','条件式多视前馈','形状、相机、尺度与条件输入'),
 ('A10','depth-anything-3','Depth Anything 3','Recovering the Visual Space from Any Views','复用完整的预训练骨干，以 depth-ray 组织空间。','2025.11 · arXiv','单图／多图；可选相机条件','depth-ray；实用 camera head','前馈；metric／GS 需区分变体','紧凑表示与教师监督的交点'),
 ('A12','vggt-omega','VGGT-Ω','原文标题：VGGT-Ω · 架构、数据与训练规模','让架构更易训练，把预算用于模型与数据。','2026.05 · CVPR 2026','多张 RGB；无需输入相机','深度、相机；可复用场景 tokens','前馈；部分 register attention','保留几何监督，减少稠密读出')
]
E={e['id']:e for e in json.loads((R/'catalogue.json').read_text(encoding='utf-8'))}
FM=json.loads((R/'research/figure-manifest.json').read_text(encoding='utf-8'))
FIG={(f['slug'],f['key']):f for f in FM}
esc=html.escape

def enhance_base():
 p=R/'research/build_html.py';s=p.read_text(encoding='utf-8')
 s=s.replace('<link rel="stylesheet" href="{prefix}assets/style.css"></head><body id="top">','<link rel="stylesheet" href="{prefix}assets/style.css"><link rel="stylesheet" href="{prefix}assets/editorial.css"></head><body id="top" class="{active}-page"><div class="reading-progress" aria-hidden="true"></div>')
 s=s.replace('<script src="{prefix}assets/app.js"></script></body>','<script src="{prefix}assets/app.js"></script><script src="{prefix}assets/reading.js"></script></body>')
 s=s.replace('2026.10.24 · 第一阶段','2026.10.24 · 研究阅读')
 s=s.replace('本次交付为清单审查、总览与一个完整样章。其余专题已有归属与阅读问题，正文待样章反馈后展开。','清单审查、总览、专题样章与六篇独立论文精读。其余专题已有归属与阅读问题，正文待展开。')
 if 'class="mobile-toc"' not in s:
  pos=s.index(" return f'''<!doctype html>")
  s=s[:pos]+" if toc:body=body.replace('</header>','</header><details class=\"mobile-toc\"><summary>本页目录</summary><div>'+''.join(f'<a href=\"#{i}\">{esc(t)}</a>' for i,t in toc)+'</div></details>',1)\n"+s[pos:]
 # The overview retains its topic discussion links and adds reusable study links.
 if "study_pages={'A01'" not in s:
  pos=s.index(" return f'''<details class=\"paper\"")
  s=s[:pos]+" study_pages={'A01':'dust3r','A06':'vggt','A08':'pi3','A09':'mapanything','A10':'depth-anything-3','A12':'vggt-omega'}\n if e['id'] in study_pages:deep+=f'<p class=\"read-next\"><a href=\"papers/{study_pages[e[\"id\"]]}.html\">独立论文精读 · 原图、方法与实验 →</a></p>'\n"+s[pos:]
 p.write_text(s,encoding='utf-8')

def figure(slug,key):
 f=FIG[(slug,key)]
 return f'''<figure class="figure-plate {'narrow' if f['width']/f['height']<1.6 else ''}" id="figure-{key}"><div class="figure-heading"><span><span class="fig-number">{f['label'].upper()}</span> &nbsp; {f['title']}</span><a href="../{f['pdf']}#page={f['page']}">原文 p.{f['page']} ↗</a></div><button class="figure-open" data-title="{esc(slug+' · '+f['label'])}" aria-label="放大 {esc(f['label']+' '+f['title'])}"><img src="../{f['image']}" width="{f['width']}" height="{f['height']}" loading="eager" alt="{esc(slug+' 原论文 '+f['label']+'：'+f['title'])}"></button><figcaption><strong>读图提示。</strong>{f['reading']}<span class="figure-credit">原论文 {f['label']} · arXiv:{f['version']} · PDF 第 {f['page']} 页 · 原页裁切，保留图表标注；中文解读为本页补充。点击图表可放大，亦可打开原尺寸或原文。</span></figcaption></figure>'''

def improve_chapter():
 p=R/'research/chapter-body.html';s=p.read_text(encoding='utf-8')
 if 'id="paper-studies"' not in s:
  cards=''
  for pid,slug,name,subtitle,thesis,date,inputs,outputs,run,short in META:
   f=FIG[(slug,'architecture')]
   cards+=f'<a class="paper-tile" href="../papers/{slug}.html"><div class="tile-art"><img src="../{f["image"]}" alt="{esc(name)} 原文架构图缩略" loading="lazy"></div><div class="tile-body"><span class="eyebrow">{pid} / PAPER STUDY</span><h3>{name}</h3><p>{short}</p><span class="tile-link">原图 · 方法 · 实验 · 讨论 <span>↗</span></span></div></a>'
  library='<section id="paper-studies"><h2><span class="section-number">COMPANION READINGS</span>六篇骨干，六个独立精读入口</h2><p>本专题负责建立比较框架。需要补论文细节时，进入独立精读页；每页固定提供 motivation、method、training、experiment、discussion，并保留原论文关键图表。其他专题也可直接链接到这些页面和段落。</p><div class="reading-map">'+cards+'</div><div class="intro-note"><strong>两层阅读</strong><span>先沿本页比较设计选择；遇到陌生方法，再跳入原论文精读。图表可放大，公式与图像均支持离线阅读。</span></div></section>'
  s=s.replace('</header>','<div class="reading-rail"><span>专题比较 + 独立论文精读</span><span>·</span><span>主线约 20 分钟</span><button data-reading-size aria-pressed="false">加大字号</button></div></header>'+library,1)
  s=s.replace('<header class="hero">','<div class="breadcrumb"><a href="../index.html">研究地图</a><span>/</span><span>专题 01</span></div><header class="hero">',1)
  s=s.replace('<span class="badge">完整样章</span>','<span class="badge">专题研究</span>')
  for pid,slug,name,*_ in META:
   pattern=r'(<article class="method" id="method-'+pid+r'">.*?</h3>)'
   links=f'<div class="study-links"><a href="../papers/{slug}.html">{name} 独立精读 ↗</a><a href="../papers/{slug}.html#motivation">Motivation</a><a href="../papers/{slug}.html#method">Method</a><a href="../papers/{slug}.html#experiment">Experiment</a><a href="../papers/{slug}.html#discussion">Discussion</a></div>'
   s=re.sub(pattern,lambda m:m[1]+links,s,count=1,flags=re.S)
  s=re.sub(r'<h2>(\d\d) / (.*?)</h2>',lambda m:f'<h2><span class="section-number">SECTION {m[1]}</span>{m[2]}</h2>',s)
  s=s.replace('样章反馈重点：推导深度是否合适；方法卡与专题讨论的比例是否合适；研究假设是否需要更具体到实验变量。其他专题正文将据此展开。','六篇论文精读作为可复用补充页独立维护。后续专题可直接引用各页的 method、experiment、discussion 等段落，不必重复整篇介绍。')
  p.write_text(s,encoding='utf-8')
 # Add the companion section to the generated TOC exactly once.
 p=R/'research/build_html.py';s=p.read_text(encoding='utf-8')
 s=s.replace("toc=[('question','研究问题')","toc=[('paper-studies','六篇论文精读'),('question','研究问题')")
 p.write_text(s,encoding='utf-8')

def build():
 enhance_base();improve_chapter()
 spec=importlib.util.spec_from_file_location('atlas_builder',R/'research/build_html.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 (R/'papers').mkdir(exist_ok=True)
 registry=[]
 for idx,m in enumerate(META):
  pid,slug,name,subtitle,thesis,date,inputs,outputs,run,short=m;e=E[pid]
  content=(R/'research/paper-bodies'/(slug+'.html')).read_text(encoding='utf-8')
  content=re.sub(r'\{\{fig:([^}]+)\}\}',lambda m:figure(slug,m[1]),content)
  content=re.sub(r'\{\{ref:([^}]+)\}\}',lambda m:f'<p class="source-ref">原文依据：<a href="{e["source_url"]}">{esc(m[1])}</a> · <a href="../research/sources/{e["version"]}.pdf">本地 PDF</a></p>',content)
  nfig=sum(f['slug']==slug for f in FM)
  hero=f'''<div class="breadcrumb"><a href="../index.html">研究地图</a><span>/</span><a href="../topics/01-geometry.html#paper-studies">论文精读</a><span>/</span><span>{name}</span></div><header class="hero"><div class="eyebrow">PAPER STUDY {idx+1:02d} / {pid} / {date}</div><h1 class="paper-title">{name}</h1><div class="paper-subtitle">{subtitle}</div><p class="paper-thesis">{thesis}</p><div class="meta"><span class="badge">通用几何 · 以场景观测重建为主</span><span class="badge">{e['version']}</span><span class="badge warm">{nfig} 处原论文图表</span></div><div class="hero-actions"><a class="button" href="#method">从方法开始 ↓</a><a class="button secondary" href="../research/sources/{e['version']}.pdf">打开原论文 ↗</a></div><div class="paper-facts"><div><small>INPUT</small>{inputs}</div><div><small>OUTPUT</small>{outputs}</div><div><small>EXECUTION</small>{run}</div></div><div class="reading-rail"><span>精读导读约 12–18 分钟 · 推导可展开</span><button data-reading-size aria-pressed="false">加大字号</button></div></header>'''
  sources=f'''<section class="paper-section" id="sources"><h2><span class="section-number">SOURCE RECORD</span>原文、版本与复用入口</h2><div class="prose"><p>本文依据 <strong>{e['version']}</strong> 撰写，覆盖动机、主方法、训练、主要实验与讨论。图表从该版本 PDF 原页裁切，图号与页码随图保留；正文中的统一符号推导、反例解释与研究延伸已作区分。未运行模型或复现表格结果。</p><p><a href="{e['source_url']}">arXiv 原文 HTML</a> · <a href="https://arxiv.org/abs/{e['version']}">版本与作者信息</a> · <a href="../research/sources/{e['version']}.pdf">本地完整 PDF</a> · <a href="../{e['source_local']}">本地全文文本</a></p><p class="small muted">固定段落链接：<a href="#motivation">#motivation</a> · <a href="#method">#method</a> · <a href="#training">#training</a> · <a href="#experiment">#experiment</a> · <a href="#discussion">#discussion</a>。可由任何专题引用；<a href="../research/figure-manifest.json">图表来源与裁切记录</a>保留原始版本和坐标。</p></div><div class="study-context">专题关联：<a href="../topics/01-geometry.html#method-{pid}">表示与参考系中的 {name} →</a> · <a href="../index.html#paper-{pid}">总览方法卡</a></div></section>'''
  nxt=META[(idx+1)%len(META)]
  end=f'<nav class="paper-endnav" aria-label="论文阅读导航"><a href="../topics/01-geometry.html#method-{pid}"><small>BACK TO TOPIC</small>返回专题中的方法比较 ↗</a><a href="{nxt[1]}.html"><small>NEXT PAPER</small>{nxt[2]} →</a></nav>'
  toc=[('motivation','01 · 动机与问题'),('method','02 · 方法与表示'),('training','03 · 训练与监督'),('experiment','04 · 实验与证据'),('discussion','05 · 讨论与边界'),('reading','06 · 阅读核对'),('sources','原文与版本记录')]
  page=mod.shell(name+' · 论文精读',hero+content+sources+end,active='study',prefix='../',toc=toc)
  (R/'papers'/(slug+'.html')).write_text(page,encoding='utf-8')
  registry.append({'id':pid,'slug':slug,'title':name,'path':'papers/'+slug+'.html','version':e['version'],'sections':[x[0] for x in toc],'figures':nfig})
 (R/'papers/registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Built six reusable paper studies and refreshed the sample chapter.')

if __name__=='__main__':build()
