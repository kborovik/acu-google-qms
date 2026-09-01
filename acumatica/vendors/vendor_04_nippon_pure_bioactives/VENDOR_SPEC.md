# Vendor Profile Specification: Nippon Pure Bioactives Inc.
## Acumatica Cloud ERP Vendor Master: `VEND-NIPPON-PHARMA`

---

## 1. Corporate & Commercial Information

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            VENDOR AT A GLANCE                               │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Acumatica Vendor ID:     │ VEND-NIPPON-PHARMA                               │
│ Legal Name:              │ Nippon Pure Bioactives Corporation               │
│ Operating Country:       │ Japan (Chuo-ku, Tokyo)                           │
│ Vendor Class:            │ RAW_API_FERMENTATION                             │
│ Currency / Payment Terms:│ USD / NET45                                      │
│ Health Canada Foreign Lic│ Foreign Site Annex FSA-JP-TK-883921              │
│ Quality Rating Tier:     │ Tier-1 Preferred (99.8% Historical Pass Rate)    │
│ Average Lead Time:       │ 21 Business Days (Air Freight Expedited)         │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Facility & Contact Details
* **Headquarters / Production Complex:** 2-8-1 Nihonbashi Honcho, Chuo-ku, Tokyo 103-0023, Japan
* **Quality Assurance Director:** Kenji Takahashi, Ph.D. (`k-takahashi@nippon-purebio.co.jp` / +81-3-5555-4819)
* **International Export Division:** `intl-sales@nippon-purebio.co.jp`

---

## 2. Regulatory Licences & Certifications

* **Japan PMDA GMP Compliance:** Pharmaceutical and Medical Devices Agency (PMDA) Certificate #JP-GMP-2024-819.
* **US FDA Drug Master File (DMF):** DMF #029481 on file for active pharmaceutical and high-purity dietary ingredients.
* **Health Canada Foreign Site Annex:** FSA-JP-TK-883921 for importing fermentation APIs into Canadian GMP facilities.
* **ISO Accreditations:** ISO 9001:2015 and ISO 14001:2015.

---

## 3. Supplied Product Portfolio

Nippon Pure Bioactives Inc. supplies ultra-high purity fermentation-derived active ingredients:

| Product Code | Description | Item Class | Primary Inspection Plan | Default QC Bay |
| :--- | :--- | :--- | :--- | :--- |
| **`RAW-COQ10-99`** | Pure Coenzyme Q10 (Ubiquinone) USP Grade 99.0% - 101.0% | `RAW_API_FERMENTATION` | `QPLAN-API-COQ10` | `QC-HOLD-BAY-C` |
| **`RAW-THEA-98`** | Pure L-Theanine 98.5% Fermentation High-Purity Powder | `RAW_API_FERMENTATION` | `QPLAN-API-THEA98` | `QC-HOLD-BAY-C` |

---

## 4. Inbound Quality Governance & Testing Routing

1. **Analytical Testing Routing:**
   * Primary Laboratory: **Great Lakes Bio-Analytical Services Inc.** (`LAB-GL-ANALYTICAL`) for High-Resolution UPLC/DAD Potency Assays, Specific Optical Rotation polarimetry, and Residue on Ignition.
   * Secondary Laboratory: **Pacific Rim BioNutra Testing Laboratories Ltd.** (`LAB-PACIFIC-TEST`) for USP <467> residual solvent profiling and bioburden testing.
2. **Receiving Tolerance & Rejection Criteria:**
   * Ubiquinone assay must conform strictly within $99.0\% - 101.0\%$ (w/w).
   * L-Theanine specific optical rotation $[\alpha]_D^{20}$ must fall between $+7.7^\circ \text{ and } +8.5^\circ$.
   * Strict Heavy Metals limits: Lead $\le 0.20$ ppm, Arsenic $\le 0.50$ ppm.
