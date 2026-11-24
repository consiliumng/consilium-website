"""Build the Consilium lean-clinic report in the house style of the US-Nigeria MOU report.

Style (taken from the MOU report): white A4 pages, Newsreader Bold blue numbered section headings,
Plus Jakarta Sans body, three-panel cover with the colour logo, contents page with blue page-number
circles, blue-ruled "key box" callouts, bordered tables with blue headers, a blue serif pull quote,
and an About Consilium back page.

Run:  python -I -X utf8 healthcare-streamlining/scripts/build_report.py
Needs: data/model.json (scripts/model.py), data/worldbank.csv (scripts/fetch_worldbank.py)
Out  : build/report.html, dist/Consilium-Lean-Clinic-Report-2026.pdf, dist/toc.json
"""
import sys, pathlib, subprocess, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_charts import *  # noqa: F401,F403
import report_charts as rc

ROOT, BUILD, DIST = rc.ROOT, rc.BUILD, rc.DIST
FONTS = (BUILD / "fonts2/fonts.css").read_text(encoding="utf-8").replace("url(", "url(fonts2/") if False else None
fonts_css = (BUILD / "fonts2/fonts.css").read_text(encoding="utf-8")
fonts_css = fonts_css.replace("url(", "url(fonts2/")

# ------------------------------------------------------------------ content helpers
fig_n = [0]
tab_n = [0]

def fig(head, body, src):
    fig_n[0] += 1
    return (f'<figure class="f"><p class="figt">Figure {fig_n[0]} — {head}</p>{body}'
            f'<p class="src">{src}</p></figure>')

def table_title(text):
    tab_n[0] += 1
    return f'<p class="figt tt">Table {tab_n[0]} — {text}</p>'

def neg(v):
    return "–" if abs(v) < 1 else "−" + m1(v)

def box(title, inner):
    return f'<div class="box"><p class="bt">{title}</p>{inner}</div>'

# ------------------------------------------------------------------ sections
SECTIONS = [
    "1. Introduction",
    "2. Two Gaps, Not One",
    "3. One Patient, Two Journeys",
    "4. Three Clinics, One Set of Books",
    "5. When the Lean Model Pays",
    "6. Where It Fits, and What Can Go Wrong",
    "7. What a ₦100 Million Health Centre Needs to Keep Running",
    "8. Making the Change",
    "9. Recommended Action Points by Audience",
    "10. Conclusion",
    "Appendix A. Assumptions",
    "Appendix B. Method, Limits and Sources",
]

def sec(i):  # heading with number baked into the SECTIONS list
    return f'<h2 id="s{i}">{esc(SECTIONS[i])}</h2>'

def cells(total, lit, cols):
    return '<div class="cells" style="grid-template-columns:repeat(%d,1fr)">%s</div>' % (
        cols, "".join(f'<i class="{"on" if k < lit else ""}"></i>' for k in range(total)))

def cover():
    bars = "".join(f'<div style="height:{rec*(i+1)/1e6/217*100:.0f}%"><span>{rec*(i+1)/1e6:.0f}</span></div>' for i in range(5))
    return f'''<section class="cover">
<div class="dots"></div>
<img class="logo" src="../../assets/consilium-logo.png" alt="Consilium">
<div class="pn p1"><div class="tag">Illustrative model</div><div class="big">14</div>
<div class="cap">patients a day: where a lean clinic starts to earn more than a paper one</div>{cells(20, 14, 4)}<div class="of">14 of the baseline 20 patients a day</div></div>
<div class="pn p2"><div class="tag">Who pays</div><div class="big">{wb("NGA","SH.XPD.OOPC.CH.ZS"):.0f}%</div>
<div class="cap">of Nigeria's health spending is paid by households out of pocket</div>{cells(100, 72, 10)}</div>
<div class="pn p3"><div class="tag">Running cost</div><div class="big">{m0(rec)}</div>
<div class="cap">a year to run a lean clinic, before rent</div><div class="bars">{bars}</div><div class="of">Cumulative ₦m, years 1 to 5</div></div>
<div class="ttl"><h1>The Lean Clinic, 2026: What Keeps a ₦100 Million Health Centre Running</h1>
<p>A Break-Even Guide to Electronic Records, Rapid Tests and Point-of-Care Diagnostics for Nigerian Clinic Operators and Primary Care Planners</p></div>
<div class="cnum">1</div></section>'''

def toc_page(pages):
    rows = "".join(
        f'<div class="tr"><span>{esc(s)}</span><b>{pages.get(s, "")}</b></div>' for s in SECTIONS)
    return f'<section class="tocpage"><div class="toc">{rows}</div></section>'

