# -*- coding: utf-8 -*-
"""One-shot patch: switch build_site.py's inline CSS/JS constants to assets_src/ files."""
import os, re

here = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(here, 'build_site.py')
s = open(target, encoding='utf-8').read()

i1 = s.index('CSS = r"""')
i2 = s.index('TEMPLATE = """')
loader = (
    "# CSS/JS 源文件在 tools/assets_src/,改样式请编辑那里后重新构建\n"
    "_ASR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets_src')\n"
    "CSS = open(os.path.join(_ASR, 'style.css'), encoding='utf-8').read()\n"
    "JS  = open(os.path.join(_ASR, 'app.js'),  encoding='utf-8').read()\n\n"
)
s = s[:i1] + loader + s[i2:]
open(target, 'w', encoding='utf-8').write(s)
print('patched. CSS/JS now loaded from tools/assets_src/.')
