# Vendor Profile Specification: Pacific Organic Ingredients Ltd.
## Acumatica Cloud ERP Vendor Master: `VEND-PACIFIC-ORG`

---

## 1. Corporate & Commercial Information

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            VENDOR AT A GLANCE                               │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Acumatica Vendor ID:     │ VEND-PACIFIC-ORG                                 │
│ Legal Name:              │ Pacific Organic Ingredients Limited              │
│ Operating Country:       │ Canada (Burnaby, British Columbia)               │
│ Vendor Class:            │ RAW_NUTRACEUTICAL                                │
│ Currency / Payment Terms:│ USD / NET30                                      │
│ Health Canada Site Lic:  │ #304882 / Foreign Site Annex FSA-CA-BC-119284    │
│ Quality Rating Tier:     │ Tier-1 Preferred (99.1% Historical Pass Rate)    │
│ Average Lead Time:       │ 7 Business Days                                  │
│ Designated Testing Lab:  │ Pacific Rim BioNutra Labs (LAB-PACIFIC-TEST)     │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Facility & Contact Details
* **Headquarters / Cold Storage:** 7800 Riverfront Way, Suite 100, Burnaby, BC V5J 5L3, Canada
* **Director of QC & Microbiology:** Sarah Chen, M.Sc. (`qc@pacificorganic.ca` / +1-604-555-0831)
* **Order Desk:** `sales@pacificorganic.ca`

---

## 2. Regulatory Licences & Certifications

* **Health Canada Site Licence:** #304882 (Manufacturing, Packaging, Labelling, Importing NHPs).
* **FDA Dietary Supplement cGMP:** Audited under 21 CFR Part 111 by SGS North America.
* **Organic Certification:** Quality Assurance International (QAI - COR / USDA NOP).
* **Cold-Chain Transport Certification:** Validated refrigerated logistics monitoring with continuous temperature loggers.

---

## 3. Supplied Product Portfolio

Pacific Organic Ingredients Ltd. supplies specialized botanical extracts and probiotic actives:

| Product Code | Description | Item Class | Primary Inspection Plan | Default QC Bay |
| :--- | :--- | :--- | :--- | :--- |
| **`RAW-CURC-95`** | Turmeric Curcuminoid Extract 95% Pure Standardized | `RAW_BOTANICAL` | `QPLAN-BOT-CURC95` | `QC-HOLD-BAY-A` |
| **`RAW-GUT-PRB100`**| Multi-Strain Probiotic Blend 100 Billion CFU/g Freeze-Dried | `RAW_BIOLOGICAL` | `QPLAN-BIO-PRB100` | `QC-COLD-HOLD-01` |

---

## 4. Inbound Quality Governance & Cold-Chain Testing Routing

1. **Analytical Testing Routing:**
   * Primary Laboratory: **Pacific Rim BioNutra Testing Laboratories Ltd.** (`LAB-PACIFIC-TEST` / SCC #8172) for viable plate enumeration (ISO 7889/20128), Curcuminoid HPLC assay, and USP <467> residual ethanol solvent testing.
   * Secondary Laboratory: **Great Lakes Bio-Analytical Services Inc.** (`LAB-GL-ANALYTICAL`) for secondary ICP-MS elemental impurity checks.
2. **Document Standard & Normalization:**
   * Inbound Document: SCC & AOAC PTM / USP Standard Certificate (Bilingual English/French).
   * Unit Normalization: $\text{Billion CFU/g} \rightarrow \text{Billion CFU/g (or } \times 10^9\text{ CFU/g)}$, $a_w \text{ (water activity)}$, $\text{ppm (ethanol)}$.
   * Synonym Normalization: *Viable Probiotic Cell Count*, *Total Curcuminoids Purity*, *Water Activity (Aw)*, *Residual Solvents (Ethanol)*.
3. **Cold-Chain Receiving Gate (`RAW-GUT-PRB100`):**
   * Receiving dock inspects TempTale logger upon truck arrival.
   * If transit temperature exceeded $8.0^\circ\text{C}$ for $> 4\text{ hours}$, lot is automatically locked in Quarantine with cold-chain breach NCR.
