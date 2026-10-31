# 15 | Learning to Guide: Guidance Law Based on Deep Meta-learning and Model Predictive Path Integral Control
> Liang C., Wang W., Liu Z., Lai C., Zhou B. | IEEE Access 2019 | arXiv:1904.06892

> 精读版本说明:所读 PDF 为 IEEE Access early-access 版(DOI 10.1109/ACCESS.2019.2909579,13 页,页脚印刷页码除首页外均显示"2",不可用),以下页码均指 **PDF 第 X 页**(p.1–p.13)。正式发表版为 IEEE Access vol.7, pp.47353–47365, 2019(见代码仓 README 引用)。

## 0. 一句话定位
本文把"深度神经网络动力学模型 + MPPI(采样式随机最优 MPC)"用于带终端落角约束的机动目标拦截,并用 meta-learning(借鉴 Nagabandi et al. [33] 的 online adaptation)让 NN 动力学模型在拦截过程中**在线适应**目标机动、扰动与执行器故障,另贡献了一个 MPPI 温度系数 λ 的自适应设定。与端到端 RL(直接学策略)的区别:控制问题仍由 MPPI 在线优化求解,神经网络只学**动力学预测模型**(model-based RL),训练数据需求小、代价函数可显式编码落角约束(p.1 摘要、p.2 贡献 1–3)。

## 1. 问题建模
- **状态量/观测量(原文符号)**:p.6 "Problem Formulation":状态 $x_t=[R,\theta_m,\psi_m,\theta_L,\psi_L,\dot R,\dot\theta_m,\dot\psi_m,\dot\theta_L,\dot\psi_L,\dot R,\dot\theta_m,\dot\psi_m,\ddot R,\ddot\theta_m,\ddot\psi_m,\ddot\theta_L,\ddot\psi_L]^T$,并注明"the last five are the extended state we estimate by deep neural dynamic model"(原文此行中间 $\dot R,\dot\theta_m,\dot\psi_m$ 重复出现一次,疑为排版笔误;末五项为扩展状态 $[\ddot R,\ddot\theta_m,\ddot\psi_m,\ddot\theta_L,\ddot\psi_L]^T$)。可观测量为 $[R,\theta_m,\psi_m,\theta_L,\psi_L,\dot R,\dot\theta_m,\dot\psi_m,\dot\theta_L,\dot\psi_L]^T$(p.6)。Monte Carlo 与半实物实验中带不确定性的"actual observation"为 $[R,\theta_m,\psi_m,\dot R,\dot\theta_m,\dot\psi_m]^T$(p.9、p.11)。
- **控制量(原文符号)**:拦截器加速度指令,出现在运动学方程中的 $a_{zm},\ a_{ym}$(p.5 式(18)(19)),执行器输出 $u_i$、指令 $u_{ci}$、执行器增益 $\eta_i$(p.7 式(36));图 6/图 10 纵轴为 $a_{ym}, a_{zm}$ 加速度指令。
- **动力学模型**:
  - 三维追逐-目标运动学(引用 [41]),p.5 式(15)–(21):$\dot R=V_T\cos\theta_t\cos\psi_t-V_M\cos\theta_m\cos\psi_m$;$R\dot\theta_L=V_T\sin\theta_t-V_M\sin\theta_m$;$R\dot\psi_L\cos\theta_L=V_T\cos\theta_t\sin\psi_t-V_M\cos\theta_m\sin\psi_m$;$\dot\theta_m=\frac{a_{zm}}{V_M}-\dot\psi_L\sin\theta_L\sin\psi_m-\dot\theta_L\cos\psi_m$;$\dot\psi_m=\frac{a_{ym}}{V_M\cos\theta_m}+\dot\psi_L\tan\theta_m\cos\psi_m\sin\theta_L-\dot\theta_L\tan\theta_m\sin\psi_m-\dot\psi_L\cos\theta_L$;$\dot\theta_t,\dot\psi_t$ 与之同构(把 M 换成 T、$a_{zt}/V_T$ 等)。
  - 变速拦截器速度模型(引用 [43]),p.6–7 式(29)–(35):$\dot V_M=\frac{T-D}{m}-g(\cos\psi_m\cos\theta_m\sin\theta_L+\sin\theta_m\cos\theta_L)$;$D=D_0+D_i$,$D_0=C_{D0}Qs$,$D_i=\frac{K}{m^2}(a_{ym}^2+a_{zm}^2)Qs$*(式(31) 为分式,提取有歧义,见第 8 节)*;$K=\frac{1}{\pi A_r e}$;$Q=\frac12\rho V_M^2$*(同上)*;$T=7500\ (0\le t\le T_B),\ 0\ (t>T_B)$;$m=90.035+3.31(T_B-t)\ (0\le t\le T_B),\ 90.035\ (t>T_B)$。
  - NN 动力学模型(扩展状态观测器形式),p.3 式(1):$\hat x_{t+1}=f_\theta(x_t,u_t)=[q_{t+1};\dot q_{t+1};\ddot q_{t+1}]=[q_t+\dot q_t\Delta t;\ \dot q_t+\ddot q_t\Delta t;\ f_\theta(x_t,u_t)\Delta t]$,状态分为可观测部分 $(q,\dot q)$ 与扩展状态 $\ddot q$,$\Delta t$ 为离散时间增量。
  - MPPI 系统模型,p.4 式(3)(4):$x_{t+1}=f(x_t,u_t+\delta u_t)$,$\delta u_t\sim\mathcal N(0,\Sigma)$。
