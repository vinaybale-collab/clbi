# Corporate Land and Biodiversity Index (CLBI) v1.1: how it works

**Draft for Landstack · Urvara.Life · 27 October 2026 · For discussion, not for publication**

Website, with every company and every value: **vinaybale-collab.github.io/clbi**

## 1. In one paragraph

CLBI compares India's 500 largest listed companies with others **in the same sector**. It asks one question: *how much pressure on nature does each company report, for every rupee it earns?* It looks at three pressures, greenhouse gases, water and waste, all for the year April 2025 to March 2026. Each value comes from what the company itself has published, and each one can be traced to its page and source. The maths is simple enough to check by hand.

**What a rank means.** Rank 1 means that, among its sector peers, the company reported the lowest pressure per rupee of revenue. It does *not* mean the company's footprint is small in absolute terms, or that it is good for biodiversity.

**What CLBI is not:**

- a measure of biodiversity impact or of nature-related risk;
- an ESG rating;
- a ranking across sectors (a cement maker is never compared with a bank);
- a judgement that any company has done something wrong.

## 2. Principles

1. **Company data only.** Ranks use only what companies themselves report. Nothing estimated or modelled enters a rank, and a blank stays blank. The land ratios and prices in the pilot and annex are clearly labelled as research-based.
2. **Every number traceable.** Each value carries its source link, page or filing field, and confidence tier. Values from reports also carry the exact words quoted from the report.
3. **Compare like with like.** Companies are compared only within their sector, and only where at least 10 companies have complete data.
4. **Simple, open maths.** Anyone with the same data can reproduce every score. The dataset recomputes them with spreadsheet formulas.
5. **Doubtful values are held back.** A value that looks wrong is not scored until the company confirms it, even if it is printed in the filing.
6. **Credit is small and never offsets pressure.** Restoration, recycling and renewable electricity earn a few points; they do not cancel emissions or water use.

## 3. Which companies

The universe is the **500 NSE-listed companies with the highest average market capitalisation** over January–June 2026, as published by AMFI. REITs, InvITs and trusts are excluded.

Companies are grouped by the **NSE's own 22-sector classification**. Financial Services is split into sub-groups (banks, lenders, capital-market firms), because these businesses are too different to compare with each other.

A group is ranked only if **at least 10 of its companies** have complete data. This gives **373 ranked companies in 16 groups**. The breakdown is below.

| Peer group | Companies | Ranked | Also ranked on air |
|---------------------------------------|------------:|----------:|------------:|
| Capital Goods | 68 | 55 | 26 |
| Healthcare | 51 | 50 | 31 |
| Automobile & Auto Components | 39 | 35 | 24 |
| Fast Moving Consumer Goods | 30 | 26 | 23 |
| Chemicals | 27 | 26 | 21 |
| Consumer Services | 26 | 18 | 10 |
| Information Technology | 20 | 18 | 11 |
| Metals & Mining | 20 | 17 | 12 |
| Consumer Durables | 19 | 18 | – |
| Oil, Gas & Consumable Fuels | 19 | 14 | – |
| Power | 18 | 13 | – |
| Construction Materials (cement) | 11 | 11 | 11 |
| Services | 14 | 10 | – |
| *Financial Services, separate:* banks · lenders · capital markets | 27 · 32 · 16 | 25 · 26 · 11 | – |
| Scores shown, too few complete for a rank: Construction, Realty, insurers | 33 | – | – |
| Listed only (fewer than 10 companies): Telecom, Textiles, Diversified, Media, holding companies, others | 30 | – | – |
| **Total** | **500** | **373** | **169** |

**Financial Services** is shown on a separate sheet with a warning. A bank's own footprint is its offices and data centres. Its real effect on nature comes through what it lends to and invests in, and companies do not report that.

## 4. What is measured

| Pressure | What companies report (BRSR, Principle 6) | Unit | Companies with a value |
|--------------|------------------------------|-----------|----------:|
| Climate | Scope 1 + Scope 2 greenhouse-gas emissions | tonnes CO2e | 473 |
| Water | Total water withdrawal | kilolitres | 474 |
| Waste | Total waste generated | tonnes | 473 |
| Air (separate rank) | NOx + SOx + particulate matter | tonnes | 245 |

