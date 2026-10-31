# -*- coding: utf-8 -*-
"""Sync site/ -> docs/ for GitHub Pages (Pages 挂载 main 分支的 /docs 目录)."""
import os, shutil

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(WS, 'site')
DST = os.path.join(WS, 'docs')

if not os.path.isdir(SRC):
    raise SystemExit('site/ 不存在,先运行 tools/build_site.py')
if os.path.isdir(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
print('docs/ synced from site/ :', sum(len(f) for _, _, f in os.walk(DST)), 'files')
