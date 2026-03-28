# Restaurant & Bar Data Enrichment Roadmap

**Dataset:** 1,020,535 US restaurants and bars filtered from 12.3M Google Maps businesses
**Current columns:** title, link, phone, category_titles, zip_code, normalized_display_link
**Goal:** Maximize the value of every row using only free data sources (no per-call API costs)

---

## Tier 1: Bulk Downloads + Local Joins (100% coverage, zero API calls)

These enrichments apply to every single row. They require one-time file downloads and local joins. Can all be completed in a single day.

### 1. Census Bureau Demographics (via zip code)

**Source:** American Community Survey (ACS) 5-year estimates, ZCTA-level
**Download:** `https://data.census.gov` or API at `https://api.census.gov/data/2022/acs/acs5`
**Coverage:** 100% (every zip maps to a ZCTA)
**Effort:** Half a day

**New columns:**
| Column | Description | Example |
|--------|-------------|---------|
| `population` | Total residents in zip | 42,891 |
| `median_household_income` | Median HHI | $68,500 |
| `per_capita_income` | Per capita income | $34,200 |
| `median_age` | Median age of residents | 36.4 |
| `poverty_rate` | % below poverty line | 12.3% |
| `unemployment_rate` | % unemployed | 4.1% |
| `pct_bachelors_plus` | % with bachelor's degree or higher | 38.7% |
| `household_size_avg` | Average household size | 2.6 |
| `pct_owner_occupied` | % homeowners vs renters | 54.2% |
| `pct_renter_occupied` | % renters | 45.8% |

**Why it matters:** A restaurant in a zip with $120K median income and 55% bachelor's+ is a fundamentally different sales prospect than one in a zip with $35K median income. This data powers segmentation, ICP scoring, and territory planning.

---

### 2. Geographic Enrichment (via zip code)

**Source:** HUD USPS Crosswalk Files + USDA Rural-Urban Continuum Codes
**Download:** `https://www.huduser.gov/portal/datasets/usps_crosswalk.html` and `https://www.ers.usda.gov/data-products/rural-urban-continuum-codes/`
**Coverage:** 100%
**Effort:** Half a day

**New columns:**
| Column | Description | Example |
|--------|-------------|---------|
| `city` | City name | Austin |
| `county` | County name | Travis County |
| `state` | State abbreviation | TX |
| `metro_area` | CBSA metro area name | Austin-Round Rock-Georgetown |
| `urban_rural_code` | USDA 1-9 scale (1=large metro core, 9=rural) | 1 |
| `metro_flag` | Boolean: is this in a metro area? | true |
| `region` | Census region (Northeast, South, Midwest, West) | South |
| `timezone` | Derived from state | Central |

**Why it matters:** Enables geographic segmentation, territory mapping, and metro-level campaign targeting. The metro_area field alone lets you group restaurants by DMA for localized campaigns.

---

### 3. IRS Income Data (via zip code)

**Source:** IRS Statistics of Income (SOI), Individual Income Tax by Zip Code
**Download:** `https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-zip-code-data-soi`
**Coverage:** 100%
**Effort:** Half a day

**New columns:**
| Column | Description | Example |
|--------|-------------|---------|
| `num_tax_returns` | Number of tax returns filed in zip | 18,450 |
| `total_income_amount` | Aggregate income in zip | $1.2B |
| `avg_income_per_return` | Average income per filer | $65,040 |
| `pct_returns_over_100k` | % of filers earning $100K+ | 28.3% |
| `pct_returns_over_200k` | % of filers earning $200K+ | 9.1% |

**Why it matters:** More granular than census income data. The bracket distribution shows wealth concentration: a zip with 30% of filers over $200K is fine dining territory.

---

### 4. Market Density Data (via county)

**Source:** USDA Food Environment Atlas + BLS Quarterly Census of Employment and Wages
**Download:** `https://www.ers.usda.gov/data-products/food-environment-atlas/` and `https://www.bls.gov/cew/`
**Coverage:** 100% (county-level)
**Effort:** Half a day

**New columns:**
| Column | Description | Example |
|--------|-------------|---------|
| `restaurants_per_1000_pop` | Restaurant density in county | 2.4 |
| `fast_food_per_1000_pop` | Fast food density | 0.8 |
| `full_service_per_1000_pop` | Full-service restaurant density | 1.1 |
| `county_restaurant_count` | Total restaurants in county | 1,240 |
| `avg_restaurant_wage` | Average weekly wage in food service (NAICS 722) | $485 |
| `county_total_food_employment` | Total food service employees in county | 14,200 |

**Why it matters:** Competition density tells you how saturated a market is. High density + high income = premium market. High density + low income = brutal competition. Low density + high income = underserved opportunity.

---

### 5. Business Name Analysis (computed, no download)

**Source:** Built in-house. Chain lookup table from Wikipedia + FDD filings. Keyword matching for cuisine.
**Coverage:** 100%
**Effort:** 1 day

