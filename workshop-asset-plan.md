# Workshop Asset Plan: The Big List for Each Company

Techstars Chicago / Texas -- March 30, 2026

The journey: Start with the big list, contact lots of folks, learn from actual pain points and messaging, make the small list.

---

## LineSight

**The Big List:** Every steel and metal service center in the US with slitting, shearing, or processing capabilities.

**What's on it:**
- Company name, address, phone, website
- Google Maps category (steel fabricator, metal supplier, etc.)
- Owner/VP of Operations name + LinkedIn URL
- Number of Google reviews (proxy for size/longevity)
- Whether their website mentions "slitting," "coil processing," "cut to order" (boolean, scrapable)
- State and region

**What we have now:** 72,367 leads from Google Maps (32K core). Missing: owner names, LinkedIn, website keyword scan.

**Enrichment needed:** Scrape each website for keywords like "slitting," "coil," "service center." That alone could cut 72K down to 5K high-confidence leads. Then Apollo/LinkedIn for owner/ops names.

---

## Seated with Love

**The Big List:** Every wedding venue in the US with estimated annual wedding volume.

**What's on it:**
- Venue name, address, phone, website
- Listed on The Knot (yes/no), WeddingWire (yes/no)
- Number of reviews on The Knot/Google (proxy for volume)
- Whether they have a "preferred vendor list" page (scrapable)
- Whether they have an existing planning portal or login page (scrapable)
- Venue type (barn, hotel, estate, country club, restaurant)
- Coordinator name + email if on website

**What we have now:** 164,715 leads from Google Maps (39K core wedding venues). Missing: The Knot/WeddingWire cross-reference, coordinator names.

**Enrichment needed:** Cross-reference with The Knot and WeddingWire listings. Venues with 50+ reviews on The Knot are doing 30+ weddings/year. That's the volume filter. Then scrape contact pages for coordinator names and emails.

---

## Plexus

**The Big List:** Every company in the US building or operating autonomous hardware, with the hardware/ops engineering lead identified.

**What's on it:**
- Company name, website, HQ city
- Vertical (autonomous vehicles, aerospace, robotics, drones, IoT)
- Funding stage and amount (from Crunchbase/PitchBook)
- Engineering team size (from LinkedIn headcount)
- Hardware/ops lead name + LinkedIn URL + title
- Whether they have job postings mentioning "telemetry," "fleet," "embedded," "observability"
- GitHub repos (open-source signal of what stack they use)

**What we have now:** 23K from Google Maps (low quality for this ICP). This list needs to be built from Crunchbase, LinkedIn, and job boards, not Google Maps.

**Enrichment needed:** Crunchbase export of companies tagged robotics/aerospace/autonomous vehicles with 10-500 employees. LinkedIn Sales Navigator search for "Hardware Engineer" or "Telemetry Engineer" titles. That's the real list.

---

## WattShift

**The Big List:** Every solar installer and HVAC contractor in the US, segmented by state and regulatory environment.

**What's on it:**
- Company name, address, phone, website
- Type: solar installer, HVAC contractor, or property manager
- State and utility territory
- NEM 3.0 / post-net-metering market (yes/no)
- Estimated annual installs (from Google reviews as proxy, or EnergySage data)
- Owner/GM name + LinkedIn URL
- NABCEP certified (yes/no, for solar)
- Whether they sell batteries (from website, indicates they already feel the NEM 3.0 pain)

**What we have now:** 188,737 leads (6K core solar, 81K HVAC, 63K property mgmt). Missing: owner names, install volume, battery sales signal.

**Enrichment needed:** Focus on the 6K solar leads first. Cross-reference with EnergySage and NABCEP directories. Scrape websites for "battery" or "storage" mentions: those companies already feel the pain of NEM 3.0 and are looking for alternatives. That's the warmest segment.

---

## Offline

**The Big List:** Every IRL community organizer in the top 20 US cities with an active Instagram and recurring events.

**What's on it:**
- Community/club name
- Instagram handle + follower count
- City
- Community type (run club, supper club, dance, book club, fitness, art)
- Organizer's full name
- Organizer's LinkedIn URL
- Organizer's day job (from LinkedIn, this is the "Why" trigger)
- Event frequency (weekly, biweekly, monthly)
- Event platform (Luma, Partiful, Eventbrite, or just Instagram)

**What we have now:** 174 run clubs across 15 cities with Instagram handles, 29 ranked by followers. This is one community type in 15 cities.

**Enrichment needed:** Repeat the SERP methodology for supper clubs, dance communities, book clubs, fitness groups. Then the critical step: find each organizer on LinkedIn and confirm they have a full-time job. That's the signal that they want to monetize but can't quit their day job. That's the outreach hook.

---

## CloudReno

**The Big List:** Every kitchen and bath renovation company in the US with the owner's name, approximate age, years in business, and LinkedIn profile.