def body():
    o = []
    # ---------------- 1 Introduction
    o.append(f'''<section class="first">{sec(0)}
<p>Few questions about Nigerian health care have drawn as much attention lately as this one: what does it cost to build a functional primary health centre? Figures near ₦100 million are widely quoted. In 2022 an official of the National Primary Health Care Development Agency (NPHCDA) put a full-fledged centre, with solar power, a borehole and staff quarters, at about ₦120 million. Enugu State's ₦24 billion for 260 new centres works out at about ₦92 million each.</p>
<p>That is a fair answer to the question asked. It does not answer the question that decides whether the centre works: what does it cost to run, and who pays? A centre with no nurse on duty, no test kits and no records is a building, not a health centre. Those costs are not one-off. They arrive every year, and a clinic that cannot cover them will stop doing the work it was built for.</p>
<p>This report is written for the people who answer that second question. It speaks first to clinic operators, who must decide whether electronic medical records (EMRs), rapid diagnostic tests (RDTs) and point-of-care (POC) analysers will pay for themselves. It then turns to the planners, insurers and development partners who fund primary care and decide what a centre is given to work with.</p>
<p class="pq">A building is not a health centre. The bill that decides whether it works arrives every year afterwards.</p>
<p>The argument has three parts. First, Nigeria has a funding gap and a spending gap, and only the second is within a clinic's or a state's reach this year. Second, a lean clinic, one that keeps records electronically and does its routine tests in the consulting room, can cut the time and cost of a visit for the family. Third, for the operator the case is real but modest: it depends on patient volume, and we show where the break-even sits so that readers can test it against their own numbers.</p>
{box("Key Findings", f"""<ul>
<li><strong>Two gaps.</strong> Government health spending is {wb("NGA","SH.XPD.GHED.GE.ZS"):.1f}% of government spending against the 15% Abuja target, and households pay {wb("NGA","SH.XPD.OOPC.CH.ZS"):.0f}% of the bill. Yet per person Nigeria spends about as much as Rwanda, which has far better outcomes. How money is organised matters as well as how much there is.</li>
<li><strong>A day lost.</strong> In our illustrative case, a child with a fever takes about 5¾ hours to treat and costs the family {n(tot["A"])}, transport included. With tests done in the room it takes about 75 minutes and costs {n(tot["C"])}.</li>
<li><strong>Modest for the operator.</strong> The lean set-up costs {m1(C["capex"])} against {m1(A["capex"])} for a paper clinic. At 20 patients a day it earns about {m1(d_profit)} a year more and pays back in about {payback:.0f} months. Below about 14 patients a day it earns no more than a paper clinic. A small side-lab alone does not help.</li>
<li><strong>The biggest lever has the least evidence.</strong> If faster service brings 20% more patients, extra profit rises to about {m0(up20["d_profit"])} a year and payback falls to about {up20["payback"]:.0f} months. No Nigerian study we found has measured this.</li>
<li><strong>Running costs overtake the build.</strong> Running a lean clinic costs about {m0(rec)} a year before rent. That passes the ₦100 million to ₦120 million cost of a primary health centre in {yrs100:.1f} to {yrs120:.1f} years.</li></ul>""")}
<p>Section 2 sets out the two gaps. Section 3 follows one patient through two kinds of clinic. Sections 4 and 5 build the operator's economics and show when they work. Section 6 says where the model fits and what can go wrong. Section 7 turns to the ₦100 million health centre. Sections 8 and 9 cover the changeover and what each audience should do next.</p>
<p class="small">Everything in this report that concerns clinic economics is a model built on stated assumptions (Appendix A), in constant 2026 naira. It is not a forecast and it is not a national sample.</p>
</section>''')

    # ---------------- 2 Two gaps
    o.append(f'''<section>{sec(1)}
<p>Ask a clinic owner, a hospital director or a state health commissioner what is wrong with Nigerian health care, and most will say money. They are right. They are not describing the whole problem.</p>
<h3>2.1 The Funding Gap Is Real</h3>
<p>Government spending on health was {wb("NGA","SH.XPD.GHED.GE.ZS"):.1f}% of total government spending in 2023, against the target of 15% set by the Abuja Declaration of 2001. Households paid {wb("NGA","SH.XPD.OOPC.CH.ZS"):.0f}% of all health spending directly, so that illness is paid for at the point of care, out of income. External support is also changing: US funding for HIV and other programmes is moving towards Nigerian financing by 2030.</p>
<h3>2.2 Money Alone Does Not Explain the Outcomes</h3>
<p>Per person, Nigeria spent more than Rwanda in every year from 2015 to 2023. In 2023 it spent US${wb("NGA","SH.XPD.CHEX.PC.CD"):.0f} against US${wb("RWA","SH.XPD.CHEX.PC.CD"):.0f}, or int${wb("NGA","SH.XPD.CHEX.PP.CD"):.0f} against int${wb("RWA","SH.XPD.CHEX.PP.CD"):.0f} once local prices are taken into account. Yet Rwanda's maternal mortality was about a quarter of Nigeria's, and its people lived 13 years longer.</p>
{fig("Nigeria spends more per person than Rwanda, but households carry the bill and outcomes lag", chart_two_gaps(),
     "Source: World Bank, World Development Indicators (SH.XPD.CHEX.PP.CD, SH.XPD.OOPC.CH.ZS, SH.STA.MMRT, SP.DYN.LE00.IN), 2023, retrieved 24 November 2026. Maternal mortality is a modelled estimate. PPP int$ adjusts for local prices.")}
<p>The comparison does not mean that Rwanda's model can be copied. Rwanda is far smaller, pools household payments through insurance and receives substantial donor support. It shows only that how money is organised and used matters as much as how much there is. Totals are no help here: Nigeria's health spending was about US${ng_total:.0f} billion in 2023 and Rwanda's about US${rw_total:.1f} billion, which says nothing about efficiency.</p>
<h3>2.3 The Spending Gap</h3>
<p>The second deficit is one of use. Money already in the system is lost to repeat tests, slow paper records, courier delays and fragmented laboratory chains. Closing it does not replace closing the funding gap. But a clinic or a state can start on it this year, without waiting for new capital. The rest of this report is about that second gap.</p>
<p class="small">Exchange-rate note. Nigeria's US-dollar figures fall after the 2023 devaluation (the official rate averaged ₦645 per US$ in 2023 and ₦1,479 in 2024), so year-to-year dollar comparisons need care. Purchasing-power figures are steadier. The World Bank had no 2024 spending data at the time of writing.</p>
</section>''')

    # ---------------- 3 Patient journeys
    o.append(f'''<section>{sec(2)}
<p>To see where the spending gap shows up, follow one patient. Imagine Mrs Bola, a composite of the families who use small clinics, whose seven-year-old son wakes with a high fever. She suspects malaria.</p>
<h3>3.1 The Traditional Journey</h3>
<p>She reaches the clinic at 9:15 am. It takes 45 minutes to find her son's paper file. After a two-hour wait the doctor writes an order for a malaria test and the usual blood work, to be done at a partner laboratory. She travels there, waits 90 minutes for results, returns to the doctor, pays at the cashier and collects the drugs. It is almost 3 pm.</p>
<h3>3.2 The Lean Journey</h3>
<p>In a clinic with electronic records, desk-side rapid tests and a point-of-care analyser, the file opens in seconds. The doctor orders the tests, a nurse runs them in the room while the next patient is seen, and the doctor reviews the results within the same visit. The whole visit takes about 75 minutes.</p>
{fig("A visit that takes 5¾ hours can take about 75 minutes", chart_journey(),
     "Source: Consilium illustration based on the composite case in Section 3. The timings are assumed, not measured. Lean path: digital file 2 minutes, wait 25, consultation 10, tests in the room 20, review, payment and drugs 18.")}
<h3>3.3 What It Costs the Family</h3>
<p>The clinic's own bill is higher in the lean model, because the clinic now does the tests. The family's total is lower, because it no longer pays an outside laboratory or for the extra trips. A model that shows only the clinic's bill, ₦13,500 against ₦9,000, misses this.</p>
{fig(f"The lean visit costs the family {n(tot['A']-tot['C'])} less and saves about 4½ hours", chart_patient_cost(),
     f"Source: Consilium clinic model. Consultation and drugs from the draft case (₦5,000 and ₦4,000). Outside laboratory ₦6,500 = malaria test ₦2,500 (Consilium price file, 2026, grade C) + full blood count ₦4,000 (assumed). Transport ₦1,000 per return trip (assumed). Time valued at the ₦70,000 minimum wage over 176 hours, ₦{mw_hour:,.0f} an hour.")}
<p>The saving comes from doing the work in the room for about ₦1,800 of consumables, against a ₦6,500 outside laboratory bill. That gap is what the clinic and the patient share. If a clinic charged more than the outside laboratory, the family would not gain and the case would fail.</p>
</section>''')

    # ---------------- 4 Three clinics
    pl = lambda label, f, cls="": f'<tr class="{cls}"><td>{label}</td>' + "".join(f'<td class="num">{f(r)}</td>' for r in (A, Bm, C)) + "</tr>"
    o.append(f'''<section>{sec(3)}
<p>To see what changes for the operator, we model one single-room outpatient clinic on Lagos mainland in three set-ups, all in constant 2026 naira, with the same number of patients in each.</p>
{table_title("Three ways of running the same clinic")}
<table class="tbl keep"><tr><th style="width:15%"></th><th>A. Paper records, tests sent out</th><th>B. Paper records, small side-lab</th><th>C. Lean: EMR, rapid tests, analysers</th></tr>
<tr><td><strong>Records</strong></td><td>Paper files and cards</td><td>Paper files and cards</td><td>Electronic records, cloud-hosted</td></tr>
<tr><td><strong>Tests</strong></td><td>All sent to an outside laboratory</td><td>Basic blood count in-house; malaria and others sent out</td><td>Malaria and other rapid tests, plus analysers, all in the room</td></tr>
<tr><td><strong>Staff</strong></td><td>Doctor, 2 nurses, records clerk</td><td>Doctor, 2 nurses, laboratory scientist, records clerk</td><td>Doctor, 2 nurses, laboratory scientist, front-desk clerk</td></tr>
<tr><td><strong>Premises</strong></td><td>{m1(P["rent_year"]["A"])} a year</td><td>{m1(P["rent_year"]["B"])} a year (space for lab)</td><td>{m1(P["rent_year"]["C"])} a year (space for lab)</td></tr>
<tr><td><strong>Power</strong></td><td colspan="3">3-phase connection plus a 5kVA solar inverter in all three, which matches the NPHCDA minimum for a Level 2 facility.</td></tr></table>
<h3>4.1 Set-Up Cost</h3>
{fig(f"The lean clinic costs about twice as much to set up: {m1(C['capex'])} against {m1(A['capex'])}", chart_capex(),
     "Source: Consilium clinic model. Equipment figures are estimates from the draft case; we could not verify the analyser price or the brands it named. Entry-level point-of-care readers listed in Nigeria cost ₦310,000 to ₦850,000 (GoMed, Jiji, 2026). Rent is counted as a yearly cost, not as set-up capital.")}
<p>Most of the difference is the analysers and the computers. A tenth is the cost of changing over: converting paper records and training staff. Four choices in this model differ from the way these comparisons are often drawn. Rent is a running cost and is not counted twice. The inverter is counted once, in all three clinics. Drug costs are deducted, because revenue from drugs is not profit. And the paper clinic employs a records clerk, not a laboratory scientist it has no use for.</p>
<h3>4.2 What the Operator Earns</h3>
<p>At the baseline of 20 patients a day, six days a week, this is what each model earns in a year.</p>
{table_title("Annual operating cash profit, constant 2026 naira")}
<table class="tbl blue keep"><tr><th>Per year</th><th class="num">A. Paper</th><th class="num">B. Side-lab</th><th class="num">C. Lean</th></tr>
{pl("Patient visits", lambda r: f"{r['visits']:,.0f}")}
{pl("Revenue per visit (average)", lambda r: n(r["rev_visit"]))}
{pl("Revenue", lambda r: m1(r["revenue"]), "hl")}
{pl("Drugs, test consumables and supplies", lambda r: neg(r["variable"]))}
{pl("Discounts and bad debt (3%)", lambda r: neg(r["leak"]))}
{pl("Staff, including 10% on-costs", lambda r: neg(r["fixed"]["staff"]))}
{pl("Rent", lambda r: neg(r["fixed"]["rent"]))}
{pl("Electricity", lambda r: neg(r["fixed"]["electricity"]))}
{pl("EMR, internet, printing", lambda r: neg(r["fixed"]["admin_it"]))}
{pl("Data-protection compliance", lambda r: neg(r["fixed"]["compliance"]))}
{pl("Equipment upkeep and calibration", lambda r: neg(r["fixed"]["equip_maint"]))}
{pl("Cleaning, security, licences, accounting", lambda r: neg(r["fixed"]["overhead"]))}
{pl("Operating cash profit", lambda r: m1(r["profit"]), "tot")}
{pl("Margin", lambda r: f"{r['margin']:.0%}")}
{pl("Set-up cost", lambda r: m1(r["capex"]))}
</table>
<p class="small">Before tax, the owner's drawings and depreciation. Not included: registration and licence fees, professional indemnity, marketing. Staff pay uses placeholder figures (Appendix A).</p>
{fig(f"The lean clinic adds {m1(d_profit)} a year, and new fixed costs take back much of the gain", chart_waterfall(),
     "Source: Consilium clinic model, 20 patients a day, 300 days, 60% of visits needing a work-up, in-room price ₦4,500 and consumable cost ₦1,800 per work-up. Figures in ₦m a year.")}
{box("Two Findings the Usual Story Misses", f"""<ul>
<li>The side-lab clinic (B) earns <strong>no more than the paper clinic</strong>: {m1(Bm["profit"])} against {m1(A["profit"])}. A small lab adds as much cost as it keeps.</li>
<li>The lean clinic's advantage comes from doing the <strong>whole work-up in the room</strong>, not from any single machine. Keeping the work-up margin in-house adds about ₦9.2m a year. A laboratory scientist, bigger premises, EMR and compliance, and analyser upkeep take back about ₦6.4m.</li></ul>""")}
</section>''')

    # ---------------- 5 When it pays
    tab = "".join(
        f'<tr><td>{s["name"]}</td><td class="num">{"+" if s["d_profit"]>=0 else "−"}{m1(abs(s["d_profit"]))}</td>'
        f'<td class="num">{(str(round(s["payback"])) + " months") if s["payback"] and s["payback"]<=120 else "No payback"}</td></tr>'
        for s in M["scenarios"])
    o.append(f'''<section>{sec(4)}
<p>The question for an operator is not whether the lean model works in general, but whether it works at their patient numbers and with their costs. Payback is the extra set-up cost divided by the extra yearly profit. It is very long near break-even and short once volume is comfortable.</p>
<h3>5.1 Volume Decides</h3>
{fig("Below about 14 patients a day the lean set-up earns no more than a paper clinic", chart_payback(),
     "Source: Consilium clinic model. Payback = ₦" + f"{d_capex/1e6:.1f}m extra set-up cost ÷ extra yearly profit of the lean clinic over the paper clinic. Lines stop where payback exceeds 60 months or the lean clinic earns less. Constant 2026 naira.")}
<p>At 14 patients a day the lean clinic only just breaks even, and payback runs to many years. At 16 it is about five years, at 18 about two and a half, and at 20 about {payback:.0f} months. A clinic that sees fewer than 15 patients a day should start with rapid tests and a basic EMR and wait on the analysers.</p>
<h3>5.2 Scenarios</h3>
{table_title("The lean clinic compared with the paper clinic, by scenario")}
<table class="tbl blue keep"><tr><th>Case</th><th class="num">Extra profit a year</th><th class="num">Payback</th></tr>{tab}</table>
<h3>5.3 Which Assumptions Matter Most</h3>
{fig("Three assumptions matter most: volume, cost per test, and the share of visits that need a work-up", chart_tornado(),
     "Source: Consilium clinic model, change in the extra yearly profit of the lean clinic over the paper clinic. Each bar moves one input to the low and high value shown in its label, holding the rest at base case. The faster-service bar is an upside scenario: we have no Nigerian evidence on it.")}
<p>Two points follow. The consumable cost per work-up, which we assume at ₦1,800, is the number an operator most needs to confirm with written quotes: at ₦3,000 the base-case gain disappears. And the largest single lever, extra patients from faster service, is also the one we can least support. It is a reasonable hypothesis, because a patient who is diagnosed and treated in one visit is more likely to return and to refer others, but it needs measuring, not assuming.</p>
</section>''')

    # ---------------- 6 Where it fits, risks
    o.append(f'''<section>{sec(5)}
<h3>6.1 Where the Model Fits</h3>
<p>A break-even near 14 patients a day means the full lean set-up suits busy urban clinics. Quiet or rural facilities cannot spread the fixed costs and should share them.</p>
{table_title("Indicative set-up by type of facility")}
<table class="tbl keep"><tr><th style="width:23%">Type of facility</th><th style="width:40%">Indicative set-up</th><th>Why</th></tr>
<tr><td><strong>Busy urban clinic</strong><br>15 or more patients a day</td><td>EMR, rapid tests, one or two point-of-care analysers, in-house work-up</td><td>Volume spreads the fixed costs. This is the case modelled here.</td></tr>
<tr><td><strong>Primary health centre</strong><br>Lower volume</td><td>Basic EMR, rapid tests for malaria, HIV, syphilis, hepatitis B, glucose and pregnancy, 5kVA solar</td><td>Cheap tools with fast results. Analysers stay at a hub.</td></tr>
<tr><td><strong>Secondary hospital</strong></td><td>EMR linked to a laboratory system, analysers with quality control, rapid tests at triage</td><td>Volume supports analysers and a trained laboratory team.</td></tr>
<tr><td><strong>Hub and spokes</strong><br>Rural networks</td><td>Analysers at one hub; rapid tests and records at each spoke; sample and result transport</td><td>Shares the expensive equipment across several quiet sites. Needs funding that does not depend on each site's mark-up.</td></tr></table>
<p class="small">Indicative only, based on our judgement and the approach of the WHO Model List of Essential In Vitro Diagnostics, which matches tests to the level of care. Confirm against current national guidance.</p>
<h3>6.2 What Can Go Wrong</h3>
{table_title("Risks and what to do about them")}
<table class="tbl"><tr><th style="width:18%">Risk</th><th style="width:44%">Why it matters</th><th>What to do</th></tr>
<tr><td><strong>Imported consumables</strong></td><td>Cartridges and rapid tests are mostly imported. A 30% cost rise cuts the extra profit to {m1(sc["Imported consumables up 30%"]["d_profit"])}; two months a year without stock cuts it to {m1(sc["Two months a year without cartridges"]["d_profit"])}.</td><td>Reagent-rental or lease terms, a stock buffer of a few weeks, and a fallback to an outside laboratory during stock-outs.</td></tr>
<tr><td><strong>Power and downtime</strong></td><td>An EMR that stops when the power or the internet fails stops the clinic. Small clinics rarely have IT staff.</td><td>Solar with battery for the digital core, offline mode, a support contract with a response time, and paper downtime forms.</td></tr>
<tr><td><strong>Test accuracy</strong></td><td>Malaria and HIV rapid tests perform well, but HIV needs confirmatory testing. Rapid typhoid tests do not: a Cochrane review found them too inaccurate to replace blood culture. Some clinicians avoid rapid malaria tests over sensitivity concerns.</td><td>Use rapid tests where the evidence is good, follow national algorithms, and keep quality control on analysers.</td></tr>
<tr><td><strong>Data and regulation</strong></td><td>The Nigeria Data Protection Act treats health data as sensitive, on paper as well as on screen. The National Digital Health Architecture is a national blueprint; binding EMR certification rules were not settled at the time of writing, and a Digital Health Services Bill was pending.</td><td>Ask vendors for Data Protection Act compliance and interoperability support in writing, register with the data-protection regulator where required, and check laboratory licensing with the relevant council.</td></tr>
<tr><td><strong>People and habit</strong></td><td>Staff used to paper will revert to it under pressure. Record conversion is slow and some records will be lost.</td><td>Phase the change, keep paper as a fallback for the first weeks, and name a champion on each shift.</td></tr>
<tr><td><strong>Demand</strong></td><td>The case rests on patient numbers. A clinic seeing 12 patients a day does not break even on the lean set-up.</td><td>Start with rapid tests and a basic EMR. Add analysers when volume proves it.</td></tr></table>
</section>''')

    # ---------------- 7 ₦100m
    o.append(f'''<section>{sec(6)}
<p>The clinic model describes a private, single-room facility. A primary health centre is a public facility with different staffing, pay scales and services. The two are not the same, but the costs that make a clinic work are of the same kind, so the clinic model gives a useful order of magnitude.</p>
<h3>7.1 What the Build Cost Covers</h3>
<p>The NPHCDA's own specification for a Level 2 facility asks for a borehole with an overhead tank, accommodation of at least two bedrooms, and at least 5kVA of solar power for the main building. Those are one-off costs, and they are what the ₦100 million to ₦120 million quoted for a centre buys. They do not cover the staff who work there, the medicines, the test kits or the data system.</p>
<h3>7.2 What It Costs to Run</h3>
<p>Running our lean clinic costs about {m0(rec)} a year before rent: staff, drugs, consumables, power, IT and overheads. A public centre owns its building, so rent is left out. On that basis, cumulative running costs pass ₦100 million after {yrs100:.1f} years and ₦120 million after {yrs120:.1f} years.</p>
{fig(f"Running a lean clinic costs about {m0(rec)} a year, so its cumulative cost passes the build cost in year 3", chart_phc(),
     "Source: Consilium clinic model, Clinic C annual running cost excluding rent, ₦" + f"{rec/1e6:,.1f}m. Build cost: NPHCDA estimate reported by WikkiTimes and Voice of Nigeria (2022); Enugu State Government via Premium Times (₦24 billion for 260 centres, our arithmetic). Constant 2026 naira.")}
<h3>7.3 What Follows</h3>
<p>For planners, the question to put to any ₦100 million facility is not only what it costs to build, but who pays for years two to five and what they get for it. Setting up the lean kit of records, rapid tests and a point-of-care reader costs a few million naira, a few per cent of the build. It is the part of the budget that determines how much of the building's capacity is used. We found no current NPHCDA costing document to check the running-cost figure against, and public facilities differ from private clinics in staffing and free services, so the figure is a guide and not a government costing.</p>
</section>''')

    # ---------------- 8 Making the change
    o.append(f'''<section>{sec(7)}
<p>A realistic plan assumes the clinic stays open throughout and that some things will go wrong. The sequence below takes about seven weeks.</p>
{box("Weeks 1 to 3: Equipment and Power", """<ul><li><strong>Buy and install.</strong> Computers, network and router, the EMR, rapid test kits and analysers. A 5kVA solar inverter for the digital core. Technicians set up the EMR and connect the analysers so that results record automatically.</li>
<li><strong>Friction.</strong> Delivery delays, a vendor whose software does not meet the requirements, power that does not carry the load. The clinic keeps operating on paper.</li></ul>""")}
{box("Weeks 4 to 6: Records and Staff", f"""<ul><li><strong>Convert and train.</strong> Clerks scan and key in active files, starting with patients seen in the last year. Doctors, nurses and front-desk staff train on the new workflow.</li>
<li><strong>Friction.</strong> Slower days, errors in transcribed records, staff who revert to paper. Budget about {m1(P["capex"]["C_transition"])} for this phase.</li></ul>""")}
{box("Week 7 Onward: The New Workflow", """<ul><li><strong>Go live.</strong> Records open at the point of consultation. Blood samples are taken in the room and results return in about 15 minutes. Rapid tests are done at the desk for high-prevalence presentations.</li>
<li><strong>Review monthly.</strong> Track time per visit, tests per visit and consumable cost per work-up, and tell patients what has changed.</li></ul>""")}
<p>Leasing or reagent rental, rather than outright purchase, reduces the up-front cost and shifts some of the equipment risk to the supplier. Whether the terms are better in practice depends on quotes we do not have, so we have not modelled them.</p>
</section>''')

    # ---------------- 9 Action points
    o.append(f'''<section>{sec(8)}
{table_title("What each audience should do next")}
<table class="tbl blue keep"><tr><th style="width:21%">Audience</th><th style="width:18%">When</th><th>What to do</th></tr>
<tr><td><strong>Clinic operators</strong></td><td>Before buying</td><td>Count your real patients a day and the share of visits that need a work-up. Get written quotes for the consumable cost per test, not only the price of the machine. Start with rapid tests and a basic EMR, and add analysers when volume justifies them. Prefer reagent rental or a lease to buying outright.</td></tr>
<tr><td><strong>Primary care planners</strong></td><td>At the next budget cycle</td><td>Cost five years of running costs beside every build. Put records, rapid tests and solar power in the standard package. Use hub-and-spoke arrangements for analysers in low-volume areas. Make interoperability and data protection procurement criteria.</td></tr>
<tr><td><strong>Insurers and state ministries</strong></td><td>In the next tariff review</td><td>Pay for point-of-care tests in the tariff, so clinics do not depend on mark-ups. Keep the in-room price at or below the outside laboratory's. Use digital records to see what is spent per episode of care.</td></tr>
<tr><td><strong>Development partners</strong></td><td>Next funding round</td><td>Fund consumables, power and data as well as buildings. Back a 90-day pilot that measures time, family cost and tests per visit. Publish the results, whatever they show.</td></tr></table>
{box("The 90-Day Pilot", """<p>Three or four clinics for 90 days. Measure five things: the consumable cost per work-up, the share of visits that need one, patients per day before and after, the time from arrival to treatment, and what families pay per episode. These five numbers would turn this model into evidence. They are the assumptions that move the result most, and the ones this report cannot supply.</p>""")}
</section>''')

    # ---------------- 10 Conclusion
    o.append(f'''<section>{sec(9)}
<p>Nigeria's funding problem will take years to close. Its spending problem can start to close this year, in clinics and in budgets, by people willing to run the numbers.</p>
<p>The numbers in this report do not say that every clinic should buy the equipment. They say something narrower and more useful. For a busy clinic, doing the routine work-up in the consulting room can pay for itself within about two years, can save the family hours and money, and does so only if volume, uptake and consumable costs hold. For a quiet clinic it does not, and a shared model is the better route. For a ₦100 million health centre, the build is the beginning of the spending, not the end of it.</p>
<p>The honest next step is a pilot that replaces our assumptions with measurements. Until then, the most useful thing a clinic owner or a planner can do with this report is to put their own numbers into it.</p>
</section>''')

    # ---------------- appendix A
    pay = P["pay"]
    rows_a = [
        ("Patients per day (all clinics, base case)", f'{P["visits_per_day"]}', "Draft baseline. Same in every clinic in the base case."),
        ("Operating days a year", f'{P["days_per_year"]}', "Six days a week, 50 weeks. Assumption."),
        ("Consultation fee", n(P["consult_fee"]), "Draft. Public hospital consultations ran ₦3,500 to ₦4,200 in the Consilium price file (2024 to 2026)."),
        ("Visits with a drug sale", f'{P["drug_share"]:.0%}', "Assumption. Drug revenue ₦4,000, cost ₦2,500 (draft: gross profit ₦1,500)."),
        ("Visits needing a lab work-up", f'{P["test_share"]:.0%}', "Assumption. The draft implied every visit. Tested at 40% and 80%."),
        ("Outside laboratory price for the work-up", n(P["ext_lab_price"]), "Malaria test ₦2,500 (Consilium price file, 2026, grade C) plus full blood count ₦4,000 (assumed)."),
        ("In-room price, lean clinic", n(P["c_bundle_price"]), "Draft diagnostic fee. Tested at ₦3,500 and ₦5,500."),
        ("Consumable cost per work-up, lean clinic", n(P["c_bundle_cost"]), "Assumption, and the most important unknown. Tested at ₦1,000 and ₦3,000. Needs distributor quotes."),
        ("Side-lab price and cost, clinic B", f'{n(P["b_inhouse_price"])} / {n(P["b_inhouse_cost"])}', "Draft price; cost assumed."),
        ("Supplies per visit", n(P["supplies_per_visit"]), "Gloves, syringes, waste. Assumption."),
        ("Discounts and bad debt", f'{P["leakage"]:.0%}', "Share of revenue. Assumption."),
        ("Monthly pay: doctor, nurse, laboratory scientist, clerk", " / ".join(n(pay[k]) for k in ("doctor", "nurse", "mls", "clerk")), "Draft figures for the first three; clerk assumed. Placeholders to be replaced with HCW Pay Check medians (the 2025 survey median across six cadres was ₦250,000)."),
        ("Staff on-costs", f'{P["oncost"]:.0%}', "Employer pension and similar. Assumption."),
        ("Rent a year, A / B and C", f'{m1(P["rent_year"]["A"])} / {m1(P["rent_year"]["B"])}', "Draft. Converted flat on Lagos mainland; unsourced."),
        ("Electricity a month, A / B and C", f'{n(P["electricity_month"]["A"])} / {n(P["electricity_month"]["C"])}', "Draft."),
        ("EMR, internet, printing a month, A and B / C", f'{n(P["admin_it_month"]["A"])} / {n(P["admin_it_month"]["C"])}', "Draft."),
        ("Data compliance a month, A and B / C", f'{n(P["compliance_month"]["A"])} / {n(P["compliance_month"]["C"])}', "Assumption. The Data Protection Act applies to paper records too."),
        ("Equipment upkeep a month, B / C", f'{n(P["equip_maint_month"]["B"])} / {n(P["equip_maint_month"]["C"])}', "Assumption: calibration and quality control."),
        ("General overheads a month", n(P["overhead_month"]), "Cleaning, security, water, licence renewals, accounting. Assumption."),
        ("Set-up: power (all three)", m1(P["capex"]["shared_power"]), "3-phase ₦0.4m plus 5kVA solar inverter ₦4.2m (draft)."),
        ("Set-up: records, lab, IT, diagnostics", f'A {m1(P["capex"]["A_admin"])}; B {m1(P["capex"]["B_admin"]+P["capex"]["B_lab"])}; C {m1(P["capex"]["C_it"]+P["capex"]["C_diag"])}', "Draft figures. Changeover for C: " + m1(P["capex"]["C_transition"]) + " (assumed)."),
    ]
    tr = "".join(f"<tr><td>{a}</td><td class='num'>{b}</td><td>{c}</td></tr>" for a, b, c in rows_a)
    o.append(f'''<section>{sec(10)}
<p>All amounts are constant 2026 naira, with no inflation and no price growth. Profit is operating cash profit before tax, owner's drawings and depreciation. Set-up costs are counted separately. Payback is extra set-up cost divided by extra yearly profit. The model is in the project folder as <em>model.py</em> and reproduces every figure in this report.</p>
<table class="tbl blue dense"><tr><th style="width:31%">Input</th><th class="num" style="width:23%">Value</th><th>Source or status</th></tr>{tr}</table>
</section>''')

    # ---------------- appendix B
    src = [
        ("World Bank, World Development Indicators: health spending, out-of-pocket share, maternal mortality, life expectancy, population, exchange rate (retrieved 24 November 2026)", "https://data.worldbank.org/indicator/SH.XPD.CHEX.PC.CD"),
        ("NPHCDA director on ₦120 million for a standard primary health centre (2022), WikkiTimes", "https://wikkitimes.com/?p=92811"),
        ("The same figure, Voice of Nigeria", "https://von.gov.ng/?p=141865"),
        ("Enugu State: ₦24 billion for 260 Type-2 primary health centres, Premium Times", "https://www.premiumtimesng.com/news/more-news/874607-were-spending-n24-billion-for-260-new-phcs-in-enugu-official.html"),
        ("NPHCDA Level 2 facility requirements (borehole, accommodation, 5kVA solar)", "https://nphcda.gov.ng/?p=10395"),
        ("Cochrane review: rapid diagnostic tests for typhoid and paratyphoid fever (Wijedoru, Mallett and Parry, 2017)", "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD008892.pub2"),
        ("Nigeria Data Protection Act and GAID 2025, health data obligations (Mondaq)", "https://www.mondaq.com/nigeria/data-protection/1781892/data-dignity-digital-health-balancing-technological-innovation-and-patient-privacy"),
        ("National Digital Health Architecture (allAfrica, 2 October 2026)", "https://allafrica.com/stories/202610020381.html"),
        ("Point-of-care reader listings: Finecare FS-114 (GoMed)", "https://gomed.ng/product/finecare-machine-fs-114"),
        ("Malaria test prices at Ibadan and Lagos facilities (Tribune)", "https://tribuneonlineng.com/dangerous-trend-primary-health-care-under-threat-over-rising-cost-of-malaria-treatment"),
        ("Health workers avoiding rapid malaria tests over sensitivity concerns (Leadership)", "https://leadership.ng/nigerias-malaria-shame/"),
        ("Consilium, cost of healthcare across Nigerian elections, 2011 to 2026 (malaria test price, minimum wage)", "https://consilium.ng/reports/healthcare-cost/"),
        ("Consilium Nigerian Health Worker Report 2025 (median salary ₦250,000)", "https://hcw25.consilium.ng"),
    ]
    sl = "".join(f'<li>{esc(t)}.<br><a href="{u}">{u}</a></li>' for t, u in src)
    o.append(f'''<section>{sec(11)}
<h3>What This Report Is, and Is Not</h3>
<ul class="plain">
<li><strong>It is a model, not a forecast.</strong> It shows how a clinic's economics respond to patient volume, test uptake, prices and costs. It does not predict any clinic's results.</li>
<li><strong>It is not a national sample.</strong> The clinic is a single-room outpatient clinic on Lagos mainland. Public facilities differ.</li>
<li><strong>Several inputs are assumptions.</strong> The most important are the consumable cost per work-up, the share of visits needing one, patient volume and staff pay. The pay figures are placeholders pending HCW Pay Check medians.</li>
<li><strong>The speed benefit is unproven.</strong> We treat extra patients from faster service as an upside scenario, not the base case.</li>
<li><strong>The patient journey is illustrative.</strong> Timings are composite and assumed.</li>
<li><strong>Prices are mostly grade C.</strong> The malaria test price comes from our own price file, where recent prices rest on press and online listings. Equipment prices are listings, not quotes.</li>
<li><strong>Not covered:</strong> tax, licence fees, financing costs, inflation, programme-supplied tests and insurance payment delays.</li></ul>
<h3>Sources</h3>
<ul class="plain src-list">{sl}</ul>
</section>''')

    # ---------------- About
    o.append('''<section class="about"><img src="../../assets/consilium-logo.png" alt="Consilium" style="height:12mm;margin-bottom:5mm">
<h2 style="margin-top:0">About Consilium</h2>
<p>Consilium is a Nigerian healthcare intelligence platform on a mission to make sense of healthcare policy, finance, and the workforce — in a way that actually matters to real people.</p>
<p>Consilium started in 2023 as a newsletter trying to connect the dots between Nigeria's economic reality and the health of its people. The writing is still there — and still free to read at <a href="https://consilium.substack.com">consilium.substack.com</a>.</p>
<p><strong>2023.</strong> Published foundational pieces on health infrastructure, Nigeria's economic downturn and its downstream effects on patients, abortion legislation and public health, and a first look at state-level health budget disparities ahead of 2024.</p>
<p><strong>2024.</strong> Expanded analytical scope beyond clinical economics. Covered the Naira-USD exchange rate in depth — mapping a ten-month currency trajectory and its compounding effect on imported medicines and medical equipment. Built the audience that would carry the platform into its next phase.</p>
<p><strong>2025.</strong> Analysed the impact of the USA's withdrawal from the WHO on Nigeria's $40 million in global health funding. Profiled Nigeria's fastest-growing health innovators — the supply chain operators, premium hospitals, pharmacy aggregators, and manufacturers reshaping the market. Made the case for turning Detty December medical tourism into a structured healthcare marketplace.</p>
<p><strong>2026.</strong> Consilium evolves into an intelligence platform. Our first major data product — the Nigerian Healthcare Worker Survey — establishes national remuneration standards, working conditions, and the real state of Nigeria's health workforce across 537 respondents spanning six professional cadres and 36 states.</p>
<p>There is no shortage of opinion on Nigerian healthcare. There is a shortage of rigorous, primary data — and stories that connect evidence to the people building, funding, or simply trying to use the system. We are building the infrastructure to fix that.</p>
<p>Consilium is available for commissioned research partnerships with government agencies, development finance institutions, private organisations, health sector investors, and international organisations seeking primary data on Nigeria's healthcare system. If this work is relevant to what you are building or funding, we want to hear from you.</p>
<p>We are committed to the same thing we were committed to when we started: making sense of Nigerian healthcare in a way that actually matters. The tools are getting sharper, the data is getting richer, and the community is growing.</p>
<p>Email: office@consilium.ng</p></section>''')
    return "".join(o)

