from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'research/build_html.py';s=p.read_text(encoding='utf-8')
for a,b in [
 ('href="{prefix}topics/01-geometry.html">样章','href="{prefix}index.html#topics">专题'),
 ('清单审查、总览、专题样章与六篇独立论文精读。其余专题已有归属与阅读问题，正文待展开。','10 个研究专题、23 篇独立论文精读与 69 项文献索引。'),
 ('阶段 1 · 总览 + 样章','10 个专题 · 23 篇独立精读'),
 ('阅读样章：表示与参考系','从表示与参考系开始'),
 ('<strong>1</strong><span>完整样章</span>','<strong>23</strong><span>独立论文精读</span>'),
 ('样章统一推导','专题 01 统一推导'),
 ('样章六篇骨干额外检查表示、训练目标和代表性消融','23 篇独立精读额外检查表示、训练目标和代表性消融'),
 ('后续专题展开时可按具体问题继续增补','后续可按具体研究问题继续增补'),
 ('<b>下阶段写作顺序：</b>待样章的深度、图示和证据形式获得反馈后，按“在线状态 → 计算扩展 → 几何后端 → 动态 → 条件与尺度 → 监督/可靠性 → 渲染 → 物体”展开。每章沿用问题、统一记号、方法卡、证据对照、失败条件与可证伪假设。','<b>阅读结构：</b>10 个专题沿用研究问题、统一记号、设计比较、方法卡、实验条件、失败边界与可证伪假设。23 篇骨干精读提供独立段落链接、原论文关键图表和版本记录。新增结论应先回到固定版本原文核对，再更新方法卡与关联专题。'),
 ("('provenance','来源与下一步')","('provenance','来源与更新约定')")
]:s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
print('Updated shared navigation and completion labels.')
