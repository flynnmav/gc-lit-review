# 03 | The Complete Differential Game of Active Target Defense
> Garcia E., Casbeer D.W., Pachter M. | JGCD 2020 (arXiv 预印本) | arXiv:2002.04054

## 0. 一句话定位
补全 TAD(Target-Attacker-Defender)主动目标防御微分博弈的"最后一块拼图":此前 [20],[21],[30] 已解决 T/D 团队赢取区 Re 内的博弈(ATDDG),[22] 对 Attacker 赢取区 Rc 的求解被本文证明是错的(不满足半透屏障,其 Pure Pursuit 策略非最优),[23],[24] 给了几何解但无最优性证明(p.1-2);本文用双侧 Pontryagin 最大值原理严格求解 Rc 内的 Game of Degree(称为 Capture Differential Game, CDG),给出 C1 Value 函数并验证 HJI 方程,再用 Theorem 3 证明 CDG 与 ATDDG 在 Barrier 上解重合,从而给出全状态空间 R6 = Rc ∪ Re 的完整解(p.2, p.4)。**与"快防御者"经典假设的关系(本文原话,p.3 Remark):本文不需要 VD > VA,主文取临界情形 VA = VD(归一化 VA = VD = 1, VT = α < 1);并明确指出当 VA > VD(D 更慢)且要求点捕获时 A 必胜、T/D 无解,而 VD > VA 情形"结果可推广"(论文未给推导)。**即去除"防御者更快"这一支配性论证后,真正需要重新求解且可解的正是等速边界情形;此时 Game of Kind 的屏障不再是 A-D Apollonius 圆,而是 Theorem 1 给出的、以 A-D 视线角 σ 与中点 (x0, y0) 为参数、关于 T 坐标的双二次型(横截面为双曲线,p.4 Remark)。

## 1. 问题建模
- **状态量(原文符号)**: x = (xT, yT, xA, yA, xD, yD) ∈ R6,游戏集为全空间 R6(p.2, Sec. II-A)。
- **控制量(原文符号)**: T/D 团队控制 uT,D = {φ, ψ},Attacker 控制 uA = {χ};φ 为 Target 航向角、χ 为 Attacker 航向角、ψ 为 Defender 航向角(Fig. 1, p.3;Hamiltonian (14), p.5);容许控制 χ, φ, ψ ∈ [−π, π](p.3)。
- **动力学模型**: Isaacs 式 "simple motion"(全向/holonomic 质点、常速、瞬时改变航向),ODE 组 (1)(p.3):
  ẋA = cos χ, ẏA = sin χ;ẋD = cos ψ, ẏD = sin ψ;ẋT = α cos φ, ẏT = α sin φ(各带初值)。
  速度归一化 VA = VD = 1,VT = α,α = VT/VA < 1 为问题参数(p.2-3)。
- **参与者与支付/终端流形**: 三方零和二人博弈(T、D 结盟对抗 A)。双终止集 S = Se ∪ Sc(式 (2), p.3):Se := {x | ‖A−D‖ = 0}(D 拦截 A,T 逃脱,T/D 胜),Sc := {x | ‖A−T‖ = 0}(A 捕获 T,A 胜)。Rc 内的 CDG:终止条件 xA = xT, yA = yT(式 (9), p.4),终端流形 Sc 是 R6 中 4 维超平面(式 (13), p.5);支付 J = Φ(xf) = 终端时刻 D-T 距离(式 (10)-(11), p.4),Value V(x0) = max_{uA(·)} min_{uT,D(·)} J(式 (12), p.4)——A 最大化、T/D 最小化终端 D-T 距离;tf 自由。
- **机动目标**: Target 可机动(控制为航向 φ),速度比 α < 1;非机动 Target 的情形引 [12],[13],本文不处理(p.1)。
- **约束(输入/状态/视场)**: 航向角 ∈ [−π, π];"Both, the state and the controls, are unconstrained"(p.3);终端为点捕获(point capture,p.3)。视场/传感约束:未提及。
- **噪声/时延**: 未提及;CDG 为完美信息博弈,各方知道动力学 (1) 与 α、可获取当前状态 x,但"不知道对手当前决策",无需 discriminatory/stroboscopic 策略(p.4, Sec. II-C)。

