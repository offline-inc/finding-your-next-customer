"""
Filter 12M US business dataset from Google Maps for WattShift channel partner leads.
Targets: solar installers, HVAC contractors, property management companies.
"""

import csv
import io
import os
import re
import zipfile
from collections import Counter

DATA_DIR = "/Users/mertiseri/code/Play/finding-your-next-customer/google-maps-12m-us-businesses"
OUTPUT_PATH = "/Users/mertiseri/code/Play/finding-your-next-customer/companies/wattshift/partner_leads_national.csv"

# Category matching sets (lowercase)
CORE_SOLAR = {
    "solar energy equipment supplier",
    "solar energy company",
    "solar energy system service",
    "solar hot water system supplier",
}

CORE_HVAC = {
    "hvac contractor",
    "air conditioning contractor",
    "heating contractor",
}

CORE_PROPERTY = {
    "property management company",
    "property maintenance",
}

SECONDARY = {
    "energy equipment and solutions",
    "energy supplier",
    "mechanical contractor",
    "insulation contractor",
}

# Name keywords (lowercase)
NAME_KEYWORDS = re.compile(
    r"solar|hvac|heating|cooling|air\s*conditioning|property\s*management|energy",
    re.IGNORECASE,
)

# Priority market zip prefixes
# California: 900-961, New York: 100-149
CA_RANGE = range(900, 962)
NY_RANGE = range(100, 150)


def parse_categories(cat_str: str) -> list[str]:
    """Extract category names from string like "['HVAC contractor', 'Heating']"."""
    if not cat_str:
        return []
    # Strip brackets and split by comma, then strip quotes/spaces
    inner = cat_str.strip("[]")
    cats = []
    for part in inner.split(","):
        clean = part.strip().strip("'\"")
        if clean:
            cats.append(clean)
    return cats


def classify_row(title: str, categories: list[str]) -> str | None:
    """Return relevance tier or None if not relevant."""
    cat_lower = {c.lower() for c in categories}

    if cat_lower & CORE_SOLAR:
        return "core_solar"
    if cat_lower & CORE_HVAC:
        return "core_hvac"
    if cat_lower & CORE_PROPERTY:
        return "core_property"
    if cat_lower & SECONDARY:
        return "secondary"
    if NAME_KEYWORDS.search(title or ""):
        return "name_match"
    return None


def is_priority_market(zip_code: str) -> bool:
    """Check if zip code is in CA or NY (NEM 3.0 priority markets)."""
    if not zip_code:
        return False
    try:
        prefix = int(zip_code[:3])
    except (ValueError, IndexError):
        return False
    return prefix in CA_RANGE or prefix in NY_RANGE


def main():
    zip_files = sorted(
        f
        for f in os.listdir(DATA_DIR)
        if f.startswith("google-maps-scrape-part") and f.endswith(".zip")
    )

    print(f"Found {len(zip_files)} zip files to process")

    results = []
    total_rows = 0

    for zf_name in zip_files:
        zf_path = os.path.join(DATA_DIR, zf_name)
        print(f"Processing {zf_name}...", end=" ", flush=True)
        part_count = 0

        with zipfile.ZipFile(zf_path, "r") as zf:
            for csv_name in zf.namelist():
                if not csv_name.endswith(".csv"):
                    continue
                with zf.open(csv_name) as f:
                    reader = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8"))
                    for row in reader:
                        total_rows += 1
                        title = row.get("title", "")
                        cat_str = row.get("category_titles", "")
                        zip_code = row.get("zip_code", "")

                        categories = parse_categories(cat_str)
                        tier = classify_row(title, categories)

                        if tier is None:
                            continue

                        results.append({
                            "title": title,
                            "link": row.get("link", ""),
                            "phone": row.get("phone", ""),
                            "category_titles": cat_str,
                            "zip_code": zip_code,
                            "normalized_display_link": row.get("normalized_display_link", ""),
                            "relevance_tier": tier,
                            "priority_market": is_priority_market(zip_code),
                        })
                        part_count += 1

        print(f"{part_count} matches")

    # Write output
    fieldnames = [
        "title", "link", "phone", "category_titles", "zip_code",
        "normalized_display_link", "relevance_tier", "priority_market",
    ]

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Stats
    print(f"\n{'='*60}")
    print(f"Total rows scanned: {total_rows:,}")
    print(f"Total matches: {len(results):,}")
    print(f"Output: {OUTPUT_PATH}")

    tier_counts = Counter(r["relevance_tier"] for r in results)
    print(f"\nBreakdown by tier:")
    for tier in ["core_solar", "core_hvac", "core_property", "secondary", "name_match"]:
        print(f"  {tier}: {tier_counts.get(tier, 0):,}")

    priority_count = sum(1 for r in results if r["priority_market"])
    non_priority = len(results) - priority_count
    print(f"\nPriority market (CA/NY):")
    print(f"  priority_market=true:  {priority_count:,}")
    print(f"  priority_market=false: {non_priority:,}")

    # Priority breakdown by tier
    print(f"\nPriority market breakdown by tier:")
    for tier in ["core_solar", "core_hvac", "core_property", "secondary", "name_match"]:
        count = sum(1 for r in results if r["relevance_tier"] == tier and r["priority_market"])
        print(f"  {tier} (priority): {count:,}")


if __name__ == "__main__":
    main()
