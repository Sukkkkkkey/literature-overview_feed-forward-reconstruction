"""MoGe series studies; called by build_complete.py, with no PDF/runtime dependency."""
from pathlib import Path
import html,json,re,math
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1]
S=R/'research/moge-series'
PAPERS=[
 dict(id='H02',slug='moge-1',name='MoGe',version='2410.19115v3',date='2024-10',
 title='MoGe: Unlocking Accurate Monocular Geometry Estimation for Open-Domain Images with Optimal Training Supervision',
 authors='Ruicheng Wang¹* · Sicheng Xu² · Cassie Dai³* · Jianfeng Xiang⁴* · Yu Deng² · Xin Tong² · Jiaolong Yang²†',
 affiliations='¹ USTC · ² Microsoft Research · ³ Harvard · ⁴ Tsinghua University',
 notes='* 工作完成于 Microsoft Research 实习期间；† 通讯作者。单位依固定 PDF 署名。',
 publication='已发表 · CVPR 2025',publication_url='https://openaccess.thecvf.com/content/CVPR2025/html/Wang_MoGe_Unlocking_Accurate_Monocular_Geometry_Estimation_for_Open-Domain_Images_with_CVPR_2025_paper.html',
 project='https://wangrc.site/MoGePage/',model='https://huggingface.co/Ruicheng/moge-vitl',demo='https://huggingface.co/spaces/Ruicheng/MoGe',
 abstract='We present MoGe, a powerful model for recovering 3D geometry from monocular open-domain images. Given a single image, our model directly predicts a 3D point map of the captured scene with an affine-invariant representation, which is agnostic to true global scale and shift. This new representation precludes ambiguous supervision in training and facilitates effective geometry learning. Furthermore, we propose a set of novel global and local geometry supervision techniques that empower the model to learn high-quality geometry. These include a robust, optimal, and efficient point cloud alignment solver for accurate global shape learning, and a multi-scale local geometry loss promoting precise local geometry supervision. We train our model on a large, mixed dataset and demonstrate its strong generalizability and high accuracy. In our comprehensive evaluation on diverse unseen datasets, our model significantly outperforms state-of-the-art methods across all tasks, including monocular estimation of 3D point map, depth map, and camera field of view. Code and models can be found on our project page.',
 abstract_page=2,license='CC BY 4.0',question='相对几何：怎样消除监督中的歧义？',figures=2),
 dict(id='H03',slug='moge-2',name='MoGe-2',version='2507.02546v1',date='2025-07',
 title='MoGe-2: Accurate Monocular Geometry with Metric Scale and Sharp Details',
 authors='Ruicheng Wang¹* · Sicheng Xu² · Yue Dong² · Yu Deng² · Jianfeng Xiang³* · Zelong Lv¹* · Guangzhong Sun¹ · Xin Tong² · Jiaolong Yang²†',
 affiliations='¹ USTC · ² Microsoft Research · ³ Tsinghua University',
 notes='* 工作完成于 Microsoft Research 实习期间；† 通讯作者。',
 publication='已发表 · NeurIPS 2025',publication_url='https://papers.nips.cc/paper_files/paper/2025/hash/336572db3e99930814d6b328d4220cb6-Abstract-Conference.html',doi='10.52202/085713-1207',
 project='https://wangrc.site/MoGe2Page/',model='https://huggingface.co/Ruicheng/moge-2-vitl',demo='https://huggingface.co/spaces/Ruicheng/MoGe-2',
 abstract='We propose MoGe-2, an advanced open-domain geometry estimation model that recovers a metric scale 3D point map of a scene from a single image. Our method builds upon the recent monocular geometry estimation approach, MoGe [61], which predicts affine-invariant point maps with unknown scales. We explore effective strategies to extend MoGe for metric geometry prediction without compromising the relative geometry accuracy provided by the affine-invariant point representation. Additionally, we discover that noise and errors in real data diminish fine-grained detail in the predicted geometry. We address this by developing a unified data refinement approach that filters and completes real data from different sources using sharp synthetic labels, significantly enhancing the granularity of the reconstructed geometry while maintaining the overall accuracy. We train our model on a large corpus of mixed datasets and conducted comprehensive evaluations, demonstrating its superior performance in achieving accurate relative geometry, precise metric scale, and fine-grained detail recovery – capabilities that no previous methods have simultaneously achieved.',
 abstract_page=1,license='CC BY 4.0',question='尺度与标签：怎样兼得米制几何和细节？',figures=3),
 dict(id='N13',slug='moge-3',name='MoGe-3',version='2607.17967v2',date='2026-07',
 title='MoGe-3: Fine-Detail Monocular Geometry Estimation with Self-Guided Sparse Volumetric Refinement',
 authors='Lingyu Kong¹˒³*‡ · Ruicheng Li¹˒³*‡ · Ruicheng Wang²˒³*‡ · Sicheng Xu³ · Chengtang Yao³ · Jianfeng Xiang¹˒³‡ · Jiaolong Yang³†',
 affiliations='¹ Tsinghua University · ² USTC · ³ Microsoft Research',
 notes='* 共同第一作者；‡ 工作完成于 Microsoft Research 实习期间；† 通讯作者。标记含义依 PDF，符号为便于阅读统一。',
 publication='预印本版本 · 作者页称 NeurIPS 2026 接收',publication_url='https://qft-333.github.io/moge3page/',
 publication_note='会议官方记录未核实；本页的方法、图表与数值均固定于 arXiv v2，不将作者项目页表格混入 PDF 消融。',
 project='https://qft-333.github.io/moge3page/',model='https://huggingface.co/Ruicheng/moge-3-vitl',demo='https://huggingface.co/spaces/Ruicheng/MoGe-3',
 abstract='Monocular geometry estimation has recently achieved impressive performance across diverse scenes.',
 abstract_page=1,license='arXiv non-exclusive distribution license',excerpt=True,question='几何邻域：怎样让细结构在 3D 中成立？',figures=3)
]
CAPTIONS={
 ('moge-1','architecture'):('点图先预测，相机随后恢复','沿输出看 pointmap 与 mask；右侧深度、焦距需要后续恢复。训练框中的全局/局部损失不等同于推理步骤。'),
 ('moge-1','experiment'):('同一小模型中的表示与监督消融','先区分各列对齐自由度，再看 ROE scale-inv.、affine-inv. 和 Full；局部收益不能替代尺度评价，截断的收益也非每列单调。'),
 ('moge-2','architecture'):('相对点图与全局尺度分支分离','黄色分支恢复稠密形状，绿色 MLP 从 CLS token 估计全局尺度。新增分支使用全局表征，并未加入真实尺度观测。'),
 ('moge-2','data'):('从错位真实标签到受约束的补全','由左到右比较原标签、过滤和补全：上排是 SfM 缺失，下排是 LiDAR/图像错位。真实边界深度与教师局部梯度承担不同职责。'),
 ('moge-2','experiment'):('把尺度头和数据改良分别消融','上半表比较尺度预测设计，下半表比较训练数据，均为 ViT-B。重点同时看右端 F1 与 metric depth Rel，避免只读变绿的一列。'),
 ('moge-3','architecture'):('每轮预测几何，重新决定稀疏邻域','上方循环重新体素化；下方瓶颈注入 2D 特征。留意 Feat 与 Coord 是不同量，输出是 log-depth 残差。'),
 ('moge-3','experiment'):('冻结基座后的参数匹配对照','2D Conv. 与 D=200 的差距支持稀疏几何邻域；同时检查 metric depth 的退步。这是测试 5 步的冻结基座实验，不是主表的联合训练 3 步模型。'),
 ('moge-3','iterations'):('先有联合训练收益，再有迭代细化收益','K=0 的六边形为原 MoGe-2，实线起点为联合训练后的基座。多数局部收益集中在前几步，不能据曲线声称无限迭代收敛。')
}
TOC=[('abstract','Abstract'),('method','方法与训练'),('experiment','实验与证据'),('discussion','讨论与边界'),('reading','阅读核对'),('sources','原文与版本')]

