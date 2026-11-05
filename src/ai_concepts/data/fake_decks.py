"""Generate fake investment committee (IC) deck data for topics 04+. All companies and numbers are made up.

Writes (project root):
    data/fake_decks.jsonl      one line per slide, shaped like the real deck JSONL
    data/fake_decks_new.jsonl  one extra deck (Surf portfolio review) used to demo weekly updates
    data/fake_metrics.jsonl    one line per metric per deck: what an extraction step (topic 11) would pull out

    uv run python src/ai_concepts/data/fake_decks.py

Placeholder fields (project, company, sector, deck_stage, deck_date) stand in for whatever the real data carries.
"""

import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "src/ai_concepts/logs"

log = logging.getLogger("fake_decks")

# Each deal: who it is, how its decks phrase EBITDA, and the numbers at each stage.
# ebitda_label varies on purpose (acronym / adjusted / spelled out / synonym), as seen in 03.
DEALS = [
    {
        "project": "Surf", "company": "Tidewater Waste Services", "sector": "Waste", "subsector": "solid waste collection",
        "region": "Southeast US", "ebitda_label": "Adj. EBITDA", "margin": 0.24, "growth": 0.07,
        "screening": {"date": "2024-03-12", "ebitda": 38.0},
        "final_ic": {"date": "2024-06-20", "ebitda": 41.5, "multiple": 12.0, "moic": 2.6, "irr": 21, "decision": "Approved"},
        "portfolio": {"date": "2025-09-15", "ebitda": 44.2},
        "overview": "Vertically integrated collection and transfer business serving 180k residential and 22k commercial customers across Georgia and the Carolinas; owns 4 transfer stations and 1 landfill.",
        "thesis": ["Route density: tuck-in acquisitions in existing markets lift margins 300-400bps.",
                   "Landfill ownership gives internalization and pricing power as regional capacity tightens.",
                   "Fragmented market with 40+ sub-scale haulers to acquire at 5-7x."],
        "market": "Southeast solid waste volumes growing 3-4% a year on population migration; pricing up CPI+1-2% annually.",
        "risks": ["Fuel cost spikes (mitigant: fuel surcharge pass-through on 85% of contracts).",
                  "Landfill permit expansion delayed (mitigant: 14 years remaining airspace today).",
                  "Integration risk on M&A pipeline."],
        "diligence": "QoE confirmed run-rate Adj. EBITDA; $2.1M of add-backs accepted, $0.8M rejected. Customer churn 6% a year, in line with peers.",
    },
    {
        "project": "Granite", "company": "Keystone Recycling", "sector": "Waste", "subsector": "recycling / materials recovery",
        "region": "Mid-Atlantic", "ebitda_label": "earnings before interest, taxes, depreciation and amortization", "margin": 0.18, "growth": 0.05,
        "screening": {"date": "2022-01-18", "ebitda": 22.0},
        "final_ic": {"date": "2022-04-07", "ebitda": 24.3, "multiple": 11.0, "moic": 2.3, "irr": 18, "decision": "Approved"},
        "overview": "Operates 3 materials recovery facilities processing 450k tons a year of single-stream recyclables for municipal contracts.",
        "thesis": ["Long-term municipal contracts (avg 7 years) with tipping fees indexed to inflation.",
                   "Optical sorting upgrade cuts labor cost per ton by ~20%.",
                   "Commodity floor pricing on 60% of volume limits downside."],
        "market": "Recycling volumes stable; commodity prices for OCC and plastics volatile, swinging +/-30% year to year.",
        "risks": ["Commodity price exposure on 40% of volume.",
                  "Contamination rates rising in single-stream collection.",
                  "Capex for sorting upgrades could run over budget."],
        "diligence": "Commodity sensitivity: every 10% drop in blended commodity price cuts earnings before interest, taxes, depreciation and amortization by about $1.4M.",
    },
    {
        "project": "Ember", "company": "Cinder Renewables", "sector": "Waste", "subsector": "landfill gas to energy",
        "region": "Midwest", "ebitda_label": "operating profit before D&A", "margin": 0.42, "growth": 0.03,
        "screening": {"date": "2021-05-03", "ebitda": 30.5},
        "final_ic": {"date": "2021-08-26", "ebitda": 29.0, "multiple": 11.0, "moic": 2.0, "irr": 15, "decision": "Approved with conditions"},
        "overview": "Owns and operates 11 landfill gas-to-energy plants under long-term gas rights agreements with landfill owners.",
        "thesis": ["Contracted gas rights averaging 15 years remaining.",
                   "Renewable natural gas conversions earn RIN credits on top of power sales.",
                   "Low maintenance capex once plants are built."],
        "market": "Demand for renewable natural gas rising with state clean fuel standards; RIN credit prices volatile.",
        "risks": ["RIN credit price volatility drives 35% of operating profit before D&A.",
                  "Gas flow declines as landfills close.",
                  "Regulatory change to renewable fuel standards."],
        "diligence": "Gas flow modeling by third-party engineer cut year 3 volumes by 6%, reducing operating profit before D&A from the screening estimate.",
    },
    {
        "project": "Harbor", "company": "BlueCove Medical Waste", "sector": "Waste", "subsector": "medical waste",
        "region": "Northeast US", "ebitda_label": "EBITDA", "margin": 0.27, "growth": 0.09,
        "screening": {"date": "2023-02-14", "ebitda": 15.8},
        "final_ic": {"date": "2023-05-30", "ebitda": 17.1, "multiple": 13.0, "moic": 2.8, "irr": 23, "decision": "Approved"},
        "overview": "Collects and treats regulated medical waste for 9,000 hospitals, clinics and dental offices; operates 2 autoclave treatment facilities.",
        "thesis": ["Recurring, regulation-driven demand with low customer churn (4%).",
                   "Small-quantity generators (dental, vet) are underserved by national players.",
                   "Add-on acquisitions of route-based competitors at 6-8x."],
        "market": "Regulated medical waste market growing 5-6% a year with outpatient care expansion.",
        "risks": ["Treatment facility outage (mitigant: overflow agreement with third party).",
                  "Pricing pressure from national players on large hospital contracts.",
                  "Driver shortages."],
        "diligence": "Customer interviews showed high switching costs; 2 of top 10 customers renegotiated pricing down 5%.",
    },
    {
        "project": "Falcon", "company": "Northwind Logistics", "sector": "Transportation", "subsector": "truckload freight",
        "region": "Midwest", "ebitda_label": "EBITDA", "margin": 0.12, "growth": 0.04,
        "screening": {"date": "2023-09-05", "ebitda": 49.0},
        "final_ic": {"date": "2023-11-16", "ebitda": 52.0, "multiple": 8.5, "moic": 2.1, "irr": 17, "decision": "Approved"},
        "overview": "Asset-based truckload carrier with 1,400 tractors focused on dedicated contracts for retail and food distribution.",
        "thesis": ["Dedicated contracts (65% of revenue) are less cyclical than spot freight.",
                   "Fleet age reduction lowers maintenance and fuel cost.",
                   "Freight cycle at a trough at entry."],
        "market": "Truckload spot rates down 20% from peak; contract rates stabilizing.",
        "risks": ["Freight recession extends.", "Driver wage inflation.", "Customer concentration: top 3 are 35% of revenue."],
        "diligence": "Customer contracts reviewed; average remaining term 2.5 years with fuel pass-through.",
    },
    {
        "project": "Juniper", "company": "Halcyon Health", "sector": "Healthcare", "subsector": "outpatient clinics",
        "region": "Texas", "ebitda_label": "Adj. EBITDA", "margin": 0.16, "growth": 0.11,
        "screening": {"date": "2022-08-22", "ebitda": 26.0},
        "final_ic": {"date": "2022-10-27", "ebitda": 27.4, "multiple": 14.0, "moic": 2.5, "irr": 20, "decision": "Approved"},
        "overview": "Operates 64 outpatient physical therapy and primary care clinics across Texas.",
        "thesis": ["De novo clinics break even in 18 months.", "Payer mix shifting to commercial.", "Platform for regional roll-up."],
        "market": "Outpatient care growing 6-8% a year as care shifts out of hospitals.",
        "risks": ["Reimbursement cuts.", "Clinician hiring.", "De novo ramp slower than plan."],
        "diligence": "Same-clinic visit growth of 7% verified; 3 underperforming clinics flagged for closure.",
    },
    {
        "project": "Atlas", "company": "Kestrel Software", "sector": "Software", "subsector": "vertical SaaS for field services",
        "region": "US", "ebitda_label": "EBITDA", "margin": 0.31, "growth": 0.22,
        "screening": {"date": "2024-01-10", "ebitda": 18.5},
        "final_ic": {"date": "2024-03-21", "ebitda": 19.2, "multiple": 22.0, "moic": 3.0, "irr": 25, "decision": "Declined"},
        "overview": "Scheduling and invoicing software for HVAC, plumbing and waste haulers; 6,500 customers.",
        "thesis": ["Net revenue retention of 112%.", "Payments attach rate rising.", "Underpenetrated in waste hauling vertical."],
        "market": "Field service software market growing 12% a year; competitive with two well-funded rivals.",
        "risks": ["Valuation: 22x EBITDA leaves little room for error.", "Competition.", "Payments revenue is volume-sensitive."],
        "diligence": "Cohort analysis showed SMB churn of 14% a year, higher than management's 9%. Committee declined at the price.",
    },
    {
        "project": "Quarry", "company": "Ironclad Aggregates", "sector": "Building materials", "subsector": "aggregates and quarries",
        "region": "Mountain West", "ebitda_label": "EBITDA", "margin": 0.29, "growth": 0.05,
        "screening": {"date": "2021-10-04", "ebitda": 61.0},
        "final_ic": {"date": "2021-12-09", "ebitda": 58.4, "multiple": 9.5, "moic": 2.2, "irr": 17, "decision": "Approved"},
        "overview": "Owns 12 quarries and 5 ready-mix plants with 600 million tons of permitted reserves.",
        "thesis": ["Permitted reserves are a local moat; new permits take 5-10 years.",
                   "Infrastructure spending supports volumes.",
                   "Pricing up mid-single digits a year."],
        "market": "Aggregates demand tied to infrastructure and housing starts in fast-growing Mountain West metros.",
        "risks": ["Housing slowdown.", "Diesel and energy costs.", "Permit renewal on 2 quarries."],
        "diligence": "Reserve audit confirmed 600M tons; one quarry's permit renewal pushed out 18 months, cutting EBITDA estimate.",
    },
]


