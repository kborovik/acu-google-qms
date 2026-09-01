# Manufactured Finished Product Specification: ImmunoShield Botanical Active Plus
## Acumatica Item Master: `FG-IMMUNE-DEFENSE-60C` | Manufacturer: `CanNordic BioNutra Inc.`

---

## 1. Product Master & Regulatory Identification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITEM MASTER ATTRIBUTES                             │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Inventory ID:            │ FG-IMMUNE-DEFENSE-60C                            │
│ Brand Name:              │ ImmunoShield™ Botanical Active Plus              │
│ Item Class:              │ FG_NUTRACEUTICAL (Manufactured Finished Goods)   │
│ Manufacturer:            │ CanNordic BioNutra Inc. (Site Licence #302194)   │
│ Dosage Form:             │ Two-Piece Vegetable Capsule (Size 00 Clear)      │
│ Packaging / Pack Size:   │ 60 Capsules / Amber HDPE Bottle, Induction Seal  │
│ Health Canada NPN:       │ NPN-80099412                                     │
│ Base UOM:                │ EA (1 Bottle = 60 Capsules)                      │
│ Standard Batch Size:     │ 100,000 Capsules (1,666.67 Bottles = 55.0 kg)    │
│ Lot/Serial Class:        │ LOT_EXP_QC (Mandatory Finished Lot QC Hold)      │
│ Valuation Method:        │ Standard Costing                                 │
│ Default Warehouse:       │ WH-MISS-FG-01 (Finished Goods Warehouse)         │
│ Total Shelf Life:        │ 36 Months (1,095 Days) from Blending Date        │
│ Bill of Materials ID:    │ BOM-IMMUNE-DEF-01                                │
│ QMS Inspection Plan:     │ QPLAN-FG-IMMUNE60                                │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Bill of Materials (BOM) & Formulation Composition

### 2.1 Formula per Finished Vegetable Capsule (Size 00)
| Line | Inventory ID | Ingredient / Component Description | Vendor / Origin | Claim / Potency | Mg / Capsule | Batch Qty (100k Caps) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | `RAW-ECH-EXT4` | Organic Echinacea Purpurea Extract 4% | `VEND-NORTH-BIO` | 8.0 mg Polyphenols | **200.0 mg** | 20.00 kg |
| **02** | `RAW-ELD-EXT10`| European Elderberry Extract 10% Anthocyanins | `VEND-NORTH-BIO` | 15.0 mg Anthocyanins| **150.0 mg** | 15.00 kg |
| **03** | `RAW-ASH-EXT5` | Organic Ashwagandha Extract 5% Withanolides | `VEND-ALPINE-EXT` | 5.0 mg Withanolides | **100.0 mg** | 10.00 kg |
| **04** | `RAW-EXC-RICE` | Organic Nu-FLOW® Rice Hull Extract (Flow Aid) | Ribus Inc. / Excipient | Flow / Glidant | **90.0 mg** | 9.00 kg |
| **05** | `RAW-EXC-VCAP00`| Size 00 Clear Hypromellose (HPMC) Capsule Shell | CapsCanada / Lonza | Shell Matrix | **1.0 EA** | 100,000 EA |
| **06** | `PKG-BOT-150CC`| 150cc Amber HDPE Plastic Bottle | Alpha Packaging | Packaging Primary | **1.0 EA** | 1,667 EA |
| **07** | `PKG-CAP-38MM` | 38-400 Child-Resistant Cap with Induction Seal| Berry Global | Packaging Closure | **1.0 EA** | 1,667 EA |
| **08** | `PKG-LBL-IMM60`| ImmunoShield 60-Count Bilingual Label (EN/FR) | CCL Label | Packaging Tertiary| **1.0 EA** | 1,667 EA |

---

## 3. Manufacturing Routing & Operational Work Centers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     MANUFACTURING ROUTING: BOM-IMMUNE-DEF-01                │
├──────────┬──────────────────┬──────────────────────┬────────────────────────┤
│ Oper #   │ Work Center      │ Description          │ Quality Check Gate     │
├──────────┼──────────────────┼──────────────────────┼────────────────────────┤
│ **10**   │ `WC-DISPENSING`  │ Raw Material Kitting │ Lot Release Lock Verification│
│ **20**   │ `WC-BLENDING`    │ V-Cone Dry Blending  │ Blend Uniformity Assay (RSD <5%)│
│ **30**   │ `WC-ENCAPS-01`   │ Bosch Capsule Filling│ Fill Weight Check (Every 15m)│
│ **40**   │ `WC-POLISH-MET`  │ Dedusting & Met-Det  │ 1.0mm Fe / 1.5mm Non-Fe Test │
│ **50**   │ `WC-PACKAGING`   │ Bottling & Induction │ Seal Integrity & Count Check │
│ **60**   │ `WC-QMS-HOLD`    │ Quarantine Staging   │ Final Lab Release Gating     │
└──────────┴──────────────────┴──────────────────────┴────────────────────────┘
```

---

## 4. Finished Product Quality Inspection Plan (`QPLAN-FG-IMMUNE60`)

| Step | Parameter / Analyte | Test Method | Acceptance Specification | Criticality |
| :--- | :--- | :--- | :--- | :--- |
| **10** | **Visual Appearance** | Visual Inspection | Size 00 clear vegetable capsule containing dark purple/brown speckled powder | **Major** |
| **20** | **Average Fill Weight** | USP <2091> (20 Caps) | $540.0\text{ mg} \pm 5.0\%$ ($513.0\text{ mg} - 567.0\text{ mg}$) | **Critical** |
| **30** | **Disintegration Time** | USP <2040> (Simulated Gastric Fluid) | $\le 20\text{ minutes}$ at $37^\circ\text{C} \pm 2^\circ\text{C}$ | **Critical** |
| **40** | **Total Polyphenols Assay** | HPLC-DAD (as Cichoric/Caftaric) | $\ge 8.00\text{ mg / capsule}$ ($90.0\% - 120.0\%$ Claim) | **Critical** |
| **50** | **Total Anthocyanins Assay** | HPLC-UV (Cyanidin-3-glucoside) | $\ge 15.00\text{ mg / capsule}$ ($90.0\% - 120.0\%$ Claim)| **Critical** |
| **60** | **Total Withanolides Assay** | HPLC-UV | $\ge 5.00\text{ mg / capsule}$ ($90.0\% - 120.0\%$ Claim) | **Critical** |
| **70** | **Elemental Impurities (Lead)**| ICP-MS (USP <2232>)| $\le 0.50\text{ ppm}$ | **Critical** |
| **80** | **Microbial TAMC** | USP <2021> | $\le 1,000\text{ CFU/g}$ | **Major** |
| **90** | **Microbial TYMC** | USP <2021> | $\le 100\text{ CFU/g}$ | **Major** |
| **100**| **Pathogens (E. coli / Salm)**| USP <2022> | Absent in 10g / 25g | **Critical** |

---

## 5. Acumatica Production Order & Finished Good Release

* Upon production order closure (`AMProdItem`), Acumatica automatically creates finished goods lot (e.g. `LOT-FG-IMM-260301`) in **`QC Hold`** status.
* When laboratory tests from `LAB-GL-ANALYTICAL` confirm active potency ($\ge 100\%$ of label claim) and microbial safety, `INLotSerialStatus` flips to **`Released`**, making stock available for customer order fulfillment.
