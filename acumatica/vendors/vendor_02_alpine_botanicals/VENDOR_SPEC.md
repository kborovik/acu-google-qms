# Vendor Profile Specification: Alpine Botanical Extracts GmbH
## Acumatica Cloud ERP Vendor Master: `VEND-ALPINE-EXT`

---

## 1. Corporate & Commercial Information

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            VENDOR AT A GLANCE                               │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Acumatica Vendor ID:     │ VEND-ALPINE-EXT                                  │
│ Legal Name:              │ Alpine Botanical Extracts GmbH & Co. KG          │
│ Operating Country:       │ Germany (Holzminden, Lower Saxony)               │
│ Vendor Class:            │ RAW_BOTANICAL_IMPORT                             │
│ Currency / Payment Terms:│ EUR / NET60                                      │
│ Health Canada Foreign Lic│ Foreign Site Annex FSA-EU-DE-910482              │
│ Quality Rating Tier:     │ Tier-1 Preferred (98.9% Historical Pass Rate)    │
│ Average Lead Time:       │ 18 Business Days (Air/Ocean Freight)             │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Facility & Contact Details
* **Headquarters / Manufacturing Facility:** Industriestrasse 42, 37603 Holzminden, Lower Saxony, Germany
* **Head of Quality & Compliance:** Dr. Klaus Richter (`quality@alpine-extracts.de` / +49-5531-99201)
* **Export Order Desk:** `export@alpine-extracts.de`

---

## 2. Regulatory Licences & Certifications

* **EU GMP Certification:** Certificate #DE_NI_01_GMP_2025_0044 issued by Lower Saxony State Office for Consumer Protection and Food Safety (LAVES).
* **Health Canada Foreign Site Annex:** Registered under Health Canada GMP Mutual Recognition Agreement (MRA) for EU member states.
* **Organic Certification:** Kiwa BCS Öko-Garantie GmbH (EU Organic Regulation 2018/848 & Canada Organic Regime COR equivalent).
* **ISO Accreditations:** ISO 9001:2015 and ISO 22000:2018.

---

## 3. Supplied Product Portfolio

Alpine Botanical Extracts GmbH supplies premium standardized root and adaptogenic botanical extracts:

| Product Code | Description | Item Class | Primary Inspection Plan | Default QC Bay |
| :--- | :--- | :--- | :--- | :--- |
| **`RAW-ASH-EXT5`** | Organic Ashwagandha Root Extract 5% Withanolides | `RAW_BOTANICAL` | `QPLAN-BOT-ASH5` | `QC-HOLD-BAY-B` |
| **`RAW-RHOD-EXT3`** | Standardized Rhodiola Rosea Extract 3% Rosavins / 1% Salidroside | `RAW_BOTANICAL` | `QPLAN-BOT-RHOD3` | `QC-HOLD-BAY-B` |

---

## 4. Inbound Quality Governance & Testing Routing

1. **Analytical Testing Routing:**
   * Primary Laboratory: **Great Lakes Bio-Analytical Services Inc.** (`LAB-GL-ANALYTICAL`) for Withanolide and Rosavin HPLC-UV/DAD assays.
   * Secondary Laboratory: **Pacific Rim BioNutra Testing Laboratories Ltd.** (`LAB-PACIFIC-TEST`) for USP <467> residual ethanol solvent testing and microbiological bioburden.
2. **Receiving Tolerance & Rejection Criteria:**
   * Ashwagandha withanolides must meet $\ge 5.00\%$ (w/w).
   * Rhodiola must meet dual chemical markers: Total Rosavins $\ge 3.00\%$ and Salidroside $\ge 1.00\%$.
   * Lead (Pb) $\le 0.50$ ppm, Arsenic (As) $\le 1.00$ ppm, Cadmium (Cd) $\le 0.30$ ppm, Mercury (Hg) $\le 0.10$ ppm.
