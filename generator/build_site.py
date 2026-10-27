#!/usr/bin/env python3
"""
CLBI v1.1 static site generator.

Reads the CLBI outputs and inputs (read-only) and writes a complete static site to ./docs
(GitHub Pages serves /docs). Re-run whenever outputs_v11 changes:

    python3 site/build_site.py

Nothing here estimates anything. The only arithmetic is formatting and the step-by-step
reproduction of the published calculation (intensity = value / revenue, position among
reporters, element score formula, credit sums, nature cost = quantity x price). Every
reproduced number is checked against the stored value; where they disagree only the stored
value is shown.
"""
import datetime
import html
import json
import math
import os
import re
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import markdown as md_lib
except ImportError:  # pragma: no cover
    md_lib = None

# ----------------------------------------------------------------------------------------------- paths
SITE = Path(__file__).resolve().parent
BASE = SITE.parent
OUT = SITE / "docs"
ASSETS_SRC = SITE / "assets_src"
OUTPUTS = BASE / "outputs_v11"
INPUTS = BASE / "inputs"
METHOD_MD = BASE / "CLBI_v1.1_Methodology_Note.md"
PVA = Path(os.environ.get(
    "CLBI_PVA",
    "/home/claude/codex/deliverables/CLBI_Full500_v2_2026-10-23/completion-2026-10-23/"
    "integration/tables/Physical_Variable_Accounts_15500.csv"))
CHART_JS = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"
FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
         "&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&display=swap")
BUILD_DATE = datetime.date.today().isoformat()

# ----------------------------------------------------------------------------------------------- vocab
TIERS = {
    "XML_explicit_unit_current_entity_period": (1, "Filed XBRL, explicit unit",
        "Value read from the BRSR XBRL file the company filed with NSE; the unit is declared explicitly in the filing."),
    "PDF_current_column_and_unit_reconciled": (2, "XBRL checked against filed PDF",
        "XBRL value whose column and unit were checked against the BRSR PDF filed alongside it."),
    "GAPFILL_public_report": (3, "Company report, verbatim quote",
        "XBRL was missing or blank, so the value was taken from the company's annual report, sustainability report or BRSR PDF, with URL, page and a verbatim quote."),
    "XML_unit_backfill_rule_R1_or_R2": (4, "XBRL with BRSR-prescribed unit reading",
        "XBRL value whose unit label was ambiguous (for example 'MtCO2e'); it is read as the BRSR format prescribes (metric tonnes)."),
    "CORRECTED_from_filed_PDF": (5, "Corrected to the company's published figure",
        "The filed value contained a unit slip; it was corrected to the figure the company itself published."),
}
NO_VALUE = {
    "not_reported_or_not_found": "Not reported",
    "reported_but_unit_unverified (excluded)": "Reported, but the unit could not be verified: not used",
    "not quantified in filing (PDF checked)": "Not quantified in the filing (PDF checked)",
    "excluded: extended_period_source_unaligned": "Excluded: filing period does not match FY2025-26",
}
METRICS = [  # (metric, label, element, used for)
    ("scope1_tco2e", "Scope 1 GHG emissions", "climate", "Climate score (with Scope 2); nature cost"),
    ("scope2_tco2e", "Scope 2 GHG emissions", "climate", "Climate score (with Scope 1); nature cost"),
    ("water_withdrawal_m3", "Water withdrawal", "water", "Water score"),
    ("water_consumption_m3", "Water consumption", "water", "Nature cost (water is priced on consumption)"),
    ("waste_generated_tonnes", "Waste generated", "waste", "Waste score; recycling credit (denominator)"),
    ("waste_recovered_tonnes", "Waste recovered", "waste", "Recycling credit (numerator)"),
    ("waste_disposed_tonnes", "Waste disposed", "waste", "Shown for completeness"),
    ("nox_tonnes", "Nitrogen oxides (NOx)", "air", "Air rank; nature cost"),
    ("sox_tonnes", "Sulphur oxides (SOx)", "air", "Air rank; nature cost"),
    ("pm_tonnes", "Particulate matter (PM)", "air", "Air rank; nature cost"),
    ("renewable_electricity_share_pct", "Renewable share of electricity", "credit", "Renewable-electricity credit"),
]
UNITS = {"tCO2e": "tCO₂e", "m3": "m³ (kL)", "tonnes": "tonnes", "%": "%"}
ELEMENTS = {
    "climate": dict(label="Climate", unit="tCO₂e", what="Scope 1 + Scope 2 emissions",
                    comps=["scope1_tco2e", "scope2_tco2e"]),
    "water": dict(label="Water", unit="m³", what="water withdrawal", comps=["water_withdrawal_m3"]),
    "waste": dict(label="Waste", unit="tonnes", what="waste generated", comps=["waste_generated_tonnes"]),
    "air": dict(label="Air", unit="tonnes", what="NOx + SOx + PM", comps=["nox_tonnes", "sox_tonnes", "pm_tonnes"]),
}
CORE = ["climate", "water", "waste"]
CORE_METRICS = ["scope1_tco2e", "scope2_tco2e", "water_withdrawal_m3", "waste_generated_tonnes"]
FIN_CAVEAT = ("Offices, branches and data centres only. For banks, lenders, insurers and intermediaries the reported footprint "
              "covers offices, branches and data centres. Their main environmental pressure comes through what they "
              "finance or insure, which BRSR does not report, and their revenue is not comparable with industrial "
              "revenue. Compare these companies only with each other.")


# ----------------------------------------------------------------------------------------------- helpers
def e(x):
    return html.escape("" if x is None else str(x), quote=True)


def isnum(x):
    if x is None:
        return False
    try:
        return not (pd.isna(x)) and np.isfinite(float(x))
    except (TypeError, ValueError):
        return False


def has(x):
    if x is None:
        return False
    if isinstance(x, float) and math.isnan(x):
        return False
    try:
        if pd.isna(x):
            return False
    except (TypeError, ValueError):
        pass
    return str(x).strip() not in ("", "nan", "None")


def truthy(x):
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    return str(x).strip().lower() in ("true", "1", "yes")


def _group_in(digits):
    if len(digits) <= 3:
        return digits
    last3, rest = digits[-3:], digits[:-3]
    parts = []
    while len(rest) > 2:
        parts.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.insert(0, rest)
    return ",".join(parts + [last3])


def fnum(x, dp=2, strip=True):
    """Indian digit grouping (lakh/crore). dp = max decimals; trailing zeros stripped."""
    if not isnum(x):
        return None
    x = float(x)
    s = f"{abs(x):.{dp}f}"
    if "." in s:
        ip, fp = s.split(".")
        if strip:
            fp = fp.rstrip("0")
    else:
        ip, fp = s, ""
    out = _group_in(ip) + ("." + fp if fp else "")
    return ("−" if x < 0 and float(s) != 0 else "") + out


def fsig(x, sig=4):
    """Significant-figure formatting with Indian grouping for large numbers."""
    if not isnum(x):
        return None
    x = float(x)
    if x == 0:
        return "0"
    ax = abs(x)
    mag = math.floor(math.log10(ax))
    if mag >= sig - 1:
        return fnum(round(x), 0)
    dp = sig - 1 - mag
    if dp > 7:
        m = f"{x:.{sig - 1}e}"
        mant, ex = m.split("e")
        return f"{mant.rstrip('0').rstrip('.')} × 10<sup>{int(ex)}</sup>"
    return fnum(x, dp)


def fraw(x):
    """Raw reported values: keep up to 3 decimals (more for tiny values)."""
    if not isnum(x):
        return None
    ax = abs(float(x))
    if ax != 0 and ax < 0.01:
        return fsig(x, 3)
    return fnum(x, 3)


def finr(x, dp=2):
    v = fnum(x, dp)
    return None if v is None else f"₹{v} cr"


def fscore(x):
    return None if not isnum(x) else f"{float(x):.1f}"


def fpct(x, dp=1):
    if not isnum(x):
        return None
    x = float(x)
    if abs(x) < 0.1 and x != 0:
        return fsig(x, 2) + "%"
    return fnum(x, dp, strip=False) + "%"


def fdate(x):
    try:
        d = datetime.date.fromisoformat(str(x)[:10])
        return f"{d.day} {d.strftime('%b')} {d.year}"
    except ValueError:
        return e(x)


def miss(text="not reported"):
    return f'<span class="missing">{e(text)}</span>'


def show(v, alt="not reported"):
    return v if v is not None else miss(alt)


def slugify(s):
    s = str(s).lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def human(s):
    s = str(s).replace("_", " ").strip()
    return s[:1].upper() + s[1:] if s else s


def jdump(obj):
    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        raise TypeError(type(o))
    s = json.dumps(obj, default=conv, ensure_ascii=False, separators=(",", ":"))
    return s.replace("</", "<\\/")


def num(x):
    return float(x) if isnum(x) else None


def link(url, text=None, cls="src"):
    if not has(url):
        return miss("no URL recorded")
    url = str(url)
    if text is None:
        m = re.match(r"https?://([^/]+)(/.*)?", url)
        host = m.group(1) if m else url
        fname = (m.group(2) or "").rstrip("/").split("/")[-1] if m else ""
        text = host + ("/…/" + fname if fname else "")
        if len(text) > 70:
            text = text[:67] + "…"
    return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(text)}</a>'


# ----------------------------------------------------------------------------------------------- load
def load():
    D = {}
    D["scores"] = pd.read_csv(OUTPUTS / "CLBI_v1_scores_all500.csv")
    D["lineage"] = pd.read_csv(OUTPUTS / "CLBI_v1_company_data.csv")
    D["queries"] = pd.read_csv(OUTPUTS / "CLBI_v1_data_queries.csv")
    D["robust"] = pd.read_csv(OUTPUTS / "CLBI_v1_robustness.csv")
    movers = OUTPUTS / "CLBI_v1_credit_movers.csv"
    D["movers"] = pd.read_csv(movers) if movers.exists() else None
    D["stats"] = json.loads((OUTPUTS / "build_stats.json").read_text())
    D["gapfill"] = pd.read_csv(INPUTS / "gapfill_values.csv")
    D["land"] = pd.read_csv(INPUTS / "land_values.csv")
    lg = INPUTS / "land_values_gapfill.csv"
    D["land_gf"] = pd.read_csv(lg) if lg.exists() else None
    D["prices"] = pd.read_csv(INPUTS / "prices.csv")
    D["comp"] = pd.read_csv(INPUTS / "comparator_values.csv")
    D["comp_groups"] = pd.read_csv(INPUTS / "comparator_groups.csv")
    D["land_ratios"] = pd.read_csv(INPUTS / "land_ratios.csv")
    pat = INPUTS / "pat_fy2026.csv"
    D["pat"] = pd.read_csv(pat) if pat.exists() else None
    D["method_md"] = METHOD_MD.read_text(encoding="utf-8")
    # optional: PDF reconciliation notes ("qualifications"). Only the text is read; the modelled
    # quantity columns are never loaded.
    D["quals"] = {}
    if PVA.exists():
        pva = pd.read_csv(PVA, usecols=["symbol", "metric", "complete_provenance_json"])
        for r in pva.itertuples(index=False):
            try:
                q = json.loads(r.complete_provenance_json).get("qualifications") or []
            except Exception:
                q = []
            q = [str(x).strip() for x in q if str(x).strip()]
            if q:
                D["quals"][(r.symbol, r.metric)] = q
    return D


# ----------------------------------------------------------------------------------------------- model
def status_of(r):
    cf = str(r.get("coverage_flag") or "")
    if isnum(r.get("rank_rev")):
        return "ranked", "Ranked"
    if cf.startswith("rank withheld"):
        return "withheld", "Rank withheld"
    if "scores shown, no rank" in cf:
        return "scores", "Scores only"
    if "below 10 companies" in cf:
        return "listed", "Listed only"
    if cf.startswith("revenue period"):
        return "revenue", "Not ranked: revenue"
    return "data", "Not ranked: data"


CAUTION_LEGEND = "† check before naming: business model not like-for-like, or a value 100–300× from the peer median"


def caution_of(r):
    v = r.get("naming_caution") if isinstance(r, dict) else getattr(r, "naming_caution", None)
    return str(v).strip() if has(v) else ""


def dagger(text, cls="dagger"):
    if not text:
        return ""
    return f'<span class="{cls}" title="Check before naming: {e(text)}" aria-label="Check before naming: {e(text)}">†</span>'


def leader(sub):
    """Highest-ranked company in a group without a naming caution (None for financial groups)."""
    if str(sub.score_group.iloc[0]).startswith("Financial Services"):
        return None
    c = sub[sub.rank_rev.notna()].copy()
    if "naming_caution" in c:
        c = c[~c.naming_caution.map(has)]
    if not len(c):
        return None
    return c.sort_values(["rank_rev", "mcap_rank"]).iloc[0]


STATUS_HELP = {
    "ranked": "Ranked within its peer group.",
    "withheld": "Rank withheld while a data query on a ranked element is open.",
    "scores": "Scores are shown, but too few peers have enough data for a rank.",
    "listed": "Peer group is too small to rank; listed for reference.",
    "revenue": "Revenue period or boundary does not match the BRSR year.",
    "data": "A core metric is missing or a reported zero is unconfirmed.",
}


