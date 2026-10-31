# -*- coding: utf-8 -*-
"""Final integrity check for the built site (no shell interpolation issues)."""
import glob, re

pat = re.compile(r'\*\*|(?<!\w)#{1,4}\s|\$\$')   # literal ** , stray headings, $$ math delims
issues = 0
pages = sorted(glob.glob('site/**/*.html', recursive=True))
for f in pages:
    t = open(f, encoding='utf-8').read()
    text = re.sub(r'<[^>]+>', '', t)
    hits = [m.group(0) for m in pat.finditer(text)]
    em = t.count('<em>')
    if hits or em:
        issues += 1
        print('ISSUE', f, '| hits:', hits[:5], '| em:', em)
print('pages:', len(pages), '| issue pages:', issues)

# cross-link sanity: every paper page link resolves
import os
for f in glob.glob('site/paper/*.html'):
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'href="(\.\./pdfs/[^"]+|[^"]*\.html)"', t):
        target = os.path.normpath(os.path.join('site/paper', m.group(1).split('?')[0]))
        if not os.path.exists(target):
            issues += 1
            print('BROKEN LINK in', f, '->', m.group(1))
for f in ['site/index.html', 'site/papers.html', 'site/comparison.html', 'site/gaps.html']:
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'href="(paper/[^"]+|pdfs/[^"]+|assets/[^"]+)"', t):
        target = os.path.normpath(os.path.join('site', m.group(1).split('?')[0]))
        if not os.path.exists(target):
            issues += 1
            print('BROKEN LINK in', f, '->', m.group(1))
print('final issues:', issues)
