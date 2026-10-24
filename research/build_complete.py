"""Build the complete offline atlas from reviewed content and source records."""
from pathlib import Path
import json,re,html
import build_paper_studies as studies
R=Path(__file__).resolve().parents[1]
studies.build()
import build_html as atlas
E=atlas.E;esc=atlas.esc
META=json.loads((R/'research/additional-studies.json').read_text(encoding='utf-8'))
REG=json.loads((R/'papers/registry.json').read_text(encoding='utf-8'))
CORE_TOPICS={'A01':['01','05','08'],'A06':['01','03','04','09'],'A08':['01','04','09'],'A09':['01','02','06'],'A10':['01','02','07','08'],'A12':['01','04','08']}
for e in REG:e['topics']=CORE_TOPICS[e['id']]
OUTPUTS={
 'H02':'相对 pointmap、有效 mask、恢复的焦距与深度','A07':'局部 / 共同参考系点图与相机',
 'B02':'点图、相机、持久状态；可查询几何','N07':'相机、深度、点图与跟踪特征',
 'C02':'相机、深度与压缩的场景权重','C03':'相机、点图及可查询 fast weights',
 'A02':'点图、置信度、局部描述子','E01':'逐时刻几何与优化后的相机轨迹',
 'N09':'按需三维位置、轨迹、深度与相机','F01':'可渲染的 3D Gaussian 集合',
 'F02':'深度与像素对齐 3D Gaussians','N03':'跨视表征；下游 disparity / flow',
 'G02':'相机与可渲染 3D Gaussians','G01':'探针、对应分析与机制干预证据',
 'G04':'位姿风险、精修门控与可选修正','H07':'triplane-NeRF；可额外提取 mesh',
 'N12':'NeRF / Mesh 物体资产（分变体）'}
TOC=[('motivation','01 · 动机与问题'),('method','02 · 方法与表示'),('training','03 · 训练与协议'),('experiment','04 · 实验与证据'),('discussion','05 · 讨论与边界'),('reading','06 · 阅读核对'),('sources','原文与版本记录')]
for idx,m in enumerate(META,7):
 pid=m['id'];slug=m['slug'];e=E[pid];name=m['name'];tid=m['topics'][0];topic=atlas.TOPIC_PATHS[tid]
 content=(R/'research/paper-bodies'/(slug+'.html')).read_text(encoding='utf-8')
 content=re.sub(r'\{\{fig:([^}]+)\}\}',lambda x:studies.figure(slug,x[1]),content)
 content=re.sub(r'\{\{ref:([^}]+)\}\}',lambda x:f'<p class="source-ref">原文依据：{esc(x[1])} · <a href="../research/sources/{e["version"]}.pdf">固定版本 PDF</a> · <a href="{e["source_url"]}">原文 HTML</a></p>',content)
 nfig=sum(f['slug']==slug for f in studies.FM)
 hero=f'''<div class="breadcrumb"><a href="../index.html">研究地图</a><span>/</span><a href="../index.html#studies">独立论文精读</a><span>/</span><span>{name}</span></div><header class="hero"><div class="eyebrow">PAPER STUDY {idx:02d} / {pid} / {e['date']}</div><h1 class="paper-title">{name}</h1><div class="paper-subtitle">{esc(m['subtitle'])}</div><p class="paper-thesis">{m['thesis']}</p><div class="meta"><span class="badge">{e['scope']}</span><span class="badge">{e['version']}</span><span class="badge warm">{nfig} 处原论文图表</span></div><div class="hero-actions"><a class="button" href="#method">从方法开始 ↓</a><a class="button secondary" href="../research/sources/{e['version']}.pdf">打开原论文 ↗</a></div><div class="paper-facts"><div><small>INPUT</small>{esc(e['inputs'])}</div><div><small>OUTPUT</small>{OUTPUTS[pid]}</div><div><small>EXECUTION</small>{esc(e['execution'])}</div></div><div class="reading-rail"><span>精读导读 · 推导可展开 · 原图可放大</span><button data-reading-size aria-pressed="false">加大字号</button></div></header>'''
 context=' · '.join(f'<a href="../topics/{atlas.TOPIC_PATHS[t]}.html">{t} · {atlas.TN[t]}</a>' for t in m['topics'])
 sources=f'''<section class="paper-section" id="sources"><h2><span class="section-number">SOURCE RECORD</span>原文、版本与复用入口</h2><div class="prose"><p>本页依据 <strong>{e['version']}</strong> 的方法、实验与补充材料撰写。图号和页码以该版本 PDF 为准；网页转换的编号可能不同。图表为原页裁切，中文解读、统一符号说明与研究延伸另行标明。未运行模型或复现表中结果。</p><p><a href="{e['source_url']}">arXiv 原文 HTML</a> · <a href="https://arxiv.org/abs/{e['version']}">版本与作者信息</a> · <a href="../research/sources/{e['version']}.pdf">本地完整 PDF</a> · <a href="../{e['source_local']}">本地全文文本</a></p><p class="small muted">固定段落链接：<a href="#motivation">#motivation</a> · <a href="#method">#method</a> · <a href="#training">#training</a> · <a href="#experiment">#experiment</a> · <a href="#discussion">#discussion</a>。<a href="../research/figure-manifest.json">图表版本与裁切记录</a> · <a href="../research/additional-study-sources.json">PDF 来源与 SHA-256</a></p></div><div class="study-context">专题关联：{context} · <a href="../index.html#paper-{pid}">总览方法卡</a></div></section>'''
 end=f'<nav class="paper-endnav" aria-label="论文阅读导航"><a href="../topics/{topic}.html#method-{pid}"><small>BACK TO TOPIC</small>返回专题中的方法比较 ↗</a><a href="../index.html#studies"><small>CONTINUE READING</small>选择下一篇论文精读 →</a></nav>'
 (R/'papers'/(slug+'.html')).write_text(atlas.shell(name+' · 论文精读',hero+content+sources+end,active='study',prefix='../',toc=TOC),encoding='utf-8')
 REG.append(dict(id=pid,slug=slug,title=name,path='papers/'+slug+'.html',version=e['version'],sections=[t[0] for t in TOC],figures=nfig,topics=m['topics']))
