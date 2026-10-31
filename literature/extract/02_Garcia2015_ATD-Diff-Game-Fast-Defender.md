# 02 | Active Target Defense Differential Game with a Fast Defender
> Garcia E., Casbeer D.W., Pachter M. | ACC 2015 | arXiv:1502.02747
> （PDF 共 9 页；以下页码均指 arXiv PDF 的实际页序）

## 0. 一句话定位
本文是 Pachter–Garcia–Casbeer "主动目标防御微分博弈"谱系的直接续作：把同速情形的结果（[23] Pachter et al., Allerton 2014，解归结为四阶多项式求根，p.8）推广到 **Defender 快于 Attacker（β=VD/VA>1，即 γ=VA/VD<1）** 的一般情形，解归结为一个六阶复指数方程求根（p.6, p.8）；并首次给出该博弈中 Target 生存的**临界速度比 ᾱ**（Prop.2, p.4），特别处理了 Target 初始位置比 Defender 更靠近 Attacker 的危险几何（p.2）。与前作 [21][22]（假设 Attacker 用 PP/PN 固定策略、T-D 团队解最优控制）不同，本文把 Attacker 也作为博弈理性方，在零和三人微分博弈框架下同时给出三方最优策略（p.2）。

## 1. 问题建模
- **状态量（原文符号）**：真实空间 xT, yT, xA, yA, xD, yD（p.2, 式(1)-(3)）；降维（reduced）状态空间：R（Attacker–Target 距离）、r（Attacker–Defender 距离）、θ（R 与 r 两线间夹角）（p.2 Fig.1；p.3 Sec III）。
- **控制量（原文符号）**：惯性系航向角 φ̂, χ̂, ψ̂（p.2）；降维空间中为相对航向角 φ, χ, ψ，满足 φ̂=φ+λ, χ̂=λ+θ−χ, ψ̂=ψ+θ+λ−π（p.2, 式(1)-(3) 下方），λ 为 Attacker→Target 视线角（p.3 顶部）。
- **动力学模型**：二维平面、常速、"simple motion" a la Isaacs 点质量（p.2 Sec II）：
  - ẋT=VT cos φ̂, ẏT=VT sin φ̂；ẋA=VA cos χ̂, ẏA=VA sin χ̂；ẋD=VD cos ψ̂, ẏD=VD sin ψ̂（p.2, 式(1)-(3)）
  - 以 VA 归一化的降维动力学（p.3, 式(4)-(6)）：Ṙ=α cos φ−cos(θ−χ)；ṙ=−cos χ−β cos ψ；θ̇=−(α/R)sin φ+(1/R)sin(θ−χ)−(β/r)sin ψ+(1/r)sin χ。
- **参与者与支付/终端流形**：参与者为 Target–Defender 团队（合作方）与 Attacker（对抗方）（p.1-2）。支付 J=∫[t0,tf] Ṙ dt = R(tf)−R(t0)，即 Defender 拦截 Attacker 时刻的 Target–Attacker 距离（p.3, 式(7)）；团队 max_{φ,ψ} min_χ J。终端流形：r(tf)=rc（rc 为 Defender 捕获半径），终端时间 tf 自由（p.2-3, p.3 式(12)）；Sec IV 中改用点捕获 r(tf)→0（p.4）。
- **机动目标**：未提及专门机动模型；Target 为常速 VT 质点，α=VT/VA<1（Attacker 快于 Target 飞机）（p.2）。
- **约束（输入/状态/视场）**：输入为航向角，**未提及**转弯速率/侧向加速度约束；状态约束仅有终端 r(tf)=rc（p.3）；视场/传感**未提及**（仅 Example 3 提到 T-D 团队可测量 Attacker 当前位置 A=(xA(t),yA(t))，p.8）。
- **噪声/时延**：未提及。

