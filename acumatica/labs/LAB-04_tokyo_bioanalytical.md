# Testing Laboratory Specification: Tokyo Bio-Analytical Testing Laboratories Inc.
## Acumatica Lab Master: `LAB-TOKYO-BIO` | Vendor ID: `VEND-LAB-TOKYOBIO`

---

## 1. Laboratory Profile & Regulatory Accreditation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LABORATORY FACILITY PROFILE                           │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Laboratory Code:         │ LAB-TOKYO-BIO                                    │
│ Acumatica Vendor ID:     │ VEND-LAB-TOKYOBIO                                │
│ Assigned Vendor Partner: │ Nippon Pure Bioactives Inc. (VEND-NIPPON-PHARMA) │
│ Legal Name:              │ Tokyo Bio-Analytical Testing Laboratories Inc.   │
│ Facility Location:       │ 3-14-5 Nihonbashi Muromachi, Chuo-ku,            │
│                          │ Tokyo 103-0022, Japan                            │
│ ISO/IEC Accreditation:   │ JIS Q 17025:2018 / ISO 17025 (JNLA #JNLA-09418) │
│ Japan PMDA Licence:      │ JP-PMDA-LAB-2024-819 (API & Fermentation Testing)│
│ US FDA Registration:     │ FEI-3008491028 (21 CFR Part 211 / API cGMP)      │
│ Health Canada Foreign DEL│ FSA-JP-TK-LAB-4491 (Canada-Japan GMP MRA)        │
│ Turnaround Times:        │ Standard: 5 Days | Rush: 2 Days | Emergency: 24h │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Key Scientific Personnel & Contacts
* **Laboratory Director & Chief Analyst:** Dr. Hiroshi Nakamura, Ph.D., P.Chem. (`h-nakamura@tokyobio-labs.co.jp`)
* **QA & Pharmacopoeial Compliance Officer:** Yuki Tanaka, B.Pharm., CQA (`y-tanaka@tokyobio-labs.co.jp`)
* **Inbound EDI & Ingestion Desk:** `coa-qa@tokyobio-labs.co.jp` | +81-3-5555-8930

---

## 2. Document Standard & Inbound Format

Tokyo Bio-Analytical Testing Laboratories issues analytical results conforming to the **Japanese Pharmacopoeia (JP 18 / 日本薬局方) & JIS Standard (*試験成績書 - Shiken Seisekisho / Certificate of Analysis*)**:
* **Language:** Bilingual Japanese (`ja-JP`) / English (`en-US`).
* **Header Structure:** Includes 成績書番号 (Certificate #), 品名 (Item Name), ロット番号 (Lot #), 製造年月日 (Mfg Date), 有効期限 (Expiry Date), 試験実施日 (Testing Date), and 判定 (Final Disposition / 適合 - Pass).
* **Compliance Framework:** Japanese Pharmacopoeia 18th Edition General Tests (JP 1.07 Heavy Metals, JP 2.41 LOD, JP 2.44 Residue on Ignition, JP 2.49 Polarimetry).

---

## 3. Core Analytical Competencies & Validated Methods Scope

### 3.1 Fermentation API Purity & Potency (JP / USP Monographs)
* **Instrumentation:** Waters ACQUITY UPLC H-Class PLUS with Photodiode Array (PDA) & QDa Mass Detector.
* **Methods:** High-resolution gradient reversed-phase chromatography for Ubiquinone (CoQ10) and L-Theanine.
* **Accuracy & Precision:** Repeatability RSD $\le 0.5\%$, Limit of Quantification (LOQ) $0.001\% \text{ (w/w)}$.

### 3.2 High-Precision Polarimetry & Physical Constants
* **Instrumentation:** JASCO P-2000 Digital Polarimeter with Temperature Control ($20.0^\circ\text{C} \pm 0.1^\circ\text{C}$) at Sodium D-line (589 nm).
* **Specific Optical Rotation $[\alpha]_D^{20}$:** Direct measurement per JP 2.49 / USP <781S> in 100 mm micro-cells.

### 3.3 Heavy Metals & Residue on Ignition (JP 1.07, JP 2.44 & ICP-MS)
* **Instrumentation:** Shimadzu ICPMS-2030 Mass Spectrometer and Yamato FO-310 Muffler Furnaces.
* **Detection & Quantification Limits:**
  * **Lead (Pb / 鉛):** $\text{LOQ} = 0.005\text{ ppm (5 ppb)}$
  * **Arsenic (As / ヒ素):** $\text{LOQ} = 0.005\text{ ppm (5 ppb)}$
  * **Cadmium (Cd / カドミウム):** $\text{LOQ} = 0.002\text{ ppm (2 ppb)}$
  * **Mercury (Hg / 水銀):** $\text{LOQ} = 0.001\text{ ppm (1 ppb)}$
  * **Residue on Ignition (強熱残分):** $800^\circ\text{C} \pm 25^\circ\text{C}$ Gravimetric Assay ($\text{LOQ} = 0.01\%$).

---

## 4. Units of Measure (UoM) & Standard SI Conversion Matrix

| Japanese Raw UoM | Standard SI Target UoM | Conversion Algorithm | Parameter Application |
| :--- | :--- | :--- | :--- |
| **`% (w/w)`** or **`質量%`** (mass%) | **`% (w/w)`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | API Potency (Ubiquinone, Theanine) |
| **`ppb`** ($\mu\text{g/kg}$) | **`ppm`** | $\text{value} / 1000.0$ | Trace heavy metals (Pb, As, Cd, Hg) |
| **`ppm`** or **`mg/kg`** | **`ppm`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Elemental impurities & solvents |
| **`度`** / **`deg`** / **`°`** | **`deg (°)`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Specific optical rotation $[\alpha]_D^{20}$ |
| **`強熱残分 %`** | **`% (w/w)`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Residue on Ignition (USP <281>) |
| **`個/g`** or **`CFU/g`** | **`CFU/g`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | TAMC (生菌数), TYMC (真菌数) |

---

## 5. Bilingual Terminology & Analyte Normalization Matrix

| Japanese Term (*試験成績書*) | English Term / Synonym | Canonical Acumatica Parameter | Target Test ID |
| :--- | :--- | :--- | :--- |
| **定量法: ユビデカレノン** | Ubiquinone (CoQ10) Assay | `active_potency` | `ASSAY_COQ10` |
| **定量法: L-テアニン** | Pure L-Theanine Potency | `active_potency` | `ASSAY_THEANINE` |
| **比旋光度 [α]D20** | Specific Optical Rotation | `density_specific_gravity` | `PHYS_OPT_ROT` |
| **強熱残分** | Residue on Ignition (Ash) | `loss_on_drying` | `PHYS_ROI` |
| **乾燥減量** | Loss on Drying | `loss_on_drying` | `PHYS_LOD` |
| **純度試験: 鉛 (Pb)** | Lead (Pb) | `heavy_metal_lead` | `HM_LEAD` |
| **純度試験: ヒ素 (As)** | Arsenic (As) | `heavy_metal_arsenic` | `HM_ARSENIC` |
| **純度試験: カドミウム (Cd)** | Cadmium (Cd) | `heavy_metal_cadmium` | `HM_CADMIUM` |
| **純度試験: 水銀 (Hg)** | Mercury (Hg) | `heavy_metal_mercury` | `HM_MERCURY` |
| **生菌数: 一般生菌数** | Total Aerobic Microbial Count | `microbial_tamc` | `MICRO_TAMC` |
| **真菌数 (カビ・酵母)** | Total Combined Yeast & Mold | `microbial_tymc` | `MICRO_TYMC` |
| **大腸菌 (不検出 / 陰性)** | E. coli (Absent in 10g) | `pathogen_e_coli` | `PATH_ECOLI` |
| **サルモネラ (不検出 / 陰性)** | Salmonella (Absent in 25g)| `pathogen_salmonella` | `PATH_SALM` |
| **残留溶媒 (エタノール)** | Residual Solvents (Ethanol) | `residual_solvents` | `SOLV_ETHANOL` |

---

## 6. Acumatica QMS Digital Integration Schema & Payload

Payloads from Tokyo Bio-Analytical feed directly into Acumatica `QMSInspectionOrder`:

```json
{
  "lab_identifier": "LAB-TOKYO-BIO",
  "certificate_number": "SHIKEN-TB-2026-90412",
  "issue_date": "2026-03-01T11:00:00Z",
  "document_standard": "JP18_JIS_SHIKEN_SEISEKISHO",
  "sample_details": {
    "acumatica_inventory_id": "RAW-COQ10-99",
    "lot_serial_nbr": "LOT-CQ2603-08A",
    "client_po": "PO-049220",
    "vendor_id": "VEND-NIPPON-PHARMA"
  },
  "analytical_results": [
    {
      "test_name": "定量法: ユビデカレノン",
      "canonical_parameter": "active_potency",
      "method": "HPLC-UV (JP 18 / USP Monograph)",
      "specification": "99.0 - 101.0 %",
      "result_raw_numeric": 99.82,
      "result_raw_uom": "% (w/w)",
      "normalized_numeric": 99.82,
      "normalized_uom": "% (w/w)",
      "disposition": "PASS"
    },
    {
      "test_name": "強熱残分",
      "canonical_parameter": "loss_on_drying",
      "method": "JP 2.44 / USP <281>",
      "specification": "<= 0.10 %",
      "result_raw_numeric": 0.038,
      "result_raw_uom": "%",
      "normalized_numeric": 0.038,
      "normalized_uom": "% (w/w)",
      "disposition": "PASS"
    },
    {
      "test_name": "純度試験: 鉛 (Pb)",
      "canonical_parameter": "heavy_metal_lead",
      "method": "ICP-MS (JP 1.07)",
      "specification": "<= 0.20 ppm",
      "result_raw_numeric": 24.0,
      "result_raw_uom": "ppb",
      "normalized_numeric": 0.024,
      "normalized_uom": "ppm",
      "disposition": "PASS"
    },
    {
      "test_name": "生菌数: 一般生菌数 (TAMC)",
      "canonical_parameter": "microbial_tamc",
      "method": "JP 4.05",
      "specification": "<= 1000 CFU/g",
      "result_raw_numeric": 45.0,
      "result_raw_uom": "個/g",
      "normalized_numeric": 45.0,
      "normalized_uom": "CFU/g",
      "disposition": "PASS"
    }
  ],
  "authorized_signatory": "Dr. Hiroshi Nakamura, Ph.D., P.Chem."
}
```
