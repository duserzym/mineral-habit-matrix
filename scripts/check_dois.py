"""Check every reference DOI against Crossref and print registered vs. cited titles.

    python scripts/check_dois.py
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
bad = 0
for f in sorted((ROOT / "site" / "data").glob("*.json")):
    if f.name == "index.json":
        continue
    for r in json.loads(f.read_text()).get("references", []):
        doi = r.get("doi")
        if not doi:
            continue
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mineral-habit-matrix (doi check)"})
            msg = json.load(urllib.request.urlopen(req, timeout=30))["message"]
            title = (msg.get("title") or [""])[0]
            year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
            cited = re.sub("<[^>]+>", "", r["citation"])
            print(f"OK   {f.stem:9s} {doi}\n     crossref: {year} {title}\n     cited:    {cited[:160]}")
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"FAIL {f.stem:9s} {doi}: {e}")
print(f"\n{bad} DOI lookups failed")
sys.exit(1 if bad else 0)