def build_model(D):
    S = D["scores"].copy()
    S["slug"] = S.symbol.map(slugify)
    assert S.slug.is_unique, "company slug collision"
    S["gslug"] = S.score_group.map(slugify)
    st = S.apply(lambda r: status_of(r), axis=1)
    S["status_key"] = [s[0] for s in st]
    S["status_label"] = [s[1] for s in st]

    # lineage lookup
    L = D["lineage"]
    lin = {}
    for r in L.to_dict("records"):
        lin[(r["symbol"], r["metric"])] = r
    gf = {(r["symbol"], r["metric"]): r for r in D["gapfill"].to_dict("records")}

    # derivation of element positions: rank *_per_rev among non-null stored scores in the group
    deriv = {}
    for el in ELEMENTS:
        for g, sub in S.groupby("score_group"):
            s = sub[sub[f"{el}_score_rev"].notna() & sub[f"{el}_per_rev"].notna()]
            n = len(s)
            if n < 2:
                for sym in s.symbol:
                    deriv[(sym, el)] = None
                continue
            pos = s[f"{el}_per_rev"].rank(method="average")
            for sym, p, stored in zip(s.symbol, pos, s[f"{el}_score_rev"]):
                der = 100 * (n - p) / (n - 1)
                deriv[(sym, el)] = dict(n=n, pos=float(p), derived=der, ok=abs(der - stored) < 1e-6)

    prices = {r.pressure: r for r in D["prices"].itertuples()}
    comp_q = {r["symbol"]: r for r in D["comp"].to_dict("records")}
    land_q = {r["symbol"]: r for r in D["land"].to_dict("records")}
    land_gf = {r["symbol"]: r for r in D["land_gf"].to_dict("records")} if D["land_gf"] is not None else {}
    pat = {r["symbol"]: r for r in D["pat"].to_dict("records")} if D["pat"] is not None else {}
    queries = D["queries"]
    return dict(S=S, lin=lin, gf=gf, deriv=deriv, prices=prices, comp_q=comp_q, land_q=land_q,
                land_gf=land_gf, pat=pat, queries=queries)


def tier_strip(M, sym):
    """Four squares: scope 1, scope 2, water withdrawal, waste generated -> tier number or None."""
    out = []
    for m in CORE_METRICS:
        r = M["lin"].get((sym, m))
        t = None
        if r is not None and isnum(r.get("raw_value")) and r.get("source_status") in TIERS:
            t = TIERS[r["source_status"]][0]
        out.append(t)
    return out


# ----------------------------------------------------------------------------------------------- layout
NAV = [("index.html", "Overview", "home"), ("rankings.html", "Rankings", "rankings"),
       ("sectors.html", "Sectors", "sectors"), ("methodology.html", "Methodology", "methodology"),
       ("data-quality.html", "Data quality", "dq"), ("downloads.html", "Downloads", "downloads")]


def page(title, body, root, active="", charts=False, data=None, init="", desc="", body_cls=""):
    nav = "".join(
        f'<a href="{root}{href}"{" aria-current=\"page\"" if key == active else ""}>{e(lbl)}</a>'
        for href, lbl, key in NAV)
    scripts = []
    if charts:
        scripts.append(f'<script src="{CHART_JS}"></script>')
    scripts.append(f'<script src="{root}assets/companies.js"></script>')
    scripts.append(f'<script src="{root}assets/clbi.js"></script>')
    if data is not None:
        scripts.append(f'<script id="page-data" type="application/json">{jdump(data)}</script>')
    if init:
        scripts.append(f"<script>CLBI.ready(function(){{{init}}});</script>")
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(title)}</title>
<meta name="description" content="{e(desc or 'Corporate Land and Biodiversity Index v1.1 (draft): India’s 500 largest listed companies compared with sector peers on reported environmental pressure, with every number traced to its source.')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{root}assets/style.css">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
</head>
<body class="{body_cls}" data-root="{root}">
<a class="skip" href="#main">Skip to content</a>
<div class="draft-bar" role="note"><div class="wrap"><strong>Draft for review — not for publication.</strong> <span>Figures may change before release.</span></div></div>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="{root}index.html" aria-label="CLBI home">
      <svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect x="1" y="1" width="30" height="30" rx="7" fill="var(--forest)"/><path d="M9 22c0-7 5-12 14-12-1 8-5 13-12 13" fill="none" stroke="var(--paper)" stroke-width="2.2" stroke-linecap="round"/><path d="M10 23l7-7" stroke="var(--paper)" stroke-width="2.2" stroke-linecap="round"/></svg>
      <span class="brand-text"><span class="brand-name">Corporate Land &amp; Biodiversity Index</span><span class="brand-sub">CLBI v1.1 draft</span></span>
    </a>
    <div class="header-search" data-search></div>
  </div>
  <nav class="wrap site-nav" id="site-nav" aria-label="Main">{nav}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-row">
    <p class="footer-line">CLBI v1.1 draft · Urvara.Life with Landstack · data FY2025-26 · build date {BUILD_DATE}</p>
    {footer_links(root)}
    <p class="footer-note">Every value is a company's own disclosure unless labelled otherwise. Illustrative nature costs are not liabilities and are not used in any rank.</p>
  </div>
</footer>
{chr(10).join(scripts)}
</body>
</html>
"""


def footer_links(root):
    if not DELIV_COPIED:
        return f'<p class="footer-links"><a href="{root}downloads.html">Downloads</a></p>'
    links = "".join(f'<a href="{root}downloads/{e(fn)}">{e(label)}</a>' for fn, label, _, _ in DELIV_COPIED)
    return f'<p class="footer-links">{links}<a href="{root}downloads.html">All downloads</a></p>'


def write(path, text):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def status_pill(key, label, title=None):
    t = f' title="{e(title)}"' if title else ""
    return f'<span class="pill pill-{key}"{t}>{e(label)}</span>'


def tiers_html(strip):
    names = ["Scope 1", "Scope 2", "Water withdrawal", "Waste generated"]
    cells = []
    for nm, t in zip(names, strip):
        if t is None:
            cells.append(f'<i class="tq t0" title="{e(nm)}: not reported"></i>')
        else:
            lab = [v for v in TIERS.values() if v[0] == t][0][1]
            cells.append(f'<i class="tq t{t}" title="{e(nm)}: tier {t}, {e(lab)}"></i>')
    return f'<span class="tiers" aria-label="Source tiers for core values">{"".join(cells)}</span>'


# ----------------------------------------------------------------------------------------------- companies.js
def write_companies_js(M):
    S = M["S"].sort_values("mcap_rank")
    rows = [[r.symbol, r.company, r.slug, r.score_group] for r in S.itertuples()]
    write("assets/companies.js", "window.CLBI_COMPANIES=" + jdump(rows) + ";\n")


# ----------------------------------------------------------------------------------------------- markdown
def md(text):
    if md_lib is None:
        return "<pre>" + e(text) + "</pre>"
    return md_lib.markdown(text, extensions=["tables", "toc", "sane_lists"])


METHOD_IDS = []


def manchor(*keys):
    """Link to the methodology section whose heading contains one of the keywords."""
    for k in keys:
        for hid, text in METHOD_IDS:
            if k.lower() in text.lower():
                return f"methodology.html#{hid}"
    return "methodology.html"


def md_sections(text):
    parts = re.split(r"(?m)^## ", text)
    out = {}
    for p in parts[1:]:
        head, _, body = p.partition("\n")
        out[head.strip()] = body.strip()
    return out


# ----------------------------------------------------------------------------------------------- home
def hero_specimen(M):
    """A real lineage example for the hero: the methodology's worked example (ACC) if ranked, else the
    largest ranked company with a Tier 1 Scope 1 value."""
    S = M["S"]
    ok = S[S.rank_rev.notna() & ~S.score_group.str.startswith("Financial Services")]
    if "naming_caution" in ok:
        ok = ok[~ok.naming_caution.map(has)]
    cands = list(ok[ok.symbol == "ACC"].itertuples()) + list(ok.sort_values("mcap_rank").itertuples())
    for r in cands:
        L = M["lin"].get((r.symbol, "scope1_tco2e"))
        d = M["deriv"].get((r.symbol, "climate"))
        if not (isnum(r.rank_rev) and L and isnum(L.get("raw_value")) and L.get("source_status") in TIERS and d and d["ok"]):
            continue
        tn, tl, _ = TIERS[L["source_status"]]
        field = L.get("source_field") if has(L.get("source_field")) else ""
        return f"""<aside class="specimen" aria-label="Example: one number traced to its source">
  <p class="sp-title">One number, traced <span class="sp-dots" aria-hidden="true"><i class="sw-climate"></i><i class="sw-water"></i><i class="sw-waste"></i><i class="sw-air"></i></span></p>
  <p class="sp-co"><a href="company/{r.slug}.html">{e(r.company)}</a><span>{e(r.score_group)}</span></p>
  <div class="sp-row"><span class="sp-l">Scope 1 emissions, FY2025-26</span><span class="sp-v num">{fraw(L['raw_value'])} <small>tCO₂e</small></span></div>
  <div class="sp-row"><span class="sp-l">Source</span><span class="sp-s">{link(L.get('source_url'))}<span class="field">{e(field)}</span></span></div>
  <div class="sp-row"><span class="sp-l">Confidence</span><span class="sp-s"><span class="tier"><i class="tq t{tn}"></i>Tier {tn}: {e(tl)}</span></span></div>
  <ol class="sp-flow">
    <li><span class="num">{fsig(r.climate_per_rev, 4)}</span><small>tCO₂e per ₹ crore, with Scope 2</small></li>
    <li><span class="num">{float(r.climate_score_rev):.0f}</span><small>climate score, {fnum(d['pos'], 1)} of {d['n']}</small></li>
    <li><span class="num">{int(r.rank_rev)}<em>/{int(r.ranked_n_rev)}</em></span><small>final rank in peer group</small></li>
  </ol>
  <a class="sp-cta" href="company/{r.slug}.html">See every number for {e(r.company)}</a>