- **目标机动模型**:目标速度恒定 270 m/s,横向加速度 $a_{yt}=a_{zt}=40\sin(t)$ m/s²(Case 1/2),Monte Carlo 与半实物实验为 $30\sin(t)$ m/s²(p.7 Table I;p.11)。
- **代价函数(MPPI 的 L 与 φ)**:
  - 轨迹代价通式,p.4 式(5):$S(\tau_t^n)=\phi(x_N)+\sum_{t=0}^{T-1}c_t(x_t,u_t)$($c_t$ 为 running cost,$\phi$ 为 terminal cost;Alg.1 第 9 行写作 $\phi(x_T)$,p.5;终端代价 $\phi$ 在引导问题中的具体形式全文未给出)。Alg.1 第 7 行运行代价累加形式:$S(\tau_t^n)\mathrel{+}=c_t(x_t,u_t)+\lambda u_{t-1}^T\Sigma^{-1}\delta u_{t-1}^n$(p.5)。
  - 引导问题的具体运行成本(Remark 3,p.6):参考规划 $e_0=[\theta_L-\theta_{LD},\ \psi_L-\psi_{LD}]^T$(式(23)),$e_1=\dot e_0+K_1e_0$(式(24)),$\dot e_1=-K_2e_1$(式(25));则 $e_2=\dot e_1+K_2e_1$(式(27)),$c(\cdot)=\|e_2\|^2$(式(28)),即 MPPI 作为跟踪控制器跟踪 Remark 2 生成的参考。
- **约束(输入限幅等)**:拦截器最大加速度能力 200 m/s²(p.7);执行器故障模型(p.7 式(36)):$u_i=u_{ci}(\eta_i=1,$无故障$)$,$u_i=\eta_iu_{ci}\ (0<\eta_i<1,$效力损失 loss of effectiveness$)$;故障时段 $T_\eta$(Table I 中 Case 1/2 为 $[3.0\text{s},+\infty)$)。无显式输入限幅公式;控制饱和只在讨论中定性提及(p.7)。MPPI 每步只执行控制序列首项(p.4)。
- **噪声/时延**:
  - MPPI 控制注入高斯噪声 $\delta u_t\sim\mathcal N(0,\Sigma)$(p.4 式(4)),作者称该假设合理因为控制输入实际交给低层伺服控制器执行(p.4);
  - 训练数据增广:归一化后向状态加白噪声(p.4);
  - Monte Carlo 观测不确定性:$[R,\theta_m,\psi_m,\dot R,\dot\theta_m,\dot\psi_m]^T$ 乘以 $1+0.15\sin(t)$;LOS 角测量噪声为 std 8 mrad 高斯;LOS 角速率噪声为 std 等于其当前值 1% 的高斯(p.9);
  - 半实物实验:观测幅值不确定度至 8%,LOS 高斯噪声(p.11);
  - 时延:无显式时延模型;实验中存在自动驾驶仪滞后("lag caused by missile autopilot"),通过把在线自适应学习率降至 $\alpha=0.00065$ 补偿(p.11)。