## 2. 假设条件
1. 三参与者均做 Isaacs "simple motion"(holonomic、平面、常速)(p.2, Sec. II-A)。
2. 速度比 α = VT/VA < 1(Target 慢于 Attacker);当 VA < VT 时"不需要 Defender,Target 总能跑赢"(p.2)。
3. Attacker 与 Defender 能力相近:VA = VD,无损归一化为 VA = VD = 1,VT = α(p.3)。
4. **速度比取值范围的完整论述(p.3 Remark)**:若 VA > VD(D 更慢)且要求点捕获,则 A 无视初始条件必捕获 T——慢者 D 无法点拦截快者 A,A 总能绕开慢速点去抓 T;又因 α < 1,T/D 无法永远把 A 挡在 T 之外(用 [22] 的记号即无法恒保持 R = A−T 间距、r = A−D 间距 > 0),T 与 D 的会合(réndezvous)策略必然导致 T 被捕。故本文只解 VA = VD,并称"结果可推广到 VD > VA"(无推导)。
5. 终止条件为点捕获(A-T 与 A-D 间距均为零才计终止,p.3;正捕获半径情形引 [11], p.1)。
6. 容许控制 χ, φ, ψ ∈ [−π, π],状态与控制无其他约束(p.3)。
7. Game of Kind 划分先行给定:Red ⊂ Re(T 到 D 不远于到 A 时必逃脱,即使 α → 0,p.3, 式 (3));x ∉ Red 上由 Barrier 函数 B(x; α) 的符号划分 Rea(B<0,逃脱)与 Rc(B>0,捕获)(式 (4)-(5), p.3),屏障 B = {x ∉ Red | B(x;α)=0}(式 (6), p.4)。B(x;α) 的显式表征即 Theorem 1,其证明在 [30](p.4)。
8. 完美信息 + 状态反馈策略 + 对手当前决策不可知(无需歧视性/频闪策略)(p.4, Sec. II-C)。
9. CDG 内无奇异曲面,Isaacs 条件成立:min_{φ,ψ} max_χ H = max_χ min_{φ,ψ} H(p.5, 式 (14) 之后),故可用双侧("Two-person")PMP 合成正则解(p.5, Sec. III)。
10. 参数范围:Theorem 1 要求 0 < α < 1(p.4);Theorem 2 允许 0 ≤ α < 1(p.5)。
11. **拦截几何与参数平面划分(哪些初始条件 T 必死/可活)**:固定 A、D 位置时,屏障 B 的横截面是 (x,y) 平面上的一条双曲线,只有"A 支"有效,"D 支"落在 D 的支配区(Red,由 A-D 线段的中垂线 OBS 界定)内无意义(p.4 Remark, Fig. 2)。初始条件归类:T 距 D 不远于距 A(Red)→ 必可活;x ∉ Red 且 B(x;α)<0(Rea)→ 可活;x ∉ Red 且 B(x;α)>0(Rc)→ 在最优博弈下 T 必死,此时进行 CDG,支付为终端 D-T 距离(p.3-4);B(x;α)=0 → 屏障上,A 捕获 T 与 D 拦截 A 同时发生(p.5, Sec. II-C 末;Thm 3, p.9-10)。
12. 支付函数的衔接性要求:CDG 的支付 (10) 设计成与 [30] 中 ATDDG 支付衔接,使屏障成为半透面、两 Game of Degree 在 B 上给出同一策略与同一 Value(p.5 首段;Thm 3)。

