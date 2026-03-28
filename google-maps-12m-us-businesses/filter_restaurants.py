"""Filter 12M Google Maps businesses down to restaurants & bars using 481 category keys."""

import csv
import io
import os
import zipfile
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load categories from the markdown file
def load_categories(md_path):
    cats = set()
    with open(md_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                cats.add(line[2:].strip().lower())
    return cats

# Parse the category_titles field: "['Restaurant', 'Pizza restaurant']"
def parse_categories(raw):
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    # Remove brackets
    raw = raw.strip("[]")
    # Split on comma, strip quotes and whitespace
    return [c.strip().strip("'\"") for c in raw.split(",") if c.strip()]

def main():
    categories = load_categories(os.path.join(SCRIPT_DIR, "category_keys.md"))
    print(f"Loaded {len(categories)} target categories")

    output_dir = os.path.join(SCRIPT_DIR, "filtered")
    os.makedirs(output_dir, exist_ok=True)

    ROWS_PER_FILE = 510_300
    header = ["title", "link", "phone", "category_titles", "zip_code", "normalized_display_link"]

    total_matched = 0
    total_scanned = 0
    file_num = 1
    current_writer = None
    current_file = None
    rows_in_current = 0

    def open_new_file():
        nonlocal current_writer, current_file, rows_in_current, file_num
        if current_file:
            current_file.close()
        path = os.path.join(output_dir, f"restaurants_bars_part{file_num}.csv")
        current_file = open(path, "w", newline="", encoding="utf-8")
        current_writer = csv.writer(current_file)
        current_writer.writerow(header)
        rows_in_current = 0
        print(f"  Writing to restaurants_bars_part{file_num}.csv")
        file_num += 1

    open_new_file()

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
                    if len(row) < 4:
                        continue
                    row_cats = parse_categories(row[3])
                    if any(c.lower() in categories for c in row_cats):
                        current_writer.writerow(row)
                        total_matched += 1
                        rows_in_current += 1
                        if rows_in_current >= ROWS_PER_FILE:
                            open_new_file()

        print(f"  Running total: {total_matched:,} matched / {total_scanned:,} scanned ({total_matched/total_scanned*100:.1f}%)")

    if current_file:
        current_file.close()

    print(f"\nDone! {total_matched:,} restaurants & bars out of {total_scanned:,} businesses ({total_matched/total_scanned*100:.1f}%)")
    print(f"Output: {file_num - 1} file(s) in {output_dir}/")

if __name__ == "__main__":
    main()
