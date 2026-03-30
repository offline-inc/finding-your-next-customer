# GTM Core: The Complete Sales Agent Toolkit

From Mert Iseri's "Finding Your Next Customer" workshop. Every tool below is something I actually use to build AI sales agents. Each section includes working code your Claude agent can replicate.

## How to use this guide

1. Install [Claude Code](https://claude.ai/claude-code) ($100/mo)
2. Clone this repo and open a terminal in the directory
3. Run `claude`
4. Tell it what you need:

```
"Set up an email waterfall so I can find prospect emails"
"Help me scrape Google Maps for restaurants in Austin"
"Build me a copy generator for cold outreach"
"Set up Stripe so I can create payment links"
"Set up LinkedIn outreach via Unipile"
```

Claude reads the `.claude/CLAUDE.md` file in this repo automatically. It contains the same content as this document, formatted as agent instructions. Point your agent at any section and say "set up [tool name] the way GTM Core recommends."

For each tool: you'll need the API keys listed in that section. Create a `.env` file with your keys and your agent handles the rest.

---

## Subscriptions You'll Need

Before diving in, here's every paid service referenced in this guide. You don't need all of them. Pick the categories relevant to your workflow.

| Service | What For | Cost | Free Tier? | Sign Up |
|---------|----------|------|-----------|---------|
| Kitt | Email finding | Usage-based | Yes, free for individuals | trykitt.ai |
| Findymail | Email finding | $49/mo | Yes, 50 credits | findymail.com |
| LeadMagic | Email finding | Usage-based | Yes, free credits | leadmagic.io |
| Prospeo | Email finding (LinkedIn) | $39/mo | Yes, 75 credits | prospeo.io |
| NeverBounce | Email verification | Pay-per-check | Yes, 1K free | neverbounce.com |
| SmartLead | Email sequencing | $39/mo | No | smartlead.ai |
| Instantly | Email sequencing | $30/mo | No | instantly.ai |
| AgentMail | Domains/inboxes/sending | $20/mo | Yes, 3 inboxes | agentmail.to |
| Apollo | Contact/company data | $49/mo | Yes, 10K records/mo | apollo.io |
| Unipile | LinkedIn API | Contact sales | No | unipile.com |
| SerpAPI | Google search API | $25/mo | Yes, 250/mo | serpapi.com |
| Apify | Google Maps scraping | $49/mo | Yes, $5 credits | apify.com |
| FireCrawl | Website scraping | $19/mo | Yes, 500 pages/mo | firecrawl.dev |
| Scraping Bee | Website scraping | $49/mo | Yes, 1K credits | scrapingbee.com |
| Kernel | Stealth cloud browsers | Usage-based | Limited | kernel.sh |
| OpenMart | SMB business data | Usage-based | Yes | openmart.com |
| Stripe | Payments | 2.9% + $0.30/txn | Yes (test mode) | stripe.com |
| Cloudflare | Domains + hosting | $10-12/yr per domain | Yes (Pages free) | cloudflare.com |
| Google Cloud | Google Docs API | Free | Yes | console.cloud.google.com |
| Anthropic | Claude API (copy gen) | Usage-based | Free credits | console.anthropic.com |
| Fletch PMM | Copywriting frameworks | $50/yr membership | No | fletchpmm.com |
| Granola | Meeting recording/notes | $14/user/mo | Yes (30-day limit) | granola.ai |
| Google Calendar | Scheduling | Free | Yes | console.cloud.google.com |
| Salesforce | CRM | $25/user/mo | No | salesforce.com |

---

## Environment Variables Reference

Every API key referenced in this guide. Create a `.env` file with the keys you need:

```bash
# .env.example
# Copy to .env and fill in your values. Only include services you use.

# --- Email Finding (Waterfall) ---
# You need at least 2 finders + 1 verifier for the waterfall to be useful.
KITT_API_KEY=              # trykitt.ai > Dashboard > API Keys
FINDYMAIL_API_KEY=         # findymail.com > Settings > API
LEADMAGIC_API_KEY=         # leadmagic.io > Dashboard > API
PROSPEO_API_KEY=           # prospeo.io > Settings > API Key

# --- Email Verification ---
NEVERBOUNCE_API_KEY=       # neverbounce.com > API Settings > API Key

# --- Email Sequencing ---
SMARTLEAD_API_KEY=         # smartlead.ai > Settings > API > API Key
INSTANTLY_API_KEY=         # instantly.ai > Settings > Integrations > API

# --- Email Sending & Inboxes ---
AGENTMAIL_API_KEY=         # agentmail.to > Dashboard > API Keys

# --- Prospect Research ---
APOLLO_API_KEY=            # apollo.io > Settings > API Keys

# --- Web Search ---
SERPAPI_API_KEY=            # serpapi.com > Dashboard > Your API Key

# --- Web Scraping ---
APIFY_API_TOKEN=           # apify.com > Settings > Integrations > API token
FIRECRAWL_API_KEY=         # firecrawl.dev > Dashboard > API Keys
SCRAPINGBEE_API_KEY=       # scrapingbee.com > Dashboard

# --- Browser Rental ---
KERNEL_API_KEY=            # kernel.sh > Dashboard > API Keys

# --- LinkedIn ---
UNIPILE_API_KEY=           # unipile.com > Dashboard > API credentials
UNIPILE_ACCOUNT_ID=        # unipile.com > Dashboard > Account section
UNIPILE_API_BASE_URL=      # unipile.com > Dashboard (your instance URL)

# --- Local/SMB Data ---
OPENMART_API_KEY=          # openmart.com > Dashboard

# --- Payments ---
STRIPE_SECRET_KEY=         # stripe.com > Developers > API keys (sk_test_ for dev)

# --- Domains & Deployment ---
CLOUDFLARE_API_TOKEN=      # cloudflare.com > My Profile > API Tokens
CLOUDFLARE_ACCOUNT_ID=     # cloudflare.com > any domain > Overview sidebar

# --- Google Docs ---
# Uses OAuth2, not an API key. See Documents section for setup.
GDOCGEN_CREDENTIALS_PATH=  # Path to credentials.json from Google Cloud Console
GDOCGEN_TOKEN_PATH=         # Auto-created at ~/.google-doc-generator/token.json

# --- Copy Generation ---
ANTHROPIC_API_KEY=         # console.anthropic.com > API Keys

# --- Meeting Recording ---
# Granola uses OAuth via MCP, no API key needed. Requires Business plan ($14/mo).

# --- Calendar ---
# Google Calendar uses OAuth, no API key. Reuses Google Cloud project from Docs setup.
# Token auto-created at ~/.google-doc-generator/token.calendar.json

# --- CRM (Salesforce) ---
# Option A: Quick start (username + password + security token)
SF_USERNAME=               # Your Salesforce login email
SF_PASSWORD=               # Your Salesforce password
SF_SECURITY_TOKEN=         # Salesforce > Settings > Reset My Security Token (emailed to you)
# Option B: Production (JWT Bearer - server-to-server, no password needed)
SF_ISSUER=                 # Connected App's Consumer Key (client_id)
SF_KEYPATH=                # Path to your private key .pem file
SF_BASE_URL=               # "login" for production, "test" for sandbox
```

---

## 1. Email Outreach

This section covers the full email pipeline: find emails, generate personalized copy, sequence at scale, and manage your sending infrastructure.

### 1a. Find Prospect Emails (Email Waterfall)

**What it does:** Checks multiple email-finding providers in sequence: Kitt, Findymail, LeadMagic, Prospeo. When a provider finds an email, it verifies it with NeverBounce. If verification fails, it caches that email as invalid and moves to the next provider. Stops immediately when a valid, verified email is found.

**Why it matters:** No single provider has every email. Running a waterfall across providers dramatically increases your hit rate. Providers only charge when they find an email, making it economical. The verification step prevents you from emailing invalid addresses (which kills your sender reputation).

**Providers (in order):**

| # | Provider | Best For | Pricing |
|---|----------|----------|---------|
| 1 | Kitt | Primary finder, requires domain | Usage-based |
| 2 | Findymail | Good coverage, requires domain | $49/mo |
| 3 | LeadMagic | Accepts company name (no domain needed) | Usage-based |
| 4 | Prospeo | Best when you have a LinkedIn URL | $39/mo |

**Verifier:** NeverBounce. Only emails with status `valid` are accepted. Catchall emails are treated as invalid.

#### Agent Setup Instructions

Tell your Claude: "Replicate the email waterfall tool as a skill, the way GTM Core recommends."

**What your agent should build:** A Python async service with these components:

**1. Data structures:**

```python
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Set, List


@dataclass
class WaterfallStep:
    """One provider in the waterfall sequence."""
    provider_id: str          # e.g., "kitt_finder", "findymail"
    verifier_id: str = "neverbounce"
    output_field: str = "email"


@dataclass
class WaterfallContext:
    """State tracked during waterfall execution."""
    invalid_values: Set[str] = field(default_factory=set)  # Emails known to be bad
    attempts: List[Dict[str, Any]] = field(default_factory=list)
    total_api_calls: int = 0

    def mark_invalid(self, value: str) -> None:
        """Cache an email as invalid to skip redundant verification."""
        if value and isinstance(value, str):
            self.invalid_values.add(value.lower())

    def is_known_invalid(self, value: str) -> bool:
        """Check if we already verified this email as bad."""
        if not value or not isinstance(value, str):
            return False
        return value.lower() in self.invalid_values

    def record_attempt(self, provider_id: str, value: Optional[str], verified: bool) -> None:
        self.attempts.append({"provider": provider_id, "value": value, "verified": verified})
```

**2. Core waterfall logic:**

```python
# Provider sequence: Kitt -> Findymail -> LeadMagic -> Prospeo
EMAIL_PROVIDERS = ["kitt_finder", "findymail", "leadmagic", "prospeo"]
VERIFIER = "neverbounce"
VALID_RESULTS = {"valid"}  # Strict: only "valid" passes. Catchall = invalid.


async def execute_waterfall(
    inputs: Dict[str, Any],     # first_name, last_name, domain, company_name, linkedin_url
    api_keys: Dict[str, str],   # provider_id -> api_key
) -> Dict[str, Any]:
    """
    Run email providers in sequence. Verify each result with NeverBounce.
    Stop on first valid email. Cache invalid emails to avoid re-verification.

    Required inputs: first_name, last_name, and (domain OR company_name)
    Optional: linkedin_url (enables better Prospeo results)
    """
    context = WaterfallContext()

    for provider_id in EMAIL_PROVIDERS:
        api_key = api_keys.get(provider_id)
        if not api_key:
            continue  # Skip providers without keys

        # 1. Call the email finder
        email = await call_provider(provider_id, inputs, api_key)
        context.total_api_calls += 1

        if not email:
            context.record_attempt(provider_id, None, False)
            continue

        # 2. Skip if we already know this email is invalid
        if context.is_known_invalid(email):
            context.record_attempt(provider_id, email, False)
            continue

        # 3. Verify with NeverBounce
        nb_key = api_keys.get("neverbounce")
        if not nb_key:
            # No verifier key: accept unverified (not recommended)
            context.record_attempt(provider_id, email, True)
            return {"email": email, "source": provider_id, "status": "unverified",
                    "metadata": {"api_calls": context.total_api_calls, "attempts": context.attempts}}

        verification = await verify_email(email, nb_key)
        context.total_api_calls += 1

        if verification in VALID_RESULTS:
            context.record_attempt(provider_id, email, True)
            return {"email": email, "source": provider_id, "status": "valid",
                    "metadata": {"api_calls": context.total_api_calls, "attempts": context.attempts}}
        else:
            context.mark_invalid(email)
            context.record_attempt(provider_id, email, False)
            continue

    # All providers exhausted
    return {"email": "", "source": "", "status": "not_found",
            "metadata": {"api_calls": context.total_api_calls, "attempts": context.attempts,
                         "invalid_cached": list(context.invalid_values)}}
```

**3. Provider call patterns:**

```python
import httpx


async def call_provider(provider_id: str, inputs: dict, api_key: str) -> Optional[str]:
    """Call an email finder provider. Returns email or None."""
    async with httpx.AsyncClient(timeout=30) as client:
        if provider_id == "kitt_finder":
            resp = await client.post(
                "https://api.trykitt.ai/v1/find-email",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"first_name": inputs["first_name"], "last_name": inputs["last_name"],
                      "domain": inputs.get("domain", "")},
            )
        elif provider_id == "findymail":
            resp = await client.post(
                "https://app.findymail.com/api/search/name",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"first_name": inputs["first_name"], "last_name": inputs["last_name"],
                      "domain": inputs.get("domain", "")},
            )
        elif provider_id == "leadmagic":
            resp = await client.post(
                "https://api.leadmagic.io/email-finder",
                headers={"X-API-Key": api_key},
                json={"first_name": inputs["first_name"], "last_name": inputs["last_name"],
                      "domain": inputs.get("domain"), "company_name": inputs.get("company_name")},
            )
        elif provider_id == "prospeo":
            resp = await client.post(
                "https://api.prospeo.io/email-finder",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"first_name": inputs["first_name"], "last_name": inputs["last_name"],
                      "domain": inputs.get("domain", ""),
                      "linkedin_url": inputs.get("linkedin_url")},
            )
        else:
            return None

        if resp.status_code != 200:
            return None

        data = resp.json()
        email = data.get("email", "")
        if isinstance(email, dict):
            email = email.get("email") or email.get("address") or ""
        return email if email else None


async def verify_email(email: str, api_key: str) -> str:
    """Verify email with NeverBounce. Returns: valid, invalid, catchall, unknown."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.neverbounce.com/v4/single/check",
            json={"key": api_key, "email": email},
        )
        if resp.status_code != 200:
            return "error"
        return resp.json().get("result", "unknown")
```

**Keys your agent will ask for:**
- At minimum: 2 email finder keys + `NEVERBOUNCE_API_KEY`
- Recommended: all 4 finders + NeverBounce for maximum coverage

**Output format:**

```json
{
  "email": "alex@acme.com",
  "source": "findymail",
  "status": "valid",
  "metadata": {
    "api_calls": 4,
    "attempts": [
      {"provider": "kitt_finder", "value": null, "verified": false},
      {"provider": "findymail", "value": "alex@acme.com", "verified": true}
    ]
  }
}
```

---

### 1b. Generate Email Copy (Copy Generator)

**What it does:** Takes a lead list with enrichment data and generates personalized email sequences using Claude's Batch API. Post-processes every email through a spam word detector and cleans formatting. Outputs objects ready to feed into sequencer APIs.

**Why it matters:** You bypass the entire front-end UI of sequencer products. No product does this end-to-end today. You generate complete, spam-checked email objects programmatically and push them via API.

#### Agent Setup Instructions

Tell your Claude: "Build me a copy generator the way GTM Core recommends."

**What your agent should build:**

**1. Spam word detector** (critical for deliverability):

```python
import re
from typing import Optional

SPAM_WORDS = {
    # Urgency
    "act now", "limited time", "expires", "urgent", "hurry",
    "last chance", "don't miss", "final notice",
    # Money/Free
    "free", "no cost", "100% free", "bonus", "cash",
    "earn money", "extra income", "financial freedom",
    # Promises
    "guarantee", "guaranteed", "risk free", "no obligation",
    "promise", "best price", "lowest price",
    # Action words
    "click here", "click below", "buy now", "order now",
    "call now", "apply now", "sign up free",
    # Suspicious
    "congratulations", "winner", "you've been selected",
    "exclusive offer", "special offer", "limited offer",
    "one time offer", "this isn't spam",
    # Commonly filtered
    "sales", "stop",
}


def detect_spam_words(text: str, check_caps: bool = True) -> list[dict]:
    """Flag spam trigger words and ALL CAPS patterns (5+ chars)."""
    issues = []
    for word in SPAM_WORDS:
        pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            issues.append({
                "word": word,
                "position": match.start(),
                "type": "spam_word",
                "suggestion": f"Remove or rephrase '{word}'",
            })

    if check_caps:
        for match in re.finditer(r'\b[A-Z]{5,}\b', text):
            word = match.group()
            if word.lower() not in {"covid", "https", "http"}:
                issues.append({
                    "word": word,
                    "position": match.start(),
                    "type": "all_caps",
                    "suggestion": f"Avoid ALL CAPS: '{word}' -> '{word.title()}'",
                })
    return issues


def is_spam_free(text: str) -> bool:
    return len(detect_spam_words(text)) == 0
```

**2. Copy generation pipeline:**

```python
import anthropic

client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY from env


def generate_sequence(lead: dict, num_emails: int = 3) -> dict:
    """Generate a personalized email sequence for one lead."""
    prompt = f"""Write a {num_emails}-email cold outreach sequence for:
Name: {lead['first_name']} {lead['last_name']}
Title: {lead.get('title', 'Unknown')}
Company: {lead.get('company', 'Unknown')}
Company description: {lead.get('company_description', '')}
Background: {lead.get('education', '')}

Rules:
- Matter-of-fact tone. No corporate buzzwords.
- Each email under 100 words.
- No spam trigger words (free, guarantee, act now, click here, limited time).
- No em-dashes. Use periods and commas.
- No emojis.
- Email 1: introduce yourself and the value prop.
- Email 2: follow up with a specific insight about their company.
- Email 3: short breakup email.
- Include 2 subject line variations per email.

Return JSON array of objects with: step, subject_a, subject_b, body, delay_days"""

    response = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    # Parse, validate spam-free, return
    return parse_and_validate(response.content[0].text, lead)
```

**3. Post-processing (clean before sending):**

```python
def clean_email_copy(text: str) -> str:
    """Clean generated copy for deliverability."""
    import re
    # Remove em-dashes (replace with comma or period)
    text = text.replace("—", ",").replace("–", ",")
    # Remove emojis
    text = re.sub(r'[\U0001F600-\U0001F9FF\U0001FA00-\U0001FA6F\U00002702-\U000027B0]', '', text)
    # Fix double spaces
    text = re.sub(r' {2,}', ' ', text)
    # Fix double punctuation
    text = re.sub(r'([.!?,]){2,}', r'\1', text)
    return text.strip()
```

**Output format (ready for SmartLead/Instantly API):**

```json
{
  "lead_email": "alex@acme.com",
  "sequences": [
    {
      "step": 1,
      "subject_a": "Quick question about Acme's outbound",
      "subject_b": "Saw Acme is scaling the sales team",
      "body": "Hi Alex, ...",
      "delay_days": 0
    },
    {
      "step": 2,
      "subject_a": "Following up",
      "subject_b": "One more thing about Acme",
      "body": "Hi Alex, wanted to follow up...",
      "delay_days": 3
    }
  ]
}
```

**Keys needed:** `ANTHROPIC_API_KEY`

**For batch generation (cost-effective at scale):** Use the Anthropic Batch API to submit many leads at once. You send all prompts in one request and retrieve results when ready. ~50% cheaper than real-time calls.

---

### 1c. Sequence Emails at Scale

**What it does:** Create email campaigns, upload leads with personalized sequences, send from pre-warmed inboxes, and monitor replies. All via API.

**Why it matters:** This is the execution layer. You never touch the SmartLead or Instantly UI. Your agent creates campaigns, loads leads, starts sending, and checks for replies.

**Recommendation:** SmartLead (our primary) or Instantly

#### Agent Setup Instructions

Tell your Claude: "Set up SmartLead API integration the way GTM Core recommends."

**What your agent should build:** An async SmartLead client:

```python
import httpx
from typing import Any

BASE_URL = "https://server.smartlead.ai/api/v1"


class SmartLeadClient:
    """Async SmartLead API client. API key passed as query parameter."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def _request(self, method: str, endpoint: str,
                       params: dict | None = None, json: dict | None = None) -> Any:
        url = f"{BASE_URL}/{endpoint}"
        request_params = dict(params) if params else {}
        request_params["api_key"] = self.api_key
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.request(method, url, params=request_params, json=json)
            response.raise_for_status()
            return response.json()

    # --- Campaign lifecycle ---

    async def create_campaign(self) -> dict:
        """Create empty campaign. Returns {'id': int}."""
        return await self._request("POST", "campaigns/create")

    async def update_settings(self, campaign_id: int, settings: dict) -> dict:
        """Configure campaign: name, tracking, plain text mode, etc."""
        return await self._request("POST", f"campaigns/{campaign_id}/settings",
                                   json={k: v for k, v in settings.items() if v is not None})

    async def update_schedule(self, campaign_id: int, schedule: dict) -> dict:
        """Set timezone, send days, send hours, daily volume."""
        return await self._request("POST", f"campaigns/{campaign_id}/schedule", json=schedule)

    async def update_sequence(self, campaign_id: int, sequences: list[dict]) -> dict:
        """Set email sequence steps (subject, body, delay)."""
        return await self._request("POST", f"campaigns/{campaign_id}/sequences",
                                   json={"sequences": sequences})

    async def upload_leads(self, campaign_id: int, leads: list[dict]) -> dict:
        """Upload leads. Max 100 per batch."""
        return await self._request("POST", f"campaigns/{campaign_id}/leads",
                                   json={"lead_list": leads})

    async def attach_email_accounts(self, campaign_id: int, account_ids: list[int]) -> dict:
        """Attach sending inboxes to campaign."""
        return await self._request("POST", f"campaigns/{campaign_id}/email-accounts",
                                   json={"email_account_ids": account_ids})

    async def start_campaign(self, campaign_id: int) -> dict:
        return await self._request("POST", f"campaigns/{campaign_id}/status",
                                   json={"status": "START"})

    async def pause_campaign(self, campaign_id: int) -> dict:
        return await self._request("POST", f"campaigns/{campaign_id}/status",
                                   json={"status": "PAUSED"})

    # --- Monitoring ---

    async def get_analytics(self, campaign_id: int) -> dict:
        return await self._request("GET", f"campaigns/{campaign_id}/analytics")

    async def get_leads(self, campaign_id: int, offset: int = 0, limit: int = 100) -> dict:
        return await self._request("GET", f"campaigns/{campaign_id}/leads",
                                   params={"offset": offset, "limit": limit})

    async def get_email_accounts(self, campaign_id: int) -> list:
        return await self._request("GET", f"campaigns/{campaign_id}/email-accounts")

    async def get_all_email_accounts(self) -> list:
        return await self._request("GET", "email-accounts/")
```

**Full campaign launch workflow:**

```python
async def launch_campaign(client: SmartLeadClient, name: str, leads: list[dict],
                          sequences: list[dict], email_account_ids: list[int]):
    # 1. Create campaign
    campaign = await client.create_campaign()
    cid = campaign["id"]

    # 2. Configure settings
    await client.update_settings(cid, {"name": name, "track_opens": True, "track_clicks": True})

    # 3. Set schedule (weekdays, business hours, EST)
    await client.update_schedule(cid, {
        "timezone": "America/New_York",
        "days_of_the_week": [1, 2, 3, 4, 5],
        "start_hour": "09:00",
        "end_hour": "17:00",
        "min_time_btw_emails": 8,  # minutes
        "max_new_leads_per_day": 50,
    })

    # 4. Set sequence
    await client.update_sequence(cid, sequences)

    # 5. Upload leads (batch at 100)
    for i in range(0, len(leads), 100):
        await client.upload_leads(cid, leads[i:i+100])

    # 6. Attach inboxes
    await client.attach_email_accounts(cid, email_account_ids)

    # 7. Start
    await client.start_campaign(cid)
    return cid
```

**Keys needed:** `SMARTLEAD_API_KEY`

---

### 1d. Set Up Outreach Domains and Inboxes

**What it does:** Register domains, configure DNS (SPF, DKIM, DMARC), and create sending inboxes for cold outreach.

**Why it matters:** Cold outreach requires separate domains from your main business domain. Scaling means setting up many domains and inboxes.

**Recommendation:** AgentMail (fully agentic) or Hypertide (hypertide.io, managed service)

#### Agent Setup Instructions

Tell your Claude: "Set up AgentMail for cold outreach domains the way GTM Core recommends."

```bash
# Create inbox
curl -X POST https://api.agentmail.to/v1/inboxes \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Sales Outreach", "domain": "yourdomain.com"}'

# Get DNS records to configure
curl -X GET https://api.agentmail.to/v1/domains/yourdomain.com/dns \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY"

# Add the returned SPF, DKIM, DMARC records to your domain's DNS
```

**Keys needed:** `AGENTMAIL_API_KEY`

---

## 2. Prospect Research

### 2a. Company Search and Enrichment

**What it does:** Search for companies by industry, size, location, and keywords. Enrich a known domain with firmographic data (employee count, revenue, industry, tech stack, funding).

**Why it matters:** Before you reach out to a person, you need to know the company is worth reaching out to. Company search lets you build targeted account lists. Company enrichment lets you qualify and personalize.

**Recommendation:** Apollo

#### Agent Setup Instructions

Tell your Claude: "Set up Apollo company search the way GTM Core recommends."

**Search for companies by criteria:**

```python
import httpx

APOLLO_URL = "https://api.apollo.io/api/v1"

async def search_companies(
    api_key: str,
    locations: list[str] | None = None,
    employee_ranges: list[str] | None = None,
    keywords: list[str] | None = None,
    industry_tag_ids: list[str] | None = None,
    per_page: int = 25,
    page: int = 1,
) -> dict:
    """Search Apollo for companies matching criteria.

    Args:
        locations: e.g. ["Chicago, Illinois", "California, United States"]
        employee_ranges: e.g. ["1,10", "11,50", "51,200"]
        keywords: e.g. ["solar installer", "kitchen remodel"]
        industry_tag_ids: Apollo industry tags (get from their docs)
        per_page: max 100
        page: pagination
    """
    payload = {"per_page": per_page, "page": page}
    if locations:
        payload["organization_locations"] = locations
    if employee_ranges:
        payload["organization_num_employees_ranges"] = employee_ranges
    if keywords:
        payload["q_organization_keyword_tags"] = keywords
    if industry_tag_ids:
        payload["organization_industry_tag_ids"] = industry_tag_ids

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{APOLLO_URL}/mixed_companies/search",
            headers={"Content-Type": "application/json", "X-Api-Key": api_key},
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

    companies = []
    for org in data.get("organizations", []):
        companies.append({
            "name": org.get("name"),
            "domain": org.get("primary_domain"),
            "industry": org.get("industry"),
            "employee_count": org.get("estimated_num_employees"),
            "city": org.get("city"),
            "state": org.get("state"),
            "country": org.get("country"),
            "linkedin_url": org.get("linkedin_url"),
            "phone": org.get("phone"),
            "founded_year": org.get("founded_year"),
            "keywords": org.get("keywords", []),
        })
    return {
        "companies": companies,
        "total": data.get("pagination", {}).get("total_entries", 0),
        "page": page,
    }
```

**Quick curl version:**

```bash
# Search for solar installers in California with 1-50 employees
curl -X POST https://api.apollo.io/api/v1/mixed_companies/search \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -d '{
    "organization_locations": ["California, United States"],
    "organization_num_employees_ranges": ["1,50"],
    "q_organization_keyword_tags": ["solar installer"],
    "per_page": 25
  }'
```

**Enrich a single company by domain:**

```python
async def enrich_company(api_key: str, domain: str) -> dict:
    """Get detailed firmographic data for a known company domain."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{APOLLO_URL}/organizations/enrich",
            headers={"Content-Type": "application/json", "X-Api-Key": api_key},
            json={"domain": domain},
        )
        resp.raise_for_status()
        org = resp.json().get("organization", {})

    return {
        "name": org.get("name"),
        "domain": domain,
        "industry": org.get("industry"),
        "employee_count": org.get("estimated_num_employees"),
        "annual_revenue": org.get("annual_revenue_printed"),
        "city": org.get("city"),
        "state": org.get("state"),
        "country": org.get("country"),
        "description": org.get("short_description"),
        "linkedin_url": org.get("linkedin_url"),
        "phone": org.get("phone"),
        "founded_year": org.get("founded_year"),
        "technologies": org.get("current_technologies", []),
        "keywords": org.get("keywords", []),
        "funding_total": org.get("total_funding_printed"),
        "latest_funding_round": org.get("latest_funding_round_type"),
        "seo_description": org.get("seo_description"),
    }
```

**Quick curl version:**

```bash
# Enrich a company by domain
curl -X POST https://api.apollo.io/api/v1/organizations/enrich \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -d '{"domain": "acme.com"}'
```

**Useful search filters:**

| Filter | Example | What it does |
|--------|---------|-------------|
| `organization_locations` | `["Chicago, Illinois"]` | Filter by city, state, or country |
| `organization_num_employees_ranges` | `["1,10", "11,50"]` | Filter by employee count |
| `q_organization_keyword_tags` | `["solar", "HVAC"]` | Search by industry keywords |
| `organization_industry_tag_ids` | (Apollo-specific IDs) | Filter by Apollo's industry taxonomy |
| `per_page` | `100` | Results per page (max 100) |

**Caveat:** Apollo's free tier gives you 10K records/month. Company searches count against this. All provider data is stale (refreshed monthly/quarterly). Always pair with website scraping (FireCrawl) for current info.

**Keys needed:** `APOLLO_API_KEY`

---

### 2b. Contact Enrichment

**What it does:** Given a person's name and company, return their email, phone, title, LinkedIn URL, and other contact details.

**Recommendation:** Apollo

```python
async def enrich_contact(api_key: str, first_name: str, last_name: str,
                         domain: str | None = None,
                         linkedin_url: str | None = None) -> dict:
    """Enrich a person's contact details via Apollo."""
    payload = {"first_name": first_name, "last_name": last_name}
    if domain:
        payload["domain"] = domain
    if linkedin_url:
        payload["linkedin_url"] = linkedin_url

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{APOLLO_URL}/people/match",
            headers={"Content-Type": "application/json", "X-Api-Key": api_key},
            json=payload,
        )
        resp.raise_for_status()
        person = resp.json().get("person", {})

    return {
        "name": f"{person.get('first_name', '')} {person.get('last_name', '')}".strip(),
        "email": person.get("email"),
        "title": person.get("title"),
        "company": person.get("organization", {}).get("name"),
        "linkedin_url": person.get("linkedin_url"),
        "phone": person.get("phone_numbers", [{}])[0].get("sanitized_number") if person.get("phone_numbers") else None,
        "city": person.get("city"),
        "state": person.get("state"),
    }
```

```bash
# Quick curl: enrich a contact
curl -X POST https://api.apollo.io/api/v1/people/match \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -d '{"first_name": "Alex", "last_name": "Johnson", "domain": "acme.com"}'
```

**Keys needed:** `APOLLO_API_KEY`

---

### 2c. People Search (Find Employees at a Company)

**What it does:** Given a company domain, return all people matching criteria with their emails, titles, and LinkedIn URLs.

**Why it matters:** You found the company. Now you need the right person at that company. People search lets you filter by title, seniority, and department to find your buyer.

**Recommendation:** Apollo

```python
async def search_people(
    api_key: str,
    domains: list[str] | None = None,
    titles: list[str] | None = None,
    seniority: list[str] | None = None,
    per_page: int = 25,
    page: int = 1,
) -> dict:
    """Search for people at specific companies by title and seniority.

    Args:
        domains: e.g. ["acme.com", "bigcorp.com"]
        titles: e.g. ["VP of Operations", "Director of Facilities"]
        seniority: e.g. ["vp", "director", "c_suite", "owner", "founder"]
        per_page: max 100
    """
    payload = {"per_page": per_page, "page": page}
    if domains:
        payload["organization_domains"] = domains
    if titles:
        payload["person_titles"] = titles
    if seniority:
        payload["person_seniorities"] = seniority

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{APOLLO_URL}/mixed_people/search",
            headers={"Content-Type": "application/json", "X-Api-Key": api_key},
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

    people = []
    for p in data.get("people", []):
        people.append({
            "name": f"{p.get('first_name', '')} {p.get('last_name', '')}".strip(),
            "email": p.get("email"),
            "title": p.get("title"),
            "company": p.get("organization", {}).get("name"),
            "domain": p.get("organization", {}).get("primary_domain"),
            "linkedin_url": p.get("linkedin_url"),
            "seniority": p.get("seniority"),
            "city": p.get("city"),
            "state": p.get("state"),
        })
    return {
        "people": people,
        "total": data.get("pagination", {}).get("total_entries", 0),
        "page": page,
    }
```

**Quick curl version:**

```bash
curl -X POST https://api.apollo.io/api/v1/mixed_people/search \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -d '{"organization_domains": ["acme.com"], "person_titles": ["marketing"], "per_page": 25}'
```

**Caveat:** All provider data is stale. They refresh monthly or quarterly. Always pair with LinkedIn validation (2d).

**Keys needed:** `APOLLO_API_KEY`

---

### 2d. LinkedIn Profile Lookup and Outreach

**What it does:** Fetch LinkedIn profiles, search for people, send connection requests, manage your LinkedIn inbox. All via API.

**Why it matters:** LinkedIn is the source of truth for current employment. Also the primary channel for B2B outreach beyond email.

**Recommendation:** Unipile

**Caveat:** This is a gray area. LinkedIn does not want you to automate their platform. Unipile is a company that provides an API layer over LinkedIn accounts. Proceed with caution. You can get your account restricted. The risk is manageable with best practices, but you're operating against LinkedIn's TOS.

#### Agent Setup Instructions

Tell your Claude: "Set up Unipile for LinkedIn the way GTM Core recommends."

**What your agent should build:** An async Unipile client:

```python
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


class UnipileClient:
    """Async client for Unipile LinkedIn API.
    Auth: X-API-KEY header. Requires account_id for all operations."""

    def __init__(self, api_key: str, account_id: str, base_url: str):
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = base_url.rstrip("/")
        self.headers = {"X-API-KEY": api_key, "Content-Type": "application/json", "Accept": "application/json"}

    @retry(retry=retry_if_exception_type(httpx.ConnectError), stop=stop_after_attempt(3),
           wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _request(self, method: str, endpoint: str,
                       params: dict | None = None, json_data: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.request(method, url, headers=self.headers, params=params, json=json_data)
            resp.raise_for_status()
            return resp.json() if resp.text.strip() else {"ok": True}

    # --- Profiles ---

    async def get_profile(self, identifier: str) -> dict:
        """Get LinkedIn profile by slug or provider ID."""
        return await self._request("GET", f"/users/{identifier}",
                                   params={"account_id": self.account_id})

    async def get_own_profile(self) -> dict:
        return await self._request("GET", "/users/me", params={"account_id": self.account_id})

    # --- Messaging ---

    async def list_chats(self, limit: int = 50, cursor: str | None = None) -> dict:
        params = {"account_id": self.account_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        return await self._request("GET", "/chats", params=params)

    async def get_messages(self, chat_id: str, limit: int = 20) -> dict:
        return await self._request("GET", f"/chats/{chat_id}/messages",
                                   params={"account_id": self.account_id, "limit": limit})

    async def send_message(self, chat_id: str, text: str) -> dict:
        """Send message to existing chat."""
        return await self._request("POST", f"/chats/{chat_id}/messages",
                                   json_data={"account_id": self.account_id, "text": text})

    async def start_chat(self, attendee_id: str, text: str) -> dict:
        """Send first message to a connection."""
        return await self._request("POST", "/chats",
                                   json_data={"account_id": self.account_id, "text": text,
                                              "attendees_ids": attendee_id})

    # --- Connections ---

    async def send_invite(self, provider_id: str, message: str | None = None) -> dict:
        """Send connection request. Message max 300 chars."""
        data = {"provider_id": provider_id, "account_id": self.account_id}
        if message:
            data["message"] = message[:300]
        return await self._request("POST", "/users/invite", json_data=data)

    async def list_connections(self, limit: int = 100) -> dict:
        return await self._request("GET", "/users/relations",
                                   params={"account_id": self.account_id, "limit": limit})

    async def list_sent_invitations(self) -> dict:
        return await self._request("GET", "/users/invite/sent",
                                   params={"account_id": self.account_id})
```

**Best practices to avoid account restriction:**
- Max 20-25 connection requests per day
- Randomize timing between actions
- Personalize every message
- Warm up gradually (start with 5/day, increase over 2 weeks)

**Keys needed:** `UNIPILE_API_KEY`, `UNIPILE_ACCOUNT_ID`, `UNIPILE_API_BASE_URL`

---

### 2e. Local and SMB Business Data

**What it does:** Find contact info, owner details, and business data for small/medium businesses not on LinkedIn.

**Recommendation:** OpenMart for API data, or build custom scrapers for niche public databases.

**Key insight:** Owned and earned data is always more valuable than API broker data. Everyone has access to the same Apollo/ZoomInfo data. If you can find an obscure public database (like a state licensing board) and build a scraper for it, you're fishing in a pond nobody else is fishing in. That's your alpha.

**Keys needed:** `OPENMART_API_KEY`

---

## 3. Web Scraping and Search

### 3a. Run Google Searches via API (SerpAPI)

**What it does:** Execute Google searches programmatically and get structured results.

**Why it matters:** Lets you run research projects with sub-agents. "Find me all run clubs in Austin." Direct API access to Google results is incredibly useful for market research.

**Recommendation:** SerpAPI

#### Agent Setup Instructions

Tell your Claude: "Replicate the SerpAPI integration the way GTM Core recommends."

```python
import httpx

SERPAPI_URL = "https://serpapi.com/search"


async def search_google(query: str, api_key: str, num: int = 10) -> dict:
    """Execute a Google web search via SerpAPI. Returns structured results."""
    params = {"api_key": api_key, "engine": "google", "q": query, "num": num, "gl": "us", "hl": "en"}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(SERPAPI_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    results = [
        {"title": r.get("title", ""), "url": r.get("link", ""), "snippet": r.get("snippet", "")}
        for r in data.get("organic_results", [])
    ]
    return {"success": True, "results": results, "knowledge_graph": data.get("knowledge_graph")}


async def search_google_news(query: str, api_key: str, sort_by_date: bool = False) -> dict:
    """Google News search via SerpAPI."""
    params = {"api_key": api_key, "engine": "google_news", "q": query, "gl": "us", "hl": "en"}
    if sort_by_date:
        params["so"] = "1"
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(SERPAPI_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    return {"success": True, "results": [
        {"title": r.get("title", ""), "url": r.get("link", ""), "snippet": r.get("snippet", "")}
        for r in data.get("news_results", [])
    ]}
```

**Keys needed:** `SERPAPI_API_KEY`

---

### 3b. Google Maps, Social Media and Reviews (Apify)

**What it does:** Run Google Maps searches, search Facebook/Instagram, pull business reviews. Returns structured data: name, address, phone, website, rating, review count, categories, coordinates.

**Why it matters:** Google Maps is a goldmine for local business prospecting.

**Recommendation:** Apify (Google Maps Scraper actor: `nwua9Gu5YrADL7ZDj`)

#### Agent Setup Instructions

Tell your Claude: "Set up Apify Google Maps scraping the way GTM Core recommends."

```python
from apify_client import ApifyClientAsync

ACTOR_ID = "nwua9Gu5YrADL7ZDj"  # Google Maps Scraper


async def search_google_maps(api_token: str, categories: list[str],
                              zip_code: str, max_results: int = 100) -> list[dict]:
    """Search Google Maps for businesses by zip code and category."""
    client = ApifyClientAsync(token=api_token)

    per_search = max(1, max_results // len(categories))
    run_input = {
        "searchStringsArray": categories,     # e.g. ["restaurant", "cafe"]
        "postalCode": zip_code,               # e.g. "10001"
        "countryCode": "us",
        "maxCrawledPlacesPerSearch": per_search,
        "language": "en",
        "exportPlaceUrl": True,
    }

    # Start the actor run
    run = await client.actor(ACTOR_ID).start(run_input=run_input)
    run_id = run["id"]

    # Poll until done (runs take 1-10 minutes depending on volume)
    import asyncio
    while True:
        run_info = await client.run(run_id).get()
        if run_info["status"] in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
            break
        await asyncio.sleep(10)

    if run_info["status"] != "SUCCEEDED":
        return []

    # Fetch results
    items = []
    async for item in client.dataset(run_info["defaultDatasetId"]).iterate_items():
        if not item.get("placeId"):
            continue
        items.append({
            "place_id": item["placeId"],
            "name": item.get("title", ""),
            "address": item.get("address"),
            "city": item.get("city"),
            "state": item.get("state"),
            "zip": item.get("postalCode"),
            "phone": item.get("phone"),
            "website": item.get("website"),
            "rating": item.get("totalScore"),
            "review_count": item.get("reviewsCount"),
            "categories": item.get("categories", []),
            "lat": (item.get("location") or {}).get("lat"),
            "lng": (item.get("location") or {}).get("lng"),
        })
    return items
```

**Keys needed:** `APIFY_API_TOKEN`

**Useful actors:** `compass~crawler-google-places` (Maps), `apify/facebook-pages-scraper`, `apify/instagram-scraper`, `apify/yelp-scraper`

---

### 3c. Website Scraping (FireCrawl)

**What it does:** Extract content from any website. Returns clean, LLM-ready markdown.

**Why it matters:** If you have 200 business websites, scrape them, feed to your agent, and generate personalized outreach.

**Recommendation:** FireCrawl

#### Agent Setup Instructions

Tell your Claude: "Set up FireCrawl for website scraping the way GTM Core recommends."

```python
import asyncio
import random
import httpx

FIRECRAWL_URL = "https://api.firecrawl.dev/v1"


async def scrape_website(url: str, api_key: str) -> dict:
    """Scrape a website and return clean markdown content."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(f"{FIRECRAWL_URL}/scrape", headers=headers,
                                 json={"url": url})
        if resp.status_code in {429, 502, 503, 504}:
            # Retry with exponential backoff + jitter
            wait = min(2.0, 0.25 * 2) + random.uniform(0.0, 0.15)
            await asyncio.sleep(wait)
            resp = await client.post(f"{FIRECRAWL_URL}/scrape", headers=headers,
                                     json={"url": url})
        resp.raise_for_status()
        return resp.json()


async def discover_urls(url: str, api_key: str, limit: int = 50,
                        search: str | None = None) -> dict:
    """Discover crawlable URLs for a website via sitemap."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"url": url, "limit": limit}
    if search:
        payload["search"] = search
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(f"{FIRECRAWL_URL}/map", headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
    return {"urls": data.get("links", []), "count": len(data.get("links", []))}
```

**Keys needed:** `FIRECRAWL_API_KEY`

---

### 3d. Screenshot-to-Text (Image2Text)

**What it does:** Takes a screenshot of a website and runs OCR to extract text. The fallback scraping method that always works, even on JavaScript-heavy sites.

**Why it matters:** Some websites resist traditional scraping. A screenshot always works.

#### Agent Setup Instructions

Tell your Claude: "Build me an Image2Text service the way GTM Core recommends."

**What your agent should build:** A FastAPI service with Playwright + Tesseract:

```python
# Dependencies: pip install fastapi playwright pytesseract pillow
# Also: playwright install chromium, brew install tesseract (macOS)

import io
from PIL import Image
from playwright.async_api import async_playwright
import pytesseract

# --- Browser service (persistent, one instance) ---

_browser = None

async def start_browser():
    global _browser
    pw = await async_playwright().start()
    _browser = await pw.chromium.launch(headless=True)

async def screenshot_url(url: str, timeout_ms: int = 30000, full_page: bool = False) -> Image.Image:
    """Navigate to URL, take screenshot, return PIL Image. No state leaks."""
    context = await _browser.new_context(viewport={"width": 1440, "height": 900})
    page = await context.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        screenshot_bytes = await page.screenshot(full_page=full_page)
        return Image.open(io.BytesIO(screenshot_bytes))
    finally:
        await context.close()

# --- OCR service ---

def extract_text(image: Image.Image) -> str:
    """Extract text from image using Tesseract OCR."""
    return pytesseract.image_to_string(image).strip()

# --- Combined endpoint ---

async def image_to_text(url: str, full_page: bool = False) -> dict:
    image = await screenshot_url(url, full_page=full_page)
    text = extract_text(image)
    lines = [l for l in text.splitlines() if l.strip()]
    return {"text": text, "characters": len(text), "lines": len(lines)}
```

**Supported input:** URLs (screenshot taken automatically) or direct image uploads (JPEG, PNG, WebP, TIFF, BMP).

**Keys needed:** None. Self-contained service using open-source tools.

**System dependencies:** Tesseract OCR (`brew install tesseract`), Playwright Chromium (`playwright install chromium`)

---

### 3e. Stealth Cloud Browsers for Scale Scraping (Kernel)

**What it does:** Rent stealth cloud browser sessions with residential proxies, fingerprint randomization, and profile rotation. Connect Playwright to remote browsers via Chrome DevTools Protocol (CDP). Each browser session has its own IP, fingerprint, and browsing profile, making your scraping look like normal human traffic.

**Why it matters:** Running 200 Google searches from one browser gets you blocked with CAPTCHAs. With Kernel, you spin up stealth browser sessions with rotating proxies and profiles. Each session looks like a different person on a different computer. Essential for any serious-volume web scraping, especially against Google, LinkedIn, or other sites with aggressive bot detection.

**Recommendation:** Kernel (kernel.sh)

#### Agent Setup Instructions

Tell your Claude: "Set up Kernel for stealth browser scraping the way GTM Core recommends."

**What your agent should build:** A Kernel client that creates stealth browsers and connects Playwright:

```python
import httpx
from playwright.async_api import async_playwright, Browser, Page


class KernelClient:
    """Stealth cloud browser client using Kernel's API + Playwright CDP."""

    def __init__(self, api_key: str, timeout: int = 120):
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = "https://api.kernel.sh"

    async def create_browser(self, proxy_id: str | None = None,
                              profile_id: str | None = None) -> dict:
        """Create a stealth cloud browser session. Returns CDP WebSocket URL."""
        payload = {"stealth": True, "timeout": self.timeout}
        if proxy_id:
            payload["proxy_id"] = proxy_id
        if profile_id:
            payload["profile_id"] = profile_id

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/browsers",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            resp.raise_for_status()
            return resp.json()  # Contains cdp_ws_url

    async def connect_playwright(self, cdp_ws_url: str) -> tuple:
        """Connect Playwright to a Kernel browser via CDP."""
        pw = await async_playwright().start()
        browser = await pw.chromium.connect_over_cdp(cdp_ws_url)
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        return pw, browser, page


async def scrape_with_stealth(api_key: str, url: str) -> str:
    """Full workflow: create stealth browser, navigate, extract content."""
    kernel = KernelClient(api_key)

    # 1. Create stealth browser (residential proxy, randomized fingerprint)
    session = await kernel.create_browser()
    cdp_url = session["cdp_ws_url"]

    # 2. Connect Playwright
    pw, browser, page = await kernel.connect_playwright(cdp_url)

    try:
        # 3. Navigate and scrape
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        content = await page.content()
        return content
    finally:
        await browser.close()
        await pw.stop()
```

**For scale scraping with CAPTCHA detection (real pattern from our Google scraping):**

```python
import asyncio
import random

# Proxy and profile rotation pools
PROXY_POOL = ["proxy_1", "proxy_2", "proxy_3"]  # From Kernel dashboard
PROFILE_POOL = ["profile_1", "profile_2"]         # From Kernel dashboard

# CAPTCHA detection
CAPTCHA_SIGNALS = ["unusual traffic", "type the characters", "verify you are human",
                   "g-recaptcha", "automated queries"]

async def scrape_batch(api_key: str, urls: list[str], max_concurrent: int = 2) -> list[dict]:
    """Scrape URLs with proxy rotation, CAPTCHA detection, and adaptive cooldowns."""
    semaphore = asyncio.Semaphore(max_concurrent)
    consecutive_blocks = 0
    results = []

    for url in urls:
        async with semaphore:
            # Rotate proxy and profile
            proxy = random.choice(PROXY_POOL)
            profile = random.choice(PROFILE_POOL)

            kernel = KernelClient(api_key, timeout=1000)
            session = await kernel.create_browser(proxy_id=proxy, profile_id=profile)
            pw, browser, page = await kernel.connect_playwright(session["cdp_ws_url"])

            try:
                await page.goto(url, wait_until="domcontentloaded")
                html = await page.content()

                # Check for CAPTCHA
                if any(signal in html.lower() for signal in CAPTCHA_SIGNALS):
                    consecutive_blocks += 1
                    if consecutive_blocks >= 2:
                        # Adaptive cooldown: pause 180 seconds
                        await asyncio.sleep(180)
                        consecutive_blocks = 0
                    continue

                consecutive_blocks = 0
                results.append({"url": url, "content": html})

            finally:
                await browser.close()
                await pw.stop()

            # Random delay between requests (3-7 seconds)
            await asyncio.sleep(random.uniform(3.0, 7.0))

    return results
```

**Keys needed:** `KERNEL_API_KEY`

**Key configuration options:**
- Proxy pool: set up multiple residential proxies in Kernel dashboard, rotate per request
- Profile pool: different browser fingerprints (user agent, screen size, WebGL, etc.)
- Max concurrent browsers: start with 2, scale based on your Kernel plan
- CAPTCHA cooldown: 2-strike rule with 180-second pause
- Inter-request delay: 3-7 seconds randomized to mimic human behavior

---

## 4. Domains and Deployment

### 4a. Search, Purchase Domains, and Deploy Landing Pages

**What it does:** Check domain availability (single or batch), generate smart domain suggestions with prefix/suffix variations, purchase domains at cost via Cloudflare Registrar, deploy static sites to Cloudflare Pages, and configure DNS to connect your domain to your site. The complete flow from "I have an idea" to "it's live at mydomain.com with SSL."

**Why it matters:** You should be in control of your website. No Squarespace, no Wix, no designers. Tell Claude "build me a landing page for X" and deploy it in minutes. Update your website with words, not design tools. Domains cost $10/year and hosting is free.

**Recommendation:** Cloudflare (Registrar + Pages)

**Cloudflare at-cost domain pricing:**

| TLD | Annual Price |
|-----|-------------|
| .com | $10.46 |
| .net | $12.17 |
| .org | $12.17 |
| .co | $13.20 |
| .dev | $13.04 |
| .io | $44.99 |
| .ai | ~$75.00 |
| .me | $7.74 |

#### Agent Setup Instructions

Tell your Claude: "Set up Cloudflare domain management and deployment the way GTM Core recommends."

**What your agent should build:** An async Cloudflare client covering Pages, Registrar, and DNS:

```python
import logging
import mimetypes
from pathlib import Path
import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

# Cloudflare limits: 100 projects, 500 deploys/month, 20K files, 25MB/file
MAX_FILES_PER_DEPLOY = 20_000
MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024


class CloudflareError(Exception):
    def __init__(self, message: str, status_code: int | None = None, errors: list | None = None):
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(message)


def _is_retryable(exc: BaseException) -> bool:
    return isinstance(exc, CloudflareError) and exc.status_code is not None and exc.status_code >= 500


class CloudflareClient:
    """Async client for Cloudflare Pages, Registrar, and DNS APIs."""

    def __init__(self, account_id: str, api_token: str, zone_id: str | None = None):
        self.account_id = account_id
        self.api_token = api_token
        self.zone_id = zone_id
        self.base_url = "https://api.cloudflare.com/client/v4"
        self._client: httpx.AsyncClient | None = None

    @property
    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_token}"}

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=60, headers=self._headers)
        return self._client

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10),
           retry=retry_if_exception(_is_retryable))
    async def _request(self, method: str, path: str, *, json: dict | None = None,
                       files: list | None = None) -> dict:
        client = await self._get_client()
        url = f"{self.base_url}{path}"
        kwargs = {}
        if json is not None:
            kwargs["json"] = json
        if files is not None:
            kwargs["files"] = files
        response = await client.request(method, url, **kwargs)
        body = response.json()
        if not body.get("success", False):
            errors = body.get("errors", [])
            msg = "; ".join(e.get("message", str(e)) for e in errors) or f"HTTP {response.status_code}"
            raise CloudflareError(msg, status_code=response.status_code, errors=errors)
        return body.get("result", {})

    # --- Pages API ---

    async def create_project(self, project_name: str) -> dict:
        """Create a new CF Pages project."""
        return await self._request("POST", f"/accounts/{self.account_id}/pages/projects",
                                   json={"name": project_name, "production_branch": "main"})

    async def deploy(self, project_name: str, directory: Path) -> dict:
        """Upload static files via Direct Upload. Returns deployment URL."""
        file_parts = []
        for file_path in sorted(directory.rglob("*")):
            if file_path.is_dir() or file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
                continue
            relative = "/" + str(file_path.relative_to(directory))
            content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
            file_parts.append((relative, (file_path.name, file_path.read_bytes(), content_type)))

        if len(file_parts) > MAX_FILES_PER_DEPLOY:
            raise CloudflareError(f"Too many files ({len(file_parts)} > {MAX_FILES_PER_DEPLOY})")
        if not file_parts:
            raise CloudflareError("No files to deploy")

        client = await self._get_client()
        resp = await client.post(
            f"{self.base_url}/accounts/{self.account_id}/pages/projects/{project_name}/deployments",
            files=file_parts)
        body = resp.json()
        if not body.get("success"):
            raise CloudflareError("Deploy failed", status_code=resp.status_code)
        return body.get("result", {})

    async def add_custom_domain(self, project_name: str, domain: str) -> dict:
        """Attach a custom domain to a Pages project."""
        return await self._request("POST",
            f"/accounts/{self.account_id}/pages/projects/{project_name}/domains",
            json={"name": domain})

    async def delete_project(self, project_name: str) -> bool:
        await self._request("DELETE", f"/accounts/{self.account_id}/pages/projects/{project_name}")
        return True

    async def list_projects(self) -> list[dict]:
        result = await self._request("GET", f"/accounts/{self.account_id}/pages/projects")
        return result if isinstance(result, list) else [result]

    # --- Registrar API ---

    async def register_domain(self, domain: str, auto_renew: bool = True) -> dict:
        """Register a domain at cost via CF Registrar."""
        return await self._request("POST", f"/accounts/{self.account_id}/registrar/domains",
                                   json={"name": domain, "auto_renew": auto_renew})

    async def get_domain_registration(self, domain: str) -> dict:
        return await self._request("GET", f"/accounts/{self.account_id}/registrar/domains/{domain}")

    # --- DNS API ---

    async def create_dns_record(self, record_type: str, name: str, content: str,
                                proxied: bool = True, zone_id: str | None = None) -> dict:
        zid = zone_id or self.zone_id
        return await self._request("POST", f"/zones/{zid}/dns_records",
            json={"type": record_type, "name": name, "content": content, "proxied": proxied})

    async def configure_pages_dns(self, domain: str, cf_project_name: str,
                                  zone_id: str | None = None) -> dict:
        """CNAME domain -> project.pages.dev"""
        return await self.create_dns_record("CNAME", domain, f"{cf_project_name}.pages.dev",
                                           zone_id=zone_id)
```

**Full workflow: Idea to Live Site**

```
1. Suggest domains    -> brainstorm with TLD/prefix/suffix variations
2. User picks one     -> confirm price
3. Purchase           -> register_domain("mybrand.com")
4. Build site locally -> bun run build (Next.js, Vite, plain HTML)
5. Create project     -> create_project("mybrand")
6. Deploy             -> deploy("mybrand", Path("./out"))  OR  wrangler pages deploy ./out
7. Verify pages.dev   -> curl https://mybrand.pages.dev
8. Setup DNS          -> configure_pages_dns("mybrand.com", "mybrand")
9. Add custom domain  -> add_custom_domain("mybrand", "mybrand.com")
10. Verify production -> curl https://mybrand.com  (SSL auto-provisioned, ~1 min)
```

**Alternative: CLI-only approach (no Python needed):**

```bash
# Prerequisites (one-time)
bun add -g wrangler && wrangler login

# Create + deploy
wrangler pages project create mybrand
wrangler pages deploy ./out --project-name=mybrand

# Verify
curl -s -o /dev/null -w "%{http_code}" "https://mybrand.pages.dev"
```

**Keys needed:** `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`

**How to create the API token:**
1. cloudflare.com > My Profile > API Tokens > Create Token
2. Permissions needed: Account > Cloudflare Pages > Edit, Account > Registrar > Edit, Zone > DNS > Edit
3. Save the token (shown once)

---

## 5. Payments

### 5a. Accept Payments on the Internet

**What it does:** Create payment links, invoices, and checkout sessions. Let prospects pay you with a credit card immediately. Your agent can create a product, set a price, and generate a shareable payment URL in seconds.

**Why it matters:** Speed to revenue. You close a deal on a call, create a payment link, send it, and get paid. No logging into dashboards, no invoicing delays. Works for one-time payments, subscriptions, and custom amounts.

**Recommendation:** Stripe (API or CLI)

#### Agent Setup Instructions

Tell your Claude: "Set up Stripe payment links the way GTM Core recommends."

**Option A: Stripe CLI (fastest for quick links)**

```bash
# Install (one-time)
brew install stripe/stripe-cli/stripe
stripe login

# Create a product + price + payment link in three commands
stripe products create --name "Strategy Session" --description "1-hour GTM strategy session"
# Returns prod_XXX

stripe prices create --product prod_XXX --unit-amount 50000 --currency usd
# Returns price_XXX (amount in cents, so 50000 = $500)

stripe payment_links create --line-items '[{"price": "price_XXX", "quantity": 1}]'
# Returns a shareable URL: https://buy.stripe.com/XXX
```

**Option B: Python SDK (for embedding in automations)**

```python
import stripe

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# Create a checkout session (one-time payment)
session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    line_items=[{
        "price_data": {
            "currency": "usd",
            "product_data": {"name": "Website Redesign Package"},
            "unit_amount": 250000,  # $2,500 in cents
        },
        "quantity": 1,
    }],
    mode="payment",
    success_url="https://yourdomain.com/success",
    cancel_url="https://yourdomain.com/cancel",
)
print(session.url)  # Send this link to the customer

# Create an invoice
invoice = stripe.Invoice.create(
    customer="cus_XXX",  # or create customer first
    collection_method="send_invoice",
    days_until_due=30,
)
stripe.InvoiceItem.create(
    customer="cus_XXX",
    invoice=invoice.id,
    amount=100000,  # $1,000
    currency="usd",
    description="Consulting - March 2026",
)
stripe.Invoice.send_invoice(invoice.id)

# Verify webhook signatures (for payment confirmations)
event = stripe.Webhook.construct_event(
    payload=request_body,
    sig_header=request.headers["Stripe-Signature"],
    endpoint_secret=os.environ["STRIPE_WEBHOOK_SECRET"],
)
```

**Keys needed:** `STRIPE_SECRET_KEY` (use `sk_test_` for testing, `sk_live_` for real payments)

**Common use cases:**
- Payment link for a fixed service ($500 strategy session)
- Checkout session with custom amount (project quotes)
- Recurring subscription (monthly retainer)
- Invoice with net-30 terms (enterprise clients)

---

## 6. Copywriting

### 6a. Marketing Copy with Frameworks (Copywriting Library)

**What it does:** A Claude skill backed by a library of 451 B2B positioning, messaging, and copywriting frameworks from Fletch (Anthony Pierri). Search by topic, browse by number, or get random inspiration. Every framework includes written content and a visual diagram.

**Why it matters:** Most B2B marketing copy is terrible. "AI-powered agentic innovation cloud platform" means nothing. Your customers want to know: what do you do, how does it help me, and will it make me look good for spending money on it. Fletch charges $20K for a single website critique. This skill gives you all 451 of their published frameworks for $50/yr.

**Recommendation:** Build your own copywriting library skill

**Source:** Fletch PMM (fletchpmm.com), $50/yr membership for access to their full article archive.

#### Agent Setup Instructions

Tell your Claude: "Build me a copywriting library skill the way GTM Core recommends."

**Step 1: Get the content**

Sign up for Fletch PMM ($50/yr). Download or scrape all their published articles. Each article becomes two files:
- `NNN-title-slug.md` (the written framework)
- `NNN-title-slug-graphic.png` (the visual diagram)

Create an index file `00-index.md` listing all entries.

**Step 2: Create the skill file**

Create `~/.claude/skills/copywriting-library/skill.md`:

```markdown
---
name: copywriting-library
description: Access the copywriting library with 451 B2B positioning, messaging, and copywriting frameworks from Fletch. Use when writing homepage copy, hero messaging, value propositions, product positioning, or any marketing content. Triggers on keywords like copy, messaging, positioning, hero, homepage, value proposition, tagline, B2B marketing.
---

# Copywriting Library - 451 B2B Positioning & Messaging Frameworks

This skill provides access to a comprehensive copywriting library containing 451 articles on B2B positioning, messaging, and copywriting best practices from Fletch (Anthony Pierri).

## Library Location

**Path:** /path/to/your/copywriting-library/

**Contents:**
- 00-index.md - Full index of all 451 entries with titles
- NNN-title-slug.md - Individual article content
- NNN-title-slug-graphic.png - Associated visual framework/diagram

## Usage Modes

### 1. Search by Topic
When you need help with a specific copywriting challenge:

    grep -i "hero" /path/to/library/00-index.md
    grep -i "positioning" /path/to/library/00-index.md
    grep -i "value prop" /path/to/library/00-index.md

Then read the relevant article(s) and display the associated graphic.

### 2. Browse by Number
When user asks for a specific article:

    cat /path/to/library/043-*.md

### 3. Random Inspiration

    RANDOM_NUM=$(printf "%03d" $((RANDOM % 451 + 1)))
    cat /path/to/library/${RANDOM_NUM}-*.md

## Key Topics in the Library

| Topic | Example Articles |
|-------|------------------|
| Hero Messaging | #1, #111, #243, #339, #350, #370 |
| Homepage Structure | #3, #45, #145, #173, #202, #289, #297 |
| Positioning Strategy | #2, #4, #5, #17, #40, #98, #321 |
| Value Propositions | #148, #251, #260, #265, #382, #420, #430 |
| Multi-Product | #49, #66, #116, #172, #192, #224 |
| Differentiation | #6, #126, #152, #155, #203, #344, #444 |
| ICP/Target Audience | #10, #76, #91, #166, #174, #359 |
| Market Maturity | #4, #25, #101, #198, #206, #208 |
| Use Cases | #38, #95, #131, #159, #303, #408, #409 |
| Features Section | #60, #281, #451 |
| Problem Framing | #14, #18, #34, #205, #252, #368, #379 |

## Recommended Frameworks (Start Here)

These are the most actionable frameworks for immediate use:

1. #43 - Positioning & Messaging Canvas - Complete positioning framework
2. #137 - Positioning & Messaging Canvas (alt version) - Updated version
3. #98 - World's Simplest Positioning Equation - Quick positioning formula
4. #289 - World's Clearest Homepage Template - Homepage structure
5. #173 - 7 Essential Sections of a Homepage - Homepage checklist
6. #260 - How to Use the Fletch Value Proposition Canvas - VP framework
7. #130 - The Fletch Messaging Model - Core messaging architecture
8. #438 - Fletch's Value Proposition Messaging Canvas - VP template

## Workflow

1. Identify the challenge - What does the user need? (hero, positioning, homepage, etc.)
2. Search the index - Find relevant articles by grepping the index
3. Read top matches - Read 2-3 most relevant articles
4. Show graphics - Display associated PNG diagrams when available
5. Synthesize advice - Combine insights to give actionable recommendations
```

**Step 3: Stock the library**

Here are the first 100 articles in the index to give you a sense of the coverage (the full library has 451):

| # | Title |
|---|-------|
| 1 | A clear hero answers 1 of these 2 questions |
| 2 | Learn the two most important positioning strategies |
| 3 | How to tell if your homepage is clear enough |
| 4 | How to position in a mature category |
| 5 | Positioning for $100M Niches |
| 6 | The only way to differentiate with "business outcomes" |
| 7 | The Power of a Clear & Simple Message |
| 8 | The big market risk |
| 9 | The best messaging advice I ever received |
| 10 | You're building your ICP wrong |
| 14 | How to Position the Problem You Solve (as a B2B startup) |
| 16 | How to go from jargon & buzzwords to an actual positioning strategy |
| 17 | The only positioning deck you'll ever need |
| 18 | How to choose the "right problem" as a B2B startup |
| 19 | Your homepage needs to talk to a Real Buyer |
| 25 | How to position for an emerging market |
| 33 | Why "increasing revenue" shouldn't be your hero message |
| 34 | How to choose the right "problem" (as a B2B startup) |
| 38 | The definitive PMM definition: Use Case |
| 42 | Don't be Afraid to Pick an Enemy |
| 43 | Positioning & Messaging Canvas |
| 44 | How B2B Buyers Shop |
| 45 | Your homepage should be boring |
| 49 | Three Ways to do Multi-Product Homepages |
| 60 | How to write a webpage feature section |
| 76 | ICP Scorecard - How to prioritize market segments |
| 85 | How to showcase your positioning in the first scroll |
| 91 | How to Build your ICP |
| 95 | How to write a Use Case section for your homepage |
| 98 | World's Simplest Positioning Equation |
| 111 | HERO messaging: features vs benefits |
| 126 | The "Better Mousetrap" Mistake |
| 130 | The Fletch Messaging Model |
| 137 | The Positioning & Messaging Canvas (alt) |
| 145 | Product Marketing doesn't know how to write a homepage |
| 148 | What a value proposition is |
| 150 | How to handle competitive objections |
| 155 | How to build a Competitive Position |
| 159 | How to write a use case section |
| 173 | 7 Essential Sections of a Homepage |
| 192 | Multi-product homepages: Platform positioning |
| 202 | The complete guide to writing your homepage |
| 205 | Why you should lead with the problem |
| 224 | When to split products into separate homepages |
| 243 | Writing a hero section that converts |
| 251 | Why most value propositions don't work |
| 260 | How to Use the Fletch Value Proposition Canvas |
| 265 | Value Propositions: Outcomes vs. Features |
| 281 | How to write a features section that sells |
| 289 | World's Clearest Homepage Template |
| 297 | The anatomy of a high-converting homepage |
| 303 | Use case pages that actually work |
| 321 | Advanced positioning strategies |
| 339 | Hero messaging: the 3-second test |
| 344 | Differentiation when everyone claims the same thing |
| 350 | Above-the-fold messaging that works |
| 368 | Problem framing: your most underrated weapon |
| 370 | Hero section: show, don't tell |
| 379 | The problem with problem-first messaging |
| 382 | Value prop teardowns: what works and why |
| 408 | Use cases: the bridge between features and outcomes |
| 420 | Value propositions for technical products |
| 430 | Messaging hierarchy for complex products |
| 438 | Fletch's Value Proposition Messaging Canvas |
| 444 | When differentiation doesn't matter |
| 451 | The ultimate features section framework |

**Hard rules to encode in your skill:**
- No em-dashes. Use periods, commas, colons.
- No corporate jargon or buzzwords ("AI-powered", "innovative", "cutting-edge", "leverage").
- No hedge words ("arguably", "perhaps", "might").
- Matter-of-fact: "We increase your harvest rates by 30%" beats "We are an AI-powered agricultural innovation platform."
- Every sentence earns its place. Cut the fluff.
- Your customers want to know how you can get them promoted, not how innovative your technology is.
- Fletch's core philosophy: Clear, specific messaging beats vague outcome claims every time.

**No API keys needed.** This is a Claude skill built from reference material.

---

## 7. Documents

### 7a. Create and Share Google Docs

**What it does:** Programmatically create Google Docs from markdown content, apply formatting (headings, tables, lists, bold), and share them via link. Your agent writes content, creates a polished Google Doc, and gives you a shareable URL.

**Why it matters:** Shareable summaries, proposals, and meeting recaps. Take a call transcript from Granola, generate a summary, create a Google Doc, and send the link. Everyone already uses Google Docs, so the recipient doesn't need to install anything.

**Recommendation:** Build your own Google Doc generator (Python, uses Google Docs API + Drive API)

#### Agent Setup Instructions

Tell your Claude: "Build me a Google Doc generator the way GTM Core recommends."

**What the user needs to do first (one-time, manual):**

1. Go to console.cloud.google.com > create a new project (e.g., "Doc Generator")
2. APIs and Services > Library > enable **Google Docs API** and **Google Drive API**
3. APIs and Services > Credentials > Create Credentials > OAuth 2.0 Client ID
4. If prompted, configure the OAuth consent screen (External, add `documents` and `drive` scopes)
5. Application type: **Desktop application** (important: not "Web application")
6. Download the JSON file > save as `credentials.json`

**What your agent should build:**

The tool has four components: auth, markdown parser, request builder, and client. Here's how each works.

**1. Authentication (one-time browser flow, then headless forever):**

```python
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/documents",  # Create/edit docs
    "https://www.googleapis.com/auth/drive",       # Manage sharing and folders
]
TOKEN_PATH = os.path.expanduser("~/.google-doc-generator/token.json")


def get_credentials(credentials_path: str) -> Credentials:
    """Get Google OAuth credentials. Opens browser on first run, then uses cached token."""
    creds = None

    # Try cached token first
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # Refresh or re-auth if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Silent refresh, no browser
        else:
            # First time: opens browser for user to grant permission
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Cache token for future use
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    return creds
```

**2. Markdown to Google Docs conversion strategy:**

The Google Docs API uses `batchUpdate` with index-based operations. The approach:
1. Parse markdown into structured elements (headings, paragraphs, tables, lists)
2. Build the full plain text and track where each element starts/ends (index positions)
3. Insert all text in one `insertText` request
4. Apply formatting (heading styles, bold, bullet/numbered lists) in a second pass using the tracked positions
5. Handle tables separately because `insertTable` is a structural API call that changes the document's index space

```python
import re
from enum import Enum


class ElementType(Enum):
    HEADING1 = "h1"
    HEADING2 = "h2"
    HEADING3 = "h3"
    PARAGRAPH = "paragraph"
    BULLET = "bullet"
    NUMBERED = "numbered"
    TABLE = "table"
    HR = "hr"
    BLANK = "blank"


def parse_markdown(text: str) -> list[dict]:
    """Parse markdown into structured elements with type and content."""
    elements = []
    lines = text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            elements.append({"type": ElementType.BLANK, "content": ""})
        elif line == "---":
            elements.append({"type": ElementType.HR, "content": ""})
        elif line.startswith("### "):
            elements.append({"type": ElementType.HEADING3, "content": line[4:]})
        elif line.startswith("## "):
            elements.append({"type": ElementType.HEADING2, "content": line[3:]})
        elif line.startswith("# "):
            elements.append({"type": ElementType.HEADING1, "content": line[2:]})
        elif line.startswith("- "):
            elements.append({"type": ElementType.BULLET, "content": line[2:]})
        elif re.match(r"^\d+\.\s", line):
            elements.append({"type": ElementType.NUMBERED, "content": re.sub(r"^\d+\.\s", "", line)})
        elif line.startswith("|"):
            # Collect full table
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not re.match(r"^\|[\s\-:|]+\|$", lines[i].strip()):  # Skip separator rows
                    table_lines.append(lines[i].strip())
                i += 1
            elements.append({"type": ElementType.TABLE, "content": table_lines})
            continue
        else:
            elements.append({"type": ElementType.PARAGRAPH, "content": line})

        i += 1

    return elements
```

**3. Google Docs API client:**

```python
from googleapiclient.discovery import build


def create_google_doc(creds, title: str, markdown: str,
                      sharing: str = "private", folder_id: str | None = None) -> str:
    """Create a Google Doc from markdown. Returns the document URL."""
    docs_service = build("docs", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # 1. Create empty document
    doc = docs_service.documents().create(body={"title": title}).execute()
    doc_id = doc["documentId"]

    # 2. Move to folder if specified
    if folder_id:
        drive_service.files().update(
            fileId=doc_id,
            addParents=folder_id,
            removeParents="root",
        ).execute()

    # 3. Parse markdown and build requests
    elements = parse_markdown(markdown)
    requests = build_insert_requests(elements)  # Your agent builds this

    # 4. Apply text + formatting
    if requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests},
        ).execute()

    # 5. Insert tables (separate pass, because insertTable changes indices)
    insert_tables(docs_service, doc_id, elements)  # Your agent builds this

    # 6. Set sharing
    if sharing == "anyone_with_link":
        drive_service.permissions().create(
            fileId=doc_id,
            body={"type": "anyone", "role": "reader"},
        ).execute()
    elif sharing == "anyone_with_link_edit":
        drive_service.permissions().create(
            fileId=doc_id,
            body={"type": "anyone", "role": "writer"},
        ).execute()

    return f"https://docs.google.com/document/d/{doc_id}/edit"
```

**4. Key Google Docs API request patterns your agent needs to know:**

```python
# Insert text at a position
{"insertText": {"location": {"index": 1}, "text": "Hello world\n"}}

# Apply heading style
{"updateParagraphStyle": {
    "range": {"startIndex": 1, "endIndex": 12},
    "paragraphStyle": {"namedStyleType": "HEADING_1"},
    "fields": "namedStyleType",
}}

# Bold text
{"updateTextStyle": {
    "range": {"startIndex": 1, "endIndex": 6},
    "textStyle": {"bold": True},
    "fields": "bold",
}}

# Create bullet list
{"createParagraphBullets": {
    "range": {"startIndex": 1, "endIndex": 20},
    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
}}

# Insert table (3 rows, 2 columns)
{"insertTable": {
    "location": {"index": 1},
    "rows": 3,
    "columns": 2,
}}
```

**Important implementation details:**
- All indices are 1-based (index 0 is before the document body starts)
- `insertText` shifts all indices after the insertion point. Build text bottom-up or track offsets.
- `insertTable` is structural. Do it in a separate batchUpdate after all text formatting.
- Bold markers (`**text**`) should be tracked during text insertion, then the markers deleted and bold formatting applied in a cleanup pass.
- Tables: after inserting a table, you must read the document back to find the cell indices, then insert text into each cell individually.

**Dependencies:**

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

**What your agent needs from the user:**
1. A Google account
2. Google Cloud Console access (free)
3. The `credentials.json` file from the OAuth setup (user downloads this themselves)
4. One browser interaction for initial OAuth grant

After the first auth, everything is headless. The token auto-refreshes silently.

---

## 8. Meeting Recording and Transcripts

### 8a. AI Meeting Notes (Granola)

**What it does:** Records your meetings (without a bot joining the call), transcribes them, generates AI summaries, and makes everything searchable. Query your meeting history with natural language: "What did we decide about pricing in last week's call with Acme?"

**Why it matters:** Every sales call contains gold: objections, buying signals, competitor mentions, next steps. Without recording and transcribing, you lose all of it. Granola captures meetings without the awkwardness of a bot joining the call (it records system audio directly). The MCP integration means your Claude agent can search your meeting history and pull context into any workflow.

**Recommendation:** Granola
- Provider: granola.ai
- Pricing:
  - Basic: Free (30-day history limit, core AI notes)
  - Business: $14/user/month (unlimited history, integrations, advanced AI models)
  - Enterprise: $35+/user/month (SSO, API access, analytics)
- Auth: OAuth2 (for MCP integration)

#### Agent Setup Instructions

Tell your Claude: "Set up Granola meeting notes the way GTM Core recommends."

**Step 1: Install Granola**

Download from granola.ai. Works on Mac and Windows. No bot joins your calls. It captures system audio directly.

**Step 2: Connect the MCP server (for Claude Code integration)**

Add Granola's MCP server to your Claude Code config. This lets your agent search meetings, get transcripts, and pull meeting context into workflows.

```json
// Add to your Claude Code MCP settings
{
  "granola": {
    "type": "mcp",
    "url": "https://mcp.granola.ai"
  }
}
```

After adding, authenticate via OAuth when prompted.

**Step 3: Query your meetings**

Once connected, your agent can:

```
// Natural language queries via MCP
"What were the action items from my call with Acme Corp last Tuesday?"
"Summarize all meetings this week where pricing was discussed"
"What objections came up in my demos this month?"
"Pull the transcript from my last call with Alex Johnson"
```

**MCP tools available:**
- `query_granola_meetings` - Natural language search across all meetings (recommended)
- `list_meetings` - List meetings by time range (this_week, last_week, last_30_days)
- `get_meetings` - Get detailed notes, summaries, and attendees by meeting ID
- `get_meeting_transcript` - Get the full verbatim transcript for a specific meeting

**Useful patterns for sales:**
- After a call: "Summarize that call and create a Google Doc with next steps" (pairs with gdocgen)
- Pipeline review: "What did prospects say about pricing in all my calls this week?"
- Prep for follow-up: "What did Alex mention about their budget in our last meeting?"
- CRM updates: "What deals moved forward based on this week's meetings?"

**Keys needed:** None (OAuth via MCP). Requires Granola Business plan ($14/mo) for MCP integration.

---

## 9. Calendar

### 9a. Google Calendar Integration

**What it does:** Read your calendar, create events, check availability, and manage scheduling via API. Your agent can check your schedule before booking meetings and create calendar events programmatically.

**Why it matters:** Your agent needs to know when you're free. Pairing calendar access with meeting recording (Granola) and Google Docs gives you a complete meeting workflow: check availability, schedule, record, transcribe, summarize, share.

**Recommendation:** Google Calendar API (via MCP or direct OAuth)

#### Agent Setup Instructions

Tell your Claude: "Set up Google Calendar access the way GTM Core recommends."

**Option A: Google Calendar MCP (easiest for Claude Code)**

Install the Google Calendar MCP server. This gives Claude Code direct access to your calendar.

```bash
# Install the MCP server
npm install -g @anthropic/google-calendar-mcp
```

Configure in your Claude Code MCP settings, then authenticate via OAuth when prompted.

**Option B: Direct OAuth (for custom scripts)**

If you already set up Google Docs (section 7), you can reuse the same Google Cloud project. Just add the Calendar scope:

1. In your Google Cloud project, enable the **Google Calendar API**
2. Add scope: `https://www.googleapis.com/auth/calendar.readonly` (or `calendar` for read/write)
3. Re-run the OAuth flow to grant calendar permissions

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file("~/.google-doc-generator/token.calendar.json")
service = build("calendar", "v3", credentials=creds)

# List upcoming events
events = service.events().list(
    calendarId="primary",
    maxResults=10,
    singleEvents=True,
    orderBy="startTime",
).execute()

for event in events.get("items", []):
    print(event["summary"], event["start"].get("dateTime"))
```

**Keys needed:** None (OAuth). Reuses your Google Cloud project from the Google Docs setup.

---

## 10. CRM

### 10a. Salesforce Integration

**What it does:** Read and write deals, contacts, and pipeline data. Your agent can check deal status, update opportunities, log activities, and keep your CRM current without you ever opening the Salesforce UI.

**Why it matters:** CRM data goes stale because reps hate updating it. If your agent can update Salesforce after every call (pairing with Granola transcripts), your pipeline stays accurate automatically.

**Recommendation:** Salesforce API

#### Agent Setup Instructions

Tell your Claude: "Set up Salesforce API access the way GTM Core recommends."

**Two auth options. Pick one:**

**Option A: Quick start (username + password)**

Fastest to set up. Good for personal use and getting started.

```bash
pip install simple-salesforce
```

```python
import os
from simple_salesforce import Salesforce

sf = Salesforce(
    username=os.environ["SF_USERNAME"],
    password=os.environ["SF_PASSWORD"],
    security_token=os.environ["SF_SECURITY_TOKEN"],
    domain="login",  # or "test" for sandbox
)
```

How to get the security token:
1. In Salesforce: Settings > My Personal Information > Reset My Security Token
2. Salesforce emails it to you
3. Store in `.env`

**Option B: JWT Bearer flow (production, no password stored)**

This is what we use in production. Server-to-server auth with a private key. No password stored anywhere. Tokens auto-refresh.

Setup (one-time):
1. In Salesforce Setup, create a Connected App (App Manager > New Connected App)
2. Enable OAuth, add scopes: `api`, `refresh_token`
3. Generate a certificate/key pair: `openssl req -x509 -sha256 -nodes -days 36500 -newkey rsa:2048 -keyout server.key -out server.crt`
4. Upload `server.crt` to the Connected App
5. Pre-authorize the Connected App for your user's profile
6. Save the Consumer Key (this is your `SF_ISSUER`)

```python
import os
import time
import httpx
import jwt


class SalesforceClient:
    """Salesforce API client with JWT Bearer auth and auto-refresh."""

    def __init__(self):
        self.base_url = os.environ.get("SF_BASE_URL", "login")  # "login" or "test"
        self.issuer = os.environ["SF_ISSUER"]       # Connected App Consumer Key
        self.username = os.environ["SF_USERNAME"]     # Salesforce username
        self.key_path = os.environ["SF_KEYPATH"]      # Path to server.key
        self.token = None
        self.instance_url = None

    async def authenticate(self):
        """Get access token via JWT Bearer flow."""
        with open(self.key_path) as f:
            private_key = f.read()

        claim = {
            "iss": self.issuer,
            "exp": int(time.time()) + 300,
            "aud": f"https://{self.base_url}.salesforce.com",
            "sub": self.username,
        }
        assertion = jwt.encode(claim, private_key, algorithm="RS256")

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"https://{self.base_url}.salesforce.com/services/oauth2/token",
                data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                      "assertion": assertion},
            )
            resp.raise_for_status()
            data = resp.json()
            self.token = data["access_token"]
            self.instance_url = data["instance_url"]

    async def query(self, soql: str) -> dict:
        """Run a SOQL query."""
        if not self.token:
            await self.authenticate()
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.instance_url}/services/data/v59.0/query",
                params={"q": soql},
                headers={"Authorization": f"Bearer {self.token}"},
            )
            if resp.status_code == 401:  # Token expired, refresh
                await self.authenticate()
                resp = await client.get(
                    f"{self.instance_url}/services/data/v59.0/query",
                    params={"q": soql},
                    headers={"Authorization": f"Bearer {self.token}"},
                )
            resp.raise_for_status()
            return resp.json()

    async def create(self, object_type: str, data: dict) -> dict:
        """Create a Salesforce record."""
        if not self.token:
            await self.authenticate()
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.instance_url}/services/data/v59.0/sobjects/{object_type}",
                json=data,
                headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            )
            resp.raise_for_status()
            return resp.json()

    async def update(self, object_type: str, record_id: str, data: dict) -> bool:
        """Update a Salesforce record."""
        if not self.token:
            await self.authenticate()
        async with httpx.AsyncClient() as client:
            resp = await client.patch(
                f"{self.instance_url}/services/data/v59.0/sobjects/{object_type}/{record_id}",
                json=data,
                headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            )
            resp.raise_for_status()
            return True
