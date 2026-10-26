# Feed-forward 3D Reconstruction · 研究阅读地图

以几何重建为中心的中文文献研究，明确区分场景、物体、动态几何与可渲染表示。方法理解为主体，研究假设为延伸。

直接用浏览器打开 [index.html](index.html)。页面、样式、交互和论文图表均支持离线阅读；外部原文链接需要联网。

- [总览与文献方法卡](index.html)
- [专题 01：通用多视几何、表示与参考系](topics/01-geometry.html)
- [清单审查与来源记录](review.html)
- `topics/`：以研究问题组织的专题；`papers/`：可跨专题复用的独立论文精读。
- `assets/figures/`：原论文关键图表；版本、页码、裁切坐标记录在 `research/figure-manifest.json`。
- `catalogue.json`：文献元数据、分类、核心贡献、输入条件与阅读边界。
- `research/`：内容源文件、生成工具和可追溯的论文缓存。

初版核查日期：2026-10-24；MoGe 系列更新于 2026-10-26。此项目是有边界的系统阅读地图，不宣称穷尽全部工作；未运行或复现论文模型。实验结论按各论文的输入、对齐、数据集与后端条件解释，不将异协议结果拼接成排行榜。

论文及原论文图表的著作权归原作者或出版方；中文解释与统一符号推导属于本研究笔记。每处原图保留来源和版本。原始 Obsidian 笔记不属于本仓库，也不会被生成工具修改。

当前版本共 **38 个 HTML 页面**：总览、审查记录、10 个研究专题、25 篇独立论文精读和 1 个系列比较页。70 项索引包含 68 篇方法/分析论文、1 项工程版本和 1 篇综述导航；各专题覆盖全部方法主归属。图表档案收录 69 处原文裁切（含保留的历史图），并提供固定段落链接、可展开推导和原尺寸图表查看。

[MoGe 系列比较](papers/moge.html) 串联 [MoGe](papers/moge-1.html)、[MoGe-2](papers/moge-2.html) 与 [MoGe-3](papers/moge-3.html)：相对几何监督 → 米制尺度与标签细化 → 稀疏几何邻域。三篇精读均提供原图、方法解释、受控消融与限制；每页阅读量按统一规则估算在 10 分钟内。MoGe-3 的会议接收信息仅核实到作者项目页，页面明确区分这一状态与正式会议记录。

MoGe 内容源和覆盖/自审/验证记录位于 `research/moge-series/`；用主构建脚本即可重建。新增论文 PDF 仅作为本地阅读缓存，不随仓库提交；页面使用固定版本官方 PDF 入口，原图与中文正文仍支持离线阅读。原 `papers/moge.html` 的章节和图表锚点继续有效。

| 专题 | 核心问题 |
|---|---|
| [01 · 表示与参考系](topics/01-geometry.html) | 点图、相机、射线和尺度怎样组织？ |
| [02 · 单目先验与条件](topics/02-priors.html) | 哪些量来自观测，哪些来自先验？ |
| [03 · 在线与长期状态](topics/03-streaming.html) | 历史怎样保留、更新与遗忘？ |
| [04 · 计算扩展](topics/04-scaling.html) | 稀疏交互与快速权重如何交换精度、容量和成本？ |
| [05 · 匹配与几何后端](topics/05-backends.html) | 学习前端之后仍需哪些求解？ |
| [06 · 动态与 4D 查询](topics/06-dynamics.html) | 如何区分点身份、运动时刻和坐标系？ |
| [07 · 可渲染场景](topics/07-rendering.html) | 渲染质量能支持多强的几何结论？ |
| [08 · 监督与预训练](topics/08-supervision.html) | 几何知识从哪里来，监督成本怎样转移？ |
| [09 · 机制与可靠性](topics/09-reliability.html) | 模型用了什么信息，何时值得信任或优化？ |
| [10 · 物体与生成先验](topics/10-objects.html) | 完整资产的合理性与真实形状如何区分？ |

内容源文件位于 `research/topic-bodies/` 和 `research/paper-bodies/`。修改后运行 `python research/build_complete.py` 更新整套页面；`python research/check_html.py` 核查本地链接、锚点与清单。图表已附在仓库中，普通重建页面无需下载论文或安装 PDF 工具。重新裁切原图才需要 `pypdfium2` 与 Pillow；浏览器排版检查另需配置本机 Playwright 和浏览器路径。

验证记录见 [research/validation.json](research/validation.json)：所有页面检查桌面与手机宽度、离线图片加载及段落跳转，论文页检查图表放大。原文内容经过阅读核对，未进行模型实验或代码复现。
