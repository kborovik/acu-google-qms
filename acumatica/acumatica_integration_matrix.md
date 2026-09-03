# Acumatica Cloud ERP Quality & Integration Architecture Matrix
## Inbound Material Ingestion, QMS Tolerance Evaluation & Automated Lot Governance

---

## 1. System Architecture Overview

The Acumatica Cloud ERP integration layer connects the **Certificate of Analysis (CoA) Ingestion Engine** with Acumatica's **Inventory Management (IN)**, **Purchase Orders (PO)**, and **Quality Management System (QMS)** modules.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              ACUMATICA INBOUND QUALITY CONTROL BUS                                     │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 1. DOCK ARRIVAL & PO RECEIPT                       ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Inbound shipment arrives at warehouse dock from one of 5 qualified suppliers.                      │
 │ • Clerk posts `POReceipt` with line splits (`POReceiptLineSplit`).                                   │
 │ • Acumatica sets `INLotSerialStatus.LotStatus = 'QC Hold'`.                                          │
 │ • Material locked: Cannot be allocated to BOMs or Work Orders.                                       │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 2. MULTI-LAB CoA DOCUMENT INGESTION                ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Ingests CoA from 5 dedicated global testing laboratories with distinct standards:                  │
 │   - LAB-GL-ANALYTICAL: Health Canada / CALA Standard (Bilingual EN/FR)                               │
 │   - LAB-EURO-PHYTO: Ph. Eur. / DIN Prüfbericht Standard (Bilingual DE/EN)                            │
 │   - LAB-PACIFIC-TEST: SCC & AOAC PTM / USP Standard (Bilingual EN/FR)                                │
 │   - LAB-TOKYO-BIO: Japanese Pharmacopoeia (JP 18) / JIS 試験成績書 Standard (Bilingual JA/EN)       │
 │   - LAB-FJORD-ANALYTICAL: GOED Monograph & Marine Lipid Analysesertifikat (Bilingual NO/EN)          │
 │ • Multilingual layout parser normalizes terms and converts heterogeneous UoMs into standard SI.      │
 │ • Visual bounding boxes `[x_min, y_min, x_max, y_max]` recorded for 1-click audit verification.       │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 3. SPECIFICATION & TOLERANCE MATCHING ENGINE       ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Ingestion Engine queries Acumatica `QMSInspectionPlan` via REST API.                               │
 │ • Compares normalized assay, heavy metals (Pb, As, Cd, Hg), microbial CFUs against tolerances.       │
 │ • Validates remaining shelf life: `ExpiryDate >= ReceivingDate + MinShelfLifeDays`.                  │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 4. AUTOMATED ERP GOVERNANCE DECISION               ▼
                    ├─────────────────────────────────────────────────┐
                    │                                                 │
          [ALL PARAMETERS PASS]                             [OUT-OF-SPECIFICATION (OOS)]
                    │                                                 │
                    ▼                                                 ▼
 ┌──────────────────────────────────────┐          ┌──────────────────────────────────────┐
 │ • `QMSInspectionOrder`: Set 'Pass'   │          │ • `QMSInspectionOrder`: Set 'Fail'   │
 │ • `INLotSerialStatus`: 'Released'    │          │ • `INLotSerialStatus`: 'Quarantine'  │
 │ • Production Work Orders unblocked   │          │ • `QMSNonConformance` (NCR) raised   │
 │ • PDF & JSON archived on Lot record  │          │ • QA Manager alerted for root-cause  │
 │ • Physical green placards affixed    │          │ • Pallet moved to locked quarantine  │
 └──────────────────────────────────────┘          └──────────────────────────────────────┘