</aside>"""
    return ""


def build_home(D, M):
    S, st = M["S"], D["stats"]
    n_univ = st.get("universe", len(S))
    n_ranked = int(S.rank_rev.notna().sum())
    n_groups_ranked = int(S[S.rank_rev.notna()].score_group.nunique())
    L = D["lineage"]
    core = L[L.metric.isin(CORE_METRICS) & L.raw_value.notna()]
    tier_share = core.source_status.value_counts()
    n_core = len(core)
    secs = md_sections(D["method_md"])
    sec1, sec1_head, aside_head, aside = None, "", "", ""
    for k, v in secs.items():
        if k.startswith("1.") and sec1 is None:
            sec1, sec1_head = v, k
        elif "principle" in k.lower() and not aside:
            aside_head, aside = re.sub(r"^\d+\.\s*", "", k), v
    is_part = sec1 or ""
    if "**What is new" in is_part:
        is_part, new_part = is_part.split("**What is new", 1)
        if not aside:
            aside = "**What is new" + new_part
    sec1_link = manchor(sec1_head) if sec1_head else "methodology.html"

    # universe grid
    groups = []
    for g, sub in S.groupby("score_group"):
        sub = sub.copy()
        sub["_r"] = sub.rank_rev.fillna(1e9)
        sub = sub.sort_values(["_r", "mcap_rank"])
        groups.append((g, sub))
    groups.sort(key=lambda t: (-int(t[1].rank_rev.notna().sum() > 0), -len(t[1]), t[0]))
    rows_html = []
    for g, sub in groups:
        cells = []
        for r in sub.itertuples():
            if isnum(r.rank_rev):
                lvl = max(1, min(5, int(math.ceil((float(r.final_score_rev) + 1e-9) / 20))))
                tip = f"{r.company} — rank {int(r.rank_rev)} of {int(r.ranked_n_rev)} in {g}, score {float(r.final_score_rev):.1f}"
                cells.append(f'<a class="u u{lvl}" href="company/{r.slug}.html" data-tip="{e(tip)}" aria-label="{e(r.company)}"></a>')
            else:
                tip = f"{r.company} — {r.status_label.lower()}"
                cells.append(f'<a class="u u0" href="company/{r.slug}.html" data-tip="{e(tip)}" aria-label="{e(r.company)}"></a>')
        nr = int(sub.rank_rev.notna().sum())
        rows_html.append(
            f'<div class="u-row"><a class="u-label" href="sector/{sub.gslug.iloc[0]}.html">{e(g)}'
            f'<span>{nr} of {len(sub)} ranked</span></a><div class="u-cells">{"".join(cells)}</div></div>')

    # quick picks: largest by market cap
    picks = S.sort_values("mcap_rank").head(6)
    pick_html = " ".join(f'<a class="chip" href="company/{r.slug}.html">{e(r.company)}</a>' for r in picks.itertuples())

    # coverage by metric
    rc = st.get("reported_counts", {})
    cov_rows = []
    for el in ["climate", "water", "waste", "air"]:
        if el in rc:
            v = rc[el]
            cov_rows.append(
                f'<div class="cov"><span class="cov-l"><i class="sw sw-{el}"></i>{ELEMENTS[el]["label"]}</span>'
                f'<span class="cov-bar"><span class="cov-fill fill-{el}" style="width:{100 * v / n_univ:.1f}%"></span></span>'
                f'<span class="cov-n num">{v} <small>of {n_univ}</small></span></div>')
    tier_rows = []
    tier_bar = []
    for code, (tn, lab, _) in TIERS.items():
        c = int(tier_share.get(code, 0))
        sh = 100 * c / n_core if n_core else 0
        tier_bar.append(f'<span class="tb t{tn}" style="width:{sh:.2f}%" title="Tier {tn}: {e(lab)} — {sh:.1f}%"></span>')
        tier_rows.append(f'<li><i class="tq t{tn}"></i><span class="tl">Tier {tn}: {e(lab)}</span><span class="num">{sh:.1f}%</span></li>')

    # sector tiles
    tiles = sector_tiles(D, M)

    stats_html = f"""
    <div class="kpis">
      <div class="kpi"><span class="kpi-v num">{n_univ}</span><span class="kpi-l">companies in the universe, by six-month average market capitalisation</span></div>
      <div class="kpi"><span class="kpi-v num">{n_ranked}</span><span class="kpi-l">ranked within their peer group on climate, water and waste</span></div>
      <div class="kpi"><span class="kpi-v num">{n_groups_ranked}</span><span class="kpi-l">peer groups with a published rank</span></div>
      <div class="kpi"><span class="kpi-v num">{st.get('data_queries', len(D['queries']))}</span><span class="kpi-l">open data queries, each excluded until the company confirms</span></div>
    </div>"""

    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="kicker">Corporate Land and Biodiversity Index, version 1.1 draft</p>
      <h1>How much pressure do India’s 500 largest companies put on nature, per rupee they earn?</h1>
      <p class="lead">CLBI compares each company only with its sector peers, on the climate, water and waste figures it reports itself. Pick a company to see every number, where it came from and how it was calculated.</p>
      <div class="hero-search" data-search data-size="lg" data-autofocus="0"></div>
      <p class="picks"><span>Try</span> {pick_html}</p>
    </div>
    {hero_specimen(M)}
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <h2>The index at a glance</h2>
      <p>Each square is one company, grouped by peer group and ordered by rank. Darker green means a higher score: lower reported pressure per rupee of revenue than most peers. Hollow squares are listed but not ranked. Select any square to open the company.</p>
    </div>
    <div class="universe" id="universe">{''.join(rows_html)}</div>
    <div class="u-legend"><span><i class="u u1"></i><i class="u u2"></i><i class="u u3"></i><i class="u u4"></i><i class="u u5"></i> Final score 0 → 100</span><span><i class="u u0"></i> Not ranked</span></div>
  </div>
</section>

<section class="section">
  <div class="wrap">{stats_html}</div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div class="prose">
      <h2>What CLBI is, and what it is not</h2>
      {md(is_part)}
    </div>
    <div class="prose aside-prose">
      {('<h3>' + e(aside_head) + '</h3>') if aside_head else ''}
      {md(aside)}
      <p class="muted small">From the <a href="{sec1_link}">methodology note</a>.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div>
      <h2 class="h3">Coverage by metric</h2>
      <p class="muted">Companies with a reported value for FY2025-26, out of {n_univ}.</p>
      <div class="covs">{''.join(cov_rows)}</div>
    </div>
    <div>
      <h2 class="h3">Where the core values come from</h2>
      <p class="muted">Confidence tier of the {fnum(n_core, 0)} core values with a recorded figure (Scope 1, Scope 2, water withdrawal, waste generated).</p>
      <div class="tierbar">{''.join(tier_bar)}</div>
      <ul class="tier-list">{''.join(tier_rows)}</ul>
      <p class="small"><a href="data-quality.html">What each tier means</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Peer groups</h2><p>Companies are only ever compared within their own peer group. A cement maker is never ranked against a bank.</p></div>
    {tiles}
  </div>
</section>
"""
    write("index.html", page("Corporate Land and Biodiversity Index (CLBI) v1.1 draft", body, "", "home",
                             init="CLBI.universe();", body_cls="home"))


def sector_tiles(D, M):
    S = M["S"]
    els = D["stats"].get("elements_scored_by_sector", {})
    rows = []
    for g, sub in S.groupby("score_group"):
        nr = int(sub.rank_rev.notna().sum())
        rows.append((nr > 0, len(sub), g, sub, nr))
    rows.sort(key=lambda t: (-t[0], -t[1], t[2]))
    out = []
    for ranked, n, g, sub, nr in rows:
        el = els.get(g, [])
        dots = "".join(f'<i class="sw sw-{x}" title="{ELEMENTS[x]["label"]}"></i>' for x in el if x in ELEMENTS)
        fs = '<span class="tile-note">Offices, branches and data centres only</span>' if g.startswith("Financial Services") else ""
        state = f"{nr} of {n} ranked" if nr else f"{n} listed, not ranked"
        out.append(
            f'<a class="tile{"" if nr else " tile-muted"}" href="{{root}}sector/{sub.gslug.iloc[0]}.html">'
            f'<span class="tile-name">{e(g)}</span>'
            f'<span class="tile-bar"><span style="width:{100 * nr / n:.1f}%"></span></span>'
            f'<span class="tile-meta"><span class="num">{state}</span><span class="dots">{dots}</span></span>{fs}</a>')
    return '<div class="tiles">' + "".join(out) + "</div>"


def build_sectors_index(D, M):
    tiles = sector_tiles(D, M).replace("{root}", "")
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>Peer groups</h1>
  <p class="lead">CLBI ranks companies only within a peer group of at least ten with all three core metrics. Financial Services is split into sub-groups because a bank’s footprint is its offices, not what it finances.</p>
</div></section>
<section class="section"><div class="wrap">{tiles}
<p class="muted small">Coloured dots show which elements are scored in each group: <i class="sw sw-climate"></i> climate <i class="sw sw-water"></i> water <i class="sw sw-waste"></i> waste <i class="sw sw-air"></i> air (separate rank).</p>
</div></section>"""
    write("sectors.html", page("Peer groups | CLBI v1.1 draft", body, "", "sectors"))


def fix_home_tiles():
    p = OUT / "index.html"
    p.write_text(p.read_text(encoding="utf-8").replace("{root}", ""), encoding="utf-8")


# ----------------------------------------------------------------------------------------------- rankings
def build_rankings(D, M):
    S = M["S"]
    rows = []
    for r in S.itertuples():
        rows.append(dict(
            s=r.symbol, c=r.company, u=r.slug, g=r.score_group, gu=r.gslug,
            r=num(r.rank_rev), n=num(r.ranked_n_rev), f=num(r.final_score_rev), p=num(r.pressure_score_rev),
            cr=num(r.credit_points), a=num(r.rank_air), q=r.quartile_rev if has(r.quartile_rev) else None,
            k=r.status_key, kl=r.status_label, why=str(r.coverage_flag) if has(r.coverage_flag) else "",
            t=tier_strip(M, r.symbol), m=num(r.mcap_rank), nc=caution_of(r)))
    n_air = {g: int(sub.rank_air.notna().sum()) for g, sub in S.groupby("score_group")}
    groups = sorted(S.score_group.unique())
    opts = "".join(f'<option value="{e(g)}">{e(g)}</option>' for g in groups)
    sopts = "".join(f'<option value="{k}">{e(v)}</option>' for k, v in
                    [("ranked", "Ranked"), ("withheld", "Rank withheld"), ("scores", "Scores only"),
                     ("listed", "Listed only"), ("revenue", "Not ranked: revenue"), ("data", "Not ranked: data"),
                     ("unranked", "Any not ranked")])
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>Rankings</h1>
  <p class="lead">All {len(S)} companies. Ranks are within the peer group only, so a rank of 1 means the lowest reported pressure per rupee of revenue among that group’s ranked companies.</p>
</div></section>
<section class="section tight"><div class="wrap">
  <div class="filters" role="search">
    <label class="f-search"><span class="sr">Filter by name or symbol</span><input id="f-q" type="search" placeholder="Filter by name or symbol" autocomplete="off"></label>
    <label><span class="sr">Peer group</span><select id="f-g"><option value="">All peer groups</option>{opts}</select></label>
    <label><span class="sr">Status</span><select id="f-s"><option value="">Any status</option>{sopts}</select></label>
    <span class="f-count num" id="f-count" aria-live="polite"></span>
  </div>
  <div class="table-wrap">
    <table class="data rank-table" id="rank-table">
      <thead><tr>
        <th data-k="c" class="l">Company</th>
        <th data-k="g" class="l">Peer group</th>
        <th data-k="r" class="r" title="Rank within peer group, of n ranked">Rank</th>
        <th data-k="f" class="r">Final score</th>
        <th data-k="p" class="r">Pressure</th>
        <th data-k="cr" class="r">Credit</th>
        <th data-k="a" class="r" title="Separate air-pollution rank within the peer group">Air rank</th>
        <th data-k="t" class="c" title="Source tier of Scope 1, Scope 2, water withdrawal and waste generated">Data</th>
        <th data-k="k" class="l">Status</th>
      </tr></thead>
      <tbody></tbody>
    </table>
  </div>
  <button class="more-btn" id="f-more" type="button" hidden>Show all</button>
  <div class="legend-row small muted">
    <span class="dagger-legend">{e(CAUTION_LEGEND)}</span>
    <span><strong>Data</strong>: four squares for Scope 1, Scope 2, water withdrawal and waste generated, coloured by confidence tier.</span>
    <span class="tier-keys"><i class="tq t1"></i>1 Filed XBRL <i class="tq t2"></i>2 Checked against PDF <i class="tq t3"></i>3 Report quote <i class="tq t4"></i>4 BRSR unit reading <i class="tq t5"></i>5 Corrected <i class="tq t0"></i> not reported</span>
  </div>
</div></section>"""
    write("rankings.html", page("Rankings | CLBI v1.1 draft", body, "", "rankings",
                                data=dict(rows=rows, nair=n_air), init="CLBI.rankings();"))


