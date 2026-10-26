"""Idempotently integrate the reviewed MoGe sequel into the atlas catalogue."""
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[2];S=R/'research/moge-series'
sys.path.insert(0,str(R/'research'))
from build_moge_series import CAPTIONS
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
note='''MoGe-3 source review / checked 2026-10-26
Fixed source: https://arxiv.org/pdf/2607.17967v2 (22 physical pages)
Full paper and technical appendices A-D were inspected. The local PDF is a reading cache, excluded from publication.
Official code: https://github.com/microsoft/MoGe
Author project: https://qft-333.github.io/moge3page/
Publication: author page reports NeurIPS 2026 acceptance; official proceedings record was not verified.
Study: papers/moge-3.html; series: papers/moge.html.
Core mechanism: MoGe-2-initialized base, image/log-depth sparse voxel shell, DINO feature injection, iterative depth residuals with fixed rays.
Training: refiner receives synthetic gradients only; staged joint training; shared-scale local loss differs from the earlier MoGe losses.
Evidence: Table 3 frozen-base 2D/3D ablation; Figure 4 joint-base K=0 versus iterative SSR; Table 2 and C.4 latency.
Limitations: local evaluation uses Spring/Synth4K, metric and boundary scores are not uniformly improved, fly-points remain.
See coverage.json for section-level evidence and exclusions. This note is an original summary, not a copy of the source paper.
'''
p=S/'moge3-source-note.txt';p.write_text(note,encoding='utf-8')
data=read(R/'catalogue.json');data=[e for e in data if e['id']!='N13']
data.append(dict(id='N13',name='MoGe-3',arxiv='2607.17967',url='https://arxiv.org/abs/2607.17967',priority='P1',addition_candidate=True,topic='02',scope='通用几何',execution='单图基础预测＋固定步数稀疏几何细化',inputs='单张 RGB；无需给定相机或真实尺度',idea='MoGe-2 初始化后，在像素/log-depth 稀疏体素壳上迭代预测深度残差，用几何邻域减轻前后景特征混合。',boundary='refiner 仅接受合成数据梯度；细化固定射线，边界飞点仍存在；局部精度、米制误差与延迟需分开评价。',evidence='§3；Table 3 参数匹配 2D 对照；Figure 4 迭代；附录 A–C 的训练、局部指标与延迟。',version='2607.17967v2',source_local='research/moge-series/moge3-source-note.txt',source_url='https://arxiv.org/html/2607.17967v2',source_note=True,review_level='固定 PDF 正文与技术附录核查',type='论文',date='2026-07',added=True,checked='2026-10-26',source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),cross_topics=[]))
write(R/'catalogue.json',data)
q=read(R/'research/method-questions.json');q['N13']='稀疏邻域、DINO 特征注入和联合训练分别贡献多少？固定射线与仅合成数据梯度限制了什么？';write(R/'research/method-questions.json',q)
figs=[f for f in read(R/'research/figure-manifest.json') if f['slug'] not in ['moge-2','moge-3']]
for f in read(S/'figures.json'):
 f.update(title=CAPTIONS[f['slug'],f['key']][0],reading=CAPTIONS[f['slug'],f['key']][1],pdf='research/sources/'+f['version']+'.pdf',source=f['url'])
 figs.append(f)
write(R/'research/figure-manifest.json',figs)
# Current totals; historical original-56 and initial-12 statements stay historical.
p=R/'research/build_html.py';text=p.read_text(encoding='utf-8')
for a,b in [('独立论文精读 · 23 篇','独立论文精读 · 25 篇'),('23 篇独立论文精读与 69 项','25 篇独立论文精读、1 个系列比较与 70 项'),('10 个专题 · 23 篇独立精读','10 个专题 · 25 篇独立精读'),('<strong>23</strong>','<strong>25</strong>'),('<strong>67</strong>','<strong>68</strong>'),('<strong>12</strong>','<strong>13</strong>'),('23 篇独立精读额外','25 篇独立精读额外'),('>69 项</span>','>70 项</span>'),('另补 12 篇论文和 1 篇综述导航，共 69 项。','另补 13 篇论文和 1 篇综述导航，共 70 项（含 2026-10-26 补入的 MoGe-3）。'),('Depth Anything / MoGe → MoGe-2 / MetricAnything；Pow3R','Depth Anything / MoGe → MoGe-2 → MoGe-3；MetricAnything / Pow3R'),('12篇补入</span>','13篇补入</span>'),('67篇论文 + 1工程版本 + 1综述','68篇论文 + 1工程版本 + 1综述'),('补入12篇：各补哪一段','补入13篇：各补哪一段')]:text=text.replace(a,b)
text=text.replace("'N12':'区分生成多视图、可微网格和真实观测重建。'}","'N12':'区分生成多视图、可微网格和真实观测重建。','N13':'补齐 MoGe 系列：从相对几何和尺度/标签改良，推进到稀疏几何邻域细化。'}")
p.write_text(text,encoding='utf-8')
print('Integrated 70 catalogue entries and 69 original figure records')
