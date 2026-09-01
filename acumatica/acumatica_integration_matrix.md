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
 │ • Inbound shipment arrives at warehouse dock.                                                        │
 │ • Clerk posts `POReceipt` with line splits (`POReceiptLineSplit`).                                   │
 │ • Acumatica sets `INLotSerialStatus.LotStatus = 'QC Hold'`.                                          │
 │ • Material locked: Cannot be allocated to BOMs or Work Orders.                                       │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 2. CoA DOCUMENT INGESTION                          ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • CoA PDF captured via Dock Scanner, Webhook, or Supplier EDI portal.                                │
 │ • AI Multimodal Parser extracts Analyte Matrix, Units, Batch #, Lab Accreditation.                   │
 │ • Visual bounding boxes `[x_min, y_min, x_max, y_max]` recorded for 1-click audit verification.       │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 3. SPECIFICATION & TOLERANCE MATCHING ENGINE       ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Ingestion Engine queries Acumatica `QMSInspectionPlan` via REST API.                               │
 │ • Compares measured assay, heavy metals (Pb, As, Cd, Hg), microbial CFUs against tolerances.        │
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
      "TestID": "HM_ARSENIC",
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

## 5. Automated Multi-Lab Routing Engine

When an inbound CoA is ingested, the engine validates the certifying laboratory's accreditation against the authorized lab directory:

1. **Chemical & Elemental Impurity Assays (HPLC, GC-MS, ICP-MS):**
   * Routing Priority: `LAB-GL-ANALYTICAL` (Great Lakes Bio-Analytical Services Inc., CALA #9481).
2. **Microbiological, Pathogen & Residual Solvent Assays (USP <2021>/<2022>, USP <467>):**
   * Routing Priority: `LAB-PACIFIC-TEST` (Pacific Rim BioNutra Testing Laboratories Ltd., SCC #8172).
3. **Dual-Testing Protocol for High-Risk Categories:**
   * Marine oils (`RAW-OMEGA3-70`) and probiotic actives (`RAW-GUT-PRB100`) undergo split-sample validation across both accredited laboratories prior to final ERP release.
