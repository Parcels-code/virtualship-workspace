import json
import re
import sys

# `html_str = pio.to_html(fig, ...)` followed by `display(HTML(html_str))`
PATTERN = re.compile(r"(\w+) = pio\.to_html\((\w+).*\)\ndisplay\(HTML\(\1\)\)")


def patch_notebook(nb: dict) -> int:
    """Patch a notebook dict in place, returning the number of replacements."""
    n_total = 0
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source, n = PATTERN.subn(r"\2.show()", "".join(cell["source"]))
            if n:
                cell["source"] = source.splitlines(keepends=True)
                cell["outputs"] = []  # stale docs output
                n_total += n
    return n_total


if __name__ == "__main__":
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            nb = json.load(f)
        if patch_notebook(nb):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=1, ensure_ascii=False)
            print(f"Patched plotly figures -> fig.show() in {path}")
