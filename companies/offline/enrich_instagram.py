"""
Second pass: visit run club websites to extract Instagram handles,
then look up follower counts via SerpAPI.
"""

import json
import os
import re
import time
from urllib.parse import urlparse

import httpx

SERPAPI_KEY = os.environ["SERPAPI_KEY"]
SERPAPI_BASE_URL = "https://serpapi.com/search.json"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "run_clubs_ranked.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "run_clubs_enriched.json")

# Skip aggregator/directory URLs - we want actual club websites
SKIP_DOMAINS = {
    "reddit.com", "yelp.com", "facebook.com", "meetup.com",
    "latimes.com", "phillymag.com", "303magazine.com",
    "runguides.com", "clubsta.co", "sweatpals.com",
    "strava.com", "tripadvisor.com", "dallasites101.com",
    "ekneewalker.com", "do210.com", "do512.com", "do615.com",
    "mysanantonio.com", "seattlemet.com", "pdxmonthly.com",
    "nashvilleguru.com", "locallywell.com", "sanantonioreport.org",
    "nycforfree.co", "livingroomre.com", "fathomnutrition.com",
    "cussingrunner.com", "readandrunchicago.com",
    "vanderbilthealth.com", "my.vanderbilthealth.com",
    "crimsonconnect.du.edu",
}


def is_club_website(url: str) -> bool:
    """Check if URL is likely an actual run club website (not aggregator)."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    if any(skip in domain for skip in SKIP_DOMAINS):
        return False
    if "instagram.com" in domain:
        return False
    return True


def fetch_page(url: str) -> str | None:
    """Fetch a webpage and return its HTML content."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return None


def extract_instagram_from_html(html: str) -> list[str]:
    """Extract Instagram handles from HTML content."""
    handles = set()

    # Pattern 1: instagram.com/handle links
    ig_url_pattern = r'(?:https?://)?(?:www\.)?instagram\.com/([A-Za-z0-9_.]+)/?'
    for match in re.finditer(ig_url_pattern, html):
        handle = match.group(1).lower()
        if handle not in ("p", "reel", "reels", "explore", "stories", "accounts", "about", "legal", "developer", "static"):
            handles.add(handle)

    # Pattern 2: @handle near "instagram" text
    ig_at_pattern = r'@([A-Za-z0-9_.]{3,30})'
    for match in re.finditer(ig_at_pattern, html):
        handle = match.group(1).lower()
        # Check if near "instagram" context
        start = max(0, match.start() - 100)
        context = html[start:match.end() + 50].lower()
        if "instagram" in context or "insta" in context:
            handles.add(handle)

    return list(handles)


