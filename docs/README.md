# 部署说明

纯静态站点(无构建、无外部 CDN、无 Cookie),整目录拷走即可用。

## 本地预览
- 直接双击 index.html,或
- `python -m http.server 8000` 后访问 http://127.0.0.1:8000

## 托管
- GitHub Pages:push 本目录到仓库,Settings → Pages → 选择分支根目录。
- Netlify / Vercel:拖拽本目录到 Deploy 即可。
- 任意 Nginx/Apache:root 指向本目录。

## 目录
- index.html 首页;papers.html 论文卡片墙;paper/NN.html 各篇精读
- comparison.html 五维对比 + 可排序机读表 + 记号对应;gaps.html 研究空白 G1–G12
- pdfs/ 17 篇原文;assets/ 样式与脚本
- 重建:在工作区根目录执行 `python -I -X utf8 tools/build_site.py`
