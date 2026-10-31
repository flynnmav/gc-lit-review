# 01 | An Introduction to Pursuit-Evasion Differential Games
> Weintraub I., Pachter M., Garcia E. | ACC 2020 (tutorial) | arXiv:2003.05013

## 0. 一句话定位
ACC 2020 教程(tutorial)论文,是追逃微分博弈的"坐标基准"型综述:以参与者数量为纲(1v1、Nv1、1vM、NvM)梳理 Isaacs 以来谱系(p.1 摘要、p.2–5 Sec. III),技术核心是两个 simple-motion 多智能体案例的完整"建模—求解—验证"闭环:①Two Cutters and Fugitive Ship(2 追 1 逃,时间最优协同捕获,Sec. IV,p.5–11);②主动目标防御微分博弈 ATDDG(Target–Attacker–Defender,Sec. V,p.12–16)。相对已有文献的新增内容:对 2P1EDG 给出验证定理的完整证明、识别其 dispersal 型奇异面、并用其解近似多追多逃指派问题(p.6 "extends the presentation in [60] by offering a complete proof of the verification theorem";p.11);Sec. V 则是对 [111] 方法的总结。**注意:本文并不讲解 PN/PP/APN 制导律的博弈论解释**——PN/PP 仅在综述里作为文献提及(p.12–13,[91],[109] 中 defender 用 PN、attacker 用 PP),两个案例全部基于 Isaacs 式 simple motion(常速、航向控制)。

## 1. 问题建模
教程包含多个子问题,按"通用框架 + 两个案例"分列。

### 1.0 通用框架(Sec. IV 开头,p.6)
- 状态量(原文符号):$x(t)$,初值 $x(0)=x_0$。
- 控制量(原文符号):$u(t)$、$v(t)$,分别为两队的控制,须属于适当子空间;考虑状态反馈策略 $u(t)=\mu(t,x(t))$、$v(t)=\nu(t,x(t))$(p.6)。
- 动力学模型(类型与方程,p.6,式 (1)):$\dot{x}=f(t,x(t),u(t),v(t)$, $t\in[0,t_f]$。
- 参与者与支付/终端流形:零和两人(两队)博弈;性能泛函(p.6,式 (2)):$J=q(x(t_f))+\int_0^{t_f}g(t,x(t),u(t),v(t))\,\mathrm{d}t$;终端流形由终端代价 $q(x(t_f))$ 刻画(未给具体集合)。
- 机动目标:未提及(通用层面)。
- 约束(输入/状态/视场):仅说控制"required to belong to an appropriate subspace"(p.6),未具体化。
- 噪声/时延:未提及(通用框架为确定性)。

### 1.1 子问题 A:Two Cutters and Fugitive Ship(2P1EDG,2 追 1 逃,Sec. IV,p.5–8)
- 状态量(原文符号):$x := (x_E, y_E, x_{P1}, y_{P1}, x_{P2}, y_{P2})\in\mathbb{R}^6$,即 E、P1、P2 的笛卡尔坐标 $x_E=(x_E,y_E)$、$x_{P1}$、$x_{P2}$(p.6)。
- 控制量(原文符号):E 的瞬时航向 $u_E=\{\varphi\}$;P1、P2 的瞬时航向 $u_P=\{\psi_1,\psi_2\}$(p.6)。
- 动力学模型(类型与方程):simple motion(全向、常速、速度归一化),p.6 式 (4):
$$\dot{x}_E=\cos\varphi,\ \dot{y}_E=\sin\varphi;\quad \dot{x}_{P1}=\beta_1\cos\psi_1,\ \dot{y}_{P1}=\beta_1\sin\psi_1;\quad \dot{x}_{P2}=\beta_2\cos\psi_2,\ \dot{y}_{P2}=\beta_2\sin\psi_2$$
其中 $\beta_1=v_{P1}/v_E>1$、$\beta_2=v_{P2}/v_E>1$(两追者速度不必相等)。
- 参与者与支付/终端流形:参与者 E(最大化捕获时间)与协同的 P1、P2(最小化捕获时间);性能泛函(p.6,式 (6)):$\min_{\psi_1,\psi_2}\max_\varphi \int_0^{t_f}\mathrm{d}t$。终端流形为点捕获(p.6,式 (5)):a) $x_{P1}=x_E, y_{P1}=y_E$,或 b) $x_{P2}=x_E, y_E=y_E$,或 c) a) 与 b) 同时成立。
- 机动目标:被追的 E 即机动体,控制量仅为航向 $\varphi$(可瞬时改变方向)。
- 约束(输入/状态/视场):状态与控制无额外约束;开阔平面(无障碍/边界;p.6 以"逃出影响区/安全港"为动机但未建模);点捕获(零捕获半径)。
- 噪声/时延:无(确定性、完全信息;p.11 dispersal 面讨论中隐含"量测 E 新位置后重解博弈")。

