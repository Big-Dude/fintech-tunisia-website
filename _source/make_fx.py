"""Refresh the built-in EUR->TND fallback rate from the daily open dataset (@fawazahmed0/currency-api on npm).
The live page also fetches the rate itself each day; this only sets the value used if that fetch fails."""
import json, os, subprocess, tarfile, tempfile, sys
HERE = os.path.dirname(os.path.abspath(__file__))
with tempfile.TemporaryDirectory() as d:
    subprocess.run(["npm", "pack", "@fawazahmed0/currency-api@latest", "--silent"], cwd=d, check=True, capture_output=True)
    tgz = [f for f in os.listdir(d) if f.endswith(".tgz")][0]
    with tarfile.open(os.path.join(d, tgz)) as t:
        j = json.load(t.extractfile("package/v1/currencies/eur.min.json"))
rate, date = float(j["eur"]["tnd"]), j["date"]
assert 1 < rate < 10, rate
json.dump({"rate": round(rate, 6), "date": date, "source": "fawazahmed0/currency-api (mid-market, daily)"},
          open(os.path.join(HERE, "remit", "fx.json"), "w"), indent=1)
print("EUR/TND", rate, date)
