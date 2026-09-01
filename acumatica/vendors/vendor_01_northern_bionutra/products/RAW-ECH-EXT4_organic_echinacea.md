# Product Quality Specification: Organic Echinacea Purpurea Extract 4%
## Acumatica Inventory Master: `RAW-ECH-EXT4` | Vendor: `VEND-NORTH-BIO`

---

## 1. Item Master & ERP Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ RAW-ECH-EXT4                                     │
│ Item Class:              │ RAW_BOTANICAL                                    │
│ Description:             │ Organic Echinacea Purpurea Extract 4% Polyphenols│
│ Botanical Name:          │ Echinacea purpurea (L.) Moench (Aerial Parts)    │
│ Health Canada NPN Ref:   │ NPN-80029384                                     │
│ Base / Purchase UOM:     │ KG / KG                                          │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Expiration & QC Hold)      │
│ Valuation Method:        │ FIFO (First-In, First-Out)                       │
│ Default Warehouse:       │ WH-MISS-01 (Mississauga Main Facility)           │
│ Quarantine Staging Bay:  │ QC-HOLD-BAY-A                                    │
│ Total Shelf Life:        │ 36 Months (1,095 Days)                           │
│ Min Required Shelf Life: │ 24 Months (730 Days) at Dock Arrival             │
│ Quality Inspection Plan: │ QPLAN-BOT-ECH4                                   │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Quality Parameter Acceptance Criteria Matrix

| Parameter Step | Analyte / Test Description | Test Method | Specified Target Range | Standard Unit | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 10** | **Total Active Polyphenols** *(Cichoric, Caftaric, Chlorogenic)* | HPLC-DAD (USP Monograph) | $\ge 4.00$ | $\% \text{ (w/w)}$ | **Critical** |
| **Step 20** | **Loss on Drying (Moisture)** | USP <731> ($105^\circ\text{C}$ for 2h) | $\le 5.00$ | $\% \text{ (w/w)}$ | **Major** |
| **Step 30** | **Lead (Pb)** | ICP-MS (USP <2232> / AOAC 2013.06)| $\le 0.50$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 40** | **Arsenic (As)** | ICP-MS (USP <2232> / AOAC 2013.06)| $\le 1.00$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 50** | **Cadmium (Cd)** | ICP-MS (USP <2232> / AOAC 2013.06)| $\le 0.30$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 60** | **Mercury (Hg)** | ICP-MS (USP <2232> / AOAC 2013.06)| $\le 0.10$ | $\text{ppm (mg/kg)}$ | **Critical** |
| **Step 70** | **Total Aerobic Microbial (TAMC)** | USP <2021> (Membrane Filtration) | $\le 10,000$ | $\text{CFU/g}$ | **Major** |
| **Step 80** | **Total Combined Yeast & Mold (TYMC)** | USP <2021> (Spread Plate) | $\le 1,000$ | $\text{CFU/g}$ | **Major** |
| **Step 90** | **Escherichia coli** | USP <2022> (Enrichment / Selective)| Absent in 10g | Text | **Critical** |
| **Step 100**| **Salmonella spp.** | USP <2022> (AOAC PCR Rapid) | Absent in 25g | Text | **Critical** |

---

## 3. Acumatica QMS Decision Matrix & State Governance

```
                                [Inbound CoA Ingestion]
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    │                                             │
             [ALL TESTS PASS]                              [ANY OOS OCCURS]
                    │                                             │
                    ▼                                             ▼
       ┌─────────────────────────┐                   ┌─────────────────────────┐
       │ QMSInspectionOrder: Pass│                   │ QMSInspectionOrder: Fail│
       │ LotStatus: Released     │                   │ LotStatus: Quarantine   │
       │ unblock Work Orders     │                   │ QMSNonConformance (NCR) │
       └─────────────────────────┘                   └─────────────────────────┘
```

### 3.1 Passing Sample Result (Approved)
* **Active Polyphenols:** $4.32\%$ (Pass)
* **Lead (Pb):** $0.084\text{ ppm}$ (Pass)
* **TAMC:** $420\text{ CFU/g}$ (Pass)
* **Action:** `INLotSerialStatus` flipped to `Released`.

### 3.2 Out-of-Spec Scenario (Rejected / NCR)
* **Lead (Pb):** $0.85\text{ ppm}$ ($\text{Exceeds limit of } 0.50\text{ ppm}$).
* **Action:** `INLotSerialStatus` locked in `Quarantine`, `QMSNonConformance` ticket generated with Critical severity for vendor return.
