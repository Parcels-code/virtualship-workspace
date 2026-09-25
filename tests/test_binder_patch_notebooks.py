import importlib.util
import json
import urllib.request
from pathlib import Path

import pytest

from test_binder_files import CONFIG, get_target_files

_spec = importlib.util.spec_from_file_location(
    "patch_notebooks", Path(__file__).parent.parent / ".binder" / "patch_notebooks.py"
)
patch_notebooks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(patch_notebooks)


def _code(nb):
    return "\n".join(
        "".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"
    )


def test_patch_notebook():
    nb = {
        "cells": [
            {
                "cell_type": "code",
                "source": [
                    'html_str = pio.to_html(fig, include_plotlyjs="cdn")\n',
                    "display(HTML(html_str))",
                ],
                "outputs": [{"output_type": "display_data"}],
            }
        ]
    }
    assert patch_notebooks.patch_notebook(nb) == 1
    assert nb["cells"][0]["source"] == ["fig.show()"]
    assert nb["cells"][0]["outputs"] == []


@pytest.mark.parametrize("file_path", get_target_files())
def test_upstream_notebook_fully_patched(file_path):
    """Catch drift: any plotly HTML embedding upstream must be rewritten by the patch."""
    url = (
        f"https://raw.githubusercontent.com/{CONFIG['repo_owner']}/"
        f"{CONFIG['repo_name']}/{CONFIG['branch']}/{file_path}"
    )
    with urllib.request.urlopen(url) as response:
        nb = json.load(response)
    patch_notebooks.patch_notebook(nb)
    assert "to_html(" not in _code(nb), (
        f"{file_path} embeds plotly HTML in a way .binder/patch_notebooks.py doesn't "
        "rewrite to `fig.show()`, so it won't render on Binder. Update PATTERN."
    )
