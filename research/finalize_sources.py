"""Apply corrections confirmed against fixed-version PDF pages."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def replace(path,pairs):
 p=R/path;s=p.read_text(encoding='utf-8')
 for a,b in pairs:s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
replace('research/paper-bodies/nas3r.html',[
 ('Tables 5–7','Tables 5–6'),
 ('参数化是稳定训练的关键证据','输入、数据与预训练的独立证据'),
 ('Table 8 对比三维输出参数化，说明局部深度→相机变换对训练的重要性。Table 7 检验骨干结构，Table 9 则考察后续任务微调，分别对应表示、架构和可迁移性。','Table 8 增加上下文视图时，NVS 与相机指标共同改善；Table 7 比较 RE10K、DL3DV 及混合训练数据，检验数据扩展；Table 9 比较自监督、从零监督训练及自监督初始化后的监督微调，检验迁移。局部深度参数化是方法的结构选择，不应把这三张表误写成参数化消融。')])
replace('research/paper-bodies/instantmesh.html',[
 ('Tables 2–4 分别检查图像质量、几何和组件消融。','Tables 2–4 在 GSO 轨道视角、OmniObject3D 轨道视角和另一组基准视角上，同时比较图像与几何指标。')])
replace('research/paper-bodies/pixelsplat.html',[('约 1 dB','约 1.47 dB')])
replace('research/render_additional_figures.py',[
 ('[.39,.625,.94,.805]','[.415,.625,.94,.805]'),
 ('[.51,.085,.94,.455]','[.51,.085,.94,.42]'),
 ('[.17,.10,.83,.395],\'推理时缓存历史 KV\'','[.17,.10,.83,.373],\'推理时缓存历史 KV\''),
 ('[.17,.18,.83,.63]','[.17,.18,.83,.71]')])
p=R/'research/additional-studies.json';m=json.loads(p.read_text(encoding='utf-8'))
titles={'vgg-t3':'VGG-T³: Offline Feed-Forward 3D Reconstruction at Scale','zipmap':'ZipMap: Linear-Time Stateful 3D Reconstruction via Test-Time Training','d4rt':'Efficiently Reconstructing Dynamic Scenes One D4RT at a Time','geocond':'GeoCond: A Conditioning-Aware Reliability Adapter for Feed-Forward 3D Reconstruction'}
for e in m:
 if e['slug'] in titles:e['subtitle']=titles[e['slug']]
p.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
p=R/'catalogue.json';d=json.loads(p.read_text(encoding='utf-8'))
for e in d:
 if e['id']=='G01':e['boundary']=e['boundary'].replace('线性可读出','小型 MLP 探针可读出')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Applied PDF-grounded corrections.')
