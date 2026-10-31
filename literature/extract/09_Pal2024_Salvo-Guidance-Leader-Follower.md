# 09 | Cooperative Salvo Guidance over Leader-Follower Network with Free-Will Arbitrary Time Convergence
> Pal R.S., Kumar S.R., Mukherjee D. (IIT Bombay) | arXiv:2407.15324v1, 22 Jul 2024 | 文中未标注期刊/会议信息(IEEE 双栏排版);其初步版本为作者自引 [28](ACC 2023, pp. 4936–4941,见 p.2 与 p.13 文献)

## 0. 一句话定位
在齐射(impact-time)协同制导谱系中,本文把 "free-will arbitrary time convergence"(任意预设时间收敛,[25]–[27] 提出,仅限无向图、只能平均一致性)首次搬到 **leader-follower 有向/无向混合拓扑**的 time-to-go 一致性上(p.2 贡献 1–3):收敛时间上界可由设计者**任意指定且与初值、增益均无关**(区别于 finite-time [7][8][10] 与 fixed-time [11][24]),且因为收敛目标是 leader 的 tgo 而非平均值,可将打击时间精确设定在**各弹初始 tgo 区间之外**(p.2 贡献 3;仿真中 Td=30 s > 最大初始 tgo 27.74 s,p.7)。相对全连通一致性方法,leader-follower 结构通信负担小(leader 只需一条有向边连到一个 follower,followers 间无向环即可,p.6)、目标值可任意指派;代价是引入 leader 单点故障(p.12 作者承认)以及两阶段串行( followers 须等 leader 收敛后才开始机动,p.7)。

## 1. 问题建模
- **状态量(原文符号)**:平面交战几何量 $r_i$(径向距离)、$\theta_i$(LOS 角)、$\gamma_{Mi}$(flight path angle)、$\theta_{Mi}=\gamma_{Mi}-\theta_i$(heading angle error)、$V_{ri},V_{\theta i}$(相对速度沿/垂直 LOS 分量)(p.3, 式(4)-(6));一阶自动驾驶情形增加 $a_{Mi}$(achieved lateral acceleration)(p.3 式(7))。协同层误差变量:leader $e_\ell(t)=tgo_\ell-tgod$(p.4),followers $e_i(t)=tgo_i-tgo_\ell$(p.4),堆叠为 $\delta=[e_1,\dots,e_n]^T$;一阶情形再加 $\nu=\dot\delta$ 及 leader 的 $\delta_\ell=e_\ell,\ \nu_\ell=\dot e_\ell$(p.5–6)。
- **控制量(原文符号)**:理想自动驾驶情形为 $a_{Mi}$(lateral acceleration);一阶自动驾驶情形为指令加速度 $a_{Mci}$(p.3 式(7))。均由辅助输入 $u_\ell, u_i$(或 $u_f$)经反馈线性化/backstepping 生成(p.4 式(11)(14);p.5 式(30);p.6 式(34))。
- **动力学模型**:平面质点运动学(p.3, 式(4)-(6)):$\dot r_i=V_{ri}=-V_{Mi}\cos\theta_{Mi}$,$r_i\dot\theta_i=V_{\theta i}=-V_{Mi}\sin\theta_{Mi}$,$\dot\gamma_{Mi}=a_{Mi}/V_{Mi}$。自动驾驶:(i) 理想(瞬时实现 $a_{Mi}$);(ii) 一阶滞后 $\dot a_{Mi}=(a_{Mci}-a_{Mi})/\tau_i$(p.3 式(7))。time-to-go 采用 [7] 的估计式(p.3–4 式(8)):$tgo_i=\frac{r_i}{V_{Mi}}\left(1+\frac{\theta_{Mi}^2}{2K}\right),\ K=2N-1$,$N=3$(PN 导航比),含小角近似。
- **通信拓扑**:leader-follower 混合拓扑。单一 leader;followers 之间为**无向、连通、无权图**(仿真用 4 节点环,p.6);leader 到一个或多个 follower 为**单向有向边**。交互矩阵 $H=L_f+B$,$L_f$ 为 follower 图 Laplacian,$B$ 为 leader 关联(incidence)矩阵(p.2–3);$H$ 对称正定(p.3)。不要求持续连通性讨论——按假设 follower 图连通、通信无时延无失败(Assumption 2/4,p.3)。
- **目标泛函/终端条件**:无最优性泛函。终端条件为时间指派:leader 的 $tgo_\ell$ 在预设时刻 $t_{f\ell}$ 前收敛到 $tgod=T_d-t_{el\ell}$;followers 的 $e_i$ 在预设时刻 $t_f$ 前收敛到 0;从而所有弹 $\dot{tgo}=-1$ 同步、于 $t=T_d$ 同时命中(p.3–4)。到达时间指定方式:$T_d$ 只告知 leader(Assumption 2),通过 leader→follower 的信息流传递;$t_{f\ell},t_f$(及一阶情形的 $t_1$)在开跑前离线固定指定,论文未考虑在线重设。
- **机动目标**:未提及(仅静止目标;机动目标被明确列为未来工作,p.1 Note to Practitioners 与 p.12)。
- **约束**:设计层面未显式处理输入饱和;仿真中 $|a_{Mi}|\le 300\ \mathrm{m/s^2}$(p.7、p.10);控制界进入建模被列为未来工作(p.12)。视场(FOV)约束:未提及。
- **噪声/时延**:Assumption 4 明确不考虑通信时延与失败(p.3);时延/退化/故障列为未来工作(p.12)。无过程/量测噪声建模。