## 2. 假设条件
1. **MPPI 采样分布假设**:$\delta u_t\sim\mathcal N(0,\Sigma)$ 高斯;作者论证其合理性:"control inputs are normally given to a lower level servomotor controller to execute in actual system"(p.4,式(4) 下方)。
2. **传统 MPPI 的假设(被本文放松的对象)**:"the traditional MPPI framework assumes the actual environment similar to the training dataset for the deep neural network"(p.1 摘要;p.2 II.D 再述)。
3. **元学习任务分布构造**:元训练数据从系统采样——随机初始状态 + 每时间步零均值随机指令;每条轨迹记录到终端条件(命中目标)或预设最大时间戳(p.3)。**关键:训练集生成时导弹速度恒 800 m/s、目标 270 m/s 且"no maneuvers"(p.6)——即元训练任务集不含目标机动与执行器故障**,测试时才引入 $\sin(t)$ 机动与 $\eta=0.5/0.6$ 的故障;在线适应阶段假设"at every time step, the task is slight different as the changing environment the controller facing"(p.3)——把连续变化环境视为每步一个略有差异的任务。故**训练任务集 ≠ 测试机动集合**,适应能力完全依赖在线梯度更新。
4. **数据预处理假设**:扩展状态真值 $q̈_{t+1}$ 可由观测 $\dot q$ 数值差分获得(p.3);归一化为零均值、降方差(部分状态只降方差不归一到 1,理由是高方差原始数据低值段难训练,p.4)。
5. **实时性假设**:选择全连接网络(而非 LSTM)是因"costs less time to execute in practice",且制导问题采样难、数据少时小网更优(p.3);仿真采样/控制周期 5 ms(p.7)。**全文无单步计算耗时实测**,实时性仅为设计论证(见第 6 节)。
6. **目标机动**:目标为机动目标($40\sin(t)$ 等),非静止;终端约束为 LOS 角 $\theta_L\to\theta_{LD},\ \psi_L\to\psi_{LD}$ 且 $\dot\theta_L=\dot\psi_L=0$(p.2、p.6 式(22))。
7. **实验假设**:半实物实验中导弹为轴对称、气动系数取自 [45],假设 roll-stabilized 于恒定滚转姿态(p.10);相对运动信息由 CCD 视觉子系统生成(p.10)。
8. **温度系数固定的缺陷论证**:固定 λ 会因状态不同区域数据方差不同而改变输出控制序列性能,因此 λ 应随代价标准差自适应(p.4–5 Remark 1 及式(13) 前后论述;属论证而非定理)。

