#!/usr/bin/env python3
# Script adopted from https://github.com/mitmproxy/pdoc/blob/main/examples/mkdocs/make.py
from pathlib import Path
import shutil

from pdoc import pdoc
from pdoc import render

here = Path(__file__).parent
out = here / "docs" / "api"
if out.exists():
    shutil.rmtree(out)

# Render documentation into docs/api...
render.configure(template_directory=here / "pdoc-template")
pdoc("operations", output_directory=out)

# ...and rename the .html files to .md so that mkdocs picks them up!
for f in out.glob("**/*.html"):
    f.rename(f.with_suffix(".md"))