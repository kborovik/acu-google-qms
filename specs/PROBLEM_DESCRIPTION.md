# Inbound Quality & Material Compliance Ingestion Platform
## Problem Description, Canadian Market Standards & Acumatica ERP Specification

---

## 1. Executive Summary & Strategic Focus

In mid-market manufacturing, processing, and distribution, inbound raw materials and components are accompanied by dense, unstructured technical documents that verify quality, safety, and regulatory compliance.

### Strategic Anchor: **Certificate of Analysis (CoA) Ingestion**
Among all compliance document types, the **Certificate of Analysis (CoA)** represents the single largest operational bottleneck and the highest-volume document class across regulated mid-market industries (Food & Beverage, Natural Health Products, Pharmaceuticals, Cannabis, Cosmetics, and Specialty Chemicals). 

Under Canadian federal regulations (**Health Canada GMP / NHPR** and **CFIA Safe Food for Canadians Regulations**), materials **cannot be released into production or distributed** until their specific lot CoA is inspected, cross-checked against strict regulatory and customer quality specifications, and permanently linked to the ERP lot genealogy.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PRODUCT ARCHITECTURE STRATEGY                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  PRIMARY MVP WEDGE:          SHARED ENGINE ARCHITECTURE:                    │
│  ┌─────────────────────────┐ ┌───────────────────────────────────────────┐  │
│  │ Certificate of Analysis │ │ • Multi-Modal Layout-Aware Table Parser   │  │
│  │ (CoA) Ingestion Engine  │ │ • Unit Conversion & Chemical Normalizer   │  │
│  │ (Health Canada & CFIA)  │ │ • Dynamic Tolerance & Spec Matcher        │  │
│  └────────────┬────────────┘ │ • Bi-directional Acumatica REST Connector │  │
│               │              └─────────────────────┬─────────────────────┘  │
│               ▼                                    ▼                        │
│  SECONDARY MODULE (METALS/MFG):       TERTIARY MODULES (EXPANSION):         │
│  ┌─────────────────────────┐          ┌──────────────────────────────────┐  │
│  │ Material Test Reports   │          │ • Certificates of Conformance    │  │
│  │ (MTR / MTC - CSA/ASTM)  │          │ • Safety Data Sheets (WHMIS SDS) │  │
│  └─────────────────────────┘          └──────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

Today, mid-market enterprises running **Acumatica Cloud ERP** rely on manual data entry and visual inspection. Quality technicians and receiving clerks spend 15 to 45 minutes per shipment re-keying chemical compositions, mechanical properties, microbial thresholds, and lot numbers into ERP custom fields or spreadsheets. This manual workflow creates substantial operational latency ("QC Material Holds"), introduces human transcription errors, and exposes organizations to catastrophic regulatory penalties, product recalls, or failed audits.

### Reference Implementation Organization: **CanNordic BioNutra Inc.**
The operational baseline, workflows, test datasets, and Acumatica ERP integration mappings across these specifications are modeled against **CanNordic BioNutra Inc.** (Mississauga, ON)—a Canadian hybrid contract manufacturer (CDMO) and raw ingredient importer operating under Health Canada Site Licence #302194 and CFIA SFCR regulations. See [`specs/COMPANY_PROFILE.md`](COMPANY_PROFILE.md) for the complete organizational profile.

This platform solves this by deploying a **Multimodal AI Ingestion Pipeline** that parses unstructured CoA PDFs, standardizes units, checks values against Acumatica Quality Management tolerance specifications, and automatically releases inventory lots or triggers Non-Conformance Reports (NCR).

---

## 2. Market & Regulatory Standards Matrix (Canada & North America)

