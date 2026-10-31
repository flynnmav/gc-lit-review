# -*- coding: utf-8 -*-
"""
Build a zero-dependency static site from the literature review workspace.

Inputs : papers/*.pdf, literature/extract/*.md, literature/comparison_table.{md,csv}, literature/gaps.md
Outputs: site/  (index.html, papers.html, paper/NN.html, comparison.html, gaps.html,
                 assets/style.css, assets/app.js, pdfs/*.pdf, README.md)

Run:  python -I -X utf8 tools/build_site.py
"""
import csv, glob, hashlib, html, json, os, re, shutil

WS  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = lambda *p: os.path.join(WS, *p)
OUT = SRC('site')

# ----------------------------------------------------------------------------- metadata
PAPERS = [
 dict(id='01', group='A', title='An Introduction to Pursuit-Evasion Differential Games',
      authors='I. Weintraub, M. Pachter, E. Garcia', year='2020',
      venue='ACC 2020 (tutorial)', arxiv='2003.05013'),
 dict(id='02', group='A', title='Active Target Defense Differential Game with a Fast Defender',
      authors='E. Garcia, D. W. Casbeer, M. Pachter', year='2015',
      venue='ACC 2015', arxiv='1502.02747'),
 dict(id='03', group='A', title='The Complete Differential Game of Active Target Defense',
      authors='E. Garcia, D. W. Casbeer, M. Pachter', year='2020',
      venue='JGCD 2020 (arXiv 预印本)', arxiv='2002.04054'),
 dict(id='04', group='A', title='Multiple Pursuer Multiple Evader Differential Games',
      authors='E. Garcia, D. W. Casbeer, A. Von Moll, M. Pachter', year='2019',
      venue='arXiv 长文 (29 页)', arxiv='1911.03806'),
 dict(id='05', group='A', title='Optimal Strategies for Guarding a Compact and Convex Target Set: A Differential Game Approach',
      authors='Y. Lee, E. Bakolas', year='2021',
      venue='arXiv', arxiv='2104.00717'),
 dict(id='06', group='A', title='Cooperative Nonlinear Guidance Strategies for Guaranteed Pursuit-Evasion',
      authors='S. Kumar, S. R. Kumar, A. Sinha', year='2024',
      venue='arXiv v3', arxiv='2402.06176'),
 dict(id='07', group='B', title='Fixed-time Cooperative Guidance Law for Multiple Missiles in Simultaneous Attacks',
      authors='H. Yu, K. Dai, H. Li, Y. Zou, S. Ma, H. Zhang (NUDT)', year='2021',
      venue='arXiv(疑未定稿)', arxiv='2106.02772'),
 dict(id='08', group='B', title='Time-Optimal Collaborative Guidance Using the Generalized Hopf Formula',
      authors='M. R. Kirchner, R. Mar, G. Hewer, J. Darbon, S. Osher, Y. T. Chow', year='2018',
      venue='IEEE L-CSS 2018', arxiv='1709.06590'),
 dict(id='09', group='B', title='Cooperative Salvo Guidance over Leader-Follower Network with Free-Will Arbitrary Time Convergence',
      authors='R. S. Pal, S. R. Kumar, D. Mukherjee', year='2024',
      venue='arXiv', arxiv='2407.15324'),
 dict(id='10', group='B', title='Nonlinear Cooperative Salvo Guidance with Seeker-Limited Interceptors',
      authors='L. Gopikannan, S. R. Kumar, A. Sinha', year='2025',
      venue='arXiv', arxiv='2509.15136'),
 dict(id='11', group='B', title='Trajectory Encryption Cooperative Salvo Guidance',
      authors='L. Gopikannan, S. R. Kumar, A. Sinha', year='2025',
      venue='arXiv v2', arxiv='2509.17341'),
 dict(id='12', group='B', title='Cooperative Guidance of Multiple Missiles: a Hybrid Co-evolutionary Approach',
      authors='X. Lan, J. Chen, Z. Zhao, T. Zou', year='2022',
      venue='IEEE TCST 录用稿(页眉)', arxiv='2208.07156'),
 dict(id='13', group='C', title='Reinforcement Learning for Angle-Only Intercept Guidance of Maneuvering Targets',
      authors='B. Gaudet, R. Furfaro, R. Linares', year='2020',
      venue='AIAA Scitech 2020', arxiv='1906.02113'),
 dict(id='14', group='C', title='Integrated and Adaptive Guidance and Control for Endoatmospheric Missiles via Reinforcement Meta-Learning',
      authors='B. Gaudet, R. Furfaro', year='2023',
      venue='AIAA Scitech 2023 预印本', arxiv='2109.03880'),
 dict(id='15', group='C', title='Learning to Guide: Guidance Law Based on Deep Meta-learning and Model Predictive Path Integral Control',
      authors='C. Liang, W. Wang, Z. Liu, C. Lai, B. Zhou', year='2019',
      venue='IEEE Access 2019(有代码仓)', arxiv='1904.06892'),
 dict(id='16', group='C', title='Cooperative Guidance Strategy for Active Defense Spacecraft with Imperfect Information via Deep Reinforcement Learning',
      authors='Z. Li, H. Liang, J. Wu, J. Wang, Y. Zheng', year='2021',
      venue='arXiv(含占位符)', arxiv='2212.03093'),
 dict(id='17', group='C', title='Learning-Based Multi-Stage Strategy for a Fixed-Wing Aircraft to Evade a Missile Detected at a Short Distance',
      authors='Z. Niu, X. Zhou, H. Xiong', year='2025',
      venue='arXiv(版权行指向 IEEE TAES)', arxiv='2511.05828'),
]
GROUPS = {
    'A': ('微分博弈与目标防御', 'T-A-D 三方博弈、多追多逃、区域守卫:Apollonius 几何、屏障面、HJI/PMP 闭环鞍点'),
    'B': ('多弹协同制导',     '同时到达/齐射:一致性、固定时间与预设时间共识、 leader-follower、感知异构'),
    'C': ('强化学习制导',     'RL/MPC 制导:角度-only 拦截、6DOF 一体化 G&C、元学习 MPPI、不完美信息防御、逃逸'),
}

