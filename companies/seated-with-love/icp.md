# Seated with Love - Ideal Customer Profile

**One-liner:** White-label wedding planning platform for venues

**Stage:** Early. No named customers on site. Pricing at $0-$14.99/mo. Very thin web presence (7 pages, no blog, no testimonials).

## Who buys

- **Wedding venues** - banquet halls, estates, barns, boutique hotels, country clubs, rooftop event spaces that host weddings as a primary or major revenue stream
- **Event venues expanding into weddings** - restaurants with private dining rooms, wineries/breweries with event spaces, museums and galleries that rent for weddings
- **Multi-venue operators** - companies running multiple venue properties who need a consistent digital planning experience across locations (Pro tier supports multi-venue)

## What the product actually does

The platform is a venue-branded couple portal with:
- Pre-filled wedding website templates (venue photos, address, maps, parking, FAQs)
- Interactive floor plan builder with reusable templates (ceremony vs. reception, seasonal, indoor/outdoor)
- RSVP management
- Document portal (contracts, vendor recs, parking passes)
- Seating chart exports
- 30-second couple onboarding via email invite

## Key pains

- After booking, couples disappear into Google and plan elsewhere. The venue loses touch and influence
- Coordinators waste time answering the same questions repeatedly ("Can you resend the contract?")
- No digital planning experience to offer. Competing venues that feel "modern" win bookings
- Vendor referral revenue left on the table (30% affiliate share model)
- Priced out of existing event management software (Honeybook, Aisle Planner charge per-planner)
- Floor plan communication is manual and error-prone

## Where to find them (Google Maps / search terms)

- Wedding venue
- Event venue
- Banquet hall
- Wedding barn
- Reception venue
- Private event space
- Wedding estate
- Country club wedding

## Qualifying signals

- Host 20+ weddings per year (enough volume to justify even the $14.99/mo)
- Have a "preferred vendor list" on their website (already referring, not getting paid)
- Still using contact forms or PDF packages instead of digital tools
- Active on The Knot or WeddingWire listings
- No existing venue management software (check for login portals on their site)

## Lead Dataset (from 12M Google Maps US Businesses)

We filtered 12 million US businesses from Google Maps and found **164,715 venue leads** nationally, tiered by relevance:

| Tier | Count | Description |
|------|------:|-------------|
| Core | 38,964 | Wedding venues, banquet halls, wedding chapels |
| Secondary | 66,023 | Event venues, conference centers, wedding services |
| Tertiary | 52,670 | Wineries, breweries, country clubs, boutique hotels, lodges |
| Name match | 7,058 | Business name contains "wedding", "banquet", "ballroom", "bridal" |

**Golden slice: 24,041 leads** in core tier with both phone number and website, explicitly tagged "Wedding venue" on Google Maps.

### Data available per lead

| Field | Coverage |
|-------|----------|
| Business name | 100% |
| Phone number | 91% |
| Website | 76% |
| ZIP code | 100% |
| Google Maps URL | 79% |
| Categories | 100% |

### File location

`companies/seated-with-love/venue_leads_national.csv` (164,715 rows)

## Enrichment Pipeline: Venue to Named Coordinator

The key contact at wedding venues is the **on-site coordinator** (also titled event coordinator, wedding coordinator, venue coordinator, event manager, wedding planner, banquet manager). These people are on LinkedIn.

### Step-by-step enrichment

1. **Apollo People Search** - For each venue domain, search for people with coordinator/event manager/wedding planner titles. Returns: name, title, LinkedIn URL, sometimes email and phone.
2. **Email Waterfall** (Kitt, Findymail, LeadMagic, Prospeo + NeverBounce) - For coordinators missing emails from Apollo. Prospeo works best here because you have LinkedIn URLs from Step 1.
3. **Apollo Contact Enrichment** - Fill in missing direct phone numbers.
4. **Unipile LinkedIn Validation** - Verify LinkedIn profiles are current and person still works at the venue.

### Target output per lead

| Field | Source |
|-------|--------|
| Venue name | Google Maps dataset |
| Venue phone | Google Maps dataset |
| Venue website | Google Maps dataset |
| Venue ZIP | Google Maps dataset |
| Coordinator name | Apollo People Search |
| Coordinator title | Apollo People Search |
| Coordinator LinkedIn | Apollo People Search |
| Coordinator email | Email Waterfall |
| Coordinator phone | Apollo Contact Enrichment |

### Cost estimate (per 500 leads)

| Service | Usage | Approximate Cost |
|---------|-------|-----------------|
| Apollo People Search | 500 domain lookups | Free tier (10K/mo) |
| Email Waterfall | ~1,000 finder calls + 500 verifications | ~$20-40 |
| Apollo Contact Enrichment | ~200 phone lookups | Free tier |
| Unipile LinkedIn validation | 500 profile checks | Usage-based |

### Recommended execution

Start with one metro area (e.g., 500 venues in Chicago). Prompt Claude:

> "Take the first 500 wedding venues in Illinois from venue_leads_national.csv. For each one, use Apollo to find anyone with 'coordinator', 'event manager', or 'wedding planner' in their title. Then run the email waterfall on every person you find. Output a CSV with venue name, coordinator name, title, LinkedIn, email, phone."

Output goes directly into SmartLead as a call/outreach list.

## Key ICP question to resolve

What venue size/type converts best at $14.99/mo? Barns? Hotels? Multi-venue operators?