## 3. 方法核心
机制一句话:先用 Theorem 1 的双曲型屏障把 R6 分成 Re/Rc(Game of Kind);在 Rc 内把"必死"博弈建成以**终端 D-T 距离**为支付的零和 Game of Degree(CDG),用双侧 PMP 证明三玩家协态全为常数 → 最优航向恒定 → 直线轨迹;最优拦截点 I* 必在 A-T Apollonius 圆上、且满足一个多项式方程 (20),三人最优策略都是"指向 I*";由此得到显式 Value V = DI − TI/α,验证其 C1 且满足 HJI;最后证明在屏障上 CDG 与 ATDDG 的解重合(V=0),屏障为半透面。关键公式:
- 动力学 (1)(p.3);终止集 (2)(p.3);支配半空间 Red (3)、区域划分 Rea/Rc/Re (4)-(5)、屏障 (6)(p.3-4)。
- **Barrier 方程(Theorem 1, p.4)**:B(x; α) = bxx xT² + byy yT² + 2bxy xT yT + 2bx xT + 2by yT + b(式 (7)),系数 bxx = cos²σ − α², byy = sin²σ − α², bxy = sin σ cos σ, bx, by, b 由式 (8) 给出,其中 cos σ = (xA−xD)/‖A−D‖, sin σ = (yA−yD)/‖A−D‖,(x0, y0) 为 A-D 中点(p.4)。
- CDG 支付与 Value:(9)-(12)(p.4);终端流形超平面 (13)(p.5)。
- Hamiltonian (14)(p.5):H = λxA cos χ + λyA sin χ + λxD cos ψ + λyD sin ψ + αλxT cos φ + αλyT sin φ;Isaacs 条件成立(p.5)。
- **A-T Apollonius 圆(15)-(16)(p.5)**:(x−xc)² + (y−yc)² = r²,xc = (xT − α²xA)/(1−α²), yc = (yT − α²yA)/(1−α²), r = α‖T−A‖/(1−α²)。
- **最优策略角(Theorem 2, p.5-6)**:cos φ* = (x*−xT)/‖I*−T‖, cos ψ* = (x*−xD)/‖I*−D‖, cos χ* = (x*−xA)/‖I*−A‖(式 (17)-(19),含 sin 分量)——三人皆指向捕获点 I* = (x*(x), y*(x))。
- **捕获点方程(p.6)**:I* 为 (15) 与式 (20) 联立之解;(20) 为关于 (x,y) 的多项式方程:‖I−T‖²·[(I−D)×(I−T) − α²((I−D)×(I−A) + (I−A)×(I−D) 项组合)]² − α‖I−D‖²·[(I−A)×(I−T)]² = 0(逐项见 p.6)。
- **Value 函数(21)(p.6)**:V(x) = √([x*−xD]²+[y*−yD]²) − (1/α)√([x*−xT]²+[y*−yT]²) = DI − TI/α(即 DI − AI,由 (55) TI = αAI,p.7)。
- PMP 细节:ME1 (22) 与控制-协态关系 (23)-(25)(p.6);协态动力学 ˙λ = −∂H/∂x ⇒ 全部协态为常数 → 最优航向恒定、直线轨迹(p.6);增广终端值 Φa (26)、横截条件 (27)-(35)、ME1 展开式 (36)(p.6);时间关系 tf − t = AI = TI/α(式 (55), p.7);D 的终端位置 (56)(p.7);协态的纯状态表达 (57)(p.8)。
- **C1 验证**:由 (59)-(64) 证明 dV/dx* = 0(p.8),梯度 ∂V/∂x 显式 (67)-(68)(p.9)。
- **HJI 验证** (69)-(70)(p.9):利用 AI = DI、TI = αAI,化简得 ∂V/∂x · f = 0。
- **六次多项式(Corollary 1, p.9)**:x* = xc + r cos ω*, y* = yc + r sin ω*,ω* 为复变量 v = e^{iω} 的六次方程 (71) 之根,系数 a0,b0,a1,b1,a2,b2,a3 由 (72) 给出。
- **State-space 划分与屏障上的解(Theorem 3, p.9-10)**:x ∈ B 时 A-T Apollonius 圆与 A-D 中垂线 OBS 相切,切点即 I*,此时 ω* = ρ(A 到 D 的视线角),该瞄准点同时满足 (15) 与 (20),V(x|x∈B) = 0;任何其他角度 ω ≠ ρ 给出终端分离 DT > 0;ATDDG([30] 中式 (15)/(77),即本文 (78))在同一瞄准点下同样取零(p.10)。
- [22] 的失败机理(p.2, p.5, p.12):其以捕获时间为目标导致 Attacker 实施 Pure Pursuit,所设计策略不构成半透屏障,一方可用本文最优策略使状态穿越屏障而翻盘。