(R/'papers/registry.json').write_text(json.dumps(REG,ensure_ascii=False,indent=2),encoding='utf-8')
SR={e['id']:e for e in REG}
QUESTIONS=json.loads((R/'research/method-questions.json').read_text(encoding='utf-8'))
COMPANIONS={'02':['H02','A07','A09','A10'],'03':['B02','N07'],'04':['C02','C03','A12'],'05':['A02','F02'],'06':['E01','N09','B02'],'07':['F01','F02','G02'],'08':['N03','G02','A10'],'09':['G01','G04','A06'],'10':['H07','N12']}
STEPS={
 '02':[('观测约束','图像 / 相机 / 稀疏测量'),('学习先验','相对形状与深度'),('尺度来源','预测 / 条件恢复')],
 '03':[('当前图像','局部可见证据'),('历史状态','读写 / 检索 / 遗忘'),('输出与轨迹','局部误差 → 长程漂移')],
 '04':[('输入 tokens','每图分辨率 × 视图数'),('信息压缩','稀疏选择 / fast weights'),('几何查询','精度 / 延迟 / 容量')],
 '05':[('学习前端','对应 / 点图 / 相对位姿'),('几何约束','三角化 / 对齐 / 回环'),('共同地图','求解与误差修正')],
 '06':[('点的身份','源像素 / 外观特征'),('时间与参考系','目标时刻 ≠ 相机坐标'),('动态输出','几何 / 位移 / 轨迹')],
 '07':[('多视输入','已知或预测相机'),('可渲染表示','位置 / 形状 / 外观'),('双重验证','渲染质量 + 几何误差')],
 '08':[('上游信息','标签 / 配对 / 教师'),('学习信号','补全 / 蒸馏 / 渲染'),('独立验证','迁移 / 消融 / 成本')],
 '09':[('几何预测','误差不一定可见'),('诊断与干预','probe / knockout / 风险'),('决策依据','相信 / 拒绝 / 精修')],
 '10':[('单图观测','可见表面有限'),('物体先验','直接补全 / 生成视图'),('完整资产','可用性 + 忠实度')]}
