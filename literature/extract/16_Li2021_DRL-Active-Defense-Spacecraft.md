# 16 | Cooperative Guidance Strategy for Active Defense Spacecraft with Imperfect Information via Deep Reinforcement Learning

> Li Z., Liang H., Wu J., Wang J. (Sun Yat-sen University, Guangzhou), Zheng Y. (Science and Technology on Space Physics Laboratory, Beijing) | arXiv:2212.03093 (v1, 2021-12) | 文中未注明期刊/会议出处(为 AIAA 期刊风格预印本,含 Nomenclature、Lemma/Remark 体例)
> 注:以下页码 p.X 均指 PDF 页码(共 27 页);式(XX)指原文公式编号。

## 0. 一句话定位

DRL 版主动目标防御(target–defender–interceptor,TDI)论文:用**单个 TD3 agent 同时生成目标航天器 T 与防御飞行器 D 的制导指令**(action = [u_T, u_D], p.12),对抗采用最优导引律(OGL)的拦截弹 I,并在 T/D 一侧引入"乘性噪声 + 掩模"的不完美信息模型(p.12–13)。与博弈论方法的关系:**基线含解析博弈/最优导引策略**——win-rate 基准是 SOGL(式(34),引 [20] Qi et al.),实时性对照是 LQOGL(引理 1,引 [3] Liang et al. 的微分博弈最优导引);Garcia–Casbeer–Fuchs–Pachter 的主动防御微分博弈工作 [7] 仅在引言作为背景引用(p.3),并非实验对手。论文明确以"OGL 家族假设完美信息、先验知识苛刻"(Remark 1, p.10)为动机,把**非对称信息结构**(I 完美信息、T/D 不完美)作为对博弈论/最优控制方法的差异化卖点。

## 1. 问题建模

- **参与者与团队结构**:1 个目标航天器 T(target)、1 个主动防御飞行器 D(defender / active protection vehicle / ADV)、1 个高机动小航天器作为拦截弹 I(interceptor);无诱饵(p.5)。T+D 组成完全合作联盟("target pair", zero-sum strictly competitive game, p.11、13);**同一个训练好的 agent 被分配给 T 和 D**(p.12)。
- **状态量/观测量**:
  - MDP 定义为 7 元组 {s, o, a, P_sa, R, Ω, γ},o_t ∈ O^m 是 s_t 的(不完美)观测,策略为状态反馈 π: O→A, a_t = π(o_t)(Sec. III.A, p.11)。
  - 完美信息模型的状态 s_t = [y_t, V_t, a_t, a_max, τ]^T(式(29), p.12),即相对信息状态 + 拦截时间。
  - 线性化交战状态向量 x = [y_IT, ẏ_IT, y_ID, ẏ_ID, a_I, a_T, a_D](式(7), p.7),其中 y_IT、y_ID 为垂直于 X 轴的相对距离分量。
  - **imperfect information 的具体含义**(Sec. II.B.2 / III.A.2, p.12–13):不是时延,而是 (a) T/D 一侧的先验知识被删除(掩模 Γ),(b) 观测被测量噪声污染:o_t = Ω(s_t) = Γ s_t × (I + ω_{o,t}) = [y_t; V_t; a_t] × [δy_{o,t}; δV_{o,t}; δa_{o,t}],ω_{o,t} = [δy; δV; δa] ~ U(0_9, Σ) ∈ R^9,Σ = [σ_y I_3, σ_v I_3, σ_a I_3]^T,σ_y, σ_v, σ_a 非负(式(30), p.13;该式与动作空间的式(30)编号重复)。即**逐元素乘性均匀噪声 + 掩模**的部分可观测模型。I 一侧保持完美信息(Remark 1, p.10)。agent 实际观测为 13 维向量(p.18),但 13 个分量的具体构成未列。
