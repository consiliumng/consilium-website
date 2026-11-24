"""Data prep and SVG charts for the Consilium lean-clinic report (imported by build_report.py)."""
import csv, json, pathlib, html
import csv, json, pathlib, subprocess, sys, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD, DIST = ROOT / "build", ROOT / "dist"
DIST.mkdir(exist_ok=True)
M = json.load(open(ROOT / "data/model.json", encoding="utf-8"))
P = M["assumptions"]
B = M["base"]
WB = {}
for r in csv.DictReader(open(ROOT / "data/worldbank.csv", encoding="utf-8")):
    WB[(r["country"], r["indicator"], r["year"])] = float(r["value"])
wb = lambda c, i, y="2023": WB[(c, i, y)]

BLUE, DEEP, INK, LIME, SKY = "#3D35EB", "#2D28C8", "#123184", "#C8F5A0", "#2CB1F4"
GREY, MIST, LINE, CTXF, CTXL = "#4A4A63", "#F4F4F8", "#E0E0E8", "#BDBDDB", "#7E7EA6"

def m1(x):  # naira millions, one decimal
    return f"₦{x/1e6:,.1f}m"
def m0(x):
    return f"₦{x/1e6:,.0f}m"
def n(x):
    return f"₦{x:,.0f}"
def esc(s):
    return html.escape(s, quote=False)

# ---------------------------------------------------------------- numbers used in text
A, C, Bm = B["A"], B["C"], B["B"]
d_profit, d_capex, payback = B["d_profit"], B["d_capex"], B["payback_months"]
rec = M["recurrent_C_excl_rent"]
yrs100, yrs120 = 100e6 / rec, 120e6 / rec
sc = {s["name"]: s for s in M["scenarios"]}
up20 = sc["Faster service brings 20% more visits"]
mw_hour = 70000 / 176
ep = M["episode"]
tot = {k: ep[k]["consult"] + ep[k]["tests"] + ep[k]["drugs"] + ep[k]["transport"] for k in "ABC"}
ng_total = wb("NGA", "SH.XPD.CHEX.PC.CD") * wb("NGA", "SP.POP.TOTL") / 1e9
rw_total = wb("RWA", "SH.XPD.CHEX.PC.CD") * wb("RWA", "SP.POP.TOTL") / 1e9
assert abs(tot["A"] - 17500) < 1 and abs(tot["C"] - 13500) < 1

# waterfall parts: C minus A
contrib = lambda r: r["revenue"] - r["leak"] - r["variable"]
f_a, f_c = A["fixed"], C["fixed"]
wf = [
    ("Paper clinic\nprofit", A["profit"], "total"),
    ("Work-up margin\nkept in-house", contrib(C) - contrib(A), "up"),
    ("Lab scientist", -(f_c["staff"] - f_a["staff"]), "down"),
    ("Bigger premises\nand power", -((f_c["rent"] - f_a["rent"]) + (f_c["electricity"] - f_a["electricity"])), "down"),
    ("EMR, data and\ncompliance", -((f_c["admin_it"] - f_a["admin_it"]) + (f_c["compliance"] - f_a["compliance"])), "down"),
    ("Analyser\nupkeep", -(f_c["equip_maint"] - f_a["equip_maint"]), "down"),
    ("Lean clinic\nprofit", C["profit"], "total"),
]
assert abs(sum(v for _, v, t in wf[:-1][1:]) + A["profit"] - C["profit"]) < 1

# ---------------------------------------------------------------- svg helpers
def T(x, y, s, cls="t", anchor="start", extra=""):
    lines = str(s).split("\n")
    out = [f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}" {extra}>']
    for i, ln in enumerate(lines):
        out.append(f'<tspan x="{x}" dy="{0 if i == 0 else 1.15}em">{esc(ln)}</tspan>')
    out.append("</text>")
    return "".join(out)

def svg(w, h, body, label):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">{body}</svg>')

