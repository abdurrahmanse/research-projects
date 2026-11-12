"""Convert a '# %%' percent-format script into an .ipynb, optionally executing it.

Cells:  '# %%'            -> code cell
        '# %% [markdown]' -> markdown cell (every following line starts with '# ')
Usage:  python tools/make_notebook.py src.py out.ipynb [--run]
"""
import os
import sys

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def parse(text):
    cells, kind, buf = [], None, []

    def flush():
        body = "\n".join(buf).strip("\n")
        if kind and body:
            if kind == "md":
                body = "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#") for l in body.split("\n"))
                cells.append(new_markdown_cell(body))
            else:
                cells.append(new_code_cell(body))

    for line in text.split("\n"):
        if line.startswith("# %%"):
            flush()
            kind, buf = ("md" if "[markdown]" in line else "code"), []
        else:
            buf.append(line)
    flush()
    return cells


src, out = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8") as f:
    nb = new_notebook(cells=parse(f.read()))

if "--run" in sys.argv:
    from nbconvert.preprocessors import ExecutePreprocessor

    ExecutePreprocessor(timeout=1800, kernel_name="python3").preprocess(
        nb, {"metadata": {"path": os.path.dirname(os.path.abspath(out))}}
    )

nbformat.write(nb, out)
print("wrote", out)