## 4. 理论结果
- **Theorem 1(p.4)**:对 0 < α < 1,分隔 R6 为 Re 与 Rc 的屏障面为 B(x; α) = 0,B 为 (7)-(8) 给出的关于 (xT, yT) 的二次型(系数依赖 A-D 视线角 σ、中点与 A 的位置)。前提:0 < α < 1;证明见 [30]。
- **Theorem 2(p.5-6)**:对 CDG (1),(9)-(12),设 x ∈ Rc、速度比 0 ≤ α < 1,则 T、D、A 的最优状态反馈策略为 (17)-(19)(均指向捕获点 (x*, y*),(x*, y*) 为 (15)+(20) 之解);Value 函数 (21) 为 C1、满足 HJI PDE、在 Rc 内显式成立(证明 p.6-9,含无奇异面结论:p.5 "V and ∂V/∂x are continuous for any x ∈ Rc; hence, no singular surfaces exist")。
- **Corollary 1(p.9)**:最优捕获坐标可写为 (x*, y*) = (xc + r cos ω*, yc + r sin ω*),ω* 为六次多项式方程 (71)(系数 (72))的根。前提:同 Theorem 2。
- **Theorem 3(p.9,证明 p.10)**:当 x ∈ B(屏障面)时,CDG 与 ATDDG 给出相同的最优解与相同的 Value(V = 0),即同一瞄准点(切点,ω* = ρ)且 A 捕获 T 与 D 拦截 A 同时发生。前提:x ∈ B;Apollonius 圆与 OBS 相切 (73)。
- 另有三条未编号 Remark:p.3(VA > VD 时 T/D 必败、本文聚焦 VA = VD、可推广到 VD > VA);p.4(屏障横截面为双曲线、仅 A 支有效);p.5(CDG 支付的实战解释:D 尽量贴近 T,可利用 A 的非最优行为,状态穿入 Re 后切换 ATDDG 策略即可逃脱)。
- 对 [22] 的否定性结果:以反例(Example 3, p.11-12)证明 [22] 策略非最优、不构成半透屏障(p.1 摘要、p.2);p.1 摘要称本文合成的是"该微分博弈唯一提供半透屏障面的正则解"。

## 5. 实验设置
纯理论论文,仅有 3 个说明性数值算例(Sec. V, p.10-12),无统计性实验、无代码:
- **Example 1(p.10, Fig. 3)**:屏障上初始条件:α = 0.7,T = (7.5, −3.28), A = (7.2, −4.5), D = (3, −2);x ∈ B。最优瞄准点 I* = (6.305, −1.224) 时不变;全程 B(x(t); α) = 0;三人同时到达 I*,V = 0。指标:轨迹图 + Barrier 函数时间历程。
- **Example 2(p.11, Fig. 4)**:Rc 内最优博弈:α = 0.5,T = (6.4, 3), A = (8, 0.5), D = (1.5, −1);x ∈ Rc。所有参与者连续在线重解 (17)-(19);Barrier 函数全程为正,最优捕获点时不变,A 捕获 T。
- **Example 3(p.11-12, Fig. 5-6)**:同 Example 2 参数,但 Attacker 实施 [22] 的 Pure Pursuit(PP);T/D 实施本文 CDG 最优策略 (17)-(18) 并在区域切换 Rc→Re 时改用 ATDDG 策略(切换发生在 t ≈ 0.243, Fig. 5.a);系统于 t ≈ 4.523 进入子区 Red(Fig. 5.b 显示式 (3) 中两距离之差 AT − DT);A 在捕获 T 之前被 D 拦截。结论:PP(最小化捕获时间)在 Defender 存在时非最优,[22] 策略不提供半透面。指标:Barrier 函数、AT − DT、轨迹。
- 对比基线:仅 [22] 的 PP 策略(Example 3);评价指标为屏障函数符号变化、终端结局(拦截/捕获)、Value。无数值实验规模/Monte Carlo/统计指标。

## 6. 局限性
- **作者承认的**:
  - Isaacs 方法不随状态维数扩展:"Isaacs' method does not scale well as the dimension of the state increases",闭式 C1 Value 函数在高维状态空间很难获得(p.2)。
  - 速度设置只覆盖 VA = VD:VA > VD 时 T/D 无解(直接排除,p.3 Remark);VD > VA 仅声明"结果可推广"而无推导(p.3 Remark);Theorem 1 证明外包给 [30](p.4)。
  - 对 [22] 的反驳基于反例而非一般性定理("We show by counterexample", p.2)。
  - 模型为 Isaacs simple motion + 点捕获,无惯性/过载/捕获半径(正捕获半径情形仅引 [11], p.1;非机动目标仅引 [12],[13], p.1)。
