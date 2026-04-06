"""
Generate warm feedback-ask outreach emails for dcdx beauty industry contacts.

These are NOT sales emails. The tone is casual, personal, and research-oriented.
Andrew is reaching out because these people downloaded dcdx reports (Magnetic 100,
beauty quarterly reports, etc.) and he wants to start a conversation about trends
they're seeing, specifically around IRL / community in beauty.

Input:  dcdx_contacts_enriched.csv (from enrich_dcdx_contacts.py)
Output: dcdx_outreach_drafts.csv (ready to review and send)

Requires: ANTHROPIC_API_KEY in environment.
"""

import csv
import json
import os
import re
import sys

import anthropic

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "dcdx_contacts_enriched.csv")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "dcdx_outreach_drafts.csv")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Only generate emails for High and Medium confidence contacts
CONFIDENCE_FILTER = {"High", "Medium"}

# Batch size for generation (controls progress output)
BATCH_LOG_INTERVAL = 25

# ---------------------------------------------------------------------------
# Tone examples and system prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You write short, casual outreach emails for Andrew, founder of dcdx (a Gen Z research firm).

These are NOT sales emails. They are warm, low-pressure notes to people who have already engaged with dcdx content (downloaded reports like the Magnetic 100, quarterly beauty reports, etc.). Andrew wants to start a genuine conversation.

Voice rules:
- Casual, lowercase-friendly. Like texting a professional contact.
- Short. 3-5 sentences max. No fluff.
- No em-dashes. Use periods and commas.
- No emojis.
- No corporate speak ("leverage", "synergy", "innovative", "cutting-edge").
- No hedge words ("arguably", "perhaps").
- No "I hope this finds you well" or any version of that.
- Reference specific dcdx content they engaged with (from the Sources field).
- Tie into a trend observation (IRL events, community, beauty brand strategy).
- End with a genuine question, not a CTA or calendar link.
- Sign off as "Andrew" (just the name, no title block).

Tone examples:
- "Kinda random note but know you've seen some of our Magnetic 100 / beauty reports from dcdx. Been seeing a ton of interest in IRL / community from beauty brands. Curious if that's on your radar too?"
- "Noticed you grabbed our Q1 beauty report. The data on community-led brands has been wild this year. Would love to hear what you're seeing on your end."
- "Hey [name], saw you downloaded our beauty report. One thing that keeps coming up in our research is how much IRL activations are driving brand loyalty with Gen Z. Is that something you're thinking about at [company]?"

Output exactly one JSON object with these fields:
- subject: short, casual subject line (no caps lock, no clickbait)
- body: the email body (3-5 sentences, ends with a question)

