import logging
import os
import re
import time
from typing import Any, Dict, List, Tuple

import pandas as pd
from fastmcp import Context, FastMCP
from fastmcp.utilities import logging

logger = logging.get_logger(__name__)


mcp = FastMCP("Vegan Recipes API Runner — Progress Demo")

# All params are OPTIONAL; the tool will ignore columns not recognized.
# (name, expected_type_hint) — types are advisory only for display / reference.
API_PARAMS: List[Tuple[str, str]] = [
    ("cuisine", "string"),
    ("dietary_restrictions", "string"),  # comma/semicolon-separated list OK
    ("include_ingredients", "string"),  # comma/semicolon-separated list OK
    ("exclude_ingredients", "string"),  # comma/semicolon-separated list OK
    ("max_prep_time_mins", "integer"),
    ("limit", "integer"),
    ("sort_by", "string"),  # e.g., "rating", "prep_time", "popularity"
    ("city", "string"),
    ("country", "string"),
]

ALLOWED_NAMES = [name for name, _ in API_PARAMS]
TYPE_HINTS = {name: typ for name, typ in API_PARAMS}

# ---------------------- Helpers ----------------------------------------------

_LIST_PARAMS = {"dietary_restrictions", "include_ingredients", "exclude_ingredients"}

# Simple synonym map to automatically map common header variants -> API params
_SPLIT_RE = re.compile(r"[;,]")


def _split_list(s: str) -> List[str]:
    """Split on comma/semicolon, trim whitespace, drop empties."""
    items = [p.strip() for p in _SPLIT_RE.split(str(s))]
    return [p for p in items if p]


def _safe_int(value: Any) -> Any:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        # Allow floats like 5.0 -> 5
        f = float(str(value).strip())
        i = int(f)
        return i
    except Exception:
        return None


def _normalize_arg(param: str, raw: Any) -> Tuple[Any, str]:
    """
    Normalize raw CSV cell into (python_value, printable_repr).
    - list-like params => List[str]
    - numeric ints parsed for limit / max_prep_time_mins when possible
    - strings are quoted in printable repr
    - blanks/NaN -> (None, "None")
    """
    if raw is None:
        return None, "None"
    if isinstance(raw, float) and pd.isna(raw):
        return None, "None"

    if param in {"limit", "max_prep_time_mins"}:
        ival = _safe_int(raw)
        if ival is not None:
            return ival, str(ival)
        # ignore invalid numerics instead of passing as strings
        return None, "None"

    if param in _LIST_PARAMS:
        items = _split_list(raw)
        return items, "[" + ", ".join(repr(x) for x in items) + "]"

    s = str(raw).strip()
    if not s:
        return None, "None"
    return s, repr(s)


def _auto_map_headers(headers: List[str]) -> List[Dict[str, str]]:
    """Map CSV headers to known API params using exact header names.

    Returns list of dicts: {csv_column, param, type}
    Only headers that exactly match known params (case-insensitive) are returned; order preserved from CSV.
    """
    mapped: List[Dict[str, str]] = []
    for h in headers:
        if h is None:
            continue
        key = str(h).strip()
        if not key:
            continue
        k = key.lower()
        if k in ALLOWED_NAMES:
            mapped.append(
                {
                    "csv_column": key,
                    "param": k,
                    "type": TYPE_HINTS[k],
                }
            )
    return mapped


# ---------------------- Tool --------------------------------------------------


@mcp.tool
async def run_vegan_recipes_api_on_csv(csv_path: str, ctx: Context) -> dict:
    """
    Run a CSV through the Vegan Recipes API with PROGRESS updates.

    Flow:
      1) Validate that csv_path is an absolute path.
      2) Load the CSV with pandas and automatically map headers -> optional API params.
      3) For each row, build a call like: recipes.search(cuisine='Italian', limit=10, ...)
         - Send a progress update after each request.
         - Sleep 1s between requests to simulate API latency.

    IMPORTANT: csv_path MUST be an absolute system path (e.g., '/Users/alex/data/recipes.csv').
    Relative paths are rejected in this demo.
    """
    # 1) Enforce absolute path to avoid surprises in different client working dirs
    if not os.path.isabs(csv_path):
        return {
            "ok": False,
            "message": (
                "csv_path must be an ABSOLUTE path (e.g., '/Users/you/vegan_queries.csv'). "
                "Relative paths are not supported in this demo."
            ),
        }

    # 2) Load CSV with pandas
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return {"ok": False, "message": f"Failed to read CSV: {e}"}

    headers = [str(c) for c in list(df.columns)]
    if not headers:
        return {"ok": False, "message": "No headers found in CSV."}

    # Auto-map headers to known API params
    selected = _auto_map_headers(headers)

    # Build example calls for *all* rows (no row cap; pandas handles it efficiently)
    api_calls: List[str] = []

    total = int(df.shape[0])
    await ctx.info(
        f"Preparing {total} API request(s) from '{os.path.basename(csv_path)}'"
    )

    logger.info("Hello from Alex on Thursday evening in Toronto")
    logger.error("Hello from Alex on Thursday evening in Toronto")

    # Precompute index so we can always send a final 100%
    for i, row in enumerate(df.itertuples(index=False), start=1):
        row_dict = (
            row._asdict()
            if hasattr(row, "_asdict")
            else {h: getattr(row, h) for h in headers}
        )
        args_pairs: List[str] = []
        for sel in selected:
            csv_col = sel["csv_column"]
            param = sel["param"]
            raw = row_dict.get(csv_col)
            norm, rep = _normalize_arg(param, raw)
            if norm is None:
                continue
            args_pairs.append(f"{param}={rep}")

        call = f"recipes.search({', '.join(args_pairs)})"
        print(call)
        api_calls.append(call)

        # Send request
        await ctx.info(f"Sent request {i}/{total}: {call}")
        await ctx.report_progress(progress=i, total=total)
        time.sleep(1)

    # Ensure we signal completion (covers empty CSV case too)
    await ctx.report_progress(progress=total, total=max(total, 1))

    return {
        "ok": True,
        "summary": {
            "csv_path": csv_path,
            "headers": headers,
            "selected_params": selected,
            "rows_processed": total,
        },
    }


if __name__ == "__main__":
    mcp.run()
