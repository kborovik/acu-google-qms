# Product Quality Specification: Multi-Strain Probiotic Blend 100B CFU/g
## Acumatica Inventory Master: `RAW-GUT-PRB100` | Vendor: `VEND-PACIFIC-ORG`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-GUT-PRB100                                   │
│ Item Class:              │ RAW_BIOLOGICAL                                   │
│ Description:             │ Multi-Strain Probiotic Blend 100B CFU/g Powder   │
│ Bacterial Strains:       │ L. acidophilus, B. lactis, L. plantarum, B. bifid│
│ Health Canada NPN Ref:   │ NPN-80084920                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-COLD-01 (Refrigerated Warehouse 2-8°C)   │
│ Quarantine Staging Bay:  │ QC-COLD-HOLD-01 (Refrigerated Hold Bay)          │
│ Total Shelf Life:        │ 24 Months (730 Days)                             │
│ Min Required Shelf Life: │ 18 Months (540 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-BIO-PRB100                                 │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **Total Viable Cell Count** | ISO 7889 / ISO 20128 (MRS/TOS Agar)| $\ge 100.0$ | $\text{Billion CFU/g}$ | **Critical** |
| **Step 20** | **Water Activity ($a_w$)** | USP <922> (Chilled Mirror @ $25^\circ\text{C}$)| $\le 0.20$ | $a_w \text{ (index)}$ | **Critical** |
| **Step 30** | **Non-Lactic Contaminant Count**| ISO 21528-2 (VRBG Agar) | $\le 10$ | $\text{CFU/g}$ | **Critical** |
| **Step 40** | **Yeast and Mold (TYMC)** | USP <2021> (Chloramphenicol Agar) | $\le 100$ | $\text{CFU/g}$ | **Major** |
| **Step 50** | **Lead (Pb)** | ICP-MS (USP <2232>)| $\le 0.20$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 60** | **Arsenic (As)** | ICP-MS (USP <2232>)| $\le 0.50$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Escherichia coli** | USP <2022> | Absent in 10g | Text | **Critical** |
| **Step 80** | **Salmonella spp.** | USP <2022> | Absent in 25g | Text | **Critical** |

---

## 3. Cold-Chain Storage & ERP Governance

* **Strict Cold-Chain Protocol:** Inbound receipt triggers an automated prompt in Acumatica mobile app for receiving clerk to verify data logger reading ($2.0^\circ\text{C} - 8.0^\circ\text{C}$).
* **Water Activity ($a_w$) Criticality:** If $a_w > 0.20$, cell viability degrades rapidly; material is flagged as out-of-spec and quarantined immediately.
* **Testing Assignment:** Exclusively routed to **Pacific Rim BioNutra Testing Laboratories Ltd.** (`LAB-PACIFIC-TEST` / DEL #203819) under anaerobic chamber incubation conditions.
