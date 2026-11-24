"""Clinic economics model for the Consilium leaner-diagnostics report.

All money is in constant 2026 naira (no inflation, no price growth). Every input is an
assumption stated in ASSUMPTIONS and printed in the report appendix. Cash view: operating cash
profit before tax, owner's drawings and depreciation; capex is counted separately.

Three single-consulting-room outpatient clinics (Lagos mainland, the draft's set-up):
  A  paper records, all tests sent to an outside lab
  B  paper records, small side-lab (basic blood count only), infectious-disease tests sent out
  C  EMR + desk-side RDTs + point-of-care (POC) analysers, all febrile work-up done in-room

Run:  python -I scripts/model.py   -> prints results and writes data/model.json
"""
import json, pathlib, copy

OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "model.json"

BASE = dict(
    visits_per_day=20,          # the draft's baseline (same demand for every model in the base case)
    days_per_year=300,          # 6 days x 50 weeks
    consult_fee=5000,           # draft
    drug_share=0.80,            # share of visits with a drug sale (assumption)
    drug_revenue=4000,          # draft
    drug_cogs=2500,             # draft: gross profit 1,500 on 4,000
    test_share=0.60,            # share of visits needing a lab work-up (assumption; draft implied 100%)
    ext_lab_price=6500,         # outside lab: malaria test 2,500 (Consilium price file, 2026) + full blood count 4,000 (assumption)
    ext_malaria_price=2500,
    b_inhouse_price=2000,       # draft: B keeps a basic blood count
    b_inhouse_cost=600,
    c_bundle_price=4500,        # draft: C diagnostic fee
    c_bundle_cost=1800,         # RDT + POC consumables per work-up (assumption; the draft's flat 300k/month implied ~580)
    supplies_per_visit=400,     # gloves, syringes, waste (not in draft)
    leakage=0.03,               # discounts and bad debt, share of revenue (not in draft)
    oncost=0.10,                # employer pension etc on gross pay
    pay=dict(doctor=400_000, nurse=200_000, mls=200_000, clerk=120_000),  # draft figures; replace with HCW Pay Check medians
    rent_year=dict(A=3_000_000, B=4_500_000, C=4_500_000),
    electricity_month=dict(A=150_000, B=180_000, C=180_000),
    admin_it_month=dict(A=40_000, B=40_000, C=120_000),
    compliance_month=dict(A=10_000, B=10_000, C=40_000),   # NDPA: applies to paper too; C adds audit, backups, DPO retainer
    equip_maint_month=dict(A=0, B=30_000, C=50_000),
    overhead_month=250_000,     # cleaning, security, water, licence renewals, accounting (not in draft)
    capex=dict(
        shared_power=400_000 + 4_200_000,   # 3-phase connection + 5kVA solar inverter (all three; draft)
        A_admin=500_000, B_admin=500_000, B_lab=1_000_000,
        C_it=1_300_000, C_diag=3_100_000, C_transition=1_000_000,  # transition (record conversion, training): not in draft
    ),
    fx_shock=0.0,               # % rise in imported consumable cost (C bundle, B reagents)
    c_disruption_months=0,      # months per year C cannot run in-house tests (falls back to sending out)
    c_volume_uplift=0.0,        # extra visits C attracts because it is faster (draft implied +167% via 4/hr; base 0)
)

ROLES = dict(
    A=dict(doctor=1, nurse=2, clerk=1),
    B=dict(doctor=1, nurse=2, mls=1, clerk=1),
    C=dict(doctor=1, nurse=2, mls=1, clerk=1),
)


def staff_year(p, m):
    return sum(p["pay"][r] * n for r, n in ROLES[m].items()) * (1 + p["oncost"]) * 12


def capex(p, m):
    c = p["capex"]
    return {
        "A": c["shared_power"] + c["A_admin"],
        "B": c["shared_power"] + c["B_admin"] + c["B_lab"],
        "C": c["shared_power"] + c["C_it"] + c["C_diag"] + c["C_transition"],
    }[m]


def run(p, m):
    """Annual cash P&L for model m."""
    visits = p["visits_per_day"] * p["days_per_year"]
    if m == "C":
        visits *= 1 + p["c_volume_uplift"]
    fx = 1 + p["fx_shock"]
    ts = p["test_share"]
    # diagnostics
    if m == "A":
        diag_rev, diag_cost = 0, 0
    elif m == "B":
        diag_rev, diag_cost = ts * p["b_inhouse_price"], ts * p["b_inhouse_cost"] * fx
    else:
        in_room = 1 - p["c_disruption_months"] / 12
        diag_rev = ts * p["c_bundle_price"] * in_room
        diag_cost = ts * p["c_bundle_cost"] * fx * in_room
    rev_visit = p["consult_fee"] + p["drug_share"] * p["drug_revenue"] + diag_rev
    cogs_visit = p["drug_share"] * p["drug_cogs"] + diag_cost + p["supplies_per_visit"]
    revenue = visits * rev_visit
    leak = revenue * p["leakage"]
    variable = visits * cogs_visit
    staff = staff_year(p, m)
    fixed = dict(
        staff=staff,
        rent=p["rent_year"][m],
        electricity=p["electricity_month"][m] * 12,
        admin_it=p["admin_it_month"][m] * 12,
        compliance=p["compliance_month"][m] * 12,
        equip_maint=p["equip_maint_month"][m] * 12,
        overhead=p["overhead_month"] * 12,
    )
    profit = revenue - leak - variable - sum(fixed.values())
    return dict(model=m, visits=visits, rev_visit=rev_visit, revenue=revenue, leak=leak, variable=variable,
                fixed=fixed, fixed_total=sum(fixed.values()), profit=profit, margin=profit / revenue,
                capex=capex(p, m), diag_rev_visit=diag_rev, diag_cost_visit=diag_cost,
                gross_per_visit=rev_visit - cogs_visit - rev_visit * p["leakage"])