# ----------------------------------------------------------------------------------------------- sector
def build_sector(D, M, g, sub):
    S = M["S"]
    root = "../"
    gslug = sub.gslug.iloc[0]
    els_scored = D["stats"].get("elements_scored_by_sector", {}).get(g, [])
    is_fin = g.startswith("Financial Services")
    n = len(sub)
    nr = int(sub.rank_rev.notna().sum())
    n_air = int(sub.rank_air.notna().sum())
    comp_name = None
    cg = D["comp_groups"]
    if g in set(cg.score_group):
        crow = cg[cg.score_group == g].iloc[0]
        comp_name, comp_unit = crow.comparator_name, crow.unit
    n_comp = int(sub.rank_comp.notna().sum())

    sub = sub.copy()
    sub["_r"] = sub.rank_rev.fillna(1e9)
    sub = sub.sort_values(["_r", "final_score_rev", "mcap_rank"], ascending=[True, False, True])

    # table rows (heat cells)
    def heat(v):
        if not isnum(v):
            return '<td class="r heat hm-na"><span class="missing">–</span></td>'
        lvl = max(0, min(10, int(round(float(v) / 10))))
        return f'<td class="r heat hm{lvl}" data-v="{float(v):.4f}">{float(v):.0f}</td>'

    trs = []
    for r in sub.itertuples():
        rank = f'{int(r.rank_rev)}<small>/{int(r.ranked_n_rev)}</small>' if isnum(r.rank_rev) else '<span class="missing">–</span>'
        cells = "".join(heat(getattr(r, f"{el}_score_rev")) for el in ["climate", "water", "waste"])
        cells += heat(r.air_score_rev)
        air = f'{int(r.rank_air)}<small>/{n_air}</small>' if isnum(r.rank_air) else '<span class="missing">–</span>'
        trs.append(
            f'<tr class="{"" if isnum(r.rank_rev) else "unranked"}"><td class="r num" data-v="{num(r.rank_rev) or 9999}">{rank}</td>'
            f'<td class="l"><a href="../company/{r.slug}.html">{e(r.company)}</a>{dagger(caution_of(r))}<span class="sym">{e(r.symbol)}</span></td>'
            f'{cells}<td class="r num" data-v="{num(r.pressure_score_rev) or -1}">{show(fscore(r.pressure_score_rev), "–")}</td>'
            f'<td class="r num" data-v="{num(r.credit_points) or 0}">{"+" + format(float(r.credit_points), ".1f") if isnum(r.credit_points) else "–"}</td>'
            f'<td class="r num strong" data-v="{num(r.final_score_rev) or -1}">{show(fscore(r.final_score_rev), "–")}</td>'
            f'<td class="r num" data-v="{num(r.rank_air) or 9999}">{air}</td>'
            f'<td class="l">{status_pill(r.status_key, r.status_label, str(r.coverage_flag))}</td></tr>')

    # chart data
    comps = []
    for r in sub.itertuples():
        d = dict(s=r.symbol, c=r.company, u=r.slug, rk=num(r.rank_rev), f=num(r.final_score_rev),
                 p=num(r.pressure_score_rev), rp=num(r.restoration_points), yp=num(r.recycling_points),
                 ep=num(r.re_points), k=r.status_key,
                 nr=num(r.nature_cost_pct_revenue), ne=num(r.nature_cost_pct_ebitda),
                 rc=num(r.rank_comp), cv=num(r.comparator_value), ar=num(r.rank_air))
        for el in ELEMENTS:
            d[el] = num(getattr(r, f"{el}_per_rev"))
            d[el + "_s"] = num(getattr(r, f"{el}_score_rev"))
            d[el + "_abs"] = num(getattr(r, el))
        comps.append(d)

    # comparator table
    comp_html = ""
    if comp_name:
        cq = M["comp_q"]
        crs = []
        csub = sub[sub.comparator_value.notna()].copy()
        csub["_c"] = csub.rank_comp.fillna(1e9)
        csub = csub.sort_values(["_c", "mcap_rank"])
        unit_lbl = "t cement" if comp_unit == "t" else comp_unit
        for r in csub.itertuples():
            q = cq.get(r.symbol, {})
            per = r.climate / r.comparator_value if isnum(r.climate) and isnum(r.comparator_value) and r.comparator_value > 0 else None
            quote = f'<details class="q"><summary>Quote{(", page " + e(q.get("page"))) if has(q.get("page")) else ""}</summary><blockquote>{e(q.get("verbatim_quote"))}</blockquote></details>' if has(q.get("verbatim_quote")) else ""
            crs.append(
                f'<tr><td class="l"><a href="../company/{r.slug}.html">{e(r.company)}</a></td>'
                f'<td class="r num">{fnum(r.comparator_value, 0)} <small>{e(comp_unit)}</small></td>'
                f'<td class="r num">{show(fsig(per, 3) if per is not None else None, "–")}</td>'
                f'<td class="r num">{int(r.rank_rev) if isnum(r.rank_rev) else "–"}</td>'
                f'<td class="r num strong">{int(r.rank_comp) if isnum(r.rank_comp) else "–"}</td>'
                f'<td class="l small">{link(r.comparator_source_url)}{quote}</td></tr>')
        label = "tonne of cement produced" if comp_unit == "t" else "MWh generated"
        both = int((sub.rank_rev.notna() & sub.rank_comp.notna()).sum())
        slope = ""
        if both >= 2:
            slope = (f'<figure class="chart-card wide comp-fig"><figcaption><strong>Revenue rank against output rank</strong><span>Each line joins a company’s two ranks. Flat lines mean the two views agree; lines in terracotta move three or more places.</span></figcaption>'
                     f'<div class="chart-box" style="height:{max(300, 30 * both + 60)}px"><canvas id="slope"></canvas></div></figure>')
        comp_html = f"""
<section class="section" id="comparator"><div class="wrap">
  <div class="section-head"><h2>Per {label}: a physical comparator</h2>
  <p>Revenue favours high-price products, so {e(g)} also gets a view per {label}. The same scoring method is applied with output in place of revenue; the comparator rank is shown alongside the revenue rank, not instead of it.</p></div>
  {slope}
    <div class="table-wrap"><table class="data"><thead><tr><th class="l">Company</th><th class="r">Output FY2025-26</th><th class="r">tCO₂e per {e(unit_lbl)}</th><th class="r">Revenue rank</th><th class="r">Output rank</th><th class="l">Source</th></tr></thead><tbody>{''.join(crs)}</tbody></table>
    <p class="small muted">tCO₂e per unit = (Scope 1 + Scope 2) ÷ output, shown for reading only. {f'Output rank among {n_comp} companies with an output figure.' if n_comp else 'No output rank is published for this group in this build: fewer than ten companies have both a complete score and an output figure.'}</p>
</div></section>"""

    unranked = sub[sub.rank_rev.isna()]
    un_html = ""
    if len(unranked):
        lis = "".join(f'<tr><td class="l"><a href="../company/{r.slug}.html">{e(r.company)}</a></td><td class="l">{status_pill(r.status_key, r.status_label)}</td><td class="l small">{e(human(r.coverage_flag))}</td></tr>' for r in unranked.itertuples())
        un_html = f"""<section class="section" id="unranked"><div class="wrap"><div class="section-head"><h2>Listed but not ranked</h2><p>{len(unranked)} companies in this group have no rank. The reason is recorded for each.</p></div>
<div class="table-wrap"><table class="data"><thead><tr><th class="l">Company</th><th class="l">Status</th><th class="l">Reason</th></tr></thead><tbody>{lis}</tbody></table></div></div></section>"""

    flags_bm = int(sub.business_model_flag.notna().sum())
    ld = leader(sub)
    lead_html = ""
    if is_fin:
        lead_html = ""
    elif ld is not None:
        lead_html = (f'<p class="lead-line">Lowest reported pressure per rupee among companies cleared for naming: '
                     f'<a href="../company/{ld.slug}.html">{e(ld.company)}</a>, rank {int(ld.rank_rev)} of {int(ld.ranked_n_rev)}.</p>')
    caveat = f'<div class="callout callout-fin"><strong>Offices, branches and data centres only.</strong> {e(FIN_CAVEAT.split(". ", 1)[1])}</div>' if is_fin else ""
    els_txt = ", ".join(ELEMENTS[x]["label"].lower() for x in els_scored if x in ELEMENTS) or "none (group not scored)"

    nc = sub[sub.nature_cost_pct_revenue.notna()]
    intensity_charts = ""
    for el in ["climate", "water", "waste", "air"]:
        cnt = int(sub[f"{el}_per_rev"].gt(0).sum())
        if cnt == 0:
            continue
        intensity_charts += f"""
    <figure class="chart-card">
      <figcaption><strong><i class="sw sw-{el}"></i>{ELEMENTS[el]['label']}{' (separate rank)' if el == 'air' else ''}</strong><span>{ELEMENTS[el]['unit']} per ₹ crore of revenue, {ELEMENTS[el]['what']}. Lowest first.</span></figcaption>
      <div class="chart-box" style="height:{18 * cnt + 56}px"><canvas data-intensity="{el}"></canvas></div>
      <p class="chart-note" data-note="{el}"></p>
    </figure>"""

    body = f"""
<section class="page-head"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Overview</a><a href="../sectors.html">Peer groups</a><span>{e(g)}</span></nav>
  <h1>{e(g)}</h1>
  <p class="lead">{n} companies, {nr} ranked{f', {n_air} also ranked on air pollution' if n_air else ''}. Scored on {els_txt}.</p>
  {lead_html}
  {caveat}
  <div class="facts">
    <div><span class="num">{n}</span>companies</div>
    <div><span class="num">{nr}</span>ranked</div>
    <div><span class="num">{n_air or '–'}</span>ranked on air</div>
    <div><span class="num">{flags_bm or '–'}</span>business-model flags</div>
  </div>
</div></section>

<section class="section tight"><div class="wrap">
  <details class="howto" open><summary>How to read this page</summary>
  <ul>
    <li><strong>Intensity</strong> is the reported quantity divided by FY2025-26 revenue in ₹ crore. Lower is better.</li>
    <li><strong>Element scores</strong> (0–100) place each company among the peers that reported that element: the lowest intensity scores 100, the highest 0. Only the order matters, so one extreme value cannot distort the others.</li>
    <li><strong>Pressure score</strong> is the average of climate, water and waste; all three must be reported. <strong>Credit</strong> for restoration, recycling and renewable electricity adds up to 10 points. Air is ranked separately and is not part of the pressure score.</li>
    <li>A high rank means only that the company reported lower pressure per rupee than most peers. It is not a biodiversity or ESG rating.</li>
  </ul></details>
</div></section>

<section class="section" id="table"><div class="wrap">
  <div class="section-head"><h2>Ranked table</h2><p>Element scores are shaded from light (0, highest pressure) to deep green (100, lowest). Select a column to sort.</p></div>
  <div class="table-wrap"><table class="data sortable heat-table">
    <thead><tr><th class="r" data-sort>Rank</th><th class="l" data-sort>Company</th><th class="r" data-sort><i class="sw sw-climate"></i>Climate</th><th class="r" data-sort><i class="sw sw-water"></i>Water</th><th class="r" data-sort><i class="sw sw-waste"></i>Waste</th><th class="r" data-sort><i class="sw sw-air"></i>Air</th><th class="r" data-sort>Pressure</th><th class="r" data-sort>Credit</th><th class="r" data-sort>Final</th><th class="r" data-sort>Air rank</th><th class="l">Status</th></tr></thead>
    <tbody>{''.join(trs)}</tbody></table></div>
  {('<p class="small muted dagger-legend">' + e(CAUTION_LEGEND) + '</p>') if sub.naming_caution.map(has).any() else ''}
</div></section>

<section class="section" id="composition"><div class="wrap">
  <div class="section-head"><h2>How each final score is built</h2><p>Pressure score plus the three credits, for every company with a pressure score. Credit is deliberately small: it recognises effort, it does not offset pressure.</p></div>
  <figure class="chart-card wide"><div class="chart-box" style="height:{max(200, 20 * int(sub.pressure_score_rev.notna().sum()) + 70)}px"><canvas id="stack"></canvas></div>
  <div class="legend"><span><i class="sw" style="background:var(--pressure)"></i>Pressure score</span><span><i class="sw" style="background:var(--c-rest)"></i>Restoration credit</span><span><i class="sw" style="background:var(--c-recy)"></i>Recycling credit</span><span><i class="sw" style="background:var(--c-re)"></i>Renewable electricity credit</span></div></figure>
</div></section>

<section class="section" id="intensity"><div class="wrap">
  <div class="section-head"><h2>Intensity per ₹ crore of revenue</h2><p>Coloured bars are ranked companies; pale bars are scored but not ranked; grey bars are reported but not scored (reported zero, open data query, or group not scored). A logarithmic axis is used where values span more than a hundredfold.</p></div>
  <div class="grid-2">{intensity_charts or '<p class="muted">No intensity data.</p>'}</div>
</div></section>
{comp_html}
<section class="section" id="naturecost"><div class="wrap">
  <div class="section-head"><h2>Illustrative nature cost</h2><p><span class="tag-illus">Illustrative — not a liability, not used in rank.</span> Reported quantities multiplied by India-specific prices, as a share of revenue and of EBITDA. Each dot is a company; the vertical line is the group median{' (shown only where at least 5 companies have a value)'}. Read it as a sector pattern, not a precise company figure.</p></div>
  {('<figure class="chart-card wide"><div class="chart-box" style="height:260px"><canvas id="strip"></canvas></div><p class="chart-note" id="strip-note"></p></figure>') if len(nc) else '<p class="muted">No company in this group has an illustrative nature cost.</p>'}
</div></section>
{un_html}
"""
    data = dict(group=g, comps=comps, n_air=n_air, comp=bool(comp_name), comp_unit=(comp_unit if comp_name else None))
    write(f"sector/{gslug}.html", page(f"{g} | CLBI v1.1 draft", body, root, "sectors", charts=True,
                                       data=data, init="CLBI.sector();"))