## 2. 假设条件
1. 三方速度 VT, VA, VD 均为常数（p.2, Sec II）。
2. Simple motion（伊萨克斯式点质量：控制量直接是航向角，可瞬时转向，无机动动力学）（p.2, Sec II）。
3. 运动限制在二维平面（p.2, Fig.1 与式(1)-(3)）。
4. Attacker 导弹快于 Target 飞机：α=VT/VA<1（p.2）；若 α≥1 则 Target 总能逃跑、无需 Defender，问题不存在（p.5）。
5. 本文核心假设：Defender 快于 Attacker，β=VD/VA>1；Sec IV-V 以 γ=1/β=VA/VD<1 表述（p.2；p.4）。
6. Attacker 知道 Defender 的位置（p.2, Introduction："Assuming that the Attacker knows the position of the Defender"）。
7. Attacker 不预设固定制导律，而是博弈最优方（区别于 [21][22] 中 PP/PN 假设）（p.1-2）；Example 3 另讨论 Attacker 非最优（PN）时的鲁棒性（p.8）。
8. Attacker 属"消耗性"方：宁可被拦截也要把拦截点逼近 Target 以造成损伤（p.2）。
9. Sec III 数值解允许有限捕获半径 rc（p.3）；Sec IV 明确取点捕获 r(tf)→0（p.4），Sec V 的 Apollonius 圆几何（D 与 A 同时可达点的轨迹）同样基于点捕获极限（p.4-5）。
10. Sec IV 坐标系：以 A、D 为锚，AD 延长线为 X 轴、垂直平分线为 Y 轴，A=(xA,0), D=(−xA,0), T=(xT,yT)（p.4，坐标选择不失一般性）。

## 3. 方法核心
**机制概述**：论文分两层求解同一博弈。第一层（Sec III, pp.2-4）：在降维状态 (R,r,θ) 上写出 PMP 必要条件，把最优航向的闭式解（Prop.1）代回状态/协态方程，数值求解 TPBVP。第二层（Sec IV-V，解析）：γ<1 时 Attacker-Defender 单挑的 **DA Apollonius 圆**（圆心 a、半径 rA，p.4 式(29)(30)）把平面分成 D 先达区（圆外）与 A 先达区（圆内）（p.5）；Target 的生存条件等价于 AT Apollonius 圆与 DA 圆相交，临界速度比 ᾱ 对应**两圆相切**（Prop.2, pp.4-5）。随后把动态博弈约化为 DA 圆上的静态 minmax 点选择博弈：Defender 最优策略恒为 w*=u（在 Attacker 瞄准点处拦截，p.6、p.7）；Target 在圆外时 min_u max_v 的鞍点为 u*=v*（Prop.3），等价于 Attacker 在圆上选拦截点 I 最小化 J=IT+α·AI；Target 在圆内时 max_v min_u 的鞍点仍为 u*=v*（Prop.4），等价于最大化 J=α·AI−IT。两种情形的最优拦截点 I=(ϕ*, rA) 的极角 ϕ* 均由**同一个六阶复指数方程 (41)** 的根给出（Th.1/Th.2），最坏情况枚举 6 个根即可（p.6）。

**关键公式**（均标注页码）：
- 降维动力学 (4)-(6)：p.3。
- 支付 (7)：max_{φ,ψ} min_χ J=∫Ṙdt，p.3。
- Hamiltonian (8) 与协态方程 (9)-(11)：p.3。
- 终端条件 (12)：r(tf)=rc, λR(tf)=0, λθ(tf)=0, α²+2(αβ+cos θ(tf))λr(tf)+(β²−1)λ²r(tf)−1=0，p.3。
- Prop.1 最优航向（p.3, 式(13)-(18)）：sin ψ*=（λθ/r)/√(λ²r+λ²θ/r²)，cos ψ*=λr/√(λ²r+λ²θ/r²)；sin φ*=(λθ/R)/√((1−λR)²+λ²θ/R²)，cos φ*=(1−λR)/√((1−λR)²+λ²θ/R²)；sin χ*=χs/√(χ²s+χ²c)，cos χ*=χc/√(χ²s+χ²c)，其中 χs=(1−λR)sin θ−(λθ/R)cos θ+λθ/r，χc=(1−λR)cos θ+(λθ/R)sin θ−λr。二阶条件：∂²H/∂ψ²>0（式(20)）、∂²H/∂φ²>0（式(22)）、∂²H/∂χ²<0（式(28)），p.3-4。
- DA Apollonius 圆：圆心 a=((1+γ²)/(1−γ²))xA（式(29)），半径 rA=(2γ/(1−γ²))xA（式(30)），p.4。
- 临界速度比（Prop.2, p.4, 式(31)）：ᾱ=(γ√((xA+xT)²+yT²)−√((xA−xT)²+yT²))/(2γxA)。（注：分式结构经与 Example 2 数值核对确认；按 yT=0 特例 (37) 反推亦可唯一确定。）
- 推导用几何：AT Apollonius 圆心 O 坐标 (33)、半径 rO=α/(1−α²)d、相切条件 rO=rA−q（式(34)(35)）、四次方程因式分解 (36)，p.5。
- 特例 yT=0：ᾱ=[xA(γ−1)+xT(γ+1)]/(2γxA)（式(37)）；ᾱ=0 的临界 Target 初始位置 xT=(1−γ)xA/(1+γ)（式(38)），p.5。
- 圆外情形约化：min_{xI,yI} J(xI,yI) s.t. (a−xI)²+y²I=r²A（式(39)），J=√((xI−xT)²+(yI−yT)²)+α√((xA−xI)²+y²I)（式(40)），p.6。
- 圆内情形约化：max_{xI,yI} J s.t. 同一约束（式(46)），J=α√((xA−xI)²+y²I)−√((xI−xT)²+(yI−yT)²)（式(47)），p.7。
- 极角形式代价 (42)/(48) 与驻值条件 (43)(44)，p.6-7；六阶复指数方程 (41)（系数由 l=e^{iλ}, M=(2γ²/(1−γ²))xA=|aA|, N=√((a−xT)²+y²T)=|aT|, rA, α 构成，p.6）：Th.1（圆外）取最小 J(ϕ) 的根，Th.2（圆内）取最大 J(ϕ) 的根。

