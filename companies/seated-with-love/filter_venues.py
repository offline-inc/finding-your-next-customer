"""Filter 12M Google Maps businesses to find wedding/event venue leads for Seated with Love."""

import csv
import io
import os
import re
import zipfile

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "google-maps-12m-us-businesses")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Category tiers (all lowercase for matching)
CORE_CATEGORIES = {
    "wedding venue", "banquet hall", "wedding chapel",
}

SECONDARY_CATEGORIES = {
    "event venue", "wedding service", "conference center",
}

TERTIARY_CATEGORIES = {
    "winery", "brewery", "brewpub", "lodge", "resort hotel",
    "inn", "bed & breakfast", "bed and breakfast",
    "country club", "golf club",
    "vineyard", "boutique hotel", "rooftop bar",
}

# Categories that disqualify a name_match (avoid real estate schools, etc.)
EXCLUDE_CATEGORIES = {
    "real estate school", "real estate agency", "real estate agent",
    "commercial real estate agency", "real estate consultant",
    "real estate attorney", "real estate appraiser",
    "property management company", "real estate developer",
    "insurance agency", "car dealer", "auto repair shop",
    "dental clinic", "dentist", "doctor", "hospital",
    "pharmacy", "veterinarian", "law firm", "attorney",
    "accounting firm", "bank", "credit union",
    "grocery store", "supermarket", "convenience store",
    "gas station", "laundromat", "dry cleaner",
    "storage facility", "moving company",
}

# Name keywords that suggest wedding venue even if category doesn't match.
# "estate" excluded from name match (too many false positives like real estate).
NAME_KEYWORDS = re.compile(
    r"\b(wedding|banquet|ballroom|reception hall|bridal|nuptial)\b",
    re.IGNORECASE,
)


def parse_categories(raw):
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    raw = raw.strip("[]")
    return [c.strip().strip("'\"") for c in raw.split(",") if c.strip()]


def classify(title, raw_categories):
    """Return relevance tier or None if not a match."""
    cats_lower = [c.lower() for c in parse_categories(raw_categories)]

    # Check core first
    for c in cats_lower:
        if c in CORE_CATEGORIES:
            return "core"

    # Check secondary
    for c in cats_lower:
        if c in SECONDARY_CATEGORIES:
            return "secondary"

    # Check tertiary
    for c in cats_lower:
        if c in TERTIARY_CATEGORIES:
            return "tertiary"

    # Check business name keywords (but exclude obviously unrelated businesses)
    if NAME_KEYWORDS.search(title or ""):
        if not any(c in EXCLUDE_CATEGORIES for c in cats_lower):
            return "name_match"

    return None


def main():
    output_path = os.path.join(OUTPUT_DIR, "venue_leads_national.csv")
    header = ["title", "link", "phone", "category_titles", "zip_code", "normalized_display_link", "relevance_tier"]

    tier_counts = {"core": 0, "secondary": 0, "tertiary": 0, "name_match": 0}
    total_scanned = 0
    total_matched = 0

    with open(output_path, "w", newline="", encoding="utf-8") as out_f:
        writer = csv.writer(out_f)
        writer.writerow(header)

        for i in range(1, 14):
            zip_path = os.path.join(DATA_DIR, f"google-maps-scrape-part{i}.zip")
            if not os.path.exists(zip_path):
                print(f"Skipping part{i} (not found)")
                continue

            print(f"Processing part{i}...")
            with zipfile.ZipFile(zip_path, "r") as zf:
                csv_name = zf.namelist()[0]
                with zf.open(csv_name) as f:
                    reader = csv.reader(io.TextIOWrapper(f, encoding="utf-8", errors="replace"))
                    next(reader)  # skip header
                    for row in reader:
                        total_scanned += 1
                        if len(row) < 4:
                            continue
                        title = row[0]
                        raw_cats = row[3]
                        tier = classify(title, raw_cats)
                        if tier:
                            writer.writerow(row + [tier])
                            tier_counts[tier] += 1
                            total_matched += 1

            print(f"  Running: {total_matched:,} matched / {total_scanned:,} scanned")

    print(f"\n{'='*60}")
    print(f"Total: {total_matched:,} venue leads from {total_scanned:,} businesses")
    print(f"{'='*60}")
    for tier, count in tier_counts.items():
        print(f"  {tier:12s}: {count:>8,}")
    print(f"  {'TOTAL':12s}: {total_matched:>8,}")
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