The main source is the **Business Responsibility and Sustainability Report (BRSR)** that every listed company files with the stock exchange. Revenue comes from the company's annual financial filing with NSE, on the same basis as its BRSR (standalone or consolidated). Scope 2 is taken **as reported** by every company.

**Where the 1,897 core values recorded for the 500 companies come from** (1,592 of them enter a rank):

| Tier | Source | Share |
|-------|-------------------------------------------|-------:|
| 1 | The BRSR data file filed with NSE, with the unit stated | 70.2% |
| 2 | The same file, with the unit checked against the BRSR PDF | 17.2% |
| 3 | The company's annual or sustainability report, or the BRSR PDF, used where the data file was blank. The exact words are recorded. An independent recheck of 40 of these values matched 38 exactly. | 10.2% |
| 4 | The data file, where the unit label "MtCO2e" was read as metric tonnes (the unit the BRSR form prescribes). Where the PDF could be checked, it agreed 96% of the time. | 2.2% |
| 5 | A filed value corrected to the company's own published figure (unit slips only) | 0.2% |

**Values held back.** These are listed in the dataset, and that element is not scored until the company confirms it:

- **Extreme values:** more than 300 times above or below the peer-group median, per rupee of revenue. These are usually unit slips (kilograms entered as tonnes) or boundary problems (head office only). There are 29 such values. A company with an open query on climate, water or waste is not ranked until it is resolved.
- **Impossible values:** a Scope 2 figure that would need more grid electricity than the company's whole revenue could buy (2 values).
- **Reported zeros:** a reported zero, including a zero for Scope 1 or Scope 2 alone. For an operating company, zero usually means "not measured" rather than "none".

## 5. How a score is worked out

1. **Divide by revenue.** For each pressure, divide the reported amount by revenue in ₹ crore. This gives the *intensity*.
2. **Compare with peers.** Within the peer group, line up the companies that report that pressure, from lowest to highest intensity. The lowest scores 100, the highest scores 0, and the rest are spaced evenly in between.

   > score = 100 × (number of companies − position) ÷ (number of companies − 1)
3. **Average the three.** The pressure score is the simple average of the climate, water and waste scores. **All three are required**, so leaving something out can never help a company.
4. **Add credit** (section 6): up to 10 points, with the total capped at 100.
5. **Rank** within the peer group.

**Worked example: ACC (cement, 11 companies ranked).**

- **Inputs.** Revenue is ₹25,766 crore. Emissions are 15,293,369 tonnes CO2e, so the intensity is 593.5 tonnes per ₹ crore.
- **Climate.** This is the 3rd lowest of 11 companies, so the climate score is 100 × (11 − 3) ÷ 10 = **80**.
- **Water.** Also 3rd lowest of 11, so the water score is **80**.
- **Waste.** 6th lowest, so the waste score is **50**.
- **Pressure score.** (80 + 80 + 50) ÷ 3 = **70.0**.
- **Credit.** ACC earns +5.6:
  - +2 for tree planting;
  - +3.0 because it recovers all its waste;
  - +0.6 for a 28% renewable electricity share.
- **Result.** Final score **75.6, rank 2 of 11**. The credit does not change its place.
- **Other views.** ACC is also 3rd per tonne of cement and 3rd on air pollution.

## 6. Credit for positive action (up to 10 points)

| Credit | Rule | Points | Companies |
|--------------|---------------------------------|-------:|------------:|
| Restoration, Tier A | At least 10 ha restored, afforested or conserved, stated as an area | +5 | 6 |
| Restoration, Tier B | Other measured restoration: tree planting, water bodies, smaller areas | +2 | 75 |
| Recycling | 3 × share of waste recovered | 0–3 | 416 |
| Renewable electricity | 2 × renewable share of electricity | 0–2 | 410 |

The following earn **no** restoration credit:

- plans and promises;
- unfinished work;
- farm or sourcing programmes;
- statements without a number;
- compensatory afforestation required by law for forest a company has cleared.

Credit is deliberately small:

