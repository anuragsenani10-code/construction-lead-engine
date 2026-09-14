# Construction Lead Engine

Low-cost lead discovery and qualification engine for construction/BIM prospects.

## MVP flow

Filters → web discovery → website crawl → contact extraction → public-work-contact validation → pain-signal detection → lead scoring → CSV export.

### Default filters
- Location: New York, USA
- Industries: General Contractor, Construction Management, Architecture, Engineering, BIM, MEP
- Company size: 5–500
- Lead target: 50
- Decision-maker titles: Owner, President, CEO, VP, Director, Project Manager, Preconstruction Manager, Estimator, BIM Manager

## Important contact rule
The engine only records contact details that are publicly published for professional/business use. It does not guess private phone numbers or fabricate emails. Verification is evidence-based; `unverified` remains the value when evidence is insufficient.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main --state "New York" --limit 50 --query "construction contractor BIM"
```

For web discovery, set `SEARCH_API_KEY` for a supported search provider. Crawling uses Crawl4AI. The app stores results in SQLite and writes `output/leads.csv`.

## Output fields
Company, website, location, industry, decision maker, title, work email, direct business phone, email status, phone status, pain signals, evidence URLs, score, priority, reason, discovered at.