### 1.2 子问题 B:ATDDG(主动目标防御微分博弈,Sec. V,p.12–16)
- 状态量(原文符号):$x := (x_T, y_T, x_A, y_A, x_D, y_D)\in\mathbb{R}^6$(T=Target、A=Attacker、D=Defender 的笛卡尔坐标);博弈集为整个 $\mathbb{R}^6$(p.13)。降维状态空间(利用 WLOG 规范几何 $x_D=-x_A,\ y_A=0,\ y_D=0,\ y_T\ge 0$):$x=(x_A, x_T, y_T)$(p.13)。
- 控制量(原文符号):T/D 队控制 $u_{T,D}=\{\varphi,\psi\}$(φ 为 T 的航向,ψ 为 D 的航向);A 的控制 $u_A=\{\chi\}$(p.13)。
- 动力学模型(类型与方程):simple motion "à la Isaacs",p.13 式 (41):
$$\dot{x}_A=\cos\chi,\ \dot{y}_A=\sin\chi;\quad \dot{x}_D=\cos\psi,\ \dot{y}_D=\sin\psi;\quad \dot{x}_T=\alpha\cos\varphi,\ \dot{y}_T=\alpha\sin\varphi$$
速度归一化 $V_A=V_D=1$、$V_T=\alpha$。
- 参与者与支付/终端流形:两队零和——T/D 队(T 与 D 协同)对 A。终止集(p.13,式 (42)–(44)):$S=S_e\cup S_c$,$S_e=\{x\,|\,\sqrt{(x_A-x_D)^2+(y_A-y_D)^2}=0\}$(D 拦截 A,T 逃生),$S_c=\{x\,|\,\sqrt{(x_A-x_T)^2+(y_A-y_T)^2}=0\}$(A 捕获 T)。本文聚焦 $S_e$ 情形的 Game of Degree,支付为终端 A–T 距离(p.13,式 (45)):$J_c(u_A,u_B,\tilde{x}_0):=\tfrac{1}{2}[(x_{Af}-x_{Tf})^2+(y_{Af}-y_{Tf})^2]$。Game of Kind 的解即谁能赢(p.13)。
- 机动目标:T 为主动机动目标(Active Target,可机动并与 D 协同,p.12);A、D 亦全向机动。
- 约束(输入/状态/视场):容许控制 $\chi,\varphi,\psi\in[-\pi,\pi]$(p.13);"Both, the state and the controls, are unconstrained"(p.13);点捕获;无视场约束。
- 噪声/时延:本案例无(确定性);综述提及相关工作用 EKF 与传感器模型([92],p.13)、PN/PP + 信息受限 + T 航向率约束([91],[109],p.12–13),但均非本文案例设定。
- 常用性能指标(p.12):Game of Kind 的胜负;Game of Degree 中,若 T 逃生,用 A 被 D 拦截瞬间 A–T 距离;若 T 被捕,用捕获瞬间 D–A 距离;捕获时间亦是关注指标。

## 2. 假设条件
**通用框架(Sec. IV 开头)**
1. 策略限制在状态反馈策略类 $u(t)=\mu(t,x(t))$、$v(t)=\nu(t,x(t))$(p.6)。
2. Theorem 1(验证用)要求存在 $C^1$ 的 Value 函数 $V(t,x)$ 满足 HJI PDE 及终端条件(p.6)。

**子问题 A(2P1EDG,Sec. IV)**
3. Simple motion:三方全向(holonomic)、速度为正常数 $v_E, v_{P1}, v_{P2}$(p.6,IV-A)。
4. 两追者都快于逃逸者:$\beta_1>1,\ \beta_2>1$(p.6;Prop. 1 重申 p.8)。
5. 两追者显式协同(exlicit cooperation)以最小化捕获时间;E 最大化捕获时间(p.6)。
6. 速度按 $v_E$ 归一化(式 (4) 中 E 速度为 1);Remark(p.11):真实捕获时间 = $V/v_E$。
7. 点捕获:任一追者与 E 重合即结束(式 (5),p.6)。
8. 开阔平面、无障碍与边界、状态无约束(全文建模未含;p.6 仅以"安全港"为动机叙述)。
9. 完全信息、确定性(隐含;p.11:"After measuring the Evader's new position, the Pursuers recompute the solution of the game")。
10. IV-D 多追多逃扩展中:每个 Pursuer 恰好指派给一个 Evader;"We do not consider cases where three Pursuers may be assigned to a single Evader"(p.11,算例只用 2–2–1 指派)。

**子问题 B(ATDDG,Sec. V)**
11. Simple motion à la Isaacs,欧氏平面博弈(p.13)。
12. 目标慢于攻击者:$\alpha=V_T/V_A<1$(p.13;Theorem 3 中参数范围写作 $0\le\alpha<1$,p.14;Prop. 2 中为 $0<\alpha<1$,p.13)。
13. 攻击者与防御者能力相当:$V_A=V_D$,归一化 $V_A=V_D=1$、$V_T=\alpha$(p.13)。
14. 容许控制 $\chi,\varphi,\psi\in[-\pi,\pi]$;状态与控制均无约束(p.13)。
15. 两种终端均为点捕获(间距为零,式 (43)(44),p.13)。
16. 聚焦 D 拦截 A(式 (43))成立时的 Game of Degree,支付为终端 A–T 距离(式 (45),p.13)。
17. WLOG 降维几何:$x_D=-x_A,\ y_A=0,\ y_D=0,\ y_T\ge0$,降维状态 $(x_A,x_T,y_T)$(p.13);依赖问题的平移/旋转不变性。
18. T 与 D 协同对抗 A(ATDDG 的定义,p.12)。
19. 正则解为直线轨迹(协态恒定,证明中导出,p.14)。
20. ATDDG 逃逸区策略的验证由 [112] 完成;捕获区仅有候选解 [113]、验证尚在进行("a topic of current research",p.16)。

