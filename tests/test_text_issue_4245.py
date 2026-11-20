import subprocess
import sys
from textwrap import dedent

import pytest


@pytest.mark.parametrize("method", ["stylize", "stylize_before"])
@pytest.mark.parametrize("start", [-3, -4])
def test_slice_after_negative_style_start(method, start):
    script = dedent("""
        import sys
        from rich.text import Span, Text

        text = Text("abc")
        getattr(text, sys.argv[1])("red", start=int(sys.argv[2]))
        result = text[1:]
        assert result.plain == "bc", result.plain
        assert result.spans == [Span(0, 2, "red")], result.spans
    """)

    try:
        result = subprocess.run(
            [sys.executable, "-c", script, method, str(start)],
            capture_output=True,
            text=True,
            timeout=3,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"{method}(start={start}): text[1:] did not return", pytrace=False)

    assert result.returncode == 0, result.stderr