**What's on it:**
- Company name, address, phone, website
- Owner first name, last name
- Owner LinkedIn URL
- Estimated owner age (from LinkedIn graduation year or years in business)
- Years in business (from Google Maps "in business since" or state license database)
- Google review count + average rating (reputation signal)
- Whether website has been redesigned recently (outdated website = owner stopped investing)
- Revenue estimate (from employee count, Dun & Bradstreet, or ZoomInfo)
- Whether they have a visible #2/GM on LinkedIn (succession signal)

**What we have now:** 87,255 leads (42K core K&B remodelers). Missing: owner names, ages, LinkedIn profiles, succession signals.

**Enrichment needed:** This is the most enrichment-heavy list. Apollo or LinkedIn Sales Navigator for owner names. Cross-reference with state contractor license databases for license issue date (20+ years ago = likely boomer-owned). Scrape LinkedIn for graduation year to estimate age. The killer filter: owner is 55+, in business 15+ years, no visible #2 on LinkedIn, 4+ stars on Google. That might be 2,000-3,000 companies out of 42K.

---

## Kaizen Design

**The Big List:** Every health system in the US with 5+ facilities, the VP of Facilities or Director of Capital Planning identified, and their recent/planned construction projects.

**What's on it:**
- Health system name
- HQ city and state
- Number of facilities (from our domain grouping + AHA data)
- Annual capital spend estimate (from bond filings, trade press, or FMI reports)
- VP of Facilities / Director of Capital Planning name + LinkedIn URL + email
- Recent construction projects (from trade press, Dodge Data, or BidClerk)
- Whether they have published building design standards (some systems post these publicly)
- Architecture firms they work with (from project announcements)

**What we have now:** 580 health system domains with 10+ facilities. Missing: decision-maker names, capital spend, construction activity.

**Enrichment needed:** This is a small, high-value list. Manually identify the facilities/capital planning leader at each of the top 50 systems by size. Cross-reference with Becker's Hospital Review "largest health systems" lists, ASHE conference attendee lists, and Modern Healthcare construction announcements. The output is a spreadsheet of 50 named humans with context on their current construction activity.

---

## ForgeBee

Two lists, matched to their staged ICP.

### List A (near-term): Every university bee research lab and USDA agricultural research station in the US

**What's on it:**
- University/institution name
- Department (entomology, agriculture, biology)
- Principal Investigator name + email + lab website
- Research focus (colony health, pollination, pesticide effects, genomics)
- Active USDA/NSF grants (from USDA SBIR/NIFA databases)
- Whether they've published on colony collapse or queen health (PubMed search)

### List B (long-term): Every large-scale grower of pollination-dependent crops in California's Central Valley

**What's on it:**
- Farm/company name, address
- Crop type (almond, blueberry, cherry, apple, melon)
- Estimated acreage (from USDA Census of Agriculture, county assessor data)
- Owner/operator name
- Current pollination provider (if discoverable)
- Cooperative membership (California Almond Board, Blue Diamond, etc.)

**What we have now:** 108K leads from Google Maps (very broad), 831 bee/honey, 3,795 CA Central Valley. List A doesn't exist yet.

**Enrichment needed:** List A is the priority. Search PubMed for "honey bee colony" + "queen monitoring" + university affiliation. Search USDA NIFA grant database for bee-related awards. That gives a list of maybe 30-50 PIs who are the exact buyers for the QMC. List B is longer-term: USDA Census of Agriculture data by county for almond acreage, then cross-reference with California Almond Board membership.

---

## Summary: The Pattern

| Company | Big List Size | Key Enrichment | Killer Filter |
|---------|--------------|----------------|---------------|
| LineSight | 72K metal businesses | Website keyword scan for "slitting"/"coil" | Mentions slitting + 10K tons/yr |
| Seated with Love | 165K venue leads | The Knot/WeddingWire review count | 50+ reviews = 30+ weddings/yr |
| Plexus | Build from Crunchbase (not Maps) | LinkedIn for hardware eng leads | Job posts mentioning "telemetry" |
| WattShift | 189K solar/HVAC/property | Website scan for "battery"/"storage" | Solar + NEM 3.0 state + no battery |
| Offline | Expand from 174 to 1,000+ clubs | LinkedIn for organizer's day job | Has day job + runs events weekly |
| CloudReno | 87K K&B remodelers | Owner LinkedIn for age + tenure | Owner 55+, 15yr, no visible #2 |
| Kaizen Design | 580 health systems | Named decision-maker at each | Active capital program $50M+ |
| ForgeBee | 50 bee labs + 6K almond growers | PubMed + USDA grants for labs | PI published on colony health |

The journey for every company is the same:
1. **Start with the big list** (we built these today)
2. **Contact lots of folks** (volume outreach to learn)
3. **Learn from actual pain points and messaging** (what resonates, what doesn't)
4. **Make the small list** (the niche that responds)
