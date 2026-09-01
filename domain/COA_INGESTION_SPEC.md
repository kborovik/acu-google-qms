# Certificate of Analysis (CoA) Ingestion Engine
## Technical Engineering & Acumatica ERP Integration Specification

---

## 1. Scope & Objective

This specification details the architecture, data schemas, normalization pipeline, tolerance evaluation engine, and Acumatica ERP integration contracts for the **Certificate of Analysis (CoA) Ingestion Engine**.

The primary objective is to automate the extraction of analytical test parameters from unstructured supplier CoA documents, validate those results against Acumatica ERP Quality Specifications, and automate inventory lot release decisions under Canadian regulatory frameworks (**Health Canada GMP / NHPR** and **CFIA SFCR**).

---

## 2. Ingestion Pipeline Architecture & Receiving Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CoA INSPECTION & RECEIVING WORKFLOW                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
 1. PHYSICAL DOCK ARRIVAL             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Truck docks at warehouse; clerk checks seals, packaging & lot labels.   │
 │ • Clerk registers `POReceipt` & `POReceiptLineSplit` in Acumatica ERP.    │
 │ • Acumatica immediately marks lot status as "QC Hold" (Quarantine).       │
 │ • Physical pallets are staged in quarantine bay with yellow QC Hold tags. │
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 2. CoA DOCUMENT CAPTURE              ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Supplier CoA PDF is captured via dock scanner, email, or vendor portal. │
 │ • Pipeline matches document to Vendor, PO Receipt line, and Lot Number.   │
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 3. MULTIMODAL AI PARSING & NORMALIZATION ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Vision/Layout parser extracts test matrix (Assays, Heavy Metals, CFUs). │
 │ • Bilingual terms & synonyms normalized (e.g., Plomb/Pb -> heavy_metal_pb)│
 │ • Units converted to standard SI (ppm <-> mg/kg, % w/w, CFU/g).           │
 │ • Visual provenance bounding boxes (x, y, w, h) captured for audit.       │
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 4. SPECIFICATION & TOLERANCE MATCHING ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Engine queries Acumatica `QMSInspectionPlan` for expected item specs.   │
 │ • Evaluates every analyte against Health Canada limits & internal ranges. │
 │ • Validates remaining shelf-life against Expiration Date.                 │
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 5. AUTOMATED ERP DECISION & LOT GOVERNOR ▼
          ├───────────────────────────────────────────┐
          │ ALL IN-SPEC                               │ OUT-OF-SPEC / CONTAMINATION
          ▼                                           ▼
 ┌──────────────────────────────────┐        ┌──────────────────────────────────┐
 │ • `QMSInspectionOrder` completed │        │ • Lot flagged as "Quarantine"    │
 │ • Lot status flipped: "Released" │        │ • Acumatica NCR ticket generated │
 │ • Unblocked for production work  │        │ • QA Manager alerted immediately │
 │ • PDF attached to ERP Lot record │        │ • Pallet moved to locked storage │
 └──────────────────────────────────┘        └──────────────────────────────────┘