- **动作空间**:action = [u_T, u_D](式(30), p.12),**连续**;actor 输出层 2 个单元,分别对应 T 和 D 的"uniform guidance command"(p.18),幅值受 u_i^max 约束(式(6))。
- **动力学模型**(端末段,平面,非 CW 方程):
  - 极坐标运动学(I-T 与 I-D 两个碰撞三角形,式(1)(2), p.6);
  - 航迹角动力学 φ̇_i = a_i/V_i, i ∈ {I, T, D}(式(3), p.6);
  - 绕初始视线线性化(式(4)(5), p.6),得 ẋ = Ax + B[u_I, u_T, u_D]^T(式(8)(9a)(9b), p.7),A 为 7×7(ẏ_IT 行含 a_I − a_T,ẏ_ID 行含 a_I − a_D,加速度行含 −1/τ_i),B = [0_{5×3}; diag(1/τ_I, 1/τ_T, 1/τ_D)];
  - 各玩家一阶动力学 å_i = −(a_i − u_i)/τ_i(式(6), p.7);
  - 恒速 → 固定时间交战:预测拦截时间 t_fIT = ρ_IT^0/(V_I+V_T),t_fID = ρ_ID^0/(V_I+V_D)(式(10), p.7),t_goIT = t_fIT − t, t_goID = t_fID − t(式(11), p.7);
  - 二维(3D 简化为平面, p.5);仿真中玩家绕地球圆轨道运动,**仿真计入引力**(p.19)。
- **奖励函数**(p.13–14):
  - r_medium = |Z_IT/α_1|^{β_1} − |Z_ID/α_2|^{β_2}(式(31), p.14):Z_IT 增大或 Z_ID 收敛到 0 则奖励增大;
  - r_terminal = +σ(成功)/ −σ(否则)(式(32), p.14);成功 = 拦截弹被 D 摧毁(t = t_fID)或被 D 驱离且未能命中 T(p.14);
  - σ ≥ c/γ^n(式(33), p.14):若期望 agent 提前 n 步预见到终端奖励,则折扣后的终端奖励须超过 r_medium 的界 [−c, c]。
- **约束**:控制幅值 u_i ≤ u_i^max(式(6)上下文, p.7);杀伤半径(判定)由 Table 3 给出(p.20):拦截弹 0.25 m、目标 0.5 m、防御器 0.25 m;η 为 I-D 切换阈值、"always equal to the defender kill radius"(p.9)。**未提及**视场约束与避碰约束。
- **噪声/时延**:乘性均匀测量噪声 + 掩模(式(30), p.13),六组噪声算例(Table 5, p.25);**无时延建模**(未提及);完美信息模型下 T–D 之间通信"ideal and occur with no lag"(p.12)。

## 2. 假设条件

1. 端末段(endgame)所有玩家为恒速质点,轨迹可绕初始视线线性化,三维交战简化为平面;"in most cases those hypotheses will not harm the result generality [19]"(p.5)。
2. 各玩家动力学为一阶过程,时间常数 τ_i,制导指令界 u_i^max(p.6–7, 式(6))。
3. 各玩家速度恒定 → 交战为固定时间过程,拦截时间由初始距离/速度和按式(10)计算(p.7)。
4. **拦截弹拥有关于 T 和 D 的完美信息**(相对状态与机动性:最大加速度、时间常数);**T 和 D 的观测不完美且含噪**(p.12–13;Remark 1, p.10)。
5. T 与 D 完全合作,两者间通信理想且无滞后(p.12)。
6. 同一训练好的 agent 同时配给 T 和 D(p.12)。
7. 交战为严格竞争的零和博弈,pursuit-evasion 奖励天然稀疏(p.13)。
8. **拦截弹策略**:训练时采用最优导引且"足够激进"("the interceptor was employed with the optimal guidance and is sufficiently aggressive", p.13);课程分三阶段——不机动(0g)→ 方波信号(6g)→ OGL(2g/4g/6g)(Table 1, p.15);评估时拦截弹用 SOGL/LQOGL(引理 1/2, p.8–10)。拦截弹策略**不可学习**(非对抗训练、无自博弈)。
9. 实验场景:所有玩家绕地球圆轨道运动,仿真计入引力;假设拦截弹机动性与时间常数优于 T 和 D(p.19)。
10. 信息不完美的数学处理 = 掩模 Γ + 乘性均匀测量噪声 U(0_9, Σ)(式(30), p.13);噪声幅值 Σ = [σ_y I_3, σ_v I_3, σ_a I_3]^T。
11. 奖励超参 α_1, α_2, β_1, β_2, σ 非通用——玩家数量与机动性会完全改变环境(p.14)。
12. LQOGL 的 K(t)、P(t) 中 ω_1, ω_2, ξ_1, ξ_2 为非负常数,保证拦截弹趋向目标并躲开防御器(p.9, 式(18)(19))。