## 3. 方法核心
机制:教程以 Isaacs 框架演示两类标准解法并形成闭环——(i) 2P1EDG 用"两侧 PMP":写 Hamiltonian、$\min\max H\equiv0$ 得到以协态表示的最优航向 (9)–(11),协态动力学为零 → 协态恒定 → 最优轨迹为直线;按激活的终端条件分三情形:a)/b) 退化为 1P1E(E 沿初始视线反向逃离,$\varphi^*=\lambda_i$),c) 同时捕获由两个 Apollonius 圆的交点给出瞄准点;再用 HJI 验证定理(Theorem 1,取自 [88])验证分段 Value 函数 $C^1$ 且满足 HJI(Theorem 2,附完整证明),并识别 dispersal 型奇异面。(ii) ATDDG 先解 Game of Kind(Prop. 2,显式超方程边界),再在逃逸区用两侧 PMP + 降维状态把博弈度化归为关于 A/D 拦截点纵坐标 $y$ 的一维优化,一阶条件为四次方程 (49),最优航向为状态反馈 (48)。关键公式:

**通用验证框架**
- HJI PDE 与验证定理(p.6,式 (3),Theorem 1 引自 [88]):$-\frac{\partial V}{\partial t}=\frac{\partial V}{\partial x}\cdot f(t,x,u^*,v^*)+g(t,x,u^*,v^*)$,$V(t_f,x)=q(x)$ ⇒ $(u^*,v^*)$ 为状态反馈鞍点均衡。

**2P1EDG(Sec. IV)**
- Hamiltonian(p.6,式 (7)):$H = 1+\lambda_{x_E}\cos\varphi+\lambda_{y_E}\sin\varphi+\beta_1\lambda_{x_{P1}}\cos\psi_1+\beta_1\lambda_{y_{P1}}\sin\psi_1+\beta_2\lambda_{x_{P2}}\cos\psi_2+\beta_2\lambda_{y_{P2}}\sin\psi_2$。
- 最优航向(p.7,式 (9)–(11)):$\cos\varphi^*=\lambda_{x_E}/\sqrt{\lambda_{x_E}^2+\lambda_{y_E}^2}$(E 最大化 H);$\cos\psi_i^*=-\lambda_{x_{Pi}}/\sqrt{\lambda_{x_{Pi}}^2+\lambda_{y_{Pi}}^2}$(Pi 最小化 H)。协态恒定(p.7),轨迹为直线。
- 单独捕获时间(p.7,式 (13)/(15)):$t_{f1}=c_1\cos(\varphi^*-\lambda_1)+\sqrt{c_1^2\cos^2(\varphi^*-\lambda_1)+c_1 r_{10}}$,其中 $\lambda_1=\arctan\frac{y_{E0}-y_{P10}}{x_{E0}-x_{P10}}$,$r_{10}=\sqrt{(x_{E0}-x_{P10})^2+(y_{E0}-y_{P10})^2}$,$c_1=\frac{1}{\beta_1^2-1}r_{10}$($t_{f2}$ 同理,下标 2)。E 最优航向由 $\max_\varphi t_{f1}$ 的一阶条件给出 $\sin(\varphi-\lambda_1)=0\Rightarrow\varphi^*=\lambda_1$(p.7,式 (16)(17))。
- 情形判别(p.7,式 (18)(19)):若 $t_{f1}(\lambda_1)\le t_{f2}(\lambda_1)$ 则 $\varphi^*=\lambda_1$(P2 无法减小捕获时间);若 $t_{f2}(\lambda_2)\le t_{f1}(\lambda_2)$ 则 $\varphi^*=\lambda_2$。
- 同时捕获情形 c):E–Pi 的 Apollonius 圆(p.7–8,式 (20)):圆心距 E 为 $c_i=\frac{1}{\beta_i^2-1}r_{i0}$、半径 $\rho_i=\frac{\beta_i}{\beta_i^2-1}r_{i0}$,圆心坐标 $a_i=x_E+\rho_i\cos\lambda_i,\ b_i=y_E+\rho_i\sin\lambda_i$,$(x-a_i)^2+(y-b_i)^2=\rho_i^2$;瞄准点 $I:(x_I,y_I)$ 取两圆交点中距 E 最远者,$\varphi_s^*=\arctan\frac{y_I-y_E}{x_I-x_E}$,$\psi_{1s}^*,\psi_{2s}^*$ 同理,且 $\lambda_m\le\varphi_s^*\le\lambda_M$($\lambda_m=\min\{\lambda_1,\lambda_2\}$,p.8)。
- 分段 Value 函数(p.8,式 (22)–(24)):$V(x)=\frac{\sqrt{(x_E-x_{P1})^2+(y_E-y_{P1})^2}}{\beta_1-1}\,(x\in\mathcal{R}_1)$;$\frac{\sqrt{(x_E-x_{P2})^2+(y_E-y_{P2})^2}}{\beta_2-1}\,(x\in\mathcal{R}_2)$;$\frac{F_1(x)t_{f2}(x)-F_2(x)t_{f1}(x)}{F_1(x)-F_2(x)}\,(x\in\mathcal{R}_s)$;其中 $t_{fi}(x)=\frac{1}{\beta_i^2-1}\{[(x_E-x_{Pi})\cos\varphi^*+(y_E-y_{Pi})\sin\varphi^*]+\{[\cdot]^2+(\beta_i^2-1)[(x_E-x_{Pi})^2+(y_E-y_{Pi})^2]\}^{1/2}\}$,$F_i(x)=[(y_E-y_{Pi})\cos\varphi^*-(x_E-x_{Pi})\sin\varphi^*]\times\{\cdots\}^{-1/2}$(式 (23)(24));$F_i$ 另有形式 $F_i=\frac{\sin(\lambda_i-\varphi^*)}{\sqrt{\cos^2(\lambda_i-\varphi^*)+\beta_i^2-1}}$(p.9,式 (29))。$\mathcal{R}_s$ 中的 $V$ 是 $t_{f1},t_{f2}$ 的凸组合(p.8)。cos φ*、sin φ* 因 φ* 无显式表达而保留在 $V$ 中(p.8)。
- 状态空间划分与奇异面(p.8):$\mathcal{R}_1$/$\mathcal{R}_2$/$\mathcal{R}_s$ 分别为仅 P1、仅 P2、同时捕获;(18)/(19) 取等号处为区域边界;dispersal 面 $\mathcal{D}\subset\mathcal{R}_s$ 定义为两 Apollonius 圆交点与 E 等距的状态集(两个最优解并存),$\mathcal{R}_s^-=\mathcal{R}_s-\mathcal{D}$,正则区域 $\mathcal{R}=\mathcal{R}_1\cup\mathcal{R}_2\cup\mathcal{R}_s^-$。
- HJI 验证形式(p.10,式 (32)(33)):$0=\left[\frac{\partial V}{\partial x}f(x,u_P^*,u_E^*)+1\right]$。

