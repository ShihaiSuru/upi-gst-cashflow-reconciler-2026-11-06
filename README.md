# UPI-GST Cashflow Reconciler

**AI-assisted tool for Indian MSMEs to match UPI transactions with GST invoices, flag delayed receivables, and project short-term cash flow.**

## The Problem

Indian MSMEs face chronic working-capital stress. Delayed payments (often 60–120 days) lock up an estimated ₹7+ lakh crore in receivables. GST is payable on accrual (when the invoice is raised), not on cash receipt. UPI has become the dominant collection channel for many small businesses, yet most founders still reconcile bank/UPI statements against GST invoices manually in spreadsheets. This creates:

- Unmatched payments that are never claimed
- Hidden delayed receivables that damage cash-flow forecasts
- Inability to show clean cash-flow trails to lenders or TReDS platforms
- Time lost that should be spent on operations

## The Solution

This repository is a practical starter for an AI-enhanced reconciler that:

1. Ingests a UPI transaction statement (CSV or simple table)
2. Ingests GST invoice data (GSTR-1 style or simplified export)
3. Matches payments to invoices using amount, date proximity, and reference text
4. Flags unmatched items and delayed receivables
5. Produces a simple near-term cash-flow projection

The current code is a clean, commented Python prototype you can run immediately and extend with LLMs, OCR, or Account Aggregator data.

## Quick Start

```bash
# Clone
git clone https://github.com/ShihaiSuru/upi-gst-cashflow-reconciler-2026-11-06.git
cd upi-gst-cashflow-reconciler-2026-11-06

# Run the demo (no external dependencies)
python upi_gst_reconciler.py
```

## Sample Output

The script prints:
- Matched invoice ↔ UPI payment pairs
- Unmatched UPI credits (possible unbilled or advance receipts)
- Unmatched / overdue invoices
- A simple 30-day cash-flow outlook based on expected collections

## Roadmap (Practical Next Steps)

- [ ] Parse real bank/UPI CSV exports (PhonePe, Google Pay Business, bank statements)
- [ ] Ingest GSTR-1 JSON or e-invoice JSON
- [ ] Fuzzy matching + LLM-based reference extraction
- [ ] Integrate with TReDS / early-payment platforms
- [ ] Working-capital estimator that factors in GST ITC and delayed receivables
- [ ] Simple Streamlit or Gradio demo for non-technical MSME owners

## Who This Is For

- MSME founders who want better cash-flow visibility
- Fintech builders building cash-flow or lending products on top of GST + UPI data
- Anyone exploring cash-flow-based underwriting for Indian small businesses

---

Built as a profile project to showcase practical MSME fintech tooling focused on AI cash-flow systems.
