# Manufactured Finished Product Specification: CardioPure Ultra Omega-3 + CoQ10 & Astaxanthin
## Acumatica Item Master: `FG-CARDIO-OMEGA-COQ10-60SG` | Manufacturer: `CanNordic BioNutra Inc.`

---

## 1. Product Master & Regulatory Identification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ FG-CARDIO-OMEGA-COQ10-60SG                       │
│ Brand Name:              │ CardioPure™ Ultra Omega-3 + CoQ10 & Astaxanthin  │
│ Item Class:              │ FG_NUTRACEUTICAL (Manufactured Finished Goods)   │
│ Manufacturer:            │ CanNordic BioNutra Inc. (Site Licence #302194)   │
│ Dosage Form:             │ Rotary Die Soft Gelatin Capsule (20 Oblong Ruby) │
│ Packaging / Pack Size:   │ 60 Softgels / Amber Glass Bottle with CRC Cap    │
│ Health Canada NPN:       │ NPN-80099418                                     │
│ Base UOM:                │ EA (1 Bottle = 60 Softgels)                      │
│ Standard Batch Size:     │ 100,000 Softgels (1,666.67 Bottles = 155.0 kg)   │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Finished Lot QC Hold)      │
│ Valuation Method:        │ Standard Costing                                 │
│ Default Warehouse:       │ WH-MISS-FG-01 (Finished Goods Warehouse)         │
│ Total Shelf Life:        │ 24 Months (730 Days) from Encapsulation Date     │
│ Bill of Materials ID:    │ BOM-CARDIO-OM3-01                                │
│ QMS Inspection Plan:     │ QPLAN-FG-CARDIO60                                │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Bill of Materials (BOM) & Formulation Composition

### 2.1 Formula per Finished Softgel (20 Oblong)
| Line | Inventory ID | Ingredient / Component Description | Vendor / Origin | Claim / Potency | Mg / Softgel | Batch Qty (100k Softgels) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | `RAW-OMEGA3-70` | Marine Omega-3 TG Oil (70% EPA/DHA min) | `VEND-NORDIC-MAR` | 400mg EPA / 300mg DHA | **1,000.0 mg** | 100.00 kg |
| **02** | `RAW-COQ10-99` | Pure Coenzyme Q10 (Ubiquinone 99% USP) | `VEND-NIPPON-PHARMA`| 100.0 mg CoQ10 | **101.0 mg** | 10.10 kg |
| **03** | `RAW-ASTA-10` | Natural Astaxanthin Oleoresin 10% | `VEND-NORDIC-MAR` | 2.0 mg Astaxanthin | **20.0 mg** | 2.00 kg |
| **04** | `RAW-EXC-BEES` | White Beeswax USP (Suspending / Thickener) | Strahl & Pitsch | Matrix Viscosity | **29.0 mg** | 2.90 kg |
| **05** | `RAW-EXC-GELBOV`| Bovine Gelatin 180 Bloom USP (Shell Mass) | Rousselot / Gelita | Shell Wall | **280.0 mg** | 28.00 kg |
| **06** | `RAW-EXC-GLYC` | Glycerin 99.7% USP (Plasticizer) | Emery Oleochemicals| Shell Elasticity | **120.0 mg** | 12.00 kg |
| **07** | `PKG-BOT-GLS250`| 250cc Amber Glass Bottle | Owens-Illinois | Packaging Primary | **1.0 EA** | 1,667 EA |
| **08** | `PKG-CAP-45MM` | 45mm Child-Resistant Continuous Thread Cap | Phoenix Closures | Packaging Closure | **1.0 EA** | 1,667 EA |
| **09** | `PKG-LBL-CAR60`| CardioPure 60-Count Bilingual Label (EN/FR) | CCL Label | Packaging Tertiary| **1.0 EA** | 1,667 EA |

---