def periods(deck_date: str) -> list[str]:
    """Three period labels ending at the deck date, e.g. FY2022, FY2023, LTM Mar-24."""
    year, month = int(deck_date[:4]), int(deck_date[5:7])
    mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][month - 1]
    return [f"FY{year - 2}", f"FY{year - 1}", f"LTM {mon}-{str(year)[2:]}"]


def fin_table(deal: dict, ebitda: float, deck_date: str) -> tuple[str, list[str], list[float], list[float]]:
    """Flattened financials table with labels intact (see 03 section 6b)."""
    p = periods(deck_date)
    e = [round(ebitda / (1 + deal["growth"]) ** k, 1) for k in (2, 1, 0)]
    r = [round(x / deal["margin"], 1) for x in e]
    label = deal["ebitda_label"]
    short = label if len(label) < 20 else "Earnings before interest, taxes, D&A"
    text = (f"($M) | {p[0]} | {p[1]} | {p[2]}\n"
            f"Revenue | {r[0]} | {r[1]} | {r[2]}\n"
            f"{short} | {e[0]} | {e[1]} | {e[2]}\n"
            f"Margin | {deal['margin']:.0%} | {deal['margin']:.0%} | {deal['margin']:.0%}")
    return text, p, r, e


def deck_slides(deal: dict, stage: str) -> tuple[list[dict], list[dict]]:
    """Return (slides, metrics) for one deck of one deal."""
    code = {"Screening": "scr", "Final IC": "ic", "Portfolio Review": "pr"}[stage]
    key = {"Screening": "screening", "Final IC": "final_ic", "Portfolio Review": "portfolio"}[stage]
    info = deal[key]
    deck_id = f"{deal['project'].lower()}-{code}"
    label = deal["ebitda_label"]
    table, p, rev, ebitda = fin_table(deal, info["ebitda"], info["date"])

    if stage == "Screening":
        pages = [
            ("Executive Summary", "exec_summary",
             f"Project {deal['project']}: opportunity to acquire {deal['company']}, a {deal['subsector']} business in the {deal['region']}. "
             f"Preliminary {label} of ${info['ebitda']}M ({p[2]}). Recommend proceeding to diligence."),
            ("Company Overview", "overview", deal["overview"]),
            ("Market", "market", deal["market"]),
            ("Preliminary Financials", "financials", "Management figures, not yet diligenced.\n" + table),
            ("Key Diligence Questions", "risks", "Questions to resolve in diligence: " + " ".join(deal["risks"])),
        ]
    elif stage == "Final IC":
        ev = round(info["ebitda"] * info["multiple"], 1)
        pages = [
            ("Executive Summary and Recommendation", "exec_summary",
             f"Project {deal['project']} ({deal['company']}). Recommendation: {info['decision']}. "
             f"Enterprise value ${ev}M, {info['multiple']}x {p[2]} {label} of ${info['ebitda']}M."),
            ("Investment Thesis", "thesis", " ".join(f"{i}. {t}" for i, t in enumerate(deal["thesis"], 1))),
            ("Market", "market", deal["market"]),
            ("Financial Summary", "financials", "Diligenced figures.\n" + table),
            ("Valuation and Returns", "valuation",
             f"Entry at {info['multiple']}x {label}. Base case {info['moic']}x MOIC and {info['irr']}% IRR over a 5-year hold."),
            ("Key Risks and Mitigants", "risks", " ".join(deal["risks"])),
            ("Diligence Findings", "diligence", deal["diligence"]),
        ]
    else:  # Portfolio Review
        pages = [
            ("Performance vs Plan", "portfolio",
             f"{p[2]} {label} of ${info['ebitda']}M vs ${deal['final_ic']['ebitda']}M at underwriting. Ahead of plan on pricing and tuck-ins."),
            ("Financials", "financials", "Actuals.\n" + table),
            ("Value Creation", "portfolio", "Closed 3 tuck-in acquisitions; route density up 9%; fuel surcharge recovery improved."),
            ("Outlook", "portfolio", "Exploring landfill permit expansion; considering dividend recap in 2026."),
        ]

    slides = []
    for n, (title, slide_type, text) in enumerate(pages, 1):
        slides.append({
            "slide_id": f"{deck_id}-s{n:02d}", "deck_id": deck_id, "slide_number": n,
            "project": deal["project"], "company": deal["company"], "sector": deal["sector"],
            "deck_stage": stage, "deck_date": info["date"],
            "title": title, "slide_type": slide_type, "search_text": text,
        })

    fin_slide = next(s["slide_id"] for s in slides if s["slide_type"] == "financials")
    base = {"deck_id": deck_id, "project": deal["project"], "deck_stage": stage, "deck_date": info["date"],
            "period": p[2], "source_slide_id": fin_slide}
    metrics = [
        {**base, "metric": "ebitda", "label_in_deck": label, "value": ebitda[2], "unit": "USD M"},
        {**base, "metric": "revenue", "label_in_deck": "Revenue", "value": rev[2], "unit": "USD M"},
    ]
    if stage == "Final IC":
        val_slide = next(s["slide_id"] for s in slides if s["slide_type"] == "valuation")
        metrics += [
            {**base, "source_slide_id": val_slide, "metric": "entry_multiple", "label_in_deck": f"x {label}", "value": info["multiple"], "unit": "x"},
            {**base, "source_slide_id": val_slide, "metric": "ev", "label_in_deck": "Enterprise value", "value": round(info["ebitda"] * info["multiple"], 1), "unit": "USD M"},
            {**base, "source_slide_id": val_slide, "metric": "moic", "label_in_deck": "MOIC", "value": info["moic"], "unit": "x"},
            {**base, "source_slide_id": val_slide, "metric": "irr", "label_in_deck": "IRR", "value": info["irr"], "unit": "%"},
        ]
    return slides, metrics


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    log.info("Wrote %s (%d rows)", path.relative_to(PROJECT_ROOT), len(rows))


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    slides, metrics, new_slides, new_metrics = [], [], [], []
    for deal in DEALS:
        for stage in ("Screening", "Final IC"):
            s, m = deck_slides(deal, stage)
            slides += s
            metrics += m
            log.info("%-8s %-10s %d slides, %d metrics", deal["project"], stage, len(s), len(m))
        if "portfolio" in deal:
            s, m = deck_slides(deal, "Portfolio Review")
            new_slides += s
            new_metrics += m
            log.info("%-8s %-10s %d slides, %d metrics (new-deck file)", deal["project"], "Portfolio", len(s), len(m))

    log.info("Totals: %d deals, %d decks, %d slides, %d metrics (+%d new slides)",
             len(DEALS), len({s['deck_id'] for s in slides}), len(slides), len(metrics), len(new_slides))
    write_jsonl(DATA_DIR / "fake_decks.jsonl", slides)
    write_jsonl(DATA_DIR / "fake_decks_new.jsonl", new_slides)
    write_jsonl(DATA_DIR / "fake_metrics.jsonl", metrics + new_metrics)


if __name__ == "__main__":
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-7s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler(LOG_DIR / "fake_decks.log", mode="w", encoding="utf-8")],
    )
    main()
