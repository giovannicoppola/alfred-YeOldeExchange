#!/usr/bin/env python3
"""Alfred script filter for YeOldeExchange.

Converts an old UK amount (pounds, shillings, pence) from a given year into
its modern equivalent, plus what it would have bought at the time.
"""

import json
import os
import re
import sys

# the converter lives next to this file; import it rather than spawning a
# second Python process on every keystroke
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uk_currency_converter_docopt import UKCurrencyConverter  # noqa: E402

ICONS = {
    'horses': 'icons/horse.png',
    'cows': 'icons/cow.png',
    'sheep': 'icons/sheep.png',
    'pigs': 'icons/pig.png',
    'quarters_of_wheat': 'icons/wheat.png',
    'stones_of_wool': 'icons/wool.png',
    'loaves_of_bread': 'icons/bread.png',
    'gallons_of_ale': 'icons/ale.png',
}

USAGE = "Format: pounds shillings pence year, e.g. 5 10 6 1850"


def log(message):
    """Log to stderr, which shows in Alfred's debugger."""
    print(message, file=sys.stderr)


def item(title, subtitle, arg="", valid=False, icon="icon.png"):
    """One Alfred result row."""
    return {"title": title, "subtitle": subtitle, "arg": arg,
            "valid": valid, "icon": {"path": icon}}


def parse_input(query):
    """Parse the query into (pounds, shillings, pence, year).

    Accepts "5 10 6 1850" as well as "£5 10s 6d 1850" or "5/10/6 1850":
    currency marks and separators are ignored, only the numbers count.
    Returns (values, None) or (None, error message).
    """
    parts = re.findall(r'\d+', query)
    if re.search(r'[^\d\s£/sdSD]', query):
        return None, "Only numbers, please. " + USAGE
    if not parts:
        return None, USAGE
    if len(parts) < 4:
        return None, f"Need 4 numbers, got {len(parts)}. {USAGE}"
    if len(parts) > 4:
        return None, f"Too many numbers ({len(parts)}). {USAGE}"

    pounds, shillings, pence, year = (int(p) for p in parts)
    if pounds > 999:
        return None, "Pounds must be between 0 and 999"
    if shillings > 19:
        return None, "Shillings must be between 0 and 19"
    if pence > 11:
        return None, "Pence must be between 0 and 11"
    if not 1270 <= year <= 2017:
        return None, "Year must be between 1270 and 2017"
    return (pounds, shillings, pence, year), None


def quantity_text(quantity, name):
    """'2.2 quarters of wheat', with fewer decimals for larger amounts."""
    label = name.replace('_', ' ')
    return f"{quantity:.1f} {label}" if quantity >= 1 else f"{quantity:.2f} {label}"


def create_alfred_items(query):
    """Build the Alfred feedback for a query."""
    parsed, error = parse_input(query)
    if error:
        return {"items": [item("Enter an old £ s d amount and a year", error)]}

    pounds, shillings, pence, year = parsed
    try:
        result = UKCurrencyConverter().convert_historical_currency(pounds, shillings, pence, year)
    except Exception as e:  # keep Alfred informed rather than returning nothing
        log(f"conversion failed: {e!r}")
        return {"items": [item("Conversion error", str(e))]}

    original = result['original_amount']
    modern = f"£{result['modern_equivalent']:,.2f}"
    conversion = (f"{original} in {year} = {modern} in {result['target_year']} "
                  f"({result['inflation_multiplier']:.1f}x inflation)")

    # no uids: Alfred would otherwise learn and reorder the rows, and the
    # conversion should always come first
    items = [item(conversion, "↩ copy the conversion", conversion, True)]

    for name, quantity in (result.get('purchasing_power') or {}).items():
        if quantity < 0.01:  # too small to be meaningful
            continue
        text = quantity_text(quantity, name)
        items.append(item(text, f"What {original} bought in {year}  ·  ↩ copy",
                          f"{original} in {year} could buy {text}", True,
                          ICONS.get(name, "icon.png")))
    return {"items": items}


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(create_alfred_items(query)))


if __name__ == "__main__":
    main()
