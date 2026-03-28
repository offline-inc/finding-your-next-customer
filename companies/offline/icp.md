# Offline - Ideal Customer Profile

**One-liner:** IRL advertising network connecting brands to micro-communities

**Stage:** Growing. 1,500+ curated communities, 10,000+ IRL communities in network. Named case studies: Le Monde Gourmand, Supersuite, Allagash Brewing, Function of Beauty. Incubated from dcdx (founder's Gen Z research firm).

## Who buys

**Demand side (brands buying "check-ins"):**
- **DTC and consumer brands targeting Gen Z/Millennials** - especially beauty, fragrance, body care, food/beverage, lifestyle. Brands like Le Monde Gourmand, Function of Beauty, Supergoop, Supersuite, Allagash Brewing
- **Brands that need product trial and sampling** - the platform delivers physical product experiences at events, not just impressions. Supersuite case study: 78% of attendees used products within 4 days
- **Experiential marketing budget holders** - brand marketing managers, experiential leads, community marketing teams. Brands already spending on experiential but wanting attribution and scale

**Supply side (community hosts):**
- **IRL micro-community organizers** - grassroots community leaders running recurring gatherings: run clubs, supper clubs, dance communities, storytelling nights, dinner clubs, fitness groups
- **NOT traditional venues or event companies.** These are community builders: Offstage Dance Studio, Earthy Corazon (queer chicanx-owned candle shop), The Collective NY (founder/investor community), Lucky Dinner Club, StoryTell
- Hosts with consistent attendance who need sponsorship revenue to sustain their communities

## How it works

- Community discovery: brands filter 1,500+ communities by city, category, followers, engagement
- Campaign management with budget tracking and approval workflows
- GPS-verified check-ins via QR codes and SMS keywords at events
- Automated SMS delivery of discount codes and product samples post-check-in
- Analytics: check-ins, redemptions, SMS engagement, cost-per-acquisition, awareness lift, purchase intent

## Key pains

**Brands:**
- Digital ad fatigue. Gen Z trust has shifted offline
- No attribution for IRL marketing (sponsoring events is guesswork)
- Want experiential marketing at scale without producing their own events
- Need measurable outcomes: the Supersuite case study showed 10x brand awareness, 86% purchase likelihood

**Hosts:**
- No infrastructure to monetize beyond ticket sales
- Can't prove attendance or engagement to sponsors
- Manual, one-off sponsor outreach
- Need brand partnerships that align with community values

## Where to find them

**Brands (demand side):**
- LinkedIn: "experiential marketing," "community marketing," "brand marketing manager" at DTC/consumer brands
- Agencies: experiential marketing agencies (BMF, MKG, Gradient Experience)
- Brands active on Glossier/DTC playbook (sampling, pop-ups, community)

**Hosts (supply side):**
- Eventbrite, Luma, Partiful, Lu.ma: active recurring event creators
- Instagram: local community accounts with "link in bio" to event RSVPs
- Run clubs, book clubs, supper clubs, dance communities in target cities
- Meetup.com: organizers with 100+ members and monthly+ events

## Qualifying signals

**Brands:** Already spending on experiential, influencer, or sampling. Marketing team mentions "community" or "IRL." DTC brand in beauty, food/bev, lifestyle category
**Hosts:** Running events monthly+. 50+ average attendance. Active social following in a specific city. Interest-driven community (not just a venue)

## Lead lists generated

### Google Maps (507,827 total, 31,232 in major cities)
- **Source:** `community_leads_national.csv`
- Filtered from 12M US Google Maps businesses
- Tiers: community_space (259K), event_adjacent (128K), name_match (120K)
- Major cities: NYC, LA, Chicago, SF, Austin, Miami, Portland, Seattle, Denver, Nashville, Atlanta
- Note: Google Maps is imperfect for grassroots communities. Best used for venue/space leads, not organizers.

### Run clubs via SERP + website scraping (174 unique clubs across 15 cities)
- **Source:** `run_clubs_enriched.json`
- 29 clubs ranked by Instagram followers, 65 with handles but unknown counts, 80 website-only
- Top handles by following:
  - @diplosrunclub (133K, multi-city, celebrity brand)
  - @lamarathon (85K, LA Marathon org)
  - @denverbeerco (54K, brewery-hosted run club)
  - @nycruns (45K, NYC)
  - @chicagoruncollective (39K, Chicago)
  - @phx_run (24K, Phoenix)
  - @downtownrungroup (21K, San Antonio)
  - @milehighrunclub (21K, NYC)
  - @fleetfeetchicago (20K, Chicago)
  - @3run2 (15K, Chicago)
  - @marinarunclub_sf (14K, San Francisco)
  - @zftrunclub_dallas (14K, Dallas)
  - @oakcliffruncrew (14K, Dallas)
  - @urbanrunclubsatx (13K, San Antonio)
  - @6run5_ (11K, Nashville)
  - @cararuns (11K, Chicago)
  - @orcarunning (11K, Seattle)
- Best grassroots targets (not corporate/celebrity): @chicagoruncollective, @3run2, @oakcliffruncrew, @6run5_, @marinarunclub_sf, @orcarunning, @portlandrunningco, @noporunclubpdx
- Methodology: SerpAPI search for "run club {city}" + "running crew {city}", then website scraping for Instagram handles, follower counts via SERP lookup
- Scripts: `find_run_clubs.py`, `enrich_instagram.py`

### Next steps for lead expansion
- Repeat SERP methodology for supper clubs, dance communities, book clubs, fitness groups
- Scrape Eventbrite/Luma/Partiful for recurring event organizers in target cities
- Cross-reference with Offline's existing 1,500 community network to identify gaps

## Key ICP question to resolve

Supply or demand first? How are you sourcing communities beyond dcdx network?
