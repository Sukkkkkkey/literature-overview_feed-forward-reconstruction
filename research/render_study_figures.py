from pathlib import Path
import json,sys
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
QA=R/'research/qa-v2';QA.mkdir(exist_ok=True)
PAGES={'2312.14132v3':[4,8,9],'2503.11651v1':[3,7,8,9],'2507.13347v3':[4,9,13],'2509.13414v3':[3,7,9],'2511.10647v1':[3,5,10,11],'2605.15195v1':[3,8,9]}
def contacts():
 for version,pages in PAGES.items():
  path=R/'research/sources'/(version+'.pdf')
  if not path.exists():continue
  doc=pdfium.PdfDocument(path);tiles=[]
  for n in pages:
   p=doc[n-1];img=p.render(scale=1.0).to_pil().convert('RGB');img.thumbnail((600,850));tile=Image.new('RGB',(620,885),'#e5e9ed');tile.paste(img,((620-img.width)//2,30));ImageDraw.Draw(tile).text((15,8),version+' / page '+str(n),fill='black');tiles.append(tile)
  sheet=Image.new('RGB',(620*len(tiles),885),'white')
  for i,t in enumerate(tiles):sheet.paste(t,(620*i,0))
  sheet.save(QA/(version+'-contact.png'))
  print(version,flush=True)
FIGURES={
 'dust3r':('2312.14132v3',[
  ('architecture','Figure 2',4,[.075,.085,.925,.307],'共同参考系的两图回归','沿两条分支看输出上标：第二张图的像素仍在第二张网格上，但 XYZ 已表达在第一相机系。图中的双 decoder 持续交换跨视信息。'),
  ('multiview','Table 3',9,[.075,.082,.93,.514],'多视深度与训练配置','先看 GT Pose、GT Intrinsics、GT Range，再比较误差。底部三行将 CroCo 预训练与图像分辨率作为消融，而不是把它们与表示贡献混在一起。'),
  ('surface','Table 4',9,[.50,.535,.93,.843],'通用回归与精密 MVS 的差距','同时读 accuracy 和 completeness：更完整的点云不一定有更小的表面距离。已知相机和训练域不同，不能把所有行当成完全同设定。')]),
 'vggt':('2503.11651v1',[
  ('architecture','Figure 2',3,[.08,.075,.925,.369],'交替注意力与任务读出','先找 frame/global attention 的交替位置，再跟随 camera 与稠密分支。图中的 tracks 需要结合正文理解为特征加查询模块的结果。'),
  ('camera','Table 1',7,[.08,.075,.50,.378],'前馈相机预测与附加 BA','比较最下面两行：前馈与 BA 是两个运行配置。训练是否见过评测域，以及十视图采样协议，也影响结果解读。'),
  ('attention','Table 5',8,[.51,.338,.93,.478],'信息交互方式的消融','在匹配参数量与层数的实验中，交替注意力优于这里的 cross-attention 和纯 global 变体；这是一项结构对照，不是任意规模的普遍结论。'),
  ('multitask','Table 6',9,[.075,.075,.50,.215],'辅助任务对 pointmap 的贡献','各行都围绕 pointmap 质量比较。删除相机、深度、跟踪监督的影响不同，说明冗余目标的价值不能只按输出数量判断。')]),
 'pi3':('2507.13347v3',[
  ('architecture','Figure 3',4,[.17,.083,.84,.385],'去掉指定参考视图的标识','上半部分用 token 或 embedding 指定参考图；下半部分取消这一机制，并配合相对监督。不要把这种输入对称性与输出坐标自由度混同。'),
  ('permutation','Table 6',9,[.17,.267,.84,.378],'输入重排带来的结果波动','表中是指标的标准差，不是几何误差本身。接近零表示改变输入顺序后更稳定，不能读成重建完美。'),
  ('ablation','Table 7',9,[.17,.822,.84,.925],'尺度与相对位姿设计','依次加入尺度不变点图与 affine-invariant pose；室内外列的改善幅度不同。点击放大查看全部指标。'),
  ('coldstart','Table 8',14,[.235,.075,.76,.180],'从头训练与 global proxy','π³ 本体并非从随机初始化就全面优于 VGGT。辅助 global proxy 改善了 ETH3D 等结果，而 7-Scenes 仍是必须保留的反例。')]),
 'mapanything':('2509.13414v3',[
  ('architecture','Figure 2',3,[.08,.085,.925,.515],'可选几何输入与因子化输出','沿左侧观察输入模态如何进入共享空间，沿底部观察尺度 token、DPT 与 pose head 如何组合为 metric 世界点。'),
  ('multiview','Figure 4',7,[.08,.085,.93,.445],'随视图数和条件输入变化的质量','实线、虚线对应不同已知信息。先比较相同输入，再比较附加测量的收益；各子图分别衡量形状、位姿、深度、射线与尺度。'),
  ('ablation','Table 5',8,[.51,.085,.925,.378],'表示分解与通用训练','左侧拆解输出表示与独立尺度；右侧比较通用与专家训练。不要忽略某些尺度或 rel 指标未改善的行。')]),
 'depth-anything-3':('2511.10647v1',[
  ('architecture','Figure 2',5,[.105,.105,.91,.405],'单一 Transformer 与 depth-ray 流程','同时看 backbone、Dual-DPT、camera token 和教师监督的连接。架构简化、输出组织和标签质量是三条不同的变化。'),
  ('head','Figure 3',7,[.49,.54,.91,.79],'Dual-DPT 共享到哪里','两个输出共享 reassembly，随后分开 fusion 与 output。它不是单个完全共享的预测分支。'),
  ('camera','Table 2',14,[.105,.11,.91,.355],'不同规模模型的相机评测','每个数据集同时报告严格和宽松角阈值。比较之前先固定模型尺度，并与几何、渲染实验分开。'),
  ('targets','Table 6',17,[.105,.375,.91,.53],'预测目标组合','这组消融没有 camera condition token。depth-ray 的优势很明显，但增加 camera 后在部分数据列又更好，结论需要保留指标条件。'),
  ('ablation','Table 7',18,[.105,.11,.91,.35],'架构、共享头、教师与条件','a–e 与 f–g 的位姿融合条件不同；星号行使用真值位姿。7-Scenes 中条件输入并没有提高 F1，是总括性结论的重要反例。')]),
 'vggt-omega':('2605.15195v1',[
  ('architecture','Figure 2',3,[.085,.085,.925,.403],'从多头到派生监督，从全局到部分寄存器交流','图中虚线指向训练期监督：matching 作用于特征，point loss 来自深度与相机反投影。register attention 只替换部分全局层，仍与帧内层配合。'),
  ('scaling','Figure 1',1,[.51,.32,.925,.64],'参数规模与数据规模','横轴分别是模型参数与训练序列数量，纵轴为 point error。单独看数据量与参数量的变化，避免把它们与最终不同训练配置的总榜分数混同。'),
  ('efficiency','Figure 7',10,[.085,.354,.50,.546],'推理显存与耗时','作者先修正 VGGT 的中间特征缓存，再比较同一 A100 上的推理。显存与速度的趋势不同；这些曲线不是“训练显存约30%”那项结论的图示。')])
}

def extract():
 manifest=[]
 for slug,(version,figs) in FIGURES.items():
  pdf=R/'research/sources'/(version+'.pdf')
  if not pdf.exists():continue
  doc=pdfium.PdfDocument(pdf);out=R/'assets/figures'/slug;out.mkdir(parents=True,exist_ok=True)
  for key,label,page,box,title,reading in figs:
   img=doc[page-1].render(scale=3).to_pil().convert('RGB');w,h=img.size
   crop=img.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(box)))
   path=out/(key+'.png');crop.save(path,optimize=True)
   manifest.append(dict(slug=slug,key=key,label=label,page=page,box=box,title=title,reading=reading,image=str(path.relative_to(R)).replace('\\','/'),width=crop.width,height=crop.height,pdf=str(pdf.relative_to(R)).replace('\\','/'),source='https://arxiv.org/pdf/'+version,version=version,operation='Unmodified PDF raster crop including original label/caption'))
 (R/'research/figure-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Extracted',len(manifest),'figures')
if __name__=='__main__':
 if '--extract' in sys.argv:extract()
 else:contacts()
