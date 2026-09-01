# Vendor Profile Specification: Nordic Marine Extracts AS
## Acumatica Cloud ERP Vendor Master: `VEND-NORDIC-MAR`

---

## 1. Corporate & Commercial Information

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            VENDOR AT A GLANCE                               │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Acumatica Vendor ID:     │ VEND-NORDIC-MAR                                  │
│ Legal Name:              │ Nordic Marine Extracts Aktieselskap              │
│ Operating Country:       │ Norway (Ålesund, Møre og Romsdal)                │
│ Vendor Class:            │ RAW_MARINE_LIPID                                 │
│ Currency / Payment Terms:│ USD / NET30                                      │
│ Health Canada Foreign Lic│ Foreign Site Annex FSA-NO-MR-672910              │
│ Quality Rating Tier:     │ Tier-1 Preferred (99.3% Historical Pass Rate)    │
│ Average Lead Time:       │ 15 Business Days (Temperature-Controlled Ocean)  │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 1.1 Facility & Contact Details
* **Headquarters / Marine Refinery:** Havnegata 18, 6003 Ålesund, Norway
* **Director of Marine QA & Compliance:** Astrid Lindholm, M.Sc. (`astrid.lindholm@nordicmarine.no` / +47-70-192800)
* **Supply Chain Desk:** `supply@nordicmarine.no`

---

## 2. Regulatory Licences & Certifications

* **Norwegian Food Safety Authority (Mattilsynet):** HACCP Approval #NO-HACCP-9481.
* **GOED Voluntary Monograph Compliance:** Compliant with Global Organization for EPA and DHA Omega-3 purity and oxidation standards.
* **Marine Stewardship Council (MSC):** Chain of Custody MSC-C-54819 for sustainable wild-catch pelagic fisheries.
* **DNV GL GMP & ISO 22000:** Audited bi-annually for North American import compliance.

---

## 3. Supplied Product Portfolio

Nordic Marine Extracts AS supplies purified marine omega-3 oils and algal astaxanthin:

| Product Code | Description | Item Class | Primary Inspection Plan | Default QC Bay |
| :--- | :--- | :--- | :--- | :--- |
| **`RAW-OMEGA3-70`** | Marine Omega-3 Triglyceride Oil (70% EPA/DHA min) | `RAW_MARINE_LIPID` | `QPLAN-LIP-OM370` | `QC-COLD-HOLD-02` |
| **`RAW-ASTA-10`** | Natural Astaxanthin Oleoresin 10% (*H. pluvialis*) | `RAW_MARINE_LIPID` | `QPLAN-LIP-ASTA10` | `QC-COLD-HOLD-02` |

---

## 4. Inbound Quality Governance & Testing Routing

1. **Analytical Testing Routing:**
   * Primary Laboratory: **Great Lakes Bio-Analytical Services Inc.** (`LAB-GL-ANALYTICAL`) for Fatty Acid GC-FID profile (EPA/DHA), Peroxide Value, p-Anisidine Value, and Heavy Metals (Pb, As, Cd, Hg, Total/Inorganic Arsenic).
   * Secondary Laboratory: **Pacific Rim BioNutra Testing Laboratories Ltd.** (`LAB-PACIFIC-TEST`) for HRGC-HRMS Dioxins / Furans / PCB testing and microbial stability.
2. **Lipid Oxidation Critical Control Limits:**
   * Peroxide Value (PV) $\le 5.0\text{ meq O}_2/\text{kg}$.
   * p-Anisidine Value (p-AV) $\le 20.0$.
   * Total Oxidation (TOTOX $= 2 \times \text{PV} + \text{p-AV}$) $\le 26.0$.
   * Any breach immediately flags lot as rancid / degraded, triggering locked quarantine and NCR generation.