# ----------------------------------------------------------------------------------------------- company
def lineage_rows(M, r):
    sym = r["symbol"]
    out = []
    for m, label, el, used in METRICS:
        L = M["lin"].get((sym, m))
        if L is None:
            continue
        val = L.get("raw_value")
        unit = UNITS.get(L.get("unit"), L.get("unit"))
        flag = L.get("flag")
        ss = L.get("source_status")
        if isnum(val):
            vtxt = f'<span class="num v">{fraw(val)}</span> <span class="unit">{e(unit)}</span>'
            if flag == "reported_zero":
                vtxt += '<span class="note-zero">Reported zero: kept, not scored, to confirm</span>'
        else:
            vtxt = miss(NO_VALUE.get(flag, "not reported"))
        if isnum(val) and ss in TIERS:
            tn, tl, _ = TIERS[ss]
            tier = f'<span class="tier"><i class="tq t{tn}"></i>{e(tl)}</span><span class="tier-n">Tier {tn}</span>'
        elif ss in TIERS and not isnum(val):
            tier = f'<span class="tier"><i class="tq t0"></i>{e(NO_VALUE.get(flag, "No value"))}</span>'
        else:
            tier = f'<span class="tier"><i class="tq t0"></i>{e(NO_VALUE.get(flag, human(ss)))}</span>'
        src = []
        if has(L.get("source_url")):
            src.append(link(L.get("source_url")))
        gfr = M["gf"].get((sym, m))
        if gfr is not None and ss in ("GAPFILL_public_report", "CORRECTED_from_filed_PDF"):
            meta = []
            if has(gfr.get("source_type")):
                meta.append(e(gfr["source_type"]))
            if has(gfr.get("page")):
                meta.append("page " + e(gfr["page"]))
            if meta:
                src.append(f'<span class="field">{", ".join(meta)}</span>')
            if has(gfr.get("source_url")) and str(gfr.get("source_url")) != str(L.get("source_url")):
                src.append(link(gfr["source_url"]))
            if has(gfr.get("verbatim_quote")):
                src.append(f'<blockquote class="quote">“{e(gfr["verbatim_quote"])}”</blockquote>')
            elif has(L.get("source_field")):
                src.append(f'<span class="field">{e(L["source_field"])}</span>')
        elif has(L.get("source_field")):
            src.append(f'<span class="field">{e(L["source_field"])}</span>')
        if ss in ("XML_explicit_unit_current_entity_period", "PDF_current_column_and_unit_reconciled",
                  "XML_unit_backfill_rule_R1_or_R2") and flag in ("reported", "reported_zero"):
            q = M_QUALS.get((sym, m))
            if q:
                src.append('<details class="q"><summary>Reconciliation note from the filed PDF</summary>' +
                           "".join(f"<p>{e(x)}</p>" for x in q) + "</details>")
        trans = L.get("transformation")
        out.append(f"""<tr>
<td data-l="Metric"><span class="m-name"><i class="sw sw-{el}"></i>{e(label)}</span><span class="m-used">{e(used)}</span></td>
<td data-l="Value" class="val">{vtxt}</td>
<td data-l="Confidence">{tier}</td>
<td data-l="Source" class="srccell">{''.join(src) or miss('no source recorded')}</td>
<td data-l="Boundary" class="small">{e(L.get('reporting_boundary')) if has(L.get('reporting_boundary')) else miss('–')}</td>
<td data-l="Transformation" class="small">{e(trans) if has(trans) else miss('–')}</td></tr>""")
    # financials
    period = ""
    if has(r.get("accounting_period_start")) and has(r.get("accounting_period_end")):
        period = f'{fdate(r["accounting_period_start"])} to {fdate(r["accounting_period_end"])}'
    rev_src = link(r.get("revenue_source_url")) + (f'<span class="field">{e(r.get("revenue_source_fact"))}</span>' if has(r.get("revenue_source_fact")) else "")
    rev_status = human(r.get("target_fy_revenue_status")) if has(r.get("target_fy_revenue_status")) else "–"
    out.append(f"""<tr class="fin">
<td data-l="Metric"><span class="m-name"><i class="sw sw-fin"></i>Revenue from operations</span><span class="m-used">Denominator of every intensity</span></td>
<td data-l="Value" class="val">{('<span class="num v">' + finr(r.get('revenue_inr_cr')) + '</span>') if isnum(r.get('revenue_inr_cr')) else miss()}</td>
<td data-l="Confidence"><span class="tier"><i class="tq tf"></i>Financial XBRL</span><span class="tier-n">Status: {e(rev_status)}</span></td>
<td data-l="Source" class="srccell">{rev_src}</td>
<td data-l="Boundary" class="small">{e(human(r.get('accounting_boundary'))) if has(r.get('accounting_boundary')) else miss('–')}{('<br>' + period) if period else ''}</td>
<td data-l="Transformation" class="small">{e(r.get('revenue_flag')) if has(r.get('revenue_flag')) else 'Taken as filed, ₹ crore'}</td></tr>""")
    pat_src = link(r.get("pat_source_url")) + (f'<span class="field">{e(r.get("pat_source_fact"))}</span>' if has(r.get("pat_source_fact")) else "")
    out.append(f"""<tr class="fin">
<td data-l="Metric"><span class="m-name"><i class="sw sw-fin"></i>Profit after tax</span><span class="m-used">Profit-basis check rank</span></td>
<td data-l="Value" class="val">{('<span class="num v">' + finr(r.get('pat_inr_crore')) + '</span>') if isnum(r.get('pat_inr_crore')) else miss()}</td>
<td data-l="Confidence"><span class="tier"><i class="tq tf"></i>Financial XBRL</span>{('<span class="tier-n">' + e(human(r.get('profit_flag'))) + '</span>') if has(r.get('profit_flag')) else ''}</td>
<td data-l="Source" class="srccell">{pat_src if has(r.get('pat_source_url')) else miss('no source recorded')}</td>
<td data-l="Boundary" class="small">{e(r.get('pat_boundary')) if has(r.get('pat_boundary')) else miss('–')}</td>
<td data-l="Transformation" class="small">Taken as filed, ₹ crore</td></tr>""")
    if isnum(r.get("ebitda_inr_crore")):
        p = M["pat"].get(sym, {})
        comp_txt = "Nature-cost denominator"
        trans = "EBITDA = profit before tax + finance costs + depreciation and amortisation (includes other income)"
        if p and all(isnum(p.get(k)) for k in ("pbt_used_inr_crore", "finance_costs_inr_crore", "depreciation_inr_crore")):
            tot = p["pbt_used_inr_crore"] + p["finance_costs_inr_crore"] + p["depreciation_inr_crore"]
            if abs(tot - float(r["ebitda_inr_crore"])) < 0.01:
                trans = (f'{fnum(p["pbt_used_inr_crore"])} (profit before tax) + {fnum(p["finance_costs_inr_crore"])} (finance costs) + '
                         f'{fnum(p["depreciation_inr_crore"])} (depreciation) = {fnum(r["ebitda_inr_crore"])}'
                         + (f'; includes other income of {fnum(p["other_income_inr_crore"])}' if isnum(p.get("other_income_inr_crore")) else ""))
        esrc = link(p.get("source_url")) if p and has(p.get("source_url")) else miss("no source recorded")
        out.append(f"""<tr class="fin">
<td data-l="Metric"><span class="m-name"><i class="sw sw-fin"></i>EBITDA</span><span class="m-used">{comp_txt}</span></td>
<td data-l="Value" class="val"><span class="num v">{finr(r.get('ebitda_inr_crore'))}</span></td>
<td data-l="Confidence"><span class="tier"><i class="tq tf"></i>Financial XBRL components</span></td>
<td data-l="Source" class="srccell">{esrc}</td>
<td data-l="Boundary" class="small">{e(p.get('pat_boundary')) if p and has(p.get('pat_boundary')) else miss('–')}</td>
<td data-l="Transformation" class="small">{e(trans)} (₹ crore)</td></tr>""")
    return "".join(out)


M_QUALS = {}


def calc_panel(M, r, gsub):
    sym = r["symbol"]
    rev = r.get("revenue_inr_cr")
    blocks = []
    for el in ["climate", "water", "waste", "air"]:
        info = ELEMENTS[el]
        val = r.get(el)
        steps = []
        # 1. quantity
        comps = []
        for m in info["comps"]:
            L = M["lin"].get((sym, m))
            v = L.get("raw_value") if L else None
            comps.append((m, v))
        lbls = {"scope1_tco2e": "Scope 1", "scope2_tco2e": "Scope 2", "water_withdrawal_m3": "Water withdrawal",
                "waste_generated_tonnes": "Waste generated", "nox_tonnes": "NOx", "sox_tonnes": "SOx", "pm_tonnes": "PM"}
        if isnum(val):
            if len(comps) > 1:
                parts = " + ".join(f'{lbls[m]} {fraw(v) if isnum(v) else "(not reported)"}' for m, v in comps)
                steps.append(f'<li><span class="st">Quantity</span><span class="eq">{parts} = <b class="num">{fraw(val)}</b> {info["unit"]}</span></li>')
            else:
                steps.append(f'<li><span class="st">Quantity</span><span class="eq">{lbls[comps[0][0]]} = <b class="num">{fraw(val)}</b> {info["unit"]}</span></li>')
        else:
            steps.append(f'<li><span class="st">Quantity</span><span class="eq">{miss("not reported")}</span></li>')
        per = r.get(f"{el}_per_rev")
        if isnum(per) and isnum(val) and isnum(rev):
            steps.append(f'<li><span class="st">Intensity</span><span class="eq">{fraw(val)} ÷ ₹{fnum(rev)} crore = <b class="num">{fsig(per, 4)}</b> {info["unit"]} per ₹ crore</span></li>')
        elif isnum(val):
            steps.append(f'<li><span class="st">Intensity</span><span class="eq">{miss("not computed: revenue not matched to the BRSR year")}</span></li>')
        score = r.get(f"{el}_score_rev")
        d = M["deriv"].get((sym, el))
        if isnum(score):
            if d and d["ok"]:
                pos = d["pos"]
                pos_txt = fnum(pos, 1)
                tie = " (tied; ties share the average position)" if pos != int(pos) else ""
                steps.append(f'<li><span class="st">Position</span><span class="eq">{pos_txt} of {d["n"]} companies in the peer group with a scored {info["label"].lower()} value, lowest intensity first{tie}</span></li>')
                steps.append(f'<li><span class="st">Score</span><span class="eq">100 × ({d["n"]} − {pos_txt}) ÷ ({d["n"]} − 1) = <b class="num">{float(score):.1f}</b></span></li>')
            else:
                steps.append(f'<li><span class="st">Score</span><span class="eq">Stored score <b class="num">{float(score):.1f}</b></span></li>')
        else:
            why = "not scored"
            if truthy(r.get(f"{el}_query_flag")):
                why = "not scored: open data query (see below)"
            elif truthy(r.get(f"{el}_zero_flag")) or (el == "climate" and truthy(r.get("climate_component_zero"))):
                why = "not scored: reported zero, to be confirmed by the company"
            elif not isnum(val):
                why = "not scored: not reported"
            elif el not in D_ELS.get(r["score_group"], []):
                why = "not scored in this peer group"
            elif not isnum(per):
                why = "not scored: no intensity"
            else:
                why = "not scored in this peer group (too few reporters or group not scored)"
            steps.append(f'<li><span class="st">Score</span><span class="eq">{miss(why)}</span></li>')
        extra = ""
        if el == "air":
            extra = '<p class="small muted">Air is ranked separately and is not part of the pressure score.</p>'
            if isnum(r.get("rank_air")):
                nair = int(gsub.rank_air.notna().sum())
                extra = f'<p class="small muted">Air is ranked separately and is not part of the pressure score. Air rank: <b>{int(r["rank_air"])} of {nair}</b>.</p>'
        blocks.append(f'<div class="calc-el"><h4><i class="sw sw-{el}"></i>{info["label"]}</h4><ol class="steps">{"".join(steps)}</ol>{extra}</div>')

    # pressure, credit, final
    ps = r.get("pressure_score_rev")
    sc = [r.get(f"{el}_score_rev") for el in CORE]
    if isnum(ps):
        if all(isnum(x) for x in sc) and abs(sum(float(x) for x in sc) / 3 - float(ps)) < 1e-6:
            ptxt = f'({" + ".join(f"{float(x):.1f}" for x in sc)}) ÷ 3 = <b class="num">{float(ps):.1f}</b>'
        else:
            ptxt = f'Stored pressure score <b class="num">{float(ps):.1f}</b>'
    else:
        ptxt = miss("not computed: climate, water and waste must all be scored")
    rp, yp, ep, cp = (r.get("restoration_points"), r.get("recycling_points"), r.get("re_points"), r.get("credit_points"))
    ctier = r.get("credit_tier")
    rest_txt = (f'Tier {e(ctier)} restoration = <b class="num">+{float(rp):.1f}</b>' if has(ctier) and str(ctier) != "none"
                else f'No qualifying restoration = <b class="num">+{float(rp or 0):.1f}</b>')
    gen = r.get("waste"); rec = r.get("waste_recovered_tonnes")
    if isnum(r.get("recycling_share")):
        share = float(r["recycling_share"])
        rtxt = ""
        if isnum(gen) and isnum(rec) and gen > 0 and abs(rec / gen - share) < 1e-6:
            rtxt = f'{fraw(rec)} recovered ÷ {fraw(gen)} generated = {share:.3f}; '
        recy_txt = f'{rtxt}3 × {share:.3f} = <b class="num">+{float(yp):.2f}</b>'
    else:
        recy_txt = f'{miss("no recycling share")} <b class="num">+{float(yp or 0):.2f}</b>'
    if isnum(r.get("re_share")):
        re_txt = f'2 × {float(r["re_share"]):.3f} (renewable share {float(r["re_share"]) * 100:.1f}%) = <b class="num">+{float(ep):.2f}</b>'
    else:
        re_txt = f'{miss("no renewable share")} <b class="num">+{float(ep or 0):.2f}</b>'
    fs = r.get("final_score_rev")
    if isnum(fs) and isnum(ps) and isnum(cp):
        ftxt = f'min(100, {float(ps):.1f} + {float(cp):.2f}) = <b class="num">{float(fs):.1f}</b>'
    elif isnum(fs):
        ftxt = f'<b class="num">{float(fs):.1f}</b>'
    else:
        ftxt = miss("no final score")
    rank_txt = ""
    if isnum(r.get("rank_rev")):
        rank_txt = f'<li><span class="st">Rank</span><span class="eq">Rank <b class="num">{int(r["rank_rev"])} of {int(r["ranked_n_rev"])}</b> by final score in {e(r["score_group"])}; without credit it would rank {int(r["rank_rev_nocredit"]) if isnum(r.get("rank_rev_nocredit")) else "–"}.</span></li>'
    total = f"""<div class="calc-total"><h4>From element scores to rank</h4><ol class="steps">
<li><span class="st">Pressure</span><span class="eq">{ptxt}</span></li>
<li><span class="st">Restoration</span><span class="eq">{rest_txt}</span></li>
<li><span class="st">Recycling</span><span class="eq">{recy_txt}</span></li>
<li><span class="st">Renewables</span><span class="eq">{re_txt}</span></li>
<li><span class="st">Credit</span><span class="eq">{('<b class="num">+' + format(float(cp), '.2f') + '</b> (capped at 10)') if isnum(cp) else miss('–')}</span></li>
<li><span class="st">Final</span><span class="eq">{ftxt}</span></li>{rank_txt}</ol></div>"""
    return f'<div class="calc-grid">{"".join(blocks)}</div>{total}'


D_ELS = {}