```

---

## 2. Acumatica REST API Endpoints & Contracts

### 2.1 Entity Contracts Summary

| Entity | Contract Version | HTTP Verb | Purpose |
| :--- | :--- | :--- | :--- |
| `POReceipt` | `Default/22.200.001` | `GET` | Fetch inbound PO receipt lines, lot numbers, and vendor ID |
| `InventoryItem` | `Default/22.200.001` | `GET` | Retrieve item master specifications, item class, and QMS plan ID |
| `QMSInspectionPlan` | `QMS/22.200.001` | `GET` | Query target tolerances, analytical test methods, and min/max limits |
| `QMSInspectionOrder` | `QMS/22.200.001` | `PUT / POST`| Populate actual test results extracted from supplier/lab CoA |
| `INLotSerialStatus` | `Default/22.200.001` | `PUT` | Flip lot status between `QC Hold`, `Released`, `Quarantine`, `Rejected` |
| `QMSNonConformance` | `QMS/22.200.001` | `POST` | Automatically open NCR ticket upon tolerance or contaminant breach |
| `UploadFile` | `Default/22.200.001` | `PUT` | Attach original CoA PDF and parsed JSON audit report to Lot/Receipt |

---

## 3. Detailed REST API Payload Specifications

### 3.1 Fetch Inbound PO Receipt & Lot Split Details
```http
GET /entity/Default/22.200.001/POReceipt?$filter=ReceiptNbr eq 'PR-2026-00412'&$expand=ReceiptDetails,ReceiptDetails/Allocations HTTP/1.1
Host: bionutra.acumatica.com
Authorization: Bearer {{oauth_token}}
Accept: application/json
```

**Response Payload:**
```json
{
  "ReceiptNbr": { "value": "PR-2026-00412" },
  "VendorID": { "value": "VEND-NORTH-BIO" },
  "ReceiptDate": { "value": "2026-03-01T10:30:00Z" },
  "Status": { "value": "Open" },
  "Details": [
    {
      "LineNbr": { "value": 1 },
      "InventoryID": { "value": "RAW-ECH-EXT4" },
      "ReceiptQty": { "value": 500.0 },
      "UOM": { "value": "KG" },
      "Allocations": [
        {
          "SplitLineNbr": { "value": 1 },
          "LotSerialNbr": { "value": "LOT-EC2603-01A" },
          "Qty": { "value": 500.0 },
          "ExpirationDate": { "value": "2029-02-28" },
          "Location": { "value": "QC-HOLD-BAY-A" }
        }
      ]
    }
  ]
}
```

---

### 3.2 Populate QMS Inspection Order with Extracted Lab Results
```http
PUT /entity/QMS/22.200.001/InspectionOrder HTTP/1.1
Host: bionutra.acumatica.com
Authorization: Bearer {{oauth_token}}
Content-Type: application/json

{
  "InspectionOrderNbr": { "value": "<AUTO_ASSIGNED_OR_EMPTY>" },
  "InventoryID": { "value": "RAW-ECH-EXT4" },
  "LotSerialNbr": { "value": "LOT-EC2603-01A" },
  "VendorID": { "value": "VEND-NORTH-BIO" },
  "ReceiptNbr": { "value": "PR-2026-00412" },
  "InspectionPlanID": { "value": "QPLAN-BOT-ECH4" },
  "TestingLabID": { "value": "LAB-GL-ANALYTICAL" },
  "LabCertificateNbr": { "value": "COA-GL-2026-09182" },
  "InspectionDate": { "value": "2026-03-01" },
  "OverallEvaluation": { "value": "Pass" },
  "Results": [
    {
      "StepNbr": { "value": 10 },
      "TestID": { "value": "ASSAY_POLYPHENOLS" },
      "TestMethod": { "value": "HPLC-DAD (USP Monograph)" },
      "TargetSpec": { "value": ">= 4.00 % (w/w)" },
      "ActualNumericValue": { "value": 4.28 },
      "ActualTextValue": { "value": "4.28 % (w/w)" },
      "Evaluation": { "value": "Pass" }
    },
    {
      "StepNbr": { "value": 20 },
      "TestID": { "value": "PHYS_LOD" },
      "TestMethod": { "value": "USP <731>" },
      "TargetSpec": { "value": "<= 5.00 % (w/w)" },
      "ActualNumericValue": { "value": 3.82 },
      "ActualTextValue": { "value": "3.82 %" },
      "Evaluation": { "value": "Pass" }
    },
    {
      "StepNbr": { "value": 30 },
      "TestID": { "value": "HM_LEAD" },
      "TestMethod": { "value": "ICP-MS (USP <2232>)" },
      "TargetSpec": { "value": "<= 0.50 ppm" },
      "ActualNumericValue": { "value": 0.084 },
      "ActualTextValue": { "value": "0.084 ppm" },
      "Evaluation": { "value": "Pass" }
    },
    {
      "StepNbr": { "value": 40 },
      "TestID": { "value": "HM_ARSENIC" },
      "TestMethod": { "value": "ICP-MS (USP <2232>)" },
      "TargetSpec": { "value": "<= 1.00 ppm" },
      "ActualNumericValue": { "value": 0.120 },
      "ActualTextValue": { "value": "0.120 ppm" },
      "Evaluation": { "value": "Pass" }
    },
    {
      "StepNbr": { "value": 70 },
      "TestID": { "value": "MICRO_TAMC" },
      "TestMethod": { "value": "USP <2021>" },
      "TargetSpec": { "value": "<= 10000 CFU/g" },
      "ActualNumericValue": { "value": 420.0 },
      "ActualTextValue": { "value": "420 CFU/g" },
      "Evaluation": { "value": "Pass" }
    },
    {
      "StepNbr": { "value": 90 },
      "TestID": { "value": "PATH_ECOLI" },
      "TestMethod": { "value": "USP <2022>" },
      "TargetSpec": { "value": "Absent in 10g" },
      "ActualTextValue": { "value": "Absent in 10g" },
      "Evaluation": { "value": "Pass" }
    }
  ]
}
```

---

### 3.3 Lot Status Governor: Release Material to Production
```http
PUT /entity/Default/22.200.001/INLotSerialStatus HTTP/1.1
Host: bionutra.acumatica.com
Authorization: Bearer {{oauth_token}}
Content-Type: application/json