- The largest effect is 5 places, in Capital Goods and Healthcare.
- In 13 of 16 ranked groups, no company gains more than 2 places.
- Rank order with and without credit is almost identical in every group (rank correlation 0.98 or higher).

Most manufacturers recover most of their waste, so the recycling credit varies little between them. Credit does not measure whether restoration has actually worked.

## 7. Physical output for cement and power

Revenue is a fair yardstick across most sectors, but it favours expensive products. For cement and power, a physical yardstick was also tested: tonnes of cement and megawatt-hours generated. These are reported on a matching basis by nearly all peers and are used in international reporting standards (SASB/ISSB).

- **Cement:** all 10 pure cement companies have production data. Their per-tonne ranks are shown alongside the revenue rank, and the two agree closely (rank correlation 0.92). Grasim is left out of this view because its standalone business is mainly fibres and chemicals.
- **Power:** generation figures were found for 10 generators. One of them (CESC) has a value held back (section 4), which leaves 9, below the 10 needed for a rank. The per-MWh intensities are shown, but not ranked. Transmission and distribution companies have no generation figure.

No other sector has an output measure that companies report consistently enough. Steel, for example, mixes crude steel, sponge iron, ferro-alloys and mining. Those sectors stay on revenue.

## 8. Other views (not part of the main rank)

**Air pollution.** Companies that report the total tonnes of NOx, SOx and dust are ranked on air within their group where at least 10 report it: **169 companies in 9 groups**. Many companies report only how concentrated pollution is at the chimney, which cannot be turned into tonnes.

**Per rupee of profit.** As a check, each company is also scored per rupee of profit after tax (350 companies). Loss-making companies are left out. Revenue-based and profit-based ranks broadly agree (median rank correlation 0.79). They agree less in service sectors, where profit margins vary widely.

**Land and biodiversity: a pilot.**

> net degraded hectares = land held (owned + leased, including mining leases) × how much nature that kind of land typically loses − land restored by the company on its own sites

The "how much nature is lost" ratio comes from three independent scientific approaches (GLOBIO, PREDICTS and life-cycle land-use factors). It ranges from about 0.60 for most sectors to 0.75 for mining. Restored land is subtracted hectare for hectare, which assumes full recovery; this is a simplification.

- **Coverage.** Companies do not report land area in their BRSR: we checked all 465 filings. So land was searched by hand for 106 companies in land-heavy sectors, in annual reports, mining-lease tables and environmental-clearance papers. A credible company-wide total was found for **19 companies** (14 of the 106, plus 5 found earlier). Most companies give land only as a rupee book value, or for single plants.
- **No rank.** No group has 10 companies with land data, so this is a **pilot, not a ranking**.
- **Legacy figures.** Land figures from Urvara's earlier Nature Impact Index are shown separately for reference only. Where both exist, they are typically 2.5 times the verified figure.
- **The fix is one disclosure.** If companies reported *total land owned and leased, in hectares, including mining leases*, this method could rank every company.

## 9. Limits to keep in mind

- **Pressure, not impact.** CLBI measures what drives biodiversity loss, not biodiversity itself.
- **Own operations only.** Supply chains, the use of products and lending or investment are excluded.
- **Self-reported.** Values are taken as published. Many are independently assured under BRSR Core, but CLBI does not audit them.
- **Mixed businesses.** NSE sectors put different businesses together: thermal plants with hydro and transmission, drug makers with hospitals. The dataset flags companies whose main activity does not match their sector, for example Aditya Birla Real Estate's paper business, or companies that mostly trade.
- **Check before naming.** 32 ranked companies carry a "check before naming" flag. Either their business is not like-for-like with their peers, or one of their scored climate, water or waste values is 100–300 times from the peer median: inside the hold-back line, but unusual. Their rank stands, but they should not be singled out, for example as a sector leader, until the value is checked with the company.
- **Standalone and consolidated mixed.** 286 ranked companies report their BRSR on a standalone basis and 86 on a consolidated basis, sometimes within the same peer group (1 does not state its basis). Revenue always matches the company's own BRSR basis.
- **Weights and water.** The three pressures are weighted equally. Water is withdrawal, which penalises plants cooled with seawater. Using water consumption instead changes ranks very little: rank correlation is 0.90 or higher in every group except banks (0.80).
- **Six ranked companies carry a revenue note.** Examples are discontinued operations, or an unstated BRSR boundary. These are flagged in the dataset.
- **One year only.** CLBI v1.1 is a snapshot and does not show improvement over time.
- **Not ranked:** 64 of the 437 companies in ranked groups, and all companies in the smaller groups. The reasons:
  - a missing value;
  - a reported zero awaiting confirmation;
  - a held-back value;
  - a revenue period that does not match the BRSR year;
  - a group too small to rank.

