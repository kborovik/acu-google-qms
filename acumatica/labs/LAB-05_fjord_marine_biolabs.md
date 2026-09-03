# Testing Laboratory Specification: Fjord Marine Bio-Testing Laboratories AS
## Acumatica Lab Master: `LAB-FJORD-ANALYTICAL` | Vendor ID: `VEND-LAB-FJORDMAR`

---

## 1. Laboratory Profile & Regulatory Accreditation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LABORATORY FACILITY PROFILE                           │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Laboratory Code:         │ LAB-FJORD-ANALYTICAL                             │
│ Acumatica Vendor ID:     │ VEND-LAB-FJORDMAR                                │
│ Assigned Vendor Partner: │ Nordic Marine Extracts AS (VEND-NORDIC-MAR)      │
│ Legal Name:              │ Fjord Marine Bio-Testing Laboratories AS         │
│ Facility Location:       │ Havnegata 34, 6003 Ålesund,                      │
│                          │ Møre og Romsdal, Norway                          │
│ ISO/IEC Accreditation:   │ NS-EN ISO/IEC 17025:2018 (Norsk Akkreditering #92│
│ Mattilsynet Approval:    │ NO-LAB-HACCP-9481 (Marine & Fishery Testing)     │
│ GOED Monograph Recogn:   │ GOED-LAB-2025-04 (Global EPA & DHA Standard)     │
│ Health Canada Foreign DEL│ FSA-NO-MR-LAB-6729 (Canada-EEA MRA Compliant)    │
│ Turnaround Times:        │ Standard: 5 Days | Rush: 2 Days | Emergency: 36h │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Key Scientific Personnel & Contacts
* **Laboratory Director & Chief Lipid Chemist:** Dr. Solveig Haugen, Ph.D., C.Chem. (`s.haugen@fjordmarinelabs.no`)
* **Director of Trace Contaminants & HRMS:** Eirik Bakke, M.Sc. (`e.bakke@fjordmarinelabs.no`)
* **Inbound Digital Intake & Webhook Desk:** `analyser@fjordmarinelabs.no` | +47-70-198420

---

## 2. Document Standard & Inbound Format

Fjord Marine Bio-Testing Laboratories issues analytical certifications following the **GOED Voluntary Monograph & Ph. Eur. Marine Lipid Standard (*Analysesertifikat*)**:
* **Language:** Bilingual Norwegian (`no-NO`) / English (`en-GB`).
* **Header Structure:** Contains Sertifikatnummer (Certificate #), Prøvemerking (Sample ID), Partinummer / Batch (Lot #), Prøvetakingsdato (Sampling Date), Mottatt dato (Received Date), and Konklusjon (Conclusion / Godkjent - Approved).
* **Compliance Framework:** GOED Voluntary Monograph (2025 Ed.), Ph. Eur. 2.4.29 (Fatty acid GC composition), Ph. Eur. 2.5.5 (Peroxide Value), Ph. Eur. 2.5.7 (Unsaponifiable Matter), EPA Method 1613B (Dioxins/Furans/PCBs).

---

## 3. Core Analytical Competencies & Validated Methods Scope

### 3.1 Marine Fatty Acid Profile & Carotenoid Assays
* **Instrumentation:** Agilent 8890 GC-FID with DB-WAX column (Omega-3 fatty acids) and Waters ACQUITY Arc HPLC with 2998 PDA (Astaxanthin).
* **Methods:** Ph. Eur. 2.4.29 and AOAC Official Method 996.06 for EPA (Eicosapentaenoic Acid), DHA (Docosahexaenoic Acid), and Total Omega-3 Fatty Acids.
* **Astaxanthin Assay:** Reversed-phase HPLC-DAD (Ph. Eur. 2.2.29) standard for *H. pluvialis* oleoresin.

### 3.2 Lipid Oxidation Critical Control Index (PV, p-AV, TOTOX, Acid Value)
* **Instrumentation:** Metrohm 905 Titrando Potentiometric Titrator and UV-Vis Spectrophotometers (350 nm).
* **Methods:**
  * **Peroxide Value (PV / Peroksidverdi):** Ph. Eur. 2.5.5 ($\text{LOQ} = 0.1\text{ meq O}_2/\text{kg}$).
  * **p-Anisidine Value (p-AV / Anisidintall):** Ph. Eur. 2.5.36 / AOCS Cd 18-90 ($\text{LOQ} = 0.5$).
  * **Total Oxidation (TOTOX):** Calculated as $2 \times \text{PV} + \text{p-AV}$ ($\le 26.0$).
  * **Acid Value (Syretall):** Ph. Eur. 2.5.1 ($\text{LOQ} = 0.05\text{ mg KOH/g}$).

### 3.3 High-Resolution Trace Contaminants (Dioxins, PCBs & Heavy Metals)
* **Instrumentation:** Thermo Scientific DFS Magnetic Sector GC-HRMS (EPA 1613B) and PerkinElmer NexION 2000 ICP-MS.
* **Dioxins & Furans (PCDD/F):** $\text{LOQ} = 0.05\text{ pg WHO-PCDD/F-TEQ/g}$.
* **Dioxin-like PCBs:** $\text{LOQ} = 0.1\text{ pg WHO-TEQ/g}$.
* **Inorganic Arsenic Speciation:** HPLC-ICP-MS ($\text{LOQ} = 0.01\text{ mg/kg}$).

---

## 4. Units of Measure (UoM) & Standard SI Conversion Matrix

| Norwegian / Nordic Raw UoM | Standard SI Target UoM | Conversion Algorithm | Parameter Application |
| :--- | :--- | :--- | :--- |
| **`meq O2/kg`** (Peroksidverdi) | **`meq O2/kg`** | $1.0 \times \text{value}$ (Baseline SI unit) | Peroxide Value (PV) |
| **`mmol O2/kg`** | **`meq O2/kg`** | $\text{value} \times 2.0$ | Peroxide Value alternative |
| **`indeks`** / unitless | **`index`** | $1.0 \times \text{value}$ (Dimensionless) | p-Anisidine Value & TOTOX |
| **`mg KOH/g`** (Syretall) | **`mg KOH/g`** | $1.0 \times \text{value}$ (Baseline SI unit) | Acid Value (Free fatty acids) |
| **`mg/g`** (Fettsyrer) | **`% (w/w)`** | $\text{value} / 10.0$ (e.g. $400\text{ mg/g} = 40.0\%$) | EPA, DHA, Astaxanthin Potency |
| **`g/100g`** | **`% (w/w)`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Fatty acid percentage |
| **`pg WHO-TEQ/g`** | **`pg TEQ/g`** | $1.0 \times \text{value}$ (Baseline SI unit) | Dioxins, Furans & Dioxin-like PCBs |
| **`mg/kg`** or **`ppm`** | **`ppm`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Heavy metals (Pb, As, Cd, Hg) |

---

## 5. Bilingual Terminology & Analyte Normalization Matrix

| Norwegian Term (*Analysesertifikat*) | English Term / Synonym | Canonical Acumatica Parameter | Target Test ID |
| :--- | :--- | :--- | :--- |
| **Fettsyreinnhold: EPA** | Eicosapentaenoic Acid (EPA) | `active_potency` | `ASSAY_EPA` |
| **Fettsyreinnhold: DHA** | Docosahexaenoic Acid (DHA) | `active_potency` | `ASSAY_DHA` |
| **Totalt EPA + DHA innhold** | Total EPA and DHA | `active_potency` | `ASSAY_EPA_DHA` |
| **Rent Astaxantin-innhold** | Astaxanthin Oleoresin Content | `active_potency` | `ASSAY_ASTAXANTHIN` |
| **Peroksidverdi (PV)** | Peroxide Value | `other_custom_assay` | `LIPID_PV` |
| **Anisidintall (p-AV)** | p-Anisidine Value | `other_custom_assay` | `LIPID_PAV` |
| **Totalt oksidasjonstall (TOTOX)**| Total Oxidation (TOTOX) | `other_custom_assay` | `LIPID_TOTOX` |
| **Syretall (Acid Value)** | Acid Value (Free Fatty Acids) | `other_custom_assay` | `LIPID_AV` |
| **Bly (Pb)** | Lead (Pb) | `heavy_metal_lead` | `HM_LEAD` |
| **Totalt Arsen (As)** | Total Arsenic (As) | `heavy_metal_arsenic` | `HM_ARSENIC` |
| **Uorganisk Arsen** | Inorganic Arsenic | `heavy_metal_arsenic` | `HM_INORG_AS` |
| **Kadmium (Cd)** | Cadmium (Cd) | `heavy_metal_cadmium` | `HM_CADMIUM` |
| **Kvikksølv (Hg)** | Mercury (Hg) | `heavy_metal_mercury` | `HM_MERCURY` |
| **Dioksiner og dioksinlignende PCB**| Dioxins, Furans & Dioxin-like PCBs | `residual_solvents` | `CONTAM_DIOXIN_PCB` |
| **Totalt kimtall (TAMC)** | Total Aerobic Microbial Count | `microbial_tamc` | `MICRO_TAMC` |
| **Gjær og muggsopp (TYMC)** | Total Combined Yeast & Mold | `microbial_tymc` | `MICRO_TYMC` |

---

## 6. Acumatica QMS Digital Integration Schema & Payload

Payloads from Fjord Marine Laboratories feed directly into Acumatica `QMSInspectionOrder`:

```json
{
  "lab_identifier": "LAB-FJORD-ANALYTICAL",
  "certificate_number": "ANALYS-FJ-2026-77301",
  "issue_date": "2026-03-01T13:30:00Z",
  "document_standard": "GOED_PHEUR_ANALYSESERTIFIKAT",
  "sample_details": {
    "acumatica_inventory_id": "RAW-OMEGA3-70",
    "lot_serial_nbr": "LOT-OM2603-05A",
    "client_po": "PO-049228",
    "vendor_id": "VEND-NORDIC-MAR"
  },
  "analytical_results": [
    {
      "test_name": "Fettsyreinnhold: EPA (Ph. Eur. 2.4.29)",
      "canonical_parameter": "active_potency",
      "method": "GC-FID (Ph. Eur. 2.4.29 / GOED)",
      "specification": ">= 40.0 % (w/w)",
      "result_raw_numeric": 425.0,
      "result_raw_uom": "mg/g",
      "normalized_numeric": 42.5,
      "normalized_uom": "% (w/w)",
      "disposition": "PASS"
    },
    {
      "test_name": "Fettsyreinnhold: DHA (Ph. Eur. 2.4.29)",
      "canonical_parameter": "active_potency",
      "method": "GC-FID (Ph. Eur. 2.4.29 / GOED)",
      "specification": ">= 20.0 % (w/w)",
      "result_raw_numeric": 218.0,
      "result_raw_uom": "mg/g",
      "normalized_numeric": 21.8,
      "normalized_uom": "% (w/w)",
      "disposition": "PASS"
    },
    {
      "test_name": "Peroksidverdi (PV)",
      "canonical_parameter": "other_custom_assay",
      "method": "Ph. Eur. 2.5.5 Potentiometric",
      "specification": "<= 5.0 meq O2/kg",
      "result_raw_numeric": 2.1,
      "result_raw_uom": "meq O2/kg",
      "normalized_numeric": 2.1,
      "normalized_uom": "meq O2/kg",
      "disposition": "PASS"
    },
    {
      "test_name": "Anisidintall (p-AV)",
      "canonical_parameter": "other_custom_assay",
      "method": "Ph. Eur. 2.5.36 Spectrophotometric",
      "specification": "<= 20.0",
      "result_raw_numeric": 11.4,
      "result_raw_uom": "index",
      "normalized_numeric": 11.4,
      "normalized_uom": "index",
      "disposition": "PASS"
    },
    {
      "test_name": "Totalt oksidasjonstall (TOTOX)",
      "canonical_parameter": "other_custom_assay",
      "method": "Calculated (2*PV + p-AV)",
      "specification": "<= 26.0",
      "result_raw_numeric": 15.6,
      "result_raw_uom": "index",
      "normalized_numeric": 15.6,
      "normalized_uom": "index",
      "disposition": "PASS"
    },
    {
      "test_name": "Dioksiner og dioksinlignende PCB",
      "canonical_parameter": "residual_solvents",
      "method": "HRGC-HRMS (EPA 1613B)",
      "specification": "<= 1.75 pg WHO-TEQ/g",
      "result_raw_numeric": 0.42,
      "result_raw_uom": "pg WHO-TEQ/g",
      "normalized_numeric": 0.42,
      "normalized_uom": "pg TEQ/g",
      "disposition": "PASS"
    }
  ],
  "authorized_signatory": "Dr. Solveig Haugen, Ph.D., C.Chem."
}
```
