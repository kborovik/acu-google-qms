# Certificate of Analysis (CoA) Ingestion Engine
## Technical Engineering & Acumatica ERP Integration Specification

---

## 1. Scope & Objective

This specification details the architecture, data schemas, normalization pipeline, tolerance evaluation engine, and Acumatica ERP integration contracts for the **Certificate of Analysis (CoA) Ingestion Engine**.

The primary objective is to automate the extraction of analytical test parameters from unstructured supplier CoA documents, validate those results against Acumatica ERP Quality Specifications, and automate inventory lot release decisions under Canadian regulatory frameworks (**Health Canada GMP / NHPR** and **CFIA SFCR**).

---

## 2. Ingestion Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CoA INGESTION PIPELINE                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
 1. DOCUMENT INGESTION                ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Inbound Channels: Email webhook, S3/GCS bucket, Acumatica Business Event│
 │ • File Formats: Multi-page PDF, Scanned TIFF/PNG/JPEG                     │
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 2. MULTIMODAL EXTRACTION             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Visual Layout & Table Extraction Engine (Vision LLM / Document AI)     │
 │ • Header Metadata: Supplier, Product Name, Lot/Batch #, Mfg/Exp Dates     │
 │ • Tabular Matrix: Parameter, Test Method, Spec Limits, Measured Value, Unit│
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 3. NORMALIZATION & STANDARDIZATION   ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Analyte Ontology Mapping (e.g., "Heavy Metals - Pb" -> "lead_pb")       │
 │ • Unit Normalization (e.g., "ppm", "mg/kg", "mcg/g" -> standard SI)       │
 │ • Date Parsing (ISO 8601 YYYY-MM-DD)                                      │
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 4. ACUMATICA SPEC MATCHING & RULES   ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Fetch Acumatica Item Profile & QMS Inspection Plan (`QMSInspectionPlan`)│
 │ • Compare Measured Values against Min / Max / Target Tolerances           │
 │ • Verify Expiry Date >= Current Date + Minimum Required Shelf Life        │
 └───────────────────────────────────────────────────────────────────────────┘
                                      │
 5. DECISION & ERP SYNCHRONIZATION    ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ • Pass: Update `QMSInspectionOrder`, flip Lot to `Released`, attach PDF   │
 │ • Fail: Update Lot to `Quarantine`, generate `QMSNonConformance` (NCR)    │
 └───────────────────────────────────────────────────────────────────────────┘
```

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
