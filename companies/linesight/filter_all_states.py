"""
Filter 12M Google Maps businesses for metal service centers across all US states.
Outputs:
  - linesight_leads_national.csv  — all leads, all tiers, all states
  - linesight_leads_by_state/     — one CSV per state
  - linesight_summary.txt         — count breakdown by state and tier
"""

import csv
import io
import os
import zipfile
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(SCRIPT_DIR, "..", "google-maps-12m-us-businesses")
OUTPUT_DIR = SCRIPT_DIR
BY_STATE_DIR = os.path.join(OUTPUT_DIR, "by_state")
os.makedirs(BY_STATE_DIR, exist_ok=True)

# ---------------------------------------------------------
# US state zip code prefix ranges
# ---------------------------------------------------------
STATE_ZIP_RANGES = {
    "AL": [(350, 370)],
    "AK": [(995, 999)],
    "AZ": [(850, 865)],
    "AR": [(716, 729)],
    "CA": [(900, 961)],
    "CO": [(800, 816)],
    "CT": [(60, 69)],
    "DE": [(197, 199)],
    "FL": [(320, 349)],
    "GA": [(300, 319)],
    "HI": [(967, 968)],
    "ID": [(832, 838)],
    "IL": [(600, 629)],
    "IN": [(460, 479)],
    "IA": [(500, 528)],
    "KS": [(660, 679)],
    "KY": [(400, 427)],
    "LA": [(700, 714)],
    "ME": [(39, 49)],
    "MD": [(206, 219)],
    "MA": [(10, 27)],
    "MI": [(480, 499)],
    "MN": [(550, 567)],
    "MS": [(386, 397)],
    "MO": [(630, 659)],
    "MT": [(590, 599)],
    "NE": [(680, 693)],
    "NV": [(889, 898)],
    "NH": [(30, 38)],
    "NJ": [(70, 89)],
    "NM": [(870, 884)],
    "NY": [(100, 149)],
    "NC": [(270, 289)],
    "ND": [(580, 588)],
    "OH": [(430, 459)],
    "OK": [(730, 749)],
    "OR": [(970, 979)],
    "PA": [(150, 196)],
    "RI": [(28, 29)],
    "SC": [(290, 299)],
    "SD": [(570, 577)],
    "TN": [(370, 385)],
    "TX": [(750, 799)],
    "UT": [(840, 847)],
    "VT": [(50, 59)],
    "VA": [(220, 246)],
    "WA": [(980, 994)],
    "WV": [(247, 268)],
    "WI": [(530, 549)],
    "WY": [(820, 831)],
    "DC": [(200, 205)],
    "PR": [(900, 988)],  # rough — will overlap CA but Puerto Rico businesses are distinct
}

def zip_to_state(zip_str):
    """Map a zip code string to a US state abbreviation, or None."""
    z = zip_str.strip().split(".")[0].zfill(5)
    try:
        prefix = int(z[:3])
    except ValueError:
        return None
    for state, ranges in STATE_ZIP_RANGES.items():
        for lo, hi in ranges:
            if lo <= prefix <= hi:
                return state
    return None


def parse_cats(raw):
    raw = raw.strip("[]")
    return [c.strip().strip("'\"").lower() for c in raw.split(",") if c.strip()]


# ---------------------------------------------------------
# Tier logic (same as IL analysis, generalized)
# ---------------------------------------------------------
DISTRIBUTOR_CATS = {"steel distributor"}

SUPPLIER_CATS = {"metal supplier", "aluminum supplier", "stainless steel plant"}
SUPPLIER_EXCLUDE = {"scrap metal dealer", "junkyard", "recycling center"}

MILL_CATS = {"steel mill", "foundry", "iron foundry", "metal rolling mill"}

NAME_SIGNALS = [
    "steel service", "metal service", "service center",
    "steel center", "metals center",
    "steel supply", "metal supply", "metals supply",
    "steel & supply", "metal & supply",
    "steel inc", "metals inc", "metals llc", "metals corp",
    "steel llc", "steel corp",
    "coil", "slit", "flat roll",
    "steel warehouse", "metals warehouse",
    "steel products", "metal products",
]
NAME_MATCH_CATS = {
    "steel fabricator", "metal fabricator", "sheet metal contractor",
    "steel distributor", "metal supplier", "manufacturer",
    "iron steel contractor", "machining manufacturer",
    "industrial equipment supplier", "construction material wholesaler",
    "metal stamping service", "laser cutting service", "metal finisher",
}


def classify_row(row):
    """Return (tier_label, row) or None if not a match."""
    if len(row) < 6:
        return None
    name = row[0].lower()
    cats = parse_cats(row[3])

    if any(c in DISTRIBUTOR_CATS for c in cats):
        return "DISTRIBUTOR"

    if any(c in SUPPLIER_CATS for c in cats) and not any(c in SUPPLIER_EXCLUDE for c in cats):
        return "SUPPLIER"

    if any(c in MILL_CATS for c in cats):
        return "MILL_FOUNDRY"

    if any(s in name for s in NAME_SIGNALS) and any(c in NAME_MATCH_CATS for c in cats):
        return "NAME_MATCH"

    return None


