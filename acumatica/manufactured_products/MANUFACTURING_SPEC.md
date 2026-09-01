# CanNordic BioNutra Inc. - In-House Manufacturing & Finished Goods Specification
## Acumatica ERP Manufacturing Edition (BOM, Routing & Finished Good QMS)

---

## 1. Executive Summary & CDMO Manufacturing Capabilities

**CanNordic BioNutra Inc.** operates a fully licensed Health Canada Site Licence (#302194) and CFIA SFCR-certified CDMO facility in Mississauga, ON. The plant converts inbound, analytically verified raw materials (`QC Released`) into high-potency finished dosage forms across two primary manufacturing suites:

1. **Suite A (Solid Dose Blending & Encapsulation):** Dry granulation, ribbon/tumble blending, semi-automatic & high-speed rotary capsule filling, electronic channel counting, induction sealing, and cartoning.
2. **Suite B (Lipid & Softgel Encapsulation):** Nitrogen-blanketed lipid suspension tanks, gelatin melting kettles, rotary-die softgel encapsulation, low-humidity drying tunnels, visual optical sorting, and automated bottling.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              CANNOT-PASS MANUFACTURING LOT GENEALOGY                                   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 1. INBOUND RAW MATERIAL RELEASE                    ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Raw materials (`RAW-ECH-EXT4`, `RAW-OMEGA3-70`, etc.) analytically tested and Released in ERP.     │
 │ • Acumatica hard-lock: Work Orders (`AMProdItem`) reject any Lot on `QC Hold` or `Quarantine`.        │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 2. BATCH PRODUCTION WORK ORDER (`AMProdItem`)      ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Work Order issued against Bill of Materials (`AMBOMItem`) & Routing operations.                    │
 │ • Barcode lot scanning allocates specific raw lots (e.g. `LOT-EC2603-01A`) to the production batch.   │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 3. FINISHED DOSAGE CONVERSION                      ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • High-speed Encapsulation (Veg-Caps) or Rotary Die Softgel Encapsulation.                           │
 │ • In-process QC testing: Fill weight variation, shell moisture, disintegration, metal detection.     │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 4. FINISHED PRODUCT LOT QUARANTINE & RELEASE       ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Finished lot created (e.g. `LOT-FG-IMM-260301`) in `QC Hold`.                                      │
 │ • Full finished product testing (potency assay, disintegration, heavy metals, microbial).            │
 │ • If compliant: Lot status set to "Released" -> Available for consumer distribution.                 │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Manufactured Finished Goods Portfolio

| Finished Inventory ID | Commercial Brand & Description | Dosage Form | Pack Size | Health Canada NPN | Bill of Materials ID | Quality Inspection Plan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`FG-IMMUNE-DEFENSE-60C`** | **ImmunoShield Botanical Active Plus** | Two-Piece Veg Capsule (Size 00) | 60 Caps / Bottle | `NPN-80099412` | `BOM-IMMUNE-DEF-01` | `QPLAN-FG-IMMUNE60` |
| **`FG-CARDIO-OMEGA-COQ10-60SG`** | **CardioPure Ultra Omega-3 + CoQ10 & Astaxanthin** | Rotary Die Softgel (20 Oblong) | 60 Softgels / Bottle | `NPN-80099418` | `BOM-CARDIO-OM3-01` | `QPLAN-FG-CARDIO60` |

---

## 3. Raw Ingredient Consumption Matrix

The manufactured products directly consume raw active ingredients supplied by qualified vendors:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FINISHED PRODUCT BILL OF MATERIALS                                   │
├──────────────────────────────────────┬─────────────────────────────────────────────────────────────────┤
│ MANUFACTURED FINISHED GOOD           │ CONSUMED RAW MATERIALS (PURCHASED INGREDIENTS)                  │
├──────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ FG-IMMUNE-DEFENSE-60C                │ • RAW-ECH-EXT4  (Echinacea 4% from VEND-NORTH-BIO)              │
│ (ImmunoShield Botanical Active Plus) │ • RAW-ELD-EXT10 (Elderberry 10% from VEND-NORTH-BIO)             │
│                                      │ • RAW-ASH-EXT5  (Ashwagandha 5% from VEND-ALPINE-EXT)            │
├──────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ FG-CARDIO-OMEGA-COQ10-60SG           │ • RAW-OMEGA3-70 (Marine Omega-3 TG Oil from VEND-NORDIC-MAR)    │
│ (CardioPure Ultra Omega + CoQ10)     │ • RAW-COQ10-99  (Pure CoQ10 USP from VEND-NIPPON-PHARMA)        │
│                                      │ • RAW-ASTA-10   (Astaxanthin Oleoresin from VEND-NORDIC-MAR)    │
└──────────────────────────────────────┴─────────────────────────────────────────────────────────────────┘
```

---

## 4. Regulatory Traceability & Lot Genealogy (Health Canada & SFCR)

Under Health Canada GMP (GUI-0001) and CFIA Safe Food for Canadians Regulations:
* Every finished batch record maintains full bi-directional lot genealogy in Acumatica:
  $$\text{Raw Material Vendor Lots} \longrightarrow \text{Manufacturing Work Order} \longrightarrow \text{Finished Goods Lot} \longrightarrow \text{Customer Sales Orders / Shipments}$$
* Enables instantaneous recall capability: 100% material traceability backwards to supplier harvest/batch and forward to retail distribution within $< 2\text{ hours}$.