**ATDDG(Sec. V)**
- Game of Kind 边界方程(p.13,式 (46)):$\alpha=\frac{\sqrt{(x_A+x_T)^2+y_T^2}-\sqrt{(x_A-x_T)^2+y_T^2}}{2x_A}$;显式区域见 Prop. 2(下节)。$x_T<0$ 时目标必逃生(p.13)。固定 $x_A>0$ 的截面为双曲线右支(p.14,式 (47)):$\frac{x_T^2}{\alpha^2 x_A^2}-\frac{y_T^2}{(1-\alpha^2)x_A^2}=1$。
- 博弈度求解思路(p.14–15):Isaacs 主方程 $\min_{\varphi,\psi}\max_\chi H=0$ ⇒ 协态恒定、直线轨迹;TPBVP 终端条件用增广 Mayer 函数 $\Phi_a$ 与乘子 $\nu_1,\nu_2$(p.14,式 (52)–(57));因 $V_A=V_D$ 且直线运动,拦截点 $I=(0,y)$ 在 AD 中垂线上,$t_f=\sqrt{x_A^2+y^2}$(p.15,式 (75));博弈化归为一维优化(p.15):case a) $x_T<0$:$\min_y\ J_1=\alpha\sqrt{x_A^2+y^2}+\sqrt{(y_T-y)^2+x_T^2}$(式 (76));case b) $x_T>0$:$\max_y\ J_2=\alpha\sqrt{x_A^2+y^2}-\sqrt{(y-y_T)^2+x_T^2}$(式 (77))。
- 最优状态反馈航向(Theorem 3,p.14,式 (48)):$\cos\varphi^*=\pm\frac{x_T}{\sqrt{x_T^2+(y_T-y)^2}},\ \sin\varphi^*=\pm\frac{y_T-y}{\sqrt{x_T^2+(y_T-y)^2}}$($x_T\ne0$;符号规则:xT<0 取正号、xT>0 取负号,p.14);$\cos\chi^*=-\frac{x_A}{\sqrt{x_A^2+y^2}},\ \sin\chi^*=\frac{y}{\sqrt{x_A^2+y^2}}$;$\cos\psi^*=+\frac{x_A}{\sqrt{x_A^2+y^2}},\ \sin\psi^*=\frac{y}{\sqrt{x_A^2+y^2}}$。
- 关键方程:四次方程(p.14,式 (49)) $(1-\alpha^2)y^4-2(1-\alpha^2)y_T y^3+[(1-\alpha^2)y_T^2+x_A^2-\alpha^2 x_T^2]y^2-2x_A^2 y_T y+x_A^2 y_T^2=0$,有两个实根 $y_1\le y_T\le y_2$;$x_T\le0$ 取 $y_1$、$x_T>0$ 取 $y_2$。$x_T=0$ 时 $\varphi^*=\phi^*+\pi/2$(p.14,式 (50)),$\tan\phi^*=\frac{\sqrt{x_A^2+(1-\alpha^2)y_T^2}}{\alpha y_T}$(p.14,式 (51);推导见 [111])。
- 终端条件推导(p.16):由 $H(t_f)\equiv0$ 与协态/控制表达式得 $\left(1-\frac{y_T}{y}\right)^2(x_A^2+y^2)=\alpha^2[x_T^2+(y_T-y)^2]$,整理即 (49);最优瞄准点 $y^*$ 是 (49) 的实根(p.16)。

