# Finding Your Next Customer

Techstars Chicago / Texas Workshop, March 30, 2026. Facilitated by Mert Iseri.

Everything from the workshop lives here: the complete sales agent toolkit, company-specific materials, and a dataset of 12M US businesses from Google Maps.

## Getting Started

1. Clone this repo
2. Install [Claude Code](https://claude.ai/claude-code) ($100/mo, this is your entire sales stack)
3. Open a terminal in this directory and run `claude`
4. Tell Claude what you need:

```
"Set up an email waterfall so I can find prospect emails"
"Help me scrape Google Maps for restaurants in Austin"
"Build me a copy generator for cold outreach"
"Set up Stripe so I can create payment links"
```

Claude reads the `.claude/CLAUDE.md` file automatically. It contains working code, API patterns, and setup instructions for every tool covered in the workshop.

## What's in here

```
gtm-core-toolkit.md           <- The complete sales agent toolkit (START HERE)
.claude/CLAUDE.md              <- Same toolkit, formatted as Claude Code agent instructions
workshop-questions.md          <- Discussion questions from the session
workshop-asset-plan.md         <- Big list definitions and enrichment roadmap
ideal-customer-profiles.md     <- ICP frameworks and examples
companies/                     <- Company-specific materials (ICPs, lead lists, filter scripts)
google-maps-12m-us-businesses/ <- 12M US business dataset from Google Maps
```

## The Toolkit (in gtm-core-toolkit.md)

Every tool Mert actually uses to build AI sales agents, with working code:

| Category | Tools |
|----------|-------|
| **Find Emails** | Email Waterfall (Kitt, Findymail, LeadMagic, Prospeo + NeverBounce verification) |
| **Generate Copy** | Copy Generator (Claude API + spam detection + formatting) |
| **Send at Scale** | SmartLead, Instantly, Email Bison |
| **Outreach Infra** | AgentMail, Hypertide |
| **Prospect Research** | Apollo, OpenMart, custom public database scrapers |
| **Web Scraping** | SerpAPI, Apify (Google Maps), FireCrawl, Image2Text, Kernel (stealth browsers) |
| **LinkedIn** | Unipile (search, connect, message) |
| **Domains + Deploy** | Cloudflare (buy domains, deploy landing pages for free) |
| **Copywriting** | Fletch PMM Library (451 B2B frameworks) |
| **Payments** | Stripe (payment links, invoices, checkout) |
| **Documents** | Google Docs API (create and share docs programmatically) |
| **Meetings** | Granola (record, transcribe, search meeting history) |
| **Calendar** | Google Calendar API |
| **CRM** | Salesforce |

## What you need

- [Claude Code](https://claude.ai/claude-code) ($100/mo)
- API keys for the specific tools you want to use (listed in each section of the toolkit)
- That's it. Claude handles the rest.

## Built by

- [Mert Iseri](https://www.linkedin.com/in/merthilmiiseri/) (248.ai)
- [Uzair Qarni](https://www.linkedin.com/in/uqarni/) (248.ai)
