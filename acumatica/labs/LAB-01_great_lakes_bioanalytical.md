# Testing Laboratory Specification: Great Lakes Bio-Analytical Services Inc.
## Acumatica Lab Master: `LAB-GL-ANALYTICAL` | Vendor ID: `VEND-LAB-GREATLAKES`

---

## 1. Laboratory Profile & Regulatory Accreditation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LABORATORY FACILITY PROFILE                           │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Laboratory Code:         │ LAB-GL-ANALYTICAL                                │
│ Acumatica Vendor ID:     │ VEND-LAB-GREATLAKES                              │
│ Assigned Vendor Partner: │ Northern BioNutra Imports Corp. (VEND-NORTH-BIO) │
│ Legal Name:              │ Great Lakes Bio-Analytical Services Inc.         │
│ Facility Location:       │ 6850 Meadowvale Town Centre Circle, Suite 400,   │
│                          │ Mississauga, ON L5N 2W7, Canada                  │
│ ISO/IEC Accreditation:   │ ISO/IEC 17025:2017 (CALA Scope #9481)            │
│ Health Canada Licence:   │ Drug Establishment Licence (DEL) #104928         │
│ US FDA Registration:     │ FEI-3019284910 (21 CFR Part 111/211 Compliant)   │
│ Turnaround Times:        │ Standard: 5 Days | Rush: 2 Days | Emergency: 24h │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Key Scientific Personnel & Contacts
* **Laboratory Director & Chief Chemist:** Dr. Ronald Henderson, Ph.D., C.Chem. (`r.henderson@greatlakes-analytical.ca`)
* **QA & Regulatory Compliance Manager:** Claire Beaulieu, M.Sc. (`c.beaulieu@greatlakes-analytical.ca`)
* **CoA Inbound / Digital Submission Desk:** `coa-inbound@greatlakes-analytical.ca` | +1-905-555-8820

---

## 2. Document Standard & Inbound Format

Great Lakes Bio-Analytical Services issues Certificates of Analysis adhering to the **Health Canada HPFBI / CALA ISO 17025 Standard**:
* **Language:** Bilingual Canadian English (`en-CA`) / Canadian French (`fr-CA`).
* **Header Structure:** Includes Certificate #, Client PO, Acumatica Inventory ID, Lot/Serial Number, Sampling Date, Issue Date, CALA Scope #9481, and Authorized Electronic Signature.
* **Compliance Framework:** Health Canada GMP Guidelines (GUI-0001 / GUI-0158), Natural Health Products Regulations (SOR/2003-196), and USP Compendial Standards.

---

## 3. Core Analytical Competencies & Validated Methods Scope

Great Lakes Bio-Analytical Services is the primary authorized laboratory for chemical assays, botanical marker standardization, and elemental impurity testing:

### 3.1 Botanical & Active Potency Assays
* **Instrumentation:** Agilent 1290 Infinity II UPLC with Photodiode Array (DAD) and Fluorescence Detectors (FLD).
* **Methods:** USP Monographs, Ph. Eur., AOAC Official Methods for Polyphenols, Anthocyanins, Withanolides, Rosavins/Salidroside, Curcuminoids, Ubidecarenone, and L-Theanine.
* **Limit of Quantification (LOQ):** $0.01\% \text{ (w/w)}$.

### 3.2 Elemental Impurities & Heavy Metals (USP <2232> / AOAC 2013.06)
* **Instrumentation:** PerkinElmer NexION 2000 ICP-MS with Collision Reaction Cell (CRC).
* **Detection & Quantification Limits:**
  * **Lead (Pb):** $\text{LOD} = 0.001\text{ ppm}, \text{LOQ} = 0.005\text{ ppm}$
  * **Arsenic (As):** $\text{LOD} = 0.002\text{ ppm}, \text{LOQ} = 0.005\text{ ppm}$
  * **Cadmium (Cd):** $\text{LOD} = 0.001\text{ ppm}, \text{LOQ} = 0.002\text{ ppm}$
  * **Mercury (Hg):** $\text{LOD} = 0.0005\text{ ppm}, \text{LOQ} = 0.001\text{ ppm}$
  * **Inorganic Arsenic Speciation:** HPLC-ICP-MS ($\text{LOQ} = 0.01\text{ ppm}$).

### 3.3 Physical-Chemical Assays
* **Loss on Drying (Moisture):** USP <731> (Mettler Toledo Halogen Moisture Analyzers & Gravimetric Ovens).
* **Residue on Ignition / Ash:** USP <281> (Carbolite Muffle Furnaces).
* **Melting Range & Specific Optical Rotation:** USP <741> / USP <781S> (Rudolph Autopol VI Automatic Polarimeter).

---

## 4. Units of Measure (UoM) & Standard SI Conversion Matrix

| Raw Inbound UoM | Standard SI Target UoM | Conversion Algorithm | Parameter Application |
| :--- | :--- | :--- | :--- |
| **`% (w/w)`** | **`% (w/w)`** | $1.0 \times \text{value}$ (Baseline SI) | Active Potency, Loss on Drying |
| **`ppm`** or **`mg/kg`** | **`ppm`** | $1.0 \times \text{value}$ (1:1 direct equivalence) | Elemental Impurities (Pb, As, Cd, Hg) |
| **`CFU/g`** | **`CFU/g`** | $1.0 \times \text{value}$ (Baseline SI) | TAMC, TYMC |
| **`%`** | **`% (w/w)`** | $1.0 \times \text{value}$ (Baseline SI) | Moisture / LOD |

---

## 5. Bilingual Terminology & Analyte Normalization Matrix

| English Term (*Certificate*) | French Term (*Certificat d'analyse*) | Canonical Acumatica Parameter | Target Test ID |
| :--- | :--- | :--- | :--- |
| **Active Polyphenols Content** | Teneur en polyphénols totaux | `active_potency` | `ASSAY_POLYPHENOLS` |
| **Anthocyanins Content** | Teneur en anthocyanes | `active_potency` | `ASSAY_ANTHOCYANINS` |
| **Loss on Drying (Moisture)** | Perte au séchage (Humidité) | `loss_on_drying` | `PHYS_LOD` |
| **Lead (Pb)** | Plomb (Pb) | `heavy_metal_lead` | `HM_LEAD` |
| **Arsenic (As)** | Arsenic (As) | `heavy_metal_arsenic` | `HM_ARSENIC` |
| **Cadmium (Cd)** | Cadmium (Cd) | `heavy_metal_cadmium` | `HM_CADMIUM` |
| **Mercury (Hg)** | Mercure (Hg) | `heavy_metal_mercury` | `HM_MERCURY` |
| **Total Aerobic Microbial Count (TAMC)** | Dénombrement germes aérobies totaux (DGAT)| `microbial_tamc` | `MICRO_TAMC` |
| **Total Combined Yeast & Mold (TYMC)** | Dénombrement levures & moisissures (DLMT)| `microbial_tymc` | `MICRO_TYMC` |
| **Escherichia coli** | Escherichia coli (Absence dans 10g) | `pathogen_e_coli` | `PATH_ECOLI` |
| **Salmonella spp.** | Salmonella spp. (Absence dans 25g) | `pathogen_salmonella` | `PATH_SALM` |

---

## 6. Acumatica QMS Digital Integration & Schema

CoA results issued by Great Lakes Bio-Analytical are transmitted digitally via REST Webhook into Acumatica `QMSInspectionOrder`:

```json
{
  "lab_identifier": "LAB-GL-ANALYTICAL",
  "certificate_number": "COA-GL-2026-09182",
  "issue_date": "2026-03-01T15:30:00Z",
  "document_standard": "HEALTH_CANADA_CALA_ISO17025",
  "sample_details": {
    "acumatica_inventory_id": "RAW-ECH-EXT4",
    "lot_serial_nbr": "LOT-EC2603-01A",
    "client_po": "PO-049182",
    "vendor_id": "VEND-NORTH-BIO"
  },
  "analytical_results": [
    {
      "test_name": "Active Polyphenols Content",
      "canonical_parameter": "active_potency",
      "method": "HPLC-DAD (USP Monograph)",
      "specification": ">= 4.00 % (w/w)",
      "result_numeric": 4.28,
      "result_uom": "% (w/w)",
      "disposition": "PASS"
    },
    {
      "test_name": "Elemental Lead (Pb)",
      "canonical_parameter": "heavy_metal_lead",
      "method": "ICP-MS (USP <2232>)",
      "specification": "<= 0.50 ppm",
      "result_numeric": 0.084,
      "result_uom": "ppm",
      "disposition": "PASS"
    }
  ],
  "authorized_signatory": "Dr. Ronald Henderson, Ph.D., C.Chem."
}
```
