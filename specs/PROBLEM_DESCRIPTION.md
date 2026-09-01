# Inbound Quality & Material Compliance Ingestion Platform
## Problem Description, Canadian Market Standards & Acumatica ERP Specification

---

## 1. Executive Summary & Strategic Focus

In mid-market manufacturing, processing, and ingredient distribution, inbound raw materials and botanical components are accompanied by dense, unstructured Certificate of Analysis (CoA) documents that verify quality, safety, and regulatory compliance.

### Strategic Focus: **Certificate of Analysis (CoA) Ingestion**
The **Certificate of Analysis (CoA)** represents the single largest operational bottleneck and the highest-volume document class across regulated health and food manufacturing.

Under Canadian federal regulations (**Health Canada GMP / NHPR** and **CFIA Safe Food for Canadians Regulations**), raw materials **cannot be released into production or blending** until their lot-specific CoA is inspected, verified against strict regulatory and customer quality specifications, and permanently linked to the ERP lot genealogy.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PRODUCT ARCHITECTURE OVERVIEW                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  INBOUND CoA SOURCES:        AI COMPLIANCE ENGINE:                          │
│  ┌─────────────────────────┐ ┌───────────────────────────────────────────┐  │
│  │ • Supplier PDF Email    │ │ • Multimodal Layout-Aware Table Parser    │  │
│  │ • Receiving Dock Scan   │ │ • Chemical, Metal & Microbial Normalizer  │  │
│  │ • Supplier Portal Upload│ │ • Dynamic Tolerance & Spec Matcher        │  │
│  └────────────┬────────────┘ └─────────────────────┬─────────────────────┘  │
│               │                                    │                        │
│               ▼                                    ▼                        │
│  ACUMATICA CLOUD ERP INTEGRATION:                                           │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ • Automated Inspection Order Population (`QMSInspectionOrder`)        │  │
│  │ • Real-time Lot Status Governor: "Released" vs. "Quarantine"          │  │
│  │ • Automatic Non-Conformance Report (`QMSNonConformance` NCR) Trigger  │  │
│  │ • Audit-Ready PDF & JSON Archival on Receipt & Lot Records            │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

Today, mid-market enterprises running **Acumatica Cloud ERP** rely on manual data entry and visual inspection. Quality technicians and receiving clerks spend 15 to 45 minutes per shipment re-keying chemical assays, heavy metals, microbial counts, and lot expiration dates into ERP inspection orders or spreadsheets. This manual workflow creates substantial operational latency ("QC Material Holds"), introduces human transcription errors, and exposes organizations to regulatory penalties, production idle time, or failed Health Canada audits.

### Reference Implementation Organization: **CanNordic BioNutra Inc.**
The operational baseline, workflows, test datasets, and Acumatica ERP integration mappings across these specifications are modeled against **CanNordic BioNutra Inc.** (Mississauga, ON)—a Canadian hybrid contract development and manufacturing organization (CDMO) and raw ingredient importer operating under Health Canada Site Licence #302194 and CFIA SFCR regulations. See [`specs/COMPANY_PROFILE.md`](COMPANY_PROFILE.md) for the complete organizational profile.

This platform solves this by deploying a **Multimodal AI Ingestion Pipeline** that parses unstructured CoA PDFs, standardizes units, checks values against Acumatica Quality Management tolerance specifications, and automatically releases inventory lots or triggers Non-Conformance Reports (NCR).

---

## 2. Market & Regulatory Standards Matrix (Canada & North America)