- **我分析的(推断依据)**:
  - **等速假设是零测度参数点且结论对其不连续**:按 p.3 Remark,VD 一旦低于 VA(哪怕极小),点捕获下 T/D 直接必败;而 VD > VA 又是另一种屏障结构。本文的屏障 (7)-(8) 与 Value (21) 均显式使用 AI = DI(等速),对 VD/VA 失配的鲁棒性完全未讨论——工程上速度匹配不可能精确成立。
  - **Value 的非负性未被证明**:V = DI − TI/α(式 (21))要是合法的"距离"支付,需在 Rc 内恒有 DI ≥ AI(D 在 A 捕获 T 之前到不了捕获点);文中从未作为引理陈述或证明,只是被 Game of Kind 结论隐含(若 DI < AI 则 D 可提前到 I 拦截,与 x ∈ Rc 矛盾)。这一步是隐含的几何论证。
  - **(71) 六次多项式的根选取无规则**:Corollary 1 只说 "ω* is a solution";仅屏障上证明了所选 ω* = ρ 的唯一性(p.10 "any other angle ω ≠ ρ results in DT > 0"),Rc 内部的 I* 唯一性、多根时的取舍、以及状态反馈每步重解六次方程的实时计算代价均未讨论。
  - **屏障附近解的连续性/衔接只有"值相等"层面的证明**:Theorem 3 证明 B 上两 Game of Degree 的 Value 与瞄准点相同,但未证明 Rc 内部的 I*(x) 当 x → B 时的极限行为(策略切换 (p.11 Example 3) 依赖在线重解,切换瞬间的策略连续性未分析)。
  - **无噪声/时延/感知误差**:策略为精确状态反馈(p.4),屏障函数 B(x;α) 对 A、D 位置的测量误差的敏感度未讨论。

## 7. 可复现性
- **已给出**:完整动力学与归一化(p.3);屏障系数显式 (8)(p.4);Apollonius 圆 (16)(p.5);最优策略 (17)-(19)(p.5);捕获点方程 (20)(p.6);Value (21)(p.6);梯度 (67)-(68)(p.9);六次多项式及全部系数 (71)-(72)(p.9);三个算例的完整参数(α、三方初始位置)与部分结果量(I* = (6.305, −1.224)、区域切换时刻 t ≈ 0.243、进入 Red 时刻 t ≈ 4.523)(p.10-11)。
- **缺失**:源代码/仿真程序;六次多项式根的选择准则;Rc 内 I* 的唯一性证明;屏障系数计算中 σ 在 A、D 重合时的退化处理;计算复杂度/实时性数据;对 [30] 的 Theorem 1 证明(需另行获取文献);速度失配 (VD ≠ VA) 的任何数值。

## 8. 待验证
(以下为无法在原文定位出处的推测,仅供后续核验)
1. Rc 内部最优捕获点 I* 的唯一性(六次方程 (71) 在 (0, 2π) 内实根个数与选取),以及由其保证的 Value (21) 非负(V ≥ 0 ⟺ DI ≥ AI)。
2. I*(x) 在 Rc 内连续、且 x → B 时收敛到切点(Thm 3 只证了 B 上取值相同)。
3. "结果可推广到 VD > VA"(p.3)是否保持同一屏障结构 (7)-(8),还是会退化为 A-D Apollonius 圆型屏障(快防御者文献中的典型几何)——本文未给任何推导。
4. Example 3 中区域切换时刻(t ≈ 0.243)对在线重解频率的依赖:论文称参与者"连续重解"(p.11),若离散重解,屏障函数穿越检测的时滞效应未讨论。
5. 屏障附近 A-D-T 近共线时 (8) 中 σ、以及 (71) 系数的数值病态问题(系数含 ‖A−D‖ 归一化)。

