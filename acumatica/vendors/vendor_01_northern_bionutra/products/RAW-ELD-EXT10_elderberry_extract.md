# Product Quality Specification: European Elderberry Extract 10% Anthocyanins
## Acumatica Inventory Master: `RAW-ELD-EXT10` | Vendor: `VEND-NORTH-BIO`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-ELD-EXT10                                    │
│ Item Class:              │ RAW_BOTANICAL                                    │
│ Description:             │ Organic European Elderberry Extract 10% Anthocyan│
│ Botanical Name:          │ Sambucus nigra L. (Fruit / Berry)                │
│ Health Canada NPN Ref:   │ NPN-80038471                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-01 (Mississauga Main Facility)           │
│ Quarantine Staging Bay:  │ QC-HOLD-BAY-A                                    │
│ Total Shelf Life:        │ 36 Months (1,095 Days)                           │
│ Min Required Shelf Life: │ 24 Months (730 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-BOT-ELD10                                  │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **Total Anthocyanins** *(Cyanidin-3-glucoside)* | HPLC-UV (Ph. Eur. / USP) | $\ge 10.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 20** | **Loss on Drying (Moisture)** | USP <731> ($105^\circ\text{C}$ for 2h) | $\le 5.00$ | $\% \text{ (w/w)}$ | **Major** |
| **Step 30** | **Lead (Pb)** | ICP-MS (USP <2232>)| $\le 0.50$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 40** | **Arsenic (As)** | ICP-MS (USP <2232>)| $\le 1.00$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 50** | **Cadmium (Cd)** | ICP-MS (USP <2232>)| $\le 0.30$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 60** | **Mercury (Hg)** | ICP-MS (USP <2232>)| $\le 0.10$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Total Aerobic Microbial (TAMC)** | USP <2021> | $\le 10,000$ | $\text{CFU/g}$ | **Major** |
| **Step 80** | **Total Combined Yeast & Mold (TYMC)** | USP <2021> | $\le 1,000$ | $\text{CFU/g}$ | **Major** |
| **Step 90** | **Escherichia coli** | USP <2022> | Absent in 10g | Text | **Critical** |
| **Step 100**| **Salmonella spp.** | USP <2022> | Absent in 25g | Text | **Critical** |

---

## 3. Storage, Handling & ERP Release Logic

* **Packaging:** 25 kg fiber drums with double food-grade polyethylene heat-sealed liners and food-grade desiccant packets.
* **Storage Temperature:** Controlled room temperature below $20^\circ\text{C}$ in a dry warehouse environment away from direct sunlight.
* **ERP Ingestion Automation:** Automatically releases to inventory upon parsing verified 10.0%+ anthocyanin content and complete heavy metal compliance from `LAB-GL-ANALYTICAL` or `LAB-PACIFIC-TEST`.