{
  "InventoryID": { "value": "RAW-ECH-EXT4" },
  "LotSerialNbr": { "value": "LOT-EC2603-01A" },
  "LotStatus": { "value": "Released" },
  "Location": { "value": "RACK-A-04-02" },
  "ExpiryDate": { "value": "2029-02-28" }
}
```

---

### 3.4 Non-Conformance Reporting (NCR) for Failed / Out-of-Spec Lots
```http
POST /entity/QMS/22.200.001/NonConformance HTTP/1.1
Host: bionutra.acumatica.com
Authorization: Bearer {{oauth_token}}
Content-Type: application/json

{
  "NCRNbr": { "value": "<AUTO_ASSIGNED>" },
  "InventoryID": { "value": "RAW-ECH-EXT4" },
  "LotSerialNbr": { "value": "LOT-EC2603-01A" },
  "VendorID": { "value": "VEND-NORTH-BIO" },
  "ReceiptNbr": { "value": "PR-2026-00412" },
  "Severity": { "value": "Critical" },
  "NonConformanceType": { "value": "Chemical Contamination / Heavy Metals" },
  "AssignedQAOfficer": { "value": "elodie.tremblay@cannordicbionutra.ca" },
  "RootCauseCategory": { "value": "Supplier Raw Material Contamination" },
  "Description": {
    "value": "CRITICAL OOS: Inbound Lot LOT-EC2603-01A failed Heavy Metal Lead (Pb) specification. Measured: 0.82 ppm (Limit: <= 0.50 ppm per Health Canada NHP Regulations SOR/2003-196). Lot locked in Quarantine; NCR initiated for supplier chargeback and return-to-vendor (RTV)."
  },
  "ActionRequired": { "value": "Quarantine Segregation & RTV Claim" },
  "InventoryHoldStatus": { "value": "Quarantine" }
}
```

---

## 4. Lot Status State Machine & Workflow Transitions

```
                    ┌─────────────────────────┐
                    │    PO RECEIPT DOCK      │
                    │       (Arrival)         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
         ┌─────────▶│         QC HOLD         │◀─────────┐
         │          │  (Quarantine Physical)  │          │
         │          └────────────┬────────────┘          │
         │                       │                       │
         │          ┌────────────┴────────────┐          │
Re-test  │          │   AI Spec Verification  │          │ Dispute
Requested│          └─────┬─────────────┬─────┘          │ Review
         │                │             │                │
         │     Passes All │             │ Out-of-Spec    │
         │                ▼             ▼                │
         │      ┌───────────────┐ ┌───────────────┐      │
         └──────│   RELEASED    │ │  QUARANTINE   │──────┘
                │(Available BOM)│ │  (NCR Raised) │
                └───────────────┘ └───────┬───────┘
                                          │
                                 Reject / │ Return to Vendor
                                          ▼
                                ┌───────────────────┐
                                │     REJECTED      │
                                │ (RTV / Destroyed) │
                                └───────────────────┘