CSS = fonts_css + """
@page{size:A4;margin:19mm 18mm 22mm 18mm;@bottom-right{content:counter(page);font-family:'Plus Jakarta Sans','Segoe UI',Arial,sans-serif;font-size:10pt;color:#000;vertical-align:top;padding-top:6mm}}
@page cover{margin:0;@bottom-right{content:none}}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Plus Jakarta Sans','Segoe UI',Arial,sans-serif;font-size:10.3pt;line-height:1.52;color:#0b0b14;font-variant-numeric:tabular-nums}
h1,h2{font-family:'Newsreader',Georgia,serif;font-weight:700;letter-spacing:-.01em}
h2{font-size:17.5pt;line-height:1.14;color:#3D35EB;margin:6mm 0 3.2mm;break-after:avoid}
section.first h2,section.about h2{margin-top:0}
h3{font-size:10.8pt;font-weight:700;margin:4.6mm 0 1.6mm;break-after:avoid;color:#000}
p{margin:0 0 3mm}
p.small{font-size:8.2pt;line-height:1.45;color:#4A4A63}
strong{font-weight:700}
a{color:#3D35EB;text-decoration:none}
p.pq{font-family:'Newsreader',Georgia,serif;font-weight:700;font-size:15.5pt;line-height:1.22;color:#3D35EB;margin:5mm 0 5mm 0;padding:0 8mm 0 0;max-width:132mm}
.box{border-left:3px solid #3D35EB;padding:.5mm 0 .5mm 4.2mm;margin:4mm 0 4.4mm;break-inside:avoid}
.box .bt{font-weight:700;font-size:10.2pt;margin:0 0 1.6mm}
.box ul{margin:0 0 0 4mm;font-size:9.5pt;line-height:1.46}
.box li{margin-bottom:1.5mm}
.box p{font-size:9.5pt}
ul.plain{margin:0 0 3mm 5mm}
ul.plain li{margin-bottom:1.8mm}
ul.src-list{font-size:8.3pt;line-height:1.4;margin-left:5mm}
figure.f{margin:3.5mm 0 4.6mm;break-inside:avoid}
.figt{font-weight:700;font-size:9.9pt;line-height:1.35;margin:0 0 2.2mm;color:#000}
.figt.tt{margin-top:3mm;break-after:avoid}
.figt{break-after:avoid}
.src{font-style:italic;font-size:7.7pt;line-height:1.42;color:#4A4A63;margin:1.8mm 0 0}
.tbl{width:100%;border-collapse:collapse;font-size:8.8pt;line-height:1.42;margin:0 0 4mm}
.tbl th{font-weight:700;text-align:left;padding:2.1mm 2.6mm;border:1px solid #D4D4E0;vertical-align:bottom}
.tbl td{padding:2mm 2.6mm;border:1px solid #D4D4E0;vertical-align:top}
.tbl tr{break-inside:avoid}
.tbl.blue th{background:#3D35EB;color:#fff;border-color:#3D35EB}
.tbl .num{text-align:right;white-space:nowrap}
.tbl tr.hl td{background:#F4F4F8;font-weight:700}
.tbl tr.tot td{font-weight:700;border-top:2px solid #123184;background:#F4F4F8}
.tbl.dense{font-size:8pt}.tbl.dense td{padding:1.5mm 2.4mm}
.halo{paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round}
table.keep{break-inside:avoid}
svg text{font-family:'Plus Jakarta Sans','Segoe UI',Arial,sans-serif}
.t{font-size:11px;fill:#123184}.ax{font-size:10.5px;fill:#4A4A63}.lbl{font-size:11px;fill:#4A4A63}.lbl2{font-size:11px;fill:#123184}
.val{font-size:12px;font-weight:700;fill:#123184}.hd{font-size:14px;font-weight:700;fill:#123184}.seg{font-size:10.5px;font-weight:600}.pt{font-size:11.2px;font-weight:700;fill:#123184}
/* cover */
section.cover{page:cover;position:relative;width:210mm;height:297mm;overflow:hidden;break-after:page;background:#fff}
.cover .dots{position:absolute;inset:0;background-image:radial-gradient(circle,#DDE4F5 .9mm,transparent 1mm);background-size:7.6mm 7.6mm;-webkit-mask-image:linear-gradient(135deg,rgba(0,0,0,.9),rgba(0,0,0,.05) 70%);mask-image:linear-gradient(135deg,rgba(0,0,0,.9),rgba(0,0,0,.05) 70%)}
.cover .logo{position:absolute;left:21mm;top:20mm;height:13mm}
.pn{position:absolute;color:#fff;padding:5mm 4.6mm;display:flex;flex-direction:column;overflow:hidden}
.pn.p1{left:21mm;top:41mm;width:55mm;height:232mm;background:radial-gradient(ellipse 130% 60% at 90% 0%,#3D35EB 0%,rgba(61,53,235,0) 70%),radial-gradient(ellipse 120% 50% at 100% 100%,rgba(44,177,244,.95) 0%,rgba(44,177,244,0) 70%),#123184}
.pn.p2{left:78.7mm;top:41mm;width:55mm;height:143mm;background:radial-gradient(ellipse 120% 60% at 100% 0%,#3D35EB 0%,rgba(61,53,235,0) 70%),radial-gradient(ellipse 80% 50% at 0% 100%,rgba(200,245,160,.5) 0%,rgba(200,245,160,0) 70%),#123184}
.pn.p3{left:136.4mm;top:41mm;width:55mm;height:143mm;background:radial-gradient(ellipse 130% 70% at 0% 0%,#3D35EB 0%,rgba(61,53,235,0) 70%),radial-gradient(ellipse 100% 60% at 100% 100%,rgba(44,177,244,.9) 0%,rgba(44,177,244,0) 70%),#123184}
.pn .tag{font-size:6.8pt;font-weight:600;letter-spacing:1.6px;text-transform:uppercase;opacity:.8;margin-bottom:4mm}
.pn .big{font-weight:300;font-size:58pt;letter-spacing:-.045em;line-height:.95;color:#C8F5A0;margin-bottom:3mm}
.pn.p1 .big{font-size:96pt}
.pn.p3 .big{font-size:44pt}
.pn .cap{font-size:8.4pt;line-height:1.4;color:rgba(255,255,255,.9);margin-bottom:5mm}
.pn .of{font-size:7pt;color:rgba(255,255,255,.72);margin-top:2.4mm}
.cells{display:grid;gap:1.3mm}
.pn.p1 .cells{gap:2.2mm;margin-top:auto}
.cells i{display:block;aspect-ratio:1;border-radius:1mm;background:rgba(255,255,255,.22)}
.cells i.on{background:#C8F5A0}
.pn.p2 .cells{gap:1mm;margin-top:auto}
.pn.p3 .bars{display:flex;align-items:flex-end;gap:2mm;height:44mm;margin-top:auto}
.pn.p3 .bars div{flex:1;background:rgba(200,245,160,.95);border-radius:1mm 1mm 0 0;position:relative}
.pn.p3 .bars span{position:absolute;top:-4.2mm;left:0;right:0;text-align:center;font-size:6.4pt;color:#fff;font-weight:600}
.ttl{position:absolute;left:78.7mm;top:196mm;width:112.5mm}
.ttl h1{font-size:21.5pt;line-height:1.12;color:#123184;margin-bottom:4mm}
.ttl p{font-size:11pt;line-height:1.42;color:#000}
.cnum{position:absolute;right:18mm;bottom:15mm;font-size:10pt}
/* contents */
section.tocpage{break-before:page;break-after:page;height:256mm;display:flex;align-items:flex-end}
.toc{width:100%;padding-bottom:6mm}
.tr{display:flex;justify-content:space-between;align-items:center;margin-bottom:6mm;gap:12mm}
.tr span{font-family:'Newsreader',Georgia,serif;font-weight:700;font-size:13.8pt;line-height:1.22;color:#3D35EB;max-width:118mm}
.tr b{flex:none;width:8mm;height:8mm;border-radius:50%;background:#3D35EB;color:#fff;font-size:9pt;display:flex;align-items:center;justify-content:center}
section.first{break-before:page}
section.about{break-before:page}
section{break-after:auto}
"""