**New columns:**
| Column | Description | Example |
|--------|-------------|---------|
| `is_chain` | Boolean: matches known chain name | false |
| `chain_name` | Normalized chain name (null if independent) | null |
| `chain_size_tier` | mega (1000+), large (100-999), regional (10-99), independent | independent |
| `inferred_cuisine` | Cuisine from name keywords (Taqueria=Mexican, Hibachi=Japanese) | Mexican |
| `cuisine_confidence` | high/medium/low based on keyword strength | high |
| `inferred_type` | bar, cafe, diner, fine_dining, fast_casual, etc. from name | restaurant |

**Why it matters:** This is the single most important segmentation column. ~200K of the 1M are chains (not your buyers). Separating them instantly focuses your pipeline on the ~800K independents. Cuisine inference enables vertical campaigns ("all Thai restaurants in Chicago").

---

## Tier 2: Free APIs + Compute Time (partial coverage, takes days to weeks)

These enrichments require HTTP requests or API calls but cost nothing. They trade compute time for data.

---

### 6. OpenStreetMap Cross-Reference (bulk download, local match)

**Source:** OpenStreetMap US extract via Geofabrik
**Download:** `https://download.geofabrik.de/north-america/us.html` (~10GB PBF file, filter locally)
**Coverage:** ~60% (OSM has ~600K US restaurant/bar/cafe/fast_food POIs)
**Matching:** Business name + zip code proximity
**Effort:** 1 day to download, parse, and match

**New columns:**
| Column | Description | Example |
|--------|-------------|---------|
| `osm_cuisine` | Cuisine tag(s) from OSM | pizza;italian |
| `outdoor_seating` | Has outdoor seating | yes |
| `delivery` | Offers delivery | yes |
| `takeaway` | Offers takeaway | yes |
| `capacity` | Number of seats | 85 |
| `wheelchair_accessible` | Wheelchair access | yes |
| `diet_vegetarian` | Vegetarian options | yes |
| `diet_vegan` | Vegan options | no |
| `payment_methods` | Accepted payment types | cash;credit_cards;contactless |
| `internet_access` | WiFi availability | wlan |

**Why it matters:** Capacity (seat count) is a proxy for restaurant size and revenue. Outdoor seating, delivery, and dietary options are real operational attributes that no other free source provides at this scale.

---

### 7. Website Analysis (HTTP requests, no API key needed)

**Source:** Direct HTTP GET to each restaurant's website URL
**Coverage:** ~70% (restaurants with a website in the dataset)
**Rate:** 1-2 requests/second (polite crawling). ~12 days for 1M at 1 req/sec.
**Effort:** 2-3 days to build scraper, 12 days to run

**New columns:**
| Column | Description | Example |
|--------|-------------|---------|
| `has_website` | Boolean: has a non-null website URL | true |
| `website_live` | Boolean: website returns 200 | true |
| `website_platform` | Detected CMS/builder | Squarespace |
| `has_online_ordering` | Detected ordering embed (Toast, ChowNow, DoorDash, UberEats, Square) | true |
| `ordering_provider` | Which ordering platform | Toast |
| `has_reservation_system` | Detected reservation widget (OpenTable, Resy, Yelp) | true |
| `reservation_provider` | Which reservation platform | OpenTable |
| `detected_pos` | POS system detected in page source (Toast, Square, Clover, Lightspeed) | Square |
| `has_ssl` | HTTPS enabled | true |
| `has_menu_page` | Link containing "menu" found | true |
| `has_catering_page` | Link containing "catering" found | false |
| `has_events_page` | Link containing "events" or "private" found | true |
| `social_instagram` | Instagram URL extracted from page | https://instagram.com/joes_tacos |
| `social_facebook` | Facebook URL extracted from page | https://facebook.com/joestacos |
| `copyright_year` | Most recent copyright year on site | 2025 |
| `is_custom_domain` | True if own domain vs. Wix/Squarespace subdomain or Yelp/Facebook page | true |

**Why it matters:** This is the highest-value enrichment for sales. Knowing a restaurant uses Square POS but has no online ordering tells you exactly what to pitch. A restaurant on Wix with no reservation system is a different conversation than one on BentoBox with OpenTable. Tech stack = sales signal.

**Detection patterns:**
- Toast: `toasttab.com` in scripts/links, `toast-restaurant` class
- Square: `squareup.com`, `square.site`, `weebly.com` (Square owns Weebly)
- ChowNow: `ordering.chownow.com` or `direct.chownow.com` embeds
- OpenTable: `opentable.com` widget/link
- Resy: `resy.com` embed
- DoorDash Storefront: `order.online` subdomain, `doordash.com` embed
- Clover: `clover.com` references
- Popmenu: `popmenu.com` in scripts
- BentoBox: `getbento.com` or `bentobox` in source

---

### 8. Foursquare Places API (99K free calls/month)

**Source:** Foursquare Places API (Starter tier)
**Endpoint:** `https://api.foursquare.com/v3/places/search` and `/places/{fsq_id}`
**Coverage:** ~60-70% match rate
**Rate:** 99,000 calls/month. Full 1M dataset in ~10 months. Or prioritize: do the 800K independents first (~8 months).
**Effort:** 1-2 days to build pipeline, then runs autonomously

