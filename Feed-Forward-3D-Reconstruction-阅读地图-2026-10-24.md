# Feed-Forward 3D Reconstruction：阅读地图与更新待读清单

调研日期：2026-10-24。主线：从 RGB 图像恢复场景几何与相机；同时覆盖在线重建、动态 4D、可渲染 Gaussian 表示及训练范式。

主体清单共 **56 项：55 篇论文 + Pi3X 工程版本**。其中原笔记已有 16 项，本次新增 40 项（39 篇论文 + Pi3X）。按 8 条研究分支组织，每项附核心贡献、设定边界、原始来源与阅读优先级；第 3 节提供首批阅读顺序。

原始依据：`D:\Obsidian\storage\Sukey\路漫漫其修远兮\A_notes\3d\papers\⭐Feed-Forward 3D Reconstruction.md`，只读。本文件独立保存在当前工作区，未回写 Obsidian。

这里的“已有”仅表示论文在原笔记中出现，不推断是否已经读完；“新增”表示本次建议补入。日期优先采用 arXiv 首次提交月份；明确标注的会议来自论文或作者页面，未标会议不代表未录用。Pi3X 单列为工程版本，不能作为另一篇论文计数。优先级是针对你现有笔记的阅读建议，不是论文质量排名。

- **P0：主线精读**，建立共同语言，或补齐目前最关键的空白。
- **P1：专题选读**，围绕一个明确问题与 P0 对照。
- **P2：背景／观察**，需要时查阅；很新的预印本先读方法与验证设计。

本次按摘要、论文页面和作者项目核对题名、时间与贡献，并对 π³ 的训练初始化等易混淆细节查阅正文。以下是有取舍的待读地图，不是穷尽式 bibliographic survey，也不是逐篇精读或复现实验报告。

## 1. 先调整分类方式

你的“single task → monocular → two-view → multi-view”适合建立入门顺序，但到 2026 年，单靠输入视图数已难以区分贡献。建议以**解决的问题**作为一级目录，把视图数、相机先验和输出表示放到论文标签里。

| 分支 | 核心问题 | 重点对照 |
|---|---|---|
| A. 通用多视几何与表示 | 怎样共同预测相机与几何？参考系如何选？ | DUSt3R → VGGT；π³ / MapAnything / DA3 / VGGT-Ω |
| B. 在线与长期记忆 | 新图像到来时保存什么？如何避免参考系外推和漂移？ | Spann3R / CUT3R → STream3R → LongStream / LingBot-Map / ABot-Recon |
| C. 可扩展计算 | 如何削减跨视图信息交换成本？ | sparse attention 与 fast-weight / TTT memory |
| D. 几何优化混合系统 | 哪些一致性约束仍值得显式求解？ | VGGSfM / MASt3R-SLAM / 分块对齐 / pose graph |
| E. 动态 4D | 是恢复每一帧形状，还是建立跨时间的物理点对应？ | MonST3R → Any4D / 4RC / UFO-4D / Point4D |
| F. 可渲染场景 | 如何同时恢复几何与外观，并支持新视角？ | pixelSplat / MVSplat → NoPoSplat / AnySplat / tttLRM |
| G. 监督、理解与可靠性 | 几何标签从何而来？模型学到了什么？何时会失效？ | NAS3R / Reliev3R / 几何表征分析 / GeoCond |
| H. 支撑与邻接方向 | 单目几何、位姿回归、物体级生成分别提供什么先验？ | MoGe-2 / MetricAnything；RayDiffusion；LRM / PF-LRM |

### 阅读时必须保留的四个边界

1. **feed-forward 模块 ≠ 完整系统无需优化。** DUSt3R 的多图重建涉及全局对齐；VGGSfM 有 BA；MASt3R-SLAM 有全局优化。它们都很值得读，但应与直接预测模型分开记录。
2. **TTT / fast weights 单独标记。** VGG-T³、ZipMap 等将场景信息写入测试时更新的权重或状态；这与传统逐场景优化 NeRF/3DGS 不同，也不宜笼统写成“测试时完全不更新任何东西”。
3. **unposed ≠ uncalibrated。** 不要求外参，不代表不要求内参。NoPoSplat 与 AnySplat 的输入条件不同；比较新视角合成时也要检查目标视角相机来自 GT、预测还是优化。
4. **可处理动态物体 ≠ 显式 4D 运动重建。** 每帧 pointmap、scene flow、长程 3D trajectories、可渲染时空 Gaussian 是不同输出。相似的动态场景视频演示可能测试的是不同能力。

### 对原笔记的具体修订建议