def nature_cost_panel(M, r):
    if not isnum(r.get("nature_cost_central")):
        return '<p class="muted">No illustrative nature cost: none of the priced quantities is available.</p>'
    P = M["prices"]
    rows = []

    def price_txt(k, unit):
        return f'₹{fnum(P[k].central, 0)} {unit}'

    def chk(q, k, stored):
        return isnum(q) and isnum(stored) and abs(float(q) * P[k].central / 1e7 - float(stored)) < max(1e-6, 1e-9 * abs(float(stored)))

    if isnum(r.get("cost_ghg")):
        q = r.get("climate")
        if chk(q, "ghg", r.get("cost_ghg")):
            rows.append(("Greenhouse gas (Scope 1 + 2)", f'{fraw(q)} tCO₂e', price_txt("ghg", "per tCO₂e"), r["cost_ghg"]))
        else:
            rows.append(("Greenhouse gas (Scope 1 + 2)", "–", price_txt("ghg", "per tCO₂e"), r["cost_ghg"]))
    if isnum(r.get("cost_water")):
        basis = r.get("water_cost_basis")
        q = r.get("water_consumption_m3") if basis == "consumption" else r.get("water")
        lab = "Water consumed" if basis == "consumption" else "Water withdrawn (fallback: consumption not reported)"
        rows.append((lab, f'{fraw(q)} m³' if chk(q, "water", r.get("cost_water")) else "–", price_txt("water", "per m³"), r["cost_water"]))
    if isnum(r.get("cost_air")):
        parts, tot = [], 0.0
        for k, m, lab in (("nox", "nox_tonnes", "NOx"), ("sox", "sox_tonnes", "SOx"), ("pm", "pm_tonnes", "Particulate matter")):
            q = r.get(m)
            if isnum(q):
                c = float(q) * P[k].central / 1e7
                tot += c
                parts.append((lab, f'{fraw(q)} tonnes', price_txt(k, "per tonne"), c))
        if parts and abs(tot - float(r["cost_air"])) < 1e-6 * max(1, abs(tot)):
            rows.extend(parts)
        else:
            rows.append(("Air pollutants", "–", "–", r["cost_air"]))
    if isnum(r.get("cost_land")):
        q = r.get("dhe_ha")
        rows.append(("Degraded land (DHE)", f'{fraw(q)} DHE-ha' if chk(q, "land_ha", r.get("cost_land")) else "–",
                     price_txt("land_ha", "per DHE-ha per year"), r["cost_land"]))
    rows.append(("Waste", miss("not valued"), miss("no defensible India price"), None))
    trs = "".join(f'<tr><td class="l">{a}</td><td class="r num">{b}</td><td class="r num">{c}</td><td class="r num">{finr(d) if d is not None else miss("–")}</td></tr>' for a, b, c, d in rows)
    ebitda_txt = fpct(r.get("nature_cost_pct_ebitda")) or miss(human(r.get("ebitda_flag")) if has(r.get("ebitda_flag")) else "not available")
    india = ""
    if isnum(r.get("cost_ghg_india_borne")) and isnum(r.get("cost_ghg")) and r["cost_ghg"] > 0:
        india = f'<div class="ch-india"><span class="num">{finr(r["cost_ghg_india_borne"])}</span>borne in India: {100 * r["cost_ghg_india_borne"] / r["cost_ghg"]:.0f}% of the {finr(r["cost_ghg"])} carbon cost</div>'
    return f"""
<div class="illus-banner"><strong>ILLUSTRATIVE — not a liability, not used in rank.</strong> A rough order of magnitude for the cost these reported pressures impose on society, at India-specific central prices (2025 rupees). Do not add across companies: one company’s Scope 2 is another’s Scope 1.</div>
<div class="table-wrap"><table class="data"><thead><tr><th class="l">Component</th><th class="r">Quantity</th><th class="r">Price (central)</th><th class="r">Cost</th></tr></thead>
<tbody>{trs}</tbody><tfoot><tr><td class="l"><strong>Total, central prices</strong></td><td></td><td></td><td class="r num"><strong>{finr(r['nature_cost_central'])}</strong></td></tr></tfoot></table></div>
<div class="cost-head">
  <div class="ch-total"><span class="num">{finr(r['nature_cost_central'])}</span>total at central prices</div>
  {india}
  <div class="ch-pct"><span class="num">{fpct(r.get('nature_cost_pct_revenue')) or '–'}</span>of revenue</div>
</div>
<p class="carbon-line">Carbon is priced at the global social cost; about a quarter of that damage falls in India.</p>
<p class="small muted">Range at low and high prices: {finr(r.get('nature_cost_low')) or '–'} to {finr(r.get('nature_cost_high')) or '–'}. As a share of EBITDA: {ebitda_txt}.</p>
<p class="small muted">Prices: <a href="../{manchor('nature cost', 'Annex')}">methodology, illustrative nature cost</a>. Cost = quantity × price ÷ 1,00,00,000 (rupees to ₹ crore).</p>"""


def land_panel(M, r):
    keys = ["land_owned_ha", "land_leased_ha", "mining_lease_ha", "land_total_ha", "land_scored_total_ha",
            "restored_own_ha", "restored_offsite_ha", "dhe_ha", "net_dhe_ha"]
    any_land = any(isnum(r.get(k)) for k in keys)
    legacy = r.get("legacy_nii_total_land_ha")
    if not any_land and not isnum(legacy):
        return None
    sym = r["symbol"]
    rows = []
    for k, lab in (("land_owned_ha", "Land owned"), ("land_leased_ha", "Land leased"), ("mining_lease_ha", "Mining leases"),
                   ("land_total_ha", "Total land stated"), ("land_scored_total_ha", "Total used for DHE"),
                   ("land_ratio", "Sector degradation ratio (central)"), ("dhe_ha", "Degraded-hectare equivalents (DHE)"),
                   ("restored_own_ha", "Restored on own land"), ("restored_offsite_ha", "Restored off-site (not deducted)"),
                   ("net_dhe_ha", "Net DHE"), ("land_per_rev", "Net DHE per ₹ crore")):
        v = r.get(k)
        if not isnum(v) and k in ("land_ratio", "land_per_rev"):
            continue
        unit = "" if k == "land_ratio" else (" DHE-ha per ₹ crore" if k == "land_per_rev" else " ha")
        rows.append(f'<tr><td class="l">{lab}</td><td class="r num">{(fsig(v, 4) if k == "land_per_rev" else fraw(v)) + unit if isnum(v) else miss("not stated")}</td></tr>')
    calc = ""
    if isnum(r.get("dhe_ha")) and isnum(r.get("land_scored_total_ha")) and isnum(r.get("land_ratio")):
        calc = (f'<p class="eqline">{fraw(r["land_scored_total_ha"])} ha × {r["land_ratio"]} = <b>{fraw(r["dhe_ha"])}</b> DHE-ha'
                + (f'; minus {fraw(r["restored_own_ha"])} ha restored on own land = <b>{fraw(r["net_dhe_ha"])}</b> net DHE-ha' if isnum(r.get("restored_own_ha")) and isnum(r.get("net_dhe_ha")) else "")
                + '</p>')
    q = M["land_q"].get(sym, {})
    qg = M["land_gf"].get(sym, {})
    srcs = []
    url = r.get("land_source_url") if has(r.get("land_source_url")) else q.get("land_source_url")
    if has(url):
        srcs.append(link(url))
    if has(r.get("land_period")):
        srcs.append(f'<span class="field">Period: {e(r["land_period"])}</span>')
    if has(r.get("land_total_basis")):
        srcs.append(f'<span class="field">Basis: {e(r["land_total_basis"])}</span>')
    if has(q.get("land_quote")):
        srcs.append(f'<blockquote class="quote">“{e(q["land_quote"])}”</blockquote>')
    if qg:
        if has(qg.get("source_url")) and qg.get("source_url") != url:
            srcs.append(link(qg["source_url"]))
        if has(qg.get("page")):
            srcs.append(f'<span class="field">{e(qg["page"])}</span>')
        if has(qg.get("verbatim_quote")):
            srcs.append(f'<blockquote class="quote">“{e(qg["verbatim_quote"])}”</blockquote>')
        if has(qg.get("restored_basis")):
            srcs.append(f'<span class="field">Restored-area basis: {e(qg["restored_basis"])}</span>')
    leg = ""
    if isnum(legacy):
        leg = (f'<p class="small muted">Legacy Nature Impact Index land figure: <b>{fraw(legacy)} ha</b>. Unscored reference only: '
               'AI-extracted, medium or low confidence, and a median of 2.5 times the verified figure where both exist. Do not use without checking.</p>')
    body = ""
    if any_land:
        body = f"""<div class="grid-2"><div class="table-wrap"><table class="data"><tbody>{''.join(rows)}</tbody></table></div>
<div class="srccell">{''.join(srcs) or miss('no source recorded')}</div></div>{calc}"""
    else:
        body = '<p class="muted">No verified company-wide land figure was found in FY2025-26 disclosures.</p>'
    return body + leg + '<p class="small muted">Pilot only: no biodiversity rank is published, because no peer group has ten companies with a credible company-wide land total. Net DHE = (land owned + leased, including mining leases) × sector degradation ratio − area restored on own land.</p>'


