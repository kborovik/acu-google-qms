# GCP Acumatica CoA Ingestion Platform

An automated quality compliance and material ingestion platform that extracts, validates, and synchronizes Certificate of Analysis (CoA) data with Acumatica Cloud ERP using a GCP-hosted LLM reasoning engine.

## Core Objectives

1. **Unstructured Certificate of Analysis Ingestion & Extraction**
   - Automatically ingest and parse unstructured supplier Certificate of Analysis (CoA) documents across formats (PDFs, scans, emails).
   - Extract analytical test results, chemical assays, heavy metals, microbial panels, and expiration metadata.

2. **Data Normalization & Audit Provenance**
   - Standardize analyte naming, bilingual descriptors (English/French), and units of measure into canonical SI formats.
   - Capture visual coordinate provenance (bounding boxes) for each extracted value to ensure Health Canada / CFIA audit traceability.

3. **Tolerance & Regulatory Compliance Verification**
   - Validate extracted analytical values against Acumatica ERP quality management specifications (`QMSInspectionPlan`).
   - Enforce compliance with regulatory safety limits under Health Canada (GMP / NHPR) and CFIA (SFCR) standards.

4. **Automated ERP Lot Governance**
   - Automatically populate inspection orders (`QMSInspectionOrder`) in Acumatica Cloud ERP.
   - Execute lot disposition decisions: release compliant inventory lots from quarantine or trigger Non-Conformance Reports (`QMSNonConformance` NCR) on failure.

5. **Cloud-Native Agent Platform Infrastructure**
   - Run ingestion and evaluation workloads via Google Cloud Vertex AI Reasoning Engine using the Google Agent Development Kit (ADK).
   - Enforce deterministic, code-defined infrastructure management via Terraform.