## 3. Manufacturing Routing & Operational Work Centers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     MANUFACTURING ROUTING: BOM-CARDIO-OM3-01                │
├──────────┬──────────────────┬──────────────────────┬────────────────────────┤
│ Oper #   │ Work Center      │ Description          │ Quality Check Gate     │
├──────────┼──────────────────┼──────────────────────┼────────────────────────┤
│ **10**   │ `WC-GEL-MELT`    │ Gelatin Preparation  │ Gel Viscosity (4.5-5.5° Engler)│
│ **20**   │ `WC-OIL-COMPOUND`│ N2-Blanketed Suspens.│ Suspension Homogeneity (RSD<3%)│
│ **30**   │ `WC-ENCAPS-SG`   │ Rotary Die Softgel   │ Fill Weight & Seam Thickness   │
│ **40**   │ `WC-TUMBLE-DRY`  │ Tumble & Tunnel Dry  │ Shell Hardness (8.0-10.0 N)    │
│ **50**   │ `WC-OPTIC-SORT`  │ Optical Vision Sort  │ Dimension & Bubble Inspection  │
│ **60**   │ `WC-PACKAGING`   │ Amber Bottling & Pack│ Cap Torque & Lot Code Print    │
│ **70**   │ `WC-QMS-HOLD`    │ Quarantine Staging   │ Final Analytical Release Gate  │
└──────────┴──────────────────┴──────────────────────┴────────────────────────┘
```

---

## 4. Finished Product Quality Inspection Plan (`QPLAN-FG-CARDIO60`)

| Step | Parameter / Analyte | Test Method | Acceptance Specification | Criticality |
| :--- | :--- | :--- | :--- | :--- |
| **10** | **Visual Appearance** | Visual Inspection | 20 Oblong dark ruby/red translucent softgel capsule, free of leaks | **Major** |
| **20** | **Average Fill Weight** | USP <2091> (20 Softgels) | $1,150.0\text{ mg} \pm 3.0\%$ ($1,115.5\text{ mg} - 1,184.5\text{ mg}$) | **Critical** |
| **30** | **Disintegration / Rupture**| USP <2040> (Rupture Test) | $\le 15\text{ minutes}$ in water at $37^\circ\text{C}$ | **Critical** |
| **40** | **EPA Content Assay** | GC-FID (Ph. Eur. 2.4.29) | $\ge 400.0\text{ mg / softgel}$ ($90.0\% - 120.0\%$ Claim) | **Critical** |
| **50** | **DHA Content Assay** | GC-FID (Ph. Eur. 2.4.29) | $\ge 300.0\text{ mg / softgel}$ ($90.0\% - 120.0\%$ Claim) | **Critical** |
| **60** | **Coenzyme Q10 Assay** | HPLC-UV (USP Monograph) | $\ge 100.0\text{ mg / softgel}$ ($90.0\% - 120.0\%$ Claim) | **Critical** |
| **70** | **Astaxanthin Assay** | HPLC-UV | $\ge 2.00\text{ mg / softgel}$ ($90.0\% - 120.0\%$ Claim) | **Critical** |
| **80** | **Peroxide Value (PV)** | AOCS Cd 8b-90 | $\le 5.0\text{ meq O}_2\text{/kg}$ | **Critical** |
| **90** | **p-Anisidine Value (p-AV)**| AOCS Cd 18-90 | $\le 20.0\text{ AnV}$ | **Major** |
| **100**| **Elemental Impurities (Lead)**| ICP-MS (USP <2232>)| $\le 0.10\text{ ppm}$ | **Critical** |
| **110**| **Microbial TAMC / TYMC** | USP <2021> | TAMC $\le 100\text{ CFU/g}$, TYMC $\le 50\text{ CFU/g}$ | **Major** |

---

## 5. Acumatica Production Order & Finished Good Release

* Finished softgel lots are staged in temperature-controlled quarantine (`QC-COLD-HOLD-02`).
* Upon receipt of the Certificate of Analysis from `LAB-GL-ANALYTICAL` and `LAB-PACIFIC-TEST`, Acumatica validates lipid oxidation (TOTOX $\le 26.0$), EPA/DHA/CoQ10/Astaxanthin potencies, and microbiological cleanliness.
* When all criteria pass, `INLotSerialStatus` is flipped from `QC Hold` $\longrightarrow$ **`Released`**.