```

### 4.1 State Definitions & Permissions

| Lot State | ERP System Code | Material Allocation Permitted | Description |
| :--- | :--- | :--- | :--- |
| **QC Hold** | `HOLD` | **NO** | Default arrival state. Material is physically quarantined on receiving docks awaiting CoA ingestion and QA sign-off. |
| **Released** | `RELEASED` | **YES** | All test criteria verified within tolerances. Inventory is unblocked and freely consumed in Manufacturing BOMs. |
| **Quarantine** | `QUARANTINE` | **NO** | Test results breached specification or regulatory limits. NCR opened. Pallet moved to locked physical quarantine bay. |
| **Rejected** | `REJECTED` | **NO** | Material definitively condemned for Return to Vendor (RTV) or bio-hazardous destruction. Inventory written off. |

---

## 5. Automated Multi-Lab Ingestion & Normalization Matrix

Each qualified vendor routes analytical certifications through a dedicated laboratory partner with distinct regional document standards, measurement units, and terminology:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               5 VENDORS <-> 5 LABORATORIES INTEGRATION TOPOLOGY                                   │
├─────────────────────┬──────────────────────────┬─────────────────────────────┬────────────────────────────────────┤
│ SUPPLIER VENDOR     │ TESTING LABORATORY       │ DOCUMENT STANDARD           │ NORMALIZATION PROFILE              │
├─────────────────────┼──────────────────────────┼─────────────────────────────┼────────────────────────────────────┤
│ VEND-NORTH-BIO      │ LAB-GL-ANALYTICAL        │ Health Canada / CALA        │ • Standard Canadian Bilingual      │
│ (Canada - Botanical)│ (Mississauga, ON, CA)    │ ISO/IEC 17025 (CALA #9481)  │ • UoMs: % (w/w), ppm, CFU/g        │
├─────────────────────┼──────────────────────────┼─────────────────────────────┼────────────────────────────────────┤
│ VEND-ALPINE-EXT     │ LAB-EURO-PHYTO           │ European Pharmacopoeia      │ • German / English (Prüfbericht)   │
│ (Germany - Root Ext)│ (München, Bavaria, DE)   │ DIN EN ISO 17025 (DAkkS)    │ • UoMs: % (m/m) -> % (w/w),        │
│                     │                          │ Ph. Eur. 11th Edition       │   mg/kg -> ppm, KbE/g -> CFU/g     │
├─────────────────────┼──────────────────────────┼─────────────────────────────┼────────────────────────────────────┤
│ VEND-PACIFIC-ORG    │ LAB-PACIFIC-TEST         │ SCC & AOAC PTM / USP        │ • West Coast Probiotics / Solvents │
│ (Canada/USA - Bio)  │ (Burnaby, BC, CA)        │ ISO/IEC 17025 (SCC #8172)   │ • UoMs: Billion CFU/g, Aw, ppm     │
├─────────────────────┼──────────────────────────┼─────────────────────────────┼────────────────────────────────────┤
│ VEND-NIPPON-PHARMA  │ LAB-TOKYO-BIO            │ Japanese Pharmacopoeia      │ • Japanese / English (試験成績書)  │
│ (Japan - API Ferm)  │ (Chuo-ku, Tokyo, JP)     │ JP 18 / JIS / JNLA #09418   │ • UoMs: mass% -> % (w/w),          │
│                     │                          │ PMDA JP-PMDA-LAB-2024-819   │   ppb -> ppm (/1000), deg [α]D20   │
├─────────────────────┼──────────────────────────┼─────────────────────────────┼────────────────────────────────────┤
│ VEND-NORDIC-MAR     │ LAB-FJORD-ANALYTICAL     │ GOED Voluntary Monograph    │ • Norwegian / English (Analysesert)│
│ (Norway - Marine)   │ (Ålesund, Møre, NO)      │ NS-EN ISO 17025 (NA #92)    │ • UoMs: mg/g -> % (w/w) (/10),     │
│                     │                          │ Mattilsynet NO-HACCP-9481   │   meq O2/kg, p-AV/TOTOX, pg TEQ/g  │
└─────────────────────┴──────────────────────────┴─────────────────────────────┴────────────────────────────────────┘
```

