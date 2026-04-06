"""
Enrich dcdx beauty industry contacts: fill in missing Company and Role fields.

Strategy:
1. Extract company name from email domain (domain -> company name mapping).
2. For corporate domains, look up the company via Apollo org enrich.
3. For contacts with a corporate email, look up their role via Apollo people match.
4. Skip gmail.com, outlook.com, icloud.com, etc. (can't infer company from domain).

Input:  Beauty Industry Contacts.numbers (455 contacts)
Output: dcdx_contacts_enriched.csv

Requires: APOLLO_API_KEY in environment or .env file.
"""

import csv
import os
import sys
import time
from typing import Optional

import httpx

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
NUMBERS_PATH = os.path.join(REPO_ROOT, "Beauty Industry Contacts.numbers")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "dcdx_contacts_enriched.csv")

# Freemail / webmail domains where we can't infer the company
FREEMAIL_DOMAINS = {
    "gmail.com", "googlemail.com", "outlook.com", "hotmail.com",
    "yahoo.com", "yahoo.co.uk", "icloud.com", "me.com", "mac.com",
    "aol.com", "protonmail.com", "proton.me", "live.com", "msn.com",
    "mail.com", "zoho.com", "yandex.com", "qq.com", "163.com",
    "126.com", "yeah.net", "foxmail.com",
}

APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY", "")
APOLLO_BASE = "https://api.apollo.io/api/v1"

# Rate limiting: Apollo free tier = 50 req/min
APOLLO_DELAY = 1.5  # seconds between requests


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_contacts_from_numbers(path: str) -> list[dict]:
    """Read the .numbers file and return list of contact dicts."""
    try:
        import numbers_parser
    except ImportError:
        print("ERROR: numbers-parser not installed. Run: pip3 install numbers-parser")
        sys.exit(1)

    doc = numbers_parser.Document(path)
    # The contacts are in the second sheet ("Beauty Contacts")
    sheet = doc.sheets[1]
    table = sheet.tables[0]

    headers = []
    for col in range(table.num_cols):
        cell = table.cell(0, col)
        headers.append(str(cell.value).strip() if cell.value else f"col_{col}")

    contacts = []
    for row in range(1, table.num_rows):
        record = {}
        for col in range(table.num_cols):
            cell = table.cell(row, col)
            val = str(cell.value).strip() if cell.value is not None else ""
            record[headers[col]] = val
        if record.get("Email"):
            contacts.append(record)

    return contacts


def domain_from_email(email: str) -> str:
    """Extract domain from email address."""
    if "@" in email:
        return email.split("@")[1].lower()
    return ""


def is_corporate_email(email: str) -> bool:
    """Check if email is from a corporate domain (not freemail)."""
    domain = domain_from_email(email)
    return bool(domain) and domain not in FREEMAIL_DOMAINS


def company_name_from_domain(domain: str) -> str:
    """Guess a company name from domain (strip TLD, title-case)."""
    # e.g. "loreal.com" -> "Loreal", "elfbeauty.com" -> "Elfbeauty"
    parts = domain.split(".")
    if len(parts) >= 2:
        name = parts[-2]  # second-level domain
    else:
        name = parts[0]
    return name.replace("-", " ").replace("_", " ").title()


# ---------------------------------------------------------------------------
# Apollo API
# ---------------------------------------------------------------------------

