"""Filter 12M Google Maps businesses for metal service centers in Illinois."""

import csv
import io
import os
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Illinois zip codes start with 600-629
IL_ZIP_PREFIXES = tuple(str(i) for i in range(600, 630))

# Categories relevant to metal service centers (LineSight's ICP)
METAL_CATEGORIES = {
    # Core metal service center categories
    "steel distributor",
    "steel fabricator",
    "steel erector",
    "steel construction company",
    "metal construction company",
    "metal fabricator",
    "metal supplier",
    "metal finisher",
    "sheet metal contractor",
    "iron steel contractor",
    # Processing / fabrication
    "metal workshop",
    "metal working shop",
    "machining manufacturer",
    "machine shop",
    "aluminum welder",
    "welder",
    "welding service",
    "laser cutting service",
    "plasma cutting service",
    "metal stamping service",
    # Supply / distribution
    "steel supplier",
    "metal distributor",
    "aluminum supplier",
    "stainless steel plant",
    "iron works",
    "iron foundry",
    "foundry",
    "steel mill",
    "metal rolling mill",
    # Related industrial
    "industrial equipment supplier",
    "manufacturer",
    "construction material wholesaler",
    "building materials supplier",
    "powder coating service",
    "plating service",
    "metal polishing service",
    "sandblasting service",
    "scrap metal dealer",
    "pipe supplier",
    "tube supplier",
}


def parse_categories(raw):
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    raw = raw.strip("[]")
    return [c.strip().strip("'\"") for c in raw.split(",") if c.strip()]


def is_il_zip(zip_code):
    """Check if zip code is in Illinois (600xx-629xx)."""
    z = str(zip_code).strip().split(".")[0]  # handle float zips like "60601.0"
    return any(z.startswith(p) for p in IL_ZIP_PREFIXES)


def main():
    output_path = os.path.join(SCRIPT_DIR, "filtered", "metal_service_centers_il.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    header = ["title", "link", "phone", "category_titles", "zip_code", "normalized_display_link"]

    total_matched = 0
    total_scanned = 0

    with open(output_path, "w", newline="", encoding="utf-8") as outf:
        writer = csv.writer(outf)
        writer.writerow(header)

        for i in range(1, 14):
            zip_path = os.path.join(SCRIPT_DIR, f"google-maps-scrape-part{i}.zip")
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
                        if len(row) < 5:
                            continue

                        zip_code = row[4]
                        if not is_il_zip(zip_code):
                            continue

                        row_cats = parse_categories(row[3])
                        if any(c.lower() in METAL_CATEGORIES for c in row_cats):
                            writer.writerow(row)
                            total_matched += 1

            print(f"  Running: {total_matched} IL metal businesses / {total_scanned:,} scanned")

    print(f"\nDone! {total_matched} metal service center leads in IL out of {total_scanned:,} businesses")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