```

**Common operations (work with either auth option):**

```python
# Query deals
deals = sf.query(
    "SELECT Id, Name, Amount, StageName, CloseDate "
    "FROM Opportunity WHERE StageName != 'Closed Won' "
    "ORDER BY CloseDate ASC LIMIT 20"
)

# Update a deal stage
sf.Opportunity.update("006XXXXXXXXXXXXXXX", {"StageName": "Negotiation/Review"})

# Create a contact
sf.Contact.create({
    "FirstName": "Alex", "LastName": "Johnson",
    "Email": "alex@acme.com", "Title": "VP of Sales",
    "AccountId": "001XXXXXXXXXXXXXXX",
})

# Log a call activity
sf.Task.create({
    "Subject": "Discovery call - discussed pricing",
    "WhoId": "003XXXXXXXXXXXXXXX",    # Contact ID
    "WhatId": "006XXXXXXXXXXXXXXX",   # Opportunity ID
    "Status": "Completed",
    "Description": "Discussed enterprise pricing. Follow up next week with proposal.",
})
```

**Keys needed:**
- Option A: `SF_USERNAME`, `SF_PASSWORD`, `SF_SECURITY_TOKEN`
- Option B: `SF_USERNAME`, `SF_ISSUER`, `SF_KEYPATH`, `SF_BASE_URL`

---

## Website Navigation Grouping

**Find Prospects**
- Prospect Research: Apollo, OpenMart, custom public database scrapers
- Web Scraping and Search: SerpAPI, Apify, FireCrawl, Image2Text, Kernel
- LinkedIn: Unipile

**Reach Prospects**
- Email Outreach: Email Waterfall (Kitt/Findymail/LeadMagic/Prospeo + NeverBounce), Copy Generator, SmartLead/Instantly, AgentMail
- Copywriting: Fletch PMM Library
- Documents: Google Docs (gdocgen)

**Close and Operate**
- Payments: Stripe
- Domains and Deployment: Cloudflare Registrar + Pages
- Meeting Recording: Granola
- Calendar: Google Calendar
- CRM: Salesforce
