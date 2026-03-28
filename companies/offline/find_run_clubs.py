"""
Find run clubs in top 15 US cities via SerpAPI, extract Instagram handles,
and rank by follower count.
"""

import json
import os
import re
import sys
import time
from urllib.parse import urlparse

import httpx

SERPAPI_KEY = os.environ["SERPAPI_KEY"]
SERPAPI_BASE_URL = "https://serpapi.com/search.json"

# Top 15 US cities likely to have active run clubs
CITIES = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "Austin",
    "San Francisco",
    "Seattle",
    "Denver",
    "Nashville",
    "Portland",
]

QUERIES_PER_CITY = [
    "run club {city}",
    "running crew {city}",
]


def search_serp(query: str) -> dict:
    """Run a Google search via SerpAPI."""
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 20,
        "gl": "us",
        "hl": "en",
    }
    resp = httpx.get(SERPAPI_BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def extract_instagram_handles(results: dict) -> list[dict]:
    """Extract Instagram handles and URLs from SERP results."""
    clubs = []
    seen_urls = set()

    organic = results.get("organic_results", [])
    for r in organic:
        url = r.get("link", "")
        title = r.get("title", "")
        snippet = r.get("snippet", "")

        if url in seen_urls:
            continue
        seen_urls.add(url)

        # Check if this is an Instagram profile
        parsed = urlparse(url)
        if "instagram.com" in parsed.netloc:
            handle = parsed.path.strip("/").split("/")[0] if parsed.path else ""
            if handle and handle not in ("p", "reel", "explore", "stories", "accounts"):
                clubs.append({
                    "name": title.replace(" (@", " (").split(" (")[0].strip() if "(@" in title else title,
                    "url": url,
                    "instagram_handle": f"@{handle}",
                    "source": "instagram_direct",
                })
            continue

        # Check if snippet or title mentions Instagram handle
        ig_pattern = r"@([A-Za-z0-9_.]+)"
        for text in [title, snippet]:
            matches = re.findall(ig_pattern, text)
            for m in matches:
                if len(m) > 3 and m.lower() not in ("gmail", "yahoo", "hotmail", "email", "com"):
                    clubs.append({
                        "name": title,
                        "url": url,
                        "instagram_handle": f"@{m}",
                        "source": "mention_in_serp",
                    })

        # Also capture the URL itself as a club lead even without IG
        if any(kw in url.lower() or kw in title.lower() for kw in ["run", "running", "crew", "stride", "mile", "pace", "track"]):
            clubs.append({
                "name": title,
                "url": url,
                "instagram_handle": "",
                "source": "website",
            })

    return clubs


def search_instagram_serp(handle: str) -> dict | None:
    """Search for an Instagram profile via SerpAPI to get follower count."""
    query = f"site:instagram.com {handle} run club"
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
        return resp.json()
    except Exception:
        return None


def extract_follower_count(text: str) -> int | None:
    """Try to extract follower count from snippet text."""
    # Patterns like "12.3K Followers", "1,234 followers", "12K followers"
    patterns = [
        r"([\d,]+\.?\d*)\s*[Kk]\s*[Ff]ollowers?",
        r"([\d,]+\.?\d*)\s*[Mm]\s*[Ff]ollowers?",
        r"([\d,]+)\s*[Ff]ollowers?",
    ]
    for pattern in patterns:
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


def main():
    all_clubs = []
    seen_handles = set()

    print(f"Searching for run clubs across {len(CITIES)} cities...")
    print("=" * 60)

    for city in CITIES:
        city_clubs = []
        for query_template in QUERIES_PER_CITY:
            query = query_template.format(city=city)
            print(f"  Searching: {query}")
            try:
                results = search_serp(query)
                clubs = extract_instagram_handles(results)
                city_clubs.extend(clubs)
                time.sleep(1)  # Rate limit courtesy
            except Exception as e:
                print(f"    ERROR: {e}")
                continue

        # Deduplicate within city
        for club in city_clubs:
            club["city"] = city
            handle = club["instagram_handle"].lower()
            url = club["url"].lower()
            key = handle if handle else url
            if key not in seen_handles:
                seen_handles.add(key)
                all_clubs.append(club)

        print(f"  {city}: {len([c for c in all_clubs if c['city'] == city])} unique clubs found")
        print()

    print("=" * 60)
    print(f"Total unique clubs/leads found: {len(all_clubs)}")

    # Now search for Instagram follower counts for clubs with handles
    clubs_with_ig = [c for c in all_clubs if c["instagram_handle"]]
    print(f"\nLooking up follower counts for {len(clubs_with_ig)} Instagram handles...")

    for i, club in enumerate(clubs_with_ig):
        handle = club["instagram_handle"].lstrip("@")
        print(f"  [{i+1}/{len(clubs_with_ig)}] Looking up @{handle}...")

        # Search Google for the Instagram profile to get follower count from snippet
        query = f"instagram.com/{handle}"
        try:
            results = search_serp(query)
            organic = results.get("organic_results", [])

            follower_count = None
            for r in organic:
                link = r.get("link", "")
                snippet = r.get("snippet", "")
                title = r.get("title", "")

                if "instagram.com" in link:
                    # Try snippet first, then title
                    for text in [snippet, title]:
                        count = extract_follower_count(text)
                        if count:
                            follower_count = count
                            break
                    if follower_count:
                        break

            club["followers"] = follower_count
            if follower_count:
                print(f"    @{handle}: {follower_count:,} followers")
            else:
                print(f"    @{handle}: followers not found in SERP")

            time.sleep(1)
        except Exception as e:
            print(f"    ERROR looking up @{handle}: {e}")
            club["followers"] = None

    # Sort by followers (descending), None at bottom
    all_clubs.sort(key=lambda c: (c.get("followers") or 0), reverse=True)

    # Output results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_clubs_ranked.json")
    with open(output_path, "w") as f:
        json.dump(all_clubs, f, indent=2)

    print("\n" + "=" * 60)
    print("RESULTS - Run Clubs Ranked by Instagram Followers")
    print("=" * 60)

    # Print clubs with followers first
    ranked = [c for c in all_clubs if c.get("followers")]
    unranked_ig = [c for c in all_clubs if c["instagram_handle"] and not c.get("followers")]
    no_ig = [c for c in all_clubs if not c["instagram_handle"]]

    print(f"\n## Ranked by followers ({len(ranked)} clubs)")
    for c in ranked:
        print(f"  {c['followers']:>8,} | {c['instagram_handle']:<25} | {c['city']:<15} | {c['name'][:50]}")

    print(f"\n## Have Instagram but followers unknown ({len(unranked_ig)} clubs)")
    for c in unranked_ig:
        print(f"           | {c['instagram_handle']:<25} | {c['city']:<15} | {c['name'][:50]}")

    print(f"\n## Website only, no Instagram found ({len(no_ig)} clubs)")
    for c in no_ig:
        print(f"           | {c['url'][:40]:<40} | {c['city']:<15} | {c['name'][:50]}")

    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
