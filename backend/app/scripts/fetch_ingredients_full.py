# scripts/fetch_all_ingredients_full.py
"""
FULL INGREDIENT SCRAPER FOR THECOCKTAILDB
----------------------------------------
This script:
  1. Fetches all cocktail categories
  2. Fetches all cocktail IDs from each category
  3. Fetches full drink details for each ID
  4. Extracts all ingredients (strIngredient1..15)
  5. Fetches ingredient details via search.php?i=<name>
  6. Normalizes, classifies, and exports a complete CSV

Output:
  all_ingredients_full.csv
"""

import csv
import time
import requests
from typing import Dict, Any, List, Optional, Set

BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1"
OUT_CSV = "all_ingredients_full.csv"

# --------------- HELPERS --------------- #

def fetch_json(url: str, params=None):
    """Safe GET wrapper."""
    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"!! Error fetching {url}: {e}")
        return None


def fetch_categories() -> List[str]:
    """Fetch all cocktail categories."""
    url = f"{BASE_URL}/list.php?c=list"
    data = fetch_json(url)
    if not data or "drinks" not in data:
        return []
    cats = [d["strCategory"] for d in data["drinks"] if d["strCategory"]]
    print(f"Found {len(cats)} categories.")
    return cats


def fetch_ids_for_category(cat: str) -> List[str]:
    """Fetch IDs of cocktails in a given category."""
    url = f"{BASE_URL}/filter.php"
    data = fetch_json(url, {"c": cat})
    if not data or "drinks" not in data:
        return []
    ids = [d["idDrink"] for d in data["drinks"] if d["idDrink"]]
    print(f"  {cat}: {len(ids)} drinks")
    return ids


def fetch_drink_details(drink_id: str) -> Optional[Dict[str, Any]]:
    """Fetch drink details by ID."""
    url = f"{BASE_URL}/lookup.php"
    data = fetch_json(url, {"i": drink_id})
    if not data or "drinks" not in data or not data["drinks"]:
        return None
    return data["drinks"][0]


def extract_ingredients_from_drink(drink: Dict[str, Any]) -> List[str]:
    """Extract up to 15 ingredient fields from drink details."""
    ingredients = []
    for i in range(1, 16):
        name = drink.get(f"strIngredient{i}")
        if name and name.strip():
            ingredients.append(name.strip())
    return ingredients


def fetch_ingredient_details_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Fetch detailed ingredient info via search.php?i="""
    url = f"{BASE_URL}/search.php"
    data = fetch_json(url, {"i": name})
    if not data:
        return None
    drinks = data.get("ingredients") or data.get("drinks") or []
    if not drinks:
        return None
    return drinks[0]


# ----------------- CLASSIFICATION ----------------- #

def classify_type(str_type: Optional[str], str_alcohol: Optional[str]) -> str:
    """Classify ingredient into simple category."""
    t = (str_type or "").lower()
    alc = (str_alcohol or "").lower()

    if "liqueur" in t or "aperitif" in t or "amaro" in t or "vermouth" in t:
        return "liqueur"
    if any(x in t for x in ["rum", "vodka", "whisky", "whiskey", "gin", "tequila", "spirit"]):
        return "spirit"
    if "brandy" in t:
        return "spirit"
    if "syrup" in t:
        return "syrup"
    if "juice" in t:
        return "juice"
    if "bitter" in t:
        return "bitter"

    # fallbacks
    if alc == "yes":
        return "spirit"
    return "other"


def normalize_abv(abv: Optional[str]) -> str:
    if not abv:
        return ""
    return abv.replace("%", "").strip()


# --------------- MAIN SCRIPT --------------- #

def main():
    print("STEP 1: Fetching categories...")
    categories = fetch_categories()

    all_drink_ids: Set[str] = set()

    print("\nSTEP 2: Fetching drink IDs from all categories...")
    for cat in categories:
        ids = fetch_ids_for_category(cat)
        for d in ids:
            all_drink_ids.add(d)
        time.sleep(0.2)

    print(f"Total unique drink IDs: {len(all_drink_ids)}")

    print("\nSTEP 3: Fetching drink details & extracting ingredients...")
    ingredient_names: Set[str] = set()

    for idx, drink_id in enumerate(all_drink_ids):
        print(f"  [{idx+1}/{len(all_drink_ids)}] Drink ID {drink_id}")
        drink = fetch_drink_details(drink_id)
        if drink:
            ings = extract_ingredients_from_drink(drink)
            for ing in ings:
                ingredient_names.add(ing.lower().strip())

        time.sleep(0.15)

    print(f"\nTotal unique ingredient names found: {len(ingredient_names)}")

    print("\nSTEP 4: Fetching ingredient details for each name...")
    csv_rows = []

    for idx, name in enumerate(sorted(ingredient_names)):
        print(f"  [{idx+1}/{len(ingredient_names)}] {name}")
        details = fetch_ingredient_details_by_name(name)
        time.sleep(0.15)

        if details:
            str_type = details.get("strType")
            str_alc = details.get("strAlcohol")
            str_abv = details.get("strABV")
        else:
            str_type = None
            str_alc = None
            str_abv = None

        csv_rows.append({
            "name": name,
            "type": classify_type(str_type, str_alc),
            "abv": normalize_abv(str_abv),
            "flavor_tags": "",
        })

    print("\nSTEP 5: Writing CSV...")
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "type", "abv", "flavor_tags"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"\n✅ DONE! Wrote {len(csv_rows)} ingredients to {OUT_CSV}")


if __name__ == "__main__":
    main()
