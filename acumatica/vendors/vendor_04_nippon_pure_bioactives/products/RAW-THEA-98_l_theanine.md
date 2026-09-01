# Product Quality Specification: Pure L-Theanine 98.5%
## Acumatica Inventory Master: `RAW-THEA-98` | Vendor: `VEND-NIPPON-PHARMA`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-THEA-98                                      │
│ Item Class:              │ RAW_API_FERMENTATION                             │
│ Description:             │ Pure L-Theanine 98.5% Fermentation High-Purity   │
│ Chemical Formula:        │ C7H14N2O3 (CAS 3081-61-6)                        │
│ Health Canada NPN Ref:   │ NPN-80071928                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-01 (Mississauga Main Facility)           │
│ Quarantine Staging Bay:  │ QC-HOLD-BAY-C                                    │
│ Total Shelf Life:        │ 36 Months (1,095 Days)                           │
│ Min Required Shelf Life: │ 24 Months (730 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-API-THEA98                                 │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **L-Theanine Content (Anhydrous)** | HPLC-UV / Titration | $98.50 - 101.50$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 20** | **Specific Optical Rotation $[\alpha]_D^{20}$** | USP <781S> ($c=5, \text{H}_2\text{O}$) | $+7.7 \text{ to } +8.5$ | $\text{degrees } (^\circ)$ | **Critical** |
| **Step 30** | **Loss on Drying (Moisture)** | USP <731> ($105^\circ\text{C}$ for 3h) | $\le 1.00$ | $\% \text{ (w/w)}$ | **Major** |
| **Step 40** | **Residue on Ignition** | USP <281> | $\le 0.20$ | $\% \text{ (w/w)}$ | **Major** |
| **Step 50** | **Enantiomeric Purity (D-Theanine)** | Chiral HPLC | $\le 0.50$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 60** | **Lead (Pb)** | ICP-MS (USP <2232>)| $\le 0.20$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Arsenic (As)** | ICP-MS (USP <2232>)| $\le 0.50$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 80** | **Total Aerobic Microbial (TAMC)** | USP <2021> | $\le 1,000$ | $\text{CFU/g}$ | **Major** |
| **Step 90** | **Total Combined Yeast & Mold (TYMC)** | USP <2021> | $\le 100$ | $\text{CFU/g}$ | **Major** |

---

## 3. Storage, Handling & ERP Release Logic

* **Chiral Integrity Verification:** Verifies optical rotation to ensure no racemic D-Theanine contamination.
* **Packaging:** 25 kg fiber drums with tamper-evident inner poly-bag.
* **Release Automation:** Automated release into Acumatica ERP upon parsing valid purity ($\ge 98.5\%$) and optical rotation compliance.