## 3. 方法核心
机制概括:元学习框架分两阶段(p.3)。**元训练阶段**:用约 30 分钟系统辨识数据(p.6)训练全连接 NN(2 隐层×200 神经元,ReLU,p.6)预测状态导数(扩展状态观测器,式(1)),损失用 MAE(而非 MSE,理由是保持高方差数据的同尺度,p.3–4),Adam 优化器 [39](p.4)。**在线自适应控制阶段**:每个控制步先用最近 $M$ 步经验 $\tau_\varepsilon(t-M,t-1)$ 按式(2) 的梯度上升规则把 $\theta^*$ 一步更新为 $\theta^{*'}$,再用更新后的模型跑 MPPI:采样 N 条噪声控制序列、按自适应温度 λ 计算重要性权值、加权平均得控制序列、只执行首项(p.4–5,Alg.1)。与 [33](fixed temperature)的差异有二:更新规则用 MAE 代替 MSE(p.4);MPPI 温度系数自适应 $\lambda=\lambda^*\sigma(S(V))$(式(13),p.5)——可解释为先把代价标准化为 std 1,保证重要性采样权值分布性质在状态各处一致(p.5)。

关键公式(均已核对原文页码):
- NN 动力学模型(扩展状态观测器):式(1),p.3。
- 在线自适应更新规则:式(2),p.4:$\Psi_\tau(\tau(t-M,t-1),\theta)=\theta+\alpha\nabla_\theta\Big(\frac1M\sum_{m=t-M}^{t-1}\big|(\dot q_{m+1}-\dot q_m)-\hat f_\theta(x_m,u_m)\big|\Big)$,$\alpha$ 预先固定。
- MPPI 基础框架(来自 [25]):系统 式(3)(4)、轨迹代价 式(5)(p.4);自由能 式(6) $\Xi(V)=-\lambda\log\big(\mathbb E_{\mathbb P}[\exp(-\frac1\lambda S(V))]\big)$;最优分布 式(7) $p^*(V)=\frac1\eta\exp(-\frac1\lambda S(V))h(V)$;KL 最小化 式(8);最优控制 式(9)(10);重要性权值 式(11)(12)(p.4)。
- 自适应温度(本文贡献,Remark 1 之后):式(13),p.5:$\lambda=\lambda^*\sigma\big(S(V)\big)$,$\sigma$ 为标准差函数,$\lambda^*$ 预设(仿真取 1,p.7)。
- 控制序列迭代更新:式(14),p.5:$u_t^{i+1}=u_t^i+\sum_{n=1}^N w_t^n\delta u_t^n$。
- **Alg.1(p.5)**"Online Adaptive control with MPPI at each time stamp":输入 $\hat f_\theta$、更新规则 $\Psi_\tau$、经验 $\tau(t-M,t-1)$、$N$(样本数)、$T$(horizon)、$\Sigma, r_t, \phi$(控制超参;原文如此,$r_t$ 未在正文定义,疑对应 $c_t$);流程:①$\theta^{*'}\leftarrow\Psi_\tau(\tau(t-M,t-1),\theta^*)$;②采 $N$ 条 $\delta u$ 序列前向传播累加 $S$(含 $\lambda u^T\Sigma^{-1}\delta u$ 项)与终端项 $\phi(x_T)$;③$S'=S-\min_n S$;④$\lambda=\sigma(S')$;⑤softmax 权值;⑥$u_t\mathrel{+}=\sum_n w_t^n\delta u_t^n$;⑦执行 $u_0$、时移序列并初始化尾项。
- 落角约束转代价:式(22)($\dot\theta_L=\dot\psi_L=0,\theta_L=\theta_{LD},\psi_L=\psi_{LD}$,p.6);Remark 2 参考规划 式(23)–(25) 与 Lyapunov 论证 式(26)(p.6);Remark 3 代价 式(27)(28)(p.6)。

**每步计算量**:每控制周期需 N=1000 条轨迹 × T=3 步 NN 前向 + 一次 M 步窗口上的梯度更新,周期 5 ms(p.7);论文未报告实测耗时与硬件。

## 4. 理论结果
**无定理/引理/命题/正式证明**(全文 grep 验证:Theorem/Lemma/Proposition/Proof 均为 0 次命中;"theorem" 唯一出现是提及 Feynman-Kac 定理的背景介绍,p.2)。理论性内容仅有:
- 自由能给出最优控制代价下界,引用 [40](p.4),非本文证明。
- Remark 1–3(p.4–6):其中 Remark 2 含一个非正式 Lyapunov 论证:取 $V=\frac12e_1^2$,则 $\dot V=e_1\dot e_1=-K_2e_1^2\le0$(式(26),p.6),据此说明规划参考下 $e_1$ 为稳定子空间、误差变量收敛到零、式(22) 的控制要求满足。该论证只针对**参考规划器**(滑动面式参考动态)本身,不涉及 MPPI 跟踪误差与元学习在线适应的收敛性/稳定性。
- 采样式 MPC + 学习的典型情况:无任何关于闭环拦截成功率或适应后模型误差的定理。

## 5. 实验设置
- **数值仿真(p.6–8)**:两个场景 Case 1/2 + Monte Carlo。初始参数 Table I(p.7):$R(0)=4000$ m(Case1/2)、3800 m(MC);$\theta_L(0)=-0.7$(Case1/2)、$\mathrm{Unif}(-0.9,-0.7)$(MC 表中印作 $\mathrm{Unif}(-0.7,-0.9)$);$V_M(0)=800$ m/s;$V_T=270$ m/s;$\theta_{LD}/\psi_{LD}=-0.6/0.8$(Case1/2)、$-0.8/0.6$(MC);$a_{yt}=a_{zt}=40\sin(t)$(Case)/$30\sin(t)$(MC);$T_B=3.5/3.0/4.0$ s;$\eta=0.5/0.5/0.6$;$T_\eta=[3.0\text{s},+\infty)/[3.0\text{s},+\infty)/[3.5\text{s},+\infty)$。采样/控制周期 5 ms;MPPI horizon 3、1000 条轨迹;$\lambda^*=1$;$K_1,K_2$ "set to [0.6, 0.5] and [3.0, 2.0] respectively"(p.7,归属歧义见第 8 节);在线自适应学习率 $\alpha=0.001$。NN:2×200 ReLU。
- **对比基线**:①standard MPPI [25] 但带本文自适应温度;②standard meta-learning MPPI [33] 固定温度(为公平比较取 0.001 与 0.0001,分别对应 Case 1 与 Case 2,声称近似覆盖自适应温度的上下限,p.7)。**无 PN/APN 或其他制导律基线**。
- **评价指标(Table II,p.7)**:Miss Distance(m)、终端 LOS 角 $\theta_{LT},\psi_{LT}$(rad)、Impact Time(s)。结果:Proposed Case1/2:miss $1.82\times10^{-5}/1.77\times10^{-5}$ m,$\theta_{LT}=-0.6010/-0.6007$,$\psi_{LT}=0.8039/0.8027$,8.71/7.53 s;Standard Meta-learning MPPI:$9.67\times10^{-5}/8.77\times10^{-5}$ m 等;Standard MPPI:0.1007/0.2933 m,落角严重偏离(0.1417/2.5044 等)。**无计算时间指标**。
- **Monte Carlo(p.9)**:3500 次交战(proposed 方法),初始 LOS 角与弹道偏角均匀分布(Table I MC 列),目标航向固定("to make the result figures clearer");观测不确定性 $1+0.15\sin(t)$、LOS 8 mrad、角速率 1% 噪声;$\eta=0.6$(40% 效力损失);结果以轨迹图(Fig.12)、终端 LOS 角与脱靶量直方图(Fig.13)呈现,无统计表。
- **半实物实验(p.10–11)**:skid-to-turn 导弹三轴转台半物理仿真,动态面控制器作自动驾驶仪,CCD 视觉导引子系统,千兆以太网互联,VR 子系统渲染(p.10,Fig.15);100 次交战;$\theta_{LD}=-0.8$ rad,$\psi_{LD}=0.6$ rad;初始 LOS 角 $\mathrm{Unif}$ 同 MC;$\eta=0.6$;目标 $30\sin(t)$ m/s² 双向;$K_1,K_2$ "set to [0.9, 0.65] and [8.0, 8.0] respectively";$\alpha=0.00065$(补偿自动驾驶仪滞后);观测不确定度至 8%;结果 Fig.16/17(轨迹、脱靶量与终端 LOS 角),自动驾驶仪滞后使性能比纯仿真变差但仍保持正的落角跟踪与拦截精度(p.11)。

## 6. 局限性
- **作者承认的**:
  - 传统 MPPI 假设实际环境与训练数据一致,面对不同目标机动、扰动与执行器故障不成立——本文动机(p.1 摘要;p.2)。
  - 模型误差累积是 model-based RL 的挑战之一;以 MPC 短预测时域缓解,并用 Fig.3 的单步/多步预测误差说明预测性能"相对较小"(p.6,定性图,无统计量)。
  - 自动驾驶仪滞后使在线适应与控制性能退化,拦截性能比纯仿真差(p.11)。
- **我分析的(附推断依据)**:
  - **无实时性证据**:声称全连接网比 LSTM 省时、5 ms 控制周期(p.3、p.7),但全文无 runtime/CPU/GPU/计算时间数据(grep 验证 0 命中);"首个高性能约束制导律"(p.2 贡献 3)的性能主张不含计算可行性验证。
  - **元训练任务分布与测试失配的边界未探明**:训练数据无目标机动、无执行器故障(p.6),适应完全靠式(2) 的 $M$ 步梯度更新;测试机动均为同族 $\sin(t)$ 形式(Table I、p.11),未测试机动频率/幅值变化、故障突变(硬-over、lock-in-place 仅在 p.7 列举但未实验)等更快变化。
  - **终端代价 $\phi$ 缺失**:Alg.1 含 $\phi(x_T)$ 项(p.5),但引导问题只给出运行代价式(28)(p.6),$\phi$ 具体形式与是否取零未说明,影响复现。
  - **脱靶量口径可疑**:Table II miss distance 达 $10^{-5}$ m 量级(p.7),更像数值积分中"同点相遇"的几何判定,不代表真实导引头/执行机构下的脱靶量;半实物实验只给图 17 无脱靶量统计表。
  - **基线设置偏弱**:两个基线都是自家框架变体(同一 NN、同一代价),无 PN/APN、无其他影响角约束制导律、无非学习 MPC-制导律对比;"better than standard MPPI"的结论主要由温度/适应差异贡献,无法评估整个 learning 框架的必要性。
  - **对照温度跨度极大**:基线固定温度 0.001 与 0.0001 相差一个量级、与 $\lambda^*=1$ 相差三个量级(p.7),"覆盖自适应温度上下限"的说法未给数据支撑。
  - **观测不确定性模型简单**:以乘性 $1+0.15\sin(t)$ 注入 6 个观测量(p.9)是确定性周期摄动,与真实导引头随机误差结构不同;且观测不确定性只加在 6 个量上,而可观测量列了 10 个(p.6 vs p.9),LOS 角本身的获取误差另用 8 mrad 噪声补充,两处口径不一致。
  - **超参数不完整**:$M$(经验窗口)、$\Sigma$(采样协方差)、训练超参(Adam 学习率、batch、epoch)均未给出,复现需猜测。

## 7. 可复现性
- **已给出**:
  - 代码链接:**见下**,仓库真实存在且为官方代码。
  - Alg.1 完整伪代码(p.5);NN 结构(2 隐层×200,ReLU,p.6);损失(MAE)与优化器(Adam)(p.3–4);在线学习率 $\alpha=0.001$(仿真)/0.00065(实验)(p.7、p.11);$\lambda^*=1$、基线温度 0.001/0.0001(p.7);N=1000、T=3、5 ms(p.7);$K_1,K_2$ 数值(有歧义);训练数据量 30 分钟及其采集方式(随机指令、800/270 m/s、无机动,p.6);Table I 全部初值;执行器故障模型式(36)(p.7);速度模型式(29)–(35) 及"参数值见 [43]"(p.6–7)。
- **缺失**:$M$ 的数值;$\Sigma$ 的数值;$\phi$ 终端代价形式;训练超参(Adam lr、batch size、迭代轮数)与训练代码;随机指令的具体分布;$K_1,K_2$ 数值归属歧义([0.6,0.5]/[3.0,2.0] 是按 Case 还是按 LOS 双通道各自取值,p.7、p.11 同样表述);Fig.3 预测误差的量化统计。
- **代码链接在原文哪里出现**:**不在本 PDF 任何页**。核验过程:全文 13 页文本 grep "github" 0 次、PDF 无任何内嵌 URI 链接注释;"tccliangchen" 在全文仅出现一次,为通讯作者邮箱 tccliangchen@hotmail.com(p.1)。该链接出现在 **arXiv:1904.06892 摘要页的 Comments 字段**("Code available at [this https URL]",并注明 published in IEEE Access 2019;arXiv 仅有 v1,2019-04-15 提交)。
- **代码仓内容核验**(github.com/tccliangchen/deep_meta-learning_guidance_law,已访问):TensorFlow 实现,MIT 许可,14 commits,12 stars;文件与论文组件一一对应——`mppi_run.py`(仿真主程序)、`mppi_controller.py`(MPPI 控制器)、`neural_dynamics_dense.py`("The neural network dynamic model with meta-learning online adaption built in")、`cost_functions.py`(MPPI 代价)、`missile_env.py`(制导环境)、`monte_carlo_simu.sh`+`get_Monte.m`(Monte Carlo 运行与 MATLAB 结果收集)、`inner_loop.py`(来自半实物仿真的内回路,"not included in this code set")、`model/`(预训练网络)。**注意**:README 明确 demo 只用预训练网络,**训练代码与数据集"will be posted afterwards if anybody asks"**——即元训练阶段不可直接复现。论文发表版(vol.7, pp.47353–47365)与仓库的对应关系由 README 引用信息确认;参数级一致性需运行代码核对(本次未验证)。

## 8. 待验证
- $K_1,K_2$ 数值归属:p.7 "set to [0.6, 0.5] and [3.0, 2.0] respectively" 与 p.11 "set to [0.9, 0.65] and [8.0, 8.0] respectively"——是"Case1 用 [0.6,0.5]、Case2 用 [3.0,2.0]"还是"$K_1$ 取每通道两值 [0.6,0.5]、$K_2$ 取 [3.0,2.0]"($e_0,e_1$ 为二维向量,$K_1,K_2$ 未必是标量),原文无法判定。
- 式(29) 重力项的精确形式(文本提取歧义):$\dot V_M=\frac{T-D}{m}-g(\cos\psi_m\cos\theta_m\sin\theta_L+\sin\theta_m\cos\theta_L)$ 是否与 [43] 原式一致。
- 式(31) 与式(33) 的分式结构:$D_i$ 疑为 $\frac{K}{m^2}(a_{ym}^2+a_{zm}^2)Qs$ 或 $K m^2(a_{ym}^2+a_{zm}^2)/(Qs)$(提取字形无法分辨分子分母);$Q$ 的提取显示 $V_M^2$ 重复("ρV_M²V_M²"),疑为提取伪影,标准动压应为 $\frac12\rho V_M^2$。
- 式(5) 终端代价自变量是 $x_N$ 还是 $x_T$(提取字符模糊;Alg.1 中明确为 $\phi(x_T)$)。
- Alg.1 第 12 行 $\lambda=\sigma(S'(\tau_t^n))$ 与式(13) $\lambda=\lambda^*\sigma(S(V))$ 的关系:Alg.1 中似乎直接取标准差(隐含 $\lambda^*=1$?与 p.7 "$\lambda^*$ is set to 1" 一致),实现与公式的一致性需跑代码确认。
- Table II 脱靶量 $10^{-5}$ m 的统计口径(是否含终端制导律切换/数值插值),及标准 MPPI 落角偏差 ~2.5 rad 的物理含义。
- 元训练阶段"每时间步任务略有不同"(p.3)如何落实为训练 batch/任务划分(直接沿用 [33] 的哪套划分),原文未说明。
- 元学习超参 $M$、$\Sigma$ 的实际取值(需查代码)。

## 9. 记号表
| 原文符号 | 含义 | 首次出现位置 |
|---|---|---|
| $f_\theta(x_t,u_t)$ | 神经网络动力学模型,θ 为网络权重 | p.3,III.A,式(1) |
| $\hat x_{t+1}$ | NN 预测的下一时刻状态 | p.3,式(1) |
| $q,\dot q$ | 可观测状态;$\ddot q$ 扩展状态 | p.3,式(1) 下方 |
| $\Delta t$ | 离散时间增量 | p.3,式(1) |
| $\theta^*/\theta^{*'}$ | 元训练后参数 / 在线自适应后参数 | p.4,III.B.2 |
| $\Psi_\tau$ | 参数更新规则(梯度上升,MAE) | p.4,式(2);Alg.1 |
| $\tau_\varepsilon(t-M,t-1)$ | 最近 M 步经验窗口 | p.4,III.B.2 |
| $\alpha$ | 在线自适应学习率(预先固定) | p.4,式(2) 下方 |
| $\delta u_t\sim\mathcal N(0,\Sigma)$ | MPPI 控制注入的高斯噪声及协方差 | p.4,式(3)(4) |
| $S(\tau_t^n)$ | 噪声序列对应的轨迹代价 | p.4,式(5) |
| $\phi$ / $c_t$ | 终端代价 / 运行代价 | p.4,式(5) 下方 |
| $V$(大写)、$h(V)$、$U$、$p^*$ | 输入序列;无控系统输入分布;开环序列;最优分布 | p.4,式(6)(7) 前 |
| $\Xi(V)$ | 系统自由能 | p.4,式(6) |
| $\lambda$ / $\lambda^*$ | MPPI 温度系数(softmax) / 预设温度系数 | p.4 Remark 1;p.5 式(13) |
| $\eta$ | 式(7) 归一化因子(与执行器增益 $\eta_i$ 重名) | p.4,式(7);p.7 式(36) |
| $w(V)$ | 重要性采样权值 | p.4,式(10)–(12) |
| $N$ | MPPI 采样轨迹数(取 1000) | p.5 Alg.1;p.7 |
| $T$ | MPPI 预测时域(取 3;与推力 $T$ 重名) | p.5 Alg.1;p.6 式(29) |
| $O_IX_IY_IZ_I/O_MX_MY_MZ_M/O_TX_TY_TZ_T$ | 惯性/拦截器/目标坐标系 | p.5,IV.A,Fig.2 |
| $V_M,V_T$ | 拦截器/目标速度 | p.5,IV.A |
| $\theta_m,\psi_m;\ \theta_t,\psi_t$ | 拦截器/目标速度方向角 | p.5,IV.A |
| $\theta_L,\psi_L;\ \dot\theta_L,\dot\psi_L$ | LOS 角及角速率 | p.5,IV.A |
| $R$ | 弹目相对距离 | p.5,式(15) |
| $a_{zm},a_{ym};\ a_{zt},a_{yt}$ | 拦截器/目标加速度分量(控制量) | p.5,式(18)–(21) |
| $T,D,D_0,D_i$ | 推力、阻力、零升阻力、诱导阻力 | p.6,式(29)–(31) |
| $C_{D0},m,K,A_r,e,\rho,s,Q$ | 零升阻力系数、质量、诱导阻力系数、展弦比、效率因子、大气密度、参考面积、动压 | p.6–7,式(30)–(33) 下方 |
| $T_B$ | 拦截器推力存在时间 | p.6,式(34) |
| $u_{ci},u_i,\eta_i$ | 第 i 个控制器指令、执行器输出、执行器增益 | p.7,式(36) |
| $T_\eta$ | 执行器故障存在时间段 | p.7,Table I |
| $\theta_{LD},\psi_{LD}$ | 期望终端 LOS 角(落角约束) | p.6,式(22) |
| $e_0,e_1,e_2$ | 误差变量(约束-参考-代价) | p.6,式(23)(24)(27) |
| $K_1,K_2$ | 参考规划增益(>0) | p.6,Remark 2,式(24)(25) |
| $x_t$ | 18 维状态向量(末 5 项扩展状态) | p.6,IV.B |
| MAE/MSE | 平均绝对/平方误差(模型训练与在线更新用 MAE) | p.3–4 |
