"""
Devfolio scraper -- writes South India hackathons straight into Supabase.

Setup:
    pip install playwright
    python -m playwright install chromium

    Set two environment variables before running (don't hardcode secrets):

    Windows (cmd):
        set SUPABASE_URL=https://rbbkizumapqrphuzpwux.supabase.co
        set SUPABASE_SECRET_KEY=sb_secret_xxxxxxxxxxxxxxxxxxxxxxxx

Run:
    python scrape_devfolio_to_db.py

This uses the SECRET key (not the publishable one) because it needs
write access. Never put the secret key directly in this file or commit
it anywhere -- only pass it via the environment variable above.

Note on auth headers: Supabase's new sb_secret_ key format is NOT a JWT,
so it must be sent only in the "apikey" header -- NOT in "Authorization:
Bearer". Sending it in Authorization causes the request to silently be
treated as unauthenticated (anon role), which triggers RLS violations
on writes even though the key itself is valid.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

API_URL = "https://api.devfolio.co/api/search/hackathons"
REQUEST_TYPES = ["application_open"]
PAGE_SIZE = 20

SOUTH_INDIA_STATES = {
    "kerala": "Kerala",
    "tamil nadu": "Tamil Nadu",
    "karnataka": "Karnataka",
    "andhra pradesh": "Andhra Pradesh",
    "telangana": "Telangana",
    "puducherry": "Puducherry",
    "pondicherry": "Puducherry",
}

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
if SUPABASE_URL.endswith("/rest/v1"):
    SUPABASE_URL = SUPABASE_URL[: -len("/rest/v1")]
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY", "").strip()


def fetch_all_for_type(page, req_type: str):
    all_hits = []
    frm = 0
    while True:
        resp = page.request.post(
            API_URL,
            data=json.dumps({"type": req_type, "from": frm, "size": PAGE_SIZE}),
            headers={"content-type": "application/json"},
        )
        if resp.status != 200:
            print(f"  [warn] status {resp.status} for type={req_type} from={frm}")
            break
        data = resp.json()
        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            break
        all_hits.extend(hits)
        total = data.get("hits", {}).get("total", {}).get("value", 0)
        frm += PAGE_SIZE
        if frm >= total:
            break
    return all_hits


def matched_state(location: str):
    location_lower = (location or "").lower()
    for keyword, state_name in SOUTH_INDIA_STATES.items():
        if keyword in location_lower:
            return state_name
    return None


def slim(src):
    setting = src.get("hackathon_setting") or {}
    location = src.get("location")
    return {
        "source": "devfolio",
        "source_uuid": src.get("uuid"),
        "name": src.get("name"),
        "tagline": src.get("tagline"),
        "location": location,
        "state": matched_state(location),
        "is_online": bool(src.get("is_online")),
        "starts_at": src.get("starts_at"),
        "ends_at": src.get("ends_at"),
        "reg_starts_at": setting.get("reg_starts_at"),
        "reg_ends_at": setting.get("reg_ends_at"),
        "team_min": src.get("team_min"),
        "team_size": src.get("team_size"),
        "participants_count": src.get("participants_count"),
        "url": f"https://{setting.get('subdomain')}.devfolio.co/"
        if setting.get("subdomain")
        else None,
        "cover_img": src.get("cover_img"),
    }


def scrape_devfolio():
    all_raw = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        print("Establishing session (passing Cloudflare)...")
        for attempt in range(1, 4):
            try:
                page.goto(
                    "https://devfolio.co/hackathons/open",
                    wait_until="load",
                    timeout=60000,
                )
                break
            except Exception as e:
                print(f"  attempt {attempt} failed: {e}")
                if attempt == 3:
                    raise
                page.wait_for_timeout(3000)

        for req_type in REQUEST_TYPES:
            print(f"Fetching type={req_type} ...")
            hits = fetch_all_for_type(page, req_type)
            print(f"  got {len(hits)} hackathon(s)")
            all_raw.extend(hits)

        browser.close()

    seen = set()
    deduped = []
    for hit in all_raw:
        src = hit["_source"]
        uuid = src.get("uuid")
        if uuid in seen:
            continue
        seen.add(uuid)
        deduped.append(src)

    return [slim(s) for s in deduped]


def upsert_to_supabase(rows):
    if not SUPABASE_URL or not SUPABASE_SECRET_KEY:
        print("\n[ERROR] SUPABASE_URL and/or SUPABASE_SECRET_KEY env vars not set.")
        print("See the setup instructions at the top of this file.")
        sys.exit(1)

    endpoint = f"{SUPABASE_URL}/rest/v1/events?on_conflict=source,source_uuid"
    headers = {
        "apikey": SUPABASE_SECRET_KEY,
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=minimal",
    }

    body = json.dumps(rows).encode("utf-8")
    req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Supabase upsert failed: {e.code}")
        print(e.read().decode("utf-8", errors="replace"))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[ERROR] Could not reach Supabase: {e.reason}")
        sys.exit(1)

    if status not in (200, 201, 204):
        print(f"[ERROR] Supabase upsert returned unexpected status: {status}")
        sys.exit(1)

    print(f"Upserted {len(rows)} row(s) into Supabase.")


def cleanup_stale_events():
    """Remove events whose registration has already closed, or whose event
    dates have already passed (for the rare case reg_ends_at is missing)."""
    now_iso = datetime.now(timezone.utc).isoformat()

    def _delete(query):
        endpoint = f"{SUPABASE_URL}/rest/v1/events?{query}"
        headers = {
            "apikey": SUPABASE_SECRET_KEY,
            "Prefer": "return=representation",
        }
        req = urllib.request.Request(endpoint, headers=headers, method="DELETE")
        try:
            with urllib.request.urlopen(req) as resp:
                deleted = json.loads(resp.read().decode("utf-8") or "[]")
                return len(deleted)
        except urllib.error.HTTPError as e:
            print(f"  [warn] cleanup query failed: {e.code} {e.read().decode(errors='replace')}")
            return 0
        except urllib.error.URLError as e:
            print(f"  [warn] cleanup query failed: {e.reason}")
            return 0

    removed_1 = _delete(f"reg_ends_at=lt.{now_iso}")
    removed_2 = _delete(f"reg_ends_at=is.null&ends_at=lt.{now_iso}")

    total = removed_1 + removed_2
    if total:
        print(f"Cleanup: removed {total} stale event(s) (registration closed or event ended).")
    else:
        print("Cleanup: nothing stale to remove.")


def main():
    all_events = scrape_devfolio()
    south_india_events = [e for e in all_events if e["state"] is not None]

    print(f"\nTotal hackathons fetched: {len(all_events)}")
    print(f"South India matched: {len(south_india_events)}")

    if not south_india_events:
        print("Nothing to upsert.")
        return

    upsert_to_supabase(south_india_events)
    cleanup_stale_events()


if __name__ == "__main__":
    main()