from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];S=R/'research/moge-series'
def save(name,data):(S/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def item(source,target,note,priority='core',status='explained',kind='section'):
 return dict(source=source,target=target,note=note,priority=priority,status=status,kind=kind)
coverage={'checked':'2026-10-26','target_base':'papers/','scope':'正文与关键技术附录；网页保留贡献主线，非逐参数复现。原文页码为固定 PDF 物理页。','papers':[
 {'page':'moge-1.html','source_version':'2410.19115v3','items':[
 item('Abstract / PDF p.2','abstract','逐字复用英文摘要，修复断行；CC BY 4.0。',status='verbatim',kind='abstract'),
 item('§1–2 / pp.2–3','motivation','合并历史背景，保留焦距/物距导致的监督歧义。',status='summarized'),
 item('§3.1, Eq.2; App.A.1 / pp.4,14','method','保留 affine 自由度、居中主点假设、投影求焦距与 z-shift；不展开迭代求解每步代数。'),
 item('§3.2, Eqs.3–8; App.A.2 / pp.5,14–17','method','解释 ROE 的分段线性候选、逆深度权重、截断与局部独立对齐。'),
 item('App.A.2, Algorithms 2–5 / pp.14–16',None,'完整断点排序与证明不改变本页主线；保留原文定位供实现时查阅。','optional','reference-only','appendix'),
 item('§3.3; App.B.1, Table 5 / pp.6,16–17','training','混合数据及按标签质量配置损失。',status='summarized'),
 item('§4.1–4.3; Tables 1–4 / pp.6–8','experiment','覆盖点图、深度、FoV 与小模型消融；保留非单调指标。',kind='experiment'),
 item('App.B.2–B.3 / pp.17–18','experiment','解释评测清理、各类对齐、训练域重叠。',kind='appendix'),
 item('App.C / pp.18–23',None,'重复定性图和逐数据集深度表保留原文；主实验族已在正文概述。','optional','reference-only','appendix'),
 item('App.D, Figure 9 / p.18','discussion','细结构与时序一致性限制；连接局部对齐不能保证全局布局的分析。',kind='limitation')],
 'claims':[{'claim':'局部点 Rel 8.59→7.62→7.16','evidence':'Table 4: ROE scale-inv., ROE affine-inv., Full','target':'experiment','conditions':'ViT-B 消融，不同表示/损失配置','type':'author-reported'},
 {'claim':'形状对齐成绩不能解释为米制精度','evidence':'§3.1 and App.B.3 freedoms','target':'discussion','conditions':'单张图无尺度观测','type':'analysis'}]},
 {'page':'moge-2.html','source_version':'2507.02546v1','items':[
 item('Abstract / p.1','abstract','固定 v1 原文，包括参考编号 [61]；CC BY 4.0。',status='verbatim',kind='abstract'),
 item('§1–2 / pp.1–3','motivation','合并相关工作，聚焦 metric scale 与标签噪声的两个瓶颈。',status='summarized'),
 item('§3.1–3.2, Eq.3, Figures 2–3 / pp.3–4','method','解释继承点图/ROE、解耦尺度、CLS-MLP 和 stopgrad 标签。'),
 item('§3.3, Eqs.4–7, Figures 4–5 / pp.5–6','training','局部对齐筛错、教师梯度与真实边界约束的 log-Poisson 补全；区分训练与推理。'),
 item('§4.1–4.3, Tables 1–4, Figures 6–7 / pp.6–9','experiment','分相对/米制/边界实验；重点保留同骨干消融与 metric depth 退步。',kind='experiment'),
 item('App.A.1–A.2 / pp.15–16','method','轻量解码器、可变分辨率与混合数据合并；不罗列通道数/采样权重。',status='summarized',kind='appendix'),
 item('App.A.3 / pp.16–17','experiment','metric point 允许平移，metric depth 不对齐；影响结论，必须明示。',kind='appendix'),
 item('App.B.1–B.2, Table B.3 / pp.17–18','experiment','分辨率/延迟的条件和代表数值；不混用最快与最清晰配置。',kind='appendix'),
 item('App.B.3–B.4 / pp.19–22',None,'重复视觉案例与完整逐数据集表留原文；主实验族和可比性已概述。','optional','reference-only','appendix'),
 item('§5 Limitations / p.9','discussion','细线、头发、前后景尺度差与域外尺度偏移。',kind='limitation')],
 'claims':[{'claim':'标签改良使 F1 10.3→12.5，但 metric depth Rel 15.8→16.5','evidence':'Table 4, raw/improved real data','target':'experiment','conditions':'ViT-B; identical ablation family','type':'author-reported'},
 {'claim':'教师偏差仍可能造成误过滤','evidence':'§3.3 relies on synthetic teacher local geometry','target':'discussion','conditions':'教师在真实域的局部结构错误','type':'mechanistic inference'}]},
 {'page':'moge-3.html','source_version':'2607.17967v2','items':[
 item('Abstract / pp.1–2','abstract','仅展示首句 11 词节选，明确标注并链接全文；非开放复用许可。',status='verbatim',kind='abstract'),
 item('§1–2 / pp.2–3','motivation','合并历史背景；突出 2D 邻域与深度不连续的冲突，作为作者假说而非唯一成因。',status='summarized'),
 item('§3.1–3.2.3, Eqs.1–5, Figure 2 / pp.3–5','method','区分体素坐标与特征，解释 log-depth/固定射线/重新体素化/DINO 注入。'),
 item('§3.3; App.A.1–A.3 / pp.5,15–16','training','明确 synthetic-only refiner gradients、预热/联合训练、共享尺度的局部损失变更。',kind='appendix'),
 item('App.A.2 optimizer and full loss hyperparameters / p.16',None,'逐超参数不影响方法主线；训练阶段和数据路由已在正文解释。','optional','reference-only','appendix'),
 item('§4.1–4.4, Tables 1–2 / pp.6–8','experiment','全局/局部/边界三个实验族；F1 非最优；主表 K=3 的延迟条件。',kind='experiment'),
 item('§4.5, Table 3, Figure 4 / pp.7–10','experiment','冻结基座、参数匹配 2D、DINO 注入、体素分辨率、迭代次数；区分联合基座 K=0。',kind='ablation'),
 item('App.B.1–B.2 / pp.16–17','experiment','SAM2+视差结构筛细节；全局尺度+逐区平移；0.01 阈值与按区域平均，不能跨代混比。',kind='appendix'),
 item('App.C, Tables C.1–C.4 / pp.17–19','experiment','逐数据集结果用于定位协议；延迟 FP16/A100/batch1/200 inputs。',status='summarized',kind='appendix'),
 item('App.D / pp.20–22',None,'更多重复定性比较留原文；页面用 Figure 4 同场景迭代图说明可见变化。','optional','reference-only','appendix'),
 item('§5 Limitations / p.10','discussion','回归边界歧义与飞点；固定射线限制和真实域局部验证缺口明确为本页分析。',kind='limitation')],
 'claims':[{'claim':'局部点 δ 46.6%→47.0% (2D) vs 55.1% (SSR)','evidence':'Table 3, Base/2D Conv./D=200','target':'experiment','conditions':'Frozen MoGe-2 ViT-L; K train3/test5','type':'author-reported'},
 {'claim':'39→121 ms','evidence':'Table 2/C.4 MoGe-2 versus ViT-L 3-step','target':'experiment','conditions':'A100 FP16 700² batch1','type':'author-reported'},
 {'claim':'固定射线可能限制相机方向错误的纠正','evidence':'§3.2 u,v fixed; Eq.4–5','target':'discussion','conditions':'初始射线错误；未声称已有专项验证','type':'mechanistic inference'}]}
], 'gaps':['MoGe-3 官方会议接收记录未核实；只报告作者项目页声明。','未运行模型、未复现训练或表格数值。','未检查官方实现 revision；不以当前默认代码替代论文协议。']}
save('coverage.json',coverage)
review={'checked':'2026-10-26','scope':'独立自审；非外部同行评审','facts':[
 {'check':'身份、版本、作者/单位','result':'三篇均以固定 PDF 首页面署名；MoGe-3 标记作有说明的符号统一。'},
 {'check':'发表状态','result':'MoGe 的 CVF 2025 与 MoGe-2 的 NeurIPS 2025/DOI 已核实；MoGe-3 官方状态明确未核实。'},
 {'check':'摘要','result':'MoGe/MoGe-2 用固定 PDF 英文原文；MoGe-3 为明确标注的首句节选。'},
 {'check':'公式与机制','result':'比对原文 Eqs；修正“均匀 XYZ 网格”的潜在误读；明确固定射线、训练梯度路由与共享尺度局部损失。'},
 {'check':'数字与归因','result':'数值取 PDF，不混入项目页新增 K=0 行；保留 metric 与边界不改善的对照；冻结基座 test5 与联合模型 test3 分开。'},
 {'check':'图表','result':'6 个新增裁切逐张目视检查；修正表格夹入下一幅图、两张图注裁断；重用两张 MoGe 图。'}],
 'editorial':['系列页解释跨代问题与可比性，各论文页保留完整主线，避免一个超长三篇合集。','每篇两个机制公式、2–3 张原图；每页额外预留 0.5 分钟辨认密集表格。','全部折叠自测计入预算，不折叠核心讲解；旧章节与 figure-* 锚点保留。'],
 'closed_book':[
 {'question':'各篇解决什么问题？','answer':'MoGe 管理单图监督歧义；MoGe-2 增加尺度并处理真实标签噪声；MoGe-3 改善深度边界处的特征交互。','verified_against':'三篇 §1/§3','pass':True},
 {'question':'新增机制分别在哪里？','answer':'对齐损失与点图；CLS-MLP/训练标签补全；像素-log-depth 稀疏 U-Net 的迭代深度残差。','verified_against':'MoGe §3.1–3.2; MoGe-2 §3.2–3.3; MoGe-3 §3.2','pass':True},
 {'question':'训练与推理如何区分？','answer':'ROE 用真值形成监督；MoGe 投影解相机；MoGe-2 的标签清理只在数据准备；MoGe-3 固定步数推理不更新权重。','verified_against':'对应 Method/Training','pass':True},
 {'question':'什么证据支持贡献？','answer':'MoGe/2 Table 4 控制表示或数据；MoGe-3 Table 3 对照匹配参数 2D 并冻结基座，Figure 4 分开联合训练和迭代收益。','verified_against':'固定 PDF 原表/原图','pass':True},
 {'question':'代价是什么？','answer':'标签改良与冻结 SSR 均存在 metric depth 退步；MoGe-3 三步 ViT-L 延迟39→121 ms；未把单项改善推广为全面提升。','verified_against':'MoGe-2 Table 4; MoGe-3 Tables 2–3/C.4','pass':True},
 {'question':'结论边界是什么？','answer':'单图尺度来自先验、局部指标协议变更、薄结构/飞点、不可见面与时序尚未解决；真实域局部测试需补证据。','verified_against':'三篇 limitations; MoGe-3 App.B','pass':True}],
 'validation_status':'结果见 validation.json；不把结构检查视为语义正确性的证明。',
 'remaining_gaps':coverage['gaps']}
save('review.json',review)
print('Recorded section-level coverage, evidence conditions and six closed-book answers')