## 3. 方法核心

机制一句话:**把 T+D 联盟当成一个单 agent,用 TD3(model-free、off-policy、actor-critic,Fujimoto et al. [25])端到端学一个 13 维观测 → 2 维连续指令 [u_T, u_D] 的确定性策略;用"非稀疏塑形奖励 + 由易到难课程(拦截弹从不动到 OGL)"解决零和博弈奖励极稀疏的难题;训练环境是线性化端末交战模型,部署时同一网络分别装在 T、D 上。**选择 TD3 的理由:模型-free 适合 P_sa、Ω、扰动分布无法显式表达的不完美信息问题;off-policy 比 PPO 更省样本、与课程学习契合(p.15)。集中式还是分布式:**训练与决策均为"集中"式单策略**(一网络出两指令),而非多智能体独立学习(p.12)。

关键公式:
- ZEM:Z_IT(t) = L_1 Φ(t, t_fIT) x(t),Z_ID(t) = L_2 Φ(t, t_fID) x(t)(式(12), p.8),L_1 = [1 0 0 0 0 0 0], L_2 = [0 0 1 0 0 0 0](式(13), p.8);展开式(14), p.8:Z_IT = x_1 + t_goIT x_2 + a_I τ_I² φ(t_goIT/τ_I) x_5 − a_T τ_T² φ(t_goIT/τ_T) x_6,Z_ID 同理(x_3, x_4, x_5, x_7);Ż_IT = τ_I φ(t_goIT/τ_I) u_I − τ_T φ(t_goIT/τ_T) u_T,Ż_ID 同理(式(15), p.8);φ(χ) = e^{−χ} + χ − 1(式(16), p.8)。
- 引理 1 LQOGL(式(17)–(19), p.8–9):u_I* = −K(t)Z_ID(t)/ω_1 · u_I^max τ_I φ((t_f2−t)/τ_I),当 ‖Z_ID‖ < η;否则 u_I* = −P(t)Z_IM(t)/ξ_1 · u_I^max τ_I φ((t_f1−t)/τ_I);K(t)、P(t) 为含 φ 函数平方的积分倒数(式(18)(19), p.9)。
- 引理 2 SOGL(式(20), p.9):u_I* = u_I^max sgn[Z_ID(t_fID)] sgn[φ((t_fID−t)/τ_I)](‖Z_ID‖<η 时,躲 D 模式);否则 u_I* = −u_I^max sgn[Z_IT(t_fIT)] sgn[φ((t_fIT−t)/τ_I)](打 T 模式)。推导:J_1 = −½Z_ID²(t_fID) / J_2 = ½Z_IT²(t_fIT)(式(21)),H_1 = λ_1 Ż_ID(式(22)),costate 与横截条件(式(23)(24)),p.9–10;合并式(28), p.10。
- T/D 基准 SOGL(式(34), p.22):u_T = −u_T^max sgn[Z_IT(t_IT)] sgn[φ((t_IT−t)/τ_T)],u_D = u_D^max sgn[Z_ID(t_ID)] sgn[φ((t_ID−t)/τ_D)](t_IT、t_ID 为预测拦截时间)。
- MDP/回报:R_t = Σ_{i=t}^{T} γ^{i−t} r_i(p.11);J(φ) = E_{τ~π_φ}[R_0^τ](p.15);确定性策略梯度 ∇_φ J = E[∇_a Q(s,a)|_{a=μ(s)} ∇_φ μ(s)](p.16);Bellman 目标 U = r + γQ'(s', μ̃'(s'))(p.16)。
- TD3 三件套(p.17):clipped double Q:U = r + γ min_{i=1,2} Q'_i(s', μ̃'(s'));delayed policy update + soft update:θ' ← τθ + (1−τ)θ';target policy smoothing:U = r + γQ'(s', μ̃'(s') + ε),ε 为截断高斯噪声。探索噪声为 OU 噪声(Fig. 3, p.18)。
- 网络结构(p.18):观测 13 维;actor 与 critic 均为 3 层全连接(64、256、512)+ layer normalization;隐层 ReLU、输出层线性;actor 输出 2 单元(u_T, u_D),critic 输出 1 单元。结构为启发式设计,"deeper and wider network is avoided for real-time performance and fast convergence"。
- 训练流程(p.13–15、20):随机初始化策略网络 → 课程 Stage 1(拦截弹不动,0~100 episodes)→ Stage 2(方波指令,6g,101~1000)→ Stage 3(OGL,2g/4g/6g,其余)→ 共 20000 episodes,8 个并行 worker、12 h,硬件 104 核 Xeon Platinum 8270 @2.70 GHz;每 100 episodes 存一次权重;每个配置 6 个随机种子(p.20)。

