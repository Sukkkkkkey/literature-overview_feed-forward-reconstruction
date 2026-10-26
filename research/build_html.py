from pathlib import Path
import json,html,re
R=Path(__file__).resolve().parents[1]
DATA=json.loads((R/'catalogue.json').read_text(encoding='utf-8'))
E={x['id']:x for x in DATA}
TOPICS=[
('01','通用多视几何：表示与参考系','把形状、相机、尺度拆开还是共同预测？参考视图特权怎样影响学习？','DUSt3R → VGGT → π³ → MapAnything / DA3 → VGGT-Ω'),
('02','单目先验、尺度与条件输入','哪些几何量可从观测约束，哪些来自数据先验？已知信息如何进入网络？','Depth Anything / MoGe → MoGe-2 → MoGe-3；MetricAnything / Pow3R'),
('03','在线重建与长期状态','历史信息存在哪里、如何写入和遗忘？局部误差怎样累积为轨迹漂移？','Spann3R → CUT3R → StreamVGGT / STream3R → LongStream / ABot-Recon'),
('04','计算扩展：稀疏注意力与 TTT','减少 token 交互还是压缩场景状态？复杂度、状态容量与精度如何交换？','Speed3R；VGG-T³ / ZipMap / Scal3R-TTT'),
('05','匹配、SfM 与几何优化后端','学习前端交给后端什么约束？哪些优化仍然必要，哪些可在潜空间中完成？','MVSNet / VGGSfM；MASt3R → Light3R-SfM / MASt3R-SLAM / VGGT-Long'),
('06','动态几何、运动与 4D 查询','逐帧点云、场景流和持续3D轨迹分别解决什么问题？坐标变化与物体运动如何分离？','MonST3R → D4RT / Any4D / 4RC → Point4D'),
('07','可渲染场景与几何证据','从点云到 Gaussian 增加了什么约束？渲染质量何时可能掩盖错误几何？','pixelSplat / MVSplat → Splatt3R / NoPoSplat → AnySplat；4DGT / tttLRM'),
('08','监督、预训练与数据质量','从跨视图预训练到光度自监督，标注成本被消除、转移还是压入教师？','CroCo / CroCo v2 → Gekko；NAS3R / Reliev3R / 特权信息'),
('09','机制理解、可靠性与失败检测','模型用了多少几何对应、多少先验？如何判断某次位姿预测值得信任？','Geometric Understanding；GeoCond；关联各骨干消融'),
('10','物体重建与生成先验','如何从局部观测恢复完整资产？归一化物体、生成视图与实测场景有何不同？','LRM / PF-LRM → TripoSR / LGM / InstantMesh')]
TN={x[0]:x[1] for x in TOPICS};TN['00']='综述导航'
TOPIC_PATHS=dict(zip([t[0] for t in TOPICS],['01-geometry','02-priors','03-streaming','04-scaling','05-backends','06-dynamics','07-rendering','08-supervision','09-reliability','10-objects']))
def esc(s):return html.escape(str(s),quote=True)
def ref(pid,prefix=''):
 e=E[pid];return f'<a href="{prefix}index.html#paper-{pid}">{esc(e["name"])}</a>'
def sources(pid,prefix=''):
 e=E[pid];return f'<a href="{esc(e["source_url"])}">原文 · {esc(e["version"])}</a> · <a href="{prefix}{e["source_local"]}">{"本地核查记录" if e.get("source_note") else "本地全文文本"}</a>'
