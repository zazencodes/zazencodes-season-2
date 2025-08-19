import uuid
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Literal

from fastmcp import Context, FastMCP

mcp = FastMCP("MCP Bookstore (Elicitation Demo)")

# --- Pre-populated "database" -------------------------------------------------

BOOKS: dict[str, dict[str, float]] = {
    # title                                   price   weight_kg
    "Dune": {"price": 19.99, "weight_kg": 0.62},
    "Neuromancer": {"price": 14.99, "weight_kg": 0.42},
    "Snow Crash": {"price": 16.50, "weight_kg": 0.50},
    "Hyperion": {"price": 18.75, "weight_kg": 0.58},
    "The Three-Body Problem": {"price": 17.95, "weight_kg": 0.55},
    "The Left Hand of Darkness": {"price": 15.25, "weight_kg": 0.44},
    "Foundation": {"price": 13.99, "weight_kg": 0.40},
    "The Dispossessed": {"price": 16.25, "weight_kg": 0.47},
    "Children of Time": {"price": 21.00, "weight_kg": 0.70},
    "Ancillary Justice": {"price": 15.99, "weight_kg": 0.45},
    "Project Hail Mary": {"price": 23.50, "weight_kg": 0.78},
    "Leviathan Wakes": {"price": 18.25, "weight_kg": 0.64},
    "Red Mars": {"price": 17.50, "weight_kg": 0.66},
    "A Memory Called Empire": {"price": 19.25, "weight_kg": 0.60},
}

# Shipping zones (fun, simplified model; USD)
# cost = base + per_kg * weight_kg
# eta_days = (min_days, max_days)
LOCATIONS: dict[str, dict[str, float | tuple[int, int]]] = {
    "Toronto, Canada": {"base": 6.00, "per_kg": 4.00, "eta_days": (1, 3)},
    "Vancouver, Canada": {"base": 7.50, "per_kg": 4.50, "eta_days": (2, 4)},
    "Montreal, Canada": {"base": 6.50, "per_kg": 4.00, "eta_days": (1, 3)},
    "New York, USA": {"base": 7.00, "per_kg": 5.00, "eta_days": (3, 5)},
    "San Francisco, USA": {"base": 8.00, "per_kg": 5.50, "eta_days": (4, 6)},
    "London, UK": {"base": 12.00, "per_kg": 7.00, "eta_days": (5, 8)},
    "Berlin, Germany": {"base": 12.00, "per_kg": 7.50, "eta_days": (5, 9)},
    "Tokyo, Japan": {"base": 13.00, "per_kg": 8.50, "eta_days": (6, 10)},
    "Sydney, Australia": {"base": 14.00, "per_kg": 9.00, "eta_days": (7, 12)},
    "São Paulo, Brazil": {"base": 13.00, "per_kg": 8.00, "eta_days": (7, 12)},
    "Other / International": {"base": 15.00, "per_kg": 9.00, "eta_days": (7, 14)},
}

LOCATIONS_LITERAL = Literal[
    "Toronto, Canada",
    "Vancouver, Canada",
    "Montreal, Canada",
    "New York, USA",
    "San Francisco, USA",
    "London, UK",
    "Berlin, Germany",
    "Tokyo, Japan",
    "Sydney, Australia",
    "São Paulo, Brazil",
    "Other / International",
]


def _normalize_title(title: str) -> str:
    title = title.strip().lower()
    # exact match by case-insensitive key
    for k in BOOKS.keys():
        if k.lower() == title:
            return k
    # simple fallback: prefix/substring match
    for k in BOOKS.keys():
        if title in k.lower():
            return k
    return ""


def _format_money(num: float) -> str:
    return f"${num:,.2f}"


def _eta_from_today(min_days: int, max_days: int) -> str:
    today = date.today()
    start = today + timedelta(days=min_days)
    end = today + timedelta(days=max_days)
    return f"{start.isoformat()}–{end.isoformat()}"


def _shipping_quote(location_name: str, weight_kg: float) -> dict[str, str | float]:
    loc = LOCATIONS[location_name]
    base = float(loc["base"])
    per_kg = float(loc["per_kg"])
    min_d, max_d = loc["eta_days"]  # type: ignore
    ship_cost = base + per_kg * weight_kg
    eta_str = _eta_from_today(int(min_d), int(max_d))
    return {
        "location": location_name,
        "shipping_cost": round(ship_cost, 2),
        "eta": eta_str,
    }


# --- Tools --------------------------------------------------------------------


@mcp.tool
async def list_books(ctx: Context) -> dict:
    """
    Return the available books with prices and weights.
    """
    catalog = [{"title": k, **v} for k, v in BOOKS.items()]
    catalog.sort(key=lambda x: x["title"])
    return {"currency": "USD", "items": catalog}


@mcp.tool
async def buy_book(ctx: Context, title: str) -> dict | str:
    """
    Two-step, human-in-the-loop purchase flow using elicitation:

    1) Look up book price and ask for approval (no payload on accept).
    2) Ask for shipping location (enum), compute shipping cost + ETA,
       show the full total, and ask for final approval to "purchase".
    """
    # --- Resolve the book -----------------------------------------------------
    resolved = _normalize_title(title)
    if not resolved:
        # Helpful failure: include a short catalog slice.
        top = sorted(BOOKS.keys())[:8]
        return {
            "ok": False,
            "message": f"Book not found for '{title}'. Try one of: {', '.join(top)}",
        }

    book = BOOKS[resolved]
    price = float(book["price"])
    weight = float(book["weight_kg"])

    # --- Step 1: price approval ----------------------------------------------
    price_msg = (
        f"Price for **{resolved}** is {_format_money(price)} (weight {weight:.2f} kg). "
        "Accept to continue to shipping options."
    )
    price_ok = await ctx.elicit(price_msg, response_type=None)
    if not price_ok.action:
        return "User rejected the price."

    # --- Step 2: choose shipping location------- ------------------------------
    locations = list(LOCATIONS.keys())

    @dataclass
    class ShippingLocationResponse:
        location: LOCATIONS_LITERAL

    loc_resp = await ctx.elicit(
        "Choose a shipping location",
        response_type=ShippingLocationResponse,
    )
    chosen_location = loc_resp.data.location
    if chosen_location not in locations:
        return f"Invalid location, select from: {locations}"

    quote = _shipping_quote(chosen_location, weight)

    # Total (pretend taxes included in book price; shipping is extra)
    shipping_cost = float(quote["shipping_cost"])
    total = round(price + shipping_cost, 2)
    eta = str(quote["eta"])

    # --- Step 3: total cost + ETA ---------------------------------------------
    final_msg = (
        f"**Order summary**\n"
        f"- Book: {resolved} — {_format_money(price)}\n"
        f"- Ship to: {chosen_location}\n"
        f"- Shipping: {_format_money(shipping_cost)} (ETA {eta})\n"
        f"**Total: {_format_money(total)}**\n\n"
        "Accept to place the order."
    )
    final_ok = await ctx.elicit(final_msg, response_type=None)
    if not final_ok.action:
        return "User rejected order"

    order_id = str(uuid.uuid4())[:8].upper()
    return {
        "ok": True,
        "message": "✅ Purchase complete.",
        "order": {
            "id": order_id,
            "title": resolved,
            "price": round(price, 2),
            "shipping_cost": shipping_cost,
            "total": total,
            "ship_to": chosen_location,
            "eta": eta,
            "currency": "USD",
        },
    }


if __name__ == "__main__":
    mcp.run()