def main():
    header = ["tier", "title", "link", "phone", "category_titles", "zip_code", "normalized_display_link"]

    # Accumulators: state -> tier -> list of rows
    state_data = defaultdict(lambda: defaultdict(list))
    seen_names = defaultdict(set)  # state -> set of names (dedup within state)

    total_scanned = 0
    total_matched = 0

    for i in range(1, 14):
        zip_path = os.path.join(SOURCE_DIR, f"google-maps-scrape-part{i}.zip")
        if not os.path.exists(zip_path):
            print(f"Skipping part{i} (not found)")
            continue

        print(f"Processing part{i}...", flush=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            csv_name = zf.namelist()[0]
            with zf.open(csv_name) as f:
                reader = csv.reader(io.TextIOWrapper(f, encoding="utf-8", errors="replace"))
                next(reader)  # skip header
                for row in reader:
                    total_scanned += 1
                    if len(row) < 6:
                        continue

                    state = zip_to_state(row[4])
                    if not state:
                        continue

                    tier = classify_row(row)
                    if not tier:
                        continue

                    # Dedup by name within state
                    name_key = row[0].strip().lower()
                    if name_key in seen_names[state]:
                        continue
                    seen_names[state].add(name_key)

                    state_data[state][tier].append(row)
                    total_matched += 1

        # Running total
        print(f"  Running: {total_matched:,} matched / {total_scanned:,} scanned", flush=True)

    print(f"\nDone scanning. Writing outputs...", flush=True)

    # ---------------------------------------------------------
    # Write national CSV
    # ---------------------------------------------------------
    national_path = os.path.join(OUTPUT_DIR, "linesight_leads_national.csv")
    with open(national_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["state"] + header)
        for state in sorted(state_data.keys()):
            for tier in ["DISTRIBUTOR", "SUPPLIER", "MILL_FOUNDRY", "NAME_MATCH"]:
                for row in state_data[state][tier]:
                    writer.writerow([state, tier] + row)

    print(f"National CSV: {national_path}", flush=True)

    # ---------------------------------------------------------
    # Write per-state CSVs
    # ---------------------------------------------------------
    for state in sorted(state_data.keys()):
        state_path = os.path.join(BY_STATE_DIR, f"linesight_{state.lower()}.csv")
        with open(state_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for tier in ["DISTRIBUTOR", "SUPPLIER", "MILL_FOUNDRY", "NAME_MATCH"]:
                for row in state_data[state][tier]:
                    writer.writerow([tier] + row)
        count = sum(len(rows) for rows in state_data[state].values())
        print(f"  {state}: {count} leads → {state_path}", flush=True)

    # ---------------------------------------------------------
    # Write summary
    # ---------------------------------------------------------
    summary_path = os.path.join(OUTPUT_DIR, "linesight_summary.txt")
    tier_totals = defaultdict(int)
    with open(summary_path, "w") as f:
        f.write("LineSight Lead Summary — Metal Service Centers (US)\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"{'State':<8} {'DIST':>6} {'SUPP':>6} {'MILL':>6} {'NAME':>6} {'TOTAL':>7}\n")
        f.write("-" * 45 + "\n")

        grand_total = 0
        for state in sorted(state_data.keys()):
            d = len(state_data[state]["DISTRIBUTOR"])
            s = len(state_data[state]["SUPPLIER"])
            m = len(state_data[state]["MILL_FOUNDRY"])
            n = len(state_data[state]["NAME_MATCH"])
            t = d + s + m + n
            grand_total += t
            tier_totals["DISTRIBUTOR"] += d
            tier_totals["SUPPLIER"] += s
            tier_totals["MILL_FOUNDRY"] += m
            tier_totals["NAME_MATCH"] += n
            f.write(f"{state:<8} {d:>6} {s:>6} {m:>6} {n:>6} {t:>7}\n")

        f.write("-" * 45 + "\n")
        f.write(f"{'TOTAL':<8} {tier_totals['DISTRIBUTOR']:>6} {tier_totals['SUPPLIER']:>6} "
                f"{tier_totals['MILL_FOUNDRY']:>6} {tier_totals['NAME_MATCH']:>6} {grand_total:>7}\n\n")
        f.write("Tiers:\n")
        f.write("  DISTRIBUTOR — Google category: 'steel distributor' (highest confidence)\n")
        f.write("  SUPPLIER    — Google category: 'metal supplier' / 'aluminum supplier' (excl. scrap)\n")
        f.write("  MILL_FOUNDRY — Steel mills, foundries, rolling mills\n")
        f.write("  NAME_MATCH  — Metal fabricator/processor with service-center-signaling name\n")

    print(f"\nSummary: {summary_path}", flush=True)
    print(f"\nTotal matched: {total_matched:,} out of {total_scanned:,} scanned", flush=True)


if __name__ == "__main__":
    main()