## 4. 理论结果
1. **Theorem 1**(p.6,引自 [88],未在本文证明):若存在 $C^1$ 函数 $V(t,x)$ 满足 HJI PDE (3) 及 $V(t_f,x)=q(x)$,则策略对 $u^*=\mu^*(t,x)$、$v^*=\nu^*(t,x)$ 是状态反馈策略类中的鞍点均衡。前提:$V\in C^1$、满足 HJI 与终端条件。
2. **Proposition 1**(p.8,式 (21);构造性/几何推导,基于 PMP,验证由 Theorem 2 完成):对 2P1EDG (4)–(6),$ \beta_1>1,\beta_2>1$ 时,博弈的解为:$\varphi^*=\lambda_1,\psi_1^*=\lambda_1$(若 $t_{f1}(\lambda_1)\le t_{f2}(\lambda_1)$);$\varphi^*=\lambda_2,\psi_2^*=\lambda_2$(若 $t_{f2}(\lambda_2)\le t_{f1}(\lambda_2)$);否则 $\varphi^*=\varphi_s^*,\psi_1^*=\psi_{1s}^*,\psi_2^*=\psi_{2s}^*$(两 Apollonius 圆交点方案)。
3. **Theorem 2**(p.9,本文附完整证明 pp.9–11):在 Proposition 1 的解与 Value 函数 (22) 之下,$V(x)$ 在 $\mathcal{R}=\mathcal{R}_1\cup\mathcal{R}_2\cup\mathcal{R}_s^-$ 上连续、连续可微($C^1$)且对任意 $x\in\mathcal{R}$ 满足 HJI 方程。前提:2P1EDG (4)–(6)、$\beta_i>1$、排除 dispersal 面 $\mathcal{D}$。证明要点:$\mathcal{R}_s$ 内 $\frac{\partial V}{\partial\varphi^*}=0$(因 $t_f=t_{f1}=t_{f2}$)、$F_1,F_2$ 异号故 $F_1-F_2\ne0$(p.9);区域边界上梯度匹配(式 (30)(31),p.9–10);HJI 在三个区域逐一验证(式 (34)–(40),p.10–11)。
4. **Remark**(p.11):$V$ 为按 $v_E$ 归一化的捕获时间;真实捕获时间需乘 $1/v_E$(常数因子不改变本文结果)。
5. **Proposition 2**(p.13–14,引自 [111]):对给定速度比 $0<\alpha<1$,攻击者的获胜区 $\mathcal{R}_c=\{(x_A,x_T,y_T)\,|\,x_A>0,x_T>0,y_T\ge0,\ x_A^2+\frac{y_T^2}{1-\alpha^2}-\frac{x_T^2}{\alpha^2}<0\}$;T/D 队获胜区(博弈度上演出的逃逸区)$\mathcal{R}_e=\{(x_A,x_T,y_T)\,|\,x_A\ge0,x_T\ge0,y_T\ge0,\ x_A^2+\frac{y_T^2}{1-\alpha^2}-\frac{x_T^2}{\alpha^2}>0\}\cup\{(x_A,x_T,y_T)\,|\,x_A\ge0,x_T\le0\}$;边界流形 $B$ 为上式取 $=0$;固定 $x_A>0$ 的截面为双曲线右支 (47)。前提:simple motion、$V_A=V_D$、降维状态。
6. **Theorem 3**(p.14,附证明概要 pp.14–16,基于 [111]):ATDDG (41)–(45) 在逃逸区内,三方最优航向为状态反馈 (48);$y$ 为四次方程 (49) 的实根(有两个实根 $y_1\le y_T\le y_2$;$x_T\le0$ 取 $y_1$、$x_T>0$ 取 $y_2$;$x_T<0$ 时 T 航向取正号、$x_T>0$ 取负号);$x_T=0$ 时 $\varphi^*=\phi^*+\pi/2$、$\tan\phi^*=\sqrt{x_A^2+(1-\alpha^2)y_T^2}/(\alpha y_T)$。前提:$0\le\alpha<1$、降维状态 $(x_A,x_T,y_T)$、$x_A>0$、$y_T\ge0$、目标可逃逸部分状态空间。正文证明中 $x_T=0$ 情形外包给 [111](p.16)。
7. **无编号结果**:2P1EDG 的 dispersal 面存在条件(两 Apollonius 圆交点与 E 等距)与例(p.8、p.11);5P3E 指派枚举结论(p.11–12,Table I)。
统计:3 个定理(Theorem 1–3)+ 2 个命题(Proposition 1–2)+ 1 个 Remark;其中 Theorem 2 与 Theorem 3 在文内附有(完整/概要)证明,Theorem 1、Proposition 2 引自 [88]/[111]。Proposition 1 与 2 属构造性/几何论证(其严格性由 Theorem 2 与 [112] 的验证补足)。