def build(pages):
    fig_n[0] = 0
    tab_n[0] = 0
    html_doc = (f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>The Lean Clinic, 2026. Consilium</title>'
                f'<style>{CSS}</style></head><body>{cover()}{toc_page(pages)}{body()}</body></html>')
    (BUILD / "report.html").write_text(html_doc, encoding="utf-8")
    chrome = next(c for c in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") if pathlib.Path(c).exists())
    pdf = DIST / "Consilium-Lean-Clinic-Report-2026.pdf"
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={pdf}", "--virtual-time-budget=20000", (BUILD / "report.html").resolve().as_uri()],
                   capture_output=True, text=True, timeout=240)
    return pdf

def find_pages(pdf):
    import pymupdf
    d = pymupdf.open(pdf)
    found = {}
    for s in SECTIONS:
        key = s.split(":")[0] if s.startswith("Appendix") else s
        key = (s[:22] if not s.startswith("Appendix") else s.split(".")[0] + "." + s.split(".")[1][:12])
        for i in range(2, len(d)):
            if d[i].search_for(key):
                found[s] = i + 1
                break
    return found, len(d)

if __name__ == "__main__":
    pdf = build({})
    pages, total = find_pages(pdf)
    pdf = build(pages)
    pages2, total2 = find_pages(pdf)
    print("pages:", total2, "toc:", pages2)
    (DIST / "toc.json").write_text(json.dumps([{"section": s, "page": str(pages2.get(s, ""))} for s in SECTIONS], ensure_ascii=False, indent=1), encoding="utf-8")
    print("pdf", pdf, pdf.stat().st_size)
