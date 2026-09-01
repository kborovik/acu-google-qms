# Product Quality Specification: Turmeric Curcuminoid Extract 95%
## Acumatica Inventory Master: `RAW-CURC-95` | Vendor: `VEND-PACIFIC-ORG`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-CURC-95                                      │
│ Item Class:              │ RAW_BOTANICAL                                    │
│ Description:             │ Turmeric Curcuminoid Extract 95% Pure Powder     │
│ Botanical Name:          │ Curcuma longa L. (Rhizome)                       │
│ Health Canada NPN Ref:   │ NPN-80053912                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-01 (Mississauga Main Facility)           │
│ Quarantine Staging Bay:  │ QC-HOLD-BAY-A                                    │
│ Total Shelf Life:        │ 48 Months (1,460 Days)                           │
│ Min Required Shelf Life: │ 30 Months (900 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-BOT-CURC95                                 │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **Total Curcuminoids** *(Curcumin, DMC, BDMC)* | HPLC-DAD (USP <2021> / ASTA 18.0) | $95.00 - 102.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 20** | **Residual Solvent: Ethanol** | Headspace GC-FID (USP <467> Opt 1) | $\le 5,000$ | $\text{ppm}$ | **Major** |
| **Step 30** | **Residual Solvent: Ethyl Acetate**| Headspace GC-FID (USP <467> Opt 1) | $\le 5,000$ | $\text{ppm}$ | **Major** |
| **Step 40** | **Loss on Drying (Moisture)** | USP <731> ($105^\circ\text{C}$ for 2h) | $\le 3.00$ | $\% \text{ (w/w)}$ | **Major** |
| **Step 50** | **Lead (Pb)** | ICP-MS (USP <2232>)| $\le 0.50$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 60** | **Arsenic (As)** | ICP-MS (USP <2232>)| $\le 1.00$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Cadmium (Cd)** | ICP-MS (USP <2232>)| $\le 0.30$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 80** | **Mercury (Hg)** | ICP-MS (USP <2232>)| $\le 0.10$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 90** | **Total Aerobic Microbial (TAMC)** | USP <2021> | $\le 1,000$ | $\text{CFU/g}$ | **Major** |
| **Step 100**| **Total Combined Yeast & Mold (TYMC)** | USP <2021> | $\le 100$ | $\text{CFU/g}$ | **Major** |
| **Step 110**| **Escherichia coli** | USP <2022> | Absent in 10g | Text | **Critical** |
| **Step 120**| **Salmonella spp.** | USP <2022> | Absent in 25g | Text | **Critical** |

---

## 3. Storage, Handling & ERP Release Logic

* **Packaging:** 25 kg fiber drums with double sealed amber poly-liners to prevent photodegradation.
* **Storage Temperature:** Store below $25^\circ\text{C}$ in ambient, humidity-controlled warehouse.
* **Release Automation:** Automated lot release upon confirmation of total curcuminoids $\ge 95.0\%$ and absence of synthetic adulterants or non-permitted extraction solvents.