### 5.1 Unit of Measure Conversion Engine (to Standard SI)

```
[Inbound Heterogeneous Lab Values]
  ├─ mg/kg, μg/g (DE, NO, JP) ──────────▶ [1:1 Direct] ─────────▶ ppm
  ├─ ppb / μg/kg (JP) ──────────────────▶ [/ 1000.0] ───────────▶ ppm
  ├─ % (m/m), mass%, g/100g (DE, JP) ───▶ [1:1 Direct] ─────────▶ % (w/w)
  ├─ mg/g fatty acids/actives (NO) ─────▶ [/ 10.0] ─────────────▶ % (w/w)
  ├─ KbE/g (DE) / 個/g (JP) ────────────▶ [1:1 Direct] ─────────▶ CFU/g
  ├─ mmol O2/kg (NO) ───────────────────▶ [* 2.0] ──────────────▶ meq O2/kg
  └─ Billion CFU/g (CA/US) ─────────────▶ [* 1.0e9 / 100.0 GCFU]▶ Acumatica Probiotic Standard
```

### 5.2 Multilingual Analyte Normalization Matrix

| Canonical Entity | English Synonyms | German Synonyms | Japanese Synonyms | Norwegian Synonyms | French Synonyms |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`active_potency`** | Active Polyphenols, Anthocyanins, Withanolides, Curcuminoids, CoQ10, EPA/DHA | Withanolid-Gesamtgehalt, Rosavine gesamt, Salidrosid | 定量法 (ユビデカレノン, L-テアニン), 純度試験 | Fettsyreinnhold (EPA, DHA), Rent Astaxantin | Teneur en polyphénols, Titre actif |
| **`loss_on_drying`** | Loss on Drying, Moisture, LOD, Residue on Ignition | Trocknungsverlust (Ph. Eur. 2.2.32), Feuchtigkeitsgehalt | 強熱残分 (JP 2.44), 乾燥減量 (JP 2.41) | Tørketap, Fuktighetsinnhold | Perte au séchage, Humidité résiduelle |
| **`heavy_metal_lead`** | Lead, Pb, Elemental Lead | Blei (Pb), Blei-Gehalt (DIN EN 15763) | 純度試験: 鉛 (Pb), 重金属 (Pb) | Bly (Pb), Blyinnhold | Plomb (Pb), Plomb élémentaire |
| **`heavy_metal_arsenic`** | Arsenic, As, Total Arsenic | Arsen (As), Gesamtarsen | 純度試験: ヒ素 (As), ヒ素試験法 | Arsen totalt (As), Uorganisk arsen | Arsenic (As), Arsenic total |
| **`microbial_tamc`** | Total Aerobic Microbial Count, TAMC, Plate Count | Gesamtkeimzahl (TAMC), Aerobe mesophile Keime | 生菌数試験: 一般生菌数 (TAMC) | Totalt kimtall (TAMC), Kimtall 30°C | Dénombrement germes aérobies totaux |
| **`microbial_tymc`** | Total Combined Yeast & Mold, TYMC | Hefen und Schimmelpilze (TYMC) | 真菌数 (カビ・酵母数 / TYMC) | Gjær og muggsopp (TYMC) | Dénombrement levures et moisissures |
| **`pathogen_e_coli`** | Escherichia coli (Absent) | E. coli (Nicht nachweisbar) | 大腸菌 (陰性 / 不検出) | Escherichia coli (Ikke påvist) | Escherichia coli (Absence) |
| **`pathogen_salmonella`**| Salmonella spp. (Absent) | Salmonellen (Nicht nachweisbar) | サルモネラ (陰性 / 不検出) | Salmonella spp. (Ikke påvist) | Salmonella spp. (Absence) |
| **`residual_solvents`** | Residual Solvents (Ethanol, Dioxins/PCBs) | Restlösemittel: Ethanol (Ph. Eur. 2.4.24) | 残留溶媒: エタノール (JP 2.46) | Dioksiner og dioksinlignende PCB | Solvants résiduels (Éthanol) |