# ----------------------------------------------------------------------------- markdown → html
def esc(t): return html.escape(t, quote=False)

def inline(t):
    """Inline markdown on ALREADY-ESCAPED text."""
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\$\$([^$]+)\$\$', r'<span class="math">\1</span>', t)
    t = re.sub(r'\$([^$\n]+)\$', r'<span class="math">\1</span>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    # 注:不实现单星斜体——笔记中的单个 * 全部是数学最优性标记(x*、T*、uE*),
    # 若按斜体配对会把 x*−xP)/∥x*− 这类片段错误斜体化(实测 7 页 31 处污染)。
    def link(m):
        label, target = m.group(1), m.group(2)
        if re.match(r'^https?://', target):
            return f'<a href="{target}" target="_blank" rel="noopener">{label}</a>'
        if target.startswith(('#', './', '/')):
            return f'<a href="{target}">{label}</a>'
        return f'{label}({target})'          # 伪链接(如 [30](03 所引))按纯文本还原
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, t)
    return t

def split_table_row(line):
    line = line.strip().strip('|')
    return [c.strip() for c in line.split('|')]

def md_to_html(md, anchor_prefix='sec'):
    """Line-based GFM subset: h1-h4, tables, blockquote, ul/ol (2 levels), hr, paragraphs, $$..$$."""
    lines = md.replace('\r\n', '\n').split('\n')
    out, i, sec = [], 0, 0
    def flush_table(j):
        rows = []
        while j < len(lines) and lines[j].lstrip().startswith('|'):
            rows.append(split_table_row(lines[j])); j += 1
        if len(rows) >= 2 and re.match(r'^\s*\|?[\s:|-]+\|?\s*$', lines[rows and j-len(rows)+1] or ''):
            pass
        # locate separator (2nd row) to decide header
        head, body = rows[0], rows[2:] if len(rows) > 2 and set(''.join(rows[1])) <= set('-:| ') else rows[1:]
        h = ['<div class="tblwrap"><table class="tbl"><thead><tr>']
        h += [f'<th>{inline(esc(c))}</th>' for c in head]
        h.append('</tr></thead><tbody>')
        for r in body:
            h.append('<tr>' + ''.join(f'<td>{inline(esc(c))}</td>' for c in r) + '</tr>')
        h.append('</tbody></table></div>')
        return '\n'.join(h), j
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1; continue
        if s.startswith('```'):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('```'):
                j += 1
            out.append(f'<pre class="codeblock">{esc("\n".join(lines[i+1:j]))}</pre>')
            i = j + 1; continue
        m = re.match(r'^(#{1,4})\s+(.*)$', s)
        if m:
            lvl, txt = len(m.group(1)), m.group(2).strip()
            if lvl <= 2:
                hid = f'{anchor_prefix}-{sec}'; sec += 1
                out.append(f'<h{lvl} id="{hid}">{inline(esc(txt))}</h{lvl}>')
            else:
                out.append(f'<h{lvl}>{inline(esc(txt))}</h{lvl}>')
            i += 1; continue
        if s == '---':
            out.append('<hr>'); i += 1; continue
        if s.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip().lstrip('>').strip()); i += 1
            out.append('<blockquote>' + inline(esc(' '.join(b for b in buf if b))) + '</blockquote>')
            continue
        if s.startswith('|'):
            tbl, i = flush_table(i)
            out.append(tbl); continue
        m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', ln)
        if m:
            # 收集列表块:标记行 + 缩进续行(并入上一项);列表内空行向后看一行再决定是否继续
            items = []  # [level, ordered, [segments]]
            while i < len(lines):
                ln2 = lines[i]
                if not ln2.strip():
                    nxt = i + 1
                    if nxt < len(lines) and items and (
                        re.match(r'^\s*([-*]|\d+\.)\s+', lines[nxt])
                        or (lines[nxt][:1] in (' ', '\t') and lines[nxt].strip())
                    ):
                        i += 1
                        continue
                    break
                mm = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', ln2)
                if mm:
                    indent = len(mm.group(1).replace('\t', '  '))
                    items.append([indent // 2, mm.group(2)[0].isdigit(), [mm.group(3)]])
                    i += 1
                elif ln2[:1] in (' ', '\t') and items:
                    items[-1][2].append(ln2.strip())
                    i += 1
                else:
                    break
            def render_list(group, level):
                typ = 'ol' if group[0][1] else 'ul'
                parts = [f'<{typ}>']
                k = 0
                while k < len(group):
                    lvl, _, segs = group[k]
                    if lvl < level:
                        break
                    if lvl > level:
                        k += 1  # 防御:无父项的深层项,跳过避免死循环
                        continue
                    text = inline(esc(' '.join(segs)))
                    k += 1
                    kids = []
                    while k < len(group) and group[k][0] > level:
                        kids.append(group[k]); k += 1
                    if kids:
                        parts.append(f'<li>{text}{render_list(kids, level + 1)}</li>')
                    else:
                        parts.append(f'<li>{text}</li>')
                parts.append(f'</{typ}>')
                return ''.join(parts)
            out.append(render_list(items, 0))
            continue
        # paragraph (merge consecutive plain lines; handle $$..$$ blocks)
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,4}\s|>|\||---\s*$|\s*[-*]\s|\s*\d+\.\s)', lines[i]):
            buf.append(lines[i].strip()); i += 1
        text = ''.join(buf)
        if '$$' in text:
            inner = re.sub(r'\$\$', '', text)
            out.append(f'<div class="mathblock">{inline(esc(inner))}</div>')
        else:
            out.append(f'<p>{inline(esc(text))}</p>')
    return '\n'.join(out), sec

