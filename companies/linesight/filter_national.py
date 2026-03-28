"""Filter 12M Google Maps US businesses for LineSight ICP: steel/metal service centers nationally."""

import csv
import io
import os
import zipfile

DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "google-maps-12m-us-businesses",
)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Category definitions ---

CORE_CATEGORIES = {
    "steel fabricator",
    "steel distributor",
    "steel construction company",
    "metal fabricator",
    "metal supplier",
    "sheet metal contractor",
    "iron steel contractor",
    "metal processing company",
    "metal finisher",
}

SECONDARY_CATEGORIES = {
    "metal workshop",
    "metal working shop",
    "machine shop",
    "machining manufacturer",
    "welder",
    "welding service",
    "laser cutting service",
    "metal stamping service",
    "steel supplier",
    "iron works",
    "iron foundry",
    "foundry",
    "steel mill",
    "metal rolling mill",
    "pipe supplier",
}

EXCLUDE_CATEGORIES = {
    "scrap metal dealer",
    "metal polishing service",
    "metal detecting equipment supplier",
}


def parse_categories(raw):
    """Parse the category_titles string like "['Steel fabricator', 'Metal supplier']"."""
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    raw = raw.strip("[]")
    return [c.strip().strip("'\"") for c in raw.split(",") if c.strip()]


def classify_row(row_cats):
    """Return 'core', 'secondary', or None based on categories.

    Excludes rows that match any exclusion category, even if they also match core/secondary.
    """
    lower_cats = [c.lower() for c in row_cats]

    # Check exclusions first
    if any(c in EXCLUDE_CATEGORIES for c in lower_cats):
        return None

    if any(c in CORE_CATEGORIES for c in lower_cats):
        return "core"

    if any(c in SECONDARY_CATEGORIES for c in lower_cats):
        return "secondary"

    return None


def main():
    output_path = os.path.join(OUTPUT_DIR, "linesight_leads_national.csv")

    header = [
        "title",
        "link",
        "phone",
        "category_titles",
        "zip_code",
        "normalized_display_link",
        "relevance_tier",
    ]

    counts = {"core": 0, "secondary": 0}
    total_scanned = 0

    with open(output_path, "w", newline="", encoding="utf-8") as outf:
        writer = csv.writer(outf)
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
                    reader = csv.reader(
                        io.TextIOWrapper(f, encoding="utf-8", errors="replace")
                    )
                    next(reader)  # skip header
                    for row in reader:
                        total_scanned += 1
                        if len(row) < 5:
                            continue

                        row_cats = parse_categories(row[3])
                        tier = classify_row(row_cats)
                        if tier is not None:
                            writer.writerow(row + [tier])
                            counts[tier] += 1

            total_matched = counts["core"] + counts["secondary"]
            print(
                f"  Running total: {total_matched:,} leads "
                f"(core={counts['core']:,}, secondary={counts['secondary']:,}) "
                f"/ {total_scanned:,} scanned"
            )

    total_matched = counts["core"] + counts["secondary"]
    print(f"\n{'='*60}")
    print(f"LineSight National Lead Filter Complete")
    print(f"{'='*60}")
    print(f"Total scanned:    {total_scanned:,}")
    print(f"Total leads:      {total_matched:,}")
    print(f"  Core tier:      {counts['core']:,}")
    print(f"  Secondary tier: {counts['secondary']:,}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
