::: {.cover}
[Methods paper · Version 1.2]{.kicker}

[Corporate Nature Pressure Index]{.cover-title}

[How we compare India's 500 largest listed companies on the environmental pressure they report, and what that pressure would cost society]{.cover-sub}

[Urvara.Life with Landstack · for ILDC 2026, Bhubaneswar]{.cover-org}

[28 October 2026 · Draft for discussion, not for publication]{.cover-date}
:::

::: {.statusnote}
**Status of this document.** This paper sets out the method behind the Corporate Nature Pressure Index (CNPI), version 1.2. The index used to be called the Corporate Land and Biodiversity Index (CLBI), and the output files still carry the `CLBI_v1_` prefix. We computed every number in this paper from the build of 2026-10-28 12:28:30 UTC (`outputs_v12/build_stats.json`), made after an independent review of data and method (Appendix F), or we quote it from a cited source. Appendix E shows how we computed the less obvious numbers. The paper adds no estimate of a company's environmental performance to what the company itself reported.

**Two products, kept apart.** The paper describes two products. (1) The **CNPI physical pressure index** ranks reported physical quantities within peer groups. (2) The **illustrative nature cost** multiplies the same quantities by published damage prices and expresses the result as a share of EBITDA. The cost never enters a rank, and a rank never uses a price.
:::

<!--TOC-->

# The method in brief

This chapter gives the whole method in a few pages: the starting idea and the reason for the change of name, the formula, the sources, the adjustments we make to reported figures, the rules that keep companies out of a rank, the path from 500 companies to 409, and the rules that apply to particular sectors. The numbered sections give the detail and the evidence.

## From land and biodiversity to nature pressure

We set out to build a **Corporate Land and Biodiversity Index** (CLBI). The aim was to compare India's largest listed companies on the land they hold, where their sites sit against sensitive habitats, and what their operations do to biodiversity. Land-use change is the largest direct driver of biodiversity loss on land (IPBES 2019), so land was the natural place to start.

We could not find the data to do it.

- The BRSR, the sustainability report SEBI requires of large listed companies, has no field for hectares, coordinates, land-use change or restoration. It asks for the *number* of plants and offices and for a free-text table of operations in or near ecologically sensitive areas (Section 10.1).
- An independent search of annual reports, mining-lease tables and environmental-clearance letters for all 500 companies found a company-wide figure for land held for **13 companies (2.6%)**, after we checked each figure by hand. It found printed coordinates for **10 of 326** named sites.
- Of 87 statements about operating near a sensitive area, 18 from 13 companies say yes or hedge (15 affirmative from 12 companies; 3 hedged from one). None gives coordinates.

A land or biodiversity score built on 13 companies would rank disclosure, and only for a handful of firms. In version 1.1, restoration, recycling and renewable electricity earned up to 10 bonus points on top of the pressure score. With so little land evidence to stand on, and with recycling and renewables now netted inside their own pressures, we set that bonus to zero in version 1.2.

Almost every company does report four quantities in a machine-readable filing: greenhouse-gas emissions, energy from non-renewable sources, water consumed, and waste it did not recover. IPBES (2019) lists climate change, pollution and the use of natural resources among the direct drivers of nature loss, and these four quantities measure them in a company's own operations. We built the index on them and renamed it the **Corporate Nature Pressure Index** (CNPI). The name states the scope: pressure the company itself reports. CNPI does not measure the state of nature or a company's biodiversity impact. Land stays in the index as evidence beside the rank (Section 10), with a site-level biodiversity metric ready for the day companies report site areas and coordinates (Section 10.3).

## The formula

For company $i$ in peer group $g$ and pressure $p$:

1. **Net pressure** $Q_{i,p}$, from the company's FY2025-26 BRSR (table below).
2. **Intensity**, per ₹ crore of revenue from operations on the same boundary as the BRSR:
$$I_{i,p} = \frac{Q_{i,p}}{\mathrm{Rev}_i}$$
3. **Score** within the group. Sort the $k$ companies with a usable intensity from lowest to highest; $\rho_{i,p}$ is the company's position, and tied values share the average position:
$$s_{i,p} = 100 \times \frac{k - \rho_{i,p}}{k - 1}$$
The lowest intensity scores 100 and the highest 0.
4. **Final score**, the unweighted mean over the pressures the group requires (four, or three where pollution is unscored):
$$F_i = \frac{1}{|\mathcal{R}_g|} \sum_{p \in \mathcal{R}_g} s_{i,p}$$
5. **Rank** within the group by $F_i$ rounded to six decimals. Rank 1 is the lowest reported pressure per rupee of revenue.

| Pressure | BRSR item | Gross figure | Offset that reduces it | Net figure we score |
|---|---|---|---|---|
| Climate | P6 EI 7 | Scope 1 + Scope 2, tCO2e | none | Scope 1 + Scope 2 |
| Energy | P6 EI 1 | total energy, GJ | energy from renewable sources | non-renewable energy |
| Water | P6 EI 3 | withdrawal, kL | water returned | consumption, capped at withdrawal |
| Pollution | P6 EI 9 | waste generated, t | waste recovered | generated minus recovered, never below 0 |
| Air (separate rank) | P6 EI 6 | NOx + SOx + PM, t | none | NOx + SOx + PM |

An offset reduces only the pressure it belongs to. Renewable power cannot make up for unrecovered waste. Sections 4 and 7 give the full definitions.

## Where the data come from

| Source | What we take from it | Coverage |
|---|---|---|
| BRSR XBRL file filed with NSE | the four pressures and air, with the unit the filing declares | 465 of 500 companies have a parseable file; 84.2% of the 4,268 core values are machine-readable with an explicit unit (tier 1) |
| Filed BRSR PDF | unit checks on XBRL values (tier 2, 8.2%); corrections of unit slips (tier 5, 1.0%) | Climate needs the most checking: 246 filings tag Scope 1 and 2 with the ambiguous unit "MtCO2e" |
| Annual and sustainability reports | values the XBRL left blank, each with a URL and a verbatim quote (tier 3, 5.6%) | 1,007 of 3,870 candidate values accepted |
| Annual financial filing with NSE | revenue from operations on the BRSR's own boundary | usable for 487 companies |
| NSE Indices classification and BRSR product lines (NIC codes, turnover shares) | peer groups | 29 groups; 54 companies moved to the group of their main activity |
| Annual reports, mining-lease tables, environmental-clearance letters | land and site evidence, outside the score | all 500 searched |
| Published damage prices | the illustrative nature cost, outside the score | Section 11 |

Every value carries its source URL, the XBRL fact or the PDF page with a verbatim quote, the transformation applied and the SHA-256 fingerprint of the source file (`CLBI_v1_company_data.csv`). Sections 3.1 to 3.7 describe each route.

## Adjustments to reported figures

We change a reported figure only by a stated rule, and the dataset shows the figure before and after.

- **Offsets.** Renewable energy, water returned and waste recovered come off their own pressure, in full (Section 4.6).
- **Water above withdrawal.** Where consumption is 1.05 to 10 times withdrawal, the company has counted recycled water as consumed. We score withdrawal (15 companies).
- **Water at exactly 20% of withdrawal.** The company has applied an assumed 80% discharge in place of a measurement. We give no offset and score withdrawal (30 companies, 24 ranked).
- **Waste recovered above generated**, up to 1.5 times: the net pressure is zero.
- **Zero Scope 2** stands where renewables supply at least 90% of energy or electricity (7 of 11 zero values).
- **Energy tables** corrected to the filed PDF count as a set: if the corrected total fails, we drop the corrected split too (13 companies corrected).
- **Seawater**, for the nature cost only. We remove the seawater inside reported consumption from priced water for 7 large water users. Ranks are unaffected.

## Values we hold back, and companies we caution

We hold back a value that looks wrong, even if the filing prints it, until the company confirms it. A company with a held-back value on a pressure its group scores loses its rank. Section 6 sets out each rule.

| Rule | Test | Effect in this build |
|---|---|---|
| V1 Reported zero | zero gross figure, or zero Scope 1 or Scope 2 on its own | marked "to confirm"; 13 companies lose their rank |
| V3 Extreme value | gross intensity above 300 times, or below 1/300 of, the peer median | 16 core values held back |
| V4 Electricity bill | Scope 2 implies a grid bill larger than revenue | 2 companies |
| V5 Grid electricity | Scope 2 implies more than 1.5 times total energy | 3 companies |
| V6 Water | consumption above 10 times withdrawal | 4 companies |
| V8 Waste | recovered above 1.5 times generated | 4 companies |
| V11 Revenue | revenue year or boundary does not match the BRSR | 13 companies |
| V12 Scope 1 and fuel | Scope 1 above 0.12 t per GJ of fossil energy, outside process-emission groups | caution, rank kept; 15 companies, 14 of them ranked |
| V13 Naming caution | unusual business model or boundary, or a value 100 to 300 times from the peer median | caution, rank kept; 31 ranked companies |

A naming caution leaves the rank alone. It tells you not to single the company out by name, for example as a sector leader, until someone checks it.

## From 500 companies to 409

Each company passes through the same tests in the same order. We count it at the first test it fails.

| Test | Remaining | Dropped |
|---|---:|---:|
| Universe: top 500 NSE companies by average market capitalisation, January–June 2026 (AMFI) | 500 | |
| A FY2025-26 BRSR source covers the required pressures | 475 | 25 |
| Every required pressure reported | 464 | 11 |
| Revenue matched to the BRSR year and boundary | 463 | 1 |
| No held-back value on a required pressure | 442 | 21 |
| No reported zero awaiting confirmation | 429 | 13 |
| Peer group and NSE sector each have at least 8 members | 416 | 13 |
| At least 8 companies in the group with complete, clean data: **ranked** | **409** | 7 |

The published exclusion list gives each of the 91 companies one main reason instead: a held-back value (24), a peer group too small to rank (25), a pressure not reported (16), revenue that does not match the BRSR (13), or a zero awaiting confirmation (13). The two views count the same 91 companies in different orders (Section 8). The 409 ranked companies sit in 24 peer groups.

## Rules for particular sectors

| Groups | Rule | Reason |
|---|---|---|
| All | Compare a company only with peers whose main business is of the same kind | Intensities differ between sectors by three to four orders of magnitude; a cross-sector rank would rank sectors |
| Power; non-ferrous metals and mining; construction and engineering; real estate | Pollution unscored; three pressures make the score | Companies put fly ash, overburden and tailings, or construction debris inside the waste table or leave them out (rule V9) |
| Cement; steel; non-ferrous metals and mining; commodity chemicals and fertilisers; oil, gas and fuels | Exempt from the Scope 1 fuel check | Process emissions are expected |
| Cement; power | A second view per tonne of cement and per MWh generated | A recognised physical yardstick that companies disclose (Section 9) |
| Five financial-services groups | Scored on their operational footprint and flagged as not comparable with the real economy; nature cost shown as a share of revenue | Financed impacts fall outside the index |
| Real estate | Land banks reported in their own category (R), apart from operating land | Land held for development differs from land used in operations |
| Building products; diversified conglomerates; investment and holding companies; textiles and apparel; telecom and media | Listed with scores where available, not ranked | Fewer than 8 members, or fewer than 8 with complete data |

## Two products, kept apart

The **pressure index** ranks physical quantities. The **illustrative nature cost** multiplies the same quantities by published damage prices: carbon at the share of climate damage borne in India (₹5,400 per tCO2e), water at a scarcity value (₹358 per kL), non-renewable energy at a depletion value (₹80 per GJ), unrecovered waste at ₹600 per tonne and air pollutants at Indian health-damage values. We report it as a share of EBITDA, by peer group, with two sensitivity lenses (Section 11). A price never enters a rank.

## Changes from version 1.1

| Area | Version 1.1 | Version 1.2 |
|---|---|---|
| Name | Corporate Land and Biodiversity Index | Corporate Nature Pressure Index |
| Pressures | three (climate, water, waste), gross, plus up to 10 bonus points for restoration, recycling and renewable electricity | four (climate, energy, water, pollution), net: each offset reduces its own pressure; bonus retired |
| Land | restoration bonus; land priced in a pilot | evidence only, no score and no price |
| Peer groups | NSE sectors, financial services split; at least 10 complete companies; 373 ranked in 16 groups | 29 groups by main activity; at least 8; 409 ranked in 24 groups |
| Validation | 300× rule, zero check, Scope 2 bill test | adds V2, V5, V6, V7, V8, V9 (pollution unscored in four groups), V10 and V12; the NIC-based "trading" flag retired |
| Nature cost | carbon at the global social cost (₹22,600 per t), about 98% of the total; water ₹40 per kL; waste not priced | carbon at the India-borne share (₹5,400 per t); water at scarcity value (₹358 per kL); energy depletion and waste priced; shown as a share of EBITDA; seawater removed |

# 1. Summary

::: {.keynums}
::: {.kn}
[500]{.n} [companies in the universe, FY2025-26 BRSR]{.l}
:::
::: {.kn}
[409]{.n} [ranked, in 24 peer groups]{.l}
:::
::: {.kn}
[91]{.n} [listed with a stated reason for not being ranked]{.l}
:::
::: {.kn}
[29]{.n} [reported values held back as implausible or inconsistent]{.l}
:::
::: {.kn}
[0.4–316%]{.n} [range of peer-group medians of illustrative nature cost, as a share of EBITDA]{.l}
:::
::: {.kn}
[68.8%]{.n} [of the costed total is carbon, at the India-borne damage price]{.l}
:::
::: {.kn}
[13]{.n} [companies with a company-wide figure for land held]{.l}
:::
::: {.kn}
[10]{.n} [of 326 named operating sites with printed coordinates]{.l}
:::
:::

**The index.** CNPI compares each of India's 500 largest NSE-listed companies with peers in the same line of business. It asks one question of each company: how much pressure on nature did you report in FY2025-26 for each ₹ crore of revenue? It uses four pressures, all from the company's own Business Responsibility and Sustainability Report (BRSR):

- **climate**: Scope 1 plus Scope 2 greenhouse-gas emissions (tCO2e);
- **energy**: energy from non-renewable sources (GJ);
- **water**: water consumed (kL);
- **pollution**: waste generated minus waste recovered (t).

Renewable energy, water returned and waste recovered reduce the pressure they belong to, in full. A company cannot trade one of them against a different pressure.

**Scoring.** We divide each pressure by revenue. Within a peer group, the company with the lowest intensity scores 100, the highest scores 0, and the rest sit at even steps by position. We average the four scores with equal weights and rank companies within their group. Each company needs all four pressures. The exception is pollution, which we leave unscored in four groups (power; non-ferrous metals and mining; construction and engineering; real estate) because companies there report their largest waste streams in different ways.

**Results.** We rank **409 of the 500 companies in 24 peer groups**. We list the other 91 with the reason: a value held back as implausible or inconsistent (24 companies), a peer group too small to rank (25), a pressure not reported (16), a revenue figure that does not match the BRSR year or boundary (13), or a reported zero awaiting confirmation (13). We rank air pollution (NOx + SOx + particulate matter) on its own for 178 companies in 14 groups.

**Outside the ranks.**

- *Land and sites.* An independent search of all 500 companies found a company-wide figure for land held for 13 companies, after we checked each figure by hand, and printed coordinates for 10 of 326 named sites. We report land as evidence and do not score it (Section 10).
- *Illustrative nature cost.* We multiply each reported quantity by a published damage price, express the total as a share of EBITDA, and report peer-group medians with their interquartile range. The medians run from 0.37% of EBITDA in IT services and software to 316.0% in Cement. Across all 370 non-financial companies with positive EBITDA the median is 4.4% (3.3% and 4.8% under the two sensitivity lenses). Carbon, priced at the share of climate damage borne in India, makes up 68.8% of the costed total; water, priced by scarcity, 11.1%; energy depletion 9.5%; air 9.3%; waste 1.2% (Section 11). These figures never enter a rank.

**Reading a rank.** Rank 1 means the company reported the lowest pressure per rupee of revenue among its peers. The rank says nothing about the size of its absolute footprint, its effect on biodiversity, or wrongdoing by any other company. CNPI measures drivers of nature loss in a company's own operations. Biodiversity impact, supply chains, products in use and what a bank finances fall outside it.

**Robustness.** Ranks change little when we drop one pressure (median Spearman correlation 0.93 across groups; lowest 0.81, in transport and logistics) or when we use gross measures in place of net ones (median 0.93; lowest 0.79, in IT services and software). They change more when profit replaces revenue as the denominator (median 0.82; lowest 0.43, in transport and logistics).

::: {.callout .meaning}
**What this means.** The index compares like with like on what companies themselves report, and you can trace every number to a filing and every exclusion to a stated rule. Its main finding concerns disclosure as much as performance. We cannot yet rank one company in five, and companies do not report most of the data a full nature index needs: site locations, land area, air pollution in tonnes (Section 14).
:::

# 2. Scope and universe

**Universe.** The universe is the 500 NSE-listed companies with the highest six-month average full market capitalisation over January–June 2026, as published by the Association of Mutual Funds in India (AMFI) (`CLBI_Dated_Top500_JanJun2026_v1.csv`). The list contains no real-estate or infrastructure investment trusts.

**Reporting year.** FY2025-26, 1 April 2025 to 31 March 2026. The XBRL parser accepts a fact if its context covers this period and no other (Section 3.1).

**Unit of analysis.** We assess the listed entity on the boundary of its own BRSR. Each BRSR states whether it covers the listed company alone (standalone) or the group (consolidated). Of the 500 companies, 362 report standalone, 111 consolidated, and 27 give no boundary. Among the 409 ranked companies the split is 312, 96 and 1. We take revenue on the same basis as the company's BRSR (Section 3.6). For about three-quarters of the index, the pressures cover the listed parent alone.

**What CNPI measures.** CNPI measures *pressures*: reported quantities of the direct drivers of nature loss that IPBES (2019) identifies, here climate change, pollution and resource use, in a company's own operations. It does not measure the state of nature or change in it. Company disclosures cannot yet measure land-use change, the driver IPBES ranks first on land (Section 10).

**Exclusions.**

- Scope 3 emissions and every other value-chain pressure.
- The effects of products in use or at end of life.
- Financed and insured impacts. The financial-services peer groups show the operational footprint of banks, lenders, insurers and intermediaries (offices and data centres), and a flag (`financials_flag`) marks them as not comparable with the real economy.
- Any estimate, model output or sector average in place of a missing value. A blank stays blank.

# 3. Data sources and lineage

We record every value in `CLBI_v1_company_data.csv`, one row per company and field. Each row holds the value, unit, flag, confidence tier (`source_status`), source URL, the XBRL fact identifier or the PDF page with a verbatim quote (`source_field`), the transformation applied, and the SHA-256 fingerprint of the source file. All 5,949 reported values carry a source URL; a value reconciled against a PDF points to the BRSR filing.

## 3.1 BRSR XBRL filings

The primary source is the BRSR XBRL file each company files with NSE (SEBI 2021; SEBI 2023). Of the 500 companies, 465 had a parseable FY2025-26 BRSR XBRL file. The CLBI XBRL parser v1.0.0 read them (`normalized_companies.json`) under four rules:

- a concept qualifies if it sits in the SEBI `in-capmkt` taxonomy namespace with a local name in Table 3.1;
- the context must be the reporting entity, for 1 April 2025 to 31 March 2026, with no dimensions, segments or restatement markers;
- the parser leaves conflicting duplicate facts unresolved and does not average them;
- the parser takes a unit from the declared XBRL measure (for example GJ, TJ, MWh, kL, tCO2e) and never guesses one.

**Table 3.1. BRSR XBRL concepts used.** All are Principle 6 essential indicators (EI) of the BRSR format.

| CNPI key | XBRL concept (`in-capmkt:`) | BRSR item | Normalised unit |
|---|---|---|---|
| `scope1_tco2e` | `TotalScope1Emissions` | P6 EI 7 | tCO2e |
| `scope2_tco2e` | `TotalScope2Emissions` | P6 EI 7 | tCO2e |
| `total_energy_gj` | `TotalEnergyConsumedFromRenewableAndNonRenewableSources` | P6 EI 1 | GJ |
| `renewable_energy_gj` | `TotalEnergyConsumedFromRenewableSources` | P6 EI 1 | GJ |
| `nonrenewable_energy_gj` | `TotalEnergyConsumedFromNonRenewableSources` | P6 EI 1 | GJ |
| `renewable_electricity_share_pct` | derived: renewable ÷ total electricity (`TotalElectricityConsumptionFrom…Sources`) | P6 EI 1 | % |
| `water_withdrawal_m3` | `TotalVolumeOfWaterWithdrawal` | P6 EI 3 | kL (= m³) |
| `water_consumption_m3` | `TotalVolumeOfWaterConsumption` | P6 EI 3 | kL |
| `waste_generated_tonnes` | `TotalWasteGenerated` | P6 EI 9 | t |
| `waste_recovered_tonnes` | `TotalWasteRecovered` | P6 EI 9 | t |
| `nox_tonnes`, `sox_tonnes`, `pm_tonnes` | `NOx`, `SOx`, `ParticulateMatter` | P6 EI 6 | t |
| `scope3_tco2e` (reported, not scored) | `TotalScope3Emissions` | P6 Leadership Indicator 2 | tCO2e |
| `revenue_inr_cr` | `RevenueFromOperations` | Section A | ₹ crore |

Source: parser metric dictionary (`parser/metric_dictionary.md`). `build_clbi.py` labels the three energy facts in `source_field` with the short name `TotalEnergyConsumption…`; the parser reads the concepts in this table.

## 3.2 Units

The parser converts declared units to the base unit with fixed multipliers (for example 1 TJ = 1,000 GJ, 1 MWh = 3.6 GJ, 1 ML = 1,000 kL). Two cases needed a rule:

- **"MtCO2e".** Many filings tag Scope 1 and 2 with "MtCO2e", which could mean metric tonnes or million tonnes, and the parser leaves these unresolved. Of the 476 reported Scope 1 values, 212 are tier-1 XBRL values with an explicit unit (Table 3.2). We resolved the rest by checking the filed PDF (tier 2), from a public report with a quote (tier 3), or with **rule R1**, which reads "MtCO2e" as metric tonnes CO2e, the unit the BRSR form prescribes (tier 4).
- **Air pollutants per year.** **Rule R2** reads "t/year" or "kg/year" as an annual mass in tonnes.

`inputs/unit_backfill.csv` holds 670 candidate rows for these rules (R1: 490; R2: 180). A value read from the filed PDF with a verbatim quote takes precedence over a rule. In the final build the rules supply 51 values: 41 Scope 1 or Scope 2 values and 10 air values.

## 3.3 PDF reconciliation

Where the parser could not resolve an XBRL unit, we compared the value with the same column of the filed BRSR PDF. We accepted it if the PDF printed the unit and the number matched (`validated_pdf_unit_overrides.json` and two adjudication files). This route supplies 410 values for 163 companies, 352 of them in the nine core fields (tier 2). A further 89 records note that the PDF, once checked, gives no figure.

## 3.4 Gap-fill from public reports

Where the XBRL was blank, agents searched the filed BRSR PDF, the annual report and the sustainability report. `consolidate_gapfill.py` accepts a candidate value if it has:

- a source URL and a verbatim quote;
- a numeric value converted to the standard unit;
- an FY2025-26 period, shown in the period, quote or notes;
- a status of "found" or "corrected", and no flag for proxy, partial or estimated values.

Of 3,870 candidate rows, we accepted 1,007. The largest rejection reasons were "not found" (1,204), "field not used" (459), "not disclosed" (372), "not applicable" (324) and "concentration only" for air (317). We rejected 25 as the wrong concept or unit, a proxy, or unreliable, and 29 because the period was not FY2025-26 (`research/gapfill_QA.csv`). The accepted rows became 395 values in `inputs/gapfill_values.csv` (389 fills of a blank, 6 corrections) for 157 companies. In the nine core fields, 239 values come from this route (tier 3).

## 3.5 Energy corrections

For several companies the XBRL energy total differs from the filed PDF by a factor of 10³ to 10¹², a unit slip such as kWh entered as GJ. `consolidate_energy.py` applies the rule of Section 3.4 to energy, water consumption and waste recovered, with one extra condition: **we use an energy table as a set**. If we cannot accept a company's corrected total, we drop its corrected renewable and non-renewable split too, so a half-corrected table cannot look consistent. Of 256 candidate rows, we accepted 112: 74 fills and 38 corrections, the corrections covering 13 companies. Rejections: "not disclosed" (51), "not found" (48), proxy, partial or estimate (19), period not FY2025-26 (15), split dropped because the total failed (6), and no number (5) (`research/energy_QA.csv`). In the nine core fields, 41 values are corrections to the filed PDF (tier 5).

## 3.6 Revenue and profit

**Revenue** is Revenue from Operations for FY2025-26 in ₹ crore, from the company's annual financial filing with NSE, on the same standalone or consolidated basis as its BRSR (`financial_revenue_ledger_all500.csv`). We use a revenue figure (`revenue_ok`) if it is verified for 1 April 2025 to 31 March 2026, or if it is verified for that year and its one open issue is an unstated BRSR boundary or a discontinued-operations note (both flagged). We do not use calendar-year filers, multi-period derivations, pro-forma or modelled revenues. 487 of the 500 companies have a usable revenue figure.

**Profit after tax** (`pat_fy2026.csv`) feeds the supplementary profit view (Section 9) and nothing else.

## 3.7 Confidence tiers

**Table 3.2. Source tier of every reported value in the nine core fields** (including reported zeros), all 500 companies.

| BRSR field (CNPI key) | T1 XBRL, explicit unit | T2 unit checked vs PDF | T3 public-report fill | T4 unit rule R1/R2 | T5 corrected to PDF | Total |
|---|---:|---:|---:|---:|---:|---:|
| `scope1_tco2e` | 212 | 153 | 91 | 20 | 0 | 476 |
| `scope2_tco2e` | 212 | 149 | 92 | 21 | 0 | 474 |
| `total_energy_gj` | 448 | 0 | 13 | 0 | 13 | 474 |
| `renewable_energy_gj` | 449 | 0 | 12 | 0 | 12 | 473 |
| `nonrenewable_energy_gj` | 448 | 0 | 12 | 0 | 13 | 473 |
| `water_withdrawal_m3` | 452 | 14 | 6 | 0 | 2 | 474 |
| `water_consumption_m3` | 455 | 17 | 1 | 0 | 0 | 473 |
| `waste_generated_tonnes` | 456 | 11 | 5 | 0 | 1 | 473 |
| `waste_recovered_tonnes` | 463 | 8 | 7 | 0 | 0 | 478 |
| All nine fields | 3595 | 352 | 239 | 41 | 41 | 4268 |


Shares of the 4,268 values: tier 1, 84.2%; tier 2, 8.2%; tier 3, 5.6%; tier 4, 1.0%; tier 5, 1.0%. Climate is the least machine-readable pressure: 212 of 476 Scope 1 values are tier 1. Of the 409 ranked companies, 221 (54.0%) rest on at least one core value outside tier 1, and 85 (20.8%) on at least one public-report fill.

::: {.figure chart="tiers"}
**Figure 3.1. Source tier of every reported value, by BRSR field.** Share of the values reported by the 500 companies (counts in Table 3.2). Tier 1 is a machine-readable XBRL value with an explicit unit.
:::

::: {.callout .limit}
**Limitation.** Energy, water and waste are machine-readable for 94–97% of companies. Climate is the exception: 246 XBRL filings tag Scope 1 and 2 with the ambiguous unit "MtCO2e". The pressure that dominates the nature cost is the one that most often needed manual reconciliation.
:::

## 3.8 Coverage, from reported to scored

**Table 3.3. Coverage by pressure** (company counts, all 500). The columns from "Zero to confirm" to "Revenue not matched" are exclusive, so usable = present − zero − held back − revenue not matched.

| Pressure | Value present (of 500) | Zero to confirm | Held back (not zero) | Revenue not matched | Usable intensity | Scored in a peer group | Counts in a published rank |
|---|---:|---:|---:|---:|---:|---:|---:|
| Climate | 473 | 13 | 6 | 4 | 450 | 437 | 409 |
| Energy | 473 | 2 | 7 | 2 | 462 | 447 | 409 |
| Water | 473 | 6 | 6 | 1 | 460 | 446 | 409 |
| Pollution | 472 | 8 | 17 | 4 | 443 | 392 | 366 |
| Air (separate rank) | 245 | 10 | 13 | 0 | 222 | 178 | 178 |


"Scored in a peer group" falls below "usable" for two reasons: a company may sit in a group too small to score, and, for pollution, in one of the four groups where we do not score it.

::: {.figure chart="coverage"}
**Figure 3.2. From reported to ranked, by pressure.** Companies with a value present, a usable intensity, a score in a peer group, and a value that counts in a published rank (pollution is unscored in four groups; air has its own rank).
:::

::: {.figure chart="funnel"}
**Figure 3.3. From 500 companies to 409 ranked.** We count each company at the first test it fails, in data order (Section 8 gives the build's own reasons).
:::

## 3.9 Land and operating sites

The BRSR has no field for land area. Our land and site evidence comes from a separate search of annual reports, mining-lease tables and environmental-clearance documents for all 500 companies, which a different AI model (DeepSeek; the "Hermes" run, `research/hermes/`) carried out on its own. Section 10 covers it.

# 4. Definitions of the pressures

Notation: $i$ indexes companies, $g$ peer groups and $p$ pressures. $\mathrm{Rev}_i$ is revenue from operations in ₹ crore. All quantities are for FY2025-26 on the company's BRSR boundary.

## 4.1 Climate

$$C_i = S1_i + S2_i$$

where $S1_i$ is total Scope 1 emissions and $S2_i$ total Scope 2 emissions, both in tCO2e (BRSR P6 EI 7). We need both components and never use a partial sum.

- **Scope 1** covers direct emissions from fuel burnt and processes on the company's own sites. **Scope 2** covers emissions from generating the electricity, heat and steam the company buys (WRI and WBCSD 2004).
- **Scope 2 method.** The GHG Protocol asks for a location-based and a market-based figure (Sotos 2015). The BRSR asks for one number and no method. We cannot assign the method in 441 of the 465 parsed filings; 10 state market-based, 6 location-based, and 8 mention both without saying which the total uses. Dividing Scope 2 by purchased non-renewable electricity gives the factor each company applied. Across 433 companies the median is 0.710 tCO2/MWh and 286 sit at 0.71, the Central Electricity Authority's weighted-average grid factor for FY2024-25 (CEA 2025). In practice most BRSR Scope 2 figures are location-based. We use Scope 2 as reported.
- **Scope 3** is unscored. Of 465 parsed filings, 141 report it with a resolvable unit, 155 with the ambiguous "MtCO2e" unit, and 169 not at all; boundaries differ as well.
- **Double counting.** Part of one company's Scope 2 is a generator's Scope 1. You must never sum climate values across companies.

## 4.2 Energy

$$E_i = E^{\mathrm{NR}}_i \quad\text{and, where } E^{\mathrm{NR}}_i \text{ is not reported,}\quad E_i = \max\!\left(0,\; E^{\mathrm{T}}_i - E^{\mathrm{R}}_i\right)$$

where $E^{\mathrm{T}}_i$ is total energy consumed, $E^{\mathrm{R}}_i$ energy from renewable sources and $E^{\mathrm{NR}}_i$ energy from non-renewable sources, all in GJ (P6 EI 1). The offset is the renewable energy itself, which the pressure leaves out. The BRSR counts biomass and bagasse burnt in boilers as renewable, so these lower the energy pressure on the same terms as contracted solar or wind. The gross energy figure is $E^{\mathrm{T}}_i$.

## 4.3 Water

Let $W^{\mathrm{wd}}_i$ be total water withdrawal and $W^{\mathrm{c}}_i$ total water consumption, both in kL (P6 EI 3). The scored water pressure is

$$
W_i =
\begin{cases}
W^{\mathrm{wd}}_i & \text{if } 1.05\,W^{\mathrm{wd}}_i < W^{\mathrm{c}}_i \le 10\,W^{\mathrm{wd}}_i \quad \text{(capped)}\\[4pt]
W^{\mathrm{wd}}_i & \text{if } W^{\mathrm{wd}}_i > 0 \text{ and } \left|\,W^{\mathrm{c}}_i / W^{\mathrm{wd}}_i - 0.20\,\right| < 0.0005 \quad \text{(assumed discharge)}\\[4pt]
W^{\mathrm{c}}_i & \text{otherwise}
\end{cases}
$$

We hold the value back if $W^{\mathrm{c}}_i > 10\,W^{\mathrm{wd}}_i$ (Section 6). The offset is the water discharged back, which the BRSR treats as not consumed. The gross water figure is $W^{\mathrm{wd}}_i$. Section 6 gives the reasons for the two special cases (rules V6 and V7).

## 4.4 Pollution

$$P_i = \max\!\left(0,\; G_i - R_i\right)$$

where $G_i$ is total waste generated and $R_i$ total waste recovered through recycling, re-use or other recovery, both in tonnes (P6 EI 9). The offset is the waste recovered. A company that reports recovering more waste than it generated in the year (from stock) gets $P_i = 0$; the pressure never goes negative. The gross pollution figure is $G_i$.

## 4.5 Air (supplementary)

$$A_i = \mathrm{NO}_{x,i} + \mathrm{SO}_{x,i} + \mathrm{PM}_{i} \quad \text{(tonnes; all three required)}$$

We rank air on its own and keep it out of the main score (Section 9). The BRSR asks for these pollutants with "please specify unit", and many companies answer with a stack concentration (mg/Nm³), which no one can convert to tonnes. We excluded 322 air values from 111 companies because we could not verify their unit as an annual mass.

## 4.6 Gross and net

Each pressure has a **gross** figure, which the zero test and the extreme-value test use (Section 6), and a **net** figure, which the score uses:

| Pressure | Gross figure $Q^{\mathrm{gross}}_{i,p}$ | Net figure $Q_{i,p}$ |
|---|---|---|
| Climate | $C_i$ | $C_i$ (no offset) |
| Energy | $E^{\mathrm{T}}_i$ | $E_i$ |
| Water | $W^{\mathrm{wd}}_i$ | $W_i$ |
| Pollution | $G_i$ | $P_i$ |
| Air | $A_i$ | $A_i$ |

The offsets matter for the 409 ranked companies. 59 of them get at least half their energy from renewable sources (median 10.6%). The median company recovers 81.6% of its waste; 174 recover at least 90%, and 41 report recovering all of it or more. 215 have a scored water value below their withdrawal.

# 5. Peer groups

**Principle.** We compare a company with companies whose main business is of the same kind. Intensities differ by three to four orders of magnitude between sectors: median Scope 1 + 2 per ₹ crore in cement is 5,242 times that in insurance (`insights/pressures/PRESSURES.md`). A cross-sector rank would rank sectors.

**Method.**

1. **Start** from the company's NSE Indices industry classification (as of 22 October 2026). The universe spans 20 NSE sectors.
2. **Verify the main activity** from the company's own BRSR Section A product lines, which give each product's NIC 2008 code (MOSPI 2008) and its share of turnover. Where these were missing or unclear, we used the annual report. The main activity is the **largest source of turnover**. Of the 500 placements, 342 cite the BRSR XBRL file as evidence. For the 487 with a numeric share, the median share of the largest line is 95.3% (174 at 100%; 31 below 50%). Each placement carries a confidence grade: high (361), medium (128) or low (11). We flag 14 companies as conglomerates.
3. **Move** a company whose main activity belongs in another NSE sector to that sector's group. We moved **54 companies** this way (for example, Godawari Power & Ispat from Capital Goods to steel; Coal India from Oil, Gas & Consumable Fuels to mining). We record each move with its evidence and source URL (`inputs/peer_groups_v12.csv`, columns `pg_evidence`, `pg_source_url`).
4. **Split** large NSE sectors that mix unlike businesses. Capital Goods becomes machinery, engineering and defence, and electrical equipment and electronics. Chemicals becomes commodity chemicals and fertilisers, and specialty chemicals and paints. Metals & Mining becomes steel and iron products, and non-ferrous metals and mining. Healthcare becomes pharmaceuticals, and hospitals and diagnostics. Automobile and Auto Components becomes automobiles, and auto components and tyres. Construction Materials becomes cement, and building products. Financial Services becomes five sub-groups: banks; lending NBFCs and housing finance; capital markets and intermediaries; insurance; investment and holding companies.

The result is **29 peer groups**.

**Minimum sizes.** Three thresholds apply (all in `P`):

- the peer group, and the company's NSE sector after any move, must each have at least 8 member companies (`min_sector_size = 8`);
- we score a pressure in a group if at least 6 of its companies have a usable value for it (`min_element_reporters = 6`);
- we publish ranks if at least 8 companies in the group have a complete, clean score (`min_ranked_to_publish = 8`).

Five groups fail: building products (4 members), diversified conglomerates (1), investment and holding companies (6), textiles and apparel (7), and telecom and media (8 members, 7 of them with complete clean data). We list their 26 companies with scores where available and do not rank them.

**Table 5.1. Peer groups.** Pressures scored: C climate, E energy, W water, P pollution.

| Peer group | Companies | Ranked | Pressures scored | Air-ranked | Profit-ranked |
|---|---:|---:|---|---:|---:|
| Healthcare: pharmaceuticals | 40 | 40 | C, E, W, P | 26 | 38 |
| Financial Services: Lending NBFC and housing finance | 33 | 29 | C, E, W, P | – | 28 |
| Auto components and tyres | 29 | 27 | C, E, W, P | 15 | 27 |
| FMCG | 28 | 27 | C, E, W, P | 22 | 26 |
| Capital goods: machinery, engineering and defence | 31 | 25 | C, E, W, P | 11 | 25 |
| Financial Services: Banks | 27 | 25 | C, E, W, P | – | 25 |
| Capital goods: electrical equipment and electronics | 29 | 24 | C, E, W, P | 10 | 24 |
| IT services and software | 24 | 20 | C, E, W, P | 12 | 20 |
| Retail, e-commerce, hotels and consumer services | 27 | 19 | C, E, W, P | 9 | 17 |
| Chemicals: commodity chemicals and fertilisers | 18 | 17 | C, E, W, P | 13 | 14 |
| Chemicals: specialty, paints and coatings | 17 | 15 | C, E, W, P | 13 | 15 |
| Metals: steel and iron products | 17 | 15 | C, E, W, P | 9 | 15 |
| Power | 17 | 13 | C, E, W | 8 | 13 |
| Oil, gas and fuels | 15 | 13 | C, E, W, P | 8 | 12 |
| Financial Services: Capital markets and financial intermediaries | 18 | 12 | C, E, W, P | – | 12 |
| Automobiles | 14 | 12 | C, E, W, P | 12 | 10 |
| Construction and engineering | 13 | 12 | C, E, W | – | 12 |
| Cement | 10 | 10 | C, E, W, P | 10 | 9 |
| Consumer durables | 10 | 10 | C, E, W, P | – | 9 |
| Metals: non-ferrous and mining | 13 | 9 | C, E, W | – | 9 |
| Financial Services: Insurance underwriting | 12 | 9 | C, E, W, P | – | – |
| Real estate | 12 | 9 | C, E, W | – | 9 |
| Healthcare: hospitals and diagnostics | 10 | 9 | C, E, W, P | – | 9 |
| Transport and logistics | 10 | 8 | C, E, W, P | – | – |
| Telecom and media | 8 | 0 | not ranked | – | – |
| Textiles and apparel | 7 | 0 | not ranked | – | – |
| Financial Services: Investment and holding companies | 6 | 0 | not ranked | – | – |
| Building products | 4 | 0 | not ranked | – | – |
| Diversified conglomerates | 1 | 0 | not ranked | – | – |
| **Total (29 groups)** | **500** | **409** |  | **178** | **378** |


::: {.callout .meaning}
**What this means.** On every pressure, peer-group medians differ by three to four orders of magnitude. A single league table of all 500 companies would rank sectors. Within a group the spread narrows, and you compare businesses that make similar things.
:::

::: {.figure chart="ladder"}
**Figure 5.1. Peer-group medians by pressure.** Median net intensity per ₹ crore of revenue by peer group (logarithmic scales; each gridline is a factor of ten). Groups with at least 6 usable values. Hollow markers: pollution shown but unscored in that group.
:::

# 6. Data validation rules

We hold back a value that looks wrong, even if the filing prints it, until the company confirms it. A company with such a value on a pressure that counts in its group loses its rank ("rank withheld"). `build_clbi.py` holds every rule below, with its threshold in the parameter dictionary `P`. `CLBI_v1_data_queries.csv` lists all held-back values with their reasons (53 rows).

**V1. Reported zeros.** We flag a zero *gross* figure, or a zero Scope 1 or Scope 2 on its own, as "to confirm" and do not score it (`exclude_reported_zero`). For an operating company, a zero most often means "not measured". A zero *net* figure with a positive gross figure, such as all waste recovered, is a genuine offset, and we score it. Zero flags in this build: climate 13 companies, energy 2, water 6, pollution 8, air 10.

**V2. Zero Scope 2 accepted where the renewable share is at least 90% (new in v1.2).** V1 does not flag a zero Scope 2 if the company's own filing shows renewable energy at 90% or more of total energy, or renewable electricity at 90% or more of electricity consumed (`scope2_zero_re_min = 0.90`):

$$S2_i = 0 \;\wedge\; \left( \frac{E^{\mathrm{R}}_i}{E^{\mathrm{T}}_i} \ge 0.90 \;\vee\; \frac{\mathrm{El}^{\mathrm{R}}_i}{\mathrm{El}^{\mathrm{T}}_i} \ge 0.90 \right) \;\Rightarrow\; \text{accepted}$$

where $\mathrm{El}^{\mathrm{R}}_i$ and $\mathrm{El}^{\mathrm{T}}_i$ are renewable and total electricity consumed. *Rationale:* at that share, a zero fits a market-based Scope 2 on contracted renewable power. *Effect:* we accept 7 of the 11 zero Scope 2 values (HINDUNILVR, BEL, POWERINDIA, BOSCHLTD, GVT&D, UBL, CUPID).

**V3. Extreme values: the 300× rule.** For each pressure, we compare the gross intensity with the median of the peer group:

$$x_{i,p} = \frac{Q^{\mathrm{gross}}_{i,p}}{\mathrm{Rev}_i}\;\;(Q^{\mathrm{gross}}_{i,p} > 0), \qquad r_{i,p} = \frac{x_{i,p}}{\operatorname{median}_{j \in g}\, x_{j,p}}, \qquad \text{held if } r_{i,p} > 300 \;\text{ or }\; r_{i,p} < \tfrac{1}{300}$$

The median covers all companies in the group with a positive gross figure and usable revenue (`extreme_ratio = 300`). *Rationale:* a value this far from like-for-like peers tends to be a unit slip (a factor of 1,000 between kWh and MWh, or kg and t) or a boundary problem (head office only). We test the **gross** figure because a very low net figure can be a genuine offset. The threshold is a judgement, and we have not run a formal sensitivity test on it (Section 13). *Effect:* on the four core pressures we hold back 16 values (2 above, 14 below). We flag 11 more pollution values as "shown only", because their groups do not score pollution, and hold back 13 air values.

**V4. Scope 2 implies an electricity bill larger than revenue.**

$$B_i = \frac{S2_i}{0.71\ \mathrm{tCO_2/MWh}} \times 1{,}000\ \tfrac{\mathrm{kWh}}{\mathrm{MWh}} \times ₹6/\mathrm{kWh} \times 10^{-7}\ \tfrac{₹\,\mathrm{crore}}{₹}, \qquad \text{held if } B_i > \mathrm{Rev}_i$$

(`scope2_grid_ef = 0.71`, the CEA FY2024-25 weighted-average factor; `scope2_tariff_inr_per_kwh = 6.0`). *Rationale:* a company cannot pay more for grid electricity than it earns, so such a value is almost always a unit error. *Effect:* 2 companies (SHYAMMETL, PFOCUS).

**V5. Scope 2 implies more grid electricity than 1.5× total energy (new in v1.2).** We compare the grid electricity implied by Scope 2, in GJ, with the company's total reported energy:

$$G^{\mathrm{S2}}_i = \frac{S2_i}{0.71} \times 3.6\ \tfrac{\mathrm{GJ}}{\mathrm{MWh}}, \qquad \text{held if } G^{\mathrm{S2}}_i > 1.5\,E^{\mathrm{T}}_i \;\wedge\; \neg\,\text{V4} \;\wedge\; \tfrac{1}{300} \le \frac{E^{\mathrm{T}}_i/\mathrm{Rev}_i}{\operatorname{median}_{j\in g}(E^{\mathrm{T}}_j/\mathrm{Rev}_j)} \le 300 \;\wedge\; \neg\,\text{V10}$$

(`scope2_energy_ratio_max = 1.5`). *Rationale:* grid electricity is part of total energy consumed, so Scope 2 cannot imply much more grid electricity than all the energy the company used; the margin of 1.5 allows for a different grid factor. **We run the test against a credible energy total**: one within the 300× band of its peers that passes V10. A tiny, implausible energy total would otherwise make a normal Scope 2 look inconsistent. *Effect:* 7 companies exceed 1.5×. One already fails V4, and we do not test three whose energy total is itself held back (THERMAX, KPITTECH, GALLANTT). We hold three: COALINDIA, CANHLIFE and INGERRAND.

**V6. Water consumption above withdrawal (new in v1.2).** When a company reports consumption more than 5% above withdrawal, but no more than 10 times it, it has in most cases counted recycled water as consumed. Freshwater drawn is the upper bound, so we score withdrawal (the "capped" case in Section 4.3). *Effect:* 15 companies (all ranked), with consumption 1.05 to 4.12 times withdrawal. Above **10 times** withdrawal, we hold the value as a probable unit error. *Effect:* 4 companies held (BAJFINANCE and BAJAJFINSV, which report zero withdrawal; BEML; PRIVISCL).

**V7. Consumption at 20% of withdrawal: scored on withdrawal (new in v1.2).** When reported consumption equals 20% of withdrawal to within 0.05 percentage points (`assumed_consumption_share = 0.20`), the company has applied an assumed 80% discharge in place of a measurement. We credit no offset, score water on withdrawal, and set the flag `water_discharge_assumed`. *Effect:* 30 companies, 24 of them ranked; most are banks, lenders and other office-based businesses. We decided on 28 October to keep the rule. Its narrow reach is a limitation (Section 13): it catches a ratio of 0.20 and no other round ratio, and no one has read the 30 filings for the word "assumed".

**V8. Waste recovered more than 1.5× waste generated (new in v1.2).** We hold the value as an inconsistent table, or a stock movement too large to count as current-year recovery. *Effect:* 4 companies (TVSMOTOR, METROBRAND, IGL, PRIVISCL). We accept recovery between 1.0 and 1.5 times generation and set $P_i = 0$.

**V9. Pollution unscored in four groups (new in v1.2).** In power, non-ferrous metals and mining, construction and engineering, and real estate, some companies put their largest waste streams (fly ash; overburden and tailings; construction and demolition debris) inside the BRSR waste table and others leave them out (`pollution_not_comparable`). The filings show the spread. Coal India reports 5,345,920,956 t generated, 91.3% of all waste reported by the 500 companies, and 5,345,918,279 t recovered, a net of about 2,676 t. GMDC, a lignite miner, reports 69 t generated. NTPC reports 57,193 t and Reliance Power 106,741,115 t. Larsen & Toubro reports 596,194 t against 9.7 t for IRCON and 24 t for NBCC. In real estate, Oberoi Realty reports 333,517.467 t generated and 333,517.46 t recovered, a net of 0.007 t. A waste score in these groups would reward whoever left out, or offset in full, the largest stream. We show pollution for these groups, unscored, with the reason, and rank them on climate, energy and water. We added real estate after the independent review (Appendix F).

**V10. Non-renewable energy above total energy (new in v1.2).** We hold the value if $E^{\mathrm{NR}}_i > 1.01\,E^{\mathrm{T}}_i$. *Effect:* none in this build.

**V11. Revenue match.** A company without a usable revenue figure (Section 3.6) has no intensity and no rank. *Effect:* 13 companies.

**V12. Scope 1 larger than fuel use could emit (new; a caution, not a hold).** Burning fuel emits at most about 0.1 tCO2 per GJ. Outside the groups where we expect process emissions (`process_emission_groups`: cement; steel and iron products; non-ferrous metals and mining; commodity chemicals and fertilisers; oil, gas and fuels), we flag a company if

$$\frac{S1_i}{E_i} > 0.12\ \mathrm{tCO_2/GJ}$$

where $E_i$ is its non-renewable energy (`scope1_fuel_max_t_per_gj = 0.12`; column `scope1_fuel_check`). We apply the check where both the climate value and the energy value are usable (not missing, zero-flagged or held back). *Rationale:* a higher ratio needs process or fugitive emissions that the filing does not label, or points to a unit or boundary error. *Effect:* 15 companies, 14 of them ranked. Three of the seven zero Scope 2 values accepted under V2 belong to companies that fail this check (BEL, POWERINDIA, CUPID); they keep their rank and carry a caution.

**V13. Naming caution.** This flag leaves the rank alone. It tells you not to single the company out by name, for example as a sector leader, until someone checks it. Three sources set it: (a) a reviewed note on the company's main activity in `inputs/peer_fit_notes.csv`, where the business differs from its peers or its BRSR boundary is unusual (for example steel-pipe converters that buy their steel, jewellers among appliance makers, a delivery platform among hotels and stores, drug makers with very low Scope 1, and UPL's standalone boundary); (b) a scored gross intensity 100–300 times above or below the peer median, inside the hold-back line but unusual; (c) rule V12. We retired an earlier rule that read the NIC division of the dominant product as "trading" or "services", because it mislabelled refiners and manufacturers. *Effect:* 31 ranked companies carry a caution: 12 from reviewed notes, 7 from value flags (10 flags: climate 2, energy 3, water 2, pollution 3) and 14 from V12, with some companies in more than one.

**Table 6.1. Values held back or flagged on the four core pressures** (`CLBI_v1_data_queries.csv`). "× median" is the gross intensity relative to the peer median.

| Company | Peer group | Pressure | Test | × median | Status |
|---|---|---|---|---|---|
| PFOCUS | Real estate | climate | Scope 2 bill > revenue | 13,174.4 | held back |
| SHYAMMETL | Metals: steel and iron products | climate | Scope 2 bill > revenue | 8.6 | held back |
| CANHLIFE | Financial Services: Insurance underwriting | climate | Scope 2 grid electricity > 1.5× total energy | 1/1 | held back |
| COALINDIA | Metals: non-ferrous and mining | climate | Scope 2 grid electricity > 1.5× total energy | 1.7 | held back |
| INGERRAND | Capital goods: machinery, engineering and defence | climate | Scope 2 grid electricity > 1.5× total energy | 1/1 | held back |
| ABSLAMC | Financial Services: Capital markets and financial intermediaries | climate | gross < 1/300 of peer median | 1/5,000 | held back |
| ETERNAL | Retail, e-commerce, hotels and consumer services | climate | gross < 1/300 of peer median | 1/833 | held back |
| ABREL | Real estate | climate | gross > 300× peer median | 345.1 | held back |
| CENTRALBK | Financial Services: Banks | energy | gross < 1/300 of peer median | ≈0 | held back |
| CHOICEIN | Financial Services: Capital markets and financial intermediaries | energy | gross < 1/300 of peer median | ≈0 | held back |
| ETERNAL | Retail, e-commerce, hotels and consumer services | energy | gross < 1/300 of peer median | 1/1,111 | held back |
| GALLANTT | Metals: steel and iron products | energy | gross < 1/300 of peer median | ≈0 | held back |
| KPITTECH | IT services and software | energy | gross < 1/300 of peer median | ≈0 | held back |
| THERMAX | Capital goods: machinery, engineering and defence | energy | gross < 1/300 of peer median | ≈0 | held back |
| ABREL | Real estate | energy | gross > 300× peer median | 813.6 | held back |
| ANANTRAJ | Real estate | waste | gross < 1/300 of peer median | ≈0 | shown only |
| CONCOR | Transport and logistics | waste | gross < 1/300 of peer median | 1/2,500 | held back |
| ETERNAL | Retail, e-commerce, hotels and consumer services | waste | gross < 1/300 of peer median | 1/1,111 | held back |
| GMDCLTD | Metals: non-ferrous and mining | waste | gross < 1/300 of peer median | 1/10,000 | shown only |
| IRCON | Construction and engineering | waste | gross < 1/300 of peer median | 1/1,429 | shown only |
| JAINREC | Metals: non-ferrous and mining | waste | gross < 1/300 of peer median | 1/588 | shown only |
| NBCC | Construction and engineering | waste | gross < 1/300 of peer median | 1/667 | shown only |
| RVNL | Construction and engineering | waste | gross < 1/300 of peer median | 1/1,000 | shown only |
| ADANIPOWER | Power | waste | gross > 300× peer median | 506.2 | shown only |
| JPPOWER | Power | waste | gross > 300× peer median | 813.6 | shown only |
| JSWENERGY | Power | waste | gross > 300× peer median | 517.3 | shown only |
| NLCINDIA | Power | waste | gross > 300× peer median | 426.8 | shown only |
| RPOWER | Power | waste | gross > 300× peer median | 22,907.6 | shown only |
| IGL | Oil, gas and fuels | waste | recovered > 1.5× generated | 1/7 | held back |
| METROBRAND | Retail, e-commerce, hotels and consumer services | waste | recovered > 1.5× generated | 1/23 | held back |
| PRIVISCL | Chemicals: specialty, paints and coatings | waste | recovered > 1.5× generated | 1.9 | held back |
| TVSMOTOR | Automobiles | waste | recovered > 1.5× generated | 1/2 | held back |
| BAJAJFINSV | Financial Services: Lending NBFC and housing finance | water | consumption > 10× withdrawal | – | held back |
| BAJFINANCE | Financial Services: Lending NBFC and housing finance | water | consumption > 10× withdrawal | – | held back |
| BEML | Capital goods: machinery, engineering and defence | water | consumption > 10× withdrawal | 1.8 | held back |
| PRIVISCL | Chemicals: specialty, paints and coatings | water | consumption > 10× withdrawal | 2.0 | held back |
| ADANIENSOL | Power | water | gross < 1/300 of peer median | 1/2,000 | held back |
| ETERNAL | Retail, e-commerce, hotels and consumer services | water | gross < 1/300 of peer median | 1/370 | held back |
| J&KBANK | Financial Services: Banks | water | gross < 1/300 of peer median | 1/769 | held back |
| JAINREC | Metals: non-ferrous and mining | water | gross < 1/300 of peer median | 1/455 | held back |


::: {.callout .limit}
**Limitation.** The hold-back rules catch values far from peers or impossible on their face. They miss some inconsistencies inside a filing. A simple cross-table test, Scope 2 divided by purchased non-renewable electricity, falls outside 0.5–1.0 tCO2/MWh for 42 companies. Rule V5 holds back three of them (COALINDIA, CANHLIFE, INGERRAND); the other 39, 34 of them ranked, pass every rule above (Section 13).
:::

# 7. Scoring

## 7.1 Intensity

For each company and pressure,

$$I_{i,p} = \frac{Q_{i,p}}{\mathrm{Rev}_i}$$

in units per ₹ crore. $I_{i,p}$ is undefined if $Q_{i,p}$ is missing, zero-flagged (V1) or held back (V3–V8, V10), or if revenue is unusable (V11).

## 7.2 Percentile score

Within peer group $g$, let $\mathcal{V}_{g,p}$ be the set of companies with a defined $I_{i,p}$, and $k = |\mathcal{V}_{g,p}|$. We score the pressure if $k \ge 6$. Let $\rho_{i,p}$ be the position of company $i$ when we sort the intensities in $\mathcal{V}_{g,p}$ from lowest to highest, with tied values sharing the average of their positions. The score is

$$s_{i,p} = 100 \times \frac{k - \rho_{i,p}}{k - 1}$$

The lowest intensity scores 100, the highest 0, and the others sit at even steps by position. The score uses the order and ignores the size of the gaps, which keeps it stable against the long right tails all four pressures show.

$\mathcal{V}_{g,p}$ includes every company with a usable value for pressure $p$, including companies whose rank we withhold because of a problem on a *different* pressure. The energy score covers more companies than we rank in 15 of the 24 ranked groups (climate and water: 14 groups; pollution: 9).

## 7.3 Averaging

Let $\mathcal{R}_g$ be the required pressures of group $g$: all four, or climate, energy and water in the four groups of rule V9. The final score is the unweighted mean

$$F_i = \frac{1}{|\mathcal{R}_g|} \sum_{p \in \mathcal{R}_g} s_{i,p}$$

defined if every $s_{i,p}$ for $p \in \mathcal{R}_g$ exists and no required pressure carries an open data query. A company gains nothing by leaving a value out. Equal weights are a choice we made, with no empirical basis (OECD and JRC 2008); Section 12 tests what dropping each pressure does.

## 7.4 Ranking and rounding

We round scores to six decimal places before ranking, so floating-point noise cannot split a genuine tie. Let $\mathcal{K}_g$ be the companies in $g$ with a defined $F_i$. Then

$$\mathrm{rank}_i = 1 + \left|\{\, j \in \mathcal{K}_g : \tilde F_j > \tilde F_i \,\}\right|, \qquad \tilde F = \operatorname{round}(F, 6)$$

This is standard competition ranking (1, 2, 2, 4). We publish ranks if $|\mathcal{K}_g| \ge 8$. In this build 30 ranked companies, in 6 groups, share a rank with at least one peer. We assign quartiles from $\mathrm{rank}_i / |\mathcal{K}_g|$ with cut-points 0.25, 0.50 and 0.75. Reports show scores to one decimal place; the files keep full precision.

## 7.5 Worked example: ACC Ltd (cement)

ACC reports on a standalone basis. Its FY2025-26 revenue from operations is ₹25,766.48 crore. All ten cement companies have complete, clean data, so $k = 10$ for every pressure and $k - 1 = 9$.

**Step 1: net quantities** (from `CLBI_v1_scores_all500.csv`).

- Climate: $C = 14{,}737{,}570 + 555{,}799 = 15{,}293{,}369$ tCO2e.
- Energy: $E = 71{,}419{,}552 - 5{,}355{,}975 = 66{,}063{,}577$ GJ.
- Water: withdrawal and consumption are both 4,141,552 kL; neither special case applies, so $W = 4{,}141{,}552$ kL.
- Pollution: $P = 398{,}506.78 - 398{,}506.00 = 0.78$ t.

**Step 2: intensities.** Dividing by 25,766.48 gives 593.54 tCO2e, 2,563.93 GJ, 160.73 kL and 0.0000303 t per ₹ crore.

**Step 3: positions among the ten cement companies.**

| Pressure | ACC intensity (per ₹ cr) | Lower peers | Position $\rho$ | Score $100(10-\rho)/9$ |
|---|---:|---|---:|---:|
| Climate | 593.54 | JSW Cement 554.54 | 2 | 88.89 |
| Energy | 2,563.93 | none (JSW Cement next, 2,626.94) | 1 | 100.00 |
| Water | 160.73 | Shree Cement 144.45; Ambuja 146.37 | 3 | 77.78 |
| Pollution | 0.0000303 | J.K. Cement 0; Ramco 0 (tied, positions 1 and 2, each 1.5) | 3 | 77.78 |

J.K. Cement and Ramco Cements each report recovering more waste than they generated in the year (10,013.76 t against 9,677.51 t, and 99,098 t against 98,128.48 t). Their net is zero, and they share position 1.5, scoring $100 \times (10 - 1.5)/9 = 94.44$.

**Step 4: average.** $F = (88.89 + 100 + 77.78 + 77.78)/4 = 86.11$.

**Step 5: rank.** The next-highest cement score is JSW Cement's 80.56, so ACC is **rank 1 of 10**. On the supplementary views (Section 9), ACC is 2nd of 10 per tonne of cement (28,970,000 t) and 2nd of 10 on air.

# 8. Exclusion lists

For every peer group, we list each company we do not rank, with a plain reason and the values behind it (`exclusions_v12.py`, writing `CLBI_v1_exclusions.csv` and `CLBI_v1_exclusion_summary.csv`). Each company gets one category, tested in this order:

1. **Held back: implausible or inconsistent value.** The company has a held-back value (V3–V8, V10) on a pressure that counts in its group; the detail names the pressure, the test and the multiple of the peer median.
2. **Reported zero awaiting confirmation** (V1).
3. **Pressure not reported.**
4. **Revenue year or boundary does not match the BRSR** (V11).
5. **Peer group too small to rank** (Section 5).

**Table 8.1. Companies not ranked, by category.**

| Category | Companies |
|---|---:|
| Held back: implausible or inconsistent value | 24 |
| Peer group too small to rank | 25 |
| Pressure not reported | 16 |
| Revenue year or boundary does not match the BRSR | 13 |
| Reported zero awaiting confirmation | 13 |
| **Total not ranked** | **91** |

Appendix C gives the same counts for each peer group.

**A second view of the same 91.** If we assign each company to the *first* stage it fails, in data order, the counts are: no FY2025-26 BRSR source that could complete the required pressures, 25; a required pressure missing, 11; revenue not matched, 1; a held-back value, 21; a zero to confirm, 13; group or NSE sector below 8 members, 13; fewer than 8 complete companies in the group, 7. A missing XBRL file did not drop a company on its own. Of the 35 companies without one, we completed 10 from filed PDFs or public reports, and 7 of these are ranked (HYUNDAI, BPCL, HINDPETRO, PIRAMALFIN, ITI, KIOCL, HBLENGINE).

# 9. Supplementary views

These views leave the main rank unchanged.

**Air rank.** In groups where at least 8 companies with usable revenue report a usable NOx + SOx + PM mass, we score air with the formula of Section 7.2 and rank it. We rank **178 companies in 14 groups** on air. Many companies report stack concentrations, which no one can convert to tonnes, and 10 companies with more than 1 Mt of Scope 1 report no usable air tonnage.

**Output yardsticks: per tonne and per MWh.** Revenue favours companies that sell at a high price. We adopted a physical yardstick where it is recognised, often disclosed and hard to redefine. Of 23 groups and sub-groups tested, two passed (`research/comparator_table.csv`): **cement**, per tonne of cement produced, and **power**, per MWh generated. For each, we divide the core pressures by the output figure, then score and average them in the same way, with the zero and hold-back flags of Section 6. We rank ten cement companies and ten power generators this way. The Spearman correlation (Spearman 1904) with the revenue rank is 0.88 for cement and 0.85 for power. Transmission companies have no generation figure and sit outside the power view.

**Profit basis.** As a check, we divide each pressure by profit after tax. We leave out loss-making companies and flag a margin below 2% as unstable (`thin_profit_margin = 0.02`). 378 companies are ranked on this basis. Of the 500, 440 have a usable profit, 24 have none loaded, 21 made a loss and 15 have a margin below 2%. Across groups, the median correlation between revenue-based and profit-based ranks is 0.82 (Table 12.1).

# 10. Land and operating-site evidence

## 10.1 Land data in the BRSR

The BRSR asks for the *number* of plants and offices (Section A), a free-text table of operations in or near ecologically sensitive areas (P6 EI 11), and environmental impact assessments (EI 12). It has no field for hectares, coordinates, land-use change or restoration. Land data must come from annual reports, mining-lease tables and environmental-clearance (EC) letters, with mixed periods and boundaries. On 28 October we decided to show land as **evidence only**, with no score and no rank, until comparable data exist.

## 10.2 The Hermes search

An independent run with a different AI model (DeepSeek, called "Hermes") searched all 500 companies (`research/hermes/`). It worked to six rules:

- no figure without a primary document (company filing, exchange attachment, EC letter, or `.gov.in` or `.nic.in` page);
- "partial" means a real number for one plant, one subsidiary or an older year, and never a company total;
- restoration stays separate from land held;
- approximate figures ("~") carry no hectare value;
- coordinates appear where an EC document printed them, and nothing is geocoded;
- conflicts between an EC letter and a filing are recorded, never settled by choice.

The run produced 590 company rows (statuses: not disclosed in area 313; partial only 165; found 93; not found 19) and 326 site rows, and kept 710 source PDFs. `land_evidence_v12.py` merges these into one category per company. A first pass assigned categories from the period and boundary text. After the independent review (Appendix F), we **classified by hand** the 28 companies that pass had placed in its top two categories, reading their quotes (`inputs/land_category_overrides.csv`). We separated operational land held from real-estate land banks, single sites, leases, concessions and allotments. We corrected two figures to company totals from the same quotes: BEL, 3,075.49 acres = 1,244.6 ha; BHEL, 16,690.71 acres = 6,754.5 ha.

**Table 10.1. Land-evidence categories** (`CLBI_v1_land_evidence.csv`).

| Category | Definition | Companies |
|---|---|---:|
| A | Company-wide land held (total, or owned plus leased), checked by hand | 13 |
| R | Real-estate land bank (includes joint-development land) | 6 |
| B | Figure covers a different or partial boundary: a single site, a mining or petroleum lease, a subsidiary's concession, or a group boundary | 7 |
| C | Partial or older figure only, or a statement that is not land held (an allotment, a land-acquisition claim) | 51 |
| D | Offices only, or land not disclosed as an area | 115 |
| E | Land not disclosed as an area | 308 |
| | **Total** | **500** |

The 13 category A companies are BEL, BHEL, HAL, JSW Steel, Tech Mahindra, Vedanta, FACT, Shyam Metalics, Emmvee, Acutaas, NMDC Steel, JSW Infrastructure and Bharat Coking Coal; the last figure is for FY2024-25.

::: {.figure chart="land"}
**Figure 10.1. Land disclosure across the 500 companies** (categories of Table 10.1).
:::

**Sites.** 187 companies name at least one site, and 140 give an area for at least one (252 sites, median 21.0 ha). 9 companies print coordinates, for 10 sites. The "near a sensitive area" field holds 87 statements from 59 companies. On reading, 49 are denials and 20 are placeholders. That leaves 18 affirmative or hedged statements from 13 companies (15 affirmative from 12; 3 hedged from one), none with coordinates (`insights/pressures/PRESSURES.md`, §6). We found a restoration area on own land for 37 companies.

**Limits of the evidence.** Some category A figures sit on a different boundary from the BRSR. JSW Steel's covers its India operations including subsidiaries, against a standalone BRSR; Tech Mahindra's covers 13 Indian locations, against a consolidated BRSR. Field types differ too: a petroleum mining lease (Oil India, 482,884 ha) or a subsidiary's concession (NAVA, 36,000 ha) is a licence area, so both sit in category B. We publish no ratio of land to revenue.

## 10.3 Proposed future biodiversity metric

Once site data allow it, we propose a site-level pressure:

$$\mathrm{BP}_i = \sum_{s \in \mathcal{S}_i} a_s \,\bigl(1 - \mathrm{MSA}_{u(s)}\bigr)\, w_s \;-\; \sum_{s \in \mathcal{S}_i} a^{\mathrm{rest}}_s \,\Delta \mathrm{MSA}_s$$

where:

- $\mathcal{S}_i$ is the set of operating sites of company $i$ on its BRSR boundary;
- $a_s$ is the area of site $s$ in hectares;
- $u(s)$ is the land use of the site (for example open-cast mine, industrial plant, greenbelt);
- $\mathrm{MSA}_{u}$ is the mean species abundance under that land use: the mean abundance of the original species relative to an undisturbed state, from the GLOBIO model (Alkemade et al. 2009; Schipper et al. 2020). $1 - \mathrm{MSA}$ is the share of original abundance lost;
- $w_s \ge 1$ is a proximity weight that rises for sites inside or near protected areas, Key Biodiversity Areas, Ramsar sites, tiger reserves or eco-sensitive zones. An overlay of site polygons on the World Database on Protected Areas (UNEP-WCMC and IUCN 2026) and the KBA layer (IUCN 2016) would set it; we have not yet chosen its functional form;
- $a^{\mathrm{rest}}_s$ and $\Delta\mathrm{MSA}_s$ are the area restored on the company's own land and the MSA gain it achieves, so restoration offsets the same pressure, as the other offsets do.

$\mathrm{BP}_i$ would be in MSA-loss hectare-equivalents, divided by revenue like the other pressures. **We cannot compute it today.** It needs site areas and coordinates (or polygons, as SBTN requires for sites of 10 ha or more) for every material site, and coordinates exist for 10 of 326 named sites.

::: {.callout .limit}
**Limitation.** Land-use change is the largest direct driver of biodiversity loss on land (IPBES 2019), and the index cannot yet measure it. Until companies report site coordinates and areas, a land or biodiversity score would rest on the 13 companies (2.6%) that publish a company-wide figure for land held.
:::

# 11. Illustrative nature cost

**Status.** This is the second product in this paper, and we keep it apart from the first. It is illustrative and never enters a rank. It puts a price on reported pressure; it is no liability, expense, bill or valuation of any company.

## 11.1 Method

For each company and each priced pressure, we multiply the scored net quantity by a damage price in constant 2025 rupees:

$$\mathrm{NC}_{i,p} = \frac{q_{i,p}\;\pi_p}{10^{7}} \quad (₹\ \text{crore}), \qquad \mathrm{NC}_i = \sum_{p} \mathrm{NC}_{i,p}$$

where $q_{i,p}$ is the quantity as scored in Section 4 (climate $C_i$; energy $E_i$; water $W_i$; pollution $P_i$; NOx, SOx and PM each on its own) and $\pi_p$ is the price in ₹ per unit. The **headline metric** is the cost as a share of EBITDA, with the share of revenue alongside:

$$\mathrm{NC}^{\mathrm{EBITDA}}_i = 100 \times \frac{\mathrm{NC}_i}{\mathrm{EBITDA}_i}, \qquad \mathrm{NC}^{\mathrm{Rev}}_i = 100 \times \frac{\mathrm{NC}_i}{\mathrm{Rev}_i}$$

EBITDA is the FY2025-26 figure in `pat_fy2026.csv`. We compute the EBITDA share for every non-financial company with positive EBITDA (370 companies), and all peer-group medians use this basis. We flag thin-margin companies and keep them in. EBITDA does not suit banks, lenders and insurers (96 companies); it is not loaded for 12 companies and is zero or negative for 6. Where EBITDA is below 5% of revenue we flag the share as unstable (8 companies: FACT, PATANJALI, RADICO, UBL, ITI, AWL, REDINGTON, BASF).

**Presentation.** We report the EBITDA share as **peer-group medians with their interquartile range**. We show a company value with its flags and its low–high range, because a single questionable input, such as a Scope 1 figure flagged under rule V12, can dominate one value. The rules (`v11_extensions.py`, `nature_cost_block`; prices in `inputs/prices_v12.csv`):

- we do not cost a held-back value (Section 6);
- we show a company total where climate is costed, so totals compare;
- low and high totals use all low and all high prices;
- **we report per company or as peer-group medians.** We publish no sector or index total: the buyer and the generator both count Scope 2 and grid electricity, so sums across companies double-count;
- land is evidence only, and we do not cost it.

## 11.2 Prices

**Table 11.1. Central price set (set B)** (`inputs/prices_v12.csv`; method, conversions and sources in `insights/prices/PRICES_V12.md`).

| Pressure | Unit | Low | Central | High | Basis of the central value |
|---|---|---:|---:|---:|---|
| Climate (headline, India-borne) | ₹/tCO2e | 2,800 | 5,400 | 11,500 | 23.9% India share (median of Ricke et al. 2018, Tol 2019, Thaller et al. 2026) × US EPA (2023) global social cost of CO2 of ₹22,598 |
| Climate, global (reference only, never added) | ₹/tCO2e | 13,900 | 22,600 | 38,400 | US EPA (2023) at 2.0% (2.5% and 1.5% for low and high); of the order of Rennert et al. (2022) |
| Energy depletion | ₹/GJ non-renewable | 0 | 80 | 550 | CE Delft (2024) external price of fossil-resource scarcity; low 0 (scarcity rent already in fuel prices); high ReCiPe 2016 surplus cost at India's fossil mix |
| Water (priced by scarcity) | ₹/kL scored | 39.6 | 358 | 440 | IFVI and VBA (2026) India value factor for water consumption, including the cost of future access, scaled to India's industrial-weighted water stress (WRI Aqueduct 4.0: 4.07 against a national 4.11; Kuzma et al. 2023). Low: damage and opportunity-cost value (Kumar 2006; IFVI ecosystem services; CE Delft). High: IFVI value scaled to the "arid" stress band |
| Waste not recovered | ₹/t | 300 | 600 | 9,200 | Median of five income-adjusted landfill-damage values; high from the only India-specific estimate |
| SOx | ₹/t | 85,000 | 2,09,000 | 13,69,000 | Median of four India health-damage estimates, Indian value of statistical life (unchanged from v1.1) |
| NOx | ₹/t | 1,11,000 | 2,10,000 | 9,93,000 | Median of three estimates (unchanged) |
| PM | ₹/t | 1,55,000 | 3,06,000 | 9,34,000 | CE Delft PM10 value transferred to India (unchanged) |

**Sensitivity lenses.** We compute two alternatives for every company (columns `nature_cost_lens_A` and `nature_cost_lens_C`):

- **Lens A (damage-only water).** Set B, with water at ₹39.6/kL, the damage and opportunity-cost value without the future-access term.
- **Lens C (global value of life for air).** Set B, with air priced on a global value of statistical life: the IFVI Global Value Factor Database India rural factors, SOx ₹10.2 lakh, NOx ₹3.4 lakh and PM ₹15.9 lakh per tonne (as implemented in `v11_extensions.py`).

We do not apply site-level water stress. Company totals carry no location, so one national price applies to every company. The waste price rests on weaker evidence than the others: its five central sources lie within 2.6 times of each other, and the full range spans 31 times.

## 11.3 Results

We apply prices to 465 companies with a costed total. The headline is the peer-group median of the EBITDA share (Table 11.3 and Figure 11.1). Table 11.2 gives the median over all companies for context.

**Table 11.2. Illustrative nature cost across all costed companies (context for the peer-group medians).**

| Measure | Lens A (water ₹39.6/kL) | **Set B (central)** | Lens C (air at global VSL) | Companies |
|---|---:|---:|---:|---:|
| % of EBITDA | 3.3% | **4.4%** | 4.8% | 370 |
| % of revenue | 0.41% | **0.58%** | 0.59% | 460 |
| Share of costed total: climate | 76.3% | **68.8%** | 54.4% | 465 |
| water | 1.4% | **11.1%** | 8.8% | 465 |
| energy depletion | 10.6% | **9.5%** | 7.5% | 465 |
| air | 10.3% | **9.3%** | 28.4% | 465 |
| waste | 1.4% | **1.2%** | 1.0% | 465 |

The shares describe how the summed cost splits across pressures; the sum itself has no meaning as a total. Under set B the median company's climate share is 64.5%. Climate is the largest component for 356 of the 465 companies and water for 106; climate falls below half the total for 124. The cost exceeds EBITDA for 39 companies and revenue for 9. At the global social cost of carbon, the climate cost alone would be 4.19 times the India-borne figure (₹22,600 ÷ ₹5,400).

**Seawater kept out of priced water.** The water price is a freshwater value, and BRSR water consumption can include seawater. For the largest water users, we read the seawater inside reported consumption from each company's own BRSR (`insights/prices/seawater_split.csv`) and recorded it with its basis and a quote (`inputs/seawater_in_consumption.csv`): seawater withdrawn minus seawater discharged to sea, or the seawater consumption the report states. We remove it from the priced quantity for 7 companies (RELIANCE, ADANIPOWER, ONGC, BPCL, TATAPOWER, HINDPETRO, NLCINDIA), 408 million kL in all; JSWENERGY reports all its seawater returned, so we remove nothing. Where the filing is unclear (NTPC, VEDL, HINDALCO, TATACHEM, GRASIM, MRPL) we remove nothing, and their priced water may include seawater. The adjustment changes the nature cost and leaves the ranks alone; ranks use water as scored in Section 4 (column `water_priced_kl`).

::: {.figure chart="ebitda"}
**Figure 11.1. Illustrative nature cost as a share of EBITDA, by peer group** (set B; median and interquartile range; logarithmic scale; non-financial groups with at least 5 companies with positive EBITDA).
:::

**Table 11.3. Illustrative nature cost by peer group, % of EBITDA** (set B, with lens medians; basis: all 370 non-financial companies with positive EBITDA, thin-margin companies included and flagged; groups with at least 5).

| Peer group | n | Median (set B) | IQR | Lens A | Lens C |
|---|---:|---:|---:|---:|---:|
| Cement | 10 | 316.0% | 283.7%–368.2% | 311.6% | 334.1% |
| Metals: steel and iron products | 16 | 165.0% | 83.8%–320.6% | 156.1% | 178.3% |
| Power | 15 | 159.9% | 0.88%–323.6% | 145.8% | 219.0% |
| Chemicals: commodity chemicals and fertilisers | 17 | 50.8% | 8.8%–104.5% | 36.4% | 50.8% |
| Textiles and apparel | 7 | 42.4% | 25.8%–92.1% | 36.6% | 43.6% |
| Metals: non-ferrous and mining | 10 | 30.4% | 19.6%–105.1% | 21.7% | 34.4% |
| Oil, gas and fuels | 13 | 15.5% | 7.2%–26.2% | 15.5% | 15.5% |
| Transport and logistics | 9 | 14.6% | 2.2%–29.8% | 14.4% | 14.6% |
| Chemicals: specialty, paints and coatings | 16 | 11.1% | 2.1%–33.4% | 9.6% | 11.4% |
| Auto components and tyres | 27 | 9.0% | 4.3%–12.3% | 7.6% | 9.6% |
| Construction and engineering | 12 | 4.7% | 0.67%–8.8% | 2.8% | 4.8% |
| FMCG | 27 | 4.4% | 1.3%–13.1% | 3.1% | 5.3% |
| Healthcare: hospitals and diagnostics | 9 | 4.3% | 3.4%–4.8% | 2.1% | 4.3% |
| Healthcare: pharmaceuticals | 40 | 4.0% | 2.3%–6.9% | 3.1% | 4.3% |
| Capital goods: machinery, engineering and defence | 28 | 3.5% | 1.6%–6.2% | 1.9% | 3.6% |
| Retail, e-commerce, hotels and consumer services | 23 | 2.7% | 0.78%–4.5% | 1.6% | 2.7% |
| Capital goods: electrical equipment and electronics | 25 | 2.6% | 1.4%–4.1% | 2.2% | 2.9% |
| Consumer durables | 10 | 2.3% | 1.2%–7.0% | 1.7% | 2.3% |
| Real estate | 10 | 2.2% | 0.83%–9.7% | 1.4% | 2.2% |
| Automobiles | 11 | 1.2% | 0.94%–2.1% | 0.86% | 1.3% |
| Telecom and media | 8 | 0.52% | 0.20%–1.2% | 0.47% | 0.52% |
| IT services and software | 22 | 0.37% | 0.22%–0.53% | 0.21% | 0.37% |


::: {.figure chart="mix"}
**Figure 11.2. The cost by pressure, by peer group** (set B). Each bar splits the group's cost by pressure: the summed cost of each pressure divided by the group's summed cost, shown as a composition.
:::

**Table 11.4. Composition by peer group** (set B; groups with at least 5 costed companies; from `CLBI_v1_rankings_by_sector.xlsx`, sheet "Nature cost by sector"). Pressure shares are the median of each company's share; % of revenue is the median with the interquartile range.

| Peer group | n | % of revenue | IQR | Climate | Energy | Water | Air | Waste |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cement | 10 | 62.63 | 53.40–68.48 | 89% | 6% | 2% | 4% | 0.0% |
| Power | 15 | 38.01 | 0.76–130.93 | 67% | 7% | 10% | 12% | 0.0% |
| Metals: steel and iron products | 16 | 34.15 | 12.61–42.10 | 73% | 10% | 8% | 2% | 0.4% |
| Metals: non-ferrous and mining | 10 | 12.88 | 6.19–25.78 | 60% | 9% | 16% | 0% | 4.6% |
| Textiles and apparel | 7 | 7.04 | 4.27–10.59 | 65% | 6% | 20% | 1% | 0.1% |
| Chemicals: commodity chemicals and fertilisers | 18 | 6.44 | 1.63–14.34 | 65% | 9% | 19% | 3% | 0.1% |
| Chemicals: specialty, paints and coatings | 16 | 2.91 | 0.37–7.66 | 67% | 8% | 20% | 1% | 0.2% |
| Oil, gas and fuels | 14 | 2.08 | 1.11–3.81 | 73% | 13% | 12% | 1% | 0.0% |
| Transport and logistics | 9 | 1.61 | 1.40–8.18 | 60% | 9% | 15% | 0% | 0.0% |
| Auto components and tyres | 27 | 1.42 | 0.80–2.00 | 70% | 7% | 20% | 0% | 0.1% |
| Healthcare: pharmaceuticals | 40 | 1.15 | 0.76–1.85 | 66% | 6% | 25% | 2% | 0.1% |
| Healthcare: hospitals and diagnostics | 9 | 1.04 | 0.80–1.31 | 48% | 3% | 49% | 0% | 0.3% |
| Capital goods: machinery, engineering and defence | 28 | 0.88 | 0.29–1.73 | 55% | 5% | 31% | 0% | 0.4% |
| FMCG | 27 | 0.77 | 0.42–1.35 | 52% | 5% | 39% | 3% | 0.0% |
| Retail, e-commerce, hotels and consumer services | 22 | 0.64 | 0.27–1.78 | 56% | 5% | 39% | 0% | 0.1% |
| Construction and engineering | 12 | 0.59 | 0.13–1.17 | 50% | 7% | 43% | 0% | 0.1% |
| Real estate | 10 | 0.58 | 0.42–1.92 | 30% | 3% | 66% | 0% | 0.2% |
| Capital goods: electrical equipment and electronics | 24 | 0.43 | 0.25–0.60 | 75% | 6% | 18% | 0% | 0.1% |
| Automobiles | 13 | 0.21 | 0.18–0.32 | 55% | 6% | 33% | 3% | 0.2% |
| Consumer durables | 10 | 0.20 | 0.10–0.54 | 67% | 5% | 27% | 0% | 0.2% |
| Telecom and media | 8 | 0.15 | 0.10–0.54 | 86% | 7% | 7% | 0% | 0.0% |
| Financial Services: Banks | 26 | 0.10 | 0.08–0.13 | 69% | 5% | 25% | 0% | 0.0% |
| IT services and software | 22 | 0.07 | 0.06–0.14 | 50% | 3% | 46% | 0% | 0.1% |
| Financial Services: Capital markets and financial intermediaries | 15 | 0.07 | 0.04–0.14 | 64% | 5% | 30% | 0% | 0.0% |
| Financial Services: Lending NBFC and housing finance | 33 | 0.04 | 0.02–0.11 | 52% | 4% | 44% | 0% | 0.0% |
| Financial Services: Insurance underwriting | 11 | 0.03 | 0.01–0.03 | 34% | 3% | 63% | 0% | 0.0% |


**Worked example (ACC).** Climate 15,293,369 t × ₹5,400 = ₹8,258.42 crore; energy 66,063,577 GJ × ₹80 = ₹528.51 crore; water 4,141,552 kL × ₹358 = ₹148.27 crore; pollution 0.78 t × ₹600 = ₹468; air (7,996 t NOx × ₹2,10,000) + (457 t SOx × ₹2,09,000) + (259 t PM × ₹3,06,000) = ₹185.39 crore. Central total ₹9,120.59 crore (low ₹4,395.20 crore; high ₹22,283.86 crore). With EBITDA of ₹3,306.46 crore and no flag, this is 275.8% of EBITDA (range 132.9% to 673.9% at all-low and all-high prices) and 35.4% of revenue; lens A gives ₹8,988.72 crore (271.9% of EBITDA) and lens C ₹9,294.85 crore (281.1%). The global-SCC reference for climate alone would be ₹34,563.01 crore.

::: {.callout .meaning}
**What this means.** At India-borne prices, carbon makes up 68.8% of the unpriced cost, and the second pressure depends on the sector: water in services, real estate and hospitals; energy depletion and air in heavy industry. For the median company the cost is a few per cent of EBITDA. For cement, steel and coal power it exceeds EBITDA. Treat these as orders of magnitude for discussion; none of them is a liability.
:::

::: {.callout .limit}
**Price convention: checked.** Set B mixes conversion conventions. The water price of ₹358/kL is a global-perspective IFVI value converted at purchasing-power parity; carbon uses the market exchange rate. We decided on 28 October to keep set B. As a check, we recomputed every price from one standard (IFVI and CE Delft) and converted all of them by a single convention (`insights/prices/convention_check.csv`). The cost mix comes out the same under purchasing-power parity and under the market exchange rate: carbon 71.6–71.9%, water 15.0–15.1%, energy 2.6–2.7%, air 9.3–9.4%, waste 1.2%. The comparable set B row, before the seawater adjustment, gives carbon 66.8%, water 13.3%, energy 9.6%, air 9.1%, waste 1.2% (same file). The conclusions hold under either convention. Three caveats remain. Each price transfers published estimates, several from outside India. The IFVI water value is per kilolitre of freshwater, so we keep seawater out of the priced quantity where the filing allows (Section 11.3). The waste price rests on five sources of modest quality.
:::

# 12. Robustness and sensitivity

We computed three alternative constructions for every ranked group (`CLBI_v1_robustness.csv`) and compared each with the published score by Spearman's rank correlation $\rho$ (Spearman 1904). The composite-indicator literature recommends testing how each construction choice moves ranks (Saisana, Saltelli and Tarantola 2005; OECD and JRC 2008).

1. **Net vs gross.** We replace each pressure by its gross figure (total energy, water withdrawn, waste generated) and score and average as before. This shows how far the offsets move ranks.
2. **Leave one pressure out.** We recompute the final score four times, each time without one core pressure, and report the lowest of the four correlations.
3. **Revenue vs profit.** We compare the revenue-based final score with the profit-based one.

**Table 12.1. Rank correlations by peer group.**

| Peer group | Ranked | ρ net vs gross | Min ρ, leave one out | ρ revenue vs profit | n (profit) |
|---|---:|---:|---:|---:|---:|
| Auto components and tyres | 27 | 0.94 | 0.96 | 0.78 | 27 |
| Automobiles | 12 | 0.82 | 0.90 | 0.84 | 10 |
| Capital goods: electrical equipment and electronics | 24 | 0.89 | 0.96 | 0.86 | 24 |
| Capital goods: machinery, engineering and defence | 25 | 0.92 | 0.94 | 0.95 | 25 |
| Cement | 10 | 0.94 | 0.89 | 0.85 | 9 |
| Chemicals: commodity chemicals and fertilisers | 17 | 0.89 | 0.93 | 0.70 | 14 |
| Chemicals: specialty, paints and coatings | 15 | 0.94 | 0.92 | 0.86 | 15 |
| Construction and engineering | 12 | 0.99 | 0.97 | 0.88 | 12 |
| Consumer durables | 10 | 0.92 | 0.93 | 0.85 | 9 |
| FMCG | 27 | 0.85 | 0.93 | 0.89 | 26 |
| Financial Services: Banks | 25 | 0.93 | 0.91 | 0.52 | 25 |
| Financial Services: Capital markets and financial intermediaries | 12 | 0.92 | 0.92 | 0.82 | 12 |
| Financial Services: Insurance underwriting | 9 | 0.98 | 0.95 | – | 0 |
| Financial Services: Lending NBFC and housing finance | 29 | 0.95 | 0.92 | 0.92 | 28 |
| Healthcare: hospitals and diagnostics | 9 | 0.87 | 0.90 | 0.71 | 9 |
| Healthcare: pharmaceuticals | 40 | 0.95 | 0.96 | 0.74 | 38 |
| IT services and software | 20 | 0.79 | 0.83 | 0.69 | 20 |
| Metals: non-ferrous and mining | 9 | 0.93 | 0.95 | 0.88 | 9 |
| Metals: steel and iron products | 15 | 0.97 | 0.97 | 0.82 | 15 |
| Oil, gas and fuels | 13 | 0.98 | 0.97 | 0.61 | 12 |
| Power | 13 | 0.95 | 0.97 | 0.96 | 13 |
| Real estate | 9 | 0.87 | 0.93 | 0.65 | 9 |
| Retail, e-commerce, hotels and consumer services | 19 | 0.98 | 0.94 | 0.64 | 17 |
| Transport and logistics | 8 | 0.90 | 0.81 | 0.43 | 7 |


::: {.figure chart="robust"}
**Figure 12.1. Rank stability by peer group.** Spearman correlation between the published score and three alternatives; 1.0 means identical order.
:::

**Reading the table.**

- **Offsets.** Net and gross ranks agree (median 0.93). Agreement is lowest in IT services and software (0.79) and automobiles (0.82), where renewable power and water recycling vary most.
- **Weights.** Dropping any one pressure changes ranks little (median of the group minima 0.93); the lowest is transport and logistics (0.81). No single pressure drives the ranking.
- **Denominator.** Revenue and profit ranks agree less (median 0.82), and least where margins vary most: transport and logistics (0.43) and banks (0.52). Insurance has no profit-basis ranks.
- **Untested choices.** We have not varied the thresholds of Section 6 (300×, 1.5×, 10×, 90%, the 20% tolerance), the minimum group size or the peer-group placements. Before publication we recommend a full uncertainty analysis that samples them together (Saisana et al. 2005).

# 13. Limitations

- **Pressure, as reported.** CNPI measures reported drivers of nature loss. It does not measure biodiversity or change in it.
- **Own operations.** We leave out supply chains, product use and financed impacts; for food, textiles and banks the operational footprint is a small part of the whole.
- **Self-reported data.** We take values as published. Auditors assure many of them under BRSR Core (SEBI 2023), but we do not audit them. More than half the ranked companies (221 of 409) rest on at least one value that needed reconciliation, a unit rule, a correction or a public-report fill.
- **Revenue as denominator** favours companies that sell high-value products. Cement and power have a physical alternative (Section 9); the other groups have none.
- **Mixed boundaries.** Standalone and consolidated filers sit in the same groups (312 and 96 among the ranked). With these data you cannot separate the boundary effect from business mix.
- **Undeclared Scope 2.** In practice most Scope 2 figures are location-based and use the previous year's grid factor (0.710 for FY2024-25; 0.675 for FY2025-26, CEA 2026). A within-filing test (Scope 2 ÷ purchased non-renewable electricity outside 0.5–1.0 tCO2/MWh) flags 42 companies. Rule V5 holds back three of them; the other 39, 34 of them ranked, pass every hold-back rule.
- **Captive power** moves emissions between Scope 1 and Scope 2 according to who owns the plant, whatever it emits.
- **Unknown water location.** Company totals carry no basin, so a kilolitre in a stressed basin counts the same as one in an abundant basin.
- **"Recovered" waste** includes fly ash sent to cement and overburden used as backfill. A near-total offset may reward a reporting category as much as a practice; 62 companies have net waste of zero or less before the zero floor.
- **Small groups.** In groups of 8–10 companies, one changed value moves ranks more.
- **A narrow assumed-discharge rule.** Rule V7 scores water on withdrawal where consumption is 20% of withdrawal. We score other round ratios that may also be assumptions as reported, and the rule changes leaders in office-based groups.
- **Mixed Scope 2 conventions.** Rule V2 accepts a zero Scope 2 where the renewable share is at least 90%, which fits a market-based figure, while most filings are location-based in practice.
- **Naming cautions** flag 31 ranked companies whose business model, boundary or a reported value needs checking before anyone names them.
- **Equal weights** are a normative choice.
- **Percentile base.** We score each pressure over all companies with a usable value on it, including some whose rank we withhold (Section 7.2). A published score can depend on companies missing from the rank.
- **Untested thresholds.** See Section 12.
- **One year.** Version 1.2 is a snapshot and shows no change over time.

# 14. What a full corporate nature index would require

CNPI v1.2 uses what the BRSR provides, and a defensible corporate nature index needs more. Table 14.1 condenses the one-sheet comparison in `insights/pressures/DATA_NEEDS.md`, which maps each parameter against the TNFD recommendations (TNFD 2023, and the October 2026 core global indicators), GRI 101 (GRI 2024), IFRS S2 (ISSB 2023), ESRS and SBTN. Severity: *critical*, the BRSR does not ask and nothing usable exists; *high*, it asks in loose or voluntary terms and comparability fails; *medium*, the number exists but its metadata prevent clean comparison.

**Table 14.1. Data needs by parameter.**

| Parameter | BRSR today | Observed in CNPI v1.2 | Gap | The one disclosure ask |
|---|---|---|---|---|
| Climate | EI 7: Scope 1 and 2 totals; Scope 3 voluntary | 473/500 with Scope 1+2; method stated in 16/465; Scope 3 resolvable in 141/465 | Medium | State the Scope 2 method and grid-factor version, report location- and market-based separately, and state the GHG consolidation boundary |
| Energy | EI 1: electricity, fuel, other; renewable vs non-renewable | 473/500; 38 values for 13 companies corrected by hand; captive generation not identifiable | Medium | Report grid-purchased and self-generated electricity on separate lines, naming the fuel already counted |
| Water quantity | EI 3–4: withdrawal by source, consumption, discharge (company level) | 473/500; consumption above withdrawal in 26; assumed 80% discharge in 30 | Medium | Compute consumption as withdrawal minus discharge (± storage); report seawater separately |
| Water location and stress | LI 1 (voluntary): area name only | No facility coordinates in the BRSR | High | Mandatory facility table with district, coordinates and the water-stress dataset named |
| Wastewater | EI 4: volume by destination and treatment | Pollutant loads not asked | High | Annual loads (COD, BOD, N, P) per discharge point |
| Waste | EI 9: eight categories; recovered and disposed by route | 472/500; recovered > generated in 25; unscored in 4 groups (incl. real estate) | Medium | Named lines for fly ash, overburden, tailings and slag; recovery from stock reported separately |
| Air | EI 6: pollutants with "please specify unit" | Mass for 245/500; 111 companies' values not usable as mass | High | NOx, SOx and PM in tonnes per year |
| Land use | Number of plants and offices only | Company-wide land held for 13/500; site areas for 140 companies | Critical | Hectares owned, leased and under mining lease, plus area disturbed and restored in the year |
| Biodiversity and sensitive sites | EI 11 free-text table; LI 3 narrative | Coordinates for 10/326 sites; 18 affirmative sensitive-site statements | Critical | Coordinates (polygons for sites ≥ 10 ha) and area for every operating site |
| Value chain | LI 2 Scope 3 (voluntary); sourcing share in % | Commodity tonnes by origin not asked | Critical | Tonnes of high-impact natural commodities by type and origin, with share certified |

The asks with the largest return concern **location and units**: site coordinates, water by facility, land area, air in tonnes and the Scope 2 method. Most companies already hold this information in environmental-clearance and consent documents, so the asks concern format more than new measurement.

# 15. Reproducibility

**Scripts** (all in `/home/claude/CLBI_work_2026-10-24/`, Python 3 with pandas, NumPy, SciPy and openpyxl):

| Order | Script | Reads | Writes |
|---:|---|---|---|
| 1 | `consolidate_gapfill.py` | gap-fill agent results | `inputs/gapfill_values.csv`, `research/gapfill_QA.csv` |
| 2 | `consolidate_energy.py` | energy agent results | `inputs/gapfill_energy.csv`, `research/energy_QA.csv` |
| 3 | `build_clbi.py` (with `v11_extensions.py`) | Codex snapshot and `inputs/` | `outputs_v12/`: scores, company data, data queries, robustness, workbook, `build_stats.json` |
| 4 | `land_evidence_v12.py` | `research/hermes/` and the scores file | `CLBI_v1_land_evidence.csv`, `CLBI_v1_land_sites.csv` |
| 5 | `exclusions_v12.py` | scores and data queries | `CLBI_v1_exclusions.csv`, `CLBI_v1_exclusion_summary.csv` |
| 6 | `make_dataset_v12.py` | `outputs_v12/`, `inputs/` | `deliverables_v12/CNPI_v1.2_Dataset.xlsx` |

**Rebuild command** for step 3:

```
python3 build_clbi.py --codex /home/claude/codex --out outputs_v12 --inputs inputs
```

**Parameters.** The dictionary `P` at the top of `build_clbi.py` holds every judgement, and each build copies it into `build_stats.json` (Appendix B).

**Input fingerprints.** `build_stats.json` records the SHA-256 hash of the 10 frozen Codex inputs (`input_sha256`) and of every CSV in `inputs/` (`inputs_sha256`, 20 files at this build). A change to any input changes its hash. The fingerprints of this build begin: `normalized_companies.json` cc960e972362d4df; `Physical_Variable_Accounts_15500.csv` 8d94ff002faf1bd9; `financial_revenue_ledger_all500.csv` f4fb2656c6836e29; `peer_groups_v12.csv` 0c60579cb02a8c44; `gapfill_values.csv` 526c074cffab0195; `gapfill_energy.csv` 3cbc4eba65993355; `prices_v12.csv` 142cdfbab49c4e2a; `seawater_in_consumption.csv` 9fdbcd5211c0b0d9.

**Spreadsheet check.** The dataset workbook recomputes intensities, scores and ranks for all 500 companies with spreadsheet formulas, so you can check the arithmetic without Python.

**Known code notes.**

- `build_clbi.py` reads `inputs/query_resolutions.csv` (467 rows, 461 marked "confirmed") and does not apply it: a confirmation does not release a held value in this build. Corrections reach the build through `gapfill_values.csv`.
- 41 gap-fill rows still show "page nan" in `source_field`: they record the source URL and lack the page.
- Version 1.2 sets the positive-action credit of v1.1 to zero (all `credit_*` parameters are 0); the code path remains.
- The `build_stats.json` field `sectors_ranked` (17) counts NSE sectors, after moves, with at least 8 members; it does not count peer groups.

# Annex: Peer-group profiles

Each peer group has one profile, in order of size, and we computed every figure from `outputs_v12`. *Median intensity* is the median net value per ₹ crore of revenue among companies with a usable value. *Spread* is the highest usable positive climate intensity divided by the lowest. *Highest-ranked without caution* is the best-ranked company with no naming caution (Section 6, V13); we name it to illustrate the method, and the naming endorses nothing. Nature cost uses set B, as a median share of EBITDA (non-financial groups) or of revenue (financial groups), where we cost at least 5 companies.

## Healthcare: pharmaceuticals

::: {.profile}
[40 of 40 members ranked on climate, energy, water, pollution. Climate intensity spans 392× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 40 / 40 / 26 |
| Drawn from NSE sectors | Healthcare (40) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 13.6 tCO2e/₹ cr (n = 40) |
| Median intensity, energy | 79.9 GJ/₹ cr (n = 40) |
| Median intensity, water | 77.6 kL/₹ cr (n = 40) |
| Median intensity, pollution | 0.250 t/₹ cr (n = 40) |
| Highest-ranked without caution | GlaxoSmithkline Pharmaceuticals Ltd. (rank 4, score 89.1) |
| Ranked with a naming caution | 5 |
| Rank correlation: net vs gross / min leave-one-out | 0.95 / 0.96 |
| Illustrative nature cost, median | 4.0% of EBITDA (n = 40) |

**Not ranked:** none; every member is ranked.
:::

## Financial Services: Lending NBFC and housing finance

::: {.profile}
[29 of 33 members ranked on climate, energy, water, pollution. Climate intensity spans 357× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 33 / 29 / 0 |
| Drawn from NSE sectors | Financial Services (33) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 0.477 tCO2e/₹ cr (n = 32) |
| Median intensity, energy | 2.37 GJ/₹ cr (n = 33) |
| Median intensity, water | 4.00 kL/₹ cr (n = 31) |
| Median intensity, pollution | 0.00045 t/₹ cr (n = 32) |
| Highest-ranked without caution | REC LIMITED (rank 1, score 93.1) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.95 / 0.92 |
| Illustrative nature cost, median | 0.04% of revenue (n = 33) |

**Not ranked (4):** Bajaj Finance Limited (held back); Bajaj Finserv Limited (held back); Home First Finance Company India Limited (not reported); Authum Investment & Infrastructure Limited (zero to confirm).
:::

## Auto components and tyres

::: {.profile}
[27 of 29 members ranked on climate, energy, water, pollution. Climate intensity spans 224× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 29 / 27 / 15 |
| Drawn from NSE sectors | Automobile and Auto Components (27); Capital Goods (1); Fast Moving Consumer Goods (1) |
| Moved in from another NSE sector | 2 |
| Median intensity, climate | 18.4 tCO2e/₹ cr (n = 27) |
| Median intensity, energy | 119 GJ/₹ cr (n = 27) |
| Median intensity, water | 70.6 kL/₹ cr (n = 27) |
| Median intensity, pollution | 0.178 t/₹ cr (n = 27) |
| Highest-ranked without caution | Tenneco Clean Air India Limited (rank 1, score 94.2) |
| Ranked with a naming caution | 1 |
| Rank correlation: net vs gross / min leave-one-out | 0.94 / 0.96 |
| Illustrative nature cost, median | 9.0% of EBITDA (n = 27) |

**Not ranked (2):** CIE Automotive India Limited (revenue mismatch); Schaeffler India Limited (revenue mismatch).
:::

## FMCG

::: {.profile}
[27 of 28 members ranked on climate, energy, water, pollution. Climate intensity spans 954× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 28 / 27 / 22 |
| Drawn from NSE sectors | Fast Moving Consumer Goods (28) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 6.24 tCO2e/₹ cr (n = 27) |
| Median intensity, energy | 31.3 GJ/₹ cr (n = 27) |
| Median intensity, water | 61.8 kL/₹ cr (n = 27) |
| Median intensity, pollution | 0.032 t/₹ cr (n = 27) |
| Highest-ranked without caution | United Spirits Limited (rank 1, score 88.5) |
| Ranked with a naming caution | 3 |
| Rank correlation: net vs gross / min leave-one-out | 0.85 / 0.93 |
| Illustrative nature cost, median | 4.4% of EBITDA (n = 27) |

**Not ranked (1):** Varun Beverages Limited (revenue mismatch).
:::

## Capital goods: machinery, engineering and defence

::: {.profile}
[25 of 31 members ranked on climate, energy, water, pollution. Climate intensity spans 320× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 31 / 25 / 11 |
| Drawn from NSE sectors | Capital Goods (31) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 5.16 tCO2e/₹ cr (n = 27) |
| Median intensity, energy | 38.6 GJ/₹ cr (n = 28) |
| Median intensity, water | 50.3 kL/₹ cr (n = 29) |
| Median intensity, pollution | 0.435 t/₹ cr (n = 30) |
| Highest-ranked without caution | Zen Technologies Ltd. (rank 1, score 82.2) |
| Ranked with a naming caution | 2 |
| Rank correlation: net vs gross / min leave-one-out | 0.92 / 0.94 |
| Illustrative nature cost, median | 3.5% of EBITDA (n = 28) |

**Not ranked (6):** BEML Ltd (held back); Ingersoll-Rand (India) Ltd. (held back); Thermax Ltd. (held back); SKF INDIA (INDUSTRIAL) LIMITED (not reported); Azad Engineering Limited (zero to confirm); KSB LIMITED (revenue mismatch).
:::

## Financial Services: Banks

::: {.profile}
[25 of 27 members ranked on climate, energy, water, pollution. Climate intensity spans 34× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 27 / 25 / 0 |
| Drawn from NSE sectors | Financial Services (27) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 1.17 tCO2e/₹ cr (n = 26) |
| Median intensity, energy | 6.21 GJ/₹ cr (n = 26) |
| Median intensity, water | 6.97 kL/₹ cr (n = 25) |
| Median intensity, pollution | 0.0008 t/₹ cr (n = 26) |
| Highest-ranked without caution | ICICI Bank Ltd. (rank 1, score 84.8) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.93 / 0.91 |
| Illustrative nature cost, median | 0.10% of revenue (n = 26) |

**Not ranked (2):** Central Bank of India (held back); Jammu and Kashmir Bank Ltd. (held back).
:::

## Capital goods: electrical equipment and electronics

::: {.profile}
[24 of 29 members ranked on climate, energy, water, pollution. Climate intensity spans 68× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 29 / 24 / 10 |
| Drawn from NSE sectors | Capital Goods (23); Consumer Durables (3); Telecommunication (2); Information Technology (1) |
| Moved in from another NSE sector | 6 |
| Median intensity, climate | 6.91 tCO2e/₹ cr (n = 24) |
| Median intensity, energy | 37.7 GJ/₹ cr (n = 24) |
| Median intensity, water | 15.8 kL/₹ cr (n = 24) |
| Median intensity, pollution | 0.049 t/₹ cr (n = 24) |
| Highest-ranked without caution | NETWEB TECHNOLOGIES INDIA LIMITED (rank 1, score 94.6) |
| Ranked with a naming caution | 1 |
| Rank correlation: net vs gross / min leave-one-out | 0.89 / 0.96 |
| Illustrative nature cost, median | 2.6% of EBITDA (n = 25) |

**Not ranked (5):** Aditya Infotech Limited (not reported); Emmvee Photovoltaic Power Limited (not reported); ABB India Limited (revenue mismatch); Siemens Energy India Limited (revenue mismatch); Siemens Ltd. (revenue mismatch).
:::

## IT services and software

::: {.profile}
[20 of 24 members ranked on climate, energy, water, pollution. Climate intensity spans 38× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 24 / 20 / 12 |
| Drawn from NSE sectors | Information Technology (19); Financial Services (2); Services (2); Healthcare (1) |
| Moved in from another NSE sector | 5 |
| Median intensity, climate | 0.849 tCO2e/₹ cr (n = 22) |
| Median intensity, energy | 3.47 GJ/₹ cr (n = 20) |
| Median intensity, water | 10.6 kL/₹ cr (n = 22) |
| Median intensity, pollution | 0.0095 t/₹ cr (n = 21) |
| Highest-ranked without caution | Persistent Systems Limited (rank 1, score 75.6) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.79 / 0.83 |
| Illustrative nature cost, median | 0.37% of EBITDA (n = 22) |

**Not ranked (4):** KPIT Technologies Ltd (held back); Fractal Analytics Limited (not reported); Pine Labs Limited (not reported); Hexaware Technologies Limited (revenue mismatch).
:::

## Retail, e-commerce, hotels and consumer services

::: {.profile}
[19 of 27 members ranked on climate, energy, water, pollution. Climate intensity spans 748× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 27 / 19 / 9 |
| Drawn from NSE sectors | Consumer Services (24); Services (2); Consumer Durables (1) |
| Moved in from another NSE sector | 3 |
| Median intensity, climate | 8.07 tCO2e/₹ cr (n = 21) |
| Median intensity, energy | 48.2 GJ/₹ cr (n = 22) |
| Median intensity, water | 34.0 kL/₹ cr (n = 22) |
| Median intensity, pollution | 0.179 t/₹ cr (n = 20) |
| Highest-ranked without caution | Lenskart Solutions Limited (rank 3, score 77.3) |
| Ranked with a naming caution | 2 |
| Rank correlation: net vs gross / min leave-one-out | 0.98 / 0.94 |
| Illustrative nature cost, median | 2.7% of EBITDA (n = 23) |

**Not ranked (8):** Eternal Limited (held back); Metro Brands Limited (held back); ITC Hotels Limited (not reported); Physicswallah Limited (not reported); Urban Company Limited (not reported); BLS International Services Ltd (zero to confirm); Meesho Limited (zero to confirm); International Gemological Institute Limited (revenue mismatch).
:::

## Chemicals: commodity chemicals and fertilisers

::: {.profile}
[17 of 18 members ranked on climate, energy, water, pollution. Climate intensity spans 152× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 18 / 17 / 13 |
| Drawn from NSE sectors | Chemicals (15); Diversified (2); Capital Goods (1) |
| Moved in from another NSE sector | 3 |
| Median intensity, climate | 61.0 tCO2e/₹ cr (n = 17) |
| Median intensity, energy | 700 GJ/₹ cr (n = 18) |
| Median intensity, water | 268 kL/₹ cr (n = 18) |
| Median intensity, pollution | 0.414 t/₹ cr (n = 18) |
| Highest-ranked without caution | Supreme Petrochem Ltd. (rank 2, score 79.3) |
| Ranked with a naming caution | 1 |
| Rank correlation: net vs gross / min leave-one-out | 0.89 / 0.93 |
| Illustrative nature cost, median | 50.8% of EBITDA (n = 17) |

**Not ranked (1):** Himadri Speciality Chemical Ltd. (zero to confirm).
:::

## Chemicals: specialty, paints and coatings

::: {.profile}
[15 of 17 members ranked on climate, energy, water, pollution. Climate intensity spans 93× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 17 / 15 / 13 |
| Drawn from NSE sectors | Chemicals (11); Consumer Durables (4); Diversified (1); Oil Gas & Consumable Fuels (1) |
| Moved in from another NSE sector | 6 |
| Median intensity, climate | 38.2 tCO2e/₹ cr (n = 16) |
| Median intensity, energy | 344 GJ/₹ cr (n = 16) |
| Median intensity, water | 70.9 kL/₹ cr (n = 15) |
| Median intensity, pollution | 0.357 t/₹ cr (n = 15) |
| Highest-ranked without caution | JSW Dulux Limited (rank 1, score 85.7) |
| Ranked with a naming caution | 1 |
| Rank correlation: net vs gross / min leave-one-out | 0.94 / 0.92 |
| Illustrative nature cost, median | 11.1% of EBITDA (n = 16) |

**Not ranked (2):** PRIVI SPECIALITY CHEMICALS LIMITED (held back); Castrol India Ltd (revenue mismatch).
:::

## Metals: steel and iron products

::: {.profile}
[15 of 17 members ranked on climate, energy, water, pollution. Climate intensity spans 309× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 17 / 15 / 9 |
| Drawn from NSE sectors | Metals & Mining (8); Capital Goods (7); Automobile and Auto Components (1); Power (1) |
| Moved in from another NSE sector | 9 |
| Median intensity, climate | 478 tCO2e/₹ cr (n = 16) |
| Median intensity, energy | 4,674 GJ/₹ cr (n = 16) |
| Median intensity, water | 615 kL/₹ cr (n = 17) |
| Median intensity, pollution | 2.86 t/₹ cr (n = 17) |
| Highest-ranked without caution | Jindal Stainless Limited (rank 3, score 81.4) |
| Ranked with a naming caution | 4 |
| Rank correlation: net vs gross / min leave-one-out | 0.97 / 0.97 |
| Illustrative nature cost, median | 165.0% of EBITDA (n = 16) |

**Not ranked (2):** GALLANTT ISPAT LIMITED (held back); Shyam Metalics and Energy Limited (held back).
:::

## Power

::: {.profile}
[13 of 17 members ranked on climate, energy, water. Climate intensity spans 1,202× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 17 / 13 / 8 |
| Drawn from NSE sectors | Power (17) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 325 tCO2e/₹ cr (n = 14) |
| Median intensity, energy | 5,693 GJ/₹ cr (n = 15) |
| Median intensity, water | 2,401 kL/₹ cr (n = 14) |
| Median intensity, pollution (shown, not scored) | 0.036 t/₹ cr (n = 10) |
| Highest-ranked without caution | NHPC Limited (rank 2, score 89.9) |
| Ranked with a naming caution | 5 |
| Rank correlation: net vs gross / min leave-one-out | 0.95 / 0.97 |
| Illustrative nature cost, median | 159.9% of EBITDA (n = 15) |

**Not ranked (4):** Adani Energy Solutions Limited (held back); Vedanta Power Limited (not reported); Reliance Power Limited (zero to confirm); Clean Max Enviro Energy Solutions Limited (revenue mismatch).
:::

## Oil, gas and fuels

::: {.profile}
[13 of 15 members ranked on climate, energy, water, pollution. Climate intensity spans 62× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 15 / 13 / 8 |
| Drawn from NSE sectors | Oil Gas & Consumable Fuels (15) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 25.1 tCO2e/₹ cr (n = 14) |
| Median intensity, energy | 294 GJ/₹ cr (n = 14) |
| Median intensity, water | 85.8 kL/₹ cr (n = 14) |
| Median intensity, pollution | 0.078 t/₹ cr (n = 13) |
| Highest-ranked without caution | Aegis Logistics Ltd. (rank 1, score 92.0) |
| Ranked with a naming caution | 1 |
| Rank correlation: net vs gross / min leave-one-out | 0.98 / 0.97 |
| Illustrative nature cost, median | 15.5% of EBITDA (n = 13) |

**Not ranked (2):** Indraprashtha Gas Ltd. (held back); Vedanta Oil and Gas Limited (not reported).
:::

## Financial Services: Capital markets and financial intermediaries

::: {.profile}
[12 of 18 members ranked on climate, energy, water, pollution. Climate intensity spans 88× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 18 / 12 / 0 |
| Drawn from NSE sectors | Financial Services (18) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 0.899 tCO2e/₹ cr (n = 14) |
| Median intensity, energy | 4.41 GJ/₹ cr (n = 16) |
| Median intensity, water | 4.27 kL/₹ cr (n = 17) |
| Median intensity, pollution | 0.00088 t/₹ cr (n = 15) |
| Highest-ranked without caution | 360 ONE WAM LIMITED (rank 1, score 76.7) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.92 / 0.92 |
| Illustrative nature cost, median | 0.07% of revenue (n = 15) |

**Not ranked (6):** Aditya Birla Sun Life AMC Limited (held back); Choice International Ltd (held back); Anand Rathi Wealth Limited (zero to confirm); ICICI Prudential Asset Management Company Limited (zero to confirm); Nuvama Wealth Management Limited (zero to confirm); CRISIL Ltd. (revenue mismatch).
:::

## Automobiles

::: {.profile}
[12 of 14 members ranked on climate, energy, water, pollution. Climate intensity spans 28× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 14 / 12 / 12 |
| Drawn from NSE sectors | Automobile and Auto Components (11); Capital Goods (3) |
| Moved in from another NSE sector | 3 |
| Median intensity, climate | 2.16 tCO2e/₹ cr (n = 13) |
| Median intensity, energy | 16.0 GJ/₹ cr (n = 13) |
| Median intensity, water | 19.2 kL/₹ cr (n = 13) |
| Median intensity, pollution | 0.084 t/₹ cr (n = 12) |
| Highest-ranked without caution | TATA MOTORS PASSENGER VEHICLES LIMITED (rank 1, score 86.7) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.82 / 0.90 |
| Illustrative nature cost, median | 1.2% of EBITDA (n = 11) |

**Not ranked (2):** TVS Motor Company Ltd. (held back); Ather Energy Limited (not reported).
:::

## Construction and engineering

::: {.profile}
[12 of 13 members ranked on climate, energy, water. Climate intensity spans 59× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 13 / 12 / 0 |
| Drawn from NSE sectors | Construction (11); Telecommunication (1); Services (1) |
| Moved in from another NSE sector | 2 |
| Median intensity, climate | 5.17 tCO2e/₹ cr (n = 12) |
| Median intensity, energy | 49.8 GJ/₹ cr (n = 12) |
| Median intensity, water | 72.3 kL/₹ cr (n = 12) |
| Median intensity, pollution (shown, not scored) | 0.943 t/₹ cr (n = 8) |
| Highest-ranked without caution | IRCON International Ltd (rank 1, score 93.9) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.99 / 0.97 |
| Illustrative nature cost, median | 4.7% of EBITDA (n = 12) |

**Not ranked (1):** Central Mine Planning & Design Institute Limited (not reported).
:::

## Cement

::: {.profile}
[10 of 10 members ranked on climate, energy, water, pollution. Climate intensity spans 3× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 10 / 10 / 10 |
| Drawn from NSE sectors | Construction Materials (10) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 1,020 tCO2e/₹ cr (n = 10) |
| Median intensity, energy | 4,258 GJ/₹ cr (n = 10) |
| Median intensity, water | 243 kL/₹ cr (n = 10) |
| Median intensity, pollution | 7.7e-05 t/₹ cr (n = 10) |
| Highest-ranked without caution | ACC Ltd (rank 1, score 86.1) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.94 / 0.89 |
| Illustrative nature cost, median | 316.0% of EBITDA (n = 10) |

**Not ranked:** none; every member is ranked.
:::

## Consumer durables

::: {.profile}
[10 of 10 members ranked on climate, energy, water, pollution. Climate intensity spans 71× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 10 / 10 / 0 |
| Drawn from NSE sectors | Consumer Durables (9); Fast Moving Consumer Goods (1) |
| Moved in from another NSE sector | 1 |
| Median intensity, climate | 2.28 tCO2e/₹ cr (n = 10) |
| Median intensity, energy | 13.3 GJ/₹ cr (n = 10) |
| Median intensity, water | 13.3 kL/₹ cr (n = 10) |
| Median intensity, pollution | 0.040 t/₹ cr (n = 10) |
| Highest-ranked without caution | Crompton Greaves Consumer Electricals Limited (rank 3, score 66.7) |
| Ranked with a naming caution | 4 |
| Rank correlation: net vs gross / min leave-one-out | 0.92 / 0.93 |
| Illustrative nature cost, median | 2.3% of EBITDA (n = 10) |

**Not ranked:** none; every member is ranked.
:::

## Metals: non-ferrous and mining

::: {.profile}
[9 of 13 members ranked on climate, energy, water. Climate intensity spans 303× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 13 / 9 / 0 |
| Drawn from NSE sectors | Metals & Mining (11); Oil Gas & Consumable Fuels (2) |
| Moved in from another NSE sector | 2 |
| Median intensity, climate | 110 tCO2e/₹ cr (n = 10) |
| Median intensity, energy | 1,074 GJ/₹ cr (n = 11) |
| Median intensity, water | 633 kL/₹ cr (n = 10) |
| Median intensity, pollution (shown, not scored) | 335 t/₹ cr (n = 9) |
| Highest-ranked without caution | NMDC Ltd (rank 1, score 89.3) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.93 / 0.95 |
| Illustrative nature cost, median | 30.4% of EBITDA (n = 10) |

**Not ranked (4):** Coal India Limited (held back); Jain Resource Recycling Limited (held back); BHARAT COKING COAL LIMITED (not reported); Vedanta Aluminium Metal Limited (revenue mismatch).
:::

## Financial Services: Insurance underwriting

::: {.profile}
[9 of 12 members ranked on climate, energy, water, pollution. Climate intensity spans 22× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 12 / 9 / 0 |
| Drawn from NSE sectors | Financial Services (12) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 0.195 tCO2e/₹ cr (n = 11) |
| Median intensity, energy | 0.925 GJ/₹ cr (n = 12) |
| Median intensity, water | 3.63 kL/₹ cr (n = 12) |
| Median intensity, pollution | 0.00058 t/₹ cr (n = 10) |
| Highest-ranked without caution | ICICI Prudential Life Insurance Company Limited (rank 1, score 78.8) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.98 / 0.95 |
| Illustrative nature cost, median | 0.03% of revenue (n = 11) |

**Not ranked (3):** Canara HSBC Life Insurance Company Limited (held back); General Insurance Corporation of India (zero to confirm); The New India Assurance Company Limited (zero to confirm).
:::

## Real estate

::: {.profile}
[9 of 12 members ranked on climate, energy, water. Climate intensity spans 25× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 12 / 9 / 0 |
| Drawn from NSE sectors | Realty (11); Media Entertainment & Publication (1) |
| Moved in from another NSE sector | 1 |
| Median intensity, climate | 5.93 tCO2e/₹ cr (n = 9) |
| Median intensity, energy | 30.7 GJ/₹ cr (n = 11) |
| Median intensity, water | 101 kL/₹ cr (n = 11) |
| Median intensity, pollution (shown, not scored) | 0.513 t/₹ cr (n = 10) |
| Highest-ranked without caution | Anant Raj Limited (rank 1, score 85.8) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.87 / 0.93 |
| Illustrative nature cost, median | 2.2% of EBITDA (n = 10) |

**Not ranked (3):** ADITYA BIRLA REAL ESTATE LIMITED (held back); Prime Focus Limited (held back); Lodha Developers Limited (zero to confirm).
:::

## Healthcare: hospitals and diagnostics

::: {.profile}
[9 of 10 members ranked on climate, energy, water, pollution. Climate intensity spans 3× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 10 / 9 / 0 |
| Drawn from NSE sectors | Healthcare (10) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 8.84 tCO2e/₹ cr (n = 9) |
| Median intensity, energy | 44.0 GJ/₹ cr (n = 9) |
| Median intensity, water | 136 kL/₹ cr (n = 9) |
| Median intensity, pollution | 0.313 t/₹ cr (n = 9) |
| Highest-ranked without caution | Dr. Lal Pathlabs Limited (rank 1, score 84.4) |
| Ranked with a naming caution | 1 |
| Rank correlation: net vs gross / min leave-one-out | 0.87 / 0.90 |
| Illustrative nature cost, median | 4.3% of EBITDA (n = 9) |

**Not ranked (1):** Dr. Agarwal's Health Care Limited (not reported).
:::

## Transport and logistics

::: {.profile}
[8 of 10 members ranked on climate, energy, water, pollution. Climate intensity spans 86× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 10 / 8 / 0 |
| Drawn from NSE sectors | Services (9); Oil Gas & Consumable Fuels (1) |
| Moved in from another NSE sector | 1 |
| Median intensity, climate | 23.3 tCO2e/₹ cr (n = 9) |
| Median intensity, energy | 323 GJ/₹ cr (n = 9) |
| Median intensity, water | 39.3 kL/₹ cr (n = 9) |
| Median intensity, pollution | 0.025 t/₹ cr (n = 8) |
| Highest-ranked without caution | GMR Airports Limited (rank 1, score 78.1) |
| Ranked with a naming caution | 0 |
| Rank correlation: net vs gross / min leave-one-out | 0.90 / 0.81 |
| Illustrative nature cost, median | 14.6% of EBITDA (n = 9) |

**Not ranked (2):** Container Corporation Of India Ltd. (held back); AEGIS VOPAK TERMINALS LIMITED (not reported).
:::

## Telecom and media

::: {.profile}
[Not ranked: 8 members, fewer than 8 of them with complete, clean data. Climate intensity spans 667× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 8 / 0 / 0 |
| Drawn from NSE sectors | Telecommunication (5); Consumer Services (2); Media Entertainment & Publication (1) |
| Moved in from another NSE sector | 3 |
| Median intensity, climate | 2.46 tCO2e/₹ cr (n = 7) |
| Median intensity, energy | 14.0 GJ/₹ cr (n = 8) |
| Median intensity, water | 4.80 kL/₹ cr (n = 8) |
| Median intensity, pollution | 0.00065 t/₹ cr (n = 8) |
| Illustrative nature cost, median | 0.52% of EBITDA (n = 8) |

**Not ranked (8):** Bharti Airtel Ltd. (group too small); Bharti Hexacom Limited (group too small); INDUS TOWERS LIMITED (group too small); Info Edge(India) Ltd. (group too small); SUN TV NETWORK LIMITED (group too small); Tata Communications Limited (group too small); VODAFONE IDEA LIMITED (group too small); IndiaMART InterMESH Limited (zero to confirm).
:::

## Textiles and apparel

::: {.profile}
[Not ranked: 7 members, below the minimum of 8. Climate intensity spans 55× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 7 / 0 / 0 |
| Drawn from NSE sectors | Textiles (5); Construction Materials (1); Chemicals (1) |
| Moved in from another NSE sector | 2 |
| Median intensity, climate | 105 tCO2e/₹ cr (n = 7) |
| Median intensity, energy | 648 GJ/₹ cr (n = 7) |
| Median intensity, water | 273 kL/₹ cr (n = 7) |
| Median intensity, pollution | 1.53 t/₹ cr (n = 7) |
| Illustrative nature cost, median | 42.4% of EBITDA (n = 7) |

**Not ranked (7):** Grasim Industries Ltd (group too small); K.P.R. Mill Ltd. (group too small); Page Industries Ltd. (group too small); Swan Corp Limited (group too small); Trident Ltd (group too small); Vardhman Textiles Limted (group too small); WELSPUN LIVING LIMITED (group too small).
:::

## Financial Services: Investment and holding companies

::: {.profile}
[Not ranked: 6 members, below the minimum of 8.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 6 / 0 / 0 |
| Drawn from NSE sectors | Financial Services (6) |
| Moved in from another NSE sector | 0 |
| Median intensity, climate | 0.048 tCO2e/₹ cr (n = 1) |
| Median intensity, energy | 0.492 GJ/₹ cr (n = 3) |
| Median intensity, water | 1.07 kL/₹ cr (n = 2) |
| Median intensity, pollution | 0.0029 t/₹ cr (n = 2) |

**Not ranked (6):** Bajaj Holdings & Investment Limited (group too small); JSW Holdings Limited (group too small); Jio Financial Services Limited (group too small); Maharashtra Scooters Ltd. (group too small); TVS Holdings Limited (group too small); Tata Investment Corporation Ltd. (group too small).
:::

## Building products

::: {.profile}
[Not ranked: 4 members, below the minimum of 8. Climate intensity spans 7× across members with a usable value.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 4 / 0 / 0 |
| Drawn from NSE sectors | Capital Goods (2); Consumer Durables (2) |
| Moved in from another NSE sector | 4 |
| Median intensity, climate | 26.4 tCO2e/₹ cr (n = 4) |
| Median intensity, energy | 154 GJ/₹ cr (n = 4) |
| Median intensity, water | 120 kL/₹ cr (n = 4) |
| Median intensity, pollution | 0.923 t/₹ cr (n = 4) |

**Not ranked (4):** ASTRAL LIMITED (group too small); Century Plyboards (India) Ltd. (group too small); Kajaria Ceramics Ltd (group too small); Supreme Industries Ltd. (group too small).
:::

## Diversified conglomerates

::: {.profile}
[Not ranked: 1 member, below the minimum of 8.]{.phead}

| Measure | Value |
|---|---|
| Members / ranked / air-ranked | 1 / 0 / 0 |
| Drawn from NSE sectors | Metals & Mining (1) |
| Moved in from another NSE sector | 1 |
| Median intensity, climate | 11.3 tCO2e/₹ cr (n = 1) |
| Median intensity, energy | 92.0 GJ/₹ cr (n = 1) |
| Median intensity, water | 81.3 kL/₹ cr (n = 1) |
| Median intensity, pollution | 1.83 t/₹ cr (n = 1) |

**Not ranked (1):** Adani Enterprises Ltd. (group too small).
:::


# References

Alkemade, R., van Oorschot, M., Miles, L., Nellemann, C., Bakkenes, M. and ten Brink, B. (2009). GLOBIO3: a framework to investigate options for reducing global terrestrial biodiversity loss. *Ecosystems* 12(3), 374–390. https://doi.org/10.1007/s10021-009-9229-5

CEA, Central Electricity Authority (2025). *CO2 Baseline Database for the Indian Power Sector, User Guide, Version 21.0* (FY2024-25 weighted-average emission factor 0.710 tCO2/MWh). New Delhi: Ministry of Power. https://cea.nic.in/wp-content/uploads/baseline/2025/12/User_Guide_V_21.0.pdf

CEA, Central Electricity Authority (2026). *CO2 Baseline Database for the Indian Power Sector, User Guide, Version 22.0* (FY2025-26 factor 0.675 tCO2/MWh). https://cea.nic.in/wp-content/uploads/baseline/2026/09/User_Guide__Version_22.0.pdf

CE Delft (de Vries, J. et al.) (2024). *Environmental Prices Handbook 2024, EU27 version 1.1*. Delft: CE Delft. https://cedelft.eu/wp-content/uploads/sites/2/2024/12/CE_Delft_230107_Environmental-Prices-Handbook-2024-EU-version_def_V1.1.pdf

GRI, Global Reporting Initiative (2024). *GRI 101: Biodiversity 2024* (effective for reports published on or after 1 January 2026). Amsterdam: GSSB. https://www.globalreporting.org/pdf.ashx?id=24534

IFVI and VBA (2026). *Environmental Methodology 2: Water Consumption*. International Foundation for Valuing Impacts and Value Balancing Alliance. https://ifvi.org/wp-content/uploads/2026/03/IFVI_VBA_Environmental_Methodology-2_Water-Consumption_FIN_04.pdf

IFVI (2024). *Global Value Factor Database*, version 1 (exposure draft, 15 October 2024), interim air and waste methodologies. International Foundation for Valuing Impacts. https://ifvi.org/methodology/environmental-topic-methodology/interim-methodologies/ (read via a CC-BY mirror, as documented in `PRICES_V12.md`)

IPBES (2019). *Summary for policymakers of the global assessment report on biodiversity and ecosystem services* (Díaz, S., Settele, J., Brondízio, E.S., Ngo, H.T. et al., eds). Bonn: IPBES secretariat. https://www.ipbes.net/sites/default/files/2020-02/ipbes_global_assessment_report_summary_for_policymakers_en.pdf

ISSB, International Sustainability Standards Board (2023). *IFRS S2 Climate-related Disclosures*. London: IFRS Foundation. https://www.ifrs.org/issued-standards/ifrs-sustainability-standards-navigator/ifrs-s2-climate-related-disclosures

IUCN (2016). *A Global Standard for the Identification of Key Biodiversity Areas, Version 1.0*. Gland: IUCN. https://portals.iucn.org/library/sites/library/files/documents/2016-048.pdf

Kumar, S. (2006). Analysing industrial water demand in India: an input distance function approach. *Water Policy* 8(1), 15–29. https://doi.org/10.2166/wp.2006.0002

Kuzma, S., Bierkens, M.F.P., Lakshman, S., Luo, T., Saccoccia, L., Sutanudjaja, E.H. and Van Beek, R. (2023). *Aqueduct 4.0: Updated decision-relevant global water risk indicators*. Technical Note. Washington, DC: World Resources Institute. https://doi.org/10.46830/writn.23.00061

MOSPI, Central Statistical Organisation (2008). *National Industrial Classification (All Economic Activities) 2008*. New Delhi: Ministry of Statistics and Programme Implementation. https://www.mospi.gov.in/sites/default/files/main_menu/national_industrial_classification/nic_2008_17apr09.pdf

OECD and JRC (Nardo, M., Saisana, M., Saltelli, A., Tarantola, S., Hoffmann, A. and Giovannini, E.) (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. Paris: OECD Publishing. https://doi.org/10.1787/9789264043466-en

Rennert, K., Errickson, F., Prest, B.C., Rennels, L., Newell, R.G., Pizer, W. et al. (2022). Comprehensive evidence implies a higher social cost of CO2. *Nature* 610, 687–692. https://doi.org/10.1038/s41586-022-05224-9

Ricke, K., Drouet, L., Caldeira, K. and Tavoni, M. (2018). Country-level social cost of carbon. *Nature Climate Change* 8, 895–900. https://doi.org/10.1038/s41558-018-0282-y

Saisana, M., Saltelli, A. and Tarantola, S. (2005). Uncertainty and sensitivity analysis techniques as tools for the quality assessment of composite indicators. *Journal of the Royal Statistical Society: Series A* 168(2), 307–323. https://doi.org/10.1111/j.1467-985X.2005.00350.x

Schipper, A.M., Hilbers, J.P., Meijer, J.R., Antão, L.H., Benítez-López, A., de Jonge, M.M.J. et al. (2020). Projecting terrestrial biodiversity intactness with GLOBIO 4. *Global Change Biology* 26(2), 760–771. https://doi.org/10.1111/gcb.14848

SEBI, Securities and Exchange Board of India (2021). *Business responsibility and sustainability reporting by listed entities*. Circular SEBI/HO/CFD/CMD-2/P/CIR/2021/562, 10 May 2021. https://www.sebi.gov.in/legal/circulars/may-2021/business-responsibility-and-sustainability-reporting-by-listed-entities_50096.html

SEBI (2023). *BRSR Core: Framework for assurance and ESG disclosures for value chain*. Circular SEBI/HO/CFD/CFD-SEC-2/P/CIR/2023/122, 12 July 2023. https://www.sebi.gov.in/legal/circulars/jul-2023/brsr-core-framework-for-assurance-and-esg-disclosures-for-value-chain_73854.html

Sotos, M. (2015). *GHG Protocol Scope 2 Guidance: An amendment to the GHG Protocol Corporate Standard*. Washington, DC: World Resources Institute. https://ghgprotocol.org/scope-2-guidance

Spearman, C. (1904). The proof and measurement of association between two things. *American Journal of Psychology* 15(1), 72–101. https://doi.org/10.2307/1412159

Thaller, A. et al. (2026). Country social cost of carbon estimates and their application to assess the natural land sink. Kiel Working Paper 2316. Kiel Institute for the World Economy (working paper, as cited in `PRICES_V12.md`).

TNFD, Taskforce on Nature-related Financial Disclosures (2023). *Recommendations of the Taskforce on Nature-related Financial Disclosures*, September 2023. https://tnfd.global/wp-content/uploads/2023/08/Recommendations_of_the_Taskforce_on_Nature-related_Financial_Disclosures_September_2023.pdf

TNFD (2026). *Recommendations of the Taskforce on Nature-related Financial Disclosures*, October 2026, Annex 1: core global disclosure metrics. https://tnfd.global/wp-content/uploads/2026/10/Recommendations-of-the-TNFD_October-2026_DIGITAL.pdf

Tol, R.S.J. (2019). A social cost of carbon for (almost) every country. *Energy Economics* 83, 555–566. https://doi.org/10.1016/j.eneco.2019.07.006

Tripathi, Gupta, Krishna and Gandhi (2026). *Business responsibility and sustainability in India: a comprehensive analysis of BRSR disclosures of India's top 1,000 listed companies for FY 2024–25*. Monograph. Bengaluru: Indian Institute of Management Bangalore. https://research.iimb.ac.in/cgi/viewcontent.cgi?article=1149&context=monographs

UNEP-WCMC and IUCN (2026). *Protected Planet: The World Database on Protected and Conserved Areas (WDPCA)*, October 2026. Cambridge, UK: UNEP-WCMC and IUCN. https://www.protectedplanet.net

US EPA (2023). *Report on the Social Cost of Greenhouse Gases: Estimates Incorporating Recent Scientific Advances*. Washington, DC: US Environmental Protection Agency. https://www.epa.gov/system/files/documents/2023-12/epa_scghg_2023_report_final.pdf

WRI and WBCSD (2004). *The Greenhouse Gas Protocol: A Corporate Accounting and Reporting Standard*, revised edition. Washington, DC and Geneva. https://ghgprotocol.org/sites/default/files/standards/ghg-protocol-revised.pdf

*Prices in Table 11.1 also rest on further sources listed and verified in `insights/prices/PRICES_V12.md` (Bierkens et al. 2019; Huijbregts et al. 2017; Rabl et al. 2008; Dijkgraaf and Vollebergh 2004; COWI 2000; Nahman 2011; Jardosh and Kathuria 2025).*

# Appendix A. Glossary

| Term | Meaning in this paper |
|---|---|
| AMFI | Association of Mutual Funds in India; publishes the six-monthly market-capitalisation list that defines the universe |
| BRSR | Business Responsibility and Sustainability Report, filed annually by India's top 1,000 listed companies under SEBI (2021) |
| BRSR Core | The subset of BRSR indicators subject to assurance (SEBI 2023) |
| Boundary | Whether a BRSR covers the listed company alone (standalone) or its group (consolidated) |
| Confidence tier | How a value reached the dataset (Table 3.2), recorded as `source_status` |
| Gross figure | The pressure before offsets: total energy, water withdrawn, waste generated |
| Held back | A reported value not scored until the company confirms it (Section 6) |
| Intensity | A net pressure divided by revenue from operations in ₹ crore |
| kL | Kilolitre, equal to one cubic metre |
| MSA | Mean species abundance: mean abundance of original species relative to an undisturbed state (GLOBIO) |
| Naming caution | A flag that a ranked company should not be singled out by name until a value or its business model is checked |
| Net figure | The pressure after the matching offset: non-renewable energy, water consumed, waste not recovered |
| NIC 2008 | India's National Industrial Classification, used in BRSR product lines |
| Peer group | The set of companies with the same kind of main business within which ranks are computed |
| Percentile score | 100 × (k − position) ÷ (k − 1), Section 7.2 |
| Pressure | A reported quantity of a direct driver of nature loss |
| Scope 1, 2, 3 | Direct emissions; emissions from purchased electricity, heat and steam; all other value-chain emissions (GHG Protocol) |
| SCC | Social cost of carbon: the monetised damage of one more tonne of CO2 |
| tCO2e | Tonnes of carbon-dioxide equivalent |
| XBRL | The machine-readable filing format in which the BRSR is filed with NSE |
| ₹ crore | Ten million rupees |

# Appendix B. Parameter table

All parameters are in `P` in `build_clbi.py` and in `build_stats.json` → `params`.

| Parameter | Value | Used in | Rationale |
|---|---|---|---|
| `min_sector_size` | 8 | Section 5 | Smallest group in which a within-group position is informative; lowered from 10 in v1.1 |
| `min_element_reporters` | 6 | Section 7.2 | A pressure is scored only if enough peers report it |
| `min_ranked_to_publish` | 8 | Section 7.4 | Ranks published only with 8 complete, clean companies |
| `core_elements` | climate, energy, water, waste | Section 4 | The four scored pressures; all required |
| `supplementary_elements` | air | Section 9 | Ranked separately |
| `pollution_not_comparable` | Power; Metals: non-ferrous and mining; Construction and engineering; Real estate | V9 | Largest waste streams reported inconsistently |
| `scope1_fuel_max_t_per_gj` | 0.12 tCO2/GJ | V12 | Fuel combustion emits at most about 0.1 t per GJ |
| `process_emission_groups` | Cement; Metals: steel and iron products; Metals: non-ferrous and mining; Chemicals: commodity chemicals and fertilisers; Oil, gas and fuels | V12 | Groups where process emissions are expected, exempt from V12 |
| `exclude_reported_zero` | climate, air | V1 | Zero totals treated as "to confirm" |
| `extreme_ratio` | 300 | V3, V5, V13 | Separates unit or boundary errors from genuine variation |
| `scope2_grid_ef` | 0.71 tCO2/MWh | V4, V5 | CEA FY2024-25 weighted-average grid factor |
| `scope2_tariff_inr_per_kwh` | ₹6.0 | V4 | Conservative grid tariff for the bill test |
| `scope2_energy_ratio_max` | 1.5 | V5 | Margin for grid-factor differences |
| `scope2_zero_re_min` | 0.90 | V2 | Renewable share consistent with a market-based zero |
| `assumed_consumption_share` | 0.20 (tolerance 0.0005) | V7 | Detects an assumed 80% discharge |
| (in code) water cap band | 1.05× to 10× withdrawal | V6 | Consumption above withdrawal counts recycled water |
| (in code) water hold | > 10× withdrawal | V6 | Likely unit error |
| (in code) waste hold | recovered > 1.5× generated | V8 | Inconsistent table or stock movement |
| (in code) energy hold | non-renewable > 1.01× total | V10 | Inconsistent table |
| (in code) naming-caution band | 100× to 300× from peer median | V13 | Unusual but inside the hold-back line |
| `thin_profit_margin` | 0.02 | Section 9 | Profit-basis ratio unstable below a 2% margin |
| (in code) EBITDA thin margin | EBITDA < 5% of revenue | Section 11 | % of EBITDA flagged as unstable |
| `credit_*` | 0 | – | v1.1 capped credit retired; offsets now act on the same pressure |
| `credit_a_min_ha` | 10 ha | – | Retained for the retired credit; not used |
| Ranking rounding | 6 decimal places | Section 7.4 | Prevents floating-point noise from splitting ties |

# Appendix C. Peer groups: companies, ranked and not ranked

Counts from `CLBI_v1_exclusion_summary.csv`. The columns after "Not ranked" give the category of each company we do not rank (Section 8).

| Peer group | Companies | Ranked | Not ranked | Held back | Zero to confirm | Not reported | Revenue mismatch | Group too small |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Healthcare: pharmaceuticals | 40 | 40 | 0 | 0 | 0 | 0 | 0 | 0 |
| Financial Services: Lending NBFC and housing finance | 33 | 29 | 4 | 2 | 1 | 1 | 0 | 0 |
| Auto components and tyres | 29 | 27 | 2 | 0 | 0 | 0 | 2 | 0 |
| FMCG | 28 | 27 | 1 | 0 | 0 | 0 | 1 | 0 |
| Capital goods: machinery, engineering and defence | 31 | 25 | 6 | 3 | 1 | 1 | 1 | 0 |
| Financial Services: Banks | 27 | 25 | 2 | 2 | 0 | 0 | 0 | 0 |
| Capital goods: electrical equipment and electronics | 29 | 24 | 5 | 0 | 0 | 2 | 3 | 0 |
| IT services and software | 24 | 20 | 4 | 1 | 0 | 2 | 1 | 0 |
| Retail, e-commerce, hotels and consumer services | 27 | 19 | 8 | 2 | 2 | 3 | 1 | 0 |
| Chemicals: commodity chemicals and fertilisers | 18 | 17 | 1 | 0 | 1 | 0 | 0 | 0 |
| Chemicals: specialty, paints and coatings | 17 | 15 | 2 | 1 | 0 | 0 | 1 | 0 |
| Metals: steel and iron products | 17 | 15 | 2 | 2 | 0 | 0 | 0 | 0 |
| Power | 17 | 13 | 4 | 1 | 1 | 1 | 1 | 0 |
| Oil, gas and fuels | 15 | 13 | 2 | 1 | 0 | 1 | 0 | 0 |
| Financial Services: Capital markets and financial intermediaries | 18 | 12 | 6 | 2 | 3 | 0 | 1 | 0 |
| Automobiles | 14 | 12 | 2 | 1 | 0 | 1 | 0 | 0 |
| Construction and engineering | 13 | 12 | 1 | 0 | 0 | 1 | 0 | 0 |
| Cement | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 |
| Consumer durables | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 |
| Metals: non-ferrous and mining | 13 | 9 | 4 | 2 | 0 | 1 | 1 | 0 |
| Financial Services: Insurance underwriting | 12 | 9 | 3 | 1 | 2 | 0 | 0 | 0 |
| Real estate | 12 | 9 | 3 | 2 | 1 | 0 | 0 | 0 |
| Healthcare: hospitals and diagnostics | 10 | 9 | 1 | 0 | 0 | 1 | 0 | 0 |
| Transport and logistics | 10 | 8 | 2 | 1 | 0 | 1 | 0 | 0 |
| Telecom and media | 8 | 0 | 8 | 0 | 1 | 0 | 0 | 7 |
| Textiles and apparel | 7 | 0 | 7 | 0 | 0 | 0 | 0 | 7 |
| Financial Services: Investment and holding companies | 6 | 0 | 6 | 0 | 0 | 0 | 0 | 6 |
| Building products | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 4 |
| Diversified conglomerates | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| **Total** | **500** | **409** | **91** | **24** | **13** | **16** | **13** | **25** |


# Appendix D. Air-ranked and profit-ranked counts

Table 5.1 gives the counts in its "Air-ranked" and "Profit-ranked" columns: air ranks in 14 groups (178 companies) and profit ranks in 22 groups (378 companies).

# Appendix E. How we computed the less obvious numbers

All paths are relative to `/home/claude/CLBI_work_2026-10-24/`. "Scores file" means `outputs_v12/CLBI_v1_scores_all500.csv`.

- **409 ranked, 24 groups, 29 groups.** Count of non-missing `rank_rev`; number of distinct `score_group` among them; number of distinct `score_group` overall.
- **Boundary counts.** `brsr_reporting_boundary` in the scores file, all rows and rows with `rank_rev` present.
- **Confidence tiers (Table 3.2).** `CLBI_v1_company_data.csv`, rows for the nine core fields with `flag` "reported" or "reported_zero", cross-tabulated by `source_status`.
- **221 and 85 ranked companies on repaired values.** For ranked companies, the set of `source_status` values over their nine core fields; counted where the set is not only tier 1, and where it contains `GAPFILL_public_report`.
- **Coverage (Table 3.3).** Present: `{e}` not null; zero: `{e}_zero_flag`; held back: `{e}_query_flag` and not zero; revenue not matched: present, not zero, not held and `revenue_ok` false; usable: `{e}_per_rev` not null; scored: `{e}_score_rev` not null.
- **Scope 2 basis and Scope 3.** `scope2_basis.classification` and `metrics.scope3_tco2e.status` in `normalized_companies.json` (465 filings).
- **Implied Scope 2 factor (433; median 0.710; 286 at 0.71; 42 outside 0.5–1.0, 34 ranked).** Scope 2 (scores file) ÷ (XBRL `nonrenewable_electricity_gj` ÷ 3.6), for companies whose XBRL total energy is within 2% of the value finally used and with both terms positive (447 agree; 433 tested).
- **Offset statistics (59; 10.6%; 81.6%; 174; 41; 215).** Ranked companies: `renewable_energy_gj` ÷ `total_energy_gj` ≥ 0.5 and its median; `waste_recovered_tonnes` ÷ `waste_generated_tonnes`, median, ≥ 0.9, ≥ 1.0; `water` < `water_withdrawal_m3`.
- **Peer-group statistics (54 moves; 342; 95.3%; 361/128/11; 14).** `inputs/peer_groups_v12.csv`: `home_sector` ≠ `nse_sector`; `pg_source_url` containing "xbrl"; median of numeric `main_activity_share_pct`; `pg_confidence`; `conglomerate` = yes.
- **Rule V5 counts (7; 1; 3; 3).** Implied grid GJ > 1.5 × `total_energy_gj` (7); of which the bill rule already fires (1); of the remaining 6, those failing the credible-energy condition (3) and those held (3).
- **Rule V7 (30; 24).** `water_discharge_assumed` true; among ranked.
- **Naming caution (31; 12; 7; 10 flags; 14) and V12 (15; 14).** Ranked companies with non-empty `naming_caution`; with non-empty `business_model_flag` (from `peer_fit_notes.csv`); whose caution contains a "x above" or "x below peer median" flag, and the count of each pressure name in those flags; with `scope1_fuel_check` true (all companies: 15; ranked: 14).
- **Ties (30 in 6 groups).** Ranked companies whose `rank_rev` is shared with another company in the same group.
- **Percentile base wider than ranked set (climate 14, energy 15, water 14, pollution 9 groups).** For each pressure, groups where the count of non-missing `{e}_score_rev` exceeds the number ranked.
- **Second view of the 91 (Section 8).** Each company assigned to the first failed stage in the order: no XBRL file and incomplete; required pressure missing; revenue; open query; zero; group or sector size; incomplete group; ranked. The XBRL list is the 465 symbols in `normalized_companies.json`.
- **Nature-cost shares and medians (Section 11).** Shares: sum of `cost_ghg`, `cost_energy`, `cost_water`, `cost_waste`, `cost_air` over the 465 companies with `nature_cost_central` present, each divided by the sum of all five; for lens A the water cost is scaled by 39.6/358 and for lens C the air cost is recomputed at ₹10.2, 3.4 and 15.9 lakh per tonne of SOx, NOx and PM. Medians of `nature_cost_pct_ebitda` (and `_lens_A`, `_lens_C`) over the 370 non-null rows; medians of `nature_cost_pct_revenue` (460 rows) and of each lens total divided by revenue. Median of `share_ghg`; largest component per row of the `share_*` columns; counts above 100%. The one-convention price check and its set B comparison row are in `insights/prices/convention_check.csv`.
- **Land categories (Table 10.1).** `land_category` in `CLBI_v1_land_evidence.csv`, after `inputs/land_category_overrides.csv` is applied by `land_evidence_v12.py`.
- **Lineage (5,949 values; 0 without URL).** Rows of `CLBI_v1_company_data.csv` with `flag` "reported" or "reported_zero", counting empty `source_url`.
- **Waste figures in V9.** `waste_generated_tonnes` and `waste_recovered_tonnes` in the scores file; Coal India's share is its generated tonnes divided by the sum over all 500 (5,854,650,379 t).
- **Robustness.** Medians and minima of the three correlation columns of `CLBI_v1_robustness.csv` over its 24 rows (insurance has no profit correlation).

# Appendix F. Review and response

An independent review of data and method (Fable, 28 October 2026; `reviews/FABLE_V12_DATA_METHOD.md`) reproduced every rank and element score of the earlier build from the gross inputs and checked the nature-cost totals. The table lists its HIGH and MEDIUM findings and our response.

| Finding | What the reviewer found | Our response in this build |
|---|---|---|
| H1 Scope 1 contradicts fuel data | Scope 1 above what the reported fuel could emit, including three companies whose zero Scope 2 was accepted (BEL, POWERINDIA, CUPID) | We added check V12: Scope 1 above 0.12 t per GJ of non-renewable energy, outside process-emission groups and against a usable energy figure, triggers a naming caution (15 companies, 14 ranked). V12 cautions and does not hold. **Open:** whether V12 should hold the value, and whether a zero Scope 2 should be accepted only when V12 passes |
| H2 Price set B not on one convention | Water ₹358/kL is a PPP-converted, global-perspective IFVI value, while carbon is converted at market exchange rates; BRSR consumption can include seawater | **Resolved.** We kept set B (decision of 28 October). A recomputation with every price from one standard (IFVI and CE Delft), converted by one convention, gives the same mix by PPP or by market exchange rate (carbon 71.6–71.9%, water 15.0–15.1%), so the conclusions hold under either convention (Section 11). We now remove seawater inside reported consumption from priced water for 7 companies, read from each company's BRSR; we leave six unclear cases unadjusted and name them. |
| H3 Leaders that will be challenged; false cautions | Jewellers ranked among appliance makers; UPL's standalone boundary; drug makers with very low Scope 1; a delivery platform among hotels; NIC rule labelled refiners as traders | We retired the NIC-based caution. Cautions now come from reviewed notes on main activity (`peer_fit_notes.csv`, 13 companies, 12 of them ranked), V12 and the 100–300× value flags; 31 ranked companies carry one. Peer profiles name a company if it has no caution. **Open:** CESC (distribution utility among generators) and GRAVITA (lead recycler among miners) carry no reviewed note |
| M1 Pollution scored in real estate | Construction debris decides the top of real estate (Oberoi Realty net 0.007 t on 333,517 t generated) | We added real estate to the groups where we do not score pollution (rule V9). Real estate now ranks 9 companies on climate, energy and water |
| M2 Exact-20% water rule | The rule changes leaders and catches only a ratio of exactly 0.20; other round ratios are not caught and no filing has been read for "assumed" | **Kept** (decision of 28 October). We disclose its narrow reach in V7 and list it as a limitation in Section 13 |
| M3 % of EBITDA fragile at company level | Values of several hundred per cent, partly driven by flagged inputs; thin margins | We present the EBITDA share as peer-group medians with IQR, show company values with their flags and low–high range, and flag margins below 5% (8 companies). We did not adopt "years of EBITDA" for values above 100% |
| M4 Lineage gaps | Seven ranked companies without a source URL on scored values; some gap-fill rows without a page; unit-converted quotes; PRIVISCL consumption still in litres | Every reported value now carries a source URL (5,949 of 5,949). **Open:** 41 gap-fill rows still lack a page; PRIVISCL's water remains held; quotes in other units remain labelled "quoted verbatim" |
| M5 Land categories regex-driven | Single sites, a land-acquisition claim, leases, an allotment and land banks were in the top category | We classified the 28 top-category rows by hand (Table 10.1): A 13, R 6, B 7, with 2 moved to C. We corrected BEL and BHEL to totals |