def h2_toc(md, anchor_prefix='sec'):
    toc = []
    for n, line in enumerate(md.replace('\r\n', '\n').split('\n')):
        m = re.match(r'^##\s+(.*)$', line.strip())
        if m:
            toc.append((f'{anchor_prefix}-{len(toc)}', m.group(1).strip()))
    return toc

def teaser(md, n=150):
    m = re.search(r'^##\s+0\..*?$', md, re.M)
    if not m: return ''
    start = m.end()
    nxt = md.find('\n## ', start)
    seg = md[start:nxt if nxt > 0 else len(md)].strip()
    seg = re.sub(r'^[:：\s]+', '', seg)
    seg = seg[:n]
    seg = re.sub(r'\*{1,2}', '', seg)   # 截断可能把成对 ** 切成单只,卡片摘要里直接去掉加粗标记
    return seg + ('…' if len(seg) >= n else '')

# ----------------------------------------------------------------------------- assets
# CSS/JS 源文件在 tools/assets_src/,改样式请编辑那里后重新构建
_ASR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets_src')
CSS = open(os.path.join(_ASR, 'style.css'), encoding='utf-8').read()
JS  = open(os.path.join(_ASR, 'app.js'),  encoding='utf-8').read()
ASSETV = hashlib.md5((CSS + JS).encode('utf-8')).hexdigest()[:8]   # 资产指纹,缓存击穿

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%%TITLE%% · 协同制导 × 微分博弈 × RL 文献综述</title>
<link rel="stylesheet" href="%%ROOT%%assets/style.css?ver=%%ASSETV%%">
</head>
<body>
<div class="bgfx" aria-hidden="true"></div>
<header class="top"><div class="topin">
  <a class="brand" href="%%ROOT%%index.html"><span>制导·博弈·学习</span><i class="dotb"></i><span class="sub">文献综述</span></a>
  <nav class="menu">
    <a href="%%ROOT%%index.html"%%NAVI%%>首页</a>
    <a href="%%ROOT%%papers.html"%%NAVP%%>论文精读</a>
    <a href="%%ROOT%%comparison.html"%%NAVC%%>对比总表</a>
    <a href="%%ROOT%%gaps.html"%%NAVG%%>研究空白</a>
  </nav>
  <button id="themeBtn">🌙 深色</button>