## 4. 理论结果
共 **2 个定理 + 4 个命题**（另有 2 个未编号的特例结果）：
- **Proposition 1**（p.3，证明 pp.3-4）：在 PMP 框架（式(4)-(12)）下，T-D 团队最优航向 φ*, ψ* 与 Attacker 最优航向 χ* 的闭式表达为式(13)-(18)；ψ*、φ* 使 H 取极小（等价最大化 R(tf)），χ* 使 H 取极大（等价最小化 R(tf)）。
- **Proposition 2**（p.4，证明 pp.4-5）：给定 γ=VA/VD<1 与初始几何，Target 生存的临界速度比 ᾱ 由式(31)给出；推导基于 AT Apollonius 圆与 DA Apollonius 圆相切（Fig.3），且解存在当且仅当两圆相交。前提：点捕获、γ<1、Target 在 DA 圆内（圆外时 ᾱ=0，p.5）；α≥1 时无博弈（p.5）。
  - 特例（未编号，p.5）：yT=0 时 ᾱ 由式(37)给出；ᾱ=0 对应的临界 Target 位置 xT=(1−γ)xA/(1+γ)（式(38)，等价于 a−rA）。
- **Proposition 3**（p.6）：Target 在 DA 圆**外**时，min_u max_v J(u,v) 的解为 u*=v*；归约为 Attacker 在 DA 圆上解 min_{xI,yI}J（式(39)(40)），J=IT+α·AI。前提：Defender 策略 w*=u，0<α<1。
- **Theorem 1**（p.6）：圆外情形最优拦截点 I=(ϕ*, rA)（相对圆心 a 的极坐标），ϕ* 为六阶复指数方程 (41) 中使代价 (42) 最小的根；复系数根至多 6 个，枚举即可。前提：Target 在 DA 圆外。
- **Proposition 4**（p.7）：Target 在 DA 圆**内**时，max_v min_u J(u,v) 的解仍为 u*=v*（Attacker 若选 u≠v 反而使代价增大，Fig.5）；归约为 max_{xI,yI}J（式(46)(47)），J=α·AI−IT。前提：w*=u、α>ᾱ（ᾱ>0 由式(31)给出）。
- **Theorem 2**（p.7，证明 p.8）：圆内情形最优拦截点 I=(ϕ*, rA)，ϕ* 为同一方程 (41) 中使代价 (48) 最大的根；驻值条件与 Th.1 相同（式(44)）。
- 另一贯穿性结论：解析解（Sec V）与 TPBVP 数值解（Sec III）在 Example 1、2 中给出相同轨迹与拦截点（pp.7-8）；(41) 的解可作为对未知 Attacker 制导律鲁棒的闭环拦截策略——T-D 持续重解 (41) 更新航向（p.8, Example 3）。