def table(match):
 rows=[r.strip().split('|') for r in match[1].strip().splitlines() if r.strip()]
 assert all(len(r)==len(rows[0]) for r in rows),rows
 return '<div class="table-scroll"><table class="wide-table"><thead><tr>'+''.join('<th>'+c+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+c+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>'
def tiles(ids):
 cards=[]
 for pid in ids:
  s=SR[pid];f=studies.FIG[(s['slug'],'architecture')]
  cards.append(f'<a class="paper-tile" href="../{s["path"]}"><div class="tile-art"><img src="../{f["image"]}" alt="{esc(s["title"])} 原文方法图" loading="lazy"></div><div class="tile-body"><span class="eyebrow">{pid} / COMPANION STUDY</span><h3>{s["title"]}</h3><p>{esc(E[pid]["idea"])}</p><span class="tile-link">动机 · 方法 · 原图 · 实验 ↗</span></div></a>')
 return '<div class="reading-map">'+''.join(cards)+'</div>'
def card(e):
 pid=e['id'];links=''
 if pid in SR:
  path='../'+SR[pid]['path'];links='<div class="study-links">'+''.join(f'<a href="{path}{anchor}">{label}</a>' for anchor,label in [('', '独立论文精读 ↗'),('#method','Method'),('#experiment','Experiment'),('#discussion','Discussion')])+'</div>'
 cross=' · '.join(f'<a href="{atlas.TOPIC_PATHS[t]}.html">{t} · {atlas.TN[t]}</a>' for t in e['cross_topics'])
 return f'''<article class="method" id="method-{pid}"><div class="method-kicker">{pid} / {e['date']} / {e['priority']}</div><h3>{esc(e['name'])}</h3>{links}<div class="tags"><span class="badge">{e['scope']}</span><span class="tag">{e['type']}</span></div><p class="method-idea">{esc(e['idea'])}</p><div class="method-detail-grid"><div><h4>输入与运行</h4><p>{esc(e['inputs'])}</p><p class="small muted">{esc(e['execution'])}</p></div><div><h4>证据与阅读边界</h4><p>{esc(e['evidence'])}</p><p class="small muted">{esc(e['boundary'])}</p></div></div><div class="method-question"><b>带着问题读：</b>{esc(QUESTIONS[pid])}</div><p class="source-ref">{atlas.sources(pid,'../')} · <a href="../index.html#paper-{pid}">总览记录</a></p>{'<p class="small cross-ref">交叉阅读：'+cross+'</p>' if cross else ''}</article>'''
def ledger(tid):
 entries=[e for e in E.values() if e['topic']==tid or tid in e['cross_topics']]
 return '<section id="sources"><h2><span class="section-number">SOURCE LEDGER</span>本专题的原文入口</h2><p>表格与方法讨论按固定来源核对；本页统一记号、比较框架及研究假设属于阅读分析。跨论文分数保留各自协议，未进行模型复现。</p><details class="source-ledger"><summary>展开 '+str(len(entries))+' 项主线与交叉来源</summary><div class="source-grid">'+''.join(f'<div><strong>{e["id"]} · {esc(e["name"])}</strong><p>{atlas.sources(e["id"],"../")}</p><p class="small muted">{esc(e["evidence"])}</p></div>' for e in entries)+'</div></details></section>'
for tid,title,question,route in atlas.TOPICS[1:]:
 path=atlas.TOPIC_PATHS[tid];entries=sorted([e for e in E.values() if e['topic']==tid],key=lambda e:(e['date'],e['id']))
 content=(R/'research/topic-bodies'/(path+'.html')).read_text(encoding='utf-8')
 content=re.sub(r'\{\{table:(.*?)\}\}',table,content,flags=re.S)
 content=content.replace('{{studies}}',tiles(COMPANIONS[tid])).replace('{{methods}}',''.join(card(e) for e in entries))
 diagram='<div class="concept-flow" role="img" aria-label="本专题的三个研究环节">'+''.join(f'<div><span>{i:02d}</span><b>{a}</b><small>{b}</small></div>' for i,(a,b) in enumerate(STEPS[tid],1))+'</div>'
 hero=f'''<div class="breadcrumb"><a href="../index.html">研究地图</a><span>/</span><a href="../index.html#topics">研究专题</a><span>/</span><span>专题 {tid}</span></div><header class="hero" data-number="{tid}"><div class="eyebrow">TOPIC {tid} / METHOD STUDY</div><h1>{title}</h1><p class="lead">{question}</p><div class="meta"><span class="badge">几何为中心 · 方法比较</span><span class="badge">{len(entries)} 项主归属</span><span class="badge warm">{len(COMPANIONS[tid])} 个精读入口</span></div>{diagram}<div class="reading-rail"><span>专题主线 + 论文方法卡 · 推导可展开</span><button data-reading-size aria-pressed="false">加大字号</button></div></header>'''
 prev=atlas.TOPICS[int(tid)-2];nxt=atlas.TOPICS[int(tid)%10]
 end=f'<nav class="paper-endnav" aria-label="专题导航"><a href="{atlas.TOPIC_PATHS[prev[0]]}.html"><small>PREVIOUS TOPIC</small>{prev[0]} · {prev[1]}</a><a href="{atlas.TOPIC_PATHS[nxt[0]]}.html"><small>NEXT TOPIC</small>{nxt[0]} · {nxt[1]}</a></nav>'
 toc=[('question','研究问题'),('notation','统一记号与推导'),('comparison','设计空间与精读'),('methods','逐篇方法卡'),('evidence','实验与比较条件'),('discussion','讨论与失败边界'),('hypotheses','可证伪研究假设'),('reading','建议阅读路径'),('sources','原文与版本')]
 (R/'topics'/(path+'.html')).write_text(atlas.shell(title,hero+content+ledger(tid)+end,active='chapter',prefix='../',toc=toc),encoding='utf-8')
# Extend the approved sample without replacing its in-depth comparisons.
p=R/'topics/01-geometry.html';s=p.read_text(encoding='utf-8')
extra='<section id="extensions"><h2><span class="section-number">EXTENSIONS</span>多参考融合、集合推理与工程扩展</h2><p>六篇骨干建立了表示比较的主线；另外三项主归属分别补充多参考融合、大规模集合推理和工程功能边界。</p>'+''.join(card(E[pid]) for pid in ['A03','A04','A11'])+'</section>'
s=s.replace('<section id="evidence">',extra+'<section id="evidence">',1)
s=s.replace('<footer class="footer">',ledger('01')+'<footer class="footer">',1)
s=s.replace('<header class="hero">','<header class="hero" data-number="01">',1)
s=s.replace('<a href="#evidence">实验能支持什么</a>','<a href="#extensions">补充方法与工程版本</a><a href="#evidence">实验能支持什么</a>')
s=s.replace('后续专题可直接引用各页的','其他专题可直接引用各页的')
p.write_text(s,encoding='utf-8')
# A compact directory links every independent study from the overview.
directory='<section id="studies"><h2><span class="section-number">PAPER COMPANIONS</span>23 篇可复用的独立论文精读</h2><p>专题建立比较框架，精读页补足论文独有的动机、推导、训练与实验。原论文关键图表可放大，并附版本、图号和 PDF 页码。</p><div class="study-directory">'
for tid,title,_,_ in atlas.TOPICS:
 ss=[e for e in REG if e['topics'][0]==tid]
 if ss:directory+=f'<div><span class="eyebrow">TOPIC {tid}</span><h3>{title.split("：")[0]}</h3>'+''.join(f'<a href="{e["path"]}"><span>{e["title"]}</span><small>{e["figures"]} 处原图表 ↗</small></a>' for e in ss)+'</div>'
directory+='</div></section>'
p=R/'index.html';s=p.read_text(encoding='utf-8');s=s.replace('<section id="library">',directory+'<section id="library">',1);p.write_text(s,encoding='utf-8')
# Add cross-topic links to the original six studies as well.
for e in REG[:6]:
 p=R/e['path'];s=p.read_text(encoding='utf-8')
 related='<div class="study-context">继续比较：'+' · '.join(f'<a href="../topics/{atlas.TOPIC_PATHS[t]}.html">{t} · {atlas.TN[t]}</a>' for t in e['topics'])+'</div>'
 s=s.replace('<nav class="paper-endnav"',related+'<nav class="paper-endnav"',1);p.write_text(s,encoding='utf-8')
print(f'Built 10 topics, {len(REG)} independent studies, overview and audit (35 HTML pages).')