def rect(x, y, w, h, fill, rx=6, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" rx="{rx}" fill="{fill}" {extra}/>'

def line(x1, y1, x2, y2, col=LINE, w=1, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{d}/>'

# ---------------------------------------------------------------- charts
def chart_phc():
    W, H, L, R, Tp, Bt = 640, 290, 58, 16, 14, 40
    ymax = 240
    y = lambda v: Tp + (H - Tp - Bt) * (1 - v / ymax)
    o = []
    for g in range(0, 241, 60):
        o.append(line(L, y(g), W - R, y(g)))
        o.append(T(L - 8, y(g) + 4, f"₦{g}m" if g else "₦0", "ax", "end"))
    o.append(rect(L, y(120), W - R - L, y(100) - y(120), CTXF, 0, 'opacity=".55"'))
    o.append(T(L + 8, y(120) - 7, "Build cost: ₦100m to ₦120m (one-off)", "lbl", extra='fill="#4A4A63"'))
    bw, gap = 64, (W - L - R - 5 * 64) / 5
    for i in range(5):
        v = rec * (i + 1) / 1e6
        x = L + gap / 2 + i * (bw + gap)
        o.append(rect(x, y(v), bw, y(0) - y(v), BLUE, 8))
        o.append(T(x + bw / 2, y(v) - 7, f"₦{v:,.0f}m", "val", "middle"))
        o.append(T(x + bw / 2, H - 20, f"Year {i+1}", "ax", "middle"))
    o.append(T(L + 8, Tp + 14, f"Running costs pass ₦100m after {yrs100:.1f} years", "hd"))
    o.append(T(L + 8, Tp + 30, "Cumulative cost of running a lean clinic, before rent", "lbl", extra='fill="#4A4A63"'))
    return svg(W, H, "".join(o), "Cumulative running cost against one-off build cost")

def chart_two_gaps():
    W, H = 640, 250
    panels = [
        ("Health spending\nper person\n(PPP int$, 2023)", "SH.XPD.CHEX.PP.CD", lambda v: f"{v:,.0f}"),
        ("Share of health\nspending paid out\nof pocket (2023)", "SH.XPD.OOPC.CH.ZS", lambda v: f"{v:.0f}%"),
        ("Maternal deaths per\n100,000 births\n(2023)", "SH.STA.MMRT", lambda v: f"{v:,.0f}"),
        ("Life expectancy\nat birth, years\n(2023)", "SP.DYN.LE00.IN", lambda v: f"{v:.1f}"),
    ]
    o, pw = [], W / 4
    for i, (title, ind, fmt) in enumerate(panels):
        nv, rv = wb("NGA", ind), wb("RWA", ind)
        mx = max(nv, rv) * 1.12
        x0 = i * pw + 14
        base_y, top = 196, 74
        hh = lambda v: (base_y - top) * v / mx
        o.append(T(x0, 14, title, "pt"))
        o.append(line(x0, base_y, x0 + pw - 28, base_y, LINE))
        for j, (val, col, nm) in enumerate([(nv, BLUE, "Nigeria"), (rv, CTXF, "Rwanda")]):
            bx = x0 + 6 + j * 62
            o.append(rect(bx, base_y - hh(val), 50, hh(val), col, 8))
            o.append(T(bx + 25, base_y - hh(val) - 7, fmt(val), "val", "middle"))
            o.append(T(bx + 25, base_y + 16, nm, "ax", "middle"))
    return svg(W, H, "".join(o), "Nigeria and Rwanda: spending per person, out-of-pocket share, maternal deaths and life expectancy")

def chart_journey():
    W, H = 640, 170
    x0, x1 = 104, 626
    sc_ = (x1 - x0) / 6.0 / 60  # px per minute
    trad = [("Find file", 45), ("Wait to see doctor", 120), ("Consult", 15), ("Trip to lab", 30), ("Wait for results", 90), ("Pay, drugs", 45)]
    lean = [("Digital file", 2), ("Wait", 25), ("Consult", 10), ("Tests in room", 20), ("Review, pay, drugs", 18)]
    o = []
    for hr in range(0, 7):
        gx = x0 + hr * 60 * sc_
        o.append(line(gx, 36, gx, 124, LINE))
        o.append(T(gx, 142, f"{hr} h", "ax", "middle"))
    o.append(T(6, 62, "Traditional\nclinic", "lbl2", extra='font-weight="600"'))
    o.append(T(6, 110, "Lean clinic", "lbl2", extra='font-weight="600"'))
    x = x0
    shades = [CTXL, CTXF]
    for i, (nm, mn) in enumerate(trad):
        w = mn * sc_
        o.append(rect(x, 46, w - 2, 32, shades[i % 2], 4))
        tc = 'fill="#fff"' if i % 2 == 0 else 'fill="#123184"'
        if w > 55:
            o.append(T(x + w / 2 - 1, 60, nm, "seg", "middle", tc))
            o.append(T(x + w / 2 - 1, 73, f"{mn} min", "seg", "middle", tc))
        else:
            cx = x + w / 2 - 1
            if i == 2:
                o.append(line(cx, 22, cx, 46, CTXL))
                o.append(T(cx - 4, 18, f"{nm} {mn} min", "seg", "end", 'fill="#123184"'))
            else:
                o.append(line(cx, 22, cx, 46, CTXL))
                o.append(T(cx + 4, 18, f"{nm} {mn} min", "seg", "start", 'fill="#123184"'))
        x += w
    o.append(T(6, 88, "5 h 45 min", "val", extra='fill="#4A4A63"'))
    x = x0
    for nm, mn in lean:
        w = mn * sc_
        o.append(rect(x, 88, max(w - 1, 2), 28, BLUE, 4))
        x += w
    o.append(T(x + 8, 107, "About 1 h 15 min", "val", extra='fill="#3D35EB"'))
    return svg(W, H, "".join(o), "Time spent in a traditional clinic visit compared with a lean one")

def chart_patient_cost():
    W, H = 640, 250
    L, bw = 70, 96
    ymax = 20000
    y = lambda v: 24 + (170 - 24) * (1 - v / ymax)
    cols = dict(consult=CTXF, tests=BLUE, drugs=CTXL, transport=SKY)
    names = dict(consult="Consultation", tests="Tests", drugs="Drugs", transport="Transport")
    o = []
    for g in (0, 5000, 10000, 15000, 20000):
        o.append(line(L, y(g), W - 150, y(g)))
        o.append(T(L - 8, y(g) + 4, f"₦{g//1000}k" if g else "₦0", "ax", "end"))
    xs = {"A": L + 24, "B": L + 24 + 130, "C": L + 24 + 260}
    labels = {"A": "Paper clinic,\nlab outside", "B": "Paper clinic,\nside-lab", "C": "Lean clinic"}
    for k in "ABC":
        acc = 0
        for s in ("consult", "tests", "drugs", "transport"):
            v = ep[k][s]
            if v <= 0:
                continue
            o.append(rect(xs[k], y(acc + v), bw, y(acc) - y(acc + v), cols[s], 0, ""))
            tc = "#fff" if s in ("tests", "drugs") else INK
            if y(acc) - y(acc + v) > 16:
                o.append(T(xs[k] + bw / 2, (y(acc) + y(acc + v)) / 2 + 4, f"₦{v:,.0f}", "seg", "middle", f'fill="{tc}"'))
            acc += v
        o.append(T(xs[k] + bw / 2, y(acc) - 8, f"₦{acc:,.0f}", "val", "middle"))
        o.append(T(xs[k] + bw / 2, 188, labels[k], "ax", "middle", 'font-weight="600"'))
        hrs = ep[k]["hours"]
        o.append(T(xs[k] + bw / 2, 220, f"{hrs:g} h in the clinic", "lbl", "middle"))
        o.append(T(xs[k] + bw / 2, 234, f"≈ ₦{hrs*mw_hour:,.0f} of time", "ax", "middle"))
    yy = 38
    for s in ("transport", "drugs", "tests", "consult"):
        o.append(rect(W - 138, yy - 10, 12, 12, cols[s], 3))
        o.append(T(W - 120, yy, names[s], "lbl"))
        yy += 22
    return svg(W, H, "".join(o), "Cash cost to the family of one febrile visit, by clinic model")

def chart_capex():
    W, H = 640, 270
    L, bw = 58, 100
    ymax = 12
    y = lambda v: 20 + (H - 90 - 20) * (1 - v / ymax)
    c = P["capex"]
    series = [
        ("Power and solar", CTXL, dict(A=c["shared_power"], B=c["shared_power"], C=c["shared_power"])),
        ("Records, filing", CTXF, dict(A=c["A_admin"], B=c["B_admin"], C=0)),
        ("Computers, network", SKY, dict(A=0, B=0, C=c["C_it"])),
        ("Lab, diagnostics", BLUE, dict(A=0, B=c["B_lab"], C=c["C_diag"])),
        ("Changeover, training", INK, dict(A=0, B=0, C=c["C_transition"])),
    ]
    o = []
    for g in (0, 3, 6, 9, 12):
        o.append(line(L, y(g), 470, y(g)))
        o.append(T(L - 8, y(g) + 4, f"₦{g}m" if g else "₦0", "ax", "end"))
    xs = {"A": L + 24, "B": L + 24 + 140, "C": L + 24 + 280}
    names = {"A": "Paper clinic,\nlab outside", "B": "Paper clinic,\nside-lab", "C": "Lean clinic"}
    for k in "ABC":
        acc = 0
        for nm, col, d in series:
            v = d[k] / 1e6
            if v <= 0:
                continue
            o.append(rect(xs[k], y(acc + v), bw, y(acc) - y(acc + v), col, 0))
            if y(acc) - y(acc + v) > 15:
                o.append(T(xs[k] + bw / 2, (y(acc) + y(acc + v)) / 2 + 4, f"{v:.1f}", "seg", "middle", 'fill="#fff"' if col in (BLUE, INK, CTXL, SKY) else f'fill="{INK}"'))
            acc += v
        o.append(T(xs[k] + bw / 2, y(acc) - 8, f"₦{acc:.1f}m", "val", "middle"))
        o.append(T(xs[k] + bw / 2, H - 62, names[k], "ax", "middle", 'font-weight="600"'))
    yy = 30
    for nm, col, d in reversed(series):
        o.append(rect(484, yy - 10, 12, 12, col, 3))
        o.append(T(502, yy, nm, "lbl2"))
        yy += 30
    return svg(W, H, "".join(o), "Set-up cost by clinic model")

def chart_waterfall():
    W, H = 640, 300
    L, bw = 52, 58
    ymax = 24
    y = lambda v: 24 + (H - 96 - 24) * (1 - v / ymax)
    o = []
    for g in (0, 6, 12, 18, 24):
        o.append(line(L, y(g), W - 12, y(g)))
        o.append(T(L - 8, y(g) + 4, f"₦{g}m" if g else "₦0", "ax", "end"))
    gap = (W - L - 12 - len(wf) * bw) / len(wf)
    run_ = 0
    for i, (nm, v, kind) in enumerate(wf):
        x = L + gap / 2 + i * (bw + gap)
        vm = v / 1e6
        if kind == "total":
            top, bot, col = vm, 0, (CTXF if i == 0 else BLUE)
            run_ = vm
        elif kind == "up":
            bot, top, col = run_, run_ + vm, BLUE
            run_ += vm
        else:
            top, bot, col = run_, run_ + vm, CTXL
            run_ += vm
        o.append(rect(x, y(top), bw, y(bot) - y(top), col, 6))
        lab = f"₦{vm:,.1f}m" if kind == "total" else (f"+{vm:,.1f}" if vm > 0 else f"−{abs(vm):,.1f}")
        o.append(T(x + bw / 2, y(top) - 7, lab, "val", "middle"))
        o.append(T(x + bw / 2, H - 56, nm, "ax", "middle"))
        if i < len(wf) - 1:
            o.append(line(x + bw, y(run_), x + bw + gap, y(run_), CTXL, 1, "3 3"))
    return svg(W, H, "".join(o), "From paper clinic profit to lean clinic profit")

def chart_payback():
    W, H = 640, 310
    L, R, Tp, Bt = 54, 120, 16, 44
    xmax, ymax = 40, 60
    x = lambda v: L + (W - L - R) * (v - 6) / (xmax - 6)
    y = lambda v: Tp + (H - Tp - Bt) * (1 - min(v, ymax) / ymax)
    o = []
    for g in (0, 12, 24, 36, 48, 60):
        o.append(line(L, y(g), W - R, y(g)))
        o.append(T(L - 8, y(g) + 4, f"{g}", "ax", "end"))
    o.append(T(L, Tp - 4, "Months to pay back", "ax"))
    for v in (6, 10, 14, 20, 25, 30, 35, 40):
        o.append(T(x(v), H - 24, str(v), "ax", "middle"))
    o.append(T((L + W - R) / 2, H - 6, "Patients seen per day", "lbl", "middle"))
    o.append(line(x(14), Tp, x(14), H - Bt, INK, 1.2, "5 4"))
    o.append(T(x(14) + 6, Tp + 12, "Break-even: about 14 a day", "lbl", extra=f'fill="{INK}"'))
    o.append(line(x(20), Tp + 28, x(20), H - Bt, CTXL, 1, "2 4"))
    o.append(T(x(20) + 5, Tp + 40, "The draft's 20", "ax"))

    def poly(rows, col, w=2.5):
        pts = [(r_["v"], r_["payback"]) for r_ in rows if r_["payback"] is not None and r_["payback"] <= ymax]
        if not pts:
            return ""
        d = " ".join(f"{'M' if i == 0 else 'L'}{x(a):.1f},{y(b):.1f}" for i, (a, b) in enumerate(pts))
        return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>', pts[-1]
    for rows, col, lab in [
        (M["by_volume_uplift20"], SKY, "Faster service brings 20% more visits"),
        (M["by_volume"], BLUE, "Base case"),
        (M["by_volume_fx"], CTXL, "Imported costs up 30%"),
    ]:
        path, last = poly(rows, col)
        o.append(path)
        pv = {r_["v"]: r_["payback"] for r_ in rows}
        if lab.startswith("Faster"):
            o.append(T(x(7), y(44), lab, "lbl halo", extra=f'fill="{INK}" font-weight="600"'))
        else:
            o.append(T(x(27), y(pv[27]) - 11, lab, "lbl halo", extra=f'fill="{INK}" font-weight="600"'))
    return svg(W, H, "".join(o), "Months to pay back the lean set-up, by patients seen per day")

def chart_tornado():
    W, H = 640, 300
    rows = sorted(M["tornado"], key=lambda r: -(abs(r["high"] - r["low"])))
    x0, x1 = 270, 626
    lo, hi = -6, 14
    x = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    rh = 34
    o = [line(x(0), 16, x(0), 16 + rh * len(rows) + 4, INK, 1.4)]
    for g in (-4, 0, 4, 8, 12):
        o.append(T(x(g), 16 + rh * len(rows) + 22, f"{g:+d}" if g else "0", "ax", "middle"))
    o.append(T((x0 + x1) / 2, H - 6, "Change in the lean clinic's extra yearly profit, ₦m (base case: +2.8)", "lbl", "middle"))
    for i, r in enumerate(rows):
        yy = 22 + i * rh
        lowv, highv = r["low"] / 1e6, r["high"] / 1e6
        o.append(T(8, yy + 16, r["label"], "lbl2"))
        if lowv < 0:
            o.append(rect(x(lowv), yy, x(0) - x(lowv), 22, CTXL, 4))
            o.append(T(x(lowv) - 5, yy + 15, f"−{abs(lowv):.1f}", "seg", "end", f'fill="{INK}"'))
        if highv > 0:
            o.append(rect(x(0), yy, x(highv) - x(0), 22, BLUE, 4))
            o.append(T(x(highv) + 5, yy + 15, f"+{highv:.1f}", "seg", "start", f'fill="{INK}"'))
    return svg(W, H, "".join(o), "Which assumptions move the result most")

