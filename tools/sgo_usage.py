"""Prints the SportsGameOdds account usage (read-only, one call)."""
import json, os, urllib.request, urllib.error
req = urllib.request.Request("https://api.sportsgameodds.com/v2/account/usage",
                             headers={"X-Api-Key": os.environ["SPORTSGAMEODDS_KEY"]})
try:
    print(json.dumps(json.load(urllib.request.urlopen(req, timeout=30)), indent=1)[:3000])
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:500])
