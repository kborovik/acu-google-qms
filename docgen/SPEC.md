# Inbound Shipping Document PDF Generator CLI

## §G GOAL
CLI generating pixel-perfect PDF shipping document suites (CoA, Packing Slip, BOL) per `domain/MANDATORY_SHIPPING_DOCUMENTS_SPEC.md`.

## §C CONSTRAINTS
- Python 3.14
- Click CLI framework
- ReportLab for vector-grade PDF rendering
- uv owns deps (`click`, `reportlab`, `pillow`); no `requirements.txt`
- ruff lint + format pass
- basedpyright strict mode pass (0 errors)
- Master data source: `acumatica/master_data/` (vendors, products, test_labs, qms_inspection_plans)
- All 5 vendors, 5 testing laboratories, and 10 raw materials supported
- Output 3 distinct document types: Certificate of Analysis (CoA), Packing Slip, Bill of Lading (BOL)
- Zero ERP leakage: external PDFs contain no internal Acumatica identifiers (no internal PO#, Acumatica VendorID, InventoryID, POReceipt#, QMS plan ID, or ERP warehouse bin codes)
- PO JSON input: docgen accepts Acumatica PO JSON to synthesize matching external shipment documents via master data

## §I INTERFACES
- cli: `uv run python -m docgen` / `uv run docgen`; subcommands `generate-suite`, `generate-coa`, `generate-packing-slip`, `generate-bol`, `batch`, `from-po`, `list-master-data`
- agent-help: bare `docgen` (no subcommand) and `docgen --help`/`-h` emit identical full multi-command Click help + LLM agent operating manual (master data IDs, resolution rules, document-dating default-today + `--as-of`, output artifacts, zero-ERP-leakage, PO JSON aliases, recipes)
- flags: `--po-json`, `--vendor-id`, `--inventory-id`, `--lot-nbr`, `--status [pass|fail]`, `--as-of YYYY-MM-DD`, `--outdir`, `--emit-json`, `--count`
- doc-coa: Certificate of Analysis PDF (`COA_<vendor>_<lot>.pdf`) with lab accreditation header, lot meta, test matrix table, pass/fail evaluation, QA signature
- doc-pack: Supplier Packing Slip PDF (`PACKING_SLIP_<vendor>_<lot>.pdf`) with supplier delivery note #, CanNordic dest, commercial product name, container count, gross/net kg, storage notes
- doc-bol: Bill of Lading PDF (`BOL_<carrier>_<lot>.pdf`) with carrier details, PRO#, trailer/seal#, pallet count, freight gross weight, chain-of-custody sign-offs
- data: `acumatica/master_data/products.json`, `vendors.json`, `test_labs.json`, `qms_inspection_plans.json`

## §V INVARIANTS
V1: three-document-suite — tool generates all 3 mandatory dock receiving documents: CoA, Packing Slip, BOL
V2: click-cli-architecture — CLI implemented via Click framework with modular subcommands; bare invocation and `--help` expand full per-subcommand help plus LLM agent operating manual (`AgentHelpGroup`)
V2b: agent-help-entrypoint — `uv run python -m docgen` with no subcommand prints the full agent help document and exits 0 (same text as `--help`)
V3: master-data-fidelity — lots, items, test criteria, and vendor/lab metadata resolve against `acumatica/master_data/`
V4: multi-lab-standards — CoA rendering adapts headers, regional units, and language terms to each of the 5 labs
V5: pass-fail-simulation — supports in-spec (pass) and out-of-spec (fail) simulation for QA quarantine/NCR testing
V6: reportlab-styling — vector-grade ReportLab templates with professional typography, bordered tables, and footer sign-off blocks
V7: typing-and-lint-clean — passes `uv run ruff check`, `uv run ruff format --check`, and `uv run basedpyright` with 0 warnings/errors
V8: zero-erp-leakage — external documents (CoA, Packing Slip, BOL) contain zero internal Acumatica identifiers (no internal PO#, Acumatica VendorID, InventoryID, POReceipt#, QMS plan ID, or ERP warehouse bin codes)
V9: po-json-input — docgen accepts Acumatica PO JSON input to generate realistic external shipment documents matching open PO lines via master data
V10: document-as-of — default as-of = run date (local YYYY-MM-DD); mfg + ship + CoA/BOL stamps = as-of; expiry = as-of + 3y (or product shelf-life when present); `--as-of YYYY-MM-DD` overrides anchor; invalid as-of → non-zero exit

## §T TASKS
id|status|task|cites
T1|x|init `docgen/` directory + `docgen/SPEC.md`|V1,V2,I.cli
T2|x|define master data models and JSON loader in `docgen/models.py`|V3,I.data
T3|x|define ReportLab typography, colors, borders, and numbered canvas in `docgen/styles.py`|V6,I.doc-coa,I.doc-pack,I.doc-bol
T4|x|implement Certificate of Analysis (CoA) PDF generator in `docgen/coa_builder.py`|V1,V4,V5,V6,I.doc-coa
T5|x|implement Supplier Packing Slip PDF generator in `docgen/packing_slip_builder.py`|V1,V3,V6,I.doc-pack
T6|x|implement Bill of Lading (BOL) PDF generator in `docgen/bol_builder.py`|V1,V3,V6,I.doc-bol
T7|x|implement Click CLI entry points, subcommands, and batch generator in `docgen/cli.py`|V2,V5,I.cli,I.flags
T8|x|configure `pyproject.toml` tool sections and verify `ruff` + `basedpyright` passes|V7,I.cli
T9|x|sanitize `docgen/packing_slip_builder.py` removing all Acumatica internal references (PO#, VendorID, InventoryID, POReceipt#, quarantine bin)|V6,V8,I.doc-pack
T10|x|sanitize `docgen/coa_builder.py` removing Acumatica InventoryID, PO reference, internal plan ID, and internal QA disposition block|V4,V6,V8,I.doc-coa
T11|x|sanitize `docgen/bol_builder.py` removing Acumatica PO and POReceipt references|V6,V8,I.doc-bol
T12|x|extend `docgen/models.py` and `docgen/cli.py` to accept `--po-json` input and build shipment suites from PO JSON|V3,V8,V9,I.cli,I.flags
T13|x|update manifest schema to distinguish external document fields from ground-truth ERP linking metadata|V3,V8,I.cli
T14|x|derive suite dates from as-of (default today); wire `--as-of` on generate-suite, from-po, generate-coa, generate-packing-slip, generate-bol, batch|V10,I.flags
T15|x|sync AGENT_HELP_EPILOG + AGENTS.md recipes for default-today / `--as-of`|V10,V2b,I.agent-help

## §B BUGS
id|date|cause|fix
B1|2026-09-03|hardcoded mfg/expiry strings → PDF dates stuck in past vs run day|V10
