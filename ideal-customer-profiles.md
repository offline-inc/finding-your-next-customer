# Ideal Customer Profiles (ICPs) — Techstars Chicago Cohort

Workshop: Finding Your Next Customer — March 30, 2026

---

## 1. LineSight

**One-liner:** AI copilot for metal service center slitting operations

**Stage:** Early. One named customer (Elite Steel). Exhibiting at NASCC Steel Conference and MSE 2026.

### Who buys

- **Steel and metal service centers with slitting lines** — companies like Elite Steel that buy coils and slit to order. LineSight's core product is specifically slitting plan optimization (not general fabrication). These centers analyze millions of coil configurations to minimize waste
- **Steel distributors with processing capabilities** — not just warehousing, but companies that shear, blank, slit, and plasma cut. The processing side is where LineSight's scheduling optimization applies
- **Toll processors** — companies that process metal owned by someone else. Throughput and material loss directly impact their margins since they're paid per job. Every percentage point of scrap is money out of their pocket

### Key pains

- Scrap waste averaging 5-10% (LineSight claims reduction to <2.5%, saving facilities like Elite Steel $550K/year)
- Production planning done via spreadsheets, pen and paper, guess-and-check
- 625+ hours/year spent on manual planning at a single facility
- Complex constraint juggling: gauges, chems, PIWs, multiple slitters, knife changes
- No optimization across these constraints simultaneously

### Where to find them (Google Maps / search terms)

- Steel service center
- Metal service center
- Steel distributor
- Metal fabricator
- Sheet metal contractor
- Steel fabricator
- Metal slitting
- Coil processing
- Steel supplier

### Qualifying signals

- Operates slitting lines (not just warehousing or basic distribution)
- Processing 10,000+ tons/year (enough volume for scrap savings to matter)
- Mentions "service center," "processing," or "cut to order" on their website
- Multiple processing machines (slitters, shears, laser/plasma cutters)
- Still using Excel or manual methods for production scheduling

---

## 2. Seated with Love

**One-liner:** White-label wedding planning platform for venues

**Stage:** Early. No named customers on site. Pricing at $0-$14.99/mo. Very thin web presence (7 pages, no blog, no testimonials).

### Who buys

- **Wedding venues** — banquet halls, estates, barns, boutique hotels, country clubs, rooftop event spaces that host weddings as a primary or major revenue stream
- **Event venues expanding into weddings** — restaurants with private dining rooms, wineries/breweries with event spaces, museums and galleries that rent for weddings
- **Multi-venue operators** — companies running multiple venue properties who need a consistent digital planning experience across locations (Pro tier supports multi-venue)

### What the product actually does

The platform is a venue-branded couple portal with:
- Pre-filled wedding website templates (venue photos, address, maps, parking, FAQs)
- Interactive floor plan builder with reusable templates (ceremony vs. reception, seasonal, indoor/outdoor)
- RSVP management
- Document portal (contracts, vendor recs, parking passes)
- Seating chart exports
- 30-second couple onboarding via email invite

### Key pains

- After booking, couples disappear into Google and plan elsewhere. The venue loses touch and influence
- Coordinators waste time answering the same questions repeatedly ("Can you resend the contract?")
- No digital planning experience to offer. Competing venues that feel "modern" win bookings
- Vendor referral revenue left on the table (30% affiliate share model)
- Priced out of existing event management software (Honeybook, Aisle Planner charge per-planner)
- Floor plan communication is manual and error-prone

### Where to find them (Google Maps / search terms)

- Wedding venue
- Event venue
- Banquet hall
- Wedding barn
- Reception venue
- Private event space
- Wedding estate
- Country club wedding

### Qualifying signals

- Host 20+ weddings per year (enough volume to justify even the $14.99/mo)
- Have a "preferred vendor list" on their website (already referring, not getting paid)
- Still using contact forms or PDF packages instead of digital tools
- Active on The Knot or WeddingWire listings
- No existing venue management software (check for login portals on their site)

---

## 3. Plexus

**One-liner:** HardwareOps: observability platform for physical systems

**Stage:** Early. One named customer (Scout Space, satellite monitoring). Actively hiring GTM. Legal name: Plexus Aerospace, Inc.

### Who buys

**Starting vertical (workshop recommendation): Autonomous vehicle companies.** This is a question for the founding team to confirm, but the product fits any company shipping software-defined hardware.