</div></header>
<main>
%%BODY%%
</main>
<footer>17 篇论文 · 结构化精读(论断带页码)· 生成于 2026-10-31 · 静态站点,可托管于 GitHub Pages / Netlify / 任意 Web 服务器</footer>
<button id="topBtn" title="回到顶部">↑</button>
<script src="%%ROOT%%assets/app.js?ver=%%ASSETV%%"></script>
</body>
</html>
"""

def page(title, body, nav=''):
    t = TEMPLATE.replace('%%TITLE%%', title).replace('%%BODY%%', body)
    t = t.replace('%%ROOT%%', '../' if nav and nav.startswith('P') else '')
    t = t.replace('%%ASSETV%%', ASSETV)
    # nav highlighting
    for key, tag in [('I','%%NAVI%%'),('P','%%NAVP%%'),('C','%%NAVC%%'),('G','%%NAVG%%')]:
        t = t.replace(tag, ' class="on"' if nav == key else '')
    return t

def badge(g):
    return f'<span class="badge g{g}">{"ABC"[ord(g)-65] and {"A":"微分博弈与目标防御","B":"多弹协同制导","C":"强化学习制导"}[g]}</span>'

def find_note(pid):
    fs = glob.glob(SRC('literature/extract', pid + '_*.md'))
    return fs[0] if fs else None

def find_pdf(pid):
    fs = glob.glob(SRC('papers', pid + '_*.pdf'))
    return fs[0] if fs else None

# ----------------------------------------------------------------------------- build
def main():
    if os.path.isdir(OUT):
        try:
            shutil.rmtree(OUT)
        except PermissionError:
            # 本地 http.server 的 cwd 占着 site/ 目录句柄(Windows)时逐文件删,忽略占用的目录
            for root, dirs, files in os.walk(OUT, topdown=False):
                for fn in files:
                    try: os.remove(os.path.join(root, fn))
                    except OSError: pass
                for dn in dirs:
                    try: os.rmdir(os.path.join(root, dn))
                    except OSError: pass
    os.makedirs(os.path.join(OUT, 'assets'))
    os.makedirs(os.path.join(OUT, 'paper'))
    os.makedirs(os.path.join(OUT, 'pdfs'))

    open(os.path.join(OUT, 'assets/style.css'), 'w', encoding='utf-8').write(CSS)
    open(os.path.join(OUT, 'assets/app.js'), 'w', encoding='utf-8').write(JS)

    # ---- paper pages + metadata
    metas = []
    for p in PAPERS:
        nfp = find_note(p['id']); pfp = find_pdf(p['id'])
        if not nfp:
            raise SystemExit('note missing for ' + p['id'])
        md = open(nfp, encoding='utf-8').read()
        body_md = md
        toc = h2_toc(body_md)
        doc_html, _ = md_to_html(body_md)
        toclinks = '<aside class="toc"><b>本页目录</b>' + ''.join(
            f'<a href="#{a}">{esc(t)}</a>' for a, t in toc) + '</aside>'
        prev_p = next((x for x in PAPERS if x['id'] == f"{int(p['id'])-1:02d}"), None)
        next_p = next((x for x in PAPERS if x['id'] == f"{int(p['id'])+1:02d}"), None)
        navlinks = '<div class="pnav">' + (
            f'<a href="{prev_p["id"]}.html">← {prev_p["id"]} {esc(prev_p["title"][:28])}…</a>' if prev_p else '<span></span>') + (
            f'<a href="{next_p["id"]}.html">{next_p["id"]} {esc(next_p["title"][:28])}… →</a>' if next_p else '<span></span>') + '</div>'
        pdf_rel = f"../pdfs/{os.path.basename(pfp)}" if pfp else None
        head = (f'<p class="tag">{badge(p["group"])} · {esc(p["authors"])} · {esc(p["year"])} · {esc(p["venue"])}'
                f' · arXiv:{p["arxiv"]}'
                + (f' · <a href="{pdf_rel}" target="_blank">📄 原文 PDF</a>' if pfp else '') + '</p>')
        page_html = page(p['id'] + ' ' + p['title'],
                         f'<div class="two"><nav>{toclinks}</nav><article class="doc">{head}{doc_html}{navlinks}</article></div>',
                         nav='P')
        open(os.path.join(OUT, 'paper', p['id'] + '.html'), 'w', encoding='utf-8').write(page_html)
        if pfp:
            shutil.copy(pfp, os.path.join(OUT, 'pdfs', os.path.basename(pfp)))
        metas.append({**p, 'note_file': os.path.basename(nfp), 'pdf_file': os.path.basename(pfp) if pfp else None,
                      'teaser': teaser(md)})

    # ---- papers.html
    cards = []
    for p, m in zip(PAPERS, metas):
        cards.append(
            f'<article class="card" data-group="{p["group"]}">'
            f'<div class="prow"><span class="ptile g{p["group"]}">{p["id"]}</span>'
            f'<div><span class="badge g{p["group"]}">{GROUPS[p["group"]][0]}</span>'
            f'<span class="tag"> · {p["year"]}</span></div></div>'
            f'<h3><a href="paper/{p["id"]}.html">{esc(p["title"])}</a></h3>'
            f'<div class="meta">{esc(p["authors"])}<br>{esc(p["venue"])} · arXiv:{p["arxiv"]}</div>'
            f'<p class="teaser">{inline(esc(m["teaser"]))}</p>'
            f'<div class="links"><a href="paper/{p["id"]}.html">精读笔记</a>'
            + (f'<a href="pdfs/{m["pdf_file"]}" target="_blank">PDF</a>' if m["pdf_file"] else '')
            + f'<a href="https://arxiv.org/abs/{p["arxiv"]}" target="_blank" rel="noopener">arXiv</a></div></article>')
    body = ('<div class="hero"><h1>论文精读 <span class="grad">· 17 篇</span></h1>'
            '<p class="sub">每篇 10 节结构化笔记:问题建模 / 假设 / 方法核心与关键公式(带页码)/ 理论结果 / 实验设置 / 局限性双栏 / 可复现性 / 待验证 / 记号表。</p></div>'
            '<div class="bar">'
            '<button class="fbtn on" data-g="*">全部 17</button>'
            '<button class="fbtn" data-g="A">A · 微分博弈与目标防御 6</button>'
            '<button class="fbtn" data-g="B">B · 多弹协同制导 6</button>'
            '<button class="fbtn" data-g="C">C · 强化学习制导 5</button>'
            '<input id="q" type="search" placeholder="搜索标题 / 作者 / 出处…"></div>'
            '<div class="grid" id="paperGrid">' + ''.join(cards) + '</div>')
    open(os.path.join(OUT, 'papers.html'), 'w', encoding='utf-8').write(page('论文精读', body, nav='P'))

    # ---- comparison.html (rendered md + interactive CSV)
    cmp_md = open(SRC('literature/comparison_table.md'), encoding='utf-8').read()
    cmp_html, _ = md_to_html(cmp_md)
    with open(SRC('literature/comparison_table.csv'), encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    data_json = json.dumps(rows, ensure_ascii=False).replace('</', '<\\/')
    csv_section = (
        '<h2 id="csv">机读对比表(可排序 / 搜索)</h2>'
        '<p class="tag">点击表头排序;搜索框过滤全部 20 列;数据来自 comparison_table.csv。</p>'
        '<div class="bar"><input id="csvQ" type="search" placeholder="在 20 列中搜索,如:固定时间 / V_D>V_A / 6DOF / 无定理…">'
        '<span id="csvCount" class="tag"></span></div><div id="csvTable"></div>'
        f'<script type="application/json" id="csv-data">{data_json}</script>')
    body = ('<div class="hero"><h1>方法对比总表</h1>'
            '<p class="sub">假设强度 / 信息结构 / 理论证明 / 对抗性 / 实验规模 五维对照 + 记号对应表 + 三类红旗清单。</p></div>'
            '<div class="doc">' + csv_section + cmp_html + '</div>')
    open(os.path.join(OUT, 'comparison.html'), 'w', encoding='utf-8').write(page('对比总表', body, nav='C'))

    # ---- gaps.html
    gaps_md = open(SRC('literature/gaps.md'), encoding='utf-8').read()
    gaps_html, _ = md_to_html(gaps_md)
    body = ('<div class="hero"><h1>研究空白与机会 <span class="grad">· 12 条</span></h1>'
            '<p class="sub">每条空白 ≥2 篇论文证据,并给出「现有工作止步于哪里、下一步是什么」;文末附待验证区与空白-论文覆盖矩阵。</p></div>'
            f'<div class="doc">{gaps_html}</div>')
    open(os.path.join(OUT, 'gaps.html'), 'w', encoding='utf-8').write(page('研究空白', body, nav='G'))

    # ---- index.html
    ICONS = {
        'A': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2.6" fill="#fff" stroke="none"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>',
        'B': '<svg viewBox="0 0 24 24"><circle cx="5" cy="12" r="2.4"/><circle cx="19" cy="5" r="2.4"/><circle cx="19" cy="19" r="2.4"/><path d="M7 10.8 17 6M7 13.2 17 18"/></svg>',
        'C': '<svg viewBox="0 0 24 24"><path d="M13 2 4.5 13.5H11l-1 8.5L18.5 10.5H12l1-8.5z"/></svg>'}
    group_cards = ''.join(
        f'<article class="card"><div class="row"><span class="gtile g{g}">{ICONS[g]}</span>'
        f'<span class="tag">{cnt} 篇 · {ids}</span></div>'
        f'<h3>{name}</h3><p class="teaser">{desc}</p>'
        f'<div class="links"><a href="papers.html?g={g}">浏览该组 →</a></div></article>'
        for g, (name, desc), cnt, ids in [
            ('A', GROUPS['A'], 6, '01–06'), ('B', GROUPS['B'], 6, '07–12'), ('C', GROUPS['C'], 5, '13–17')])
    highlights = ''.join(
        f'<article class="card"><h3><span class="mini {mc}"></span>{t}</h3><p class="teaser">{d}</p>'
        f'<div class="links"><a href="{href}">{lt} →</a></div></article>'
        for mc, t, d, href, lt in [
            ('gA', '理论-现实的剪刀差', '博弈组理论最硬、假设最虚;RL 组动力学最实、0 定理。三属性(真实动力学/最优对手/理论保证)无一同时占二。', 'gaps.html#sec-0', 'G1 · 博弈×约束'),
            ('gC', '同族文献的实锤矛盾', '03 用双侧 PMP 推翻自家 2015 年解;07 的机动目标声称被自身证明否定;11 增益下界差一倍;13 正文与表格相反;16 时间常数差 10 倍。', 'comparison.html#sec-4', '红旗清单'),
            ('gB', '最小可做实验', '以 16 的 T-A-D 场景为公共测试床:博弈最优策略(03)、保障性制导(06)、TD3(16) 同协议换边对决。', 'gaps.html#sec-10', 'G11 · 统一测试床'),
        ])
    mq = ('<span>17 篇结构化精读</span><span>✱</span><span>12 条研究空白</span><span>✱</span>'
          '<span>20+ 处矛盾红旗</span><span>✱</span><span>5 维方法对比</span><span>✱</span>'
          '<span>0 外部依赖</span><span>✱</span>') * 2
    body = ('<div class="hero ghero"><div class="gleft">'
            '<div class="eyebrow">系统性文献综述 · 2026</div>'
            '<h1><span>多智能体协同制导</span><span>微分博弈</span><mark>强化学习</mark></h1>'
            '<p class="sub">17 篇论文的结构化精读、五维方法对比与 12 条研究空白。所有论断可回溯:笔记 → 原文页码;推测一律标注「待验证」。</p>'
            '<div class="gsearch"><svg class="gsicon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'
            '<input id="globalQ" type="search" placeholder="搜索 17 篇精读笔记…" aria-label="全局搜索">'
            '<div class="hint">回车进入「论文精读」并自动过滤 · 例:固定时间 / Garcia / 规避</div></div>'
            '</div>'
            '<div class="heroart" aria-hidden="true"><i class="sq s1"></i><i class="sq s2"></i><i class="sq s3"></i><b>✱</b></div>'
            '</div>'
            '<div class="marquee"><div class="track">' + mq + '</div></div>'
            '<div class="stats">'
            '<div class="stat"><b>17</b><span>篇论文精读</span></div>'
            '<div class="stat"><b>3</b><span>研究支柱</span></div>'
            '<div class="stat"><b>12</b><span>条研究空白</span></div>'
            '<div class="stat hot"><b>20+</b><span>矛盾/笔误红旗</span></div>'
            '<div class="stat"><b>0</b><span>外部依赖</span></div>'
            '</div>'
            '<div class="grid">' + group_cards + '</div>'
            '<h2 style="margin:34px 0 14px;font-size:20px">三条最重要的横向结论</h2>'
            '<div class="grid">' + highlights + '</div>'
            '<h2 style="margin:34px 0 14px;font-size:20px">快速入口</h2>'
            '<div class="bar"><a class="fbtn" href="papers.html">📖 17 篇精读笔记</a>'
            '<a class="fbtn" href="comparison.html">📊 五维对比 + 记号对应</a>'
            '<a class="fbtn" href="gaps.html">🕳 研究空白 G1–G12</a>'
            '<a class="fbtn" href="comparison.html#sec-4">🚩 矛盾红旗清单</a></div>')
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page('首页', body, nav='I'))

    # ---- README
    open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8').write(
"""# 部署说明

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
""")

    print('site built at', OUT)
    for f in sorted(glob.glob(OUT + '/**/*', recursive=True)):
        if os.path.isfile(f):
            print(f'{os.path.getsize(f):>9}  {os.path.relpath(f, OUT)}')

if __name__ == '__main__':
    main()
