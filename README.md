# Hack Scout

A live, self-updating aggregator of hackathons and tech events across South India (Kerala, Tamil Nadu, Karnataka, Andhra Pradesh, Telangana).

- `index.html` — the frontend (static, no build step, deploy as-is)
- `scrape_devfolio_to_db.py` — daily scraper, writes into Supabase
- `.github/workflows/scrape.yml` — runs the scraper automatically every day
- `manifest.json`, `sw.js`, `icons/` — PWA support (installable on phone home screen)

## Setup after cloning
1. Create a Supabase project with the `events` table (see project history/chat for schema)
2. Add repo secrets: `SUPABASE_URL`, `SUPABASE_SECRET_KEY` (use the **legacy service_role** key — the new `sb_secret_` format has a known RLS-bypass bug)
3. Deploy `index.html` + friends to Vercel (static site, no config needed)