## 5. 实验设置
**无数值仿真实验**(无 Monte Carlo、无 PN/APN 等基线对比、无统计指标);仅有三个示意性算例(illustrative examples):
1. **区域划分图**(Fig. 4,p.8):$P_1=(0,3)$、$P_2=(0,-3)$,$\beta_1=1.3$、$\beta_2=1.25$;展示 $\mathcal{R}_1,\mathcal{R}_2,\mathcal{R}_s$ 及其边界。
2. **Dispersal 面算例**(Fig. 5,p.11):$E=(5,0)$、$P_1=(0,0)$、$P_2=(24,-4)$;$v_E=1$、$v_{P1}=1.25$、$v_{P2}=1.3125$。初始时两 Apollonius 圆交点与 E 等距(状态在 $\mathcal{D}$ 上);双方选择相反解(P 追者向南、E 向北),状态离开 dispersal 面进入正则区,追者重解博弈后捕获;说明"追者猜错通常只付极小代价"(p.11)。
3. **5 追 3 逃指派算例**(p.11–12,Table I 在 p.12):$v_P=\{1.3,1.18,1.2,1.05,1.1\}$,$P=\{(3,9),(1,5),(0,0),(0.5,-3),(1.5,-7)\}$;$v_E=\{0.98,0.85,0.76\}$,$E=\{(8,5),(10,1),(7,-3)\}$;只用 2–2–1 指派,枚举所有 $P_iP_jE_l$ 组合的 2P1EDG 价值(Table I,上标标注捕获者:$P_i$/$P_j$/同时 s);最优指派 $\{P_1E_1\}$(20.01,P1 独捕)、$\{P_2P_3E_2\}$(28.46,同时捕获)、$\{P_4P_5E_3\}$(19.97,同时捕获),全部逃逸者于 28.46 时间单位被捕获,且"no other combination can reduce this value"(p.11–12)。
**评价指标**:2P1EDG 用捕获时间;ATDDG 用终端 A–T 距离(game of degree)与胜负(game of kind)(p.12)。另给出 ATDDG 几何示意图(Fig. 6,p.12,符号引自 [91],[92])与最优航向几何图(Fig. 7,p.14)。

## 6. 局限性
**作者承认的**
- ATDDG 捕获区 $\mathcal{R}_c$ 内只有候选解([113]),验证 "is a topic of current research"(p.16)。
- $\varphi^*$ 无显式表达式,"Due to the complexity of an explicit expression of $\varphi^*$, the terms $\cos\varphi^*$ and $\sin\varphi^*$ remain in $V(x)$"(p.8),Value 函数在 $\mathcal{R}_s$ 内是隐式的。
- Dispersal 面上的策略两难:实际中 E 不会宣布策略,追者猜错要付代价(尽管通常"infinitesimally small");只有双方全程同选才出现 Isaacs 所称 "perpetual dilemma"(p.11)。
- 多追多逃扩展仅是"approximate the solution"(p.11),且算例明确不考虑 3 追 1 指派(p.11)。
- 引 Isaacs 观点:不完全信息 "appears to be the most vital area for future research"(p.3)——本教程两个案例均为完全信息确定性博弈。

**我分析的(附推断依据)**
- Simple motion(常速、无转弯半径/航向率约束、全向机动)与点捕获(零捕获半径)高度理想化;文中自引的 [91],[109](defender 用 PN、attacker 用 PP、T 有航向率约束,p.12–13)与 [110](非零捕获半径,p.12)已放宽,但本教程案例均未采用——结论向真实飞行器/导弹末端场景迁移有限。
- Proposition 1(式 (21),p.8)只显式给出捕获者策略(及 E 策略);非捕获追者(如 $\mathcal{R}_1$ 中的 P2)的最优策略未给出(仅 p.7 说明其"无法减小捕获时间"),严格意义上鞍点策略对的"另一半"缺失。
- 5P3E 指派方案基于两两 2P1E 价值表的组合枚举(Table I,p.12),文中未证明该贪心/枚举指派构成 NvM 博弈的鞍点;且算例中各 Evader 相互独立、无协同,与 III-C 综述里 evader 协同文献([74],[77],[78],p.5)形成能力落差。
- ATDDG 降维状态 $(x_A,x_T,y_T)$ 依赖规范几何 $x_D=-x_A,y_A=y_D=0$(p.13),把状态反馈律 (48) 用回任意初始几何需要坐标变换,文中未给出变换式。
- 两个案例支付度量不一致(捕获时间 vs 终端 A–T 距离),两章结果无法直接拼成统一框架;ATDDG 的四次方程 (49) 求根方法与"恰有两实根"的断言在本文未证明(外包给 [111],p.14/p.16)。
- Theorem 3 的参数范围写 $0\le\alpha<1$(p.14)而 Prop. 2 写 $0<\alpha<1$(p.13),$\alpha=0$ 的退化情形未讨论。