## 4. 理论结果

DRL 部分无定理,也无学习收敛性/稳定性的理论分析。解析部分为:
- 引理 1(LQOGL,[3] 的结果):证明援引 [3] Theorem 1("The detailed proof of similar results can be found in [3]", p.9)。
- 引理 2(SOGL,[20]):给出基于 PMP 的完整推导(J_1/J_2 分段代价、Hamiltonian、costate、横截条件,式(21)–(27), p.9–10),合并得式(28)。
- Remark 1(p.10):LQOGL 需解 Riccati 微分方程,更新频率无法满足实时航天器制导;SOGL 无 Riccati、无超参,计算效率与鲁棒性更好,代价是灵活性差且出现 chattering;OGL 家族普遍假设完美信息与先验知识,故实际中难以应用——因此选 SOGL 作基准。
- Remark 3(p.24):SOGL"stable but inflexible"(由理论框架 [27] 与苛刻假设 [28] 所致);RL 方法灵活、可持续优化,且对时间常数独立,所需先验知识更少。
- 经验性"收敛/稳定"结论:非稀疏奖励 + 课程使学习曲线稳定上升、缓解持续训练导致的过拟合(win rate 99%→70% 后回升/稳定)(p.21–22)。

## 5. 实验设置

- **场景参数**(Table 3, p.19–20 + Sec. IV.A):T 高度 500 km,D 500.1 km,I 初始高度在 499.8~500.2 km 内随机化;各玩家水平初速 V_I = V_T = V_D = 7.6 km/s(I 方向为 −7.6 km/s,迎头);I–T 水平初始距离 300 km 时交战开始;D 在交战开始时即刻发射、位于 T 前方 120 km(即 I–D 初始 180 km);最大加速度 u_I^max = 6g = 60 m/s²,u_T^max = 1g = 10 m/s²,u_D^max = 2g = 20 m/s²;时间常数:正文 p.19 写 τ_M = τ_D = 10 ms、τ_I = 5 ms,**但 Table 3(p.20)写 I 0.05 s、T 0.1 s、D 0.02 s**——两处矛盾(见第 6/8 节);kill radius:I 0.25 m、T 0.5 m、D 0.25 m。
- **对比基线**:① SOGL(式(34), p.22)——win-rate 基准,确定性环境中 win rate 87.0%(p.22);② LQOGL——仅用于计算耗时对比(Table 4, p.20):LQOGL 2.773 s/1e3 步(360 Hz),SOGL 0.0145 s(6.9×10^4 Hz),RL 方法 0.910 s(1.1×10^3 Hz)。**有博弈论渊源的基线**(SOGL 出自 defended-target 攻防博弈文献 [20],LQOGL 出自微分博弈策略文献 [3]),但没有任何实验让拦截弹采用博弈论最优策略(如 LQOGL)与 agent 对打;Fig. 8 图例将基线标为 "DG-method"(p.24),与正文 SOGL 称呼不一致。
- **评价指标**:win rate / winning probability(未给出精确判定细则),累积训练回报,计算时长与更新频率。
- **Monte Carlo 规模**:**未给出具体运行次数**(全文仅说 "Monte-Carlo simulation", p.21、25)。
- **训练/学习实验**(Exp 1, p.20–21):三种设置(稀疏奖励 / 非稀疏奖励 / 非稀疏奖励+CL)同超参对比;6 seeds;稀疏奖励下累积回报停留在 −(终端罚);非稀疏 ~6000 episodes 收敛;非稀疏+CL 在课程结束后 1800 episodes(累计 4300)超过无 CL 并取得更高收敛回报。
- **全可观测博弈验证**(Exp 2, p.21–23):无 CL agent 3200 episodes 超基线、~9500 episodes 达峰值 99%,随后跌至 ~70%(过拟合);有 CL agent ~6400 episodes 收敛至 99%。三组典型拦截弹初始位置/来袭方向的样例轨迹(Fig. 5)、ZEM(Fig. 6)与指令(Fig. 7)(p.22–23):T 持续机动充当"诱饵"把 I 引向 D 的杀伤半径。
- **对来弹参数变化的泛化**(Exp 3, p.24):拦截弹最大加速度 30~80 m/s²(Fig. 8(a))、时间常数 0.05~0.002 s(Fig. 8(b));RL 方法在 ≤ 训练值(60 m/s²)时占优,>6g 后"not good enough";RL 方法对 I 的时间常数几乎不敏感(全 1.0),而基线(DG-method/SOGL)随 τ_I 减小从 1.0 跌至 ~0.68。
- **鲁棒性**(Exp 4, p.24–25):六组不完美信息算例(Table 5, p.25):Case 1–3:σ_y = 0,σ_v = 0.05/0.1/0.2,σ_a = 1~3;Case 4–6:σ_y = 0.01/0.02/0.05,σ_v = 0.05~0.45,σ_a = 1(单位未标注)。结论:方位可精确估计(σ_y=0)时,策略对速度/加速度测量噪声不敏感(性能下降 <25%),鲁棒性优于解析法;有方位噪声时策略对速度噪声变敏感,但性能不随方位噪声增大而进一步下降(归因于策略网络对不同观测分量的加权)。