- **PR-LRM → PF-LRM**：原笔记正文是拼写错误，参考文献的 PF-LRM 正确。[原论文](https://arxiv.org/abs/2311.12024)
- **π³ 的“finetune VGGT to remove reference frame”需要扩充。** 使用 VGGT 预训练的 encoder 与 alternating-attention 权重作为初始化是事实；贡献还包括置换等变架构、局部点图和无需固定参考视图的位姿监督。不能只理解为删去 reference token。论文 v3 附录 A.2、A.4 说明了初始化与从头训练的对照。[正文](https://arxiv.org/html/2507.13347v3)
- **Reloc3R 移到位姿／定位支线**：核心是成对相对位姿回归，再用 motion averaging 得到绝对位姿，不是直接输出完整多视图场景。[原论文](https://arxiv.org/abs/2412.08376)
- **VGGSfM 移到混合系统**：可微、端到端训练与无需 BA 是两件事；它明确保留可微 BA。[作者页面](https://vggsfm.github.io/)
- **FLARE 同时交叉索引到可渲染场景**：先预测相机，再以相机条件预测几何和外观，NVS 是其核心任务之一。[原论文](https://arxiv.org/abs/2502.12138)
- **Depth Anything 分版本**：原版是单目深度基础模型；DA3 已进入任意视图的空间一致几何估计，不能只放在“monocular depth”。[DA3](https://arxiv.org/abs/2511.10647)

## 2. 分类文献卡

每行的“读点”是建议带着去验证的问题；贡献描述只概括论文提出的方法，不将作者的 benchmark 结论扩展为通用排名。

### A. 通用多视几何：pointmap、参考系与统一输出

| ID / 优先级 | 论文、时间、来源 | Core idea / contribution | 读点与设定边界 |
|---|---|---|---|
| A01 · P0 | **[DUSt3R](https://arxiv.org/abs/2312.14132)** · 2023-12 / CVPR 2024 · 已有 | 将两图几何问题改写为同一参考系中的稠密 pointmap 回归，把深度、匹配、相机恢复连接起来。 | 学会 pointmap 与尺度歧义；两图预测是前馈，多图系统需要全局对齐。 |
| A02 · P0 | **[MASt3R](https://arxiv.org/abs/2406.09756)** · 2024-06 / ECCV 2024 · 已有 | 在 DUSt3R 上增加受匹配监督的局部特征头，并用 reciprocal matching 高效获得精确对应。 | 重点是 3D 先验如何帮助 matching；后续 SLAM 的重要前端。 |
| A03 · P1 | **[MV-DUSt3R+](https://arxiv.org/abs/2412.06974)** · 2024-12 / CVPR 2025 · 已有 | 多视 decoder 一次融合多图；“+”以跨参考视图模块融合不同参考选择，另可增加 Gaussian 头。 | 与 π³ 比较：融合多个参考选择，与从结构上取消参考特权有何区别？ |
| A04 · P1 | **[Fast3R](https://arxiv.org/abs/2501.13928)** · 2025-01 / CVPR 2025 · 已有 | 多图共同前向，直接预测一致几何，替代两两重建后迭代对齐。 | 解决多视图推理组织问题；“1000+”不等于在任意分辨率、硬件上都廉价。 |
| A05 · P1 | **[MUSt3R](https://arxiv.org/abs/2503.01661)** · 2025-03 / CVPR 2025 · **新增** | 对称化并扩展 DUSt3R，使多视图直接进入共同参考系；多层 memory 支持较大集合和在线模式。 | 连接 batch multi-view 与 memory-based reconstruction；不能与 MV-DUSt3R+ 混为一篇。 |
| A06 · P0 | **[VGGT](https://arxiv.org/abs/2503.11651)** · 2025-03 / CVPR 2025 · 已有 | 用共享几何 Transformer 联合预测相机、深度、点图与 tracks，形成多任务视觉几何骨干。 | 重点读 frame/global attention、相机与几何的一致性，以及参考视图的作用。 |
| A07 · P1 | **[Pow3R](https://arxiv.org/abs/2503.17316)** · 2025-03 / CVPR 2025 · 已有 | 将内参、相对位姿、稀疏或稠密深度作为可选条件；训练时随机提供不同模态子集。 | 思路由“全未知也能做”转向“已知信息也能用”；与 MapAnything 的输入接口对照。 |
| A08 · P0 | **[π³](https://arxiv.org/abs/2507.13347)** · 2025-07 / ICLR 2026 · 已有 | 置换等变地处理图像集合，预测局部几何与无固定参考视图的相机关系，减少参考选择的敏感性。 | 将 gauge、输入置换和尺度归一化分开理解；最终模型使用 VGGT 初始化。 |
| A09 · P0 | **[MapAnything](https://arxiv.org/abs/2509.13414)** · 2025-09 · 已有 | 以 depth、local rays、poses、metric scale 的分解表示，统一不同先验输入和多种三维任务。 | 为什么要分解输出？哪些任务共享监督？metric scale 如何获得？ |
| A10 · P0 | **[Depth Anything 3](https://arxiv.org/abs/2511.10647)** · 2025-11 · **新增** | 使用普通 Transformer 与统一的 depth-ray 预测目标，通过 teacher-student 训练学习任意视图的空间一致几何。 | 与 VGGT 多头多任务、MapAnything 分解输出做三方比较；支持已知或未知相机位姿。 |
| A11 · P1 | **[Pi3X](https://github.com/yyfz/Pi3)** · 2025-12-28 官方工程升级 · **新增版本** | 卷积输出头减轻格状伪影；改进连续置信度，支持内参／位姿／深度条件及近似 metric scale。 | 放在 π³ 版本记录中；不要把工程升级、原论文主实验和后续 checkpoint 混用。 |
| A12 · P0 | **[VGGT-Ω](https://arxiv.org/abs/2605.15195)** · 2026-05 / CVPR 2026 · **新增** | 简化 dense head，以 registers 承担部分跨帧交流，降低训练开销，再扩大监督数据与无标注视频训练，覆盖静态和动态场景。 | 核心是架构效率与数据 scaling 如何相互促成；部分 register attention 不等于所有计算都线性。 |

**版本备注：** VGGT-Ω 作者页面在 **2026-09-18** 公告新增训练代码与一次额外训练的 checkpoint，并要求后续 benchmark 比较使用新的参考 checkpoint。精读时将论文表格与具体权重版本分别记下。[作者公告](https://vggt-omega.github.io/)

### B. 在线重建：记忆、参考系与长程漂移

| ID / 优先级 | 论文、首次公开时间 | Core idea / contribution | 读点与设定边界 |
|---|---|---|---|
| B01 · P1 | **[Spann3R / 3D Reconstruction with Spatial Memory](https://arxiv.org/abs/2408.16061)** · 2024-08 · **新增** | 用外部 spatial memory 保存已见场景信息，下一帧查询记忆后直接输出全局 pointmap，省去 DUSt3R 式全局对齐。 | 在线分支的概念起点：记忆存什么、怎样检索和更新？ |
| B02 · P0 | **[CUT3R / Continuous 3D Perception Model with Persistent State](https://arxiv.org/abs/2501.12387)** · 2025-01 · **新增** | 持续更新隐状态，从输入流产生同一参考系中的 metric pointmap，还可用虚拟视角查询未直接观察区域。 | 理解“场景状态可查询”；它是递归推理，不是整段视频一次 batch，也不保证无限长度无漂移。 |
| B03 · P1 | **[SLAM3R](https://arxiv.org/abs/2412.09401)** · 2024-12 · **新增** | 滑窗恢复局部点图，再由学习式 local-to-world 模块逐步对齐和形变，直接建立全局几何。 | 与 MASt3R-SLAM 对照：学习式注册与显式相机／图优化的分工不同。 |
| B04 · P1 | **[STream3R](https://arxiv.org/abs/2508.10893)** · 2025-08 · **新增** | 将顺序 pointmap 预测写成 decoder-only causal Transformer，使用因果注意力组织历史观测。 | 从递归固定状态转向序列 Transformer；仔细记录 cache 是否随序列增长及其管理方式。 |
| B05 · P1 | **[LongStream](https://arxiv.org/abs/2602.13172)** · 2026-02 · **新增** | 以关键帧相对位姿代替首帧锚定；分离尺度学习，并用 cache-consistent training 与周期刷新减轻长程退化。 | 把长程难题拆成参考系外推、尺度漂移和缓存污染；适合作为读 LingBot-Map 前的对照。 |
| B06 · P0 | **[LingBot-Map](https://arxiv.org/abs/2604.14141)** · 2026-04，v3 为 2026-09 · **新增** | Geometric Context Transformer 分设 anchor context、pose-reference window、trajectory memory，分别处理坐标锚定、局部几何和长程漂移。 | 重点分析三种 context 的必要性和存储成本，区分紧凑记忆与无限时长一致性保证。 |
| B07 · P1 | **[ABot-Recon / Revisiting Local Context for Long-Horizon Streaming 3D Reconstruction](https://arxiv.org/abs/2608.27529)** · 2026-08 · **新增** | 仅缓存前 11 帧，预测当前相机系点图和相邻相对位姿；用时序旋转精化与多步组合监督减轻漂移。 | 很有价值的反向对照：长视频性能是否必须依赖长期记忆，还是预测目标与训练方式更重要？ |

### C. 可扩展计算：稀疏 attention 与 TTT 场景记忆

| ID / 优先级 | 论文、首次公开时间 | Core idea / contribution | 读点与设定边界 |
|---|---|---|---|
| C01 · P1 | **[Speed3R](https://arxiv.org/abs/2603.08055)** · 2026-03 · **新增** | 双分支 attention：压缩分支形成粗上下文，选择分支只对最有信息的 token 做精细交互；可用于 VGGT 和 π³。 | 信息选择的速度—精度取舍；区分减少常数、降低有效 token 数与改变渐近复杂度。 |
| C02 · P1 | **[VGG-T³](https://arxiv.org/abs/2602.23361)** · 2026-02 / CVPR 2026 · **新增** | 将不断增长的 KV 场景表示经 TTT 压入固定大小 MLP，使离线多视图聚合实现对视图数的线性扩展。 | 是 offline 全局聚合路线；为什么固定容量状态还能保留几何？与 online 因果限制分开讨论。 |
| C03 · P0 | **[ZipMap](https://arxiv.org/abs/2603.04385)** · 2026-03 / CVPR 2026 · **新增** | 用 TTT 层将图像集合写入紧凑场景状态，支持线性时间、双向重建及状态查询，并提供 streaming 扩展。 | 同时看“写入”和“查询”成本；主模型的双向处理与专门 streaming 版本不应混用。 |
| C04 · P1 | **[Scal3R — Scalable Test-Time Training for Large-Scale 3D Reconstruction](https://arxiv.org/abs/2604.08542)** · 2026-04 / CVPR 2026 · **新增** | 在分块 VGGT 中加入可测试时更新的 Global Context Memory，并同步各块的上下文更新，使局部预测获得远程场景信息。 | 不是只换一个 attention 层；要把分块、全局上下文同步和对齐成本一起计入系统。[方法页](https://zju3dv.github.io/scal3r/) |

**值得做的一张比较表：** 原始 dense attention、Speed3R、VGG-T³、ZipMap、Scal3R 分别把场景信息放在“全部 tokens / 被选 tokens / MLP fast weights / 隐状态 / 分块共享上下文”的哪里？在固定分辨率下，时间、显存和可回溯查询能力如何变化？这是研究问题，不预设所有方法在相同设定下都能线性扩展。

### D. 几何优化混合系统：作为强对照保留

| ID / 优先级 | 论文、时间 | Core idea / contribution | 为什么放在这一类 |
|---|---|---|---|
| D01 · P1 | **[VGGSfM](https://vggsfm.github.io/)** · CVPR 2024 · 已有 | 从多视图 tracks 同时初始化相机，再三角化并以可微 BA 精化，构成可端到端训练的 SfM。 | “可微经典结构”与“直接 pointmap 回归”的代表性对照。 |
| D02 · P0 | **[MASt3R-SLAM](https://arxiv.org/abs/2412.12392)** · 2024-12 · **新增** | 把 MASt3R 几何和匹配先验放入跟踪、局部融合、回环与二阶全局优化系统。 | 保留显式优化能带来什么？也是判断纯前馈模型能力边界的重要基线。 |
| D03 · P2 | **[S-MUSt3R](https://arxiv.org/abs/2602.04517)** · 2026-02 · **新增** | 不重新训练 MUSt3R，通过序列分段、段间对齐和轻量回环优化扩展长视频重建。 | 体现“强基础模型 + 简洁后端”；不是 MUSt3R 自身已解决全部长程问题。 |
| D04 · P1 | **[Scal3R — Learning Efficient Multi-Relative Pose Query for Scalable Online 3D Reconstruction](https://arxiv.org/abs/2609.04201)** · 2026-09 / ECCV 2026 · **新增** | 冻结 backbone，用轻量 token 查询相对多个历史关键帧的位姿，再用在线 pose graph 与回环抑制漂移。 | 与 C04 同名但不同论文！其观察是局部深度仍可靠、全局位姿先崩溃；明确含优化后端。 |
| D05 · P2 | **[GRF-Recon](https://arxiv.org/abs/2609.20012)** · 2026-09 / ECCV 2026 · **新增** | 单目先验通过 LoRA 改善局部细节；全局 ray-field 约束和轨迹拼接优化加强跨帧一致性。 | 面向长程精度的系统路线；不能把含 ray-error 优化的总流程标成“一次前向”。 |

### E. 动态 4D：从逐时刻几何走向运动与轨迹

| ID / 优先级 | 论文、首次公开时间 | Core idea / contribution | 输出与读点 |
|---|---|---|---|
| E01 · P0 | **[MonST3R](https://arxiv.org/abs/2410.03825)** · 2024-10 · **新增** | 将 DUSt3R 微调为逐时间点预测 pointmap，以较少动态数据学习运动场景几何，再设计视频任务的全局优化。 | 动态分支起点；没有显式运动表示也能处理运动，但逐帧几何不自动给出同一物理点的长程轨迹。 |
| E02 · P1 | **[Easi3R](https://arxiv.org/abs/2503.24391)** · 2025-03 · **新增** | 利用 DUSt3R attention 中已有的相机／物体运动信息，在推理时做 attention adaptation，分离动态区域与运动。 | “无需重新训练”的路线；记录其完整推理步骤，不能把 training-free 直接等同 optimization-free。 |
| E03 · P1 | **[4DGT](https://arxiv.org/abs/2506.08015)** · 2025-06 · **新增** | 从真实单目 posed videos 学习 4D Gaussian Transformer，以统一时空 Gaussian 建模静态和动态内容，并通过密度控制与滚动窗口扩展。 | 可渲染的动态表示；输入为有相机位姿的视频，与直接从 unposed RGB 恢复相机的任务不同。 |
| E04 · P0 | **[Any4D — Unified Feed-Forward Metric 4D Reconstruction](https://arxiv.org/abs/2512.10935)** · 2025-12 · **新增** | 把局部 depth / intrinsics 与全局 extrinsics / scene flow 分解建模，联合恢复多帧稠密 metric 几何与运动，可接入深度、IMU 位姿及 Radar Doppler 等条件。 | 连接 MapAnything 的统一输入思路与 4D；核对各传感器条件下的结果，勿将条件增强结果当 RGB-only 结果。 |
| E05 · P0 | **[4RC](https://arxiv.org/abs/2602.10094)** · 2026-02 · **新增** | 视频只编码一次；条件 decoder 可按查询帧和目标时刻读出几何与运动，用基础几何加时间相关相对运动构成表示。 | 关注 encode-once / query-anywhere-anytime，以及查询成本；主干编码整段视频不等于在线因果推理。 |
| E06 · P1 | **[UFO-4D](https://arxiv.org/abs/2602.24290)** · 2026-02 / ICLR 2026 · **新增** | 从两张 unposed 图像预测动态 3D Gaussians 与相机；在同一组 primitives 上渲染外观、深度和运动，使多种监督相互约束。 | 几何—运动—外观统一表示的代表；两时刻插值能力与长视频轨迹能力分开评估。 |
| E07 · P1 | **[Point4D](https://arxiv.org/abs/2609.09145)** · 2026-09 · **新增** | 用三维坐标查询 motion decoder，将一个视频块的预测轨迹终点直接作为下一块查询，并复用可见时刻的视觉描述子。 | 从短窗口 4D 走向长程运动：遮挡、跨块误差传播、重查询机制值得精读；新预印本。 |

**推荐对照顺序：** MonST3R（逐时刻几何）→ Any4D（稠密几何与 scene flow）→ 4RC（条件查询）→ Point4D（跨块长轨迹）；若更关心 rendering，转向 4DGT → UFO-4D。

### F. 可渲染场景：从 posed sparse views 到 unconstrained views

| ID / 优先级 | 论文、首次公开时间 | Core idea / contribution | 输入条件与读点 |
|---|---|---|---|
| F01 · P1 | **[pixelSplat](https://arxiv.org/abs/2312.12337)** · 2023-12 · **新增** | 从图像对预测 Gaussian radiance field；预测三维位置概率分布并可微采样 Gaussian 均值，缓解稀疏 primitive 的优化困难。 | 以已知相机的图像对进行泛化 NVS；适合建立“前馈预测显式辐射场”的概念。 |
| F02 · P0 | **[MVSplat](https://arxiv.org/abs/2403.14627)** · 2024-03 · **新增** | plane-sweeping cost volume 提供跨视图几何证据来预测 Gaussian 中心，联合预测其余属性，仅用 photometric supervision 训练。 | 有相机几何的多视输入；读清 cost volume 这个显式几何先验如何改善 Gaussian 学习。 |
| F03 · P1 | **[Splatt3R](https://arxiv.org/abs/2408.13912)** · 2024-08 · **新增** | 在 MASt3R 的点图几何上预测额外 Gaussian 属性；通过几何学习再接 NVS 训练，将几何基础模型变为可渲染模型。 | uncalibrated 图像对；理解先稳住几何再学外观，以及用于外推视角的 loss masking。 |
| F04 · P0 | **[NoPoSplat](https://arxiv.org/abs/2410.24207)** · 2024-10 · **新增** | 直接把各输入视图的 Gaussians 预测到一个 canonical camera space，避免先逐视图预测再靠外参变换；以内参 token 提供条件。 | 无输入外参，但使用内参；重建与其另设的 coarse-to-fine pose estimation 流程要分别记录。 |
| F05 · P1 | **[FLARE](https://arxiv.org/abs/2502.12138)** · 2025-02 · 已有 | 以相机估计为桥梁，级联条件化几何与外观学习，同时使用 geometry 与 novel-view objectives。 | 与 NoPoSplat 对照“先相机后几何”和“直接 canonical Gaussians”；2–8 张未标定稀疏视图。 |
| F06 · P0 | **[AnySplat](https://arxiv.org/abs/2505.23716)** · 2025-05 · **新增** | 从未标定图像集合共同预测 3D Gaussians 与每幅图的内外参，统一几何、外观和相机输出。 | 为通用几何主线补上可直接 rendering 的出口；比较稀疏／稠密视图与相机误差的影响。 |
| F07 · P1 | **[tttLRM](https://arxiv.org/abs/2602.20160)** · 2026-02 · **新增** | 将多视观测写入 TTT fast weights，形成可解码到 GS 的隐式场景状态；NVS 预训练可迁移到显式三维重建，并支持逐步更新。 | 与 ZipMap 对照相同记忆思想在 geometry 与 renderable reconstruction 中的使用；核对相机条件，不因名称推断 pose-free。 |

**评价不能只看 PSNR：** 这里的主要目标常是图像合成。几何正确性、相机精度、跨视角一致性与渲染画质应分别看；渲染得好不等于点云、尺度或表面都准确。

### G. 监督来源、模型理解与可靠性

| ID / 优先级 | 论文、首次公开时间 | Core idea / contribution | 为什么值得补 |
|---|---|---|---|
| G01 · P0 | **[On Geometric Understanding and Learned Priors in Feed-forward 3D Reconstruction Models](https://arxiv.org/abs/2512.11508)** · 2025-12，v2 为 2026-03 · **新增** | 对 DUSt3R、VGGT、DA3 做特征 probe、attention 分析和干预，发现中间层的极线几何及其与对应关系的因果联系，并测试遮挡等输入扰动。 | 用实验回答“几何推理与数据先验各起什么作用”，避免只凭可视化判断理解能力。 |
| G02 · P1 | **[NAS3R / From None to All: Self-Supervised 3D Reconstruction via Novel View Synthesis](https://arxiv.org/abs/2603.27455)** · 2026-03 · **新增** | 在无 GT 几何／相机标注、无预训练先验的基本设置下，共享网络预测 Gaussian 和相机，用预测相机渲染目标视图；mask attention 与 depth-based Gaussians 帮助稳定训练。 | 研究不用昂贵三维标签能否学出相机与几何；需同时检查精度上限和稳定收敛的条件。 |
| G03 · P1 | **[Reliev3R](https://arxiv.org/abs/2604.00548)** · 2026-04 / CVPR 2026 · **新增** | 用预训练模型给出的单目相对深度与稀疏对应作为弱监督，结合歧义感知深度损失和三角几何重投影损失学习多视一致性。 | 不依赖多视几何标注，但依赖预训练教师；与 NAS3R 的“无先验”设定清楚区分。 |
| G04 · P1 | **[GeoCond](https://arxiv.org/abs/2609.18465)** · 2026-09 · **新增** | 冻结重建 backbone，在预测几何上训练轻量可靠性 adapter，输出位姿不确定性及 refinement gate，用于选择何时精化。 | 低视差、低重叠和大旋转下，原生 confidence 未必能反映几何病态；新预印本，适合方法和评估设计精读。 |
| G05 · P2 | **[Motion- and Gravity-Aware Feedforward 3D Reconstruction](https://arxiv.org/abs/2610.22177)** · 2026-10-15 · **新增** | 训练时用残差光流、重力方向作为 privileged information 引导几何表征；推理时只需要视觉输入。 | 最新观察项：训练时物理先验能否补足歧义？本次仅做摘要级纳入，暂不据此更换主线基线。 |

### H. 支撑与邻接方向：保留，但不与场景多视几何混排

| ID / 优先级 | 论文、首次公开时间 | Core idea / contribution | 在阅读体系中的位置 |
|---|---|---|---|
| H01 · P2 | **[Depth Anything](https://arxiv.org/abs/2401.10891)** · 2024-01 · 已有 | 利用大规模无标注数据的伪标签与语义先验提升单目深度泛化。 | 回顾数据 scaling；原版单目深度与 A10 的 DA3 任意视图几何是不同阶段。 |
| H02 · P1 | **[MoGe](https://arxiv.org/abs/2410.19115)** · 2024-10 · 已有 | 单图预测对全局尺度、偏移不敏感的点图，配合全局对齐及多尺度局部几何监督。 | 理解单目歧义、表示和损失设计；与多视图中可由对应关系约束的几何区分。 |
| H03 · P1 | **[MoGe-2](https://arxiv.org/abs/2507.02546)** · 2025-07 · **新增** | 在保留相对几何质量的同时学习 metric scale，并用合成清晰标签辅助精炼真实数据，改善细节。 | 补齐从 affine-invariant 到 metric monocular geometry 的路径。 |
| H04 · P1 | **[MetricAnything](https://arxiv.org/abs/2601.22054)** · 2026-01 · **新增** | 用随机稀疏深度构造 Sparse Metric Prompt，统一异质传感器和相机来源的预训练，再蒸馏无需 prompt 的学生。 | 数据与尺度支线；不要与 MapAnything 混名，关键是 metric depth pretraining。 |
| H05 · P2 | **[RayDiffusion / Cameras as Rays](https://arxiv.org/abs/2402.14817)** · 2024-02 · 已有 | 以局部 ray bundle 表示相机，连接图像 patch 特征与相机几何，并比较直接回归与扩散去噪。 | 回答“相机怎样参数化”；扩散推理分支不是单次确定性回归。 |
| H06 · P2 | **[Reloc3R](https://arxiv.org/abs/2412.08376)** · 2024-12 · 已有 | 大规模成对相对位姿回归，加轻量 motion averaging 实现定位。 | 位姿头与定位支线；不把它当作完整稠密三维场景恢复。 |
| H07 · P2 | **[LRM](https://arxiv.org/abs/2311.04400)** · 2023-11 · 已有 | 大模型从单图直接预测物体 NeRF，通过大量物体多视图训练获得类别泛化。 | 物体级补全／生成路线；单图不可见部分主要依赖学习先验。 |
| H08 · P2 | **[PF-LRM](https://arxiv.org/abs/2311.12024)** · 2023-11 · 已有 | 从少量 unposed 物体图像共同恢复形状与相机，先预测粗点云，再以可微 PnP 恢复相机。 | 几何 solver 如何嵌入网络的早期对照；原笔记 PR-LRM 应更正为此名称。 |
| H09 · P2 | **[LGM](https://arxiv.org/abs/2402.05054)** · 2024-02 · **新增** | 用多视 Gaussian 特征与高吞吐 U-Net 重建物体，可接多视扩散模型生成的输入。 | 理解图像／文本到 3D 的生成—重建接口；整个生成流程与纯前馈重建阶段分开计时。 |

原笔记中的 **DeMoN、DeepTAM、DeepV2D** 可继续留在“历史背景”页，先用来理解早期深度／运动联合预测即可。本轮不把它们加入优先精读队列。若以后扩展到完整 generalizable neural rendering 历史，再单开 pixelNeRF、IBRNet、MVSNeRF 等支线；若转向 image-to-3D generation，也应单开物体资产生成分支。

## 3. 建议立即执行的阅读顺序

不要同时开启全部 56 个条目。先用下面的层次建立骨架；如果对应已有论文已经精读，可直接跳过复习项。

### 第一阶段：确认表示和坐标系

- [ ] **DUSt3R → MASt3R**（已有）：写清 pointmap、共同坐标系、尺度歧义与 matching 的关系。
- [ ] **VGGT → π³ → MapAnything**（已有）：比较多头联合输出、置换等变、几何因子分解。
- [ ] **Depth Anything 3 → VGGT-Ω**（新增）：检验输出简化、数据规模、registers 各自的收益来自哪里。

产出：一张表，列出每篇的输入先验、输出变量、参考系、损失中的对齐方式、训练初始化和推理后处理。此阶段不以谁的单一 benchmark 数字更高作为主要结论。

### 第二阶段：场景如何跨时间保存

- [ ] **CUT3R → LingBot-Map**：固定隐状态与多种几何上下文的对照。
- [ ] **ZipMap**：测试时更新的权重如何成为可查询场景状态。
- [ ] **MASt3R-SLAM**：保留显式跟踪、回环和优化的参照系。

产出：按整段 batch、在线 causal、双向离线、混合后端四种执行方式比较。然后按兴趣补 STream3R / LongStream / ABot-Recon / VGG-T³ / 两篇 Scal3R。

### 第三阶段：选择一个主要输出方向

- [ ] **几何与运动方向：MonST3R → Any4D → 4RC**；进一步读 Point4D。
- [ ] **可渲染场景方向：MVSplat → NoPoSplat → AnySplat**；进一步读 UFO-4D 或 tttLRM。

两条支线不必同时全读。若你的最终目标是相机、地图或机器人感知，优先前一条；若最终目标是 novel-view synthesis、可漫游场景或视频渲染，优先后一条。

### 第四阶段：寻找可研究的问题

- [ ] **On Geometric Understanding and Learned Priors…**：几何证据与学习先验如何区分。
- [ ] **NAS3R ↔ Reliev3R**：真正的自监督与教师伪标签监督分别能走多远。
- [ ] **GeoCond**：错误预测能否被识别，何时应调用优化后端。

**若只补第一批 10 篇：** DA3、VGGT-Ω、CUT3R、LingBot-Map、ZipMap、MASt3R-SLAM、MonST3R、Any4D、AnySplat、On Geometric Understanding…。这个短名单覆盖现有笔记最明显的空白；不代表其余论文价值更低。4RC、MVSplat / NoPoSplat 随第三阶段方向紧接着读。

## 4. 最新进展的观察队列

以下“新”按首次公开时间或明确版本更新排列，避免用网页爬取时间代替论文时间。

| 时间 | 值得跟进的变化 | 建议动作 |
|---|---|---|
| 2025-11 至 2026-05 | DA3 与 VGGT-Ω：简化输出／信息交换，同时做更大规模训练 | 与 VGGT、π³、MapAnything 共用同一张架构比较表。 |
| 2026-02 至 04 | VGG-T³、ZipMap、Scal3R-TTT、tttLRM：以 fast weights 作为场景记忆 | 将 geometry、rendering、offline、streaming 分开比较。 |
| 2026-03 至 04 | NAS3R、Reliev3R：降低三维监督成本 | 为每个训练阶段记录 GT、伪标签、预训练权重的来源。 |
| 2026-08-27 | ABot-Recon：严格局部上下文的长视频重建 | 与 LingBot-Map 对照，检验长期记忆的必要条件。 |
| 2026-09-03 | Scal3R-RelativePose：多参考位姿查询 + 图优化 | 用全名或 arXiv ID 消歧，不与 Scal3R-TTT 合并。 |
| 2026-09-08 | Point4D：长程三维轨迹；LingBot-Map 发布 v3 | 分别记录新方法与旧论文版本更新。 |
| 2026-09-16 / 17 | GeoCond、GRF-Recon：可靠性判断和几何精化 | 看后端何时有益，以及总成本是否被完整计入。 |
| 2026-09-18 | VGGT-Ω 更新比较用 checkpoint | 后续实验固定权重版本。 |
| 2026-10-15 | Motion- and Gravity-Aware…：训练时引入运动与重力信号 | 暂作新预印本观察，先核验消融与测试输入要求。 |

这份观察队列覆盖本次检索核实的代表性新进展，不声称收齐截至 2026-10-24 的所有投稿。

## 5. 精读时统一使用的比较模板

每篇先回答下面 8 项，通常比先抄网络结构更容易看清真正贡献。

| 字段 | 要记录什么 |
|---|---|
| 任务与输入 | object / scene；single / pair / set / stream；static / dynamic；是否提供 K、pose、depth、IMU 等。 |
| 输出与参考系 | depth / rays / pointmap / Gaussian / flow / trajectory；local / reference / world；relative scale 或 metric。 |
| 信息融合 | pairwise cross-attention、frame/global attention、causal KV、spatial memory、registers、TTT fast weights。 |
| 监督与初始化 | GT 相机／深度／轨迹，photometric loss，伪标签教师，预训练 backbone；无某类标注不代表没有外部先验。 |
| 推理流程 | 前向次数、递归更新、PnP、对齐、BA、pose graph、TTT、Gaussian refinement；哪些是可选项。 |
| 泛化条件 | 训练与测试数据重叠；新场景、新相机、新视差、新物体；输入帧顺序和长度。 |
| 主要证据 | 消融是否同数据、同模型规模、同初始化；gain 来自架构、训练量还是额外先验。 |
| 失败与代价 | 低重叠／低视差／大旋转／遮挡／动态／重复纹理；显存、延迟、随序列增长趋势。 |

### 避免不公平比较的关键检查

- **尺度对齐**：Sim(3) 对齐、median scaling 等会移除部分尺度误差；“对齐后几何很好”不证明恢复了真实 metric scale。
- **轨迹与地图分开**：看 ATE / RPE，也看点云 accuracy、completeness 或 F-score；低轨迹误差不代表稠密表面完整。
- **动态指标分开**：静态背景几何、相机自运动、scene flow、长轨迹遮挡恢复分别评价。
- **NVS 相机来源**：GT target pose、预测 pose、优化后的 pose 不能直接视为同一难度。
- **速度口径**：相同 GPU、分辨率、帧数、精度；明确是否包含图像编码、对齐、优化、场景写入和查询。本文不跨论文拼接速度排行榜。
- **置信度含义**：训练 loss 中的 uncertainty、可见性 mask、点级质量分数、位姿可靠性并不等价。
- **长视频设定**：输入多少帧、缓存多少帧、用不用未来帧、是否重访／回环、是否滑窗和重置，分别写明。

## 6. 建议形成的研究问题

以下是根据上述论文组织出的阅读问题与个人综合判断，不是已经被证明的领域结论。

1. **几何输出是否正在收敛到更简洁的表示？** 对照 VGGT 多任务、π³ 局部点图与相机、DA3 depth-ray、MapAnything 因子分解、VGGT-Ω 简化 head。要区分输出简化和训练监督减少。
2. **长程失败来自记忆不足，还是预测目标不适定？** 对照 CUT3R / LingBot-Map 的记忆设计，与 LongStream / ABot-Recon / Scal3R-RelativePose 的参考系和相对位姿设计。
3. **场景应存成 tokens 还是可学习的状态？** 比较稀疏 attention、TTT memory 在宽基线、重复访问、细节保存和新视图查询中的取舍。
4. **显式几何约束何时仍不可替代？** 将纯前馈输出作为起点，检查 MASt3R-SLAM、GRF-Recon 和 GeoCond 的一致性／可靠性收益，而非预设优化必然有益。
5. **4D 的统一接口是什么？** 每帧 pointmap、scene flow、时刻条件查询与三维轨迹，各自最容易表达和最难表达什么？
6. **不依赖大规模 GT 三维标签能否持续提升？** NAS3R 的纯光度监督、Reliev3R 的教师信号、VGGT-Ω 的数据管线与自监督分别提供不同答案。

## 7. 综述入口与检索记录

推荐先浏览 **[Feed-Forward 3D Scene Modeling: A Problem-Driven Perspective](https://arxiv.org/abs/2604.14025)** 的问题分类和参考文献；首次提交 2026-04-15，v2 更新于 2026-10-10。其[作者维护的索引](https://ff3d-survey.github.io/)可用作后续扩展入口。本文件的分类按你的已有笔记与阅读目标重新组织，不逐项复制综述分类。

本次检索围绕 feed-forward 3D reconstruction / visual geometry、streaming / long sequence、TTT / sparse attention、dynamic 4D、pose-free Gaussian splatting、self-supervision / reliability，并补做 2026 年 8–10 月检索。主要使用 arXiv、CVF、论文作者项目与官方仓库；论文集合网站只用于发现候选，方法描述回到原始来源核对。

来源已逐条附在文献卡中，便于直接打开。最新条目优先保留 arXiv ID 作为稳定身份；同名方法以完整题名消歧。会议年份不用于替代首次公开时间，代码版本更新不用于伪装成新论文。

