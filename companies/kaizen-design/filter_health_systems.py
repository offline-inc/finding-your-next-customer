"""
Filter 12M Google Maps US businesses to find hospital/health system facilities
and architecture/construction firms for Kaizen Design ICP.

Outputs:
1. hospital_facilities_national.csv - all matching facilities
2. health_systems_by_domain.csv - grouped by website domain, sorted by facility count
"""

import csv
import io
import os
import zipfile
from collections import defaultdict

DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "google-maps-12m-us-businesses",
)
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Categories to match (lowercased for comparison)
CORE_CATEGORIES = {
    "hospital",
    "general hospital",
    "veterans hospital",
    "children's hospital",
    "heart hospital",
    "university hospital",
    "military hospital",
    "maternity hospital",
    "specialized hospital",
    "psychiatric hospital",
    "private hospital",
    "government hospital",
}

SECONDARY_CATEGORIES = {
    "hospital department",
    "medical center",
    "health care facility",
}

TERTIARY_CATEGORIES = {
    "general contractor",
    "architect",
    "construction company",
}

ALL_CATEGORIES = CORE_CATEGORIES | SECONDARY_CATEGORIES | TERTIARY_CATEGORIES

HEADER = ["title", "link", "phone", "category_titles", "zip_code", "normalized_display_link"]


def parse_categories(raw):
    """Parse category_titles field like \"['Hospital', 'Medical Center']\" """
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    raw = raw.strip("[]")
    return [c.strip().strip("'\"") for c in raw.split(",") if c.strip()]


def classify_row(row_cats):
    """Return the tier of the match: 'core', 'secondary', 'tertiary', or None."""
    lowered = [c.lower() for c in row_cats]
    if any(c in CORE_CATEGORIES for c in lowered):
        return "core"
    if any(c in SECONDARY_CATEGORIES for c in lowered):
        return "secondary"
    if any(c in TERTIARY_CATEGORIES for c in lowered):
        return "tertiary"
    return None


def main():
    print(f"Data dir: {DATA_DIR}")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"Target categories: {len(ALL_CATEGORIES)}")
    print()

    # Collect all matching rows
    all_facilities = []
    total_scanned = 0
    tier_counts = defaultdict(int)

    for i in range(1, 14):
        zip_path = os.path.join(DATA_DIR, f"google-maps-scrape-part{i}.zip")
        if not os.path.exists(zip_path):
            print(f"Skipping part{i} (not found)")
            continue

        print(f"Processing part{i}...", end=" ", flush=True)
        part_matched = 0
        with zipfile.ZipFile(zip_path, "r") as zf:
            csv_name = zf.namelist()[0]
            with zf.open(csv_name) as f:
                reader = csv.reader(io.TextIOWrapper(f, encoding="utf-8", errors="replace"))
                next(reader)  # skip header
                for row in reader:
                    total_scanned += 1
                    if len(row) < 4:
                        continue
                    row_cats = parse_categories(row[3])
                    tier = classify_row(row_cats)
                    if tier:
                        tier_counts[tier] += 1
                        part_matched += 1
                        all_facilities.append(row)

        print(f"{part_matched:,} matched (running total: {len(all_facilities):,} / {total_scanned:,})")

    print(f"\nTotal scanned: {total_scanned:,}")
    print(f"Total matched: {len(all_facilities):,}")
    for tier in ["core", "secondary", "tertiary"]:
        print(f"  {tier}: {tier_counts[tier]:,}")

    # Write facility-level CSV
    facilities_path = os.path.join(OUTPUT_DIR, "hospital_facilities_national.csv")
    with open(facilities_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER + ["tier"])
        for row in all_facilities:
            row_cats = parse_categories(row[3])
            tier = classify_row(row_cats)
            writer.writerow(row + [tier])

    print(f"\nWrote {len(all_facilities):,} facilities to {facilities_path}")

    # Group by domain (normalized_display_link)
    domain_data = defaultdict(lambda: {"names": [], "zip_codes": set(), "count": 0, "tiers": defaultdict(int)})

    for row in all_facilities:
        domain = row[5].strip() if len(row) > 5 else ""
        if not domain:
            domain = "(no website)"
        row_cats = parse_categories(row[3])
        tier = classify_row(row_cats)
        d = domain_data[domain]
        d["count"] += 1
        d["tiers"][tier] += 1
        if len(d["names"]) < 3:
            d["names"].append(row[0])
        zip_code = row[4].strip() if len(row) > 4 else ""
        if zip_code:
            d["zip_codes"].add(zip_code)

    # Filter to domains with 3+ facilities, sort descending
    qualified_domains = [
        (domain, data) for domain, data in domain_data.items() if data["count"] >= 3
    ]
    qualified_domains.sort(key=lambda x: x[1]["count"], reverse=True)

    domains_path = os.path.join(OUTPUT_DIR, "health_systems_by_domain.csv")
    with open(domains_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "facility_count", "core_count", "secondary_count", "tertiary_count", "sample_names", "zip_codes"])
        for domain, data in qualified_domains:
            writer.writerow([
                domain,
                data["count"],
                data["tiers"].get("core", 0),
                data["tiers"].get("secondary", 0),
                data["tiers"].get("tertiary", 0),
                " | ".join(data["names"]),
                " | ".join(sorted(data["zip_codes"])[:20]),  # cap at 20 zips
            ])

    print(f"Wrote {len(qualified_domains):,} domains (3+ facilities) to {domains_path}")

    # Summary stats
    total_domains = len(domain_data)
    domains_10_plus = sum(1 for d, data in domain_data.items() if data["count"] >= 10)
    # Filter to only core+secondary for health system signal
    health_domains_10_plus = sum(
        1 for d, data in domain_data.items()
        if (data["tiers"].get("core", 0) + data["tiers"].get("secondary", 0)) >= 10
    )

    print(f"\n--- Summary ---")
    print(f"Total facilities matched: {len(all_facilities):,}")
    print(f"Total unique domains: {total_domains:,}")
    print(f"Domains with 3+ facilities: {len(qualified_domains):,}")
    print(f"Domains with 10+ facilities (all tiers): {domains_10_plus:,}")
    print(f"Domains with 10+ hospital/medical facilities (core+secondary only): {health_domains_10_plus:,}")

    # Print top 20 domains
    print(f"\n--- Top 20 Domains by Facility Count ---")
    for domain, data in qualified_domains[:20]:
        core_sec = data["tiers"].get("core", 0) + data["tiers"].get("secondary", 0)
        print(f"  {data['count']:4d} facilities ({core_sec} hospital/medical) - {domain}")
        print(f"       e.g. {' | '.join(data['names'][:2])}")


if __name__ == "__main__":
    main()