Canadian companies operate under strict federal and provincial regulatory mandates alongside harmonized North American (ASTM, ASME) and international (ISO) standards. The ingestion platform must be natively aware of and validate against the following standard bodies and regulations:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CANADIAN REGULATORY & STANDARDS LANDSCAPE             │
├────────────────────────┬──────────────────────────┬─────────────────────────┤
│    HEALTH & PHARMA     │   METALS & INDUSTRIAL    │  CHEMICALS & WORKPLACE  │
├────────────────────────┼──────────────────────────┼─────────────────────────┤
│ • Health Canada GMP    │ • CSA Group (G40.21)     │ • WHMIS 2015 / HPR      │
│ • CFIA / SFCR          │ • ASTM International     │ • ECCC / CEPA           │
│ • NHP Regulations      │ • ASME BPVC Sec II/VIII  │ • Transport Canada TDG  │
│ • Cannabis Act         │ • CSA B51 / CSA Z662     │ • Bilingual (EN/FR) SDS │
└────────────────────────┴──────────────────────────┴─────────────────────────┘
```

### 2.1 Health Canada & Life Sciences (CoA Focus)
* **Good Manufacturing Practices (GMP) Guidelines (GUI-0001):** Mandates that every active pharmaceutical ingredient (API), raw material, and packaging material be tested and accompanied by an authentic Certificate of Analysis before lot release into production.
* **Natural Health Products Regulations (NHPR - SOR/2003-196):** Strict contaminant testing limits for heavy metals (Arsenic, Cadmium, Lead, Mercury), microbial counts (TPC, Yeast & Mold, *E. coli*, *Salmonella*), and pesticide residues.
* **Cannabis Act (SOR/2018-144):** Mandatory CoA testing for phytocannabinoid potency (THC, CBD, CBG), terpenes, mycotoxins, heavy metals, and residual solvents (PPM).
* **Medical Device Regulations (SOR/98-282) / ISO 13485:2016:** Traceability of materials, biocompatibility certificates, and Certificates of Conformance across supply tiers.

### 2.2 Canadian Food Inspection Agency (CFIA)
* **Safe Food for Canadians Regulations (SFCR):** Requirements for Preventive Control Plans (PCP), traceability (one step forward, one step back), and verification of food ingredients against microbial, chemical, and physical hazards.
* **Food Safety Systems:** Validation against HACCP, GFSI-benchmarked schemes (SQF, BRCGS, FSSC 22000).

### 2.3 CSA Group (Canadian Standards Association) & Heavy Industry (MTR Focus)
* **CSA G40.20 / CSA G40.21:** General requirements for rolled or welded structural quality steel. MTRs must record chemical ladle analysis (C, Mn, P, S, Si, etc.), carbon equivalence ($CE$), tensile strength (MPa), yield strength (MPa), and Charpy V-Notch impact energy (Joules at -20°C / -45°C) for grades such as 300W, 350W, 350WT, 400W.
* **CSA B51:** Boiler, pressure vessel, and pressure piping code. Requires full heat trace numbers, mill test reports, and Canadian Registration Numbers (CRN).
* **CSA Z662:** Oil and gas pipeline systems. Material properties, pipe wall thickness, fracture toughness, and hydrostatic test reports.
* **CSA W47.1 / CSA W59:** Certification of companies for fusion welding of steel; filler material conformance certificates.

### 2.4 ASTM, ASME, AISI & International Standards
* **ASTM Standards:** ASTM A36, A572, A992, A240 (Stainless Steel), A106 (Seamless Carbon Steel Pipe), B209 (Aluminum).
* **ASME BPVC Section II:** Specifications for ferrous and non-ferrous material test properties.
* **ISO 9001:2015 & AS9100D (Aerospace):** Stringent lot/serial genealogy, first article inspection reports (FAIR - AS9102), and signed certificates of conformance with retention requirements.
* **ISO/IEC 17025:2017:** Accreditation requirements for testing and calibration laboratories issuing CoAs and MTRs.

### 2.5 Workplace Health, Safety & Environmental (WHMIS & SDS)
* **WHMIS 2015 (Hazardous Products Act & Hazardous Products Regulations):** Aligned with the Globally Harmonized System (GHS). Mandatory 16-section Safety Data Sheets (SDS) with bilingual English and Canadian French support.
* **Canadian Environmental Protection Act (CEPA 1999):** Domestic Substances List (DSL / NDSL) compliance verification.
* **Transportation of Dangerous Goods (TDG) Act:** UN number, proper shipping name, hazard class, and packing group extracted from Section 14 of the SDS.

---

## 3. Document Hierarchy & Ingestion Profiles

| Document Type | Priority Level | Target Industries | Critical Extracted Data Fields | Validation & Matching Logic |
| :--- | :--- | :--- | :--- | :--- |
| **Certificate of Analysis (CoA)** | **Primary Wedge (MVP)** | Food/Beverage, Pharma, NHPs, Chemicals, Cannabis | • Supplier, Item Name, Lot/Batch #<br>• Manufacture Date, Expiry Date<br>• Analyte/Parameter (Potency, Heavy Metals, CFU/g)<br>• Test Method (HPLC, USP, AOAC)<br>• Specified Limits (Min, Max, Target)<br>• Measured Value & Pass/Fail status | Extracted test results must fall within the Acumatica Item Quality Profile limits. Date verification against minimum shelf-life requirements. |
| **Material Test Report (MTR / MTC)** | **Secondary Module** | Steel Service Centers, Fabrication, Oil & Gas, Aerospace | • Mill Name, Heat #, Slab/Coil/Plate #<br>• Specification/Grade (CSA G40.21, ASTM A572)<br>• Chemical Analysis (% C, Mn, P, S, Si, Cr, Ni, Mo, Cu, V, CE)<br>• Mechanical Tests (Yield MPa/ksi, Tensile MPa/ksi, Elongation %, Charpy Impact Joules at temp, Hardness HBW/HRC)<br>• Heat Treatment condition | Chemical element percentages and mechanical thresholds must comply with CSA/ASTM grade specifications and customer purchase order restrictions. |
| **Certificate of Conformance (CoC)** | **Expansion Module** | Precision Machining, Aerospace, Defense, Fasteners | • Supplier Name, CAGE Code<br>• PO Number, Customer Part #, Revision #<br>• Serial/Lot Numbers, Quantity Certified<br>• Applicable Specifications (MIL-SPEC, AS9100, ISO)<br>• Authorized Signatory & Date | Exact match of Part #, Revision, PO #, and Lot # against Acumatica Purchase Receipt. Verification of compliance attestations. |
| **Safety Data Sheet (SDS)** | **Expansion Module** | Industrial Chemicals, Paints/Coatings, Mining, Manufacturing | • Product Identifier & CAS Numbers<br>• GHS Hazard Classification, Signal Word, Pictograms<br>• WHMIS 2015 16-Section Structure<br>• Canadian OELs / Provincial exposure limits<br>• TDG Classification (UN #, Packing Group) | Auto-verification of current SDS revision (within 3-year Canadian review cycle), hazardous classifications, and synchronization with Acumatica Item Safety profiles. |

---

## 4. Acumatica Cloud ERP Integration Architecture

The solution connects seamlessly to **Acumatica Cloud ERP (xRP Platform)** using modern REST APIs, Webhooks/Business Events, and contract-based integrations.

```
┌──────────────────┐       ┌───────────────────────────┐       ┌──────────────────────┐
│ Inbound CoA/MTR  │       │  AI Compliance Ingestion  │       │    Acumatica ERP     │
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
   * Listens to `POReceipt` creation events or webhook triggers when a warehouse receives goods.
   * `POReceiptLineSplit`: Fetches and validates specific Lot/Serial numbers associated with the inbound receipt line.
