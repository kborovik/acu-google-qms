# Product Quality Specification: Pure Coenzyme Q10 99% USP
## Acumatica Inventory Master: `RAW-COQ10-99` | Vendor: `VEND-NIPPON-PHARMA`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-COQ10-99                                     │
│ Item Class:              │ RAW_API_FERMENTATION                             │
│ Description:             │ Pure Coenzyme Q10 (Ubiquinone) USP Grade 99.0%   │
│ Chemical Formula:        │ C59H90O4 (CAS 303-98-0)                          │
│ Health Canada NPN Ref:   │ NPN-80019283                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-01 (Mississauga Main Facility)           │
│ Quarantine Staging Bay:  │ QC-HOLD-BAY-C                                    │
│ Total Shelf Life:        │ 36 Months (1,095 Days)                           │
│ Min Required Shelf Life: │ 24 Months (730 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-API-COQ10                                  │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **Ubidecarenone (CoQ10) Assay** | HPLC-UV (USP Ubidecarenone Monograph)| $99.00 - 101.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 20** | **Melting Range** | USP <741> Class 1a | $48.0 - 52.0$ | $^\circ\text{C}$ | **Major** |
| **Step 30** | **Residue on Ignition (Sulfated Ash)**| USP <281> | $\le 0.10$ | $\% \text{ (w/w)}$ | **Major** |
| **Step 40** | **Chromatographic Impurities (Individual)**| HPLC-UV (USP Monograph) | $\le 0.50$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 50** | **Total Impurities** | HPLC-UV (USP Monograph) | $\le 1.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 60** | **Lead (Pb)** | ICP-MS (USP <2232>)| $\le 0.20$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Arsenic (As)** | ICP-MS (USP <2232>)| $\le 0.50$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 80** | **Cadmium (Cd)** | ICP-MS (USP <2232>)| $\le 0.20$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 90** | **Mercury (Hg)** | ICP-MS (USP <2232>)| $\le 0.05$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 100**| **Total Aerobic Microbial (TAMC)** | USP <2021> | $\le 1,000$ | $\text{CFU/g}$ | **Major** |
| **Step 110**| **Total Combined Yeast & Mold (TYMC)** | USP <2021> | $\le 100$ | $\text{CFU/g}$ | **Major** |

---

## 3. Storage, Handling & ERP Release Logic

* **Packaging:** 20 kg fiber drums with double sealed black polyethylene protective liners to shield from light and oxidation.
* **Storage Temperature:** Store below $25^\circ\text{C}$ in ambient, light-controlled warehouse.
* **ERP Ingestion Automation:** Instant release into Acumatica inventory if assayed purity is between $99.00\%$ and $101.00\%$ and individual chromatographic impurities do not exceed $0.50\%$.
