# GCP Acumatica CoA Ingestion Platform

An automated quality compliance and material ingestion platform that extracts, validates, and synchronizes Certificate of Analysis (CoA) data with Acumatica Cloud ERP using a GCP-hosted LLM reasoning engine.

## Core Objectives

1. **Unstructured Certificate of Analysis Ingestion and Extraction**
   - Automatically ingest and parse unstructured supplier Certificate of Analysis (CoA) documents across formats (PDFs, scans, emails).
   - Extract analytical test results, chemical assays, heavy metals, microbial panels, and expiration metadata.

2. **Data Normalization and Audit Provenance**
   - Standardize analyte naming, multilingual descriptors (English, French, German, Japanese, Norwegian), and heterogeneous units of measure into canonical SI formats.
   - Support 5 distinct testing laboratory standards across 5 global vendor partners (Health Canada/CALA, Ph. Eur./DIN, SCC/AOAC, JP 18/JIS, GOED/Nordic).
   - Capture visual coordinate provenance (bounding boxes) for each extracted value to ensure Health Canada / CFIA audit traceability.

3. **Tolerance and Regulatory Compliance Verification**
   - Validate extracted analytical values against Acumatica ERP quality management specifications (`QMSInspectionPlan`).
   - Enforce compliance with regulatory safety limits under Health Canada (GMP / NHPR) and CFIA (SFCR) standards.

4. **Automated ERP Lot Governance**
   - Automatically populate inspection orders (`QMSInspectionOrder`) in Acumatica Cloud ERP.
   - Execute lot disposition decisions: release compliant inventory lots from quarantine or trigger Non-Conformance Reports (`QMSNonConformance` NCR) on failure.

5. **Cloud-Native Agent Platform Infrastructure**
   - Run ingestion and evaluation workloads via Google Cloud Vertex AI Reasoning Engine using the Google Agent Development Kit (ADK).
   - Enforce deterministic, code-defined infrastructure management via Terraform.

## Document Generator CLI (`docgen`)

The platform includes a dedicated vector-grade PDF generator CLI built with `click` and `reportlab` to synthesize realistic 3-document dock receiving suites:
- **Certificate of Analysis (CoA):** Multi-lab standards (CALA, Ph. Eur., AOAC, JP 18, GOED).
- **Supplier Packing Slip / Delivery Note:** PO correlation, line item allocations, gross/net weights.
- **Carrier Bill of Lading (BOL):** Chain-of-custody, PRO#, trailer/seal verification, driver sign-offs.

```bash
# List master data
uv run python -m docgen list-master-data

# Generate full 3-document PDF suite for an inventory item
uv run python -m docgen generate-suite --inventory-id RAW-ECH-EXT4 --outdir ./output/sample_suite

# Generate batch of 5 suites across all vendors with pass/fail simulation
uv run python -m docgen batch --count 5 --outdir ./output/batch
```