Canadian natural health product, dietary supplement, and food manufacturers operate under strict federal regulatory mandates alongside international analytical testing standards. The ingestion platform natively parses and validates against:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REGULATORY & QUALITY COMPLIANCE MATRIX                   │
├────────────────────────┬──────────────────────────┬─────────────────────────┤
│ HEALTH CANADA (NHPR)   │       CFIA & SFCR        │  LABORATORY & PHARMA    │
├────────────────────────┼──────────────────────────┼─────────────────────────┤
│ • GMP (GUI-0001/0158)  │ • Safe Food for Cdns     │ • USP <2021> / <2022>   │
│ • NHPR (SOR/2003-196)  │ • Preventive Controls    │ • USP <2232> / <731>    │
│ • Heavy Metals Limits  │ • HACCP / GFSI Schemes   │ • ISO/IEC 17025:2017    │
│ • Finished / Raw NPN   │ • Canada Organic (COR)   │ • HPLC / ICP-MS Assays  │
└────────────────────────┴──────────────────────────┴─────────────────────────┘
```

### 2.1 Health Canada & Life Sciences Regulations
* **Good Manufacturing Practices (GMP) Guidelines (GUI-0001 / GUI-0158):** Mandates that every active ingredient, raw material, and packaging material be tested and accompanied by an authentic Certificate of Analysis before lot release into production.
* **Natural Health Products Regulations (NHPR - SOR/2003-196):** Strict contaminant testing limits for:
  * **Heavy Metals:** Arsenic ($\le 1.0$ ppm), Cadmium ($\le 0.3$ ppm), Lead ($\le 0.5$ ppm), Mercury ($\le 0.1$ ppm) under Category 1 limits.
  * **Microbial Thresholds:** Total Aerobic Microbial Count (TAMC $\le 10^4$ CFU/g), Total Combined Yeast & Mold (TYMC $\le 10^3$ CFU/g), absence of *E. coli* and *Salmonella spp.*
  * **Pesticide Residues & Residual Solvents:** USP <467> / Ph. Eur. residual solvent thresholds.

### 2.2 Canadian Food Inspection Agency (CFIA) & Organic Regimes
* **Safe Food for Canadians Regulations (SFCR):** Requirements for Preventive Control Plans (PCP), traceability (one step forward, one step back), and verification of raw food and botanical inputs against biological, chemical, and physical hazards.
* **Food Safety Systems:** Validation against HACCP, GFSI-benchmarked schemes (SQF, BRCGS, FSSC 22000).
* **Canada Organic Regime (COR):** Certification verification for certified organic botanical extracts and raw inputs.

### 2.3 Pharmacopeial & Analytical Standards (USP, AOAC, ISO)
* **USP <2021> / USP <2022>:** Microbiological enumeration and absence testing for dietary supplements.
* **USP <2232>:** Elemental contaminants in dietary supplements via ICP-MS testing.
* **USP <731>:** Loss on drying (moisture determination).
* **ISO/IEC 17025:2017:** Accreditation requirements for testing laboratories issuing CoAs.

---

## 3. CoA Ingestion Profiles & Analyte Categories

| Parameter Category | Analyte Examples | Standard Test Methods | Specified Limits / Acceptance Criteria | Acumatica / Regulatory Action |
| :--- | :--- | :--- | :--- | :--- |
| **Active Potency & Assay** | Active Polyphenols, Withanolides, Curcuminoids, Vitamin C | HPLC-DAD, HPLC-UV, Titration, UV-Vis | $\ge \text{Target Spec } \%$ (w/w) or Label Claim $\pm 10\%$ | Target potency matching; drives lot release or formulation potency adjustment. |
| **Physical & Chemical Properties** | Loss on Drying (Moisture), pH, Bulk Density, Particle Size | USP <731>, USP <786>, pH meter | $\le 5.0\%$ moisture, mesh size pass % | High moisture triggers physical quality hold (clumping / microbial risk). |
| **Heavy Metal Contaminants** | Lead (Pb), Arsenic (As), Cadmium (Cd), Mercury (Hg) | ICP-MS (USP <2232>), ICP-OES | $\text{Pb} \le 0.5$, $\text{As} \le 1.0$, $\text{Cd} \le 0.3$, $\text{Hg} \le 0.1$ ppm | Strict limit comparison; ANY breach immediately creates Acumatica NCR and quarantines lot. |
| **Microbiological Limits** | TAMC (Total Aerobic), TYMC (Yeast & Mold), *E. coli*, *Salmonella* | USP <2021>, USP <2022>, AOAC BAM | $\text{TAMC} \le 10^4\text{ CFU/g}$, $\text{TYMC} \le 10^3$, Pathogens: Absent | Out-of-spec microbial count triggers quarantine and immediate QA manager notification. |
| **Residual Solvents & Impurities** | Ethanol, Methanol, Acetone, Hexane | GC-FID (USP <467> Headspace) | USP <467> Option 1/2 limits (e.g. Ethanol $\le 5000$ ppm) | Extraction solvent safety verification for organic botanical products. |

---

## 4. Acumatica Cloud ERP Integration Architecture

The solution connects seamlessly to **Acumatica Cloud ERP (xRP Platform)** using REST APIs, Webhooks/Business Events, and contract-based integrations.

```
┌──────────────────┐       ┌───────────────────────────┐       ┌──────────────────────┐
│   Inbound CoA    │       │  AI Compliance Ingestion  │       │    Acumatica ERP     │
│   (PDF / Scan)   │──────▶│         Platform          │──────▶│    Cloud Database    │
└──────────────────┘       └───────────────────────────┘       └──────────────────────┘
         │                               │                                │
  • Email Attachment            • Multimodal Vision AI            • PO Receipt Module
  • Mobile Dock Scan            • Canadian Spec Parser            • Lot/Serial Status
  • Supplier Portal             • Unit Converter (SI/Imp)         • QMS Inspection Plan
  • ERP File Link               • Tolerance / Spec Engine         • NCR / Quarantine
