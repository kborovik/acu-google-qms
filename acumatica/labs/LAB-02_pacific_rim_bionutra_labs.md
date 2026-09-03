# Testing Laboratory Specification: Pacific Rim BioNutra Testing Laboratories Ltd.
## Acumatica Lab Master: `LAB-PACIFIC-TEST` | Vendor ID: `VEND-LAB-PACRIM`

---

## 1. Laboratory Profile & Regulatory Accreditation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LABORATORY FACILITY PROFILE                           │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Laboratory Code:         │ LAB-PACIFIC-TEST                                 │
│ Acumatica Vendor ID:     │ VEND-LAB-PACRIM                                  │
│ Assigned Vendor Partner: │ Pacific Organic Ingredients Ltd. (VEND-PACIFIC)  │
│ Legal Name:              │ Pacific Rim BioNutra Testing Laboratories Ltd.   │
│ Facility Location:       │ 4180 Lougheed Highway, Suite 250,                │
│                          │ Burnaby, BC V5C 6A7, Canada                      │
│ ISO/IEC Accreditation:   │ ISO/IEC 17025:2017 (SCC Scope #8172)             │
│ Health Canada Licence:   │ Drug Establishment Licence (DEL) #203819         │
│ AOAC International:      │ Performance Tested Methods (PTM) #092101         │
│ Turnaround Times:        │ Standard: 5 Days | Rush: 3 Days | Emergency: 36h │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Key Scientific Personnel & Contacts
* **Laboratory Director & Chief Microbiologist:** Dr. Fiona MacIntyre, Ph.D., RMCCM (`f.macintyre@pacificrimlabs.ca`)
* **Director of Analytical Chemistry:** David Suzuki, B.Sc., CQA (`d.suzuki@pacificrimlabs.ca`)
* **Intake Desk & EDI Dispatch:** `intake@pacificrimlabs.ca` | +1-604-555-4491

---

## 2. Document Standard & Inbound Format

Pacific Rim BioNutra Testing Laboratories issues analytical test reports adhering to the **SCC & AOAC PTM / USP Dietary Supplement Testing Standard**:
* **Language:** Bilingual Canadian English (`en-CA`) / Canadian French (`fr-CA`).
* **Header Structure:** Includes Laboratory Reference #, Customer Account, Purchase Order #, Lot/Batch Identifier, Incubation Conditions, Method References, and Quality Assurance Sign-off.
* **Compliance Framework:** Standards Council of Canada (SCC Scope #8172), AOAC Performance Tested Methods (PTM), Health Canada DEL #203819, and USP <2021>/<2022>/<467>.

---

## 3. Core Analytical Competencies & Validated Methods Scope

Pacific Rim BioNutra Testing Laboratories is the primary authorized laboratory for microbiological safety, probiotic enumeration, water activity, and organic solvents:

### 3.1 Microbiological Enumeration & Probiotic Viability
* **Instrumentation:** bioMérieux TEMPO Automated Enumerator and Whitley A35 Anaerobic Workstations.
* **Methods:**
  * **TAMC & TYMC:** USP <2021> / AOAC BAM.
  * **Probiotic Cell Counts:** ISO 7889 / ISO 20128 (Lactic acid bacteria and Bifidobacteria enumeration).
  * **Water Activity ($a_w$):** USP <922> (AquaLab 4TE Chilled-Mirror Dewpoint).

### 3.2 Pathogen Rapid Detection & PCR Screening
* **Instrumentation:** bioMérieux GENE-UP Real-Time PCR System.
* **Validated Pathogen Assays:**
  * *Escherichia coli* (USP <2022>): Absent in 10g ($\text{LOD} = 1\text{ CFU/10g}$).
  * *Salmonella spp.* (USP <2022> / AOAC-RI): Absent in 25g ($\text{LOD} = 1\text{ CFU/25g}$).
  * *Staphylococcus aureus* & *Pseudomonas aeruginosa* (USP <62> / <2022>).

### 3.3 Residual Solvents & Organic Contaminants
* **Instrumentation:** Agilent 7890B GC with 7697A Headspace Autosampler & 5977B MSD.
* **Methods:** USP <467> Residual Solvents (Class 1, 2, and 3 solvents including Ethanol, Methanol, Acetone, Ethyl Acetate, Hexane).
* **Botanical Assays:** Curcuminoids 95% Pure HPLC-DAD (USP Monograph).

---

## 4. Units of Measure (UoM) & Standard SI Conversion Matrix

| Raw Inbound UoM | Standard SI Target UoM | Conversion Algorithm | Parameter Application |
| :--- | :--- | :--- | :--- |
| **`Billion CFU/g`** | **`Billion CFU/g`** | $1.0 \times \text{value}$ (or $\text{value} \times 10^9\text{ CFU/g}$) | Probiotic Live Cell Counts |
| **`Aw`** | **`Aw`** | $1.0 \times \text{value}$ (Dimensionless $0.00-1.00$) | Water Activity (USP <922>) |
| **`% (w/w)`** | **`% (w/w)`** | $1.0 \times \text{value}$ (Baseline SI) | Active Curcuminoid Potency |
| **`ppm`** | **`ppm`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Residual Solvents (Ethanol) |
| **`CFU/g`** | **`CFU/g`** | $1.0 \times \text{value}$ (Baseline SI) | TAMC, TYMC |

---

## 5. Bilingual Terminology & Analyte Normalization Matrix

| English Term (*Certificate*) | French Term (*Certificat d'analyse*) | Canonical Acumatica Parameter | Target Test ID |
| :--- | :--- | :--- | :--- |
| **Viable Probiotic Cell Count** | Numération des probiotiques viables | `active_potency` | `ASSAY_PROBIOTIC_VIABLE` |
| **Total Curcuminoids Purity** | Pureté en curcuminoïdes totaux | `active_potency` | `ASSAY_CURCUMINOIDS` |
| **Water Activity (Aw)** | Activité de l'eau (Aw) | `ph_value` | `PHYS_WATER_ACT` |
| **Residual Solvents (Ethanol)** | Solvants résiduels (Éthanol) | `residual_solvents` | `SOLV_ETHANOL` |
| **Escherichia coli** | Escherichia coli (Absence dans 10g) | `pathogen_e_coli` | `PATH_ECOLI` |
| **Salmonella spp.** | Salmonella spp. (Absence dans 25g) | `pathogen_salmonella` | `PATH_SALM` |
| **Total Aerobic Microbial Count (TAMC)** | Dénombrement germes aérobies totaux | `microbial_tamc` | `MICRO_TAMC` |

---

## 6. Acumatica QMS Digital Integration & Schema

Digital CoA payloads from Pacific Rim Labs feed directly into Acumatica Quality Management workflows:

```json
{
  "lab_identifier": "LAB-PACIFIC-TEST",
  "certificate_number": "COA-PRL-2026-11840",
  "issue_date": "2026-03-01T16:45:00Z",
  "document_standard": "SCC_AOAC_PTM_USP",
  "sample_details": {
    "acumatica_inventory_id": "RAW-GUT-PRB100",
    "lot_serial_nbr": "LOT-PR2603-91B",
    "client_po": "PO-049201",
    "vendor_id": "VEND-PACIFIC-ORG"
  },
  "analytical_results": [
    {
      "test_name": "Viable Probiotic Cell Count",
      "canonical_parameter": "active_potency",
      "method": "ISO 7889 / ISO 20128",
      "specification": ">= 100.0 Billion CFU/g",
      "result_numeric": 118.5,
      "result_uom": "Billion CFU/g",
      "disposition": "PASS"
    },
    {
      "test_name": "Water Activity (Aw)",
      "canonical_parameter": "ph_value",
      "method": "USP <922>",
      "specification": "<= 0.20 Aw",
      "result_numeric": 0.114,
      "result_uom": "Aw",
      "disposition": "PASS"
    },
    {
      "test_name": "Escherichia coli",
      "canonical_parameter": "pathogen_e_coli",
      "method": "USP <2022>",
      "specification": "Absent in 10g",
      "result_text": "Absent in 10g",
      "disposition": "PASS"
    },
    {
      "test_name": "Salmonella spp.",
      "canonical_parameter": "pathogen_salmonella",
      "method": "USP <2022>",
      "specification": "Absent in 25g",
      "result_text": "Absent in 25g",
      "disposition": "PASS"
    }
  ],
  "authorized_signatory": "Dr. Fiona MacIntyre, Ph.D., RMCCM"
}
```