2. **Inventory & Lot Master (`INLotSerialStatus`):**
   * Reads the item master (`InventoryItem`), specifications, quality test classes, and custom specification tables.
   * Updates lot custom attributes (e.g., Heat Number, Melt Country, Chemical % values, Active Potency, Expiry Date, Quality Status: `Approved`, `Quarantine`, `Rejected`).
3. **Quality Management (`QMSInspectionOrder` / `QMSNonConformance`):**
   * `QMSInspectionPlan`: Queries predefined test criteria and acceptable upper/lower limits.
   * `QMSInspectionOrder`: Automatically populates measured values into inspection orders, replacing manual keyboard entry.
   * `QMSNonConformance` (NCR): Automatically generates an NCR and puts the inventory lot on hold if test values breach tolerance thresholds.
4. **Document Management & File Repository (`UploadFile`):**
   * Attaches the original PDF, parsed JSON data, and digital validation audit report directly to the Acumatica `POReceipt` and `INLotSerialStatus` records.

### 4.2 End-to-End CoA Automated Workflow

```
1. RECEIPT CREATED
   Warehouse creates PO Receipt in Acumatica -> Lot is placed in "QC Hold" -> CoA PDF captured.

2. AI EXTRACTION & RECOGNITION
   Multimodal AI extracts header data (Vendor, Item, Lot #, Expiry) and the full analytical test matrix 
   (Parameter, Test Method, Spec Min/Max, Measured Result, Unit).

3. NORMALIZATION & UNIT CONVERSION
   Standardizes variable analyte names (e.g., "Lead", "Pb", "Heavy Metals - Pb") 
   and normalizes units (e.g., ppm -> mg/kg, CFU/g, % w/w).

4. SPECIFICATION & TOLERANCE MATCHING
   Engine compares actual test results against Acumatica Quality Specs / Health Canada limits.

5. DECISION ENGINE & ERP SYNC
   ├─► ALL VALUES IN SPEC:
   │   • Updates Acumatica Inspection Order with actual test values.
   │   • Changes Lot Status from "QC Hold" to "Released/Available".
   │   • Attaches verified PDF to Lot & Purchase Receipt.
   │
   └─► OUT-OF-SPEC / CONTAMINATION DETECTED:
       • Flags lot status as "Quarantine".
       • Automatically creates Acumatica Non-Conformance Report (NCR).
       • Sends immediate high-priority alert to Quality Manager with highlighted out-of-spec test.
```

