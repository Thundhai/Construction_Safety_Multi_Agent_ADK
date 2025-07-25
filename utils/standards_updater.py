import requests
import os
import json
import time

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'standards_cache.json')
CACHE_TTL = 60 * 60 * 24  # 24 hours

DEFAULT_STANDARDS = {
    "OSHA": "https://www.osha.gov/laws-regs/regulations/standardnumber",
    "ISO 45001": "https://www.iso.org/iso-45001-occupational-health-and-safety.html",
    "HSE": "https://www.hse.gov.uk/legislation/hswa.htm"
}

def fetch_online_standards():
    # Placeholder: In production, parse and extract actual standards text/rules from these URLs or APIs
    standards = {}
    for name, url in DEFAULT_STANDARDS.items():
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                standards[name] = f"Fetched from {url} (content length: {len(resp.text)})"
            else:
                standards[name] = f"Failed to fetch from {url} (status {resp.status_code})"
        except Exception as e:
            standards[name] = f"Error fetching from {url}: {e}"
    return standards

def load_cached_standards():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if time.time() - data.get('timestamp', 0) < CACHE_TTL:
                return data.get('standards', DEFAULT_STANDARDS)
    return None

def save_cached_standards(standards):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'timestamp': time.time(), 'standards': standards}, f)

def get_latest_standards(force_refresh=False):
    if not force_refresh:
        cached = load_cached_standards()
        if cached:
            return cached
    standards = fetch_online_standards()
    save_cached_standards(standards)
    return standards