def lookup_follower_count(handle: str) -> int | None:
    """Look up Instagram follower count via SerpAPI."""
    query = f"instagram.com/{handle}"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 5,
        "gl": "us",
        "hl": "en",
    }
    try:
        resp = httpx.get(SERPAPI_BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        results = resp.json()

        for r in results.get("organic_results", []):
            link = r.get("link", "")
            if "instagram.com" not in link:
                continue
            for text in [r.get("snippet", ""), r.get("title", "")]:
                # Patterns: "12.3K Followers", "1,234 followers", "12K followers"
                for pattern in [
                    r"([\d,]+\.?\d*)\s*[Kk]\s*[Ff]ollowers?",
                    r"([\d,]+\.?\d*)\s*[Mm]\s*[Ff]ollowers?",
                    r"([\d,]+)\s*[Ff]ollowers?",
                ]:
                    match = re.search(pattern, text)
                    if match:
                        num_str = match.group(1).replace(",", "")
                        if "K" in pattern or "k" in pattern:
                            return int(float(num_str) * 1000)
                        elif "M" in pattern or "m" in pattern:
                            return int(float(num_str) * 1000000)
                        else:
                            return int(float(num_str))
        return None
    except Exception:
        return None


def main():
    with open(INPUT_PATH) as f:
        clubs = json.load(f)

    print(f"Loaded {len(clubs)} clubs from initial search")

    # Phase 1: Visit club websites to find Instagram handles
    clubs_needing_ig = [c for c in clubs if not c.get("instagram_handle") and is_club_website(c.get("url", ""))]
    print(f"\nPhase 1: Scraping {len(clubs_needing_ig)} club websites for Instagram handles...")

    new_ig_found = 0
    for i, club in enumerate(clubs_needing_ig):
        url = club["url"]
        print(f"  [{i+1}/{len(clubs_needing_ig)}] {url[:60]}...", end=" ")

        html = fetch_page(url)
        if not html:
            print("FAILED")
            continue

        handles = extract_instagram_from_html(html)
        if handles:
            # Take the first handle (most likely the club's own)
            club["instagram_handle"] = f"@{handles[0]}"
            club["source"] = "website_scrape"
            new_ig_found += 1
            print(f"-> @{handles[0]}")
        else:
            print("no IG found")

        time.sleep(0.5)

    print(f"\nPhase 1 complete: Found {new_ig_found} new Instagram handles from websites")

    # Deduplicate by Instagram handle
    seen_handles = {}
    deduped = []
    for club in clubs:
        handle = club.get("instagram_handle", "").lower()
        if handle and handle in seen_handles:
            continue
        if handle:
            seen_handles[handle] = True
        deduped.append(club)
    clubs = deduped
    print(f"After dedup: {len(clubs)} unique clubs")

    # Phase 2: Look up follower counts for all clubs with IG handles but no count
    clubs_needing_followers = [c for c in clubs if c.get("instagram_handle") and not c.get("followers")]
    print(f"\nPhase 2: Looking up follower counts for {len(clubs_needing_followers)} handles...")

    for i, club in enumerate(clubs_needing_followers):
        handle = club["instagram_handle"].lstrip("@")
        print(f"  [{i+1}/{len(clubs_needing_followers)}] @{handle}...", end=" ")

        count = lookup_follower_count(handle)
        club["followers"] = count
        if count:
            print(f"{count:,} followers")
        else:
            print("not found")

        time.sleep(1)

    # Sort by followers
    clubs.sort(key=lambda c: (c.get("followers") or 0), reverse=True)

    # Save enriched data
    with open(OUTPUT_PATH, "w") as f:
        json.dump(clubs, f, indent=2)

    # Print final results
    ranked = [c for c in clubs if c.get("followers")]
    has_ig = [c for c in clubs if c.get("instagram_handle") and not c.get("followers")]
    no_ig = [c for c in clubs if not c.get("instagram_handle")]

    print("\n" + "=" * 80)
    print(f"FINAL RESULTS: {len(ranked)} ranked + {len(has_ig)} unranked IG + {len(no_ig)} no IG")
    print("=" * 80)

    print(f"\n## RANKED BY FOLLOWERS ({len(ranked)} clubs)")
    print(f"{'Followers':>10} | {'Handle':<30} | {'City':<15} | Name")
    print("-" * 80)
    for c in ranked:
        print(f"{c['followers']:>10,} | {c['instagram_handle']:<30} | {c.get('city', '?'):<15} | {c['name'][:45]}")

    print(f"\n## INSTAGRAM HANDLE FOUND, FOLLOWERS UNKNOWN ({len(has_ig)} clubs)")
    print(f"{'Handle':<30} | {'City':<15} | Name")
    print("-" * 80)
    for c in has_ig:
        print(f"{c['instagram_handle']:<30} | {c.get('city', '?'):<15} | {c['name'][:45]}")

    print(f"\n## NO INSTAGRAM FOUND ({len(no_ig)} clubs)")
    for c in no_ig[:20]:
        print(f"  {c.get('city', '?'):<15} | {c['name'][:50]}")
    if len(no_ig) > 20:
        print(f"  ... and {len(no_ig) - 20} more")

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
