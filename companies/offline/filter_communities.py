"""
Filter 12M US business Google Maps dataset to find community organizer leads for Offline.
Reads from zipped CSVs, filters by category and business name keywords.
"""

import csv
import io
import os
import zipfile
from pathlib import Path

DATA_DIR = Path("/Users/mertiseri/code/Play/finding-your-next-customer/google-maps-12m-us-businesses")
OUTPUT_PATH = Path("/Users/mertiseri/code/Play/finding-your-next-customer/companies/offline/community_leads_national.csv")

# --- Category filters ---
COMMUNITY_SPACE_CATEGORIES = {
    "dance school", "art school", "martial arts school", "music school",
    "yoga studio", "fitness center", "community center", "youth organization",
    "non-profit organization", "nonprofit organization",
    "dance studio", "dance club", "pilates studio", "boxing gym",
    "martial arts supply store",  # often doubles as school
    "yoga instructor", "meditation center",
    "community college", "social services organization",
    "cultural center", "recreation center",
}

EVENT_ADJACENT_CATEGORIES = {
    "event venue", "live music venue", "event planner",
    "event management company", "banquet hall", "wedding venue",
    "concert hall", "performing arts theater", "theatre",
    "music venue", "nightclub",
}

# --- Name keyword filters ---
NAME_KEYWORDS = [
    "run club", "running club", "supper club", "dinner club", "book club",
    "community", "collective", "social club", "fitness club", "dance studio",
    "wellness", "run crew", "running crew", "yoga collective", "movement",
    "tribe", "squad", "gathering", "meetup", "co-op",
]

# --- Major city zip prefixes ---
MAJOR_CITY_ZIP_PREFIXES = [
    "100", "101", "102", "103", "104",  # New York
    "900", "901", "902",                # Los Angeles
    "606", "607", "608",                # Chicago
    "941",                              # San Francisco
    "787",                              # Austin
    "331", "332",                       # Miami
    "972",                              # Portland
    "981",                              # Seattle
    "802",                              # Denver
    "372",                              # Nashville
    "303",                              # Atlanta
]


def classify_row(title: str, category_titles: str, zip_code: str):
    """Returns (relevance_tier, major_city) or None if no match."""
    title_lower = title.lower() if title else ""
    cat_lower = category_titles.lower() if category_titles else ""
    zip_str = str(zip_code).strip().split(".")[0] if zip_code else ""

    # Check category match
    tier = None
    for cat in COMMUNITY_SPACE_CATEGORIES:
        if cat in cat_lower:
            tier = "community_space"
            break
    if tier is None:
        for cat in EVENT_ADJACENT_CATEGORIES:
            if cat in cat_lower:
                tier = "event_adjacent"
                break
    if tier is None:
        for kw in NAME_KEYWORDS:
            if kw in title_lower:
                tier = "name_match"
                break

    if tier is None:
        return None

    major_city = any(zip_str.startswith(prefix) for prefix in MAJOR_CITY_ZIP_PREFIXES)
    return tier, major_city


def main():
    zip_files = sorted(DATA_DIR.glob("google-maps-scrape-part*.zip"))
    print(f"Found {len(zip_files)} zip files")

    results = []
    total_rows = 0

    for zf_path in zip_files:
        print(f"Processing {zf_path.name}...", end=" ", flush=True)
        count_before = len(results)
        with zipfile.ZipFile(zf_path, "r") as zf:
            csv_name = zf_path.stem + ".csv"
            with zf.open(csv_name) as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", errors="replace"))
                for row in reader:
                    total_rows += 1
                    result = classify_row(
                        row.get("title", ""),
                        row.get("category_titles", ""),
                        row.get("zip_code", ""),
                    )
                    if result:
                        tier, major_city = result
                        results.append({
                            "title": row.get("title", ""),
                            "link": row.get("link", ""),
                            "phone": row.get("phone", ""),
                            "category_titles": row.get("category_titles", ""),
                            "zip_code": row.get("zip_code", ""),
                            "normalized_display_link": row.get("normalized_display_link", ""),
                            "relevance_tier": tier,
                            "major_city": major_city,
                        })
        print(f"+{len(results) - count_before} matches")

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["title", "link", "phone", "category_titles", "zip_code",
                  "normalized_display_link", "relevance_tier", "major_city"]
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Total rows scanned: {total_rows:,}")
    print(f"Total matches: {len(results):,}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"\n--- Breakdown by tier ---")
    tier_counts = {}
    for r in results:
        tier_counts[r["relevance_tier"]] = tier_counts.get(r["relevance_tier"], 0) + 1
    for tier, count in sorted(tier_counts.items()):
        print(f"  {tier}: {count:,}")

    print(f"\n--- Breakdown by major_city ---")
    mc_true = sum(1 for r in results if r["major_city"])
    mc_false = len(results) - mc_true
    print(f"  major_city=True:  {mc_true:,}")
    print(f"  major_city=False: {mc_false:,}")

    print(f"\n--- Major city leads by tier ---")
    mc_tier = {}
    for r in results:
        if r["major_city"]:
            mc_tier[r["relevance_tier"]] = mc_tier.get(r["relevance_tier"], 0) + 1
    for tier, count in sorted(mc_tier.items()):
        print(f"  {tier}: {count:,}")


if __name__ == "__main__":
    main()
