# mcp_sampling_viz_server.py
# Single-file FastMCP server: CSV -> profile -> client LLM sampling -> returns a 6-panel Matplotlib figure (PNG)

from __future__ import annotations

import io
import json
import re
import textwrap
from typing import Any, Dict

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fastmcp import Context, FastMCP
from fastmcp.utilities.types import Image as FMImage
from matplotlib.figure import Figure
from mcp.types import ImageContent

mcp = FastMCP(
    "SamplingVizServer",
    dependencies=["pandas", "numpy", "matplotlib", "pillow", "fastmcp"],
)

# ---------- helpers ----------


def _encode_figure(fig: Figure) -> ImageContent:
    """Render a Matplotlib figure to PNG bytes and wrap as MCP ImageContent."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    data = buf.getvalue()
    return FMImage(data=data, format="png").to_image_content()


def _extract_code(text: str) -> str:
    """Pull python code from a response that may (or may not) use ``` fences."""
    m = re.search(r"```(?:python)?\s*(.*?)```", text, flags=re.S)
    return (m.group(1) if m else text).strip()


def _profile_dataframe(df: pd.DataFrame, sample_rows: int = 5) -> str:
    """Compact JSON profile of the data for the LLM prompt + logging."""
    profile = {
        "shape": list(df.shape),
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "head": df.head(sample_rows).to_dict(orient="records"),
        "numeric_summary": df.describe(include=[np.number]).to_dict(),
    }
    return json.dumps(profile, indent=2, default=str)


def _limited_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Constrain imports inside exec to safe/expected libs only."""
    allowed = {
        "numpy",
        "pandas",
        "matplotlib",
        "matplotlib.pyplot",
        "math",
        "statistics",
    }
    if not (name in allowed or any(name.startswith(a + ".") for a in allowed)):
        raise ImportError(f"Import of '{name}' is blocked")
    import builtins as _bi

    return _bi.__import__(name, globals, locals, fromlist, level)


def _exec_user_code(code: str, scope: Dict[str, Any]) -> None:
    """Exec code in a constrained environment; raise if it errors."""
    allowed_builtins = {
        "len": len,
        "range": range,
        "min": min,
        "max": max,
        "sum": sum,
        "enumerate": enumerate,
        "zip": zip,
        "abs": abs,
        "sorted": sorted,
        "list": list,
        "dict": dict,
        "set": set,
        "tuple": tuple,
        "any": any,
        "all": all,
        "round": round,
        "__import__": _limited_import,
    }
    g = {"__builtins__": allowed_builtins}
    compiled = compile(code, "<sampling_code>", "exec")
    exec(compiled, g, scope)


# ---------- tool ----------


@mcp.tool()
async def analyze_csv_and_plot(csv_path: str, ctx: Context) -> ImageContent:
    """
    Load a CSV, profile it, request plotting code from the client's LLM via sampling,
    execute the code in a restricted namespace, and return a PNG image.
    REQUIREMENTS:
      • The generated code MUST set a variable named __result_fig__ to a matplotlib.figure.Figure.
      • The figure MUST contain six distinct subplots (e.g., a 2x3 grid).
      • No files saved; no plt.show(); no network access.
    FAILURE MODE:
      • If sampling or execution fails, this tool raises an error (no fallback).
    """
    # Load data
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV at '{csv_path}': {e}")

    # Profile + send to client logs for visibility
    profile_json = _profile_dataframe(df)
    await ctx.info(f"CSV profile:\n{profile_json}")

    # Build prompts for sampling
    system_prompt = (
        "You are a senior data visualization assistant. "
        "Return concise, robust Python that creates a SIX-subplot exploratory figure."
    )

    user_prompt = textwrap.dedent(f"""
        You are given a pandas DataFrame `df` that was loaded from a CSV.

        DATA PROFILE (JSON):
        {profile_json}

        TASK:
        - Write Python that builds a Matplotlib figure with SIX distinct subplots (e.g., 2 rows x 3 cols).
        - Prefer general EDA that adapts to arbitrary data (unknown columns).
          Examples: histograms for numeric cols, correlation heatmap (if >=2 numerics),
          scatter between top 2 numerics, category frequency bars, missingness bars,
          simple time trend if a datetime column/index is present, etc.
        - Handle missing/insufficient columns gracefully (guard conditions).
        - Use ONLY the provided objects: df (DataFrame), np, pd, plt.
        - DO NOT call plt.show(); DO NOT save files; DO NOT read external data.
        - At the end, assign the created matplotlib.figure.Figure to a variable named __result_fig__.

        EXECUTION ENVIRONMENT:
        - The following objects exist already: df, np, pd, plt.
        - If you create Axes via subplots, prefer fig, axes = plt.subplots(2, 3, figsize=(15, 8)).
        - Set titles/labels and keep plots readable.
        - RETURN ONLY PYTHON CODE (no backticks, no prose).
        - The final line MUST set: __result_fig__ = <your_figure_object>
    """).strip()

    # Request code from the client's LLM (sampling must be supported by the client)
    try:
        response = await ctx.sample(
            messages=user_prompt,
            system_prompt=system_prompt,
            max_tokens=1200,
            temperature=0.2,
        )
    except Exception as e:
        raise RuntimeError(f"Sampling failed: {e}")

    code = _extract_code(getattr(response, "text", "") or "")
    if not code:
        raise RuntimeError("Sampling returned empty code.")

    # Execute generated code in a restricted namespace with pre-provided objects
    scope: Dict[str, Any] = {"df": df, "np": np, "pd": pd, "plt": plt}
    try:
        _exec_user_code(code, scope)
    except Exception as e:
        await ctx.error(f"Generated code execution failed:\n{code}")
        raise RuntimeError(f"Execution error: {e}")

    # Retrieve the returned figure
    result_fig = scope.get("__result_fig__", None)
    if not isinstance(result_fig, Figure):
        raise RuntimeError(
            "Generated code did not set __result_fig__ to a matplotlib.figure.Figure."
        )

    # (Light) validation: ensure at least six axes exist
    if not hasattr(result_fig, "axes") or len(result_fig.axes) < 6:
        raise RuntimeError(
            f"Expected a figure with >= 6 subplots, got {len(getattr(result_fig, 'axes', []))}."
        )

    # Encode and return PNG ImageContent
    return _encode_figure(result_fig)


if __name__ == "__main__":
    mcp.run()
