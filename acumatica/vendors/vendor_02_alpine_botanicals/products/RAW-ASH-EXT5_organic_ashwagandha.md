# Product Quality Specification: Organic Ashwagandha Root Extract 5%
## Acumatica Inventory Master: `RAW-ASH-EXT5` | Vendor: `VEND-ALPINE-EXT`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-ASH-EXT5                                     │
│ Item Class:              │ RAW_BOTANICAL                                    │
│ Description:             │ Organic Ashwagandha Root Extract 5% Withanolides │
│ Botanical Name:          │ Withania somnifera (L.) Dunal (Root)             │
│ Health Canada NPN Ref:   │ NPN-80041289                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-01 (Mississauga Main Facility)           │
│ Quarantine Staging Bay:  │ QC-HOLD-BAY-B                                    │
│ Total Shelf Life:        │ 36 Months (1,095 Days)                           │
│ Min Required Shelf Life: │ 24 Months (730 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-BOT-ASH5                                   │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **Total Withanolides** *(Withaferin A, Withanolide A/D)* | HPLC-UV (USP Monograph) | $\ge 5.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 20** | **Loss on Drying (Moisture)** | USP <731> ($105^\circ\text{C}$ for 2h) | $\le 5.00$ | $\% \text{ (w/w)}$ | **Major** |
| **Step 30** | **Withaferin A Ratio** *(Safety Profiling)* | HPLC-UV | $\le 1.00$ | $\% \text{ (w/w)}$ | **Major** |
| **Step 40** | **Lead (Pb)** | ICP-MS (USP <2232>)| $\le 0.50$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 50** | **Arsenic (As)** | ICP-MS (USP <2232>)| $\le 1.00$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 60** | **Cadmium (Cd)** | ICP-MS (USP <2232>)| $\le 0.30$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Mercury (Hg)** | ICP-MS (USP <2232>)| $\le 0.10$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 80** | **Total Aerobic Microbial (TAMC)** | USP <2021> | $\le 10,000$ | $\text{CFU/g}$ | **Major** |
| **Step 90** | **Total Combined Yeast & Mold (TYMC)** | USP <2021> | $\le 1,000$ | $\text{CFU/g}$ | **Major** |
| **Step 100**| **Escherichia coli** | USP <2022> | Absent in 10g | Text | **Critical** |
| **Step 110**| **Salmonella spp.** | USP <2022> | Absent in 25g | Text | **Critical** |

---

## 3. Acumatica QMS Decision Logic & State Machine

* **Inbound Inspection Order:** Upon receipt from `VEND-ALPINE-EXT`, Acumatica creates `QMSInspectionOrder` tied to `QPLAN-BOT-ASH5`.
* **Passing Condition:** Withanolides $\ge 5.00\%$, Withaferin A $\le 1.00\%$, Heavy Metals within Health Canada limits $\implies$ `INLotSerialStatus` $\longrightarrow$ `Released`.
* **Failing Condition:** Withanolides $< 5.00\%$ or Contaminant breach $\implies$ `INLotSerialStatus` $\longrightarrow$ `Quarantine`, `QMSNonConformance` NCR generated, vendor notified.