- **Autonomous vehicle companies** — self-driving cars, mining trucks, agricultural equipment, autonomous delivery robots. Mission-critical systems generating massive telemetry that needs real-time observability
- **Aerospace and satellite companies** — building/operating satellites, launch vehicles, drones. Scout Space (their one customer) is in this category. Post-deployment hardware they can't physically access
- **Robotics companies** — warehouse automation, manufacturing robots. Software-defined machines scaling from prototype to fleet
- **IoT device fleet operators** — companies shipping connected hardware (ESP32, Raspberry Pi, STM32-based devices) at scale

### What the product actually does

- Python SDK (Linux devices) and C SDK (embedded, ~1.5 KB RAM)
- Supports 15+ telemetry protocols
- Auto-generated dashboards from device sensor data
- GPU-accelerated visualization (100K+ data points at 60fps)
- Threshold alerts + anomaly detection
- Remote device commands
- Runbook automation
- AI root-cause analysis (Pro tier+)
- Pricing starts at $500/mo. Free tier: 5 devices, live-only data

### Key pains

- The "standard stack" requires 5+ separate tools (MQTT, Telegraf, InfluxDB, Grafana, Docker), each needing independent configuration
- Silent failures: one team had 3,872 failure warnings before realizing no data was flowing
- Days to get from sensor data to dashboards. Most hardware projects fail before reaching production observability
- Debugging is primitive: printf over UART during development, then blindness once devices ship
- Enterprise platforms are bloated and expensive (LabVIEW at $4,000/seat)
- "Software teams have DevOps. Hardware teams have spreadsheets."

### Where to find them

- LinkedIn Sales Navigator: filter by "autonomous vehicles," "robotics," "aerospace" + engineering/ops titles
- Crunchbase: companies tagged robotics, aerospace, autonomous vehicles with Series A+ funding
- GitHub/open-source: teams contributing to ROS, PX4, ArduPilot, Autoware
- Trade shows: AUVSI XPONENTIAL, Space Symposium, Automate, CES (automotive)
- Job boards: companies posting roles mentioning "telemetry," "fleet monitoring," "hardware observability"

### Qualifying signals

- Shipping or testing autonomous/semi-autonomous hardware in the field
- Engineering team of 10+ (enough complexity to need observability tooling)
- Currently cobbling together MQTT + Grafana + custom Python scripts
- Scaling from single prototype to multi-device fleet
- Job postings mentioning "telemetry," "anomaly detection," or "embedded systems"

---

## 4. WattShift

**One-liner:** Energy management platform for channel partners (B2B2C)

**Stage:** Early. No named customers. Has partner portal, API docs, and sandbox environment live. Free to end users, revenue from grid compensation.

### Who buys

WattShift is **B2B2C**: they sell through channel partners who already have relationships with residential energy customers. Four explicit partner segments from their website:

1. **Solar installers** — residential solar companies, especially in post-net-metering markets (California NEM 3.0, New York VDER). They need to close deals without expensive battery add-ons. WattShift gives them a software-only upsell that reduces customer bills
2. **DER OEMs (device manufacturers)** — makers of smart thermostats, heat pumps, batteries, EV chargers (Ecobee, Honeywell, Sensibo, Mitsubishi, Daikin, etc.). Want to add energy optimization as a software feature via white-label app or API
3. **HVAC service providers / contractors** — companies doing truck rolls for HVAC installation and maintenance. Need recurring revenue beyond one-time installation fees
4. **Property managers** — operators of multi-unit residential buildings, especially high-rises. Each device becomes a channel for grid payments back to the building

### What the product actually does

- Software-only (no hardware). Connects to existing smart thermostats
- Aggregates utility tariffs, solar export rates, wholesale market prices, demand response programs, and carbon intensity into a single optimization signal
- HVAC load shifting (pre-cools/pre-heats during cheap energy windows)
- Auto-enrolls in demand response programs
- White-label app and API for partners
- Savings calculator for customer-facing sales

### Key pains

**For solar installers:**
- NEM 3.0 and similar regulatory changes are destroying solar-only economics
- Batteries are too expensive, causing lost sales
- Need a software alternative to pitch alongside solar

**For DER OEMs:**
- Rate data is expensive and complex to access
- Risk of increasing customer bills when responding to DR events incorrectly
- Complex pre-cooling/pre-heating calculations

**For HVAC contractors:**
- Need recurring revenue beyond one-time installation fees
- Customers reluctant to adopt expensive hardware solutions

