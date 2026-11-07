"""Build/refresh daily EUR, USD, GBP, CAD -> TND history (mid-market, open data) from the
@fawazahmed0/currency-api npm releases. Only downloads days missing from remit/fx_history.json."""
import io, json, os, subprocess, tarfile, urllib.request, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "remit", "fx_history.json")
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 120
CUR = ["eur", "usd", "gbp", "cad"]
hist = json.load(open(OUT)) if os.path.exists(OUT) else {}
tags = json.loads(subprocess.run(["npm", "view", "@fawazahmed0/currency-api", "dist-tags", "--json"], capture_output=True, text=True, check=True).stdout)
dates = sorted(k for k in tags if k[:2] == "20")[-DAYS:]
new = 0
for d in dates:
    if d in hist: continue
    v = tags[d]
    url = f"https://registry.npmjs.org/@fawazahmed0/currency-api/-/currency-api-{v}.tgz"
    try:
        data = urllib.request.urlopen(url, timeout=60).read()
        with tarfile.open(fileobj=io.BytesIO(data)) as t:
            row = {}
            for c in CUR:
                j = json.load(t.extractfile(f"package/v1/currencies/{c}.min.json"))
                row[c] = round(float(j[c]["tnd"]), 6)
        if all(1 < x < 10 for x in row.values()):
            hist[d] = row; new += 1
    except Exception as e:
        print("skip", d, e)
hist = {k: hist[k] for k in sorted(hist)[-DAYS:]}
json.dump(hist, open(OUT, "w"), indent=0)
last = max(hist)
json.dump({"rate": hist[last]["eur"], "date": last, "source": "fawazahmed0/currency-api (mid-market, daily)"},
          open(os.path.join(HERE, "remit", "fx.json"), "w"), indent=1)
print(f"{new} new days, {len(hist)} total, {min(hist)} → {last}: {hist[last]}")
