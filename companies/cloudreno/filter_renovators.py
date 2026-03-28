"""
Filter 12M Google Maps US businesses to find kitchen & bath renovation companies
for CloudReno acquisition targeting.

ICP: Profitable K&B renovation companies, owner-operators, $1M-$10M revenue.
"""

import csv
import io
import os
import re
import zipfile
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "google-maps-12m-us-businesses")

# Category tiers
CORE_CATEGORIES = {
    "kitchen remodeler",
    "bathroom remodeler",
}

SECONDARY_CATEGORIES = {
    "remodeler",
}

TERTIARY_CATEGORIES = {
    "tile contractor",
    "countertop contractor",
    "flooring contractor",
}

ALL_TARGET_CATEGORIES = CORE_CATEGORIES | SECONDARY_CATEGORIES | TERTIARY_CATEGORIES

# Name-based matching: require BOTH a K&B keyword AND a renovation keyword,
# OR a strong compound like "kitchen remodel" / "bath renovation" / "cabinet"
KB_NAME_KEYWORDS = ["kitchen", "bath", "bathroom"]
RENO_NAME_KEYWORDS = ["remodel", "renovation", "renovator", "refinish", "resurface", "design", "showroom"]

# These standalone keywords are strong enough signals on their own
STANDALONE_NAME_KEYWORDS = [
    "kitchen remodel", "bath remodel", "bathroom remodel",
    "kitchen renovation", "bath renovation", "bathroom renovation",
    "kitchen design", "bath design", "bathroom design",
    "cabinet", "countertop",
    "kitchen and bath", "kitchen & bath",
]

# Name-based exclusion keywords (case-insensitive)
NAME_EXCLUDE_KEYWORDS = [
    "roofing", "roof", "commercial", "industrial",
]

# Plumbing is excluded UNLESS name also contains a K&B keyword
PLUMBING_KEYWORD = "plumbing"

KB_KEYWORDS = ["kitchen", "bath", "bathroom"]

# Categories that indicate a non-renovation business (restaurants, food, etc.)
NON_RENO_CATEGORIES = {
    "restaurant", "bar", "cafe", "bakery", "caterer", "food",
    "pizza", "sushi", "diner", "bistro", "grill", "pub",
    "coffee", "tea", "ice cream", "dessert", "juice",
    "grocery", "supermarket", "convenience store",
    "hotel", "motel", "inn", "lodge", "resort",
    "church", "mosque", "synagogue", "temple",
    "school", "university", "college",
    "hospital", "clinic", "doctor", "dentist", "veterinar",
    "salon", "spa", "barber", "nail",
    "gym", "fitness", "yoga",
    "car wash", "auto", "mechanic", "tire",
    "gas station", "laundry", "dry clean",
    "pet", "dog", "cat",
    "tattoo", "piercing",
    "moving", "storage",
    "attorney", "lawyer", "accountant",
    "real estate", "insurance",
    "bank", "credit union",
    "pharmacy", "drug",
}


def parse_categories(raw):
    """Parse category_titles field: \"['Kitchen remodeler', 'Remodeler']\" """
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    raw = raw.strip("[]")
    return [c.strip().strip("'\"") for c in raw.split(",") if c.strip()]


def classify_row(title, categories_raw):
    """Return relevance_tier or None if not a match."""
    title_lower = title.lower() if title else ""
    cats = [c.lower() for c in parse_categories(categories_raw)]

    # Check exclusions first
    has_kb_keyword = any(kw in title_lower for kw in KB_KEYWORDS)

    # Exclude plumbing unless also K&B
    if PLUMBING_KEYWORD in title_lower and not has_kb_keyword:
        return None

    # Exclude roofing, commercial, industrial
    for ex in NAME_EXCLUDE_KEYWORDS:
        if ex in title_lower:
            # But allow if also has K&B keyword
            if not has_kb_keyword:
                return None

    # Check category-based tiers
    for cat in cats:
        if cat in CORE_CATEGORIES:
            return "core"

    for cat in cats:
        if cat in SECONDARY_CATEGORIES:
            return "secondary"

    for cat in cats:
        if cat in TERTIARY_CATEGORIES:
            return "tertiary"

    # Check name-based match (businesses not captured by category)
    # First, exclude if categories clearly indicate non-renovation business
    cats_joined = " ".join(cats)
    for non_reno in NON_RENO_CATEGORIES:
        if non_reno in cats_joined:
            return None

    # Strong standalone matches (compound phrases or cabinet/countertop)
    for kw in STANDALONE_NAME_KEYWORDS:
        if kw in title_lower:
            return "name_match"

    # Weaker match: requires BOTH a K&B keyword AND a renovation keyword in the name
    has_kb = any(kw in title_lower for kw in KB_NAME_KEYWORDS)
    has_reno = any(kw in title_lower for kw in RENO_NAME_KEYWORDS)
    if has_kb and has_reno:
        return "name_match"

    return None


def main():
    zip_files = sorted(
        [f for f in os.listdir(DATA_DIR) if f.startswith("google-maps-scrape-part") and f.endswith(".zip")]
    )
    print(f"Found {len(zip_files)} zip files in {DATA_DIR}")

    output_path = os.path.join(SCRIPT_DIR, "renovator_leads_national.csv")
    header = ["title", "link", "phone", "category_titles", "zip_code", "normalized_display_link", "relevance_tier"]

    total_scanned = 0
    total_matched = 0
    tier_counts = {"core": 0, "secondary": 0, "tertiary": 0, "name_match": 0}
    seen = set()  # deduplicate by (title_lower, phone)

    with open(output_path, "w", newline="", encoding="utf-8") as outf:
        writer = csv.writer(outf)
        writer.writerow(header)

        for zip_name in zip_files:
            zip_path = os.path.join(DATA_DIR, zip_name)
            print(f"Processing {zip_name}...", end=" ", flush=True)
            file_matched = 0

            with zipfile.ZipFile(zip_path, "r") as zf:
                for csv_name in zf.namelist():
                    if not csv_name.endswith(".csv"):
                        continue
                    with zf.open(csv_name) as cf:
                        reader = csv.DictReader(io.TextIOWrapper(cf, encoding="utf-8", errors="replace"))
                        for row in reader:
                            total_scanned += 1
                            title = row.get("title", "")
                            categories_raw = row.get("category_titles", "")

                            tier = classify_row(title, categories_raw)
                            if tier is None:
                                continue

                            # Deduplicate
                            dedup_key = (title.lower().strip(), (row.get("phone") or "").strip())
                            if dedup_key in seen:
                                continue
                            seen.add(dedup_key)

                            writer.writerow([
                                title,
                                row.get("link", ""),
                                row.get("phone", ""),
                                categories_raw,
                                row.get("zip_code", ""),
                                row.get("normalized_display_link", ""),
                                tier,
                            ])
                            total_matched += 1
                            file_matched += 1
                            tier_counts[tier] += 1

            print(f"{file_matched} matches")

    print(f"\n{'='*60}")
    print(f"Total scanned:  {total_scanned:>10,}")
    print(f"Total matched:  {total_matched:>10,}")
    print(f"{'='*60}")
    print(f"Breakdown by tier:")
    for tier, count in sorted(tier_counts.items(), key=lambda x: -x[1]):
        print(f"  {tier:<12} {count:>8,}")
    print(f"{'='*60}")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()