## 7. 可复现性
**已给出**
- 全部解析公式:动力学 (4)(41)、最优航向 (9)–(11)(48)、捕获时间 (13)(15)(23)、Value 函数 (22)(24)(29)、Apollonius 圆参数 $c_i,\rho_i$ 与圆方程 (20)(p.7–8)、情形判别 (18)(19)(p.7)、四次方程 (49) 与 $x_T=0$ 情形 (50)(51)(p.14)、验证定理与完整证明(Theorem 1 p.6;Theorem 2 pp.9–11)。
- 三组算例的完整参数与结果数(Fig. 4、Fig. 5、5P3E 算例 + Table I,见第 5 节),足以逐步复算验证。
- 113 篇参考文献,含各子方向入口(Homicidal Chauffeur [9],[17]–[20];Nv1 Voronoi [62],[63];ATDDG 主线 [51],[52],[91],[92],[108]–[113])。

**缺失**
- 无开源代码链接、无算法伪代码(2P1EDG 求解流程可由 IV-B 的 (16)–(21) 与 p.8 步骤复原,但未整理成算法框图)。
- 四次方程 (49) 的求根/选根数值细节未给;$x_T=0$ 情形与"两实根"存在性证明需查 [111]。
- ATDDG 捕获区策略未给出(仅引 [113],p.16);逃逸区策略的完整验证在 [112]。
- Value 函数 (22) 在 $\mathcal{R}_s$ 内依赖两圆交点的数值求解,无复杂度/数值稳定性分析;Fig. 4–7 未附绘图数据。

## 8. 待验证
1. p.7 协态动力学一行印作 "$\dot{\lambda}_{x_{P2}}=\dot{\lambda}_{y_{P1}}=0$",最后一项疑为 $\dot{\lambda}_{y_{P2}}$ 之误(疑似原文排版/抽取问题);按"所有协态恒定"的结论(p.7)不影响结果,但引用该式时需注意。
2. p.10 的 HJI 验证写作 "$\frac{\partial V(x,t)}{\partial t}=\arg\min_{u_P}\max_{u_E}[\cdots]$",其中 "arg min" 疑为 "min" 之误(后续推导用的是值 0,非 argmin)。
3. Theorem 3 证明中多处引用 "eq. (9)、(10)、(11)"(p.15),而这些编号属于 Sec. IV(2P1EDG);ATDDG 证明似乎复用了 Sec. IV 的编号指代"以协态表示的最优控制关系"(证明中另有对应的无编号显示式)。查 [111] 可确认原出处编号。
4. "四次方程 (49) 有两个实根 $y_1\le y_T\le y_2$"为断言,本文未证;推测在 [111] 中有完整论证(综述引用时宜标 [111])。
5. 式 (76)(77) 中 case a) 取 $\min_y J_1$、case b) 取 $\max_y J_2$ 的非对称写法——其博弈论解读(T/D 队始终最大化终端距离,为何 case a) 是对 $y$ 取极小)文中未展开,推测与一维约化博弈中"哪一方实际上通过 $y$ 间接选择"有关,需对照 [111] 核实。
6. 任务背景预期本教程"梳理 PN/PP/APN 等经典制导策略的博弈论解释"——经全文核对不成立:PN/PP 仅在综述中作为 [91],[109] 的设定被提及(p.12–13),APN 全文未出现;作为综述坐标基准时应把本文定位为"按参与者数量的谱系梳理 + simple motion 两案例精讲",而非制导律博弈论解释的综述。
7. Fig. 6 中的符号($\lambda_{da},\lambda_{at},\gamma_d,\gamma_a,\gamma_t,\sigma_d,\sigma_a,\phi_a,\phi_t,R_{da},R_{at},V_d,V_a,V_t$)仅在图与图注出现(p.12),正文未定义;如需在跨论文符号表中使用,应到 [91],[92] 核对其定义。