def shell(title,body,active='index',toc=None,prefix=''):
 nav=f'<a class="{"active" if active=="index" else ""}" href="{prefix}index.html">总览与阅读地图</a><a href="{prefix}index.html#studies">独立论文精读 · 25 篇</a><a class="{"active" if active=="review" else ""}" href="{prefix}review.html">清单审查与证据记录</a>'
 nav+='<details class="topic-switcher"><summary>切换研究专题 · 10</summary>'+''.join(f'<a href="{prefix}topics/{TOPIC_PATHS[i]}.html">{i} · {esc(n.split("：")[0])}</a>' for i,n,_,_ in TOPICS)+'</details>'
 if toc:nav+='<div class="rule"></div>'+''.join(f'<a href="#{i}">{esc(t)}</a>' for i,t in toc)
 if toc:body=body.replace('</header>','</header><details class="mobile-toc"><summary>本页目录</summary><div>'+''.join(f'<a href="#{i}">{esc(t)}</a>' for i,t in toc)+'</div></details>',1)
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="以几何重建为中心的 Feed-forward 3D Reconstruction 文献研究：方法、证据与阅读路径。"><title>{esc(title)} · 3D Research Atlas</title><link rel="stylesheet" href="{prefix}assets/style.css"><link rel="stylesheet" href="{prefix}assets/editorial.css"><link rel="stylesheet" href="{prefix}assets/atlas.css"></head><body id="top" class="{active}-page"><div class="reading-progress" aria-hidden="true"></div><div class="mobile-nav"><a href="{prefix}index.html">总览</a><a href="{prefix}index.html#topics">专题</a><a href="{prefix}review.html">审查记录</a></div><aside class="sidebar"><a class="brand" href="{prefix}index.html">3D Reconstruction<br>研究阅读地图</a><div class="edition">FEED-FORWARD METHODS<br>2026.10.24 · 研究阅读</div><nav>{nav}</nav><div class="rule"></div><p class="note">以几何为中心<br>方法理解为主体<br>研究假设为延伸</p><p class="note">离线可读 · 相对链接<br>原文引用联网访问<br>本地缓存供个人核对</p></aside><main>{body}<footer class="footer">初版核查：2026-10-24 · MoGe 系列更新：2026-10-26 · 10 个研究专题、25 篇独立论文精读、1 个系列比较与 70 项文献索引。<br>“方法与实验要点”表示核对关键段落与评测条件，不表示完成所有公式证明、代码复现或模型实验。原始 Obsidian 笔记保持只读。</footer></main><a class="back-top" href="#top" aria-label="回到顶部">↑ 顶部</a><script src="{prefix}assets/app.js"></script><script src="{prefix}assets/reading.js"></script></body></html>'''
def paper(e):
 topic=e['topic'];tags=f'<span class="badge">{esc(e["scope"])}</span><span class="tag">{esc(TN[topic])}</span>'
 tags+=''.join(f'<span class="tag">交叉：{esc(TN[t])}</span>' for t in e['cross_topics'])
 if e['added']:tags+='<span class="badge warm">本轮补入</span>'
 aliases={'A08':'pi3 pi³ π3','A10':'DA3 depthanything3','A12':'VGGT Omega Ω','C02':'VGG-T3 VGGT3','N10':'DA2 DAV2 depthanythingv2','H03':'MoGe2'}
 key=' '.join([e['id'],e['name'],e['idea'],e['boundary'],e['inputs'],e['execution'],aliases.get(e['id'],'')])
 deep=f'<p class="read-next"><a href="topics/{TOPIC_PATHS[topic]}.html#method-{e["id"]}">进入专题的方法讨论 →</a></p>' if topic in TOPIC_PATHS else ''
 study_pages={'A01':'dust3r','A06':'vggt','A08':'pi3','A09':'mapanything','A10':'depth-anything-3','A12':'vggt-omega'}
 study_pages.update({m['id']:m['slug'] for m in json.loads((R/'research/additional-studies.json').read_text(encoding='utf-8'))})
 study_pages.update({'H02':'moge-1','H03':'moge-2','N13':'moge-3'})
 if e['id'] in study_pages:deep+=f'<p class="read-next"><a href="papers/{study_pages[e["id"]]}.html">独立论文精读 · 原图、方法与实验 →</a></p>'
 return f'''<details class="paper" id="paper-{e['id']}" data-topic="{' '.join([topic]+e['cross_topics'])}" data-scope="{esc(e['scope'])}" data-priority="{e['priority']}" data-keywords="{esc(key.lower())}"><summary><div class="paper-head"><span class="pid">{e['id']}</span><h3>{esc(e['name'])}</h3><span class="tag">{e['date']}</span><span class="badge">{e['priority']}</span></div><p class="short">{esc(e['idea'])}</p></summary><div class="inside"><div class="tags">{tags}</div><p><b>输入与任务：</b>{esc(e['inputs'])}<br><b>运行方式：</b>{esc(e['execution'])}</p><p><b>阅读边界：</b>{esc(e['boundary'])}</p><p><b>实验与证据入口：</b>{esc(e['evidence'])}</p>{deep}<div class="source">{sources(e['id'])}<br>{esc(e['review_level'])} · {esc(e['type'])} · 核查 {e['checked']}</div></div></details>'''
hero='''<header class="hero"><div class="eyebrow">Research atlas / geometry first</div><h1>从图像到几何，<br>沿着方法的分歧阅读。</h1><p class="lead">围绕表示、参考系、状态、计算与监督建立知识结构。先弄清模型究竟预测什么，再判断论文的设计解决了哪一个问题。</p><div class="meta"><span class="badge">场景 / 物体明确区分</span><span class="badge">原文方法与实验核查</span><span class="badge warm">10 个专题 · 25 篇独立精读</span></div><div class="hero-actions"><a class="button" href="topics/01-geometry.html">从表示与参考系开始 →</a><a class="button secondary" href="review.html">查看审查与修订</a></div><div class="stats"><div class="stat"><strong>68</strong><span>方法 / 分析论文</span></div><div class="stat"><strong>10</strong><span>研究专题</span></div><div class="stat"><strong>13</strong><span>本轮补入论文</span></div><div class="stat"><strong>25</strong><span>独立论文精读</span></div></div></header>'''
body=hero+'''<section id="scope"><div class="section-head"><h2>这份地图怎样使用</h2><span class="eyebrow">Read questions, then papers</span></div><div class="steps"><div><b>01 / 把问题说清楚</b>记录输入视图、已知相机、场景或物体、目标输出与推理后端。没有统一设定的分数不放在同一排行榜里。</div><div><b>02 / 沿设计选择比较</b>以专题为主归属，以交叉标签保留联系。同一篇论文可以同时回答表示、效率或监督的问题。</div><div><b>03 / 从证据走向假设</b>先读同论文消融和评测协议，再记录未被排除的解释。研究延伸必须给出能证伪的实验。</div></div><div class="callout"><b>主线范围：</b>从 RGB 直接预测几何的通用模型为中心，向已标定 MVS、SLAM 后端、动态轨迹、可渲染场景和物体生成延伸。原清单 56 项均保留，其中 Pi3X 是工程版本；另补 13 篇论文和 1 篇综述导航，共 70 项（含 2026-10-26 补入的 MoGe-3）。</div><p class="small muted">这是有边界的系统阅读地图，不宣称穷尽该领域。稠密表面细化、语义/语言场、机器人决策与全部生成式资产模型不作本阶段主线。检索截至 2026-10-24。</p></section>'''
body+='<section id="topics"><div class="section-head"><h2>专题地图</h2><span class="small muted">主归属互斥，交叉标签可重叠</span></div><div class="grid">'
for tid,name,q,path in TOPICS:
 count=sum(x['topic']==tid for x in DATA)
 ready=True
 link=f'<a href="topics/{TOPIC_PATHS[tid]}.html">进入专题研究 →</a>'
 body+=f'<article class="card topic {"ready" if ready else ""}" id="topic-{tid}"><div class="num">TOPIC {tid}</div><h3>{name}</h3><p>{q}</p><p class="small">{path}</p><div class="foot">{link}<a href="#library" data-topic-jump="{tid}">{count} 项主归属 · 查看方法卡</a></div></article>'
body+='</div></section><section id="routes"><h2>三条阅读路径</h2>'
for name,ids in [('先建立通用几何框架',['N01','N03','A01','A06','A08','A09','A10','A12']),('再看长程重建的三种答案',['B02','N07','B05','B07','C03','C04','N08']),('最后分清动态、渲染与物体',['E01','N09','E05','E07','F02','F04','H07','N12'])]:
 body+=f'<h4>{name}</h4><div class="path">'+ '<span aria-hidden="true">→</span>'.join(ref(i) for i in ids)+'</div>'
body+='''<p class="small muted">P0 是原清单建议的优先读项，P1 是专题展开与补充；优先级不是论文质量评级。新补入论文暂列 P1，可按研究兴趣提升。</p></section><section id="library"><div class="section-head"><h2>方法卡与来源</h2><span class="small muted">点击卡片展开输入、边界与证据</span></div><div class="filterbar"><div class="filters"><input type="search" id="search" placeholder="搜索方法、表示、输入条件或关键词…" aria-label="搜索文献"><select id="topic-filter" aria-label="筛选专题"><option value="">全部专题（含交叉标签）</option>'''+''.join(f'<option value="{i}">{i} · {n}</option>' for i,n,_,_ in TOPICS)+'''</select><select id="scope-filter" aria-label="筛选场景与物体"><option value="">全部研究对象</option><option>场景</option><option>通用几何</option><option>物体</option><option>物体为主</option><option>综述</option></select><select id="priority-filter" aria-label="筛选优先级"><option value="">全部优先级</option><option>P0</option><option>P1</option><option>P2</option></select></div><div class="filterline"><span id="result-count" aria-live="polite">70 项</span><div><button id="reset-filters">清除筛选</button><button id="expand-visible">展开当前结果</button></div></div></div><div class="paper-list">'''
for e in sorted(DATA,key=lambda e:(e['topic'],e['date'],e['id'])):body+=paper(e)
body+='</div><div class="empty" id="empty">没有匹配项。试试更短的关键词或清除筛选。</div><p class="small muted">标签说明：“通用几何”指跨场景/物体的几何表示或评测范围，不表示两个域具有相同难度或精度；“物体”专题关注归一化资产与不可见表面先验补全。</p></section>'
(R/'index.html').write_text(shell('总览与阅读地图',body,toc=[('topics','专题地图'),('routes','阅读路径'),('library','方法卡与来源')]),encoding='utf-8')

changes=[
('分类结构','原 A–H 同时混合任务、架构、系统和邻接领域。','重组为10专题；每项一个主归属，并添加交叉主题、场景/物体、输入、运行方式标签。','研究组织判断'),
('VGGT：输出与优化','笼统写“输出3D跟踪、一次前馈解决所有任务”会隐藏查询与后端。','输出跟踪特征；查询 tracker 产生2D轨迹。相机表中前馈与 BA 分列。',['A06']),
('π³：不变性','“affine-invariant”易被解释成自由仿射，局部点图易被理解成各自尺度。','相机只确定到全局相似变换；相对位姿消除共同SE(3)，pointmaps与平移共享一个尺度。',['A08']),
('MapAnything / DA3：depth','把 ray-depth 与 z-depth 混用会使几何复现出错。','MapAnything：单位射线×距离；DA3：未单位化射线×z-depth。专题 01 统一推导。',['A09','A10']),
('TTT 与完整流程','“TTT”“无额外训练”“feed-forward”并非一个机制。','区分 fast-weight 内部更新、TTT3R 状态门控、Scal3R-TTT 的块对齐/可选PGO。',['C02','C03','C04','N05']),
('内参与位姿条件','unposed、无需深度标签与完全无需相机信息不同。','NoPoSplat、UFO-4D、PF-LRM 输入内参；MVSplat、4DGT、tttLRM 使用已知相机。',['F04','E06','H08','F02','E03','F07']),
('动态与渲染归属','4D输出可指逐帧几何、运动场、轨迹或可渲染时间表示。','4DGT 主归属可渲染场景、交叉动态；D4RT / Point4D 强调查询与轨迹。',['E03','N09','E07']),
('监督与可靠性','原 G 把训练数据、机制分析和风险判断合在一起。','拆成监督/预训练与机制/可靠性；把先验成本、教师成本和部署成本分开。',['G01','G02','G03','G04','G05']),
('同名和版本','Scal3R 同名；π³、Pi3X 容易混计；PR-LRM 为误写。','两个 Scal3R 以 arXiv ID 区分；Pi3X 为工程更新，不计独立论文；保留 PF-LRM 正名。',['C04','D04','A11','H08']),
('VGGT-Ω','“single head”与“register attention”容易被过度概括。','单一稠密深度头仍配相机头；只替换25%全局注意力，不据此宣称整体线性。',['A12']),
('物体与场景','物体 triplane/Gaussian 和一般场景几何不能统一比较。','独立物体专题；显式区分观测重建、不可见面先验补全与多视扩散生成。',['H07','H08','H09','N11','N12'])]
audit='''<header class="hero"><div class="eyebrow">Review record / evidence boundaries</div><h1>清单审查与修订依据</h1><p class="lead">保留原清单快照，在新的分类与方法卡中修正边界、补足关键过渡。下面记录哪些是原文事实，哪些是本次阅读组织上的判断。</p><div class="meta"><span class="badge">56项原清单保留</span><span class="badge">13篇补入</span><span class="badge warm">68篇论文 + 1工程版本 + 1综述</span></div></header><section id="verdict"><h2>审查结论</h2><p>原清单覆盖了通用几何、长序列、动态和渲染的主要方向，但不足以直接作为章节目录：若沿原分组逐篇展开，容易把“解决什么问题”和“用什么计算结构”混在一起。修订后以研究问题组织专题，保留跨主题关联。</p><p>当前核查深度覆盖原文方法及关键实验设置；25 篇独立精读额外检查表示、训练目标和代表性消融。没有运行模型或复现论文表格。对作者的性能解释，保留其适用协议，不当作跨数据集的普遍结论。</p><div class="callout note"><b>完整性的含义：</b>补齐主线中的关键过渡与反例，而非列出所有衍生模型。语义场、语言对齐、全套扩散式3D生成和传统MVS变种暂列范围之外；后续可按具体研究问题继续增补。</div></section><section id="changes"><h2>主要修订</h2><div class="table-scroll"><table class="wide-table"><thead><tr><th>问题</th><th>需要澄清</th><th>本次处理</th><th>依据</th></tr></thead><tbody>'''
for title,old,new,ids in changes:
 links=' / '.join(ref(i) for i in ids) if isinstance(ids,list) else ids
 audit+=f'<tr><td><b>{title}</b></td><td>{old}</td><td>{new}</td><td>{links}</td></tr>'
audit+='</tbody></table></div></section><section id="additions"><h2>补入13篇：各补哪一段</h2><div class="grid">'
reasons={'N01':'给未知相机直接回归提供已标定几何基线。','N02':'解释 DUSt3R 初始化从何而来。','N03':'把跨视预训练的数据、位置编码与规模变化拆开。','N04':'补足“两两回归—全局大模型”之间的潜空间对齐路线。','N05':'提供理解 TTT 术语差异的必要对照。','N06':'连接跨视补全、共视信息和几何监督成本。','N07':'补齐 VGGT 到因果 KV 缓存的直接过渡。','N08':'补齐长序列分块优化基线，使后续方法比较可理解。','N09':'补齐动态重建的独立查询接口，解释 Point4D 的出发点。','N10':'连接 Depth Anything V1 与 DA3 的教师/数据路线。','N11':'补齐单图 LRM 到直接网格资产的工程方法。','N12':'区分生成多视图、可微网格和真实观测重建。','N13':'补齐 MoGe 系列：从相对几何和尺度/标签改良，推进到稀疏几何邻域细化。'}
for e in DATA:
 if e['id'] in reasons:audit+=f'<article class="card"><div class="eyebrow">{e["id"]} / TOPIC {e["topic"]}</div><h3>{ref(e["id"])}</h3><p>{reasons[e["id"]]}</p><p class="small muted">{esc(e["evidence"])}</p></article>'
audit+='</div></section><section id="coverage"><h2>逐项归属与核查记录</h2><p class="small muted">A–H 编号保持与原清单对应；N01–N12 为本轮补入，S01 为综述导航。“原文”保留版本号（可识别时）；本地文本与源文件 SHA-256 见数据文件。来源已获取不等于逐行精读。</p><div class="table-scroll"><table class="audit-table"><thead><tr><th>编号 / 方法</th><th>主归属</th><th>输入 / 执行边界</th><th>核查入口</th></tr></thead><tbody>'
for e in sorted(DATA,key=lambda x:x['id']):
 audit+=f'<tr><td>{e["id"]}<br>{ref(e["id"])}</td><td>{e["topic"]} · {TN[e["topic"]]}<br><span class="badge">{e["scope"]}</span></td><td>{esc(e["inputs"])}<br><span class="muted">{esc(e["execution"])}</span></td><td>{esc(e["evidence"])}<br><span class="small">{sources(e["id"])}</span></td></tr>'
audit+='''</tbody></table></div></section><section id="provenance"><h2>来源与更新约定</h2><p>优先使用 arXiv 原文与作者仓库。MASt3R 网页转换只有附录，已补读 PDF 正文；4DGT 同时核对 PDF 的方法、实验页。工程条目 Pi3X 只引用官方说明，不为它补造独立实验。</p><p>日期按 arXiv 首次编号月份展示，修订版本另记。原始阅读地图保持原样；新的索引与数据文件构成此次审查结果。离线正文、公式、图示和筛选不依赖 CDN；外部论文链接点击后才联网。</p><p><a href="catalogue.json">查看结构化清单</a> · <a href="research/source-manifest.json">来源快照与 SHA-256</a> · <a href="Feed-Forward-3D-Reconstruction-阅读地图-2026-10-24.md">原始清单快照</a></p><div class="callout"><b>阅读结构：</b>10 个专题沿用研究问题、统一记号、设计比较、方法卡、实验条件、失败边界与可证伪假设。25 篇骨干精读提供独立段落链接、原论文关键图表和版本记录。新增结论应先回到固定版本原文核对，再更新方法卡与关联专题。</div></section>'''
(R/'review.html').write_text(shell('清单审查',audit,active='review',toc=[('changes','主要修订'),('additions','补入理由'),('coverage','逐项核查'),('provenance','来源与更新约定')]),encoding='utf-8')

chapter=(R/'research/chapter-body.html').read_text(encoding='utf-8')
def replace_ref(m):return ref(m[1],'../')
chapter=re.sub(r'\{\{ref:([A-Z]\d\d)\}\}',replace_ref,chapter)
chapter=re.sub(r'\{\{sources:([A-Z]\d\d)\}\}',lambda m:sources(m[1],'../'),chapter)
(R/'topics').mkdir(exist_ok=True)
(R/'topics/01-geometry.html').write_text(shell('通用多视几何：表示与参考系',chapter,active='chapter',prefix='../',toc=[('question','研究问题与答案'),('notation','统一记号'),('gauge','参考系实验'),('methods','设计选择与取舍'),('evidence','实验观察与结论'),('method-cards','六篇骨干方法卡'),('paper-studies','独立论文精读'),('hypotheses','研究延伸：待验证'),('reading','阅读与核对清单')]),encoding='utf-8')
print('Built index.html, review.html, topics/01-geometry.html')