```

### 2.1 Receiving Dock Arrival & Physical/Digital Hand-off
1. **Physical Unloading & Verification:**
   * Carrier truck docks at the receiving bay. The receiving clerk inspects trailer condition, temperature compliance (for climate-controlled botanicals), container seals (e.g., tamper-evident 25 kg fiber drums), and cross-checks physical lot tags against the delivery manifest.
2. **Inbound ERP Registration (`POReceipt`):**
   * The clerk opens Acumatica Cloud ERP and creates or confirms a `POReceipt` linked to the inbound Purchase Order.
   * Lot details (`LotSerialNbr`, batch quantity, container count, manufacturer expiration date) are registered via `POReceiptLineSplit`.
3. **Mandatory Regulatory Quarantine Lock ("QC Hold"):**
   * Under **Health Canada GMP (GUI-0001 / GUI-0158)** and **CFIA Safe Food for Canadians Regulations**, raw botanical extracts and active ingredients **cannot be released into production or blending** prior to analytical inspection and formal QC authorization.
   * Acumatica automatically assigns initial state `INLotSerialStatus.LotStatus = 'QC Hold'`. The ERP enforces an automated hard stop preventing any production Work Order or blending recipe from consuming the inventory lot.
   * Physical pallets are tagged with yellow `QC HOLD` placards and staged in the receiving quarantine bay.

### 2.2 Inbound CoA Capture & PO Association
* **Ingestion Channels:** The Certificate of Analysis PDF is acquired through:
  * Dock Scanner: Clerks scan the paper CoA included in the packing slip pouch.
  * Inbound Email Webhook: Automated ingestion of digital PDF CoAs sent by suppliers prior to shipment.
  * Supplier Portal Upload: Direct upload by pre-qualified vendors into the platform API.
* **Entity Association:** The ingestion engine correlates the document header with Acumatica records:
  * `VendorID` (e.g., `VEND-NORTH-BIO`)
  * `InventoryID` (e.g., `RAW-ECH-EXT4`)
  * `LotSerialNbr` (e.g., `LOT-EC2602-09A`)
  * `ReceiptNbr` (e.g., `PR-2026-00412`)

### 2.3 Automated Analytical Inspection Pipeline
The inspection engine performs automated four-layer verification:
1. **Multimodal Layout & Table Extraction:**
   * Extracts header metadata (Product Name, Botanical Name, Lot #, Mfg Date, Expiry Date, Testing Lab Accreditation).
   * Extracts tabular test matrix: Raw parameter name, analytical method (HPLC, ICP-MS, USP <2021>), target specifications (Min/Max), and measured values.
   * Records bounding-box coordinates (`page`, `x_min`, `y_min`, `x_max`, `y_max`) for every extracted data cell for 1-click visual audit verification.
2. **Semantic Ontology & Unit Normalization:**
   * Normalizes multilingual synonyms and abbreviations (e.g., *Plomb*, *Pb*, *Heavy Metals (as Pb)* $\longrightarrow$ `heavy_metal_lead`).
   * Normalizes diverse analytical units into SI standards (e.g., $\text{ppm} \leftrightarrow \text{mg/kg} \leftrightarrow \mu\text{g/g}$, $\% \text{ w/w} \leftrightarrow \text{g/100g}$).
   * Standardizes text qualifiers (`ND`, `Not Detected`, `< 10 CFU/g`, `Absent in 10g`, `Conforms`).
3. **Specification Matching & Tolerance Evaluation:**
   * Retrieves predefined quality limits from the item's Acumatica `QMSInspectionPlan`.
   * Evaluates each parameter against Health Canada Category 1 limits and internal product tolerances:
     * **Active Potency & Assays:** e.g., Total Polyphenols $\ge 4.00\%$ (HPLC).
     * **Heavy Metal Contaminants (ICP-MS):** Lead (Pb) $\le 0.50$ ppm, Arsenic (As) $\le 1.00$ ppm, Cadmium (Cd) $\le 0.30$ ppm, Mercury (Hg) $\le 0.10$ ppm.
     * **Microbiological Thresholds (USP <2021>/<2022>):** TAMC $\le 10^4$ CFU/g, TYMC $\le 10^3$ CFU/g, *E. coli* & *Salmonella* absent.
     * **Physical/Chemical Assays:** Loss on Drying $\le 5.00\%$ (USP <731>), Residual Solvents (USP <467>).
     * **Shelf-Life Governor:** Verifies Expiry Date $\ge \text{Current Date} + \text{Minimum Required Shelf Life}$ (e.g., 24 months).

### 2.4 Decision Engine & ERP State Machine
* **Branch A: All Parameters Pass (Approved)**
  1. `QMSInspectionOrder`: Populated in Acumatica with all measured values, test methods, and individual `Pass` ratings.
  2. `INLotSerialStatus`: Lot status automatically flipped from `QC Hold` $\longrightarrow$ **`Released`**.
  3. Manufacturing Unblocked: Inventory is instantly available for BOM allocation and production batching.
  4. Physical Move: Warehouse crew replaces yellow hold tag with green `RELEASED` tag and moves pallets to active racking.
  5. Audit Storage: Ingested PDF and normalized JSON validation payload are attached to `POReceipt` and lot master via `/files` API.
* **Branch B: Out-of-Specification / Contaminant Failure (Rejected / NCR)**
  1. `INLotSerialStatus`: Lot status remains or updates to **`Quarantine`** / **`Rejected`**; inventory hard-lock maintained.
  2. `QMSNonConformance` (NCR): Automatic NCR record generated with breach details, severity (`Critical`), and measured vs. threshold values.
  3. QA Escalation: Instant high-priority alert dispatched to Quality Assurance Manager.
  4. Physical Quarantine: Pallet tagged with red `REJECTED` placard and moved to locked quarantine cage pending Return to Vendor (RTV) or vendor dispute.
* **Branch C: Indeterminate / Low Extraction Confidence**
  1. Routed to QA review inbox with side-by-side document provenance viewer for 1-click human verification.

### 2.5 Operational Comparison: Manual Baseline vs. Automated Pipeline

| Metric | Manual Inspection (Status Quo) | Automated AI Ingestion Pipeline |
| :--- | :--- | :--- |
| **Inspection Time per CoA** | 25 – 45 minutes manual re-keying | < 10 seconds end-to-end |
| **Dock-to-Stock Latency** | 24 – 48 hours quarantine hold | Instantaneous release upon arrival |
| **Transcription Risk** | High (decimal shifts, unit confusion) | 0% transcription error |
| **Audit Readiness** | Fragmented paper binders / email attachments | 1-click PDF bounding-box provenance in ERP |

---

## 3. Canonical CoA Data Schema (JSON)

Every ingested document is normalized into the following canonical JSON schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NormalizedCoA",
  "type": "object",
  "required": [
    "document_id",
    "supplier",
    "product",
    "lot_number",
    "test_results",
    "evaluation_summary"
  ],
  "properties": {
    "document_id": { "type": "string" },
    "issued_date": { "type": "string", "format": "date" },
    "supplier": {
      "type": "object",
      "properties": {
        "raw_name": { "type": "string" },
        "acumatica_vendor_id": { "type": "string" },
        "accreditation": { "type": "string" }
      }
    },
    "product": {
      "type": "object",
      "properties": {
        "product_name": { "type": "string" },
        "acumatica_inventory_id": { "type": "string" },
        "botanical_scientific_name": { "type": "string" }
      }
    },
    "lot_number": { "type": "string" },
    "batch_size_kg": { "type": ["number", "null"] },
    "manufacturing_date": { "type": ["string", "null"], "format": "date" },
    "expiry_date": { "type": ["string", "null"], "format": "date" },
    "test_results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["canonical_parameter", "measured_value", "status"],
        "properties": {
          "raw_parameter_name": { "type": "string" },
          "canonical_parameter": { 
            "type": "string",
            "enum": [
              "active_potency",
              "loss_on_drying",
              "heavy_metal_lead",
              "heavy_metal_arsenic",
              "heavy_metal_cadmium",
              "heavy_metal_mercury",
              "microbial_tamc",
              "microbial_tymc",
              "pathogen_e_coli",
              "pathogen_salmonella",
              "residual_solvents",
              "pesticide_residues",
              "ph_value",
              "density_specific_gravity",
              "other_custom_assay"
            ]
          },
          "test_method": { "type": "string" },
          "specification_min": { "type": ["number", "null"] },
          "specification_max": { "type": ["number", "null"] },
          "target_unit": { "type": "string" },
          "measured_value_raw": { "type": ["string", "number"] },
          "measured_value_numeric": { "type": ["number", "null"] },
          "status": { "type": "string", "enum": ["PASS", "FAIL", "INDETERMINATE"] },
          "confidence_score": { "type": "number", "minimum": 0, "maximum": 1.0 },
          "provenance_bounding_box": {
            "type": "object",
            "properties": {
              "page": { "type": "integer" },
              "x_min": { "type": "number" },
              "y_min": { "type": "number" },
              "x_max": { "type": "number" },
              "y_max": { "type": "number" }
            }
          }
        }
      }
    },
    "evaluation_summary": {
      "type": "object",
      "properties": {
        "overall_status": { "type": "string", "enum": ["APPROVED", "REJECTED", "MANUAL_REVIEW_REQUIRED"] },
        "discrepancy_count": { "type": "integer" },
        "reasons": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

---

## 4. Acumatica REST API Mapping & Integration Flow

### 4.1 Endpoints & Entity Interactions

1. **Query Inbound PO Receipts:**
   ```http
   GET /entity/Default/22.200.001/POReceipt?$filter=ReceiptNbr eq '{receipt_nbr}'&$expand=ReceiptDetails
   ```
   * Retrieves line items, expected Lot numbers, and attached Item IDs.

2. **Query Item Quality Specifications:**
   ```http
   GET /entity/Default/22.200.001/InventoryItem?$filter=InventoryID eq '{item_id}'&$expand=Attributes
   ```
   * Queries configured inspection plans, tolerance limits, and minimum required shelf life.

3. **Populate QMS Inspection Order:**
   ```http
   PUT /entity/QMS/22.200.001/InspectionOrder
   Content-Type: application/json

   {
     "InspectionOrderNbr": { "value": "{inspection_nbr}" },
     "Results": [
       {
         "ParameterID": { "value": "LEAD_PB" },
         "ActualValue": { "value": 0.08 },
         "Evaluation": { "value": "Pass" }
       },
       {
         "ParameterID": { "value": "POTENCY" },
         "ActualValue": { "value": 4.32 },
         "Evaluation": { "value": "Pass" }
       }
     ]
   }
   ```

4. **Update Lot Status (Release vs. Quarantine):**
   ```http
   PUT /entity/Default/22.200.001/INLotSerialStatus
   Content-Type: application/json

   {
     "InventoryID": { "value": "RAW-ECH-EXT4" },
     "LotSerialNbr": { "value": "LOT-EC2602-09A" },
     "LotStatus": { "value": "Released" },
     "ExpiryDate": { "value": "2029-01-31" }
   }
   ```

5. **Generate Non-Conformance Report (NCR) on Failure:**
   ```http
   POST /entity/QMS/22.200.001/NonConformance
   Content-Type: application/json

   {
     "InventoryID": { "value": "RAW-ECH-EXT4" },
     "LotSerialNbr": { "value": "LOT-EC2602-09A" },
     "VendorID": { "value": "VEND-NORTH-BIO" },
     "Severity": { "value": "Critical" },
     "Reason": { "value": "Heavy metal Lead (Pb) measured 0.85 ppm exceeds allowable maximum of 0.50 ppm under Health Canada NHP Regulations." }
   }
   ```

6. **Attach Original Verified PDF to Receipt and Lot:**
   ```http
   PUT /entity/Default/22.200.001/POReceipt/{receipt_nbr}/files/{filename.pdf}
   Content-Type: application/pdf
   ```

---

## 5. Parameter Normalization Dictionary (Canadian Standard)

| Raw Synonym in Document | Canonical Analyte ID | Standard Unit | Health Canada / USP Limit Reference |
| :--- | :--- | :--- | :--- |
| `Lead`, `Pb`, `Plomb`, `Heavy Metals (as Pb)` | `heavy_metal_lead` | `ppm` (mg/kg) | $\le 0.50$ ppm (NHP Category 1) |
| `Arsenic`, `As`, `Arsenic total` | `heavy_metal_arsenic` | `ppm` (mg/kg) | $\le 1.00$ ppm (NHP Category 1) |
| `Cadmium`, `Cd` | `heavy_metal_cadmium` | `ppm` (mg/kg) | $\le 0.30$ ppm (NHP Category 1) |
| `Mercury`, `Hg`, `Mercure` | `heavy_metal_mercury` | `ppm` (mg/kg) | $\le 0.10$ ppm (NHP Category 1) |
| `Total Aerobic Count`, `TAMC`, `TPC`, `APC` | `microbial_tamc` | `CFU/g` | $\le 10,000$ CFU/g (USP <2021>) |
| `Yeast and Mold`, `TYMC`, `Y&M` | `microbial_tymc` | `CFU/g` | $\le 1,000$ CFU/g (USP <2021>) |
| `E. coli`, `Escherichia coli` | `pathogen_e_coli` | `text` | Absent in 10g (USP <2022>) |
| `Salmonella`, `Salmonella spp.` | `pathogen_salmonella` | `text` | Absent in 25g (USP <2022>) |
| `Loss on Drying`, `Moisture`, `LOD`, `Humidité` | `loss_on_drying` | `%` | $\le 5.0$ % (USP <731>) |
| `Total Cannabinoids`, `THC`, `Total CBD` | `active_potency` | `% (w/w)` | Label Claim $\pm 10\%$ (SOR/2018-144) |