def apollo_enrich_org(domain: str) -> Optional[dict]:
    """Enrich a company by domain via Apollo. Returns org data or None."""
    if not APOLLO_API_KEY:
        return None
    try:
        resp = httpx.post(
            f"{APOLLO_BASE}/organizations/enrich",
            headers={"Content-Type": "application/json", "X-Api-Key": APOLLO_API_KEY},
            json={"domain": domain},
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json()
            org = data.get("organization")
            if org:
                return {
                    "name": org.get("name", ""),
                    "industry": org.get("industry", ""),
                    "estimated_num_employees": org.get("estimated_num_employees"),
                    "linkedin_url": org.get("linkedin_url", ""),
                }
        return None
    except Exception as e:
        print(f"    Apollo org error for {domain}: {e}")
        return None


def apollo_people_match(first_name: str, last_name: str, domain: str) -> Optional[dict]:
    """Look up a person by name + domain via Apollo. Returns person data or None."""
    if not APOLLO_API_KEY:
        return None
    try:
        resp = httpx.post(
            f"{APOLLO_BASE}/people/match",
            headers={"Content-Type": "application/json", "X-Api-Key": APOLLO_API_KEY},
            json={"first_name": first_name, "last_name": last_name, "domain": domain},
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json()
            person = data.get("person")
            if person:
                return {
                    "title": person.get("title", ""),
                    "linkedin_url": person.get("linkedin_url", ""),
                    "company": person.get("organization", {}).get("name", ""),
                }
        return None
    except Exception as e:
        print(f"    Apollo people error for {first_name} {last_name} @ {domain}: {e}")
        return None


def split_name(full_name: str) -> tuple[str, str]:
    """Split a full name into first and last. Handles edge cases."""
    parts = full_name.strip().split()
    if len(parts) == 0:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Loading contacts from: {NUMBERS_PATH}")
    contacts = load_contacts_from_numbers(NUMBERS_PATH)
    print(f"Loaded {len(contacts)} contacts")

    # Count initial state
    has_company = sum(1 for c in contacts if c.get("Company"))
    has_role = sum(1 for c in contacts if c.get("Role"))
    print(f"Before enrichment: {has_company} have Company, {has_role} have Role")

    # Phase 1: Fill Company from email domain for corporate emails missing Company
    print("\n--- Phase 1: Infer Company from email domain ---")
    domain_cache = {}  # domain -> company name (from Apollo or guess)
    filled_company = 0

    for contact in contacts:
        if contact.get("Company"):
            continue
        email = contact["Email"]
        if not is_corporate_email(email):
            continue
        domain = domain_from_email(email)
        if domain not in domain_cache:
            domain_cache[domain] = company_name_from_domain(domain)
        contact["Company"] = domain_cache[domain]
        filled_company += 1

    print(f"  Filled {filled_company} Company fields from email domains")

    # Phase 2: Apollo org enrichment for corporate domains (get proper company names)
    if APOLLO_API_KEY:
        print("\n--- Phase 2: Apollo org enrichment (proper company names) ---")
        unique_domains = set()
        for c in contacts:
            email = c["Email"]
            if is_corporate_email(email):
                unique_domains.add(domain_from_email(email))

        print(f"  {len(unique_domains)} unique corporate domains to enrich")
        apollo_org_cache = {}
        enriched_orgs = 0

        for i, domain in enumerate(sorted(unique_domains)):
            if domain in apollo_org_cache:
                continue
            print(f"  [{i+1}/{len(unique_domains)}] {domain}...", end=" ")
            org = apollo_enrich_org(domain)
            if org and org["name"]:
                apollo_org_cache[domain] = org["name"]
                enriched_orgs += 1
                print(f"-> {org['name']}")
            else:
                apollo_org_cache[domain] = None
                print("not found")
            time.sleep(APOLLO_DELAY)

        # Apply Apollo company names (overwrite domain guesses with proper names)
        for contact in contacts:
            domain = domain_from_email(contact["Email"])
            if domain in apollo_org_cache and apollo_org_cache[domain]:
                contact["Company"] = apollo_org_cache[domain]

        print(f"  Enriched {enriched_orgs} company names from Apollo")

        # Phase 3: Apollo people match for missing roles
        print("\n--- Phase 3: Apollo people match (fill missing Roles) ---")
        needs_role = [c for c in contacts if not c.get("Role") and is_corporate_email(c["Email"]) and c.get("Name")]
        print(f"  {len(needs_role)} contacts need Role lookup")
        filled_roles = 0

        for i, contact in enumerate(needs_role):
            first, last = split_name(contact["Name"])
            if not first:
                continue
            domain = domain_from_email(contact["Email"])
            print(f"  [{i+1}/{len(needs_role)}] {first} {last} @ {domain}...", end=" ")
            person = apollo_people_match(first, last, domain)
            if person and person["title"]:
                contact["Role"] = person["title"]
                if person.get("linkedin_url"):
                    contact["LinkedIn"] = person["linkedin_url"]
                filled_roles += 1
                print(f"-> {person['title']}")
            else:
                print("not found")
            time.sleep(APOLLO_DELAY)

        print(f"  Filled {filled_roles} Roles from Apollo")
    else:
        print("\nAPOLLO_API_KEY not set. Skipping Apollo enrichment.")
        print("Set APOLLO_API_KEY in your environment or .env file for full enrichment.")

    # Final stats
    has_company_after = sum(1 for c in contacts if c.get("Company"))
    has_role_after = sum(1 for c in contacts if c.get("Role"))
    print(f"\n{'='*60}")
    print(f"ENRICHMENT COMPLETE")
    print(f"  Company: {has_company} -> {has_company_after} ({has_company_after - has_company} new)")
    print(f"  Role:    {has_role} -> {has_role_after} ({has_role_after - has_role} new)")
    print(f"{'='*60}")

    # Write output CSV
    fieldnames = ["Email", "Name", "Company", "Role", "Category", "Confidence",
                  "Reasoning", "Sources", "LinkedIn"]
    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(contacts)

    print(f"\nSaved to: {OUTPUT_PATH}")

    # Print a sample of enriched contacts
    print(f"\n--- Sample enriched contacts ---")
    enriched = [c for c in contacts if c.get("Company") and c.get("Role")]
    for c in enriched[:15]:
        print(f"  {c['Name']:<25} | {c['Company']:<25} | {c['Role']:<35} | {c['Email']}")


if __name__ == "__main__":
    main()