---

## 5. Technical Capabilities of the CoA Ingestion Pipeline

1. **Multimodal Layout-Aware Table Parser:**
   Handles variable multi-column tables, skewed scans, watermarks, and multi-page lab certificates without requiring rigid per-supplier templates.
2. **Chemical & Analyte Synonym Normalizer:**
   Recognizes that `As`, `Arsenic`, and `CAS 7440-38-2` refer to the same chemical entity; standardizes microbiological assay names (`Total Plate Count`, `TAMC`, `Aerobic Plate Count`).
3. **Unit Conversion & Normalization:**
   Supports bi-directional conversion between Imperial and SI Metric units, and scientific concentrations (ppm $\leftrightarrow$ mg/kg, % $\leftrightarrow$ g/100g).
4. **Bilingual Compliance Parsing (English / French):**
   Full support for Canadian bilingual CoAs and SDSs (e.g., identifying both *Numéro de lot* and *Lot Number*, *Limite d'exposition* and *Exposure Limit*).
5. **Full Auditability & Visual Provenance:**
   Every extracted data point is stored with bounding-box coordinates on the original PDF, allowing one-click visual audit verification inside the user interface.

---

## 6. Synthetic Sample Documents & Generator

To test and demonstrate the system without using proprietary client data, the platform includes a document generator capable of creating realistic Canadian-standard test documents:

1. **`coa_sample_nutraceutical_health_canada` (Core Wedge):** Natural Health Product (Echinacea Extract / Vitamin Raw Material) tested against Health Canada NHP guidelines (Heavy Metals, Microbial Limits, Assay Purity, Residual Solvents).
2. **`mtr_sample_structural_steel_csa_astm` (Secondary Module):** Mill Test Report for Structural Steel Plate certified to **CSA G40.21 Grade 350W / ASTM A572 Grade 50**, including ladle chemistry, carbon equivalent ($CE$), mechanical tensile, yield, and Charpy V-notch impact test results at -20°C.
3. **`coc_sample_aerospace_machined_parts`:** Certificate of Conformance for precision CNC machined aerospace fittings under **AS9100D / Canadian Controlled Goods Program**.
4. **`sds_sample_whmis2015_chemical`:** Fully compliant 16-section WHMIS 2015 / GHS Safety Data Sheet in bilingual Canadian format.

---

## 7. Deliverables in This Specification Package

* `specs/PROBLEM_DESCRIPTION.md`: Core problem, standards, and Acumatica ERP specification.
* `specs/COMPANY_PROFILE.md`: Reference target enterprise profile (CanNordic BioNutra Inc.).
* `specs/COA_INGESTION_SPEC.md`: Detailed engineering and API specification for the Certificate of Analysis pipeline.
* `specs/samples/`: Ready-to-use sample documents in JSON schema and formatted text/markdown.
* `specs/samples/generate_demo_documents.py`: Automated Python generator to produce realistic test/demo documents for CI/CD, unit testing, and customer demonstrations.
