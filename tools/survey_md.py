# -*- coding: utf-8 -*-
"""Survey markdown features used across the literature notes and deliverables."""
import glob, re, collections, os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
feat = collections.Counter()
sample_math = []
files = sorted(glob.glob(os.path.join(WS, 'literature/extract/*.md')))
files += [os.path.join(WS, 'literature/comparison_table.md'), os.path.join(WS, 'literature/gaps.md')]

for fp in files:
    t = open(fp, encoding='utf-8').read()
    inline = re.findall(r'\$[^$\n]{3,80}\$', t)
    feat['inline_math'] += bool(inline)
    feat['block_math'] += ('$$' in t)
    feat['fenced_code'] += ('```' in t)
    feat['tables'] += bool(re.search(r'^\|.*\|', t, re.M))
    feat['blockquote'] += bool(re.search(r'^> ', t, re.M))
    feat['ol_list'] += bool(re.search(r'^\d+\. ', t, re.M))
    feat['ul_list'] += bool(re.search(r'^- ', t, re.M))
    feat['images'] += bool(re.search(r'!\[', t))
    feat['links'] += bool(re.search(r'\]\(', t))
    feat['h4'] += bool(re.search(r'^#### ', t, re.M))
    feat['h3'] += bool(re.search(r'^### ', t, re.M))
    if inline and len(sample_math) < 6:
        sample_math.append((os.path.basename(fp), inline[0]))

print(dict(feat))
print('files:', len(files))
print('--- inline math samples ---')
for name, m in sample_math:
    print(name, '=>', m)
