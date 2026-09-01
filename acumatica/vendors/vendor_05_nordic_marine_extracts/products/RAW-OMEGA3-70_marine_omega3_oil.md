# Product Quality Specification: Marine Omega-3 Triglyceride Oil 70%
## Acumatica Inventory Master: `RAW-OMEGA3-70` | Vendor: `VEND-NORDIC-MAR`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-OMEGA3-70                                    │
│ Item Class:              │ RAW_MARINE_LIPID                                 │
│ Description:             │ Marine Omega-3 TG Oil (70% EPA/DHA min)          │
│ Biological Source:       │ Engraulis ringens / Sardinops sagax (Wild Fish)  │
│ Health Canada NPN Ref:   │ NPN-80092104                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-COLD-01 (Climate Controlled 10-15°C)     │
│ Quarantine Staging Bay:  │ QC-COLD-HOLD-02                                  │
│ Total Shelf Life:        │ 24 Months (730 Days)                             │
│ Min Required Shelf Life: │ 18 Months (540 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-LIP-OM370                                  │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **Total EPA + DHA Sum Content** | GC-FID (Ph. Eur. 2.4.29 / GOED) | $\ge 70.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 11** | **Eicosapentaenoic Acid (EPA)** | GC-FID (Ph. Eur. 2.4.29) | $\ge 40.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 12** | **Docosahexaenoic Acid (DHA)** | GC-FID (Ph. Eur. 2.4.29) | $\ge 20.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 20** | **Peroxide Value (PV)** | AOCS Cd 8b-90 (Potentiometric) | $\le 5.0$ | $\text{meq O}_2\text{/kg}$ | **Critical** |
| **Step 30** | **p-Anisidine Value (p-AV)** | AOCS Cd 18-90 (Spectrophotometric)| $\le 20.0$ | $\text{AnV units}$ | **Major** |
| **Step 40** | **Total Oxidation Value (TOTOX)** | Calculated ($2 \times \text{PV} + \text{p-AV}$) | $\le 26.0$ | Index | **Critical** |
| **Step 50** | **Lead (Pb)** | ICP-MS (USP <2232>)| $\le 0.05$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 60** | **Cadmium (Cd)** | ICP-MS (USP <2232>)| $\le 0.05$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Mercury (Hg)** | ICP-MS (USP <2232>)| $\le 0.01$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 80** | **Inorganic Arsenic (Inorg As)** | HPLC-ICP-MS (Speciation) | $\le 0.10$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 90** | **Dioxins & Furans (WHO-PCDD/F-TEQ)**| HRGC-HRMS (EPA 1613B) | $\le 1.75$ | $\text{pg/g}$ | **Critical** |
| **Step 100**| **Total Aerobic Microbial (TAMC)** | USP <2021> | $\le 100$ | $\text{CFU/g}$ | **Major** |

---

## 3. Storage, Handling & ERP Release Logic

* **Packaging:** 190 kg epoxy-phenolic lined steel drums flushed with high-purity nitrogen ($99.999\% \text{ N}_2$).
* **Storage Temperature:** Controlled cool storage ($10^\circ\text{C} - 15^\circ\text{C}$), protected from light and heat.
* **Oxidation TOTOX Safety Lock:** If calculated TOTOX $> 26.0$, lot is irrevocably quarantined and rejected due to lipid oxidation.
