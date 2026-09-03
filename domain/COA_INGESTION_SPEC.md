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
   * Carrier truck docks at the receiving bay. The receiving clerk inspects trailer condition, temperature compliance (for climate-controlled botanicals), container seals (e.g., tamper-evident 25 kg fiber drums), and cross-checks physical lot tags against the delivery manifest and shipping documents packet. For the complete document requirements and 3-way matching rules, see [`domain/MANDATORY_SHIPPING_DOCUMENTS_SPEC.md`](MANDATORY_SHIPPING_DOCUMENTS_SPEC.md).
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

## 5. Multi-Laboratory Document Standards & Normalization Architecture

The ingestion pipeline handles 5 dedicated testing laboratories corresponding to the 5 qualified suppliers, each operating under distinct regional document formats, measurement units, and multilingual terms:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 5-LABORATORY INTEGRATION ARCHITECTURE                                  │
├─────────────────────┬──────────────────────────┬─────────────────────────────┬─────────────────────────┤
│ SUPPLIER VENDOR     │ TESTING LABORATORY       │ DOCUMENT STANDARD           │ INBOUND LANGUAGE / UOM  │
├─────────────────────┼──────────────────────────┼─────────────────────────────┼─────────────────────────┤
│ VEND-NORTH-BIO      │ LAB-GL-ANALYTICAL        │ Health Canada HPFBI / CALA  │ • English / French      │
│ (Canada)            │ (Mississauga, ON, CA)    │ ISO/IEC 17025 (CALA #9481)  │ • % (w/w), ppm, CFU/g   │
├─────────────────────┼──────────────────────────┼─────────────────────────────┼─────────────────────────┤
│ VEND-ALPINE-EXT     │ LAB-EURO-PHYTO           │ European Pharmacopoeia      │ • German / English      │
│ (Germany)           │ (München, Bavaria, DE)   │ DIN EN ISO/IEC 17025 (DAkkS)│ • % (m/m), mg/kg, KbE/g │
├─────────────────────┼──────────────────────────┼─────────────────────────────┼─────────────────────────┤
│ VEND-PACIFIC-ORG    │ LAB-PACIFIC-TEST         │ SCC & AOAC PTM / USP        │ • English / French      │
│ (Canada/USA)        │ (Burnaby, BC, CA)        │ ISO/IEC 17025 (SCC #8172)   │ • Billion CFU/g, Aw, ppm│
├─────────────────────┼──────────────────────────┼─────────────────────────────┼─────────────────────────┤
│ VEND-NIPPON-PHARMA  │ LAB-TOKYO-BIO            │ Japanese Pharmacopoeia      │ • Japanese / English    │
│ (Japan)             │ (Chuo-ku, Tokyo, JP)     │ JP 18 / JIS / JNLA #09418   │ • mass%, ppb, deg [α]D20│
├─────────────────────┼──────────────────────────┼─────────────────────────────┼─────────────────────────┤
│ VEND-NORDIC-MAR     │ LAB-FJORD-ANALYTICAL     │ GOED Voluntary Monograph    │ • Norwegian / English   │
│ (Norway)            │ (Ålesund, Møre, NO)      │ NS-EN ISO/IEC 17025 (NA #92)│ • mg/g, meq O2/kg, p-AV │
└─────────────────────┴──────────────────────────┴─────────────────────────────┴─────────────────────────┘
```

### 5.1 Unit of Measure (UoM) Conversion Engine to Standard SI

The normalization engine converts all regional and domain-specific lab units into standard SI units before applying Acumatica QMS tolerance rules:

| Inbound Raw UoM | Source Lab Region | Target SI UoM | Mathematical Conversion Algorithm | Parameter Application |
| :--- | :--- | :--- | :--- | :--- |
| **`% (m/m)`**, **`mass%`**, **`g/100g`** | Germany / Japan | **`% (w/w)`** | $\text{value} \times 1.0$ (1:1 direct equivalence) | Botanical marker assays, active potency |
| **`mg/g`** (Fatty acids, Astaxanthin) | Norway | **`% (w/w)`** | $\text{value} / 10.0$ (e.g. $420\text{ mg/g} = 42.0\%$) | EPA, DHA, Astaxanthin concentrations |
| **`g/kg`** | Germany | **`% (w/w)`** | $\text{value} / 10.0$ | High-potency extracts |
| **`ppb`** ($\mu\text{g/kg}$) | Japan | **`ppm`** | $\text{value} / 1000.0$ (e.g. $24\text{ ppb} = 0.024\text{ ppm}$) | Trace elemental impurities (Pb, As, Cd, Hg) |
| **`mg/kg`**, **`μg/g`** | Germany / Norway / JP | **`ppm`** | $\text{value} \times 1.0$ (1:1 direct equivalence) | Heavy metals, residual solvents |
| **`KbE/g`** (Koloniebildende E.) | Germany | **`CFU/g`** | $\text{value} \times 1.0$ (1:1 direct equivalence) | TAMC (Gesamtkeimzahl), TYMC |
| **`個/g`** (生菌数) | Japan | **`CFU/g`** | $\text{value} \times 1.0$ (1:1 direct equivalence) | TAMC, TYMC |
| **`Billion CFU/g`** | Canada / USA | **`Billion CFU/g`** | Baseline Acumatica probiotic standard | Viable probiotic cell count |
| **`mmol O2/kg`** | Norway | **`meq O2/kg`** | $\text{value} \times 2.0$ | Peroxide Value (PV) |
| **`meq O2/kg`** | Norway | **`meq O2/kg`** | Baseline SI lipid oxidation unit | Peroxide Value (PV) |
| **`TOTOX` / `p-AV`** | Norway | **`index`** | $2 \times \text{PV} + \text{p-AV}$ | Total Oxidation calculation |
| **`deg (°)`** / **`度`** | Japan | **`deg (°)`** | Baseline specific optical rotation unit | Polarimetry $[\alpha]_D^{20}$ |

---

## 6. Parameter Normalization Dictionary (Multilingual Standard)

| Canonical Analyte ID | English Synonyms | French Synonyms | German Synonyms | Japanese Synonyms | Norwegian Synonyms | Standard SI Unit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`active_potency`** | Active Polyphenols, Anthocyanins, Withanolides, Curcuminoids, CoQ10, EPA/DHA | Teneur en polyphénols, Anthocyanes, Titre | Withanolid-Gesamtgehalt, Rosavine gesamt, Salidrosid | 定量法 (ユビデカレノン, L-テアニン), 含量 | Fettsyreinnhold (EPA, DHA), Rent Astaxantin | `% (w/w)` |
| **`loss_on_drying`** | Loss on Drying, Moisture, LOD, Residue on Ignition | Perte au séchage, Humidité résiduelle | Trocknungsverlust (Ph. Eur. 2.2.32), Feuchtigkeitsgehalt | 強熱残分 (JP 2.44), 乾燥減量 (JP 2.41) | Tørketap, Fuktighetsinnhold | `% (w/w)` |
| **`heavy_metal_lead`** | Lead, Pb, Elemental Lead | Plomb (Pb), Plomb élémentaire | Blei (Pb), Blei-Gehalt (DIN EN 15763) | 純度試験: 鉛 (Pb), 重金属 (Pbとして) | Bly (Pb), Blyinnhold | `ppm` |
| **`heavy_metal_arsenic`** | Arsenic, As, Total Arsenic | Arsenic (As), Arsenic total | Arsen (As), Gesamtarsen | 純度試験: ヒ素 (As), ヒ素試験法 | Arsen totalt (As), Uorganisk arsen | `ppm` |
| **`heavy_metal_cadmium`** | Cadmium, Cd | Cadmium (Cd) | Cadmium (Cd), Cadmium-Gehalt | 純度試験: カドミウム (Cd) | Kadmium (Cd) | `ppm` |
| **`heavy_metal_mercury`** | Mercury, Hg, Total Mercury | Mercure (Hg), Mercure élémentaire | Quecksilber (Hg), Quecksilber-Gehalt | 純度試験: 水銀 (Hg) | Kvikksølv (Hg), Totalkvikksølv | `ppm` |
| **`microbial_tamc`** | Total Aerobic Microbial Count, TAMC, APC | Dénombrement germes aérobies totaux | Gesamtkeimzahl (TAMC), Aerobe Keime | 生菌数試験: 一般生菌数 (TAMC) | Totalt kimtall (TAMC), Kimtall 30°C | `CFU/g` |
| **`microbial_tymc`** | Total Combined Yeast & Mold, TYMC | Dénombrement levures et moisissures | Hefen und Schimmelpilze (TYMC) | 真菌数 (カビ・酵母数 / TYMC) | Gjær og muggsopp (TYMC) | `CFU/g` |
| **`pathogen_e_coli`** | Escherichia coli (Absent in 10g) | Escherichia coli (Absence dans 10g) | E. coli (Nicht nachweisbar in 10g) | 大腸菌 (不検出 / 陰性) | Escherichia coli (Ikke påvist) | `text` |
| **`pathogen_salmonella`** | Salmonella spp. (Absent in 25g) | Salmonella spp. (Absence dans 25g) | Salmonellen (Nicht nachweisbar in 25g) | サルモネラ (不検出 / 陰性) | Salmonella spp. (Ikke påvist) | `text` |
| **`residual_solvents`** | Residual Solvents (Ethanol, Dioxins/PCBs) | Solvants résiduels (Éthanol) | Restlösemittel: Ethanol (Ph. Eur. 2.4.24) | 残留溶媒: エタノール (JP 2.46) | Dioksiner og dioksinlignende PCB | `ppm` / `pg TEQ/g` |