## 5. 实验设置
纯理论论文，仅 3 个数值算例（Sec VI, pp.7-8），**无代码、无 Monte Carlo、无与其它制导律（CLOS/TG 等）的横向对比**；对比基线为"Sec III 的 TPBVP 数值解 vs Sec V 的解析解"的一致性，以及"Attacker 最优 vs Attacker 用 PN"两种支付值。
- **Example 1**（Target 在 DA 圆外，p.7）：α=0.25, γ=0.8；A=(4,0), D=(−4,0), T=(0.5,4)；a=18.22, rA=17.78；(41) 的六个根 ϕ1..ϕ6=−2.9596, −2.8573, 0.0001, 0.0001, 0.2254, 0.2186；最优 ϕ*=0.2186 → I*=(0.8676, 3.8555)；与数值法结果一致（Fig.6）。
- **Example 2**（Target 在 DA 圆内，pp.7-8）：α=0.5, γ=0.93；A=(6,0), D=(−6,0), T=(3.1,2.7)；a=82.823, rA=82.605；由式(31)得 ᾱ=0.436<α=0.5（保证逃逸）；最优 ϕ*=0.0429 → I*=(0.293, 3.539)；与数值法一致（Fig.7）。
- **Example 3**（对未知 Attacker 制导律的鲁棒性，p.8）：A=(10,0), D=(−10,0), T=(3,7.5)；α=0.6, γ=0.85；Attacker 用 PN（N=3，对 T-D 未知），T-D 仅测 Attacker 当前位置并持续重解 (41)；结果 R(tf)=5.609 > J*=5.373（Attacker 最优时的支付），Target 逃逸、Attacker 被拦截（Fig.8）。
- **评价指标**：最终 T-A 距离 R(tf)／支付 J、拦截点 I* 坐标、临界速度比 ᾱ。

## 6. 局限性
- **作者承认的**：
  - 解析解需解六阶多项式，复杂度高于同速情形的四阶（[23]）（p.8, Conclusions）。
  - Sec IV 的临界速度比结果仅针对点捕获（p.4："we consider point capture"）。
  - 研究范围限于 γ<1（Defender 更快）的情形；γ>1 未在本文处理（p.2："the focus of this paper is on the case where the Defender is faster than the Attacker"）。
  - 鲁棒性仅由单一 PN 算例佐证（p.8, Example 3），未给出正式证明。
- **我分析的**（含推断依据）：
  - Simple motion 假设下控制量即航向角、无转弯速率约束（p.2 式(1)-(3)），最优策略可含航向跳变；真实导弹/飞机有侧向加速度与过载限制，最优解的可行性会打折扣。
  - Sec V 的解析解本质是基于初始几何的开环结果；Example 3 的"闭环"靠反复重解 (41) 实现（p.8），但 Prop.3/Prop.4 的静态 minmax 鞍点并未被证明构成动态博弈的反馈鞍点（无反馈值函数验证、无重解收敛性/稳定性分析）。
  - 支付只含终端距离 R(tf)，不含时间、控制能量等项（p.3 式(7)），对 Defender 的拦截路径经济性无要求。
  - 由式(31)（经核对为 ᾱ=(γ·TD−TA)/(2γxA)，TD、TA 为 T 到 D、A 的初始距离）可推 dᾱ/dγ=TA/(2γ²xA)>0：Defender 相对越快（γ 越小），Target 所需最低速度越低——该敏感性分析文中未给出（我的推导，已数值验证）。
  - 未考虑噪声、量测误差、时延与三维空间（全文无相关内容）；Example 3 的鲁棒性结论无统计性评估。

## 7. 可复现性
- **已给出**：完整模型方程 (1)-(6)（pp.2-3）；PMP 必要条件 (8)-(12)（p.3）；最优航向闭式解 (13)-(18)（p.3）；ᾱ 公式 (31) 及 yT=0 特例 (37)(38)（pp.4-5）；六阶方程 (41) 的全部系数与代价 (42)(48)（pp.6-7）；3 个算例的完整参数与中间量（a、rA、六个根、ϕ*、I*、ᾱ、J*）（pp.7-8）。
- **缺失**：无公开代码/数据；TPBVP 数值求解细节（打靶初值猜测、积分器、步长）未说明（p.4 仅述"numerically solve"）；数值解所用 rc 的具体取值未给出；Example 3 中重解 (41) 的更新频率与仿真设置未给；初值 (R0,r0,θ0) 未显式列出（可由几何换算）；Fig.6-8 无对应数据表。

