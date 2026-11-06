#!/usr/bin/env python3
"""
UPI-GST Cashflow Reconciler — Starter Prototype
================================================
A practical demo for Indian MSMEs to match UPI collections against GST invoices,
flag delayed receivables, and produce a simple short-term cash-flow view.

No external dependencies. Run with: python upi_gst_reconciler.py
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# ---------------------------------------------------------------------------
# Sample data (replace with real CSV / GSTR-1 parsing later)
# ---------------------------------------------------------------------------

UPI_TRANSACTIONS = [
    {"date": "2026-10-05", "amount": 11800, "reference": "INV-1045 ABC Traders", "utr": "UPI001"},
    {"date": "2026-10-12", "amount": 5900,  "reference": "Invoice 1048",           "utr": "UPI002"},
    {"date": "2026-10-20", "amount": 23600, "reference": "Payment for Oct supplies", "utr": "UPI003"},
    {"date": "2026-10-28", "amount": 8850,  "reference": "",                         "utr": "UPI004"},  # unmatched
    {"date": "2026-11-02", "amount": 14750, "reference": "INV-1052 XYZ Enterprises", "utr": "UPI005"},
]

GST_INVOICES = [
    {"invoice_no": "INV-1045", "date": "2026-09-28", "customer": "ABC Traders",      "amount": 11800, "gstin": "27AAAAA1111A1Z1"},
    {"invoice_no": "INV-1048", "date": "2026-10-02", "customer": "PQR Stores",        "amount": 5900,  "gstin": "29BBBBB2222B1Z2"},
    {"invoice_no": "INV-1050", "date": "2026-10-10", "customer": "LMN Industries",    "amount": 23600, "gstin": "07CCCCC3333C1Z3"},
    {"invoice_no": "INV-1052", "date": "2026-10-25", "customer": "XYZ Enterprises",   "amount": 14750, "gstin": "19DDDDD4444D1Z4"},
    {"invoice_no": "INV-1055", "date": "2026-10-30", "customer": "DEF Corp",          "amount": 17700, "gstin": "24EEEEE5555E1Z5"},  # still open
]

# ---------------------------------------------------------------------------
# Core matching logic
# ---------------------------------------------------------------------------

def parse_date(d: str) -> datetime:
    return datetime.strptime(d, "%Y-%m-%d")

def find_match(upi: Dict, invoices: List[Dict], days_window: int = 15) -> Optional[Dict]:
    """
    Simple deterministic matching:
    1. Exact amount match
    2. Invoice number appears in UPI reference (case-insensitive)
    3. Date within window
    """
    upi_date = parse_date(upi["date"])
    ref = (upi.get("reference") or "").lower()

    for inv in invoices:
        if inv["amount"] != upi["amount"]:
            continue
        inv_date = parse_date(inv["date"])
        if abs((upi_date - inv_date).days) > days_window:
            continue
        if inv["invoice_no"].lower() in ref or inv["customer"].lower() in ref:
            return inv
        # Fallback: amount + date window only (weaker match)
        return inv
    return None

def reconcile(upi_txns: List[Dict], invoices: List[Dict]) -> Dict:
    matched = []
    unmatched_upi = []
    remaining_invoices = invoices.copy()

    for upi in upi_txns:
        match = find_match(upi, remaining_invoices)
        if match:
            matched.append({"upi": upi, "invoice": match})
            remaining_invoices = [i for i in remaining_invoices if i["invoice_no"] != match["invoice_no"]]
        else:
            unmatched_upi.append(upi)

    # Anything left is potentially delayed / open
    overdue = []
    today = datetime(2026, 11, 6)  # demo date
    for inv in remaining_invoices:
        days_open = (today - parse_date(inv["date"])).days
        status = "overdue" if days_open > 45 else "open"
        overdue.append({**inv, "days_open": days_open, "status": status})

    return {
        "matched": matched,
        "unmatched_upi": unmatched_upi,
        "open_invoices": overdue,
    }

def cashflow_projection(result: Dict, horizon_days: int = 30) -> Dict:
    """Very simple projection: expected collections from open invoices within horizon."""
    expected_in = sum(i["amount"] for i in result["open_invoices"] if i["days_open"] < 90)
    recent_collections = sum(m["upi"]["amount"] for m in result["matched"])
    return {
        "recent_matched_collections": recent_collections,
        "expected_collections_next_30_days": expected_in,
        "unmatched_upi_credits": sum(u["amount"] for u in result["unmatched_upi"]),
        "note": "Replace with real payment-term assumptions and historical collection rates."
    }

# ---------------------------------------------------------------------------
# Demo run
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("UPI-GST Cashflow Reconciler — Demo")
    print("=" * 60)

    result = reconcile(UPI_TRANSACTIONS, GST_INVOICES)

    print("\n✅ MATCHED")
    for m in result["matched"]:
        print(f"  {m['invoice']['invoice_no']} ↔ {m['upi']['utr']} | ₹{m['upi']['amount']:,} | {m['upi']['date']}")

    print("\n⚠️  UNMATCHED UPI CREDITS")
    for u in result["unmatched_upi"]:
        print(f"  {u['utr']} | ₹{u['amount']:,} | {u['date']} | ref: '{u['reference']}'")

    print("\n📋 OPEN / OVERDUE INVOICES")
    for inv in result["open_invoices"]:
        print(f"  {inv['invoice_no']} | {inv['customer']} | ₹{inv['amount']:,} | {inv['days_open']} days | {inv['status']}")

    projection = cashflow_projection(result)
    print("\n📊 30-DAY CASHFLOW OUTLOOK")
    print(json.dumps(projection, indent=2))

    print("\nNext steps: load real UPI CSV + GSTR-1, add fuzzy matching, and feed into a working-capital model.")

if __name__ == "__main__":
    main()
