"""
Move the contents of `js_funcs` into a file that can test the javascript.
"""

from pathlib import Path

from bulk._bokeh_utils import js_funcs

all_code = js_funcs() + "\n\n" + Path("js", "prep.js").read_text()
Path("js", "tests.js").write_text(all_code)