```

### 4.1 Acumatica Integration Touchpoints & Entities

1. **Purchasing & Receiving (`POReceipt`):**
   * Listens to `POReceipt` creation events or webhook triggers when goods arrive at the warehouse dock.
   * `POReceiptLineSplit`: Fetches and validates specific Lot numbers associated with the inbound receipt line.
2. **Inventory & Lot Master (`INLotSerialStatus`):**
   * Reads item master records (`InventoryItem`), specifications, quality test classes, and shelf-life requirements.
   * Updates lot attributes (e.g., Active Potency %, Expiry Date, Quality Status: `QC Hold`, `Released`, `Quarantine`, `Rejected`).
3. **Quality Management (`QMSInspectionOrder` / `QMSNonConformance`):**
   * `QMSInspectionPlan`: Queries predefined test criteria and acceptable tolerance ranges.
   * `QMSInspectionOrder`: Automatically populates measured analytical values into inspection orders, eliminating manual keying.
   * `QMSNonConformance` (NCR): Automatically generates an NCR and segregates the inventory lot if test values breach tolerance thresholds.
4. **Document Management & File Repository (`UploadFile`):**
   * Attaches the original supplier PDF, parsed JSON data, and validation audit report directly to the Acumatica `POReceipt` and `INLotSerialStatus` records.

### 4.2 End-to-End Dock-to-Stock CoA Receiving & Inspection Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CoA INSPECTION & RECEIVING WORKFLOW                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
 1. PHYSICAL DOCK ARRIVAL             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Inbound truck docks; clerk inspects container seals, temps & lot tags.  │
 │ • Clerk creates `POReceipt` in Acumatica; lot assigned (e.g. LOT-EC2602). │
 │ • Acumatica locks lot in "QC Hold" (Quarantine) under Health Canada GMP.  │
 │ • Pallets staged in receiving bay with physical yellow QC Hold placards.  │
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 2. INBOUND CoA CAPTURE               ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Supplier CoA PDF captured via dock scan, email webhook, or vendor portal│
 │ • Pipeline associates PDF with Vendor ID, PO Receipt line, and Lot Number.│
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 3. MULTIMODAL AI PARSING & NORMALIZATION ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Vision/Layout parser extracts test matrix (Assays, Heavy Metals, CFUs). │
 │ • Bilingual terms & synonyms normalized (e.g., Plomb/Pb -> heavy_metal_pb)│
 │ • Units normalized (ppm <-> mg/kg, CFU/g, % w/w); bounding boxes recorded.│
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 4. SPECIFICATION & TOLERANCE MATCHING ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Engine queries Acumatica `QMSInspectionPlan` for item tolerances.       │
 │ • Evaluates potency, heavy metals, microbial CFUs, and LOD against limits.│
 │ • Verifies remaining shelf-life against Expiration Date.                 │
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 5. AUTOMATED ERP DECISION & LOT GOVERNOR ▼
          ├───────────────────────────────────────────┐
          │ ALL IN-SPEC                               │ OUT-OF-SPEC / FAILED
          ▼                                           ▼
 ┌──────────────────────────────────┐        ┌──────────────────────────────────┐
 │ • `QMSInspectionOrder` completed │        │ • Lot flagged as "Quarantine"    │
 │ • Lot status flipped: "Released" │        │ • Acumatica NCR ticket generated │
 │ • Unblocked for production work  │        │ • QA Manager alerted immediately │
 │ • PDF attached to ERP Lot record │        │ • Pallet moved to locked storage │
 └──────────────────────────────────┘        └──────────────────────────────────┘
```