## 9. 记号表
| 原文符号 | 含义 | 首次出现位置 |
|---|---|---|
| $x=(x_E,y_E,x_{P1},y_{P1},x_{P2},y_{P2})\in\mathbb{R}^6$ | 2P1EDG 完整状态(三方笛卡尔坐标) | p.6 |
| $u_E=\{\varphi\}$ | Evader 控制(瞬时航向角) | p.6 |
| $u_P=\{\psi_1,\psi_2\}$ | 两 Pursuer 控制(瞬时航向角) | p.6 |
| $v_E, v_{P1}, v_{P2}$ | 三方常速度 | p.6 |
| $\beta_i=v_{Pi}/v_E>1\ (i=1,2)$ | 归一化速度比(两追者不必相等) | p.6 |
| $x_0=(x_{E0},y_{E0},x_{P10},y_{P10},x_{P20},y_{P20})$ | 初始状态 | p.6 |
| $t_f,\ x_f$ | 终端时刻/终端状态 | p.6 |
| $f(x,u_P,u_E)$ | 归一化动力学(式 (4)) | p.6 |
| $J=q(x(t_f))+\int_0^{t_f}g\,\mathrm{d}t$ | 通用性能泛函(式 (2)) | p.6 |
| $V(t,x),\ V(x)$ | Value 函数 | p.6 / p.8 |
| $\lambda=(\lambda_{x_E},\lambda_{y_E},\lambda_{x_{P1}},\lambda_{y_{P1}},\lambda_{x_{P2}},\lambda_{y_{P2}})$ | 协态向量 | p.6 |
| $H$ | Hamiltonian(式 (7)) | p.6 |
| $\lambda_i=\arctan\frac{y_{E0}-y_{Pi0}}{x_{E0}-x_{Pi0}}$ | E 相对 Pi 的初始视线角 | p.7 |
| $r_{i0}=\sqrt{(x_{E0}-x_{Pi0})^2+(y_{E0}-y_{Pi0})^2}$ | E–Pi 初始距离 | p.7 |
| $r_i=\sqrt{(x_E-x_{Pi})^2+(y_E-y_{Pi})^2}$ | E–Pi 瞬时距离 | p.7 |
| $c_i=\frac{1}{\beta_i^2-1}r_{i0}$ | Apollonius 圆心到 E 的距离 | p.7($c_1,c_2$)、p.8($c_i$) |
| $\rho_i=\frac{\beta_i}{\beta_i^2-1}r_{i0}$ | Apollonius 圆半径 | p.8 |
| $a_i=x_E+\rho_i\cos\lambda_i,\ b_i=y_E+\rho_i\sin\lambda_i$ | Apollonius 圆心坐标 | p.8 |
| $I:(x_I,y_I)$ | 瞄准点(两圆交点中距 E 最远者) | p.8 |
| $\varphi_s^*,\ \psi_{1s}^*,\ \psi_{2s}^*$ | 同时捕获情形的最优航向 | p.8 |
| $\lambda_m=\min\{\lambda_1,\lambda_2\},\ \lambda_M=\max\{\lambda_1,\lambda_2\}$ | 视线角上下界 | p.8 |
| $\mathcal{R}_1,\mathcal{R}_2,\mathcal{R}_s$ | 仅 P1 捕获 / 仅 P2 捕获 / 同时捕获区域 | p.8 |
| $\mathcal{D}$ | dispersal surface(奇异面) | p.8 |
| $\mathcal{R}_s^-=\mathcal{R}_s-\mathcal{D},\ \mathcal{R}=\mathcal{R}_1\cup\mathcal{R}_2\cup\mathcal{R}_s^-$ | 正则区域 | p.8 |
| $t_{fi}(x)$ | 式 (23):当前状态下 E–Pi 单独博弈捕获时间 | p.8 |
| $F_i(x)$ | 式 (24):$\partial t_{fi}/\partial\varphi^*=F_i t_{fi}$ 相关函数 | p.8 |
| $Q_i$ | 式 (27) 下的根式项($Q_i>0$) | p.9 |
| $T,\ A,\ D$ | Target / Attacker / Defender | p.12 |
| $x_T=(x_T,y_T),\ x_A=(x_A,y_A),\ x_D=(x_D,y_D)$ | ATDDG 三方位置 | p.13 |
| $x=(x_T,y_T,x_A,y_A,x_D,y_D)\in\mathbb{R}^6$ | ATDDG 完整状态(博弈集=全空间) | p.13 |
| $\varphi,\ \chi,\ \psi$ | T / A / D 的瞬时航向(控制) | p.13 |
| $u_{T,D}=\{\varphi,\psi\},\ u_A=\{\chi\}$ | T/D 队与 A 的控制 | p.13 |
| $V_T,V_A,V_D$;归一化 $V_A=V_D=1,\ V_T=\alpha$ | 三方速度 | p.13 |
| $\alpha=V_T/V_A<1$ | 速度比(问题参数) | p.13 |
| $S=S_e\cup S_c;\ S_e,\ S_c$ | 终止集;D 拦截 A / A 捕获 T(式 (42)–(44)) | p.13 |
| $J_c=\tfrac12[(x_{Af}-x_{Tf})^2+(y_{Af}-y_{Tf})^2]$ | 博弈度支付(终端 A–T 距离,式 (45)) | p.13 |
| $(x_A,x_T,y_T)$ | 降维状态空间 | p.13 |
| $\mathcal{R}_e,\ \mathcal{R}_c,\ B$ | 逃逸区 / 捕获区 / 边界流形(game of kind) | p.13 |
| $y=y_A(t_f)=y_D(t_f)$ | A/D 同时拦截点(AD 中垂线上)纵坐标 | p.14–15 |
| $y_1,y_2$ | 四次方程 (49) 的两个实根,$y_1\le y_T\le y_2$ | p.14 |
| $\phi^*$ | $x_T=0$ 时 T 最优航向的辅助角(式 (50)(51)) | p.14 |
| $\Phi_a$ | 增广 Mayer 终端值函数 | p.14 |
| $\nu_1,\nu_2$ | 终端约束的 Lagrange 乘子 | p.14 |
| $J_1,\ J_2$ | case a)/b) 的一维代价(式 (76)(77)) | p.15 |
| $TT_f=\alpha\, AI=\alpha t_f,\ TI$ | Fig. 7 几何距离(T→Tf、T→I) | p.15 |
| $\xi$ | Fig. 7 中 T 的最优航向角 | p.15 |
| Fig.6 专用:$\lambda_{da},\lambda_{at},\gamma_d,\gamma_a,\gamma_t,\sigma_d,\sigma_a,\phi_a,\phi_t,R_{da},R_{at},V_d,V_a,V_t$ | DAT 几何(视线角/航向/距离/速度;正文未定义) | p.12 |

---
*精读基于 PDF 全文 18 页逐页提取(pymupdf);页码均为 arXiv 版 PDF 页码(与正文页码一致)。*
