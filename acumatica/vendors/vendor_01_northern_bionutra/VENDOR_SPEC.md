# Vendor Profile Specification: Northern BioNutra Imports Corp.
## Acumatica Cloud ERP Vendor Master: `VEND-NORTH-BIO`

---

## 1. Corporate & Commercial Information

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            VENDOR AT A GLANCE                               │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Acumatica Vendor ID:     │ VEND-NORTH-BIO                                   │
│ Legal Name:              │ Northern BioNutra Imports Corporation            │
│ Operating Country:       │ Canada (Mississauga, Ontario)                    │
│ Vendor Class:            │ RAW_BOTANICAL                                    │
│ Currency / Payment Terms:│ CAD / NET30                                      │
│ Health Canada Site Lic:  │ #302194 / Foreign Site Annex FSA-CA-ON-449102    │
│ Quality Rating Tier:     │ Tier-1 Preferred (99.4% Historical Pass Rate)    │
│ Average Lead Time:       │ 5 Business Days                                  │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Facility & Contact Details
* **Headquarters / Warehouse:** 1450 Meadowpine Blvd, Suite 300, Mississauga, ON L5N 6S2, Canada
* **QA / Regulatory Director:** Jean-Pierre Tremblay (`qa@northernbionutra.ca` / +1-905-555-0192)
* **Inbound Order Desk:** `orders@northernbionutra.ca`

---

## 2. Regulatory Licences & Certifications

* **Health Canada Good Manufacturing Practices (GMP):** Compliant with GUI-0001 / GUI-0158 Part 3 of Natural Health Products Regulations.
* **NSF / ANSI 455-2 Dietary Supplement GMP Certification:** Certificate #NSF-GMP-2025-0812 (Valid thru August 2027).
* **Pro-Cert Organic Systems:** Canada Organic Regime (COR) & USDA NOP Certified Organic Handler #COR-92810.
* **HACCP / GFSI Scheme:** FSSC 22000 Version 5.1 Certified.

---

## 3. Supplied Product Portfolio

Northern BioNutra Imports Corp. is the qualified sole-source supplier for the following raw materials:

| Product Code | Description | Item Class | Primary Inspection Plan | Default QC Bay |
| :--- | :--- | :--- | :--- | :--- |
| **`RAW-ECH-EXT4`** | Organic Echinacea Purpurea Extract 4% Polyphenols | `RAW_BOTANICAL` | `QPLAN-BOT-ECH4` | `QC-HOLD-BAY-A` |
| **`RAW-ELD-EXT10`** | Organic European Elderberry Extract 10% Anthocyanins | `RAW_BOTANICAL` | `QPLAN-BOT-ELD10` | `QC-HOLD-BAY-A` |

---

## 4. Inbound Quality Governance & Testing Routing

1. **Analytical Testing Routing:**
   * Primary Laboratory: **Great Lakes Bio-Analytical Services Inc.** (`LAB-GL-ANALYTICAL` / CALA #9481) for Active Polyphenols / Anthocyanins HPLC assays and Heavy Metals ICP-MS.
   * Secondary Laboratory: **Pacific Rim BioNutra Testing Laboratories Ltd.** (`LAB-PACIFIC-TEST` / SCC #8172) for USP <2021>/<2022> microbiological verification.
2. **Receiving Tolerance & Rejection Criteria:**
   * Failure of active potency below specification lower bound triggers automatic Quarantine and NCR.
   * Any heavy metal breach exceeding Health Canada Category 1 limits (Pb > 0.50 ppm, As > 1.00 ppm, Cd > 0.30 ppm, Hg > 0.10 ppm) triggers immediate quarantine segregation and vendor chargeback.