# Same fixed editorial estimator as the paper-to-html skill; bundled here so the
# atlas build remains portable without a user-specific skill installation.
class Reading(HTMLParser):
 def __init__(self,s):
  super().__init__();self.stack=[];self.parts=[];self.visuals=0;self.equations=0;self.feed(s)
 def handle_starttag(self,t,a):
  d=dict(a);p=self.stack[-1] if self.stack else (None,False,False,False,False)
  main=t=='main' or p[1];cl=d.get('class','').split();ignore=p[2] or t in ['nav','button','footer','script','style','dialog'] or d.get('id')=='sources' or 'reading-time' in cl
  eq='equation' in cl or 'math-line' in cl
  if main and not ignore:
   if t in ['figure','img','svg','table'] and not p[3]:self.visuals+=1
   if eq and not p[4]:self.equations+=1
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append((t,main,ignore,p[3] or t=='figure',p[4] or eq))
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==t:del self.stack[i:];break
 def handle_data(self,s):
  if self.stack and self.stack[-1][1] and not self.stack[-1][2]:self.parts.append(s)

def timed(doc,slug):
 p=Reading(doc);text=' '.join(p.parts);cjk=r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0002fa1f]'
 chars=len(re.findall(cjk,text));words=len(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[’'\-][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*",re.sub(cjk,' ',text)))
 extra=.5 if slug!='moge' else 0
 minutes=chars/350+words/160+p.visuals*.5+p.equations*.25+extra
 report=dict(cjk_characters=chars,latin_words_and_numbers=words,figures_and_tables=p.visuals,equation_blocks=p.equations,extra_minutes=extra,extra_reason='原表含多种对齐协议；额外预留辨读时间' if extra else '',estimated_minutes=round(minutes,2),budget_minutes=10,passed=minutes<=10)
 if minutes>10:raise ValueError(f'{slug}: reading budget exceeded: {minutes:.2f}')
 (S/f'{slug}-reading.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 doc=doc.replace('READING_TIME',f'预估阅读约 {math.ceil(minutes)} 分钟')
 return doc.replace('</head>',f'<meta name="paper-reading-budget-minutes" content="10"><meta name="paper-reading-extra-minutes" content="{extra}"><meta name="paper-reading-extra-reason" content="原表含多种对齐协议；额外预留辨读时间"><link rel="stylesheet" href="../assets/moge-series.css"></head>')

def build(atlas):
 esc=html.escape
 fm=json.loads((R/'research/figure-manifest.json').read_text(encoding='utf-8'))
 new=json.loads((S/'figures.json').read_text(encoding='utf-8'))
 figmap={(f['slug'],f['key']):f for f in fm+new}
 def figure(slug,key):
  f=figmap[('moge' if slug=='moge-1' else slug,key)];title,reading=CAPTIONS[slug,key]
  return f'''<figure class="figure-plate" id="fig-{key}" data-source-version="{f['version']}" data-source-locator="{f['label']}; PDF physical p.{f['page']}"><div class="figure-heading"><span class="fig-number">{f['label']} · {title}</span><a href="https://arxiv.org/pdf/{f['version']}#page={f['page']}">原论文 p.{f['page']} ↗</a></div><button class="figure-open" data-title="{title}" aria-label="放大：{title}"><img src="../{f['image']}" alt="{esc(title+'。'+reading)}" width="{f['width']}" height="{f['height']}" loading="lazy"></button><figcaption>{reading}<span class="figure-credit">原图裁切 · {f['version']} · {f['label']} · PDF 物理页 {f['page']} · 著作权归原作者。</span></figcaption></figure>'''
 def tabs(active):return '<nav class="series-tabs" aria-label="MoGe 系列阅读">'+''.join(f'<a href="{s}.html"'+(' aria-current="page"' if s==active else '')+f'>{n}</a>' for s,n in [('moge','系列比较')]+[(m['slug'],m['name']) for m in PAPERS])+'</nav>'
 records=[]
 for m in PAPERS:
  slug=m['slug'];version=m['version'];pdf=f'https://arxiv.org/pdf/{version}'
  links=[('Paper',f'https://arxiv.org/abs/{version}'),('PDF',pdf),('Project',m['project']),('Code','https://github.com/microsoft/MoGe'),('Weights',m['model']),('Demo',m['demo'])]
  hero=f'''<div class="breadcrumb"><a href="../index.html">研究地图</a><span>/</span><a href="moge.html">MoGe 系列</a><span>/</span>{m['name']}</div><header class="hero"><div class="eyebrow">MOGE SERIES / {m['id']} / ORIGINAL PAPER STUDY</div><h1 class="paper-title">{m['name']}</h1><div class="paper-subtitle">{esc(m['title'])}</div><div class="paper-identity"><p>{m['authors']}</p><p>{m['affiliations']}</p><p class="small muted">{m['notes']}</p></div><div class="meta"><span class="badge"><a href="{m['publication_url']}">{m['publication']}</a></span><span class="badge">{version}</span><span class="badge warm reading-time">READING_TIME</span></div><div class="resource-links">'''+''.join(f'<a href="{u}">{label} ↗</a>' for label,u in links)+f'''</div>{'<p class="small muted">'+m['publication_note']+'</p>' if m.get('publication_note') else ''}<div class="reading-rail"><span>单图可见表面 · 关键原图可放大</span><button data-reading-size aria-pressed="false">加大字号</button></div></header>'''
  abstract=f'''<section class="paper-section abstract-section" id="abstract"><h2><span class="section-number">ORIGINAL ABSTRACT</span>Abstract{' · 原文节选' if m.get('excerpt') else ''}</h2><div class="abstract-text" lang="en"><p>{esc(m['abstract'])}</p></div><p class="source-ref">{version} · Abstract · PDF 物理页 {m['abstract_page']} · {'仅展示原文节选；' if m.get('excerpt') else ''}<a href="{pdf}#page={m['abstract_page']}">阅读完整原文</a> · {m['license']}</p></section>'''
  content=(S/f'{slug}.html').read_text(encoding='utf-8')
  content=re.sub(r'\{\{fig:([^}]+)\}\}',lambda x:figure(slug,x[1]),content)
  content=re.sub(r'\{\{ref:([^}]+)\}\}',lambda x:f'<p class="source-ref">原文依据：{x[1]} · <a href="{pdf}">固定版本 PDF ↗</a></p>',content)
  sources=f'''<section class="paper-section" id="sources"><h2><span class="section-number">SOURCE RECORD</span>版本、依据与复用</h2><p>核查：2026-10-26。方法、公式与表格固定于 <a href="{pdf}">{version}</a>；首次预印本 {m['date']}，发表状态见 <a href="{m['publication_url']}">正式记录 / 作者声明</a>。正文与技术附录已纳入取舍记录，未运行模型复现。</p>{'<p>正式 DOI：<a href="https://doi.org/'+m['doi']+'">'+m['doi']+'</a></p>' if m.get('doi') else ''}<p><a href="../research/moge-series/sources.json">PDF 版本与 SHA-256</a> · <a href="../research/moge-series/coverage.json">章节覆盖与取舍</a> · <a href="../research/moge-series/review.json">事实与阅读自审</a> · <a href="../research/moge-series/figures.json">新增图表来源</a></p><p>相关专题：<a href="../topics/02-priors.html">单目先验、尺度与条件输入</a> · <a href="moge.html">三代方法比较</a>。文中的“本页判断”属于研究分析；图表与原始数值属于作者报告。</p></section>'''
  doc=atlas.shell(m['name']+' · 原始论文精读',hero+tabs(slug)+abstract+content+sources+tabs(slug),active='study',prefix='../',toc=TOC)
  (R/'papers'/f'{slug}.html').write_text(timed(doc,slug),encoding='utf-8')
  records.append(dict(id=m['id'],slug=slug,title=m['name'],path=f'papers/{slug}.html',version=version,sections=['abstract','motivation','method','training','experiment','discussion','reading','sources'],figures=m['figures'],topics=['02']))
 cards='<div class="reading-map moge-cards">'
 for m in PAPERS:
  f=figmap[('moge' if m['slug']=='moge-1' else m['slug'],'architecture')]
  cards+=f'''<a class="paper-tile" href="{m['slug']}.html"><div class="tile-art"><img src="../{f['image']}" alt="{m['name']} 原论文架构图缩略图" loading="lazy"></div><div class="tile-body"><span class="eyebrow">{m['date']} / {m['version']}</span><h3>{m['name']}</h3><p>{m['question']}</p><span class="tile-link">独立精读 · 方法 / 实验 / 讨论 ↗</span></div></a>'''
 cards+='</div>'
 body=(S/'moge.html').read_text(encoding='utf-8').replace('{{cards}}',cards)
 # Preserve figure anchors from the former standalone MoGe page as explicit links.
 body+='<div class="legacy-links"><span id="figure-architecture"></span><a id="fig-architecture" href="moge-1.html#fig-architecture">MoGe 原架构图 ↗</a> · <span id="figure-experiment"></span><a id="fig-experiment" href="moge-1.html#fig-experiment">MoGe 原消融表 ↗</a> · <span id="figure-ambiguity"></span><a id="fig-ambiguity" href="https://arxiv.org/pdf/2410.19115v3#page=4">MoGe 歧义示意图 ↗</a></div>'
 hero='''<div class="breadcrumb"><a href="../index.html">研究地图</a><span>/</span><a href="../topics/02-priors.html">单目先验与尺度</a><span>/</span>MoGe 系列</div><header class="hero"><div class="eyebrow">SERIES STUDY / 2024 → 2026 / THREE PAPERS</div><h1 class="paper-title">MoGe 系列</h1><p class="paper-thesis">相对形状 → 米制尺度 → 几何细节</p><p class="lead">沿着监督、数据与空间邻域，理解三代方法怎样逐步改善单目几何。</p><div class="meta"><span class="badge">3 篇独立论文</span><span class="badge">1 个系列比较入口</span><span class="badge warm reading-time">READING_TIME</span></div></header>'''
 sources='<section class="paper-section" id="sources"><h2><span class="section-number">SOURCES / CHECKED 2026-10-26</span>固定版本与发表记录</h2>'+''.join(f'<p><a href="{m["slug"]}.html#sources">{m["name"]} 来源记录</a> · <a href="https://arxiv.org/abs/{m["version"]}">{m["version"]}</a> · <a href="{m["publication_url"]}">{m["publication"]}</a></p>' for m in PAPERS)+'<p>MoGe-3 的 NeurIPS 2026 接收信息来自作者项目页，会议官方记录未核实。图表、公式和数值以所列 PDF 为准。</p><p><a href="../research/moge-series/coverage.json">覆盖与取舍</a> · <a href="../research/moge-series/review.json">自审记录</a>。所有正文与图表离线可读；原论文与代码入口需联网。</p></section>'
 toc=[('motivation','系列主线'),('method','方法比较'),('training','监督与数据'),('experiment','证据与协议'),('discussion','讨论与边界'),('reading','阅读路径'),('sources','版本与来源')]
 (R/'papers/moge.html').write_text(timed(atlas.shell('MoGe 系列 · 三篇论文的方法研究',hero+tabs('moge')+body+sources,active='study',prefix='../',toc=toc),'moge'),encoding='utf-8')
 (S/'papers.json').write_text(json.dumps(PAPERS,ensure_ascii=False,indent=2),encoding='utf-8')
 return records