## 6. 局限性

**作者承认的**:
- agent 对拦截弹最大加速度的自适应有限:拦截弹最大加速度超过训练值 6g 后性能不佳(p.24)。
- 奖励超参数取值不通用,随玩家数量与机动性改变,论文只给设计方法不给具体值(p.14)。
- LQOGL 因需解 Riccati 微分方程而不满足实时性(p.10, Table 4 p.20)。
- 未来工作承认未处理:真实航天器传感器噪声、变化的环境动态、燃耗、饱和与 chattering 现象(p.26)。

**我分析的**(推断依据):
- 对手策略空间窄:训练(课程)与评估中拦截弹始终是 OGL 类确定性规律(不动/方波/OGL),所谓 "adaptiveness to interceptor maneuverability" 实质是对 OGL 参数(加速度、时间常数、初始位置)的泛化,而非对任意/自适应策略的鲁棒性;没有博弈论最优对手(LQOGL)参与 win-rate 对抗(依据:Table 1 p.15、Exp 2/3 设置 p.21–24)。
- 信息非对称是单向照顾 I 的:假设 I 拥有完美信息而 T/D 只有含噪观测,评估偏保守;但反向(I 也不完美)与双向不完全信息的博弈场景未测(依据:Sec. II.B.2 p.12–13、Exp 4 p.24–25)。
- 模型链路存在两处"错位":制导模型是无引力平面线性化端末模型(p.5–7),而仿真计入圆轨道引力(p.19);训练环境的动力学实现(Sec. III.A.1 说状态按式(4)~(6)隐式传播)与 Sec. IV 的含引力仿真是否同一环境未明说(依据:p.12、p.19)。
- 数值矛盾:p.19 正文 τ_M = τ_D = 10 ms、τ_I = 5 ms 与 Table 3(0.1/0.02/0.05 s)互相冲突;且 ms 级时间常数相对 ~20 s 的交战时长和 500 km 轨道场景明显"导弹化",物理合理性存疑(依据:两处数值 + 式(10)推算 t_fIT ≈ 300/15.2 ≈ 19.7 s)。
- win rate 判定规则不透明:"interceptor is driven away by the defender and misses the target" 未给出几何/时间判据(依据:p.14);Fig. 4 中 win-rate 曲线纵轴超过 1(至 ~1.25),与概率 ≤1 矛盾,疑似平滑窗口伪影(依据:Fig. 4, p.22)。
- 编辑未定稿痕迹:式(30)编号重复(动作与观测各用一个)、Fig. 3 编号重复(TD3 结构 p.18 与学习曲线 p.21)、Remark 2 缺失(仅 Remark 1、3)、p.16 与 p.18 各有一处 "[引用]" 占位符(依据:全文检索)。
- 式(14) 中 "a_I τ_I² φ(·) x_5" 同时含 a_I 与 x_5(=a_I),与式(15)的量纲不自洽,疑为排版冗余(依据:p.8 式(14)(15) 对照)。
- 泛化测试只动 I 的参数,T/D 自身参数(如 u_D^max、发射时机)与多对多场景未测("two-on-two" 仅作为可扩展性一句话提及, p.25)。