## 2. 假设条件
1. **Assumption 1**(p.3):拦截弹为质点,全程速度恒定。
2. **Assumption 2**(p.3):单一 leader,其余为 follower 且在无向连通图上通信;**期望终端时间 $T_d$ 仅 leader 已知**。
3. **Assumption 3**(p.3):leader 到一个或多个 follower 的信息流为单向。
4. **Assumption 4**(p.3):弹间通信无时延、无失败。
5. 主问题陈述限定于 Assumptions 1–3(p.3);导航比固定 $N=3$(p.3–4 式(8))。
6. **leader 受控**:leader 自身也按同样运动学建模并施加制导律(式(11)/(13)、(30)-(32)),并非虚拟 leader(p.4–5)。
7. **follower 可测得自身 tgo**:式(8) 只需 $r_i,V_{Mi},\theta_{Mi}$,均为自身量测量;followers 通过通信获得 leader 的 $tgo_\ell$(误差定义 $e_i=tgo_i-tgo_\ell$ 隐含 $[\,t_{f\ell},t_f\,]$ 内需持续接收 $tgo_\ell$,p.4 式(15))。
8. **时间参数化**:$t_{f\ell},t_f,t_1$ 为开跑前固定指定的"free-will"时间,与初值、增益无关(Lemma 1,p.3);全文无在线重设机制。
9. **目标静止、二维平面交战**(p.3 Section III 开头)。
10. 式(8) 使用 $\theta_{Mi}$ 小角近似;作者承认并援引 [7][8][10][11] 的广泛使用与 V-D 节对比佐证(p.4,p.11)。

## 3. 方法核心
机制一句话:**分层两阶段的"时间基函数"预设时间一致性**——把每弹的 time-to-go 估计(式(8))经反馈线性化(理想)或精确线性化+backstepping(一阶自动驾驶)化为积分器误差动力学,再用 [25] 型时变增益控制律 $u\propto-\frac{\eta}{t_f-t}(1-e^{-(\cdot)})$ 使误差在**设计者任意指定的时刻**前收敛(Lyapunov 函数满足 Lemma 1 的 $\dot V\le-\frac{\eta}{t_f-t}(1-e^{-V})$ 型界,与初值和增益无关);leader 先在 $t_{f\ell}$ 内锁定理想时间轨线 $tgod=T_d-t_{el\ell}$($\dot{tgod}=-1$),followers 随后在 $t_f$ 前经一致性协议收敛到 leader 的 tgo,全体 $\dot{tgo}=-1$ 故在 $T_d$ 精确同时命中。