## 8. 待验证
- Sec III 数值解与 Sec V 解析解的一般等价性：文中仅靠 Example 1、2 的数值一致支撑（pp.7-8），未给出证明。
- 方程 (41) 是否恒存在唯一全局最优实根：文中说最坏情况枚举 6 个根（p.6），但未讨论多重根、根退化或多个局部极小的情形。
- Example 1、2 中数值法所用捕获半径 rc 的取值（若取点捕获极限则与解析解严格一致）——文中未说明。
- Target 在 DA 圆内的逃脱几何：代价 (47) J=α·AI−IT 隐含"Target 沿直线穿过出口点 v 后继续直行、T′ 越过 I"（即 α·AI>IT）这一解释，文中未显式陈述或证明。
- Attacker 允许中途改变瞄准点（反馈策略）时，静态鞍点 u*=v* 是否仍成立（Example 3 用重解策略在数值上成立，理论未证）。

## 9. 记号表
| 原文符号 | 含义 | 首次出现位置 |
|---|---|---|
| T, A, D | Target（被保护飞机）、Attacker（来袭导弹）、Defender（防御弹） | p.1-2 |
| VT, VA, VD | 三方速度（常数） | p.2, Sec II |
| φ̂, χ̂, ψ̂ | T/A/D 惯性系航向角 | p.2, 式(1)-(3) |
| φ, χ, ψ | 降维空间中的相对航向角（控制量） | p.2 |
| λ | Attacker→Target 视线角（惯性系） | p.3 顶部（Fig.1, p.2） |
| R | Attacker–Target 距离 | p.2 |
| r | Attacker–Defender 距离 | p.2 |
| θ | R 与 r 两视线间夹角 | p.2（Fig.1, Sec III） |
| α=VT/VA | Target/Attacker 速度比（α<1） | p.2 |
| β=VD/VA | Defender/Attacker 速度比（β>1） | p.2 |
| γ=1/β=VA/VD | Attacker/Defender 速度比（γ<1） | p.4 |
| tf | 拦截时刻（自由终端时间） | p.2-3 |
| rc | Defender 捕获半径 | p.3 |
| J | 支付 ∫Ṙdt=R(tf)−R(t0) | p.3, 式(7) |
| H | Hamiltonian | p.3, 式(8) |
| λR, λr, λθ | 协态变量 | p.3, 式(8)-(11) |
| χs, χc | Attacker 最优航向中间量 | p.3, 式(17)-(18) |
| (xA,0),(−xA,0),(xT,yT) | A/D/T 在 A-D 锚定坐标系中的位置 | p.4 |
| T′ | Target 终端位置 | p.4 |
| I=(xI,yI) | Defender 对 Attacker 的拦截点 | p.4 |
| a | DA Apollonius 圆心横坐标，a=((1+γ²)/(1−γ²))xA | p.4, 式(29) |
| rA | DA Apollonius 圆半径，rA=(2γ/(1−γ²))xA | p.4, 式(30) |
| ᾱ | Target 生存的临界速度比 | p.4, Prop.2/式(31) |
| d | A 与 T 的初始距离 | p.5, 式(32) |
| O, (xO,yO), rO | AT Apollonius 圆的圆心与半径 | p.5, 式(33) |
| q | 圆心 a 与 O 间距离 | p.5, 式(34) |
| u, v, w | Attacker/Target/Defender 在 DA 圆上的瞄准点 | p.5, Sec V-A |
| S | T′ 与拦截点间的距离（博弈支付） | p.5, Sec V-A |
| ϕ | 拦截点 I 相对圆心 a 的极角 | p.6, Th.1 |
| l=e^{iλ} | (41) 中的复参数 | p.6 |
| M | 点 A 到圆心 a 的距离，M=(2γ²/(1−γ²))xA | p.6 |
| N | 点 T 到圆心 a 的距离，N=√((a−xT)²+y²T) | p.6 |
| J* | Attacker 最优策略下的支付值 | p.8 |
| N'（PN 导航比, =3） | Example 3 中 Attacker 的 PN 导航常数 | p.8（注：与距离量 N 无关，仅出现于 Example 3） |