## 7. 可复现性

**已给出**:
- 网络结构:3 层全连接 64/256/512 + layer normalization,ReLU/线性输出,actor 2 维、critic 1 维(p.18)。
- TD3 超参(Table 2, p.18–19):γ = 0.99,学习率 α = 3×10⁻⁴,buffer 5120,batch 128,soft update 系数 5×10⁻³,policy delay 2,train frequency 6000。
- 观测构造:13 维 + 不完美信息模型(式(30),掩模+乘性均匀噪声)与六组噪声算例(Table 5)。
- 奖励结构(式(31)–(33))与课程表(Table 1:阶段、拦截弹指令、最大加速度、episode 区间)。
- 场景参数(Table 3)与训练规模(20000 episodes、8 workers、12 h、6 seeds、硬件型号)。
- 算法实现:stable baselines 的 TD3(p.18)。

**缺失**:
- 奖励超参 α_1, α_2, β_1, β_2, σ 的具体数值(p.14 明说只给方法);c 与 n 的取值。
- 13 维观测的具体分量列表(p.18 只给维数)。
- 掩模矩阵 Γ 的具体形式(哪些先验量被删)。
- OU 探索噪声参数;MDP 决策步长 dt 与 episode 长度;仿真积分步长与引力模型细节。
- Monte-Carlo 次数与 win rate 的精确定义/判定阈值。
- Table 5 噪声参数的单位/归一化方式。
- 正文与 Table 3 冲突的时间常数取值(以哪个为准)。
- 代码未开源(全文无代码链接)。

## 8. 待验证

1. 13 维观测的可能构成(例如 [y_IT, ẏ_IT, y_ID, ẏ_ID, a_I, a_T, a_D, u_T^max, u_D^max, τ_I, τ_T, τ_D, t_go] 一类的拼法)——原文未列,纯推测。
2. 式(30) 中 ω ~ U(0_9, Σ) 按字面是**单侧**(乘子 1+δ ≥ 1,观测系统性偏大);作者是否本意为对称区间 [−Σ, Σ] 需对照代码或后续版本。
3. 训练环境究竟使用线性化 EOM 隐式传播(Sec. III.A.1)还是含引力的圆轨道仿真(Sec. IV),还是"线性化模型训练 + 含引力仿真评估"。
4. Fig. 8 图例 "DG-method" 与正文 "SOGL" 是否同一基线(DG 或指 differential game,可能沿用 [3] 的 DGL 称呼)。
5. 时间常数以 p.19 正文(5/10 ms)还是 Table 3(0.05/0.1/0.02 s)为准。
6. Fig. 4 纵轴 >1 的 win-rate 曲线是绘图/平滑伪影,还是纵轴实为别的量(如相对比率)。
7. η 在实验中是否直接取 D 的 kill radius 0.25 m(p.9 说 "always equal to the defender kill radius",但未给出数值代入)。

## 9. 记号表

