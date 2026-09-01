# Product Quality Specification: Rhodiola Rosea Extract 3% Rosavins / 1% Salidroside
## Acumatica Inventory Master: `RAW-RHOD-EXT3` | Vendor: `VEND-ALPINE-EXT`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-RHOD-EXT3                                    │
│ Item Class:              │ RAW_BOTANICAL                                    │
│ Description:             │ Rhodiola Rosea Extract 3% Rosavins / 1% Salidrosi│
│ Botanical Name:          │ Rhodiola rosea L. (Rhizome & Root)               │
│ Health Canada NPN Ref:   │ NPN-80062910                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-01 (Mississauga Main Facility)           │
│ Quarantine Staging Bay:  │ QC-HOLD-BAY-B                                    │
│ Total Shelf Life:        │ 36 Months (1,095 Days)                           │
│ Min Required Shelf Life: │ 24 Months (730 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-BOT-RHOD3                                  │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **Total Rosavins** *(Rosavin, Rosin, Rosarin)* | HPLC-DAD (USP Monograph) | $\ge 3.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 20** | **Salidroside Content** | HPLC-DAD (USP Monograph) | $\ge 1.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 30** | **Loss on Drying (Moisture)** | USP <731> ($105^\circ\text{C}$ for 2h) | $\le 5.00$ | $\% \text{ (w/w)}$ | **Major** |
| **Step 40** | **Lead (Pb)** | ICP-MS (USP <2232>)| $\le 0.50$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 50** | **Arsenic (As)** | ICP-MS (USP <2232>)| $\le 1.00$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 60** | **Cadmium (Cd)** | ICP-MS (USP <2232>)| $\le 0.30$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Mercury (Hg)** | ICP-MS (USP <2232>)| $\le 0.10$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 80** | **Total Aerobic Microbial (TAMC)** | USP <2021> | $\le 10,000$ | $\text{CFU/g}$ | **Major** |
| **Step 90** | **Total Combined Yeast & Mold (TYMC)** | USP <2021> | $\le 1,000$ | $\text{CFU/g}$ | **Major** |
| **Step 100**| **Escherichia coli** | USP <2022> | Absent in 10g | Text | **Critical** |
| **Step 110**| **Salmonella spp.** | USP <2022> | Absent in 25g | Text | **Critical** |

---

## 3. Storage, Handling & ERP Release Logic

* **Packaging:** 25 kg multi-layer kraft paper drums with inner heat-sealed food-grade polyethylene bag.
* **Storage Temperature:** Cool, dry place below $25^\circ\text{C}$ with relative humidity $\le 60\%$.
* **Dual Marker Release Check:** The Acumatica QMS inspection engine verifies that BOTH Rosavins ($\ge 3.0\%$) and Salidroside ($\ge 1.0\%$) pass before triggering lot state transition to `Released`.
