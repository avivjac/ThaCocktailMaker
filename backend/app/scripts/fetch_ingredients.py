# scripts/fetch_ingredients_to_csv.py
"""
Fetch all ingredients from TheCocktailDB and save them into a CSV file
suitable for importing into Supabase 'ingredients' table.

Columns:
  - name        (text, unique)
  - type        (text: spirit / liqueur / syrup / juice / bitter / other)
  - abv         (numeric as string or empty)
  - flavor_tags (text, left empty for now – can be used later)

Run:
  python scripts/fetch_ingredients_to_csv.py
"""

import csv
import time
import requests
from typing import Dict, Any, List, Optional

BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1"
OUTPUT_CSV = "ingredients_from_cocktaildb.csv"


def fetch_all_ingredients() -> List[Dict[str, Any]]:
    """Fetch all ingredients from list.php?i=list"""
    url = f"{BASE_URL}/list.php?i=list"
    print(f"Fetching ingredient list from: {url}")
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    drinks = data.get("drinks") or []
    print(f"Found {len(drinks)} ingredients in list.")
    return drinks


def fetch_ingredient_details_by_id(ingredient_id: str) -> Optional[Dict[str, Any]]:
    """Fetch ingredient details by id using lookup.php?iid=ID"""
    url = f"{BASE_URL}/lookup.php"
    params = {"iid": ingredient_id}
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        drinks = data.get("ingredients") or data.get("drinks") or []
        if not drinks:
            return None
        return drinks[0]
    except Exception as e:
        print(f"  !! Failed to fetch details for id={ingredient_id}: {e}")
        return None

def fetch_ingredient_details_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Fetch ingredient details by name using search.php?i="""
    url = f"{BASE_URL}/search.php"
    params = {"i": name}
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        drinks = data.get("ingredients") or data.get("drinks") or []
        if not drinks:
            return None
        return drinks[0]
    except Exception as e:
        print(f"  !! Failed to fetch details for name='{name}': {e}")
        return None

def classify_type(str_type: Optional[str], str_alcohol: Optional[str]) -> str:
    """
    Map CocktailDB type fields into our simplified 'type' column.

    This is intentionally simple - you can refine it later if you want.
    """
    t = (str_type or "").lower()
    alc = (str_alcohol or "").lower()

    if "liqueur" in t:
        return "liqueur"
    if "vermouth" in t or "aperitif" in t or "amaro" in t:
        return "liqueur"
    if "spirit" in t or "whisky" in t or "whiskey" in t or "rum" in t or "vodka" in t or "gin" in t or "tequila" in t:
        return "spirit"
    if "syrup" in t:
        return "syrup"
    if "juice" in t:
        return "juice"
    if "bitter" in t:
        return "bitter"
    # fallback: use alcohol flag
    if alc == "yes":
        return "spirit"
    return "other"


def normalize_abv(str_abv: Optional[str]) -> str:
    """Normalize ABV to a plain number string or empty."""
    if not str_abv:
        return ""
    s = str(str_abv).strip().replace("%", "")
    # basic sanity check
    return s if s else ""


def main():
    base_list = fetch_all_ingredients()

    rows_for_csv: List[Dict[str, str]] = []

    for idx, ing in enumerate(base_list, start=1):
        name = (ing.get("strIngredient1") or "").strip()
        if not name:
            continue

        print(f"[{idx}/{len(base_list)}] Processing '{name}'...")

        details = fetch_ingredient_details_by_name(name)
        time.sleep(0.15)  # כדי לא להעמיס על ה-API

        if details:
            str_type = details.get("strType")
            str_alcohol = details.get("strAlcohol") or details.get("strAlcoholic")
            str_abv = details.get("strABV")
        else:
            str_type = None
            str_alcohol = None
            str_abv = None

        row_type = classify_type(str_type, str_alcohol)
        row_abv = normalize_abv(str_abv)

        row = {
            "name": name,
            "type": row_type,
            "abv": row_abv,
            "flavor_tags": "",
        }
        rows_for_csv.append(row)

    # remove duplicates by name (just in case)
    unique_by_name: Dict[str, Dict[str, str]] = {}
    for r in rows_for_csv:
        unique_by_name[r["name"].lower()] = r

    final_rows = list(unique_by_name.values())
    print(f"Total rows after de-duplication: {len(final_rows)}")

    # write CSV
    fieldnames = ["name", "type", "abv", "flavor_tags"]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)

    print(f"✅ Done! Wrote {len(final_rows)} rows to '{OUTPUT_CSV}'")


if __name__ == "__main__":
    main()
