# Testing Laboratory Specification: Euro-Phyto Analytics GmbH
## Acumatica Lab Master: `LAB-EURO-PHYTO` | Vendor ID: `VEND-LAB-EUROPHYTO`

---

## 1. Laboratory Profile & Regulatory Accreditation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LABORATORY FACILITY PROFILE                           │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Laboratory Code:         │ LAB-EURO-PHYTO                                   │
│ Acumatica Vendor ID:     │ VEND-LAB-EUROPHYTO                               │
│ Assigned Vendor Partner: │ Alpine Botanical Extracts GmbH (VEND-ALPINE-EXT) │
│ Legal Name:              │ Euro-Phyto Analytics GmbH                        │
│ Facility Location:       │ Am Gewerbepark 14, 80807 München,                │
│                          │ Bavaria, Germany                                 │
│ ISO/IEC Accreditation:   │ DIN EN ISO/IEC 17025:2018 (DAkkS #D-PL-14192-01) │
│ EU GMP Licence:          │ DE_BY_01_GMP_2025_0112 (Regierung von Oberbayern)│
│ Health Canada Foreign DEL│ FSA-EU-DE-LAB-9182 (Canada-EU MRA Compliant)     │
│ Turnaround Times:        │ Standard: 6 Days | Rush: 2 Days | Emergency: 24h │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Key Scientific Personnel & Contacts
* **Laboratory Director & Chief Chemist:** Dr. Manfred Weiss, Dr. rer. nat., Dipl.-Chem. (`m.weiss@europhyto-analytics.de`)
* **QA & Compliance Manager:** Hanna Lindner, M.Sc. (`h.lindner@europhyto-analytics.de`)
* **Inbound Digital Dispatch / Webhook Intake:** `pruefbericht@europhyto-analytics.de` | +49-89-555-73910

---

## 2. Document Standard & Inbound Format

Euro-Phyto Analytics issues Certificates of Analysis adhering to the **European Pharmacopoeia (Ph. Eur.) & DIN EN ISO/IEC 17025 standard (*Prüfbericht / Prüfzertifikat*)**:
* **Language:** Bilingual German (`de-DE`) / English (`en-GB`).
* **Header Structure:** Contains DIN Prüfbericht-Nr., Probenbezeichnung (Sample Description), Chargen-Nr. (Lot #), Eingangsdatum (Receipt Date), Prüfzeitraum (Testing Period), and Freigabestatus (Disposition).
* **Compliance Framework:** Ph. Eur. 11th Edition general chapters, DIN EN 15763 for heavy metals, and Ph. Eur. 2.4.24 for residual solvents.

---

## 3. Core Analytical Competencies & Validated Methods

### 3.1 Botanical Potency & Marker Standardisation
* **Instrumentation:** Shimadzu Nexera X3 UHPLC with Prominence DAD Detector.
* **Methods:** Ph. Eur. Monographs and DIN HPLC-UV/DAD for Withanolides (Ashwagandha) and Rosavins / Salidroside (Rhodiola).
* **Limit of Quantification (LOQ):** $0.005\% \text{ (m/m)}$.

### 3.2 Heavy Metals & Trace Elemental Impurities (DIN EN 15763 / Ph. Eur. 2.4.27)
* **Instrumentation:** Agilent 7900 ICP-MS with Ultra High Matrix Introduction (UHMI).
* **Detection & Quantification Limits:**
  * **Lead (Pb / Blei):** $\text{LOQ} = 0.005\text{ mg/kg}$
  * **Arsenic (As / Arsen):** $\text{LOQ} = 0.005\text{ mg/kg}$
  * **Cadmium (Cd / Cadmium):** $\text{LOQ} = 0.002\text{ mg/kg}$
  * **Mercury (Hg / Quecksilber):** $\text{LOQ} = 0.001\text{ mg/kg}$

### 3.3 Physical-Chemical & Residual Solvents (Ph. Eur. 2.2.32 & 2.4.24)
* **Trocknungsverlust (Loss on Drying):** Ph. Eur. 2.2.32 (Sartorius MA100 Infrared Moisture Analyzers).
* **Restlösemittel (Residual Solvents):** Ph. Eur. 2.4.24 Headspace GC-FID (Thermo Scientific TRACE 1310 with TriPlus 500).

---

## 4. Units of Measure (UoM) & Standard SI Conversion Matrix

| German / European Raw UoM | Standard SI Target UoM | Conversion Algorithm | Parameter Application |
| :--- | :--- | :--- | :--- |
| **`% (m/m)`** (Massenanteil) | **`% (w/w)`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Botanical marker potency, Trocknungsverlust |
| **`g/100g`** | **`% (w/w)`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Assay active percentage |
| **`g/kg`** | **`% (w/w)`** | $\text{value} / 10.0$ | Phytochemical concentrations |
| **`mg/kg`** or **`μg/g`** | **`ppm`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Heavy metals (Pb, As, Cd, Hg), Solvents |
| **`KbE/g`** (Koloniebildende E.)| **`CFU/g`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | TAMC (Gesamtkeimzahl), TYMC (Hefen/Pilze) |

---

## 5. Bilingual Terminology & Analyte Normalization Matrix

| German Term (*Prüfbericht*) | English Term / Synonym | Canonical Acumatica Parameter | Target Test ID |
| :--- | :--- | :--- | :--- |
| **Withanolid-Gesamtgehalt** | Total Withanolides Assay | `active_potency` | `ASSAY_WITHANOLIDES` |
| **Rosavine gesamt** | Total Rosavins Content | `active_potency` | `ASSAY_ROSAVINS` |
| **Salidrosid-Gehalt** | Salidroside Assay | `active_potency` | `ASSAY_SALIDROSIDE` |
| **Trocknungsverlust** | Loss on Drying (LOD) | `loss_on_drying` | `PHYS_LOD` |
| **Blei (Pb)** | Lead (Pb) | `heavy_metal_lead` | `HM_LEAD` |
| **Arsen (As)** | Arsenic (As) | `heavy_metal_arsenic` | `HM_ARSENIC` |
| **Cadmium (Cd)** | Cadmium (Cd) | `heavy_metal_cadmium` | `HM_CADMIUM` |
| **Quecksilber (Hg)** | Mercury (Hg) | `heavy_metal_mercury` | `HM_MERCURY` |
| **Gesamtkeimzahl (TAMC)** | Total Aerobic Microbial Count | `microbial_tamc` | `MICRO_TAMC` |
| **Hefen und Schimmelpilze** | Total Combined Yeast & Mold | `microbial_tymc` | `MICRO_TYMC` |
| **Escherichia coli (Nicht nachweisbar)**| E. coli (Absent in 10g) | `pathogen_e_coli` | `PATH_ECOLI` |
| **Salmonellen (Nicht nachweisbar)** | Salmonella spp. (Absent in 25g)| `pathogen_salmonella` | `PATH_SALM` |
| **Restlösemittel (Ethanol)** | Residual Solvents (Ethanol) | `residual_solvents` | `SOLV_ETHANOL` |

---

## 6. Acumatica QMS Digital Integration Schema & Payload

CoA payloads from Euro-Phyto Analytics are ingested directly into Acumatica `QMSInspectionOrder`:

```json
{
  "lab_identifier": "LAB-EURO-PHYTO",
  "certificate_number": "PRUEF-EP-2026-88192",
  "issue_date": "2026-03-01T14:15:00Z",
  "document_standard": "DIN_EN_ISO17025_PHEUR",
  "sample_details": {
    "acumatica_inventory_id": "RAW-ASH-EXT5",
    "lot_serial_nbr": "LOT-AS2603-12A",
    "client_po": "PO-049215",
    "vendor_id": "VEND-ALPINE-EXT"
  },
  "analytical_results": [
    {
      "test_name": "Withanolid-Gesamtgehalt",
      "canonical_parameter": "active_potency",
      "method": "HPLC-UV (Ph. Eur. Monograph)",
      "specification": ">= 5.00 % (m/m)",
      "result_raw_numeric": 5.42,
      "result_raw_uom": "% (m/m)",
      "normalized_numeric": 5.42,
      "normalized_uom": "% (w/w)",
      "disposition": "PASS"
    },
    {
      "test_name": "Trocknungsverlust (105°C)",
      "canonical_parameter": "loss_on_drying",
      "method": "Ph. Eur. 2.2.32",
      "specification": "<= 5.00 % (m/m)",
      "result_raw_numeric": 3.40,
      "result_raw_uom": "% (m/m)",
      "normalized_numeric": 3.40,
      "normalized_uom": "% (w/w)",
      "disposition": "PASS"
    },
    {
      "test_name": "Blei (Pb)",
      "canonical_parameter": "heavy_metal_lead",
      "method": "ICP-MS (DIN EN 15763)",
      "specification": "<= 0.50 mg/kg",
      "result_raw_numeric": 0.075,
      "result_raw_uom": "mg/kg",
      "normalized_numeric": 0.075,
      "normalized_uom": "ppm",
      "disposition": "PASS"
    },
    {
      "test_name": "Gesamtkeimzahl (TAMC)",
      "canonical_parameter": "microbial_tamc",
      "method": "Ph. Eur. 2.6.12",
      "specification": "<= 10000 KbE/g",
      "result_raw_numeric": 350.0,
      "result_raw_uom": "KbE/g",
      "normalized_numeric": 350.0,
      "normalized_uom": "CFU/g",
      "disposition": "PASS"
    }
  ],
  "authorized_signatory": "Dr. Manfred Weiss, Dr. rer. nat., Dipl.-Chem."
}
```