#### Detailed Lifecycle Phases:
1. **Dock Arrival & Regulatory Hold:**
   * Truck arrives; physical integrity of packaging/seals is verified.
   * `POReceipt` and `POReceiptLineSplit` are registered in Acumatica.
   * Acumatica automatically assigns `QC Hold` status (`INLotSerialStatus`), enforcing a hard stop preventing raw material allocation to manufacturing work orders until QC release.
2. **Document Ingestion & AI Inspection:**
   * Supplier CoA PDF is captured (scanner, email, portal) and matched to the PO receipt line.
   * Multimodal vision model extracts metadata and analytical test rows with visual bounding-box provenance.
   * Analyte synonyms and measurement units are normalized to standard SI units.
   * Engine evaluates values against Acumatica's `QMSInspectionPlan` and Health Canada NHP limits.
3. **Automated ERP Governance & Material Release:**
   * **Passing Lots:** Inspection order values populated in Acumatica, lot status flipped from `QC Hold` to `Released`, PDF/JSON records archived on the lot, and material unblocked for blending.
   * **Failing / Out-of-Spec Lots:** Lot status set to `Quarantine`, Non-Conformance Report (NCR) generated automatically in Acumatica QMS, instant alert sent to QA leadership, and physical material moved to locked storage pending return-to-vendor (RTV).

---

## 5. Technical Capabilities of the CoA Ingestion Pipeline

1. **Multimodal Layout-Aware Table Parser:**
   Handles variable multi-column tables, skewed scans, watermarks, and multi-page lab certificates without requiring rigid per-supplier templates.
2. **Chemical & Analyte Synonym Normalizer:**
   Recognizes that `As`, `Arsenic`, and `CAS 7440-38-2` refer to the same chemical entity; standardizes microbiological assay names (`Total Plate Count`, `TAMC`, `Aerobic Plate Count`).
3. **Unit Conversion & Normalization:**
   Supports bi-directional conversion between Imperial and SI Metric units, and scientific concentrations (ppm $\leftrightarrow$ mg/kg, % $\leftrightarrow$ g/100g).
4. **Bilingual Compliance Parsing (English / French):**
   Full support for Canadian bilingual CoAs (e.g., identifying both *Numéro de lot* and *Lot Number*, *Résultat* and *Result*, *Pertes au séchage* and *Loss on Drying*).
5. **Full Auditability & Visual Provenance:**
   Every extracted data point is stored with bounding-box coordinates on the original PDF, allowing one-click visual audit verification inside the user interface.

---

## 6. Synthetic Sample Documents & Generator

To test and demonstrate the system without using proprietary client data, the platform includes sample documents and an automated Python generator modeled after CanNordic BioNutra Inc.:

1. **`specs/samples/coa_sample_nutraceutical_health_canada.json` & `.md`:** Canonical sample for Organic Echinacea Purpurea Extract tested against Health Canada NHP guidelines (Active Potency, Loss on Drying, Heavy Metals ICP-MS, Microbial Limits USP <2021>/<2022>, Residual Solvents).
2. **`specs/samples/COA-2026-HC-88412.pdf`:** Pixel-perfect PDF Certificate of Analysis for visual extraction, OCR, and bounding-box provenance testing.
3. **`specs/samples/generate_demo_documents.py`:** Automated Python generator producing synthetic CoA documents with configurable pass/fail distributions for CI/CD and Acumatica integration tests.
4. **`specs/samples/generated_test_batch/`:** Pre-generated test batch containing passing and failing CoA JSON documents for testing automated lot release and NCR triggers.

---

## 7. Deliverables in This Specification Package

* `specs/PROBLEM_DESCRIPTION.md`: Core problem, regulatory standards, and Acumatica ERP specification.
* `specs/COMPANY_PROFILE.md`: Reference target enterprise profile (CanNordic BioNutra Inc.).
* `specs/COA_INGESTION_SPEC.md`: Detailed engineering and API specification for the Certificate of Analysis pipeline.
* `specs/samples/`: Ready-to-use sample documents in JSON schema, formatted text/markdown, and PDF.
* `specs/samples/generate_demo_documents.py`: Automated Python generator to produce realistic CoA test/demo documents.
* `specs/samples/generate_pdf_sample.py`: ReportLab PDF generator for standard CoA documents.