def build_company(D, M, r, gsub):
    root = "../"
    sym = r["symbol"]
    S = M["S"]
    ranked = isnum(r.get("rank_rev"))
    n_air = int(gsub.rank_air.notna().sum())
    n_comp = int(gsub.rank_comp.notna().sum())
    n_pat = int(gsub.rank_pat.notna().sum())
    is_fin = str(r["score_group"]).startswith("Financial Services")

    # header numbers
    big_rank = (f'<span class="big num">{int(r["rank_rev"])}</span><span class="of">of {int(r["ranked_n_rev"])}</span>'
                if ranked else '<span class="big none">–</span><span class="of">not ranked</span>')
    sec = []
    sec.append(("Final score", fscore(r.get("final_score_rev")) or "–", "out of 100"))
    sec.append(("Pressure score", fscore(r.get("pressure_score_rev")) or "–", "average of climate, water, waste"))
    sec.append(("Credit", ("+" + format(float(r["credit_points"]), ".1f")) if isnum(r.get("credit_points")) else "–", "up to 10 points"))
    sec.append(("Quartile", (str(r["quartile_rev"]).split(" ")[0] if has(r.get("quartile_rev")) else "–"),
                (str(r["quartile_rev"]).partition(" ")[2].strip("()") or "within peer group") if has(r.get("quartile_rev")) else "within peer group"))
    side = []
    side.append(("Air rank", f'{int(r["rank_air"])} of {n_air}' if isnum(r.get("rank_air")) else "–"))
    if n_comp:
        side.append(("Per-unit-output rank", f'{int(r["rank_comp"])} of {n_comp}' if isnum(r.get("rank_comp")) else "–"))
    side.append(("Profit-basis rank", f'{int(r["rank_pat"])} of {int(r["ranked_n_pat"])}' if isnum(r.get("rank_pat")) and isnum(r.get("ranked_n_pat")) else "–"))
    side.append(("Rank without credit", f'{int(r["rank_rev_nocredit"])}' if isnum(r.get("rank_rev_nocredit")) else "–"))
    side.append(("Revenue FY2025-26", finr(r.get("revenue_inr_cr")) or "–"))
    side.append(("Market-cap rank", f'{int(r["mcap_rank"])} of {len(S)}' if isnum(r.get("mcap_rank")) else "–"))
    sec_html = "".join(f'<div class="stat"><span class="stat-l">{a}</span><span class="stat-v num">{b}</span><span class="stat-s">{c}</span></div>' for a, b, c in sec)
    side_html = "".join(f'<div><dt>{a}</dt><dd class="num">{b}</dd></div>' for a, b in side)
    status_line = (f'Ranked within {e(r["score_group"])}' if ranked else e(human(r.get("coverage_flag"))))
    if ranked and has(r.get("coverage_flag")) and str(r["coverage_flag"]) != "ranked":
        status_line = e(human(r["coverage_flag"]))

    cau = caution_of(r)
    caution_html = ""
    if cau and has(r.get("business_model_flag")):
        bmd = str(r["business_model_flag"]).split(" - ")[0].strip()
        cau = cau.replace("business model not like-for-like with peers", f"business model not like-for-like with peers ({bmd})")
    if cau:
        caution_html = (f'<div class="caution" role="note"><span class="caution-mark" aria-hidden="true">†</span><div><strong>Check before naming.</strong> '
                        f'{e(cau[:1].upper() + cau[1:])}. Do not single this company out by name without checking the underlying figures.</div></div>')
    # peers for charts
    peers = {}
    for el in ELEMENTS:
        arr = []
        for p in gsub.itertuples():
            v = getattr(p, f"{el}_per_rev")
            if isnum(v) and v > 0:
                arr.append([p.symbol, float(v), isnum(getattr(p, f"{el}_score_rev")), p.company])
        peers[el] = arr
    me = {el: num(r.get(f"{el}_per_rev")) for el in ELEMENTS}
    wf = dict(climate=num(r.get("climate_score_rev")), water=num(r.get("water_score_rev")), waste=num(r.get("waste_score_rev")),
              pressure=num(r.get("pressure_score_rev")), rest=num(r.get("restoration_points")), recy=num(r.get("recycling_points")),
              re=num(r.get("re_points")), final=num(r.get("final_score_rev")), credit=num(r.get("credit_points")))

    # credits
    ct = r.get("credit_tier")
    cred_rows = []
    if has(ct) and str(ct) != "none":
        area = f'{fraw(r["credit_area_ha"])} ha' if isnum(r.get("credit_area_ha")) else None
        qty = f'{fraw(r["credit_quantity"])} {e(r.get("credit_unit") or "")}' if isnum(r.get("credit_quantity")) else None
        page_txt = f'page {fnum(r["credit_source_page"], 0)}' if isnum(r.get("credit_source_page")) else (e(r.get("credit_source_page")) if has(r.get("credit_source_page")) else "")
        cred_rows.append(f"""<div class="credit-card">
<div class="cc-head"><span class="cc-tier">Restoration, Tier {e(ct)}</span><span class="num cc-pts">+{float(r['restoration_points']):.1f}</span></div>
<p class="cc-proj">{e(r.get('credit_project')) if has(r.get('credit_project')) else miss('project not named')}</p>
<dl class="kv"><div><dt>Quantity</dt><dd>{show(qty, 'not stated')}</dd></div><div><dt>Area</dt><dd>{show(area, 'not stated as area')}</dd></div>
<div><dt>Evidence</dt><dd>{e(human(r.get('credit_evidence_status'))) if has(r.get('credit_evidence_status')) else '–'}</dd></div>
<div><dt>Source</dt><dd>{link(r.get('credit_source_url'))}{(' <span class="field">' + page_txt + '</span>') if page_txt else ''}</dd></div></dl></div>""")
    else:
        extra = ""
        if has(r.get("credit_project")):
            extra = f' A project was reviewed (<em>{e(r["credit_project"])}</em>, {e(human(r.get("credit_evidence_status")))}) but did not qualify.'
        cred_rows.append(f'<div class="credit-card muted-card"><div class="cc-head"><span class="cc-tier">Restoration</span><span class="num cc-pts">+0.0</span></div><p class="small">No quantified restoration in FY2025-26 disclosures met the rule.{extra} Plans, commitments, unfinished work and narrative claims earn no credit.</p></div>')
    rs = r.get("recycling_share")
    cred_rows.append(f"""<div class="credit-card"><div class="cc-head"><span class="cc-tier">Recycling</span><span class="num cc-pts">+{float(r.get('recycling_points') or 0):.2f}</span></div>
<p class="small">3 × (waste recovered ÷ waste generated){(', with ' + format(float(rs) * 100, '.1f') + '% recovered as reported') if isnum(rs) else ': not available'}.</p></div>""")
    rsh = r.get("re_share")
    cred_rows.append(f"""<div class="credit-card"><div class="cc-head"><span class="cc-tier">Renewable electricity</span><span class="num cc-pts">+{float(r.get('re_points') or 0):.2f}</span></div>
<p class="small">2 × renewable share of electricity{(', with ' + format(float(rsh) * 100, '.1f') + '% renewable as reported') if isnum(rsh) else ': not available'}.</p></div>""")

    # flags
    flags = []
    def fl(label, text, kind="info"):
        flags.append(f'<li class="flag flag-{kind}"><span class="fl-l">{e(label)}</span><span>{e(text)}</span></li>')
    if has(r.get("coverage_flag")):
        fl("Coverage", human(r["coverage_flag"]), "info" if ranked else "warn")
    if has(r.get("revenue_flag")):
        fl("Revenue", r["revenue_flag"], "warn")
    if has(r.get("target_fy_revenue_status")) and r["target_fy_revenue_status"] != "verified":
        fl("Revenue status", human(r["target_fy_revenue_status"]), "warn")
    if has(r.get("business_model_flag")):
        fl("Business model", human(r["business_model_flag"]), "warn")
    if has(r.get("financials_flag")):
        fl("Financial company", human(r["financials_flag"]), "warn")
    if has(r.get("profit_flag")) and r["profit_flag"] != "ok":
        fl("Profit", human(r["profit_flag"]), "info")
    if has(r.get("ebitda_flag")):
        fl("EBITDA", human(r["ebitda_flag"]), "info")
    for el in ELEMENTS:
        if truthy(r.get(f"{el}_zero_flag")):
            fl(ELEMENTS[el]["label"], "Reported zero: kept in the data, not scored, to be confirmed by the company", "warn")
        if truthy(r.get(f"{el}_query_flag")):
            fl(ELEMENTS[el]["label"], "Open data query: value excluded from the score pending company confirmation", "warn")
    if truthy(r.get("climate_component_zero")) and not truthy(r.get("climate_zero_flag")):
        fl("Climate", "Scope 1 or Scope 2 component reported as zero: to be confirmed by the company", "warn")
    if r.get("water_cost_basis") == "withdrawal (fallback)":
        fl("Nature cost", "Water priced on withdrawal because consumption is not reported", "info")
    if has(r.get("classification_status")) and str(r["classification_status"]).startswith("inferred"):
        fl("Classification", "Sector assigned by hand from the company's own business disclosures (" + human(r["classification_status"]) + ")", "info")
    q = M["queries"][M["queries"].symbol == sym]
    q_html = ""
    if len(q):
        qr = "".join(f'<tr><td class="l">{e(x.element)}</td><td class="r num">{fraw(x.reported_value)} {e(UNITS.get(x.unit, x.unit))}</td><td class="r num">{fsig(x.intensity_per_rs_cr, 4)}</td><td class="r num">{fsig(x.times_sector_median, 3)}×</td><td class="l small">{e(x.side)}</td><td class="l small">{e(x.status)}</td></tr>' for x in q.itertuples())
        q_html = f'<h3 class="h4">Open data queries</h3><div class="table-wrap"><table class="data"><thead><tr><th class="l">Element</th><th class="r">Reported</th><th class="r">Per ₹ crore</th><th class="r">× peer median</th><th class="l">Why queried</th><th class="l">Status</th></tr></thead><tbody>{qr}</tbody></table></div>'
    land = land_panel(M, r)

    fin_callout = f'<div class="callout callout-fin"><strong>Offices, branches and data centres only.</strong> {e(FIN_CAVEAT.split(". ", 1)[1])}</div>' if is_fin else ""
    bm = f'<div class="callout"><strong>Not a like-for-like peer.</strong> {e(human(r["business_model_flag"]))}.</div>' if has(r.get("business_model_flag")) and not caution_html else ""

    peer_figs = ""
    for el in ["climate", "water", "waste", "air"]:
        if not peers[el]:
            continue
        d = M["deriv"].get((sym, el))
        cap = (f'{fsig(me[el], 4)} {ELEMENTS[el]["unit"]} per ₹ crore'
               + (f', position {fnum(d["pos"], 1)} of {d["n"]} companies with a scored value' if d and d["ok"] else "")) if me[el] else "No value for this company"
        peer_figs += f"""<figure class="peer-fig"><figcaption><strong><i class="sw sw-{el}"></i>{ELEMENTS[el]['label']}</strong><span>{cap}</span></figcaption><div class="chart-box" style="height:96px"><canvas data-peer="{el}"></canvas></div></figure>"""

    toc = [("build", "Score build-up"), ("peers", "Against peers"), ("lineage", "Data lineage"), ("calc", "Calculation"),
           ("credits", "Credits"), ("cost", "Nature cost")]
    if land:
        toc.append(("land", "Land"))
    toc.append(("flags", "Flags"))
    toc_html = "".join(f'<a href="#{a}">{b}</a>' for a, b in toc)

    body = f"""
<section class="page-head company-head"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Overview</a><a href="../sector/{r['gslug']}.html">{e(r['score_group'])}</a><span>{e(sym)}</span></nav>
  <div class="ch-grid">
    <div class="ch-main">
      <h1>{e(r['company'])}</h1>
      <p class="ch-meta"><span class="sym">{e(sym)}</span><a href="../sector/{r['gslug']}.html">{e(r['score_group'])}</a>{status_pill(r['status_key'], r['status_label'], STATUS_HELP.get(r['status_key']))}</p>
      <p class="ch-status">{status_line}</p>
      {caution_html}
      <div class="stats">{sec_html}</div>
    </div>
    <div class="ch-rank">
      <span class="rank-l">Rank in peer group</span>
      <div class="rank-v">{big_rank}</div>
      <dl class="side">{side_html}</dl>
    </div>
  </div>
  {fin_callout}{bm}
</div>
<nav class="toc wrap" aria-label="On this page">{toc_html}</nav>
</section>

<section class="section" id="build"><div class="wrap">
  <div class="section-head"><h2>Score build-up</h2><p>The three element scores average into the pressure score; the credits are then added to give the final score, capped at 100. Air is ranked separately and is not included.</p></div>
  <figure class="chart-card wide"><div class="chart-box" style="height:300px"><canvas id="waterfall"></canvas></div></figure>
</div></section>

<section class="section" id="peers"><div class="wrap">
  <div class="section-head"><h2>Against peers</h2><p>Intensity per ₹ crore of revenue for every company in {e(r['score_group'])} with a value. {e(r['company'])} is the large green dot; peers are grey, hollow where the value is not scored. Logarithmic axis where values span more than a hundredfold.</p></div>
  <div class="peer-grid">{peer_figs or '<p class="muted">No intensity data for this peer group.</p>'}</div>
</div></section>

<section class="section" id="lineage"><div class="wrap">
  <div class="section-head"><h2>Data lineage</h2><p>Every input, exactly as used: the value and unit, how confident we are in it, where it came from, the reporting boundary and what was done to it. Values are FY2025-26 (1 April 2025 to 31 March 2026). Missing stays missing: nothing is estimated.</p></div>
  <div class="table-wrap lineage-wrap"><table class="data lineage"><thead><tr><th class="l">Metric</th><th class="l">Value</th><th class="l">Confidence</th><th class="l">Source</th><th class="l">Boundary</th><th class="l">Transformation</th></tr></thead>
  <tbody>{lineage_rows(M, r)}</tbody></table></div>
</div></section>

<section class="section" id="calc"><div class="wrap">
  <div class="section-head"><h2>Calculation, step by step</h2><p>Worked with this company’s own numbers. Intensity = value ÷ revenue. Element score = 100 × (n − position) ÷ (n − 1), where n is the number of peers with a scored value and position 1 is the lowest intensity. Each reproduced score is checked against the published one.</p></div>
  {calc_panel(M, r, gsub)}
</div></section>

<section class="section" id="credits"><div class="wrap">
  <div class="section-head"><h2>Credit for positive action</h2><p>Up to 10 points in total: restoration (+5 for Tier A, +2 for Tier B), recycling (0–3) and renewable electricity (0–2). Credit recognises effort; it does not offset pressure.</p></div>
  <div class="credit-grid">{''.join(cred_rows)}</div>
</div></section>

<section class="section" id="cost"><div class="wrap">
  <div class="section-head"><h2>Illustrative nature cost</h2></div>
  {nature_cost_panel(M, r)}
</div></section>
{('<section class="section" id="land"><div class="wrap"><div class="section-head"><h2>Land and degraded-hectare equivalents</h2></div>' + land + '</div></section>') if land else ''}
<section class="section" id="flags"><div class="wrap">
  <div class="section-head"><h2>Flags and data queries</h2></div>
  <ul class="flags">{''.join(flags) or '<li class="flag"><span>No flags.</span></li>'}</ul>
  {q_html}
  <p class="small muted">Sector classification: {e(r.get('classification_status'))}{(' (' + e(r.get('classification_match_method')) + ')') if has(r.get('classification_match_method')) else ''}. ISIN {e(r.get('isin'))}. Companies can send corrections with a page reference to a published document; see <a href="../{manchor('Correct')}">the methodology</a>.</p>
</div></section>
"""
    data = dict(sym=sym, name=r["company"], peers=peers, me=me, wf=wf)
    write(f"company/{r['slug']}.html", page(f"{r['company']} ({sym}) | CLBI v1.1 draft", body, root, "", charts=True,
                                            data=data, init="CLBI.company();",
                                            desc=f"CLBI v1.1 draft deep dive for {r['company']}: scores, every data point and its source."))


# ----------------------------------------------------------------------------------------------- methodology
def build_methodology(D):
    text = D["method_md"]
    m = re.match(r"\s*# (.+)\n", text)
    title = m.group(1).strip() if m else "Methodology"
    if m:
        text = text[m.end():]
    html_body = md(text)
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html_body)
    toc = "".join(f'<a href="#{a}">{b}</a>' for a, b in heads)
    # wrap tables for scrolling
    html_body = html_body.replace("<table>", '<div class="table-wrap"><table class="data">').replace("</table>", "</table></div>")
    body = f"""
<section class="page-head"><div class="wrap"><h1>{e(title)}</h1><p class="lead">The methodology note, reproduced in full from its source. Download the <a href="data/CLBI_v1.1_Methodology_Note.md">Markdown version</a>.</p></div></section>
<section class="section tight"><div class="wrap doc-grid">
  <nav class="doc-toc" aria-label="Sections">{toc}</nav>
  <article class="prose doc">{html_body}</article>
</div></section>"""
    write("methodology.html", page("Methodology | CLBI v1.1 draft", body, "", "methodology"))


