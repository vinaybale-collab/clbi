# Corporate Land and Biodiversity Index (CLBI) v1.1: website

A draft for review by Landstack, prepared by Urvara.Life. It is not for publication yet, and crawlers are blocked (`robots.txt`, `noindex`).

The site is static HTML in `docs/`, served by GitHub Pages: Settings → Pages → Deploy from a branch → `main` / `/docs`.

The site covers India's 500 largest NSE-listed companies, ranked within their sector on reported greenhouse gases, water and waste per ₹ of revenue for FY2025-26. Each company page traces every value to its filing or report: source link, field or page, verbatim quote and confidence tier. It also shows the step-by-step calculation.

To regenerate the site, edit the CLBI build outputs and then run `python3 generator/build_site.py`. The generator expects the CLBI working folder.

Downloads, available on the site's Downloads page:
- the dataset (Excel);
- the methodology note;
- the presentation.
