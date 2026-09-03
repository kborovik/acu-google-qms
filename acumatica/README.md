# Acumatica Cloud ERP Quality Management & Inbound Compliance Specifications
## Multi-Vendor, Multi-Product, In-House Manufacturing & Testing Laboratory Specification Suite

---

## 1. Executive Summary

This directory contains the canonical specifications for:
* **5 Qualified Global Suppliers** (`VEND-NORTH-BIO`, `VEND-ALPINE-EXT`, `VEND-PACIFIC-ORG`, `VEND-NIPPON-PHARMA`, `VEND-NORDIC-MAR`).
* **10 Active Raw Ingredients & Botanical Extracts** (2 products per vendor).
* **2 In-House Manufactured Finished Products** produced by **CanNordic BioNutra Inc.** from raw ingredients under Health Canada Site Licence #302194.
* **5 ISO/IEC 17025 Accredited Third-Party Analytical Testing Laboratories** (`LAB-GL-ANALYTICAL`, `LAB-EURO-PHYTO`, `LAB-PACIFIC-TEST`, `LAB-TOKYO-BIO`, `LAB-FJORD-ANALYTICAL`), each dedicated to a supplier and featuring distinct document standards, units of measure (converted to standard SI), and multilingual bilingual synonym mappings.

The specification suite defines the end-to-end data schemas, quality inspection plans, tolerance boundaries, regulatory compliance thresholds (under **Health Canada Natural Health Products Regulations SOR/2003-196**, **GMP GUI-0001/GUI-0158**, **CFIA SFCR**, and **USP Pharmacopeial Standards**), and automated lot release governance workflows.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       ACUMATICA QUALITY & MANUFACTURING TOPOLOGY                                       │
├───────────────────────────────┬───────────────────────────────────┬───────────────────────────────────┬────────────────┤
│ QUALIFIED VENDOR              │ RAW MATERIAL PRODUCTS             │ DEDICATED TESTING LAB             │ DOCUMENT & UOM │
├───────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼────────────────┤
│ 1. Northern BioNutra Imports  │ • RAW-ECH-EXT4 (Echinacea 4%)     │ Great Lakes Bio-Analytical        │ Health Canada  │
│    (VEND-NORTH-BIO / Canada)  │ • RAW-ELD-EXT10 (Elderberry 10%)  │ (LAB-GL-ANALYTICAL - CALA #9481)  │ CALA Standard  │
│                               │                                   │ Specialist: HPLC & ICP-MS         │ (EN/FR; SI)    │
├───────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼────────────────┤
│ 2. Alpine Botanical Extracts  │ • RAW-ASH-EXT5 (Ashwagandha 5%)   │ Euro-Phyto Analytics GmbH         │ Ph. Eur. / DIN │
│    (VEND-ALPINE-EXT / Germany)│ • RAW-RHOD-EXT3 (Rhodiola 3%)     │ (LAB-EURO-PHYTO - DAkkS #14192)   │ Prüfbericht    │
│                               │                                   │ Specialist: Ph. Eur. Assays, LOD  │ (DE/EN; % m/m) │
├───────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼────────────────┤
│ 3. Pacific Organic Ingredients│ • RAW-CURC-95 (Curcumin 95%)      │ Pacific Rim BioNutra Labs         │ SCC & AOAC PTM │
│    (VEND-PACIFIC-ORG / Canada)│ • RAW-GUT-PRB100 (Probiotics 100B)│ (LAB-PACIFIC-TEST - SCC #8172)    │ Dietary Spec   │
│                               │                                   │ Specialist: Probiotics, Solvents  │ (EN/FR; GCFU)  │
├───────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼────────────────┤
│ 4. Nippon Pure Bioactives     │ • RAW-COQ10-99 (CoQ10 99% Pure)   │ Tokyo Bio-Analytical Labs Inc.    │ JP 18 / JIS    │
│    (VEND-NIPPON-PHARMA / JP)  │ • RAW-THEA-98 (L-Theanine 98%)    │ (LAB-TOKYO-BIO - JNLA #09418)     │ 試験成績書     │
│                               │                                   │ Specialist: Fermentation API, ORD │ (JA/EN; mass%) │
├───────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼────────────────┤
│ 5. Nordic Marine Extracts     │ • RAW-OMEGA3-70 (Omega-3 Oil 70%) │ Fjord Marine Bio-Testing Labs AS  │ GOED Monograph │
│    (VEND-NORDIC-MAR / Norway) │ • RAW-ASTA-10 (Astaxanthin 10%)   │ (LAB-FJORD-ANALYTICAL - NA #092)  │ Analysesert.   │
│                               │                                   │ Specialist: Marine Lipids, TOTOX  │ (NO/EN; mg/g)  │
├───────────────────────────────┴───────────────────────────────────┴───────────────────────────────────┴────────────────┤
│ IN-HOUSE CDMO MANUFACTURED FINISHED GOODS (CanNordic BioNutra Inc. - Site Licence #302194)                             │
├──────────────────────────────────────┬────────────────────────────────────┬────────────────────────────────────────────┤
│ Finished Product Inventory ID        │ Dosage Form & Pack Size            │ Ingredients Consumed (BOM)                 │
├──────────────────────────────────────┼────────────────────────────────────┼────────────────────────────────────────────┤
│ • FG-IMMUNE-DEFENSE-60C              │ Two-Piece Veg Capsule (Size 00)    │ • RAW-ECH-EXT4  (200 mg)                   │
│   (ImmunoShield Botanical Active)    │ 60 Veg Caps / Bottle (NPN-80099412)│ • RAW-ELD-EXT10 (150 mg)                   │
│                                      │                                    │ • RAW-ASH-EXT5  (100 mg)                   │
│                                      │                                    │                                            │
│ • FG-CARDIO-OMEGA-COQ10-60SG         │ Rotary Die Softgel (20 Oblong Ruby)│ • RAW-OMEGA3-70 (1,000 mg)                 │
│   (CardioPure Ultra Omega + CoQ10)   │ 60 Softgels / Bottle (NPN-80099418)│ • RAW-COQ10-99  (101 mg)                   │
│                                      │                                    │ • RAW-ASTA-10   (20 mg)                    │
└──────────────────────────────────────┴────────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 2. Specification Directory Structure

```
acumatica/
├── README.md                                  <- Master specification index and topology (This File)
├── acumatica_integration_matrix.md            <- Complete REST API mapping, state machine & QMS contracts
├── master_data/                               <- Enterprise Master Data JSON Payloads for Acumatica
│   ├── vendors.json                           <- 5 Vendor master profiles with Acumatica schema
│   ├── products.json                          <- 10 Raw Materials + 2 Manufactured Finished Goods
│   ├── test_labs.json                         <- 5 Laboratory profiles, accreditations, standards & UoM matrix
│   └── qms_inspection_plans.json              <- Acumatica QMS Inspection Plans & tolerance thresholds
├── vendors/                                   <- Vendor Profiles & Inbound Product Specifications
│   ├── vendor_01_northern_bionutra/
│   │   ├── VENDOR_SPEC.md                     <- Vendor Profile: Northern BioNutra Imports Corp.
│   │   └── products/
│   │       ├── RAW-ECH-EXT4_organic_echinacea.md
│   │       └── RAW-ELD-EXT10_elderberry_extract.md
│   ├── vendor_02_alpine_botanicals/
│   │   ├── VENDOR_SPEC.md                     <- Vendor Profile: Alpine Botanical Extracts GmbH
│   │   └── products/
│   │       ├── RAW-ASH-EXT5_organic_ashwagandha.md
│   │       └── RAW-RHOD-EXT3_rhodiola_rosea.md
│   ├── vendor_03_pacific_organic/
│   │   ├── VENDOR_SPEC.md                     <- Vendor Profile: Pacific Organic Ingredients Ltd.
│   │   └── products/
│   │       ├── RAW-CURC-95_turmeric_curcumin.md
│   │       └── RAW-GUT-PRB100_probiotic_blend.md
│   ├── vendor_04_nippon_pure_bioactives/
│   │   ├── VENDOR_SPEC.md                     <- Vendor Profile: Nippon Pure Bioactives Inc.
│   │   └── products/
│   │       ├── RAW-COQ10-99_coenzyme_q10.md
│   │       └── RAW-THEA-98_l_theanine.md
│   └── vendor_05_nordic_marine_extracts/
│       ├── VENDOR_SPEC.md                     <- Vendor Profile: Nordic Marine Extracts AS
│       └── products/
│           ├── RAW-OMEGA3-70_marine_omega3_oil.md
│           └── RAW-ASTA-10_astaxanthin_oleoresin.md
├── manufactured_products/                     <- In-House Finished Products Manufactured by CanNordic
│   ├── MANUFACTURING_SPEC.md                  <- CDMO Manufacturing Overview, BOM & Lot Traceability
│   ├── FG-IMMUNE-DEFENSE-60C_immunoshield.md  <- ImmunoShield Botanical Active Plus (Capsules)
│   └── FG-CARDIO-OMEGA-COQ10-60SG_cardiopure.md <- CardioPure Ultra Omega + CoQ10 (Softgels)
└── labs/                                      <- Testing Laboratory Capabilities & Accreditations
    ├── LAB-01_great_lakes_bioanalytical.md    <- Great Lakes Bio-Analytical Services (ISO 17025 / CALA)
    ├── LAB-02_pacific_rim_bionutra_labs.md    <- Pacific Rim BioNutra Testing Labs (ISO 17025 / SCC)
    ├── LAB-03_euro_phyto_analytics.md         <- Euro-Phyto Analytics GmbH (DIN EN ISO 17025 / DAkkS)
    ├── LAB-04_tokyo_bioanalytical.md          <- Tokyo Bio-Analytical Testing Labs (JP 18 / JNLA)
    └── LAB-05_fjord_marine_biolabs.md         <- Fjord Marine Bio-Testing Labs AS (GOED / NA)
```

---

## 3. End-to-End Lot Traceability & Release Gate

```
[Inbound Raw Materials from 5 Vendors via 5 Testing Labs]
               │
               ▼
[AI Multi-Standard CoA Normalizer & Unit Converter (SI)]
               │
               ▼
[Acumatica QMS Tolerance Evaluation Engine: QPLAN-*]
               │
               ▼
[Lot Status: "Released"] ──▶ [Acumatica Manufacturing Work Order: AMProdItem]
                                             │
                                             ▼
                               [Batch Conversion: Blending / Encapsulation]
                                             │
                                             ▼
                               [Finished Good Lot Created in "QC Hold"]
                                             │
                                             ▼
                               [Finished Product Testing: QPLAN-FG-*]
                                             │
                                             ▼
                               [Finished Lot Status: "Released" to Market]
```

For full implementation schemas, REST contracts, and lot disposition state machines, refer to [`acumatica_integration_matrix.md`](./acumatica_integration_matrix.md).
