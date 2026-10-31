# -*- coding: utf-8 -*-
"""Verify rendered <li> counts match source list markers, and no duplicated items."""
import glob, re, os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad = 0
pages = 0
for f in sorted(glob.glob(os.path.join(WS, 'site/paper/*.html'))):
    t = open(f, encoding='utf-8').read()
    li = len(re.findall(r'<li>', t))
    pid = os.path.basename(f)[:2]
    src = open(glob.glob(os.path.join(WS, f'literature/extract/{pid}_*.md'))[0], encoding='utf-8').read()
    markers = len(re.findall(r'^\s*([-*]|\d+\.)\s', src, re.M))
    pages += 1
    if li != markers:
        bad += 1
        print('MISMATCH', pid, 'li=', li, 'markers=', markers)
    # 重复项检查:同一精确短语在全文出现 >1 次(取每页首个 bullet 的开头 24 字做抽查)
    m = re.search(r'<li><strong>([^<]{6,30})</strong>', t)
    if m and t.count(m.group(1)) > 1:
        bad += 1
        print('DUP?', pid, m.group(1), t.count(m.group(1)))
print('paper pages:', pages, '| problems:', bad)
for name, f, s in (('comparison', 'site/comparison.html', 'literature/comparison_table.md'),
                   ('gaps', 'site/gaps.html', 'literature/gaps.md')):
    t = open(os.path.join(WS, f), encoding='utf-8').read()
    src = open(os.path.join(WS, s), encoding='utf-8').read()
    li = len(re.findall(r'<li>', t))
    markers = len(re.findall(r'^\s*([-*]|\d+\.)\s', src, re.M))
    print(name, 'li=', li, 'markers=', markers, 'OK' if li == markers else 'MISMATCH')
t3 = open(os.path.join(WS, 'site/paper/03.html'), encoding='utf-8').read()
print('03 状态量出现次数:', t3.count('状态量(原文符号)'), '(应为1)')