## 9. 记号表
| 原文符号 | 含义 | 首次出现位置 |
|---|---|---|
| T, A, D | Target(目标机)、Attacker(攻击弹)、Defender(防御弹) | p.1(Sec. I) |
| xT = (xT, yT), xA = (xA, yA), xD = (xD, yD) | 三方笛卡尔位置 | p.2(Sec. II-A) |
| x = (xT, yT, xA, yA, xD, yD) ∈ R6 | 博弈完整状态 | p.2(Sec. II-A) |
| VT, VA, VD | 三方常速度 | p.2(Sec. II-A) |
| α = VT/VA | 速度比,0 < α < 1 | p.2(Sec. II-A) |
| φ, χ, ψ | Target / Attacker / Defender 的瞬时航向角(控制) | p.2-3(Sec. II-A, Fig. 1, 式 (1)) |
| uT,D = {φ, ψ}, uA = {χ} | T/D 团队与 A 的控制 | p.2-3(Sec. II-A) |
| S = Se ∪ Sc | 终止集:D 拦截 A / A 捕获 T | p.3(式 (2)) |
| Red | D 的支配半空间:‖A−T‖ ≥ ‖D−T‖ | p.3(式 (3)) |
| Rea, Re | Red 之外 B<0 的逃脱区;Re = Red ∪ Rea | p.3(式 (4)-(5)) |
| Rc | Attacker 赢取区(Red 之外 B>0) | p.3(式 (4)) |
| B, B(x; α) | 屏障面 / 屏障函数 | p.3-4(式 (4),(6)) |
| bxx, byy, bxy, bx, by, b | 屏障二次型系数 | p.4(式 (7)-(8)) |
| σ | A-D 视线角(cos σ, sin σ 由 A−D 方向定义) | p.4(式 (8) 下方) |
| (x0(x), y0(x)) | A-D 线段中点(注意与初始状态 x0 记号冲突) | p.4(式 (8) 下方;x0 为初态见 p.2) |
| Red 中的 OBS | A-D 线段的中垂线(orthogonal bisector) | p.4(Remark, Fig. 2) |
| CDG | Capture Differential Game:Rc 内的 Game of Degree | p.4(Sec. II-C) |
| ATDDG | Active Target Defense Differential Game:Re 内的 Game of Degree([20],[21],[30]) | p.2(Sec. I) |
| tf, xf | 终端时刻 / 终端状态(tf 自由) | p.2, p.4(Sec. II-A, II-C) |
| J, Φ(xf) | 支付;终端 D-T 距离型终端代价 | p.4(式 (10)-(11)) |
| V(x0), V(x) | Value 函数 | p.4(式 (12));显式 p.6(式 (21)) |
| Sc(超平面式 (13)) | CDG 的终端流形(A-T 重合) | p.5(式 (13);4 维超平面表述见 p.4) |
| H | Hamiltonian | p.5(式 (14)) |
| λ = (λxA, λyA, λxD, λyD, λxT, λyT) | 协态(全部为常数,p.6) | p.5(Sec. III) |
| ν1, ν2 | 增广终端代价的 Lagrange 乘子 | p.6(式 (26)) |
| (xc, yc), r | A-T Apollonius 圆的圆心与半径 | p.5(式 (15)-(16)) |
| I : (x, y), I* : (x*, y*) | 拦截/捕获点及其最优解 | p.6(式 (43);I* 见 p.6 (20) 后) |
| AI, TI, DI | A / T / D 到拦截点的距离 | p.6-9(式 (55);TI, DI 见式 (67)-(68)) |
| (x*f, y*f) 等即 (xDf, yDf) | 终端时刻各方位置 | p.4(Sec. II-C);式 (37)-(42), p.6 |
| φ*, ψ*, χ* | 三方最优航向(指向 I*) | p.5-6(式 (17)-(19)) |
| ω* | 捕获点在 Apollonius 圆上的角参数 | p.9(Corollary 1, 式 (71)) |
| v = e^{iω} | Corollary 1 六次方程的复变量 | p.9(式 (71)) |
| ρ | A 到 D 的视线角(屏障上 ω* = ρ) | p.10(Thm 3 证明) |
| PP | Pure Pursuit([22] 中 Attacker 的策略) | p.11(Example 3) |
| R, r | [22] 记号:A−T 与 A−D 间距(仅引述用) | p.3(Remark) |
