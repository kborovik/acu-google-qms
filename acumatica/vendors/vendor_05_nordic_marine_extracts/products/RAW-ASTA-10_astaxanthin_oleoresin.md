# Product Quality Specification: Natural Astaxanthin Oleoresin 10%
## Acumatica Inventory Master: `RAW-ASTA-10` | Vendor: `VEND-NORDIC-MAR`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-ASTA-10                                      │
│ Item Class:              │ RAW_MARINE_LIPID                                 │
│ Description:             │ Natural Astaxanthin Oleoresin 10% (Algal Extract)│
│ Biological Source:       │ Haematococcus pluvialis (Microalgae Biomass)     │
│ Health Canada NPN Ref:   │ NPN-80063819                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-COLD-01 (Refrigerated Storage <4°C)      │
│ Quarantine Staging Bay:  │ QC-COLD-HOLD-02                                  │
│ Total Shelf Life:        │ 24 Months (730 Days)                             │
│ Min Required Shelf Life: │ 18 Months (540 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-LIP-ASTA10                                 │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **Total Natural Astaxanthin Complex** | HPLC-UV (USP Astaxanthin Monograph) | $\ge 10.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 11** | **Free Astaxanthin Ratio** | HPLC-UV | $\le 5.00$ | $\%$ of total | **Major** |
| **Step 20** | **Peroxide Value (PV)** | AOCS Cd 8b-90 | $\le 10.0$ | $\text{meq O}_2\text{/kg}$ | **Major** |
| **Step 30** | **Lead (Pb)** | ICP-MS (USP <2232>)| $\le 0.50$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 40** | **Arsenic (As)** | ICP-MS (USP <2232>)| $\le 1.00$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 50** | **Cadmium (Cd)** | ICP-MS (USP <2232>)| $\le 0.30$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 60** | **Mercury (Hg)** | ICP-MS (USP <2232>)| $\le 0.10$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Total Aerobic Microbial (TAMC)** | USP <2021> | $\le 100$ | $\text{CFU/g}$ | **Major** |
| **Step 80** | **Escherichia coli** | USP <2022> | Absent in 10g | Text | **Critical** |
| **Step 90** | **Salmonella spp.** | USP <2022> | Absent in 25g | Text | **Critical** |

---

## 3. Storage, Handling & ERP Release Logic

* **Packaging:** 20 kg light-shielded aluminum containers blanketed with argon/nitrogen inert gas.
* **Storage Temperature:** Frozen or cold storage ($\le 4^\circ\text{C}$) to prevent carotenoid isomerization and degradation.
* **ERP Ingestion Automation:** Automated lot release upon confirmation of total astaxanthin $\ge 10.0\%$ and peroxide value $\le 10.0\text{ meq/kg}$.