## 10. Sources

| Source | Period |
|--------------------------------------------|----------------------------|
| BRSR data files and PDFs, NSE filings archive | FY2025-26, collected 22–27 Oct 2026 |
| Revenue, profit, EBITDA: NSE annual financial filings | FY2025-26 |
| Company annual and sustainability reports (gap-fill, land, cement and power output) | FY2025-26 (land: latest available; FY2024-25 accepted and labelled) |
| Market-cap list: AMFI average market capitalisation | Jan–Jun 2026 |
| Sectors: NSE Indices industry classification | as of 22 Oct 2026 |

All results are produced by one set of scripts from these inputs. Every input file is fingerprinted, so any change can be detected.

## 11. Corrections

Every value is listed in the dataset and on the website (vinaybale-collab.github.io/clbi) with its source. A company that thinks a value is wrong can send a correction with the page reference in its published report. Corrections are applied only where they match a public document, and every change is logged.

---

## Annex A. Illustrative nature cost (not part of the ranking)

**What it is.** The annex multiplies each company's reported quantities by a price per unit of pressure, taken from published research. The result is a rough sense of the cost that the pressure puts on society and nature, shown as a share of revenue and of EBITDA.

**What it is not:**

- a bill, a liability or a valuation of the company;
- a precise figure: read it as sector patterns, not company numbers.

**Do not add companies together.** One company's Scope 2 emissions are another's Scope 1, so a total would double-count.

**Prices** (2025 rupees). Each central value is the middle of 3–5 independent sources.

| Pressure | Central | Range | Main basis |
|----------------------|---------:|---------------:|------------------------------|
| Greenhouse gas, per tonne CO2e | ₹22,600 | ₹13,900 – ₹38,400 | US EPA 2023 social cost of carbon; Rennert et al. 2022 (*Nature*) |
| SOx, per tonne | ₹2,09,000 | ₹85,000 – ₹13,69,000 | Middle of 4 health-damage estimates for India |
| NOx, per tonne | ₹2,10,000 | ₹1,11,000 – ₹9,93,000 | Middle of 3 estimates |
| Particulate matter, per tonne | ₹3,06,000 | ₹1,55,000 – ₹9,34,000 | CE Delft values, adjusted to India |
| Water consumed, per kilolitre | ₹40 | ₹10 – ₹200 | Kumar 2006 (*Water Policy*); IFVI 2026 |
| Degraded land, per hectare per year | ₹64,900 | ₹8,200 – ₹1,19,900 | Ecosystem Services Valuation Database (India); de Groot et al. 2012; Brander et al. 2024 |
| Waste | not valued | – | No reliable India-specific price found |

**How to read it:**

- **Greenhouse gas dominates.** It is typically 98% of the total. Its price is the global cost of climate damage, not an India-only figure, so the dataset also shows the share borne in India (about a quarter).
- **Water** is priced on consumption, not withdrawal; withdrawal is used only where consumption is not reported. Land is priced on net degraded hectares (pilot companies only).
- **Completeness.** A total is shown only where greenhouse gas is included, so the totals can be compared.

**Sector medians, as % of revenue:**

- cement ≈ 230%;
- power ≈ 120% (thermal generators far higher; hydro, solar and transmission below 5%);
- metals and mining ≈ 54%;
- textiles ≈ 21%;
- chemicals ≈ 16.5%;
- oil and gas ≈ 6%;
- most other manufacturing and services 1–5%;
- IT and financial services below 0.5%.

A figure above 100% means that, at these prices, the unpriced cost to society is larger than the company's sales. This is a known result for carbon-heavy sectors, not an error. Sector medians are shown only where at least 5 companies are costed.