def compare(p):
    a, b, c = run(p, "A"), run(p, "B"), run(p, "C")
    d_profit = c["profit"] - a["profit"]
    d_capex = c["capex"] - a["capex"]
    payback = (d_capex / d_profit * 12) if d_profit > 0 else None
    return dict(A=a, B=b, C=c, d_profit=d_profit, d_capex=d_capex, payback_months=payback)


def with_(**kw):
    p = copy.deepcopy(BASE)
    for k, v in kw.items():
        p[k] = v
    return p


def patient_episode(p):
    """Cash a family pays for one febrile visit (all costs the family bears), plus time."""
    drugs = p["drug_revenue"]  # the draft's 4,000 for a malaria presentation
    transport = 2000           # assumption: one ₦1,000 return trip per extra stop
    return dict(
        A=dict(consult=p["consult_fee"], tests=p["ext_lab_price"], drugs=drugs, transport=2 * 1000, hours=5.75),
        B=dict(consult=p["consult_fee"], tests=p["b_inhouse_price"] + p["ext_malaria_price"], drugs=drugs, transport=1000, hours=4.0),
        C=dict(consult=p["consult_fee"], tests=p["c_bundle_price"], drugs=drugs, transport=0, hours=1.25),
    )


def main():
    res = {"assumptions": BASE}
    base = compare(BASE)
    res["base"] = base
    res["episode"] = patient_episode(BASE)

    # break-even and payback by volume
    vol = []
    for v in range(6, 41):
        r = compare(with_(visits_per_day=v))
        vol.append(dict(v=v, d_profit=r["d_profit"], payback=r["payback_months"], A=r["A"]["profit"], C=r["C"]["profit"]))
    res["by_volume"] = vol
    res["by_volume_uplift20"] = [dict(v=v, payback=compare(with_(visits_per_day=v, c_volume_uplift=0.20))["payback_months"]) for v in range(6, 41)]
    res["by_volume_fx"] = [dict(v=v, payback=compare(with_(visits_per_day=v, fx_shock=0.30))["payback_months"]) for v in range(6, 41)]
    be = next((x["v"] for x in vol if x["d_profit"] > 0), None)
    res["breakeven_visits_per_day"] = be

    # scenarios
    sc = [
        ("Base case", with_()),
        ("Faster service brings 20% more visits", with_(c_volume_uplift=0.20)),
        ("Only 40% of visits need a work-up", with_(test_share=0.40)),
        ("Imported consumables up 30%", with_(fx_shock=0.30)),
        ("Two months a year without cartridges", with_(c_disruption_months=2)),
        ("Downside: 40% work-up share and +30% cost", with_(test_share=0.40, fx_shock=0.30)),
        ("Clinic sees only 12 patients a day", with_(visits_per_day=12)),
    ]
    res["scenarios"] = [dict(name=n, d_profit=compare(p)["d_profit"], payback=compare(p)["payback_months"],
                             C=compare(p)["C"]["profit"], A=compare(p)["A"]["profit"]) for n, p in sc]

    # tornado: one input at a time, low/high, effect on annual extra profit of C over A
    t = [
        ("Patients per day (12 / 28)", dict(visits_per_day=12), dict(visits_per_day=28)),
        ("Faster service: extra visits (0% / +30%)", dict(c_volume_uplift=0.0), dict(c_volume_uplift=0.30)),
        ("Share of visits with a work-up (40% / 80%)", dict(test_share=0.40), dict(test_share=0.80)),
        ("Consumable cost per work-up (₦3,000 / ₦1,000)", dict(c_bundle_cost=3000), dict(c_bundle_cost=1000)),
        ("Price charged for the work-up (₦3,500 / ₦5,500)", dict(c_bundle_price=3500), dict(c_bundle_price=5500)),
        ("Months without cartridges (3 / 0)", dict(c_disruption_months=3), dict(c_disruption_months=0)),
        ("Imported cost shock (+50% / 0%)", dict(fx_shock=0.5), dict(fx_shock=0.0)),
    ]
    b0 = compare(BASE)["d_profit"]
    res["tornado"] = [dict(label=l, low=compare(with_(**lo))["d_profit"] - b0, high=compare(with_(**hi))["d_profit"] - b0) for l, lo, hi in t]
    res["tornado_base"] = b0

    # PHC illustration: recurrent cost of model C excluding rent (a public facility owns its building)
    c = base["C"]
    rec = c["variable"] + c["leak"] * 0 + sum(v for k, v in c["fixed"].items() if k != "rent")
    res["recurrent_C_excl_rent"] = rec
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")

    f = lambda x: f"{x/1e6:,.2f}M"
    print("BASE (₦/yr)")
    for m in "ABC":
        r = base[m]
        print(m, "visits", int(r["visits"]), "rev/visit", round(r["rev_visit"]), "revenue", f(r["revenue"]), "profit", f(r["profit"]),
              f"margin {r['margin']:.1%}", "capex", f(r["capex"]), "fixed", f(r["fixed_total"]))
    print("C-A profit", f(base["d_profit"]), "capex", f(base["d_capex"]), "payback months", base["payback_months"])
    print("breakeven visits/day", be)
    for s in res["scenarios"]:
        print(f"{s['name']:48s} dProfit {f(s['d_profit']):>9} payback {s['payback'] and round(s['payback'],1)}")
    for x in res["tornado"]:
        print(f"{x['label']:55s} {f(x['low']):>9} {f(x['high']):>9}")
    print("recurrent C excl rent", f(rec))
    print("episode", res["episode"])


if __name__ == "__main__":
    main()
