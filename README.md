# 多智能体协同制导 · 微分博弈 · 强化学习 —— 系统性文献综述

17 篇论文的结构化精读、五维方法对比与 12 条研究空白,附可部署的 Neo-Brutalist 静态网站。

**在线阅读**:https://flynnmav.github.io/gc-lit-review/(GitHub Pages,由 `docs/` 目录挂载)

## 目录结构

```
├── papers/              17 篇论文 PDF(arXiv 公开版,编号 01–17)
├── literature/
│   ├── extract/         每篇 10 节结构化精读笔记(问题建模/假设/定理/局限/复现性/记号表,论断带页码)
│   ├── comparison_table.md / .csv   五维对比总表 + 20 列机读版
│   └── gaps.md          12 条研究空白(每条 ≥2 篇论文证据)+ 待验证区
├── site/                静态网站构建产物(21 页)
├── docs/                site/ 的同步副本(GitHub Pages 挂载这个目录)
└── tools/
    ├── build_site.py    网站构建脚本(整站重建)
    ├── assets_src/      CSS/JS 源文件
    ├── sync_docs.py     site/ → docs/ 同步
    └── check_*.py       完整性校验(断链/列表/泄漏)
```

## 本地查看

双击 `site/index.html`,或:

```bash
cd site && python -m http.server 8765
# 打开 http://127.0.0.1:8765
```

## 修改与更新流程

1. 改精读笔记(`literature/extract/*.md`)或对比表 CSV
2. 重建 + 同步 + 校验 + 提交推送:

```bash
python -I -X utf8 tools/build_site.py
python -I -X utf8 tools/sync_docs.py
python -I -X utf8 tools/check_site.py
git add -A && git commit -m "update: ..." && git push
```

3. GitHub Pages 约 1 分钟后自动更新。

## 综述的三条主线结论

- **假设强度与现实性成剪刀差**:博弈组(01–06)理论最硬(HJI 验证闭环鞍点)但假设最虚(全向常速+点捕获+完美信息);RL 组(13/14/17)动力学最实(6DOF/radome/半实物)但零定理。
- **同族文献内部有实锤矛盾**:03 用双侧 PMP 推翻自家 2015 年解;07 的机动目标声称被自身证明否定;13 正文与表格在燃料结论上相反……(详见红旗清单)
- **最值得做的下一步**:以 16 的 T-A-D 场景为公共测试床,让博弈最优策略、保障性制导、TD3 同协议换边对决(gaps.md G11)。