Return ONLY the JSON object, no markdown fencing."""

# ---------------------------------------------------------------------------
# Spam word check (from CLAUDE.md copy generator)
# ---------------------------------------------------------------------------

SPAM_WORDS = {
    "act now", "limited time", "expires", "urgent", "hurry",
    "last chance", "don't miss", "final notice",
    "free", "no cost", "100% free", "bonus", "cash",
    "earn money", "extra income", "financial freedom",
    "guarantee", "guaranteed", "risk free", "no obligation",
    "promise", "best price", "lowest price",
    "click here", "click below", "buy now", "order now",
    "call now", "apply now", "sign up free",
    "congratulations", "winner", "you've been selected",
    "exclusive offer", "special offer", "limited offer",
    "one time offer", "this isn't spam",
    "sales", "stop",
}


def has_spam_words(text: str) -> list[str]:
    """Return list of spam words found in text."""
    found = []
    for word in SPAM_WORDS:
        if re.search(rf'\b{re.escape(word)}\b', text, re.IGNORECASE):
            found.append(word)
    return found


# ---------------------------------------------------------------------------
# Email generation
# ---------------------------------------------------------------------------

def build_prompt(contact: dict) -> str:
    """Build the user prompt for a single contact."""
    first_name = contact.get("Name", "").split()[0] if contact.get("Name") else ""
    company = contact.get("Company", "")
    role = contact.get("Role", "")
    category = contact.get("Category", "")
    sources = contact.get("Sources", "")

    # Map source names to friendlier references
    source_refs = []
    sources_lower = sources.lower()
    if "magnetic" in sources_lower or "top 25" in sources_lower:
        source_refs.append("Magnetic 100 / Top 25 list")
    if "beauty report" in sources_lower:
        source_refs.append("beauty quarterly report")
    if "cpg" in sources_lower:
        source_refs.append("CPG report")
    if "screen time" in sources_lower:
        source_refs.append("Screen Time report")
    if not source_refs:
        source_refs.append("dcdx research")

    source_str = " and ".join(source_refs)

    parts = [f"Write a warm outreach email to {first_name}."]
    if company:
        parts.append(f"They work at {company}.")
    if role:
        parts.append(f"Their role is {role}.")
    if category:
        parts.append(f"They are in the {category} space.")
    parts.append(f"They engaged with our {source_str}.")
    parts.append("Keep it short, casual, and end with a genuine question about IRL / community trends in beauty.")

    return " ".join(parts)


def generate_email(client: anthropic.Anthropic, contact: dict) -> dict:
    """Generate one outreach email for a contact. Returns {subject, body} or empty."""
    prompt = build_prompt(contact)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()

        # Parse JSON (handle potential markdown fencing)
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        result = json.loads(text)

        subject = result.get("subject", "")
        body = result.get("body", "")

        # Spam check
        spam_in_subject = has_spam_words(subject)
        spam_in_body = has_spam_words(body)
        if spam_in_subject or spam_in_body:
            all_spam = spam_in_subject + spam_in_body
            print(f"    WARNING: spam words detected: {all_spam}")

        # Clean: remove em-dashes, emojis
        body = body.replace("\u2014", ",").replace("\u2013", ",")
        body = re.sub(r'[\U0001F600-\U0001F9FF\U0001FA00-\U0001FA6F\U00002702-\U000027B0]', '', body)

        # Ensure sign-off
        if not body.rstrip().endswith("Andrew"):
            body = body.rstrip()
            if not body.endswith("\n"):
                body += "\n\n"
            else:
                body += "\n"
            body += "Andrew"

        return {"subject": subject, "body": body}

    except json.JSONDecodeError as e:
        print(f"    JSON parse error: {e}")
        return {}
    except Exception as e:
        print(f"    Generation error: {e}")
        return {}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set in environment.")
        print("Set it in your environment or .env file.")
        sys.exit(1)

    # Load enriched contacts
    if not os.path.exists(INPUT_PATH):
        print(f"ERROR: {INPUT_PATH} not found.")
        print("Run enrich_dcdx_contacts.py first.")
        sys.exit(1)

    with open(INPUT_PATH, newline="") as f:
        reader = csv.DictReader(f)
        contacts = list(reader)

    print(f"Loaded {len(contacts)} contacts from enriched CSV")

    # Filter to High and Medium confidence
    eligible = [c for c in contacts if c.get("Confidence") in CONFIDENCE_FILTER]
    print(f"Filtered to {len(eligible)} contacts (High + Medium confidence)")

    # Further filter: need at least a first name
    eligible = [c for c in eligible if c.get("Name", "").strip()]
    print(f"After name filter: {len(eligible)} contacts")

    # Optional: --limit flag for testing
    limit = None
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
            eligible = eligible[:limit]
            print(f"Limited to first {limit} contacts (test mode)")
        except ValueError:
            pass

    # Generate emails
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    results = []
    errors = 0

    print(f"\nGenerating {len(eligible)} outreach emails...\n")

    for i, contact in enumerate(eligible):
        first_name = contact.get("Name", "").split()[0]
        company = contact.get("Company", "unknown")
        print(f"  [{i+1}/{len(eligible)}] {first_name} @ {company}...", end=" ")

        email_draft = generate_email(client, contact)
        if email_draft:
            results.append({
                "Email": contact["Email"],
                "Name": contact["Name"],
                "Company": contact.get("Company", ""),
                "Role": contact.get("Role", ""),
                "Category": contact.get("Category", ""),
                "Confidence": contact.get("Confidence", ""),
                "Sources": contact.get("Sources", ""),
                "Subject": email_draft["subject"],
                "Body": email_draft["body"],
            })
            print("done")
        else:
            errors += 1
            print("FAILED")

        # Progress update
        if (i + 1) % BATCH_LOG_INTERVAL == 0:
            print(f"\n  --- Progress: {i+1}/{len(eligible)} generated, {errors} errors ---\n")

    # Write output
    fieldnames = ["Email", "Name", "Company", "Role", "Category", "Confidence",
                  "Sources", "Subject", "Body"]
    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"  Generated: {len(results)} emails")
    print(f"  Errors:    {errors}")
    print(f"  Saved to:  {OUTPUT_PATH}")
    print(f"{'='*60}")

    # Print a few samples
    print(f"\n--- Sample drafts ---\n")
    for draft in results[:3]:
        print(f"To: {draft['Name']} <{draft['Email']}>")
        if draft['Company']:
            print(f"    ({draft['Company']}, {draft['Role']})")
        print(f"Subject: {draft['Subject']}")
        print(f"Body:\n{draft['Body']}")
        print()


if __name__ == "__main__":
    main()
