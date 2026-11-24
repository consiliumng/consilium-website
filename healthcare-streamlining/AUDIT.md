# Lean clinic report: audit of the draft, and how to rebuild

Internal. Written 24 Nov 2026. The public output is `dist/Consilium-Lean-Clinic-Report-2026.pdf` (copied to `site/`) and the page at `/reports/lean-clinic/`.

## Editorial decisions taken (veto any of these)

1. **Lead audience: clinic operators.** Impact case (family time and cost, equity, data) carried in Sections 3, 6, 7 and 9, and in the social posts.
2. **Hook: the ₦100m primary health centre debate.** Cited official figures: NPHCDA director ₦120m (2022); Enugu ₦24bn for 260 centres (about ₦92m each, our arithmetic). We could not find the Twitter thread itself, so the report does not cite it.
3. **Conclusion made modest and conditional.** "The math is clear" is gone. The report says the lean set-up is a volume bet: break-even about 14 patients a day, payback about 21 months at 20 a day.
4. **Style follows the US-Nigeria MOU report** (Newsreader + Plus Jakarta Sans, blue serif numbered headings, contents page with circles, blue-ruled key boxes, bordered tables). BRAND.md v1.5 says Plus Jakarta Sans is retired and headlines use Fraunces; the report follows the MOU PDF as instructed. The website page and social graphics follow BRAND.md.
5. **No stock photos on the cover.** Three panels carry our own figures (BRAND.md section 8 prefers own charts). Swap in photography if wanted.

## Flaws found in the draft, and what was done

### Facts
| Draft | Problem | Fix |
|---|---|---|
| Rwanda $1bn vs Nigeria $10bn | Totals, not per person; meaningless | Per-person and PPP from World Bank |
| Reviewer note: "Rwanda ~$72 vs Nigeria ~$45 per person" | **Wrong.** World Bank series shows Nigeria above Rwanda every year 2015 to 2023 (2023: US$66.82 vs 52.66; PPP int$260 vs 177) | Report states the real gap: who pays (72% vs 4% out of pocket), outcomes (maternal deaths 993 vs 229; life expectancy 54.5 vs 67.8) |
| Nigeria about $10bn total | 2023: about US$15bn (66.82 x 227.9m people) | Corrected |
| US $4.5T, UK $280bn | Out of date (US $5.3T in 2024, CMS; UK £317bn, ONS) | Removed; not needed for the argument |
| OOP 70 to 77% | Roughly right; World Bank 2023: 71.9% | Uses 72% |
| "Lysum, Mindray, Roche at ₦650k to ₦900k" | Unverifiable; no listing found for Lysum GULP-102. Entry-level POC readers found at ₦310k to ₦850k | Brands dropped; range cited with source; flagged as unverified |
| Rapid tests resolve typhoid, hepatitis, HIV "with high accuracy" | Typhoid RDTs too inaccurate to replace culture (Cochrane 2017); HIV needs confirmatory testing | Risk table; claim narrowed |
| NDHA compliance "requires" UHI, interoperability, digital POC capture | Not supported by anything found. NDHA is a blueprint; binding EMR certification rules not settled; Digital Health Services Bill pending. NDPA also covers paper records | Rewritten with caveats |
| "EMR eliminates repeat tests" | Unmeasured in Nigerian clinics | Model does not rely on it |
| Mrs Bola story | Reads as fact | Labelled a composite; timings labelled assumed |

### Model
| Draft | Problem | Fix |
|---|---|---|
| Table 2 totals for B and C | Each ₦50,000 short (1,865,000 and 2,045,000, not 1,815,000 and 1,995,000) | Rebuilt |
| Rent in capex and in monthly opex | Double counted | Rent is a yearly running cost |
| Revenue treated as profit | Drug cost ₦2,500 a visit never deducted (about ₦15m a year); would make Clinic A loss-making | COGS deducted |
| 1 to 2 patients/hour vs 20 patients/day | One room at 1.5/hour cannot see 20/day; room occupancy is not patient journey time | Base case: same volume for all three; speed benefit only as an upside scenario |
| Computers: 2, 3 and 4 in different places | Inconsistent | ₦1.3m IT line, stated once |
| Clinic A pays a lab scientist | No lab to run | A has a records clerk instead |
| Flat consumables (₦300k/month) | About ₦580 per work-up; POC/RDT cost is per test | ₦1,800 per work-up, tested ₦1,000 to ₦3,000 |
| 100% of visits are malaria work-ups | Overstates | 60% assumed, tested 40% to 80% |
| Patient pays ₦13,500 vs ₦9,000 | Leaves out the outside lab bill | Family cost compares full cash cost plus time |
| Reviewer's "corrected" model | Changed to 3 doctors/3 rooms silently; margins 46 to 67%; payback 4 months | Replaced; margins 23 to 26%; payback 21 months |
| Flat nominal naira vs 20% discount rate | Mixes real and nominal | Constant 2026 naira, no discount rate; payback only |
| Spending thesis vs revenue-capture evidence | Money moved from labs to clinics is not system saving | Report shows the family's saving and that it depends on the in-room price staying below the outside lab's |

## Open items before relying on the numbers

1. **Staff pay is the draft's placeholder** (₦400k doctor, ₦200k nurse, ₦200k lab scientist, ₦120k clerk assumed). Replace with HCW Pay Check medians; edit `scripts/model.py`, rerun.
2. **Consumable cost per work-up (₦1,800)** is the single most important input and is an assumption. Needs distributor quotes.
3. **Outside lab price (₦6,500)**: malaria test ₦2,500 is from the Consilium price file (2026, grade C); full blood count ₦4,000 is assumed.
4. Rent, electricity, IT, equipment prices are the draft's, unsourced.
5. 60% work-up share, 80% drug share, 3% leakage, 10% on-costs: assumptions.
6. Byline: none set (page shows "Consilium Research").
7. Regulatory wording on laboratory licensing is deliberately generic ("the relevant council"); check MLSCN requirements before telling operators nurses can run POC tests.

## Rebuild

```
python -I -X utf8 healthcare-streamlining/scripts/fetch_worldbank.py   # optional refresh
python -I -X utf8 healthcare-streamlining/scripts/model.py             # data/model.json
python -I -X utf8 healthcare-streamlining/scripts/build_report.py      # dist/*.pdf, dist/toc.json (two passes for contents page)
python -I -X utf8 healthcare-streamlining/scripts/build_social.py      # social/out/lean-clinic-*.png
```
Copy the new PDF to `site/` and update `content/reports/lean-clinic.md` (toc pages from `dist/toc.json`, headline numbers). Fonts are read from `build/fonts2/` (Newsreader, Plus Jakarta Sans, from Google Fonts).
