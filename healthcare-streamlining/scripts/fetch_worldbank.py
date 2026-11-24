"""Fetch the World Bank indicators used in the report (public API, no key). Writes data/worldbank.csv."""
import csv, json, urllib.request, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "worldbank.csv"
IND = {
 "SH.XPD.CHEX.PC.CD": "Health spending per person, US$ (current)",
 "SH.XPD.CHEX.PP.CD": "Health spending per person, PPP int$ (current)",
 "SH.XPD.CHEX.GD.ZS": "Health spending, % of GDP",
 "SH.XPD.OOPC.CH.ZS": "Out-of-pocket, % of health spending",
 "SH.XPD.GHED.GE.ZS": "Government health spending, % of government spending",
 "SH.STA.MMRT": "Maternal deaths per 100,000 live births (modelled)",
 "SP.DYN.LE00.IN": "Life expectancy at birth, years",
 "SP.POP.TOTL": "Population",
 "PA.NUS.FCRF": "Official exchange rate, LCU per US$ (period average)",
}
rows = []
for code, label in IND.items():
    url = f"https://api.worldbank.org/v2/country/NGA;RWA/indicator/{code}?format=json&date=2015:2024&per_page=100"
    d = json.load(urllib.request.urlopen(url, timeout=40))
    for r in d[1]:
        if r["value"] is not None:
            rows.append([r["countryiso3code"], code, label, r["date"], r["value"]])
rows.sort()
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["country", "indicator", "label", "year", "value"]); w.writerows(rows)
print(len(rows), "rows ->", OUT)