关键公式(均可在原文定位):
- tgo 估计式(8):$tgo_i=\frac{r_i}{V_{Mi}}(1+\theta_{Mi}^2/2K),K=2N-1,N=3$(p.3–4)。
- tgo 一阶动力学(9)(10):$\dot{tgo}_i=F_i+B_i a_{Mi}$,$F_i=\frac{V_{ri}tgo_i}{r_i}-\frac{V_{\theta i}\theta_{Mi}}{V_{Mi}K}$,$B_i=\frac{r_i\theta_{Mi}}{V_{Mi}^2K}$(p.4)。
- **理想自动驾驶 / leader**:反馈线性化 $a_{M\ell}=\frac{1}{B_\ell}(u_\ell-F_\ell-1)\Rightarrow \dot e_\ell=u_\ell$(式(11),p.4);free-will 律(12)(13):$u_\ell=-\frac{\eta_\ell}{t_{f\ell}-t}(1-e^{-e_\ell(t)})$($t_0\le t<t_{f\ell}$),之后 $u_\ell=0$、$a_{M\ell}=\frac{1}{B_\ell}(-F_\ell-1)$ 维持 $\dot{tgo}_\ell=-1$;$\eta_\ell>1$(p.4)。
- **理想自动驾驶 / followers**:同型线性化 $a_{Mi}=\frac{1}{B_i}(u_i-F_i-1)\Rightarrow\dot e_i=u_i$(式(14),p.4);一致性律(15):$u_f=0\ (t<t_{f\ell})$;$u_f=-\frac{\eta_f}{t_f-t}(\mathbf 1_n-e^{-H\delta})\ (t_{f\ell}\le t<t_f)$;之后 $u_f=0$;增益条件 $\eta_f>\frac{1}{\lambda_{\min}(H)}$(p.4)。
- 理想情形稳定性链:Lyapunov $V=\delta^TH\delta$,$\dot V\le-\frac{2\eta_f}{t_f-t}\|H\delta\|(1-e^{-\|H\delta\|})$(式(19),用 Lemma 3);结合 $\lambda_{\min}(H)\|\delta\|^2\le V\le\|\delta\|\|H\delta\|$(式(20)-(22))得 $\dot V\le-\frac{2\eta_f\sqrt{\lambda_{\min}(H)}}{t_f-t}\sqrt V(1-e^{-\sqrt{\lambda_{\min}(H)V}})$(式(24),p.4);换元 $\xi=\sqrt{\lambda_{\min}(H)V}$,$\dot\xi\le-\frac{\eta'}{t_f-t}(1-e^{-\xi}),\ \eta'=\lambda_{\min}(H)\eta_f$,由 Lemma 1 当 $\eta'>1$ 时 $\delta=0$ 于 $t\in(t_{f\ell},t_f]$(p.5)。
- **一阶自动驾驶 / tgo 二阶动力学**(25)(26):$\ddot{tgo}_i=\dot F_i+\dot B_i a_{Mi}-\frac{B_i}{\tau_i}a_{Mi}+\frac{B_i}{\tau_i}a_{Mci}$(p.5);辅助导数(27)-(29)及 $\dot F_i,\dot B_i$ 显式表达式(p.5)。
- **一阶 / leader**:线性化 $a_{Mc\ell}=\frac{\tau_\ell}{B_\ell}\big[u_\ell-\dot F_\ell-(\dot B_\ell-\frac{B_\ell}{\tau_\ell})a_{M\ell}\big]\Rightarrow\ddot e_\ell=u_\ell$(式(30)(31),p.5);backstepping 律(32):$u_\ell=-\delta_\ell-\frac{\partial\psi_1}{\partial t}-\nu_\ell\frac{\partial\psi_1}{\partial\delta_\ell}-\frac{\eta_{\ell2}}{t_{f\ell}-t}(1-e^{-z_\ell})$,其中 $\psi_1(\delta_\ell,t)=-\frac{\eta_\ell}{t_{f\ell}-t}(1-e^{-\delta_\ell})$,$z_\ell=\nu_\ell+\psi_1$,$\eta_\ell,\eta_{\ell2}\ge1$;依 [25] §4.2,$\delta_\ell\to0,\nu_\ell\to0$ 于 $t<t_{f\ell}$(p.5)。
- **一阶 / followers**:$\ddot e_i=\dot F_i+(\dot B_i-\frac{B_i}{\tau_i})a_{Mi}+\frac{B_i}{\tau_i}a_{Mci}$(式(33)),$a_{Mci}=\frac{\tau_i}{B_i}[u_i-\dot F_i-(\dot B_i-\frac{B_i}{\tau_i})a_{Mi}]\Rightarrow\ddot e_i=u_i$(式(34)(35)),$\dot\delta=\nu,\dot\nu=u_f$(式(36))(p.6)。
- 一阶一致性律(37)(backstepping,三段式):$z=\nu+\phi$,$\phi(t,\delta)=\frac{\eta_f}{t_f-t}(\mathbf 1_n-e^{-H\delta})$;$u_f=0\ (t<t_{f\ell})$;$u_f=-\frac{\partial\phi}{\partial\delta}\nu-\frac{\partial\phi}{\partial t}-\frac{\eta_{f2}}{t_1-t}(\mathbf 1_n-e^{-z})\ (t_{f\ell}\le t<t_1)$;$u_f=-\frac{\partial\phi}{\partial\delta}\nu-\frac{\partial\phi}{\partial t}\ (t_1\le t<t_f)$;$\eta_{f2}>1$(p.6)。其中 $\frac{\partial\phi}{\partial\delta}=\frac{\eta_f}{t_f-t}\mathrm{diag}(e^{-H\delta})H$,$\frac{\partial\phi}{\partial t}=\frac{\eta_f}{(t_f-t)^2}(\mathbf 1_n-e^{-H\delta})$(p.6)。
- 一阶稳定性链:$V_z=z^Tz$,$\dot V_z\le-\frac{2\eta_{f2}}{t_1-t}\sqrt{V_z}(1-e^{-\sqrt{V_z}})$(式(39)-(41)),$\xi=\sqrt{V_z}$ 由 Lemma 1 于 $t_1$ 前 → 0,得 $\nu=-\phi\ (t\ge t_1)$,退化为单积分器 $\dot\delta=-\frac{\eta_f}{t_f-t}(\mathbf 1_n-e^{-H\delta})$(式(43)),$\delta\to0$ 于 $t_f$(p.6)。
- **Remark 1**(p.5):沿用 [10],只要一致性在各自碰撞航线收拢之前完成($t_{f\ell},t_f$ 取得足够小于 $T_d$),$B_i\propto\theta_{Mi}$ 导致的奇异($\theta_{Mi}\to0$)可避免。

## 4. 理论结果
本文**无自行编号的定理/命题**,主结论在正文 IV-A/IV-B 中以 Lyapunov 推导给出;编号结果为 3 条引理 + 1 条注记:
- **Lemma 1**(引自 [25] Theorem 1,p.3):若存在满足 $\beta_1(x)\le V(t,x)\le\beta_2(x)$、$V(t,0)=0$ 且 $\dot V\le-\frac{\eta}{t_f-t}(1-e^{-V})$($\eta\ge1$)的 $V$,则 $x=0$ free-will arbitrary time stable,$t_f$ 可任意预指定;该不等式严格成立时恰在 $t_f$ 收敛(原文措辞 "If the equality in (3) holds strictly… convergence to x=0 occurs at tf",表述略显含混,见第 8 节)。前提:$x=0$ 为域 $D$ 内平衡点。
- **Lemma 2**(引自 [26] Lemma 2,p.3):对 $0<x\le y$,$-x(1-e^{-x})\ge-y(1-e^{-y})$。
- **Lemma 3**(引自 [26] Lemma 3,p.3):对 $x\in\mathbb R^n$,$-\|x\|(1-e^{-\|x\|})\ge-x^T(I_n-e^{-\mathrm{diag}(x)})\mathbf 1_n\ge-x^T(\mathbf 1_n-e^{-x})$。
- **Remark 1**(p.5):$\theta_{Mi}\to0$ 引起的奇异性可通过令 $t_{f\ell},t_f\ll T_d$ 及选择增益规避(前提:一致性先于碰撞航线收敛完成)。
- **主结果 A(理想自动驾驶,IV-A,p.4–5,未编号)**:在式(11)–(15) 下,若 $\eta_\ell>1$、$\eta_f>\frac1{\lambda_{\min}(H)}$,则 leader 的 $e_\ell\to0$ 于 $t\le t_{f\ell}$,followers 的 $\delta\to0$ 于 $t\in(t_{f\ell},t_f]$,即 tgo 一致性在任意预指定时刻前完成、与初值和设计参数无关。前提:Assumptions 1–4、$H$ 对称正定(follower 图连通)、$\lambda_{\min}(H)>0$。
- **主结果 B(一阶自动驾驶,IV-B,p.5–6,未编号)**:在式(30)–(37) 下,若 $\eta_\ell,\eta_{\ell2}\ge1$、$\eta_{f2}>1$、$\eta_f>\frac1{\lambda_{\min}(H)}$,则 $\delta\to0$ 且 $\nu\to0$ 于 $t_f$ 前($z\to0$ 于 $t_1$,$\delta\to0$ 于 $t_f$)。前提同上,另需 $t_{f\ell}<t_f$ 且两时间之间留足机动余量(p.6);原文结论句写作"收敛区间 $t_{f\ell}\le t< t_f-t_{f\ell}$",疑为笔误(见第 8 节)。

## 5. 实验设置
- **场景与拓扑**(p.6–11):主场景 1 leader + 4 followers,followers 为无向环,leader→Follower 1 单向边;$L_f,B$ 矩阵显式给出,$\lambda_{\min}(H)=0.186$(p.6)。可扩展性场景 1 leader + 8 followers、更复杂图(仅给图 Fig. 9a,p.10–11),$\eta_f=24.7572$。
- **初值组**(Table I,p.7):Set 1 同距离 5000 m、同速 200 m/s、不同方位角/航向角(考察 heading error 影响);Set 2 不同距离 [10500,11000,9800,10000,9500] m(考察初始位置);Set 3 不同速度 [630,630,600,570,594] m/s(考察速度差异;注意表中 Follower 2 的 $r_0$ 排版为 600 m,与 p.9 正文"均为 6000 m"矛盾,见第 8 节)。
- **参数扫描**(理想自动驾驶,p.7–9):基准 $T_d=30$ s、$t_{f\ell}=5$ s、$t_f=25$ s、$\eta_\ell=2$、$\eta_f=10.73$;变 $t_f=10$ s 考察收敛时间上界选取;变 $T_d=27.52$ s 考察可达下限;Set 2 场景 $T_d=65$ s、$t_f=50$ s、$\eta_\ell=3$;Set 3 场景 $T_d=12$ s、$t_{f\ell}=2$ s、$t_f=10$ s、$\eta_\ell=3$。
- **一阶自动驾驶**(p.9–10):Set 1 初值,$T_d=30$ s,$\tau=0.5$ s,$t_{f\ell}=5$ s、$t_f=25$ s、$t_1=24$ s,$\eta_\ell=7$、$\eta_{\ell2}=1.5$、$\eta_f=15$、$\eta_{f2}=4$;因指数项数值溢出,对式(31)(35) 两端乘 0.01 正则化;$|a_{Mi}|\le300\ \mathrm{m/s^2}$。
- **对比基线**(V-D,p.11–12):[30] Sinha, Kumar, Mukherjee(AST 2022)§3.1.1 的 leader-follower 一体化制导;同初值(10 km、400 m/s、$T_d=30$ s、leader→Follower 1,2 单向 + followers 双向,即 Fig. 9b)。
- **评价指标**:命中时刻对 $T_d$ 的精度、tgo 一致性完成时刻相对 $t_{f\ell}/t_f$、法向加速度饱和幅值与时长、终端加速度是否归零、heading error 是否归零(最大末速)、与 [30] 相比的初始 tgo 数值吻合度与指令平滑性。无 Monte Carlo、无噪声/时延/失配仿真。

## 6. 局限性
- **作者承认的**:
  - 一致性律中的指数项使 tgo 差大时指令过大而饱和;控制界未纳入设计,只能靠"明智地"选取 $T_d,t_{f\ell},t_f$ 与增益缓解(p.12;p.10 的 0.01 正则化亦是同一问题的补丁)。
  - 仅静止目标、仅 leader-follower 拓扑;一般有向拓扑 + 机动目标为未来工作(p.1 Note to Practitioners、p.12)。
  - 未考虑通信时延/退化/失败(Assumption 4,p.3;p.12 列为未来方向)。
  - leader-follower 固有单点故障:leader 失效则全体 follower 失效;leader 选取需依初始 tgo 慎重(p.12)。
- **我分析的**(附推断依据):
  - **串行两阶段浪费机动时间**:followers 在 $t<t_{f\ell}$ 时 $u_f=0$(式(15)(37)),leader 阶段占用的时间直接从 follower 一致性窗口中扣除(p.7 "follower interceptors start their maneuver after $t=t_{f\ell}$");leader 成为时间预算与可靠性瓶颈(与 p.12 单点故障承认相印证)。
  - **除以 $B_i$ 的奇异性只是"调度规避"而非不变性证明**:$a_{Mi}=\frac{1}{B_i}(u_i-F_i-1)$,$B_i\propto\theta_{Mi}$(式(10)),Remark 1(p.5)仅论证可选 $t_{f\ell},t_f\ll T_d$ 来避免 $\theta_{Mi}\to0$,无严格证明;$T_d$ 下限场景(p.8,Follower 1 航迹已近直线)正是该机制逼近失效的体现,且可达 $T_d$ 的下界无解析刻画(p.8 仅观察到)。
  - **时变增益 $\frac{1}{t_f-t},\frac{1}{t_1-t}$ 在切换点附近无界**,对实现时序误差、自动驾驶仪滞后敏感;$e^{-H\delta}$ 对大 $|\delta|$ 数值溢出(p.10 需 0.01 缩放即为证据),工程实现需抗饱和与保护逻辑,论文未讨论离散实现。
  - **tgo 估计的小角近似缺乏误差界**:式(8) 依赖 $\theta_{Mi}$ 小角近似(p.4),Set 1 中方位角最大 120°、大 heading error 下估计偏差未量化,仅凭与 [30] 的初始 tgo 数值接近(p.11)间接佐证。
  - **恒速假设与一阶自动驾驶不自洽**:真实弹体做机动时速度会衰减,Assumption 1(p.3)在带滞后模型下更受挑战,论文未讨论。
  - **增益条件依赖全局拓扑信息**:$\eta_f>\frac1{\lambda_{\min}(H)}$ 要求设计者掌握整张 follower 图(p.4),并非严格分布式;仿真中 $\eta_f=10.73\approx 2/\lambda_{\min}$(p.7)也按拓扑整体选取。
  - **无 FOV 约束**:导引律允许弹体先远离目标再回转(p.10 "interceptors tend to veer away from the target initially"),对寻的头视场不友好,论文未与 [6][19] 一类 FOV 约束方法比较。
- (拿不准、原文无出处者见第 8 节。)

## 7. 可复现性
- **已给出**:全部制导律显式表达式(式(11)-(15)、(30)-(37),p.4–6);$\dot F_i,\dot B_i$ 解析式(p.5);所有场景初值(Table I,p.7;8-follower 场景 p.11;对比场景 p.11);每场景的 $T_d,t_{f\ell},t_f,t_1$ 与增益($\eta_\ell,\eta_f,\eta_{\ell2},\eta_{f2}$)数值;$L_f,B$ 矩阵与 $\lambda_{\min}(H)=0.186$(p.6);$N=3$(p.4);加速度界 300 m/s²、$\tau=0.5$ s、正则化因子 0.01(p.7、9、10)。
- **缺失**:未提供代码/数据;积分算法与步长未说明;图中绘制的是真实 tgo 还是估计 tgo 未说明;8-follower 场景的图仅以示意图给出、无矩阵;仿真软件未注明;$t_1$ 的选取准则无解析说明(仅给 $t_1=24$ s,p.10);0.01 正则化对理论增益条件的影响未讨论。

## 8. 待验证
- p.5 "the desired time-to-go is $tgod=T_d-tgo_\ell$" 疑为笔误:p.3–4 与式(11) 前后均定义 $tgod=T_d-t_{el\ell}$(原文如此,已核对 PDF 文本)。
- p.6 结论句"converge to 0 … within a fixed time which is bounded in the interval $t_{f\ell}\le t< t_f-t_{f\ell}$"疑为笔误,按推导应为 $t_{f\ell}\le t<t_f$($z$ 于 $t_1<t_f$ 收敛、$\delta$ 于 $t_f$ 收敛);原文如此。
- Table I Set 3 中 Follower 2 的 $r_0=600$ m 与 p.9 正文"each interceptor is located at the same radial distance of 6000 m"矛盾,疑表格排版漏零。
- Lemma 1 末句"If the equality in (3) holds strictly…convergence to x=0 occurs at tf"(p.3)语义含混:"equality holds strictly"应指严格不等式,需对照 [25] Theorem 1 确认"恰在 $t_f$ 收敛"的确切条件。
- p.6 推导行"$\dot e_i=\dot{tgo}_i-\dot{tgo}_\ell=\dot{tgo}_i+1=\ddot{tgo}_i-\ddot{tgo}_\ell=\ddot{tgo}_i$"一阶/二阶混写,应理解为 $\dot e_i=\dot{tgo}_i+1$ 与 $\ddot e_i=\ddot{tgo}_i$ 两式合并,核对后仍以原意为准。
- 式(15) 隐含 followers 在 $[t_{f\ell},t_f]$ 内需**持续**接收 leader 的 $tgo_\ell$(而非 $t_{f\ell}$ 时刻快照),通信负载与该假设的必要性原文未明说。
- 0.01 正则化缩放(式(31)(35) 两端)是否等效缩放了理论增益条件($\eta$ 的有效值),原文未分析。

## 9. 记号表
| 原文符号 | 含义 | 首次出现位置 |
|---|---|---|
| $r_i$ | 第 i 弹到目标的径向距离 | p.3, Section III |
| $V_{Mi}$ | 第 i 弯速度(恒定) | p.3 |
| $\gamma_{Mi}$ | 第 i 弹 flight path angle(弹道倾角) | p.3 |
| $\theta_i$ | LOS 角 | p.3 |
| $\theta_{Mi}$ | heading angle error,$\theta_{Mi}=\gamma_{Mi}-\theta_i$ | p.3, 式(4) 下方 |
| $a_{Mi}$ | 第 i 弹(已实现的)侧向加速度 | p.3, 式(6) |
| $V_{ri},V_{\theta i}$ | 相对速度沿/垂直 LOS 的分量 | p.3, 式(4)(5) |
| $a_{Mci}$ | 侧向加速度指令 | p.3, 式(7) |
| $\tau_i$ | 自动驾驶仪时间常数 | p.3, 式(7) |
| $tgo_i$ | 第 i 弹 time-to-go(剩余时间) | p.3, 式(8) 上方 |
| $t_{impi}=t_{eli}+tgo_i$ | impact time(发射起总时间) | p.3 |
| $t_{eli}$ | 第 i 弹已飞行时间(elapsed time) | p.3 |
| $T_d$ | 期望打击时间(desired impact time) | p.3 |
| $tgod=T_d-t_{eli}$ | 期望 time-to-go 轨线($\dot{tgod}=-1$) | p.3 |
| $\mathcal G,\mathcal V,\mathcal E$ | 通信图、顶点集、边集 | p.2, Section II |
| $N_i$ | 第 i 弹的邻居集 | p.2 |
| $H=L_f+B$ | leader-follower 交互矩阵(对称正定) | p.2 |
| $L_f$ | follower 无向图 Laplacian | p.2 |
| $B$ | leader 关联(incidence)矩阵 | p.2 |
| $\lambda_{\min}(H)$ | $H$ 最小特征值 | p.4, 式(15) 下方 |
| $K=2N-1,\ N=3$ | tgo 估计中的导航比参数 | p.3–4, 式(8) |
| $F_i,\ B_i$ | tgo 动力学中的漂移/输入系数 | p.4, 式(10) |
| $e_\ell(t)=tgo_\ell-tgod$ | leader 的时间误差 | p.4, 式(11) 上方 |
| $e_i(t)=tgo_i-tgo_\ell$ | follower 时间误差 | p.4, 式(14) 上方 |
| $u_\ell,\ u_i/u_f$ | 辅助控制输入 | p.4, 式(11)(14)(15) |
| $\delta=[e_1,\dots,e_n]^T$ | follower 误差堆叠向量 | p.4, 式(15) 上方 |
| $\eta_\ell,\ \eta_f$ | leader/follower free-will 律增益 | p.4, 式(12)(15) |
| $t_{f\ell}$ | leader 收敛的任意预设时间 | p.4, 式(12) |
| $t_f$ | followers 一致性的任意预设时间 | p.4, 式(15) |
| $\mathbf 1_n,\ e^{-H\delta}$ | 全 1 向量;$e^{-H\delta}$ 按元素取负指数 | p.4, 式(15) |
| $V=\delta^TH\delta$ | 理想情形 Lyapunov 函数 | p.4, 式(16) 上方 |
| $\xi=\sqrt{\lambda_{\min}(H)V}$ | 理想情形换元变量 | p.5 |
| $\eta'=\lambda_{\min}(H)\eta_f$ | 等效增益 | p.5 |
| $\dot F_i,\ \dot B_i$ | $F_i,B_i$ 的时间导数(解析式) | p.5 |
| $\delta_\ell,\ \nu_\ell$ | leader 二阶误差状态($e_\ell,\dot e_\ell$) | p.5, 式(31) 下方 |
| $\psi_1(\delta_\ell,t),\ z_\ell$ | leader backstepping 的虚拟控制与复合变量 | p.5, 式(32) 下方 |
| $\eta_{\ell2},\ \eta_{f2}$ | 一阶情形 backstepping 第二步增益 | p.5 式(32);p.6 式(37) |
| $\nu=\dot\delta$ | follower 误差导数堆叠 | p.6, 式(36) |
| $\phi(t,\delta)$ | backstepping 虚拟控制($z=\nu+\phi$) | p.6 |
| $z=\nu+\phi$ | backstepping 复合变量 | p.6 |
| $t_1$ | 一阶情形中间切换时间($t_{f\ell}<t_1<t_f$) | p.6, 式(37) |
| $V_z=z^Tz$ | 一阶情形 Lyapunov 函数 | p.6, 式(39) 上方 |
