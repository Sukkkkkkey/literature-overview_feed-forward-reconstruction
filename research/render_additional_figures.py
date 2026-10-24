from pathlib import Path
import json,sys
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
META={e['slug']:e for e in json.loads((R/'research/additional-study-sources.json').read_text(encoding='utf-8'))}
# Normalized page coordinates. Crops retain the original figure/table and caption.
PLAN={
'moge':[
 ('architecture','Figure 3',4,[.08,.085,.93,.411],'点图预测与全局、局部监督','网络预测点图和无效区域 mask；焦距与 shift 由投影关系恢复。下方的监督流程独立展示全局与局部几何，不要把它们合为一个普通深度 loss。'),
 ('ambiguity','Figures 4–5',4,[.08,.415,.93,.613],'投影歧义与相对距离','左图讨论焦距和距离共同变化的歧义；右图讨论相对距离监督。两者解释 affine-invariant 表示与局部几何约束的不同作用。'),
 ('experiment','Table 4',7,[.415,.625,.94,.805],'点图表示与训练目标消融','各行使用受控模型配置。读清 scale-invariant / affine-invariant 两组指标，检查局部损失和 ROE 是否改善不同几何部分。')],
'pow3r':[
 ('architecture','Figure 2',3,[.08,.085,.50,.292],'可选条件与三张点图','两幅图的 decoder 互相交流，第二分支同时给出本地与第一相机系中的几何；这为一次读取两张深度和相对位姿提供接口。'),
 ('conditioning','Figure 3',4,[.51,.085,.94,.42],'模态注入的位置','K 转为逐像素 rays，稀疏 depth 与 mask 共同编码；相对位姿进入全局 token。不同条件不宜用同一种表示硬拼。'),
 ('experiment','Figure 6',7,[.08,.085,.50,.44],'错误条件下的输出与置信度','横轴是人为给错的相机条件。输出并不始终严格遵从输入；置信度响应只是在该受控协议中的证据，不是普遍可靠性保证。')],
'cut3r':[
 ('architecture','Figure 3',4,[.08,.085,.93,.44],'持久状态的读写与虚拟视角查询','每帧图像 tokens 与 state tokens 双向交互；右侧 raymap 查询只读取、不写入状态。预测未见结构仍包含先验补全。'),
 ('experiment','Table 2',6,[.08,.085,.93,.29],'视频深度：尺度不变与 metric','分别比较 per-sequence scale 与 metric 行，查看 Optim. / Onl. 标记。在线、尺度和优化配置不能从表中省略。'),
 ('state','Table 5',8,[.08,.085,.50,.205],'重新访问状态的收益','比较初次在线输出与 revisit 模式。再次读取完整状态的结果，不是初次到达时可因果获得的结果。')],
'streamvggt':[
 ('architecture','Figure 3',4,[.17,.10,.83,.365],'因果时序注意力与多任务输出','训练可以并行输入一段序列，但学生的 attention mask 阻止读取未来。完整序列教师提供的是训练监督。'),
 ('cache','Figure 4',5,[.17,.10,.83,.373],'推理时缓存历史 KV','缓存避免重算历史投影；新帧仍读取历史内容。缓存长度与当前帧延迟应随序列长度一起报告。'),
 ('experiment','Tables 8–10',10,[.17,.10,.83,.395],'剪枝、蒸馏和缓存的分项对照','三张表分别改变缓存保留、训练监督、历史信息使用。不能把这些不同因素的收益全归因于因果 mask。')],
'vgg-t3':[
 ('architecture','Figure 2',4,[.08,.085,.93,.35],'将全局 attention 转为快速权重','Update 在 KV 关联上更新小 MLP，Apply 用 Q 读取压缩后的信息；下游几何只在骨干最后读出。'),
 ('experiment','Table 6',8,[.51,.21,.93,.35],'线性化的关键组件消融','不同转换训练方案与 ShortConv2D 的对照用于检查线性化质量。与原始 softmax 模型比较时，还需统一推理长度和 attention scaling。')],
'zipmap':[
 ('architecture','Figure 2',3,[.08,.085,.93,.43],'双向重建与可查询场景状态','图像 tokens 更新 fast weights；raymap tokens 读取状态。图中的查询路径需要相应训练，不只是把任意相机丢进基础模型。'),
 ('experiment','Table 6',8,[.08,.085,.50,.235],'TTT 更新规则的消融','小规模训练对照显示 Newton–Schulz、门控和动态学习率的重要性；不能直接将该表幅度外推到完整大模型。')],
'mast3r':[
 ('architecture','Figure 2',4,[.07,.075,.93,.285],'三维点图与局部描述子共同预测','点图建立几何上下文，描述子提供精确像素匹配；下游匹配仍有搜索步骤。'),
 ('matching','Figure 3',6,[.07,.075,.93,.34],'快速 reciprocal nearest-neighbor matching','从少量种子往返迭代，找到互为最近邻的匹配并移除已收敛点。它有采样偏置，不是枚举全部密集匹配的同义词。'),
 ('experiment','Table 1',8,[.12,.08,.92,.22],'匹配损失、几何损失与局部特征','该表在同一 Map-free 验证协议中比较模块，适合判断三维监督是否帮助匹配；与 test set 最终成绩分开阅读。')],
'monst3r':[
 ('architecture','Figure 3',6,[.17,.10,.83,.342],'动态点图与全局相机优化','相机诱导 flow 与外部光流比较得到静态线索，再进入整段优化。两图前馈与最终视频结果不是同一计算量。'),
 ('experiment','Table 5',10,[.17,.55,.83,.81],'动态训练与优化项消融','各组同时考察深度与相机。将训练数据、时间步幅和 flow/平滑项的作用分开，避免只看最终最佳行。')],
'd4rt':[
 ('architecture','Figure 2',2,[.08,.085,.93,.32],'视频编码与独立点查询','查询拆开 source、target 和 camera 时间。重建场景与按需解码是两个成本阶段。'),
 ('queries','Table 1',3,[.08,.085,.50,.30],'用同一接口组合多种任务','逐项改变时间索引，检查固定的是什么。尤其区分目标时间变化与参考相机变化。'),
 ('experiment','Table 4',6,[.08,.34,.93,.61],'local 与 world 三维跟踪','两半使用不同坐标表达；有无真值内参也分开报告。world 跟踪进一步检验参考系转换。')],
'pixelsplat':[
 ('architecture','Figure 3',4,[.08,.085,.93,.44],'概率深度与可微 Gaussian 采样','Gaussian 位置从离散深度分布采样；opacity 与该桶概率相连，使渲染梯度能影响未来采样概率。'),
 ('experiment','Table 2',8,[.495,.40,.93,.54],'epipolar 编码与概率预测消融','在同一评测协议中删除不同模块，观察渲染指标。更高 PSNR 本身不证明浮动点已完全消失。')],
'mvsplat':[
 ('architecture','Figure 2',4,[.21,.14,.79,.40],'cost volume 到 Gaussian','显式深度候选搜索提供中心位置，另一分支回归其余 Gaussian 参数。两条路径在渲染损失下联合训练。'),
 ('experiment','Table 3',12,[.21,.14,.79,.365],'成本体、跨视注意力与细化','去掉 cost volume 的退化最大；去掉 cross-view attention 的版本因过拟合使用最佳 checkpoint，与其他最终 checkpoint 的条件需一并保留。')],
'croco-v2':[
 ('architecture','Figure 2',2,[.50,.085,.93,.31],'从合成补全走向真实图像对','图中并列展示真实数据、位置编码和模型规模三项变化；它们不是一个不可拆分的“更大预训练”。'),
 ('experiment','Table 1',7,[.08,.34,.93,.55],'逐项扩展 CroCo 的下游消融','分别观察 stereo 的 bad@1 和 flow 的 EPE。单项贡献应在保持其余列可比的行间判断。')],
'nas3r':[
 ('architecture','Figure 2',4,[.08,.085,.93,.323],'阻止 target-to-context 泄漏的训练闭环','context 生成 Gaussian；target 图像参与相机预测并监督渲染。mask 约束保证目标外观不能直接写入 context 表示。'),
 ('experiment','Table 8',8,[.51,.085,.93,.222],'增加上下文视图的效果','同时观察新视角合成与相机 AUC。更多输入改善结果支持模型利用跨视信息，但不能单凭该表归因于某一种参数化。')],
'geometric-understanding':[
 ('architecture','Figure 1',5,[.17,.61,.83,.91],'逐层 fundamental-matrix probing','曲线显示几何信息能被指定 MLP probe 读出；它是可解码性证据，仍需干预来讨论模型如何使用信息。'),
 ('experiment','Figure 3',8,[.17,.075,.83,.66],'定向 attention 干预','四种位置干预提供对照。读清纵轴对应 probe 几何还是下游输出，避免从 attention 图直接推断完整算法。')],
'geocond':[
 ('architecture','Figure 2',3,[.08,.085,.93,.40],'训练期 teacher 与部署期可靠性头','重排 ensemble、BA 对照用于训练标签；推理只运行一次骨干，再计算条件特征。条件特征计算与 MLP 时间都应计入。'),
 ('experiment','Table 3',6,[.51,.305,.93,.515],'门控优化的域内与域外收益','保留 FF-always、BA-always、gate 和 oracle 四种参照。域外 gate 显著好于一律 BA，但该表仍低于纯前馈。')],
'lrm':[
 ('architecture','Figure 1',4,[.17,.10,.83,.48],'图像与相机条件生成 triplane','图像通过 cross-attention 提供细节，相机通过调制组织整体几何；体渲染给出训练信号。'),
 ('ablation','Tables 8–10',23,[.17,.18,.83,.71],'相机归一化、监督视图与渲染分辨率','三个表分别改变相机条件、侧视监督数量和训练渲染分辨率。应在各表内部比较，不能把不同训练配置的分数直接串成单一提升。'),
 ('experiment','Figure 4',8,[.17,.39,.83,.49],'不可见纹理与相机假设的失败案例','这是原文主动保留的失败展示。模糊背面与错误相机造成的形变分别对应先验多解性和投影模型偏差。')],
'instantmesh':[
 ('architecture','Figure 2',3,[.08,.085,.93,.33],'生成六视图、重建与网格监督','扩散先生成视图，LRM 聚合为 triplane，FlexiCubes 支持可微网格提取。整条流程不能简写为单步前馈。'),
 ('experiment','Tables 2–4',6,[.495,.085,.93,.61],'GSO 与 OmniObject3D 的多种协议','不同数据子集、相机轨迹和表示变体分表。Mesh 与 NeRF 的优势并不完全一致，指标阈值在归一化物体坐标中解释。')]
}
manifest=json.loads((R/'research/figure-manifest.json').read_text(encoding='utf-8'))
manifest=[x for x in manifest if x['slug'] not in PLAN]
O=R/'research/contacts';O.mkdir(exist_ok=True)
for slug,figs in PLAN.items():
 e=META[slug];doc=pdfium.PdfDocument(R/e['pdf']);out=R/'assets/figures'/slug;out.mkdir(parents=True,exist_ok=True)
 tiles=[]
 for key,label,page,box,title,reading in figs:
  im=doc[page-1].render(scale=3).to_pil().convert('RGB');w,h=im.size
  im=im.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(box)))
  path=out/(key+'.png');im.save(path,optimize=True)
  manifest.append(dict(slug=slug,key=key,label=label,page=page,box=box,title=title,reading=reading,image=path.relative_to(R).as_posix(),width=im.width,height=im.height,pdf=e['pdf'],source=e['url'],version=e['version'],operation='Unmodified PDF raster crop including original label/caption'))
  im.thumbnail((580,620));tile=Image.new('RGB',(610,670),'#e7edf0');tile.paste(im,((610-im.width)//2,32));ImageDraw.Draw(tile).text((12,10),slug+' / '+key+' / p'+str(page),fill='black');tiles.append(tile)
 sheet=Image.new('RGB',(610*len(tiles),670),'white')
 for i,t in enumerate(tiles):sheet.paste(t,(i*610,0))
 sheet.save(O/(slug+'-crops.png'))
(R/'research/figure-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Total figures:',len(manifest))