| 原文符号 | 含义 | 首次出现位置 |
|---|---|---|
| a | 加速度, m/s² | Nomenclature p.2;Fig. 1 p.5 |
| ac | agent 的动作 | Nomenclature p.2 |
| A, B | 线性化运动方程的状态空间模型 | Nomenclature p.2;式(9a)(9b) p.7 |
| H | Hamiltonian | Nomenclature p.2;式(22) p.9 |
| I | 单位矩阵 | Nomenclature p.2;式(30) p.13 |
| J(·) | 代价函数 | Nomenclature p.2;式(21) p.9 |
| L_1, L_2 | 从状态提取 ZEM 的行向量 | 式(13) p.8 |
| LOS_IT, LOS_ID | I–T、I–D 视线 | p.5 |
| Q(·) | Q 值函数 | Nomenclature p.2 |
| r | 奖励信号(r_medium, r_terminal) | Nomenclature p.2;式(31)(32) p.14 |
| s_t | MDP 状态 | Nomenclature p.2;式(29) p.12 |
| o_t | MDP 观测 | Sec. III.A p.11;式(30) p.13 |
| t, t_go, t_f | 时间、剩余时间、末端时间 | Nomenclature p.2 |
| t_fIT, t_fID | 预测拦截时间(I–T、I–D) | 式(10) p.7 |
| u_i, u_i^max | 玩家 i 的制导指令及其上限, m/s² | 式(6) p.7;Table 3 p.20 |
| v, V | 速度, m/s | Nomenclature p.2;Fig. 1 p.5 |
| x | 线性化运动方程状态向量 [y_IT, ẏ_IT, y_ID, ẏ_ID, a_I, a_T, a_D] | 式(7) p.7 |
| X−O−Y | 笛卡尔惯性参考系 | Nomenclature p.2;p.5 |
| y | 高度/侧向距离, m(y_IT, y_ID 为垂直 X 轴的相对距离分量) | Nomenclature p.2;p.5 |
| Z_IT, Z_ID | 零控脱靶量(ZEM), m | Nomenclature p.2;式(12) p.8 |
| Z_IM | 拦截弹对其目标(M,即 T)的 ZEM | 式(17)(19) p.8–9 |
| α_1, α_2, β_1, β_2, σ | 奖励函数设计超参数 | Nomenclature p.2;式(31)(32) p.14 |
| φ_i | 玩家 i 的航迹角(飞行路径角), rad | Nomenclature p.2;Fig. 1 p.5;式(3) p.6 |
| φ(χ) = e^{−χ} + χ − 1 | ZEM 展开式中的函数 | 式(16) p.8 |
| Φ | 状态转移矩阵 | Nomenclature p.2;式(12) p.8 |
| γ | 折扣因子 | Nomenclature p.2;式(33) p.14;Table 2 p.18 |
| η | 杀伤半径(I–D 切换阈值), m | Nomenclature p.3;式(17) p.8;式(20) p.9 |
| λ_IT, λ_ID | 视线与 X 轴夹角, rad | Nomenclature p.3;p.5 |
| λ_1 | Lagrange 乘子 | Nomenclature p.3;式(22)–(24) p.9 |
| ρ_IT, ρ_ID | 对抗双方相对距离, m(ρ^0 为初值) | Nomenclature p.3;式(10) p.7 |
| τ_i | 玩家 i 动力学时间常数 | Nomenclature p.3;式(6) p.7(τ_M 为拦截弹目标/即 T 的时间常数,式(19) p.9) |
| ω_1, ω_2, ξ_1, ξ_2 | 最优导引律(OGL)设计参数(非负) | Nomenclature p.3;式(18)(19) p.9 |
| K(t), P(t) | LQOGL 时变增益 | 式(18)(19) p.9 |
| 下标 I, T, D | 拦截弹、目标、防御器 | Nomenclature p.3 |
| 上标 max, * | 最大值、最优解 | Nomenclature p.3 |
| Γ | 观测掩模矩阵 | 式(30) p.13 |
| ω_{o,t} = [δy; δV; δa]_{o,t} | 观测噪声向量, ~U(0_9, Σ) ∈ R^9 | 式(30) p.13 |
| Σ = [σ_y I_3, σ_v I_3, σ_a I_3]^T | 噪声幅值(σ_y, σ_v, σ_a 非负) | 式(30) p.13;Table 5 p.25 |
| Ω(·) | 观测函数(状态→观测) | Sec. III.A p.11;式(30) p.13 |
| π_φ, μ(s) | 策略函数 / actor(θ 为网络参数的记号亦用 θ_Q) | Sec. III.C p.15–16;Fig. 3 p.18 |
| ε | 目标策略平滑中的截断高斯噪声 | p.17 |
| τ(Table 2) | TD3 soft update 系数 5×10⁻³(与时间常数 τ 撞号) | Table 2 p.19 |
| α(Table 2) | TD3 学习率 3×10⁻⁴(与奖励超参 α 撞号) | Table 2 p.19 |
| 𝔹 | 经验回放池大小 5120 | Table 2 p.19 |
| n_batch, n_opt, ω(Table 2) | batch size 128 / policy delay 2 / train frequency 6000(ω 与 OGL 参数撞号) | Table 2 p.19 |
| s, o, a, P_sa, R, Ω, γ | MDP 七元组 | Sec. III.A p.11 |
| R_t = Σ γ^{i−t} r_i | 回报 | Sec. III.A p.11 |
| action = [u_T, u_D] | 动作空间 | 式(30) p.12 |