**New columns:**
| Column | Description | Example |
|--------|-------------|---------|
| `fsq_rating` | Foursquare rating (1-10) | 7.8 |
| `fsq_total_ratings` | Number of ratings | 142 |
| `fsq_price` | Price tier (1-4) | 2 |
| `fsq_popularity` | Popularity score (float) | 0.87 |
| `fsq_categories` | Detailed category taxonomy | New American Restaurant |
| `fsq_hours` | Operating hours | Mon-Thu 11:00-22:00, Fri-Sat 11:00-23:00 |
| `fsq_features_outdoor_seating` | Has outdoor seating | true |
| `fsq_features_live_music` | Has live music | false |
| `fsq_features_private_room` | Has private dining | true |
| `fsq_features_wifi` | Has WiFi | true |
| `fsq_features_parking` | Parking available | lot |
| `fsq_tastes` | Community-tagged attributes | craft beer, date night, good for groups |
| `fsq_social_instagram` | Instagram handle | @joes_tacos |
| `fsq_social_facebook` | Facebook URL | facebook.com/joestacos |
| `fsq_menu_url` | Menu URL | joestacos.com/menu |

**Why it matters:** The `tastes` and `features` fields are uniquely valuable. No other free source tells you "this place is known for craft beer and is good for groups." Combined with price tier and rating, you can build a restaurant sophistication score.

---

### 9. Phone Number Analysis (computed, no API)

**Source:** Area code lookup table (freely available) + basic pattern matching
**Coverage:** 100% (all rows with a phone number)
**Effort:** A few hours

**New columns:**
| Column | Description | Example |
|--------|-------------|---------|
| `area_code` | Extracted area code | 512 |
| `area_code_city` | City associated with area code | Austin |
| `area_code_state` | State associated with area code | TX |
| `is_toll_free` | Is this an 800/888/877/etc. number | false |
| `geo_mismatch` | Area code state doesn't match zip code state | false |

**Why it matters:** Marginal on its own since zip gives you geography. But `geo_mismatch` is a useful data quality flag. A restaurant in Texas with a 212 (NYC) area code likely means the phone number is a cell phone, which tells you something about the business (small, owner-operated). Toll-free numbers suggest a chain or multi-location operation.

---

## Enrichment Summary

| # | Enrichment | New Columns | Coverage | Cost | Compute Time |
|---|-----------|-------------|----------|------|-------------|
| 1 | Census demographics | 10 | 100% | $0 | Hours |
| 2 | Geographic mapping | 8 | 100% | $0 | Hours |
| 3 | IRS income data | 5 | 100% | $0 | Hours |
| 4 | Market density | 6 | 100% | $0 | Hours |
| 5 | Business name analysis | 6 | 100% | $0 | Hours |
| 6 | OpenStreetMap | 10 | ~60% | $0 | 1 day |
| 7 | Website analysis | 16 | ~70% | $0 | ~12 days |
| 8 | Foursquare API | 15 | ~65% | $0 | ~10 months |
| 9 | Phone analysis | 5 | 100% | $0 | Hours |
| | **Total** | **~81 columns** | | **$0** | |

After all enrichments, each restaurant row goes from 6 columns to ~87 columns.

---

## Not Implementing (Interesting but not worth the effort now)

### Foursquare at full scale (10-month timeline)
The 99K calls/month free tier is generous, but covering all 1M restaurants takes nearly a year. Worth starting as a background job but not a blocker. Could prioritize by running independents-only (~800K) or top metro areas first.

### State Alcohol License Databases
Every state publishes active liquor license holders as public records. Would add `has_liquor_license` and `license_type` (beer/wine vs full bar). High value for segmentation (full liquor = higher avg check), but requires building ~50 per-state scrapers. Start with top 10 states (CA, TX, FL, NY, IL, OH, PA, NJ, GA, NC) to cover ~60% of US restaurants. Moderate effort, good Phase 2 project.

### City Health Inspection Data
Major cities publish inspection scores as open data (NYC, Chicago, LA, SF, etc.). Would add `inspection_score`, `grade` (A/B/C), `violations`. Interesting for scoring restaurant quality, but only covers ~30-40% of restaurants (major metro areas only) and requires building per-city parsers for ~20+ different data formats. High effort for partial coverage.

### Google Places API (free tier)
$200/month credit covers ~11,700 Place Details calls/month. Would add `google_rating`, `review_count`, `price_level`, `business_status`, `opening_hours`, `dine_in`/`delivery`/`takeout` booleans. Excellent data, but would take ~7 years for 1M restaurants at free tier. Only viable for enriching active campaign leads (hundreds to low thousands per month).

### Yelp Fusion API (free tier)
500 calls/day (~15K/month). Would add `yelp_rating`, `review_count`, `price`, `transactions` (delivery, pickup, reservation). Same problem as Google: would take ~5.5 years for full coverage. Only viable for per-lead enrichment on active campaigns.