# ----------------------------------------------------------------------------------------------- downloads
DOWNLOADS = [
    ("outputs", "CLBI_v1_scores_all500.csv", "Scores, ranks and every intermediate number, one row per company."),
    ("outputs", "CLBI_v1_company_data.csv", "Data lineage: 11 metrics per company with value, unit, confidence tier, source URL, XBRL field or page, boundary and transformation."),
    ("outputs", "CLBI_v1_data_queries.csv", "Values excluded pending company confirmation, with the reason."),
    ("outputs", "CLBI_v1_robustness.csv", "Rank-stability checks for each peer group."),
    ("outputs", "CLBI_v1_credit_movers.csv", "Companies whose rank changes because of credit."),
    ("outputs", "build_stats.json", "Build parameters, counts and input fingerprints (SHA-256)."),
    ("inputs", "gapfill_values.csv", "Values filled from company reports, with URL, page and verbatim quote."),
    ("inputs", "land_values.csv", "Company-wide land figures with source and quote."),
    ("inputs", "comparator_values.csv", "Cement production and power generation, with source and quote."),
    ("inputs", "prices.csv", "India-specific prices used for the illustrative nature cost."),
    ("inputs", "land_ratios.csv", "Sector degradation ratios used for degraded-hectare equivalents."),
    ("root", "CLBI_v1.1_Methodology_Note.md", "The methodology note (Markdown)."),
]
DROP_COLS = ["codex_model_value_NOT_USED", "codex_evidence_tier"]
DELIVERABLES_DIR = BASE / "deliverables"
DELIVERABLES = [  # (file, label, description)
    ("CLBI_v1.1_Dataset.xlsx", "Dataset (Excel)", "The full workbook: one sheet per peer group, the data sheet with every source, and the annexes."),
    ("CLBI_v1.1_Methodology_Note.pdf", "Methodology note (PDF)", "How CLBI works, in print-ready form."),
    ("CLBI_v1.1_Methodology_Note.docx", "Methodology note (Word)", "The same note as an editable Word document."),
    ("CLBI_v1.1_Presentation.pdf", "Presentation (PDF)", "The CLBI v1.1 presentation."),
    ("CLBI_v1.1_Presentation.html", "Presentation (web)", "The presentation as a single web page, to open in a browser."),
]
SIZE_LIMIT = 100 * 1024 * 1024
SITE_RESERVE = 40 * 1024 * 1024


def copy_deliverables():
    """Copy the deliverables into docs/downloads/, keeping docs/ under SIZE_LIMIT. Returns the list copied."""
    out = []
    dd = OUT / "downloads"
    used = SITE_RESERVE  # room kept for the generated pages and data files, which are written afterwards
    for fn, label, desc in DELIVERABLES:
        src = DELIVERABLES_DIR / fn
        if not src.exists():
            print(f"  deliverable missing, skipped: {fn}")
            continue
        size = src.stat().st_size
        if used + size > SIZE_LIMIT:
            print(f"  deliverable skipped to keep docs/ under {SIZE_LIMIT // 2**20} MB: {fn}")
            continue
        dd.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dd / fn)
        used += size
        out.append((fn, label, desc, size))
    return out


def fsize(size):
    return f"{size / 1024:,.0f} KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:,.1f} MB"


DELIV_COPIED = []


def build_downloads(D):
    dd = OUT / "data"
    dd.mkdir(parents=True, exist_ok=True)
    items = []
    for where, fn, desc in DOWNLOADS:
        src = {"outputs": OUTPUTS, "inputs": INPUTS, "root": BASE}[where] / fn
        if not src.exists():
            continue
        dst = dd / fn
        note = ""
        if fn == "CLBI_v1_company_data.csv":
            df = pd.read_csv(src)
            dropped = [c for c in DROP_COLS if c in df.columns]
            df.drop(columns=dropped).to_csv(dst, index=False)
            if dropped:
                note = " The web copy omits the internal columns " + ", ".join(f"<code>{c}</code>" for c in dropped) + ", which hold modelled values and model tiers that CLBI does not use."
        else:
            shutil.copyfile(src, dst)
        size = dst.stat().st_size
        rows = ""
        if fn.endswith(".csv"):
            rows = f"{fnum(len(pd.read_csv(dst)), 0)} rows, "
        sz = fsize(size)
        items.append(f'<li><a class="dl" href="data/{e(fn)}" download><span class="dl-name">{e(fn)}</span><span class="dl-meta num">{rows}{sz}</span></a><p>{e(desc)}{note}</p></li>')
    deliv_html = ""
    if DELIV_COPIED:
        cards = "".join(
            f'<a class="dcard" href="downloads/{e(fn)}"{" download" if not fn.endswith(".html") else ""}>'
            f'<span class="dc-ext">{e(fn.rsplit(".", 1)[1].upper())}</span><span class="dc-name">{e(label)}</span>'
            f'<span class="dc-desc">{e(desc)}</span><span class="dc-meta num"><span class="dc-fn">{e(fn)}</span><span class="dc-sz">{fsize(size)}</span></span></a>'
            for fn, label, desc, size in DELIV_COPIED)
        deliv_html = f'<h2 class="h3 sub-h">Reports and dataset</h2><div class="dcards">{cards}</div>'
    body = f"""
<section class="page-head"><div class="wrap"><h1>Downloads</h1><p class="lead">The dataset, the methodology note, the presentation, and the data behind every page of this site.</p></div></section>
<section class="section tight"><div class="wrap narrow">
{deliv_html}
<h2 class="h3 sub-h">Data files</h2>
<p class="muted sub-p">Plain CSV and JSON, regenerated with each build of the site.</p>
<ul class="downloads">{''.join(items)}</ul>
</div></section>"""
    write("downloads.html", page("Downloads | CLBI v1.1 draft", body, "", "downloads"))


# ----------------------------------------------------------------------------------------------- data quality
def build_dq(D, M):
    L = D["lineage"]
    withv = L[L.raw_value.notna()]
    core = withv[withv.metric.isin(CORE_METRICS)]
    trs = []
    for code, (tn, lab, desc) in TIERS.items():
        a = int((withv.source_status == code).sum())
        c = int((core.source_status == code).sum())
        trs.append(f'<tr><td class="l"><span class="tier"><i class="tq t{tn}"></i>Tier {tn}</span></td><td class="l"><strong>{e(lab)}</strong><p class="small muted">{e(desc)}</p><code class="small">{e(code)}</code></td>'
                   f'<td class="r num">{fnum(a, 0)}</td><td class="r num">{100 * c / len(core):.1f}%</td></tr>')
    fl = L.flag.value_counts()
    ftr = "".join(f'<tr><td class="l">{e(NO_VALUE.get(k, human(k)))}</td><td class="l"><code class="small">{e(k)}</code></td><td class="r num">{fnum(v, 0)}</td></tr>' for k, v in fl.items())
    Q = D["queries"]
    S = M["S"].set_index("symbol")
    def qrows(Qs):
        return "".join(
        f'<tr><td class="l">{e(x.sector)}</td><td class="l">' + (f'<a href="company/{S.loc[x.symbol, "slug"]}.html">{e(x.company)}</a>' if x.symbol in S.index else e(x.company)) +
        f'</td><td class="l">{e(x.element)}</td><td class="r num">{fraw(x.reported_value)} {e(UNITS.get(x.unit, x.unit))}</td><td class="r num">{finr(x.revenue_inr_cr)}</td><td class="r num">{fsig(x.intensity_per_rs_cr, 4)}</td><td class="r num">{(fsig(x.times_sector_median, 3) if isnum(x.times_sector_median) and float(x.times_sector_median) != 0 else "&lt;0.0001")}×</td><td class="l small q-side">{e(x.side)}</td><td class="l small q-status">{e(x.status)}</td></tr>'
        for x in Qs.itertuples())
    prm = D["stats"].get("params", {})
    tariff_txt = (f' (at ₹{prm["scope2_tariff_inr_per_kwh"]:g} per kWh and {prm["scope2_grid_ef"]:g} tCO₂ per MWh)'
                  if "scope2_tariff_inr_per_kwh" in prm and "scope2_grid_ef" in prm else "")
    imp_mask = Q.side.astype(str).str.startswith("Scope 2 implies")
    Q_ext, Q_imp = Q[~imp_mask], Q[imp_mask]
    qhead = '<thead><tr><th class="l" data-sort>Sector</th><th class="l" data-sort>Company</th><th class="l" data-sort>Element</th><th class="r">Reported</th><th class="r">Revenue</th><th class="r">Per ₹ crore</th><th class="r">× median</th><th class="l">Why queried</th><th class="l">Status</th></tr></thead>'
    R = D["robust"]
    rcols = [c for c in R.columns]
    rhead = "".join(f'<th class="{"l" if c in ("sector", "elements_scored") else "r"}">{e(human(c))}</th>' for c in rcols)
    rtr = "".join("<tr>" + "".join(
        (f'<td class="l">{e(v)}</td>' if c in ("sector", "elements_scored") else f'<td class="r num">{(f"{float(v):.3f}" if isnum(v) and not float(v).is_integer() else (fnum(v, 0) if isnum(v) else "–"))}</td>')
        for c, v in zip(rcols, row)) + "</tr>" for row in R.itertuples(index=False))
    cf = D["stats"].get("coverage_flags", {})
    cftr = "".join(f'<tr><td class="l">{e(human(k))}</td><td class="r num">{v}</td></tr>' for k, v in cf.items())
    body = f"""
<section class="page-head"><div class="wrap"><h1>Data quality</h1><p class="lead">How confident we are in each value, which values are under query, and how stable the ranks are to changes in method.</p></div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Confidence tiers</h2><p>Every reported value carries one of five tiers. The share column is for the {fnum(len(core), 0)} core values with a recorded figure (Scope 1, Scope 2, water withdrawal, waste generated).</p></div>
  <div class="table-wrap"><table class="data"><thead><tr><th class="l">Tier</th><th class="l">Meaning</th><th class="r">Values, all metrics</th><th class="r">Share of core values</th></tr></thead><tbody>{''.join(trs)}</tbody></table></div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Value flags across the lineage table</h2><p>{fnum(len(L), 0)} metric rows ({L.symbol.nunique()} companies × {L.metric.nunique()} metrics).</p></div>
  <div class="table-wrap"><table class="data"><thead><tr><th class="l">Meaning</th><th class="l">Flag</th><th class="r">Rows</th></tr></thead><tbody>{ftr}</tbody></table></div>
</div></section>
<section class="section" id="queries"><div class="wrap">
  <div class="section-head"><h2>Data queries</h2><p>{len(Q)} values are not scored, and the company’s rank is withheld while a query on a ranked element is open. A value the company confirms is restored.</p></div>
  <h3 class="h3 sub-h">Extreme values <span class="count num">{len(Q_ext)}</span></h3>
  <p class="muted sub-p">Intensity more than 300 times above or below the peer-group median. Usually a unit slip (kilograms entered as tonnes) or a boundary problem (head office only).</p>
  <div class="table-wrap"><table class="data sortable compact">{qhead}<tbody>{qrows(Q_ext) or '<tr><td colspan="9" class="l muted">None.</td></tr>'}</tbody></table></div>
  <h3 class="h3 sub-h">Physically impossible (Scope 2) <span class="count num">{len(Q_imp)}</span></h3>
  <p class="muted sub-p">The Scope 2 figure would need more grid electricity than the company’s whole revenue could buy {tariff_txt}.</p>
  <div class="table-wrap"><table class="data sortable compact">{qhead}<tbody>{qrows(Q_imp) or '<tr><td colspan="9" class="l muted">None.</td></tr>'}</tbody></table></div>
</div></section>
<section class="section" id="robustness"><div class="wrap">
  <div class="section-head"><h2>Robustness</h2><p>Spearman rank correlations (ρ) within each peer group: with and without credit, revenue versus profit basis, water withdrawal versus consumption, and the lowest ρ when any one element is left out. Values near 1 mean the rank order barely changes.</p></div>
  <div class="table-wrap"><table class="data compact"><thead><tr>{rhead}</tr></thead><tbody>{rtr}</tbody></table></div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Coverage status, all companies</h2></div>
  <div class="table-wrap"><table class="data"><thead><tr><th class="l">Status</th><th class="r">Companies</th></tr></thead><tbody>{cftr}</tbody></table></div>
</div></section>"""
    write("data-quality.html", page("Data quality | CLBI v1.1 draft", body, "", "dq", init=""))


# ----------------------------------------------------------------------------------------------- main
def main():
    global M_QUALS, D_ELS
    D = load()
    M_QUALS = D["quals"]
    D_ELS = D["stats"].get("elements_scored_by_sector", {})
    M = build_model(D)
    METHOD_IDS[:] = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', md(D["method_md"]))
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in ASSETS_SRC.iterdir():
        if f.is_file():
            shutil.copyfile(f, OUT / "assets" / f.name)
    write("robots.txt", "User-agent: *\nDisallow: /\n")
    DELIV_COPIED[:] = copy_deliverables()
    write(".nojekyll", "")
    write_companies_js(M)
    build_home(D, M)
    fix_home_tiles()
    build_sectors_index(D, M)
    build_rankings(D, M)
    S = M["S"]
    for g, sub in S.groupby("score_group"):
        build_sector(D, M, g, sub)
    groups = {g: sub for g, sub in S.groupby("score_group")}
    n_mis = 0
    for r in S.to_dict("records"):
        build_company(D, M, r, groups[r["score_group"]])
    n_mis = sum(1 for v in M["deriv"].values() if v and not v["ok"])
    build_methodology(D)
    build_downloads(D)
    build_dq(D, M)
    pages = sum(1 for p in OUT.rglob("*.html") if "downloads" not in p.parts)
    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"  docs/ size {total / 2**20:.1f} MB; deliverables copied: {len(DELIV_COPIED)}")
    if total > SIZE_LIMIT:
        print(f"  WARNING: docs/ is larger than {SIZE_LIMIT // 2**20} MB")
    print(f"CLBI site built: {pages} HTML pages in {OUT}")
    print(f"  companies {len(S)}, peer groups {S.score_group.nunique()}, ranked {int(S.rank_rev.notna().sum())}")
    print(f"  element-score derivations not matching stored score: {n_mis} (stored score shown alone where so)")
    print(f"  PDF reconciliation notes loaded: {len(M_QUALS)} ({'found' if PVA.exists() else 'file not found, skipped'})")


if __name__ == "__main__":
    main()
