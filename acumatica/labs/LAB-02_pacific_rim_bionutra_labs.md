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

## 2. Core Analytical Competencies & Validated Methods Scope

Pacific Rim BioNutra Testing Laboratories is the primary authorized laboratory for microbiological safety, pathogen screening, residual solvents, and organic contaminant profiling:

### 2.1 Microbiological Enumeration & Probiotic Viability
* **Instrumentation:** bioMérieux TEMPO Automated Enumerator and Whitley A35 Anaerobic Workstations.
* **Methods:**
  * **TAMC & TYMC:** USP <2021> / AOAC BAM.
  * **Probiotic Cell Counts:** ISO 7889 / ISO 20128 (Lactic acid bacteria and Bifidobacteria enumeration).
  * **Water Activity ($a_w$):** USP <922> (AquaLab 4TE Chilled-Mirror Dewpoint).

### 2.2 Pathogen Rapid Detection & PCR Screening
* **Instrumentation:** bioMérieux GENE-UP Real-Time PCR System.
* **Validated Pathogen Assays:**
  * *Escherichia coli* (USP <2022>): Absent in 10g ($\text{LOD} = 1\text{ CFU/10g}$).
  * *Salmonella spp.* (USP <2022> / AOAC-RI): Absent in 25g ($\text{LOD} = 1\text{ CFU/25g}$).
  * *Staphylococcus aureus* & *Pseudomonas aeruginosa* (USP <62> / <2022>).

### 2.3 Residual Solvents & Organic Contaminants
* **Instrumentation:** Agilent 7890B GC with 7697A Headspace Autosampler & 5977B MSD.
* **Methods:** USP <467> Residual Solvents (Class 1, 2, and 3 solvents including Ethanol, Methanol, Acetone, Ethyl Acetate, Hexane).
* **Dioxins & PCBs:** Thermo Scientific TSQ 9000 GC-MS/MS & EPA 1613B HRGC-HRMS.

---

## 3. Acumatica QMS Digital Integration & Schema

Digital CoA payloads from Pacific Rim Labs feed directly into Acumatica Quality Management workflows:

```json
{
  "lab_identifier": "LAB-PACIFIC-TEST",
  "certificate_number": "COA-PRL-2026-11840",
  "issue_date": "2026-03-01T16:45:00Z",
  "sample_details": {
    "acumatica_inventory_id": "RAW-GUT-PRB100",
    "lot_serial_nbr": "LOT-PR2603-91B",
    "client_po": "PO-049201"
  },
  "analytical_results": [
    {
      "test_name": "Viable Probiotic Cell Count",
      "method": "ISO 7889 / ISO 20128",
      "specification": ">= 100.0 Billion CFU/g",
      "result_numeric": 118.5,
      "result_uom": "Billion CFU/g",
      "disposition": "PASS"
    },
    {
      "test_name": "Water Activity (Aw)",
      "method": "USP <922>",
      "specification": "<= 0.20 Aw",
      "result_numeric": 0.114,
      "result_uom": "Aw",
      "disposition": "PASS"
    },
    {
      "test_name": "Escherichia coli",
      "method": "USP <2022>",
      "specification": "Absent in 10g",
      "result_text": "Absent in 10g",
      "disposition": "PASS"
    },
    {
      "test_name": "Salmonella spp.",
      "method": "USP <2022>",
      "specification": "Absent in 25g",
      "result_text": "Absent in 25g",
      "disposition": "PASS"
    }
  ],
  "authorized_signatory": "Dr. Fiona MacIntyre, Ph.D., RMCCM"
}
```
