"""Filter 12M Google Maps US businesses for ForgeBee grower/bee/research leads."""

import csv
import io
import os
import re
import zipfile

DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "google-maps-12m-us-businesses",
)
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Category sets (lowercase) ---
CORE_FARM_CATEGORIES = {
    "farm", "organic farm", "dairy farm",
    "agricultural service", "agricultural production",
    "agricultural cooperative", "agriculture",
}

BEE_HONEY_CATEGORIES = {
    "honey farm", "bee relocation service",
}

RESEARCH_CATEGORIES = {
    "college of agriculture", "university",
    "agricultural high school", "agricultural organization",
    "agricultural association",
}

ALL_TARGET_CATEGORIES = CORE_FARM_CATEGORIES | BEE_HONEY_CATEGORIES | RESEARCH_CATEGORIES

# --- Name keywords (compiled regex, case-insensitive) ---
NAME_KEYWORDS = [
    "almond", "berry", "blueberry", "cherry", "apple", "orchard",
    "melon", "pollination", "bee", "honey", "apiary", "apiaries",
    "seed", "nursery", "grove",
]
NAME_RE = re.compile(r"\b(?:" + "|".join(NAME_KEYWORDS) + r")\b", re.IGNORECASE)

# --- CA Central Valley zip prefixes ---
CA_CENTRAL_VALLEY_PREFIXES = (
    "930", "931", "932", "933", "934", "935", "936", "937", "938", "939",
    "950", "951", "952", "953",
    "956", "957", "958",
)


def parse_categories(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    raw = raw.strip("[]")
    return [c.strip().strip("'\"") for c in raw.split(",") if c.strip()]


def classify_row(row: list[str]) -> str | None:
    """Return relevance_tier or None if not a match."""
    if len(row) < 4:
        return None

    cats_raw = row[3]
    cats = [c.lower() for c in parse_categories(cats_raw)]

    # Check bee/honey first (more specific)
    if any(c in BEE_HONEY_CATEGORIES for c in cats):
        return "bee_honey"

    # Research
    if any(c in RESEARCH_CATEGORIES for c in cats):
        return "research"

    # Core farm
    if any(c in CORE_FARM_CATEGORIES for c in cats):
        return "core_farm"

    # Name keyword match (title is column 0)
    title = row[0] if row[0] else ""
    if NAME_RE.search(title):
        return "name_match"

    return None


def is_ca_central_valley(zip_code: str) -> bool:
    z = zip_code.strip() if zip_code else ""
    return z.startswith(CA_CENTRAL_VALLEY_PREFIXES)


def main():
    header_out = [
        "title", "link", "phone", "category_titles",
        "zip_code", "normalized_display_link",
        "relevance_tier", "ca_central_valley",
    ]

    results = []
    total_scanned = 0
    tier_counts = {}
    ca_cv_count = 0

    for i in range(1, 14):
        zip_path = os.path.join(DATA_DIR, f"google-maps-scrape-part{i}.zip")
        if not os.path.exists(zip_path):
            print(f"Skipping part{i} (not found)")
            continue

        print(f"Processing part{i}...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            csv_name = zf.namelist()[0]
            with zf.open(csv_name) as f:
                reader = csv.reader(
                    io.TextIOWrapper(f, encoding="utf-8", errors="replace")
                )
                next(reader)  # skip header
                for row in reader:
                    total_scanned += 1
                    tier = classify_row(row)
                    if tier is None:
                        continue

                    zip_code = row[4] if len(row) > 4 else ""
                    ca_cv = is_ca_central_valley(zip_code)
                    if ca_cv:
                        ca_cv_count += 1

                    # Pad row to 6 columns if needed
                    while len(row) < 6:
                        row.append("")

                    results.append(row[:6] + [tier, str(ca_cv).lower()])
                    tier_counts[tier] = tier_counts.get(tier, 0) + 1

        print(f"  Running: {len(results):,} matched / {total_scanned:,} scanned")

    # Write output
    out_path = os.path.join(OUTPUT_DIR, "grower_leads_national.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header_out)
        writer.writerows(results)

    # Summary
    print(f"\nDone! {len(results):,} leads from {total_scanned:,} businesses")
    print(f"Output: {out_path}\n")
    print("Breakdown by tier:")
    for tier in ["core_farm", "bee_honey", "research", "name_match"]:
        print(f"  {tier}: {tier_counts.get(tier, 0):,}")
    print(f"\nCA Central Valley leads: {ca_cv_count:,} / {len(results):,}")


if __name__ == "__main__":
    main()