**For property managers:**
- High energy bills with no way to generate revenue from existing infrastructure
- Carbon emissions reduction pressure

### Where to find them

- Google Maps: "solar installer," "solar company," "HVAC contractor," "HVAC installer"
- EnergySage installer directory
- NABCEP certified installer database
- LinkedIn: "solar installer," "HVAC contractor," "property manager" + "energy"
- Trade shows: RE+, Distributech, AHR Expo (HVAC)
- State solar installer registries (especially CA, NY, TX, FL)

### Qualifying signals

- Solar installer operating in NEM 3.0 / post-net-metering markets
- HVAC contractor looking for recurring revenue models
- Property manager with 50+ units and central HVAC or smart thermostats
- DER OEM with connected devices but no energy optimization software layer

---

## 5. Offline

**One-liner:** IRL advertising network connecting brands to micro-communities

**Stage:** Growing. 1,500+ curated communities, 10,000+ IRL communities in network. Named case studies: Le Monde Gourmand, Supersuite, Allagash Brewing, Function of Beauty. Incubated from dcdx (founder's Gen Z research firm).

### Who buys

**Demand side (brands buying "check-ins"):**
- **DTC and consumer brands targeting Gen Z/Millennials** — especially beauty, fragrance, body care, food/beverage, lifestyle. Brands like Le Monde Gourmand, Function of Beauty, Supergoop, Supersuite, Allagash Brewing
- **Brands that need product trial and sampling** — the platform delivers physical product experiences at events, not just impressions. Supersuite case study: 78% of attendees used products within 4 days
- **Experiential marketing budget holders** — brand marketing managers, experiential leads, community marketing teams. Brands already spending on experiential but wanting attribution and scale

**Supply side (community hosts):**
- **IRL micro-community organizers** — grassroots community leaders running recurring gatherings: run clubs, supper clubs, dance communities, storytelling nights, dinner clubs, fitness groups
- **NOT traditional venues or event companies.** These are community builders: Offstage Dance Studio, Earthy Corazon (queer chicanx-owned candle shop), The Collective NY (founder/investor community), Lucky Dinner Club, StoryTell
- Hosts with consistent attendance who need sponsorship revenue to sustain their communities

### How it works

- Community discovery: brands filter 1,500+ communities by city, category, followers, engagement
- Campaign management with budget tracking and approval workflows
- GPS-verified check-ins via QR codes and SMS keywords at events
- Automated SMS delivery of discount codes and product samples post-check-in
- Analytics: check-ins, redemptions, SMS engagement, cost-per-acquisition, awareness lift, purchase intent

### Key pains

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

### Where to find them

**Brands (demand side):**
- LinkedIn: "experiential marketing," "community marketing," "brand marketing manager" at DTC/consumer brands
- Agencies: experiential marketing agencies (BMF, MKG, Gradient Experience)
- Brands active on Glossier/DTC playbook (sampling, pop-ups, community)

**Hosts (supply side):**
- Eventbrite, Luma, Partiful, Lu.ma: active recurring event creators
- Instagram: local community accounts with "link in bio" to event RSVPs
- Run clubs, book clubs, supper clubs, dance communities in target cities
- Meetup.com: organizers with 100+ members and monthly+ events

### Qualifying signals

**Brands:** Already spending on experiential, influencer, or sampling. Marketing team mentions "community" or "IRL." DTC brand in beauty, food/bev, lifestyle category
**Hosts:** Running events monthly+. 50+ average attendance. Active social following in a specific city. Interest-driven community (not just a venue)

---

## 6. CloudReno

**One-liner:** AI-enabled kitchen & bath renovation roll-up

**Stage:** Pre-acquisition. Seeking first 3 "founding partners" out of 24,000+ renovation businesses nationally. No acquisitions closed yet. Techstars-backed.

### Who they're acquiring

CloudReno's "customer" is an **acquisition target**. They are specifically looking for:

- **Profitable kitchen & bath renovation companies** — this is their stated focus. Not general contractors, not roofers, not commercial. Kitchen and bath remodelers with strong local reputations
- **Owner-operators approaching an exit** — owners who care deeply about their business but face the "trapped operator" problem: can't retire, can't scale, can't find a successor
- **The 24,000+ renovation businesses across the U.S.** — this is the total addressable pool. CloudReno is selecting 3 "founding partners" to start

### What CloudReno offers the seller

- Company name and brand stay ("your name stays on the truck")
- Entire team kept (explicit no-layoffs policy)
- Customer relationships unchanged
- Equity in their own business AND across the CloudReno portfolio
- CloudReno takes over marketing, estimating, purchasing, bookkeeping
- 3-year glide path: operator (Year 1), transition (Year 2), advisor with equity upside (Year 3+)
- Fair offer in 30 days based on market comps

### Key pains (for the acquisition target)

- Owner is approaching retirement with three bad options: close shop, sell to PE (lose culture), or pass to family (who may not want it)
- Business can't run without the owner (estimator, PM, and salesperson in one person)
- Can't scale beyond personal capacity
- No modern tech for marketing, estimating, or bookkeeping
- PE firms strip culture and do financial engineering. CloudReno positions as "renovation operators, not financial engineers"

### Where to find them (the 24,000)

- Google Maps: "kitchen remodeling," "bathroom remodeling," "kitchen and bath contractor," "bath renovation"
- Houzz Pro directory: filter by specialty (kitchen, bathroom) + years in business (10+ years)
- NARI (National Association of the Remodeling Industry) member directory
- NKBA (National Kitchen & Bath Association) member directory
- BBB listings: long-standing accredited remodelers
- State contractor license databases: filter by license issue date (15+ years ago)
- BizBuySell, business broker listings tagged "remodeling" or "renovation"
- Angi / HomeAdvisor contractor listings

### Qualifying signals

- Kitchen & bath focus (not general contracting or commercial)
- Owner is 55+ (check LinkedIn, About Us page, years in business)
- In business 15+ years with strong Google reviews and local reputation
- No clear #2 or next-gen leadership visible
- $1M-$10M revenue range (profitable enough to acquire, small enough to be owner-dependent)
- No modern tech stack (no CRM, paper estimates, basic QuickBooks)
- Growth potential: CloudReno must project 50%+ year-one growth to make an offer

---

## 7. Kaizen Design

**One-liner:** Digital building standards governance platform for health systems

**Stage:** Pre-revenue / early pilot. No named customers. "Get early access" CTA. Founder has deep healthcare construction background (Stanford Health, Cleveland Clinic Abu Dhabi). Won Big Idea Kearney contest.

### Who buys

Kaizen is **owner-centric**: they sell to the health system, not to architects or general contractors.

- **Health system facilities and capital planning leaders** — VP of Facilities, Director of Capital Planning, Director of Design & Construction at health systems with multiple facilities. They own the building standards documents that Kaizen digitizes
- **Health systems with active capital programs** — organizations spending $50M+/year on construction and renovation across their portfolio. The bigger the portfolio, the more painful fragmented standards become

### Secondary users (not the buyer, but benefit from the platform)

- Architecture and engineering firms designing for health systems (HKS, HDR, Perkins&Will, CannonDesign)
- Owner's representatives and construction program managers (JLL Healthcare, CBRE Healthcare, Hammes Company)
- Healthcare real estate developers building to health system specifications

### What the product actually does

- Digitizes building standards from static PDFs/binders/SharePoint into a living, cloud-based system
- Centralizes design criteria so all project teams reference the same version
- Governance and enforcement across multi-facility portfolios
- Continuous improvement loop: standards evolve over time rather than becoming outdated on publication

### Key pains

- Building standards scattered across PDFs, binders, SharePoint folders. No single source of truth
- Standards are outdated by the time they're published. Updates are slow, manual, inconsistent
- Rework and change orders from misapplied standards cost 5-15% of project budgets ($60B+ annual healthcare construction spend)
- No enforcement mechanism: architects reference old versions, miss updates, make assumptions
- Multi-facility systems can't ensure consistency across their portfolio
- Projects "consistently over budget and beyond the planned schedule"

### Where to find them

- Becker's Hospital Review: lists of largest health systems by number of facilities
- American Hospital Association (AHA) member directory
- ASHE (American Society for Health Care Engineering) membership and conference attendees
- Modern Healthcare's "Construction & Design" section
- LinkedIn: "VP Facilities" OR "Director Capital Planning" OR "Director Design and Construction" + "health system"
- FMI Capital Advisors healthcare construction reports
- Health Facilities Management magazine

### Qualifying signals

- Health system with 10+ facilities and an active capital program
- Currently maintaining building standards in static documents (Word, PDF, InDesign)
- Has a dedicated facilities planning or design standards team
- Recently completed or planning a major expansion or renovation
- Mentioned in trade press for construction projects
- $50M+/year construction spend

---

## 8. ForgeBee

**One-liner:** Pollination-as-a-service via automated bee production

**Stage:** Very early / deep tech. Currently selling Queen Monitoring Cage (QMC) to bee researchers. SBIR Phase I grant from USDA ($175K). Backed by world-class science (Gene Robinson, Wolf Prize in Agriculture, National Academy of Sciences).

### Who buys

ForgeBee is building a **vertically integrated pollination-as-a-service** model with three product stages, each with different customers:

**Near-term (now): Bee researchers**
- University and government labs studying queen health, colony behavior, and pesticide effects
- QMC is already being sold to researchers. This is current revenue

**Medium-term: Agrochemical companies**
- Companies like Bayer Crop Science, Corteva, BASF, Syngenta that need high-throughput pesticide screening on bees
- The QMC + Bee Factory enables controlled, repeatable biological assays at scale

**Long-term (the big market): Growers of pollination-dependent crops**
- Growers are farmers who grow crops that require bees to pollinate (bees carry pollen between flowers, which is how fruits and nuts form). Without pollination, these crops produce little or no yield
- **Almond growers** — the single largest pollination market in the U.S. (~$400M/year). California's Central Valley. Growers pay $200-250 per hive, need 2+ hives per acre
- **Berry growers** — blueberries, cherries, cranberries. Major regions: Pacific Northwest, Michigan, Maine, Florida
- **Apple, melon, and squash growers** — all require pollination services
- **Seed production companies** — hybrid seed production requires controlled pollination at scale
- 75% of crops worth over $15B in the U.S. require pollinators

### How the product pipeline works

1. **Queen Monitoring Cage (QMC)** — houses dozens/hundreds of queens in a controlled incubator. Machine vision for automated egg identification. Year-round egg harvesting. (Already selling to researchers)
2. **Bee Factory** — robotic system that rears eggs to adulthood in a sterile environment, protected from pathogens, parasites, pesticides. Minimal human supervision. Produces worker bees en masse
3. **Disposable Pollination Unit (DPU)** — small, non-reproductive hives with a high proportion of foragers (vs. natural ~30%). Delivered directly to fields. Foragers live their natural lifespan, then empty hives are returned or disposed. Fire-and-forget pollination

### Key pains

- Nearly 50% of honey bee colonies die annually from pathogens, parasites, pesticides, poor nutrition
- Commercial pollination is extremely stressful (bees trucked thousands of miles, exposed to chemicals)
- Growers can't find enough pollinators when they need them. Supply shrinking while demand grows
- Pollination costs rising 5-10% annually with no alternative
- No "on-demand" option. Growers book months in advance and hope colonies arrive healthy
- Climate volatility makes bloom timing unpredictable

### Where to find them

**Researchers (near-term):**
- University entomology and agriculture departments
- USDA Agricultural Research Service labs
- Academic conference attendees (Entomological Society of America)

**Growers (long-term):**
- California Almond Board member directory
- USDA NASS: top crop-producing counties for pollination-dependent crops
- Pollination broker networks (Bee Broker, Pollination Connection)
- American Beekeeping Federation membership
- Ag trade shows: Almond Conference, CPMA, Commodity Classic

### Qualifying signals

- Grower with 500+ acres of pollination-dependent crops (almonds, berries, apples)
- Located in a region with documented pollination shortages
- Already paying premium rates ($200+/hive) for pollination services
- Research lab studying bee health or pesticide effects at scale
- Agrochemical company with active pollination/bee health R&D programs

---

## Workshop discussion questions for the teams

| Company | Key ICP question to resolve |
|---|---|
| LineSight | How far beyond slitting do you go? Shearing, blanking, plasma? Or pure slitting focus? |
| Seated with Love | What venue size/type converts best at $14.99/mo? Barns? Hotels? Multi-venue operators? |
| Plexus | Which vertical first? Autonomous vehicles, aerospace, or robotics? (Recommendation: pick one) |
| WattShift | Which partner segment is converting fastest? Solar installers in NEM 3.0 markets? |
| Offline | Supply or demand first? How are you sourcing communities beyond dcdx network? |
| CloudReno | What makes a "founding partner" vs. just a profitable K&B shop? Revenue floor? Geography? |
| Kaizen Design | How many health systems have you talked to? What's the minimum portfolio size? |
| ForgeBee | Is the near-term play researchers + agrochemical, or are you going straight to growers? |
