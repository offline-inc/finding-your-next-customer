"""
Filter 12M Google Maps US businesses for Plexus HardwareOps ICP.

Plexus ICP: Companies shipping software-defined hardware needing telemetry/observability.
Autonomous vehicles, aerospace/satellite, robotics, IoT device fleet operators.

NOTE: Google Maps is NOT the ideal data source for this ICP. Tech companies,
robotics firms, and aerospace companies rarely appear in Google Maps business
listings. This filter will yield a small, low-confidence list.
"""

import csv
import io
import os
import re
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(SCRIPT_DIR)),
    "google-maps-12m-us-businesses",
)

# Categories to match (case-insensitive)
# Tight list: only categories where companies plausibly ship hardware needing telemetry
TARGET_CATEGORIES = {
    "electronics manufacturer",
    "electronic parts supplier",
    "electronics company",
    "robot manufacturer",
    "robotics company",
    "aerospace company",
    "aircraft manufacturer",
    "industrial automation company",
    "automation company",
    "semiconductor manufacturer",
    "sensor manufacturer",
    "circuit board manufacturer",
    "printed circuit board company",
    "electrical equipment manufacturer",
    "satellite communication service",
    "defense contractor",
    "drone shop",
    "drone store",
}

# Name keywords that signal Plexus ICP relevance
NAME_KEYWORDS = re.compile(
    r"\b("
    r"roboti[cx]s?|autonomous|self.driving|unmanned|uav|uas|"
    r"drone|aerospace|satellite|avionics|"
    r"iot|telemetry|sensor[s]?|embedded|"
    r"lidar|radar\s+system|computer\s+vision|"
    r"fleet\s+manage|vehicle\s+telematics|"
    r"edge\s+comput|firmware|fpga|"
    r"hardware.?ops|observability|"
    r"autonomous\s+vehicle|self.driving|"
    r"machine\s+vision|industrial\s+iot|"
    r"smart\s+device|connected\s+device"
    r")\b",
    re.IGNORECASE,
)


def parse_categories(raw):
    """Parse category_titles field: "['Manufacturer', 'Pizza restaurant']" """
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    raw = raw.strip("[]")
    return [c.strip().strip("'\"") for c in raw.split(",") if c.strip()]


def main():
    output_path = os.path.join(SCRIPT_DIR, "hardware_leads_national.csv")
    header = [
        "title", "link", "phone", "category_titles",
        "zip_code", "normalized_display_link", "match_type",
    ]

    total_scanned = 0
    total_matched = 0
    category_matches = 0
    name_matches = 0

    with open(output_path, "w", newline="", encoding="utf-8") as out_f:
        writer = csv.writer(out_f)
        writer.writerow(header)

        for part_num in range(1, 14):
            zip_name = f"google-maps-scrape-part{part_num}.zip"
            zip_path = os.path.join(DATA_DIR, zip_name)
            if not os.path.exists(zip_path):
                print(f"  Skipping {zip_name} (not found)")
                continue

            print(f"Processing {zip_name}...")
            with zipfile.ZipFile(zip_path, "r") as zf:
                for csv_name in zf.namelist():
                    if not csv_name.endswith(".csv"):
                        continue
                    with zf.open(csv_name) as raw:
                        text_stream = io.TextIOWrapper(raw, encoding="utf-8", errors="replace")
                        reader = csv.DictReader(text_stream)
                        for row in reader:
                            total_scanned += 1
                            title = row.get("title", "")
                            cats = parse_categories(row.get("category_titles", ""))
                            cats_lower = {c.lower() for c in cats}

                            match_type = None

                            # Check category match
                            if cats_lower & TARGET_CATEGORIES:
                                match_type = "category"

                            # Check name keyword match
                            if NAME_KEYWORDS.search(title):
                                match_type = "name_match" if match_type is None else "category+name"

                            if match_type:
                                writer.writerow([
                                    title,
                                    row.get("link", ""),
                                    row.get("phone", ""),
                                    row.get("category_titles", ""),
                                    row.get("zip_code", ""),
                                    row.get("normalized_display_link", ""),
                                    match_type,
                                ])
                                total_matched += 1
                                if "category" in match_type:
                                    category_matches += 1
                                if "name" in match_type:
                                    name_matches += 1

            print(f"  Running total: {total_matched:,} matches from {total_scanned:,} scanned")

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Total scanned:    {total_scanned:,}")
    print(f"Total matched:    {total_matched:,}")
    print(f"  Category match: {category_matches:,}")
    print(f"  Name match:     {name_matches:,}")
    print(f"\nOutput: {output_path}")
    print(f"\n{'='*60}")
    print(f"NOTE: Google Maps is NOT the right data source for the Plexus ICP.")
    print(f"Companies building software-defined hardware (autonomous vehicles,")
    print(f"aerospace, robotics, IoT fleet operators) rarely have Google Maps")
    print(f"listings. This list is low-confidence and should be supplemented with:")
    print(f"  1. LinkedIn Sales Navigator (search by job title + company type)")
    print(f"  2. Crunchbase (filter by industry: robotics, aerospace, IoT)")
    print(f"  3. GitHub (search repos for hardware telemetry, device management)")
    print(f"  4. PitchBook / AngelList for funded startups in these verticals")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
