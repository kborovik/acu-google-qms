# Mandatory Core Shipping Documents Specification
## Inbound Warehouse Dock Compliance, Document Hand-Off & Acumatica ERP Integration

---

## 1. Scope & Regulatory Framework

Under Canadian federal manufacturing regulations (**Health Canada Good Manufacturing Practices GUI-0001 / GUI-0158**, **Natural Health Products Regulations SOR/2003-196**, and **CFIA Safe Food for Canadians Regulations SFCR SOR/2018-108**), every inbound raw material, botanical extract, API, and active biological component received at the warehouse dock must be accompanied by a validated suite of shipping and quality assurance documents.

Raw materials **cannot be moved into production racking or released into blending Work Orders** without complete physical and digital verification of these documents against open purchase receipts in **Acumatica Cloud ERP**.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                          INBOUND SHIPMENT DOCK VERIFICATION & ERP BUS                                  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 1. PHYSICAL DOCK ARRIVAL                           ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Freight carrier truck arrives at receiving dock (e.g., CanNordic Mississauga facility).            │
 │ • Receiving clerk collects physical documentation packet from driver/carrier pouch.                 │
 │ • Clerk inspects trailer seals, pallet counts, container integrity, and temp loggers.                │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 2. 3-WAY DOCUMENT RECONCILIATION                   ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │  [BILL OF LADING (BOL)]       [SUPPLIER PACKING SLIP]         [CERTIFICATE OF ANALYSIS (CoA)]        │
 │  • Carrier & Trailer ID       • Acumatica PO Number (`PO-*`)  • Testing Laboratory & Accreditation   │
 │  • Tamper Seal Numbers        • Vendor Item & Inventory ID    • Lot/Batch Number (`LotSerialNbr`)    │
 │  • Gross Weight & Pallets     • Lot Number & Container Count  • Chemical Assays, Metals, Bioburden   │
 └──────────────────────────────────────────────────┬───────────────────────────────────────────────────┘
                                                    │
 3. ACUMATICA ERP RECEIPT CREATION                  ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Clerk posts `POReceipt` with line-item allocations (`POReceiptLineSplit`).                         │
 │ • System places lot into mandatory regulatory quarantine (`INLotSerialStatus.LotStatus = 'QC Hold'`). │
 │ • Yellow `QC HOLD` physical placards affixed to staged pallets in receiving bay.                     │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 4. AI INGESTION & DOCUMENT ATTACHMENT              ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ • Multimodal engine ingests CoA, Packing Slip, and BOL scans.                                        │
 │ • Validates analyte potency and contaminants against Acumatica `QMSInspectionPlan`.                  │
 │ • Archives high-resolution PDFs and normalized JSON payloads to ERP Lot record via `/files` API.     │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Mandatory Core Shipping Documents Matrix

Every inbound shipment arriving at the dock must include the three universal core documents detailed below:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               MANDATORY CORE SHIPPING DOCUMENT SUITE                                   │
├───────────────────────┬──────────────────────────┬─────────────────────────────┬───────────────────────┤
│ DOCUMENT TYPE         │ ISSUING AUTHORITY        │ PRIMARY PURPOSE             │ ERP TOUCHPOINT        │
├───────────────────────┼──────────────────────────┼─────────────────────────────┼───────────────────────┤
│ 1. Certificate of     │ ISO/IEC 17025 Accredited │ Verifies chemical potency,  │ `QMSInspectionOrder`  │
│    Analysis (CoA)     │ Laboratory / Supplier QA │ purity, heavy metals & CFUs │ `QMSInspectionPlan`   │
├───────────────────────┼──────────────────────────┼─────────────────────────────┼───────────────────────┤
│ 2. Supplier Packing   │ Supplier Shipping Desk / │ Verifies PO line items,     │ `POReceipt`           │
│    Slip / Delivery Doc│ Manufacturer Logistics   │ lot numbers & net weights   │ `POReceiptLineSplit`  │
├───────────────────────┼──────────────────────────┼─────────────────────────────┼───────────────────────┤
│ 3. Bill of Lading     │ Freight Carrier /        │ Confirms physical custody,  │ `POReceipt` (Header)  │
│    (BOL) / Manifest   │ Logistics Provider       │ freight seals & piece count │ `POReceipt.TrackingNbr│
└───────────────────────┴──────────────────────────┴─────────────────────────────┴───────────────────────┘
```

---

## 3. Detailed Specification for Core Documents

### 3.1 Document 1: Certificate of Analysis (CoA)
The Certificate of Analysis is the foundational regulatory artifact required under Health Canada GMP (GUI-0001) Section C.02.009.

* **Mandatory Data Elements:**
  1. **Header Metadata:**
     * Testing Laboratory Name, Facility Address, and ISO/IEC 17025 Accreditation Number (e.g., CALA #9481, DAkkS #D-PL-14192, SCC #8172, JNLA #JNLA-09418, NA #TEST-092).
     * Certificate Identification Number (e.g., `COA-GL-2026-09182`) and Issue Date.
     * Supplier / Manufacturer Name and Facility Location.
  2. **Product & Batch Identification:**
     * Product Commercial Name and Botanical/Chemical Scientific Name.
     * Manufacturer Lot/Batch Number (`LotSerialNbr`) matching physical drum labels.
     * Manufacturing Date (`MfgDate`) and Expiration/Retest Date (`ExpiryDate`).
     * Batch Quantity / Total Pack Size (kg).
     * Health Canada NPN / DMF Reference (if applicable).
  3. **Analytical Test Matrix (Minimum Required Tests):**
     * **Active Potency / Assay:** Quantitative marker assay via HPLC, GC-FID, or titration with target specification range.
     * **Heavy Metal Contaminants:** ICP-MS determination for Lead (Pb $\le 0.50$ ppm), Arsenic (As $\le 1.00$ ppm), Cadmium (Cd $\le 0.30$ ppm), and Mercury (Hg $\le 0.10$ ppm).
     * **Microbial Bioburden:** Total Aerobic Microbial Count (TAMC $\le 10^4$ CFU/g), Total Combined Yeast & Mold (TYMC $\le 10^3$ CFU/g), and absence tests for *E. coli* (in 10g) and *Salmonella spp.* (in 25g) per USP <2021>/<2022>.
     * **Physical-Chemical Tests:** Loss on Drying / Moisture (USP <731> $\le 5.0\%$), Residual Solvents (USP <467> / Ph. Eur. 2.4.24), and Specific Optical Rotation / Ash where applicable.
  4. **Authorization & Sign-off:**
     * Name, Professional Credentials, Title, and Electronic/Physical Signature of Authorized QA Officer or Lab Director.
     * Formal disposition statement (e.g., `PASS`, `CONFORMS TO SPECIFICATION`, `GODKJENT`, `適合`).

---

### 3.2 Document 2: Supplier Packing Slip / Delivery Note
The Packing Slip accompanies the physical freight and serves as the bridge between the vendor's fulfillment order and CanNordic's purchase order in Acumatica ERP.

* **Mandatory Data Elements:**
  1. **Commercial Header:**
     * Supplier Legal Name and Acumatica Vendor ID (`VendorID`, e.g., `VEND-NORTH-BIO`).
     * CanNordic Purchase Order Reference (`POOrderNbr`, e.g., `PO-049182`).
     * Vendor Sales Order / Delivery Note Number.
     * Shipping Date and Destination Warehouse ID (`WH-MISS-01`, `WH-MISS-COLD-01`).
  2. **Line-Item Lot Detail Table:**
     * CanNordic Inventory Item ID (`InventoryID`, e.g., `RAW-ECH-EXT4`).
     * Complete Product Description.
     * Supplier Lot / Serial Number (`LotSerialNbr`).
     * Number of Packages / Containers (e.g., `20 Fiber Drums @ 25.0 kg net`).
     * Net Weight and Gross Weight in KG.
     * Container Serial Numbers or Tamper-Evident Security Seal Identifiers.
  3. **Storage & Handling Directives:**
     * Prescribed Storage Temperature (e.g., `Controlled Room Temperature 15-25°C` or `Refrigerated 2-8°C`).
     * Light and moisture sensitivity precautions (e.g., `Protect from direct light; store in desiccated nitrogen-purged drums`).

---

### 3.3 Document 3: Bill of Lading (BOL) / Carrier Delivery Manifest
The Bill of Lading constitutes the legal contract between the freight carrier and CanNordic BioNutra Inc., proving chain-of-custody transfer.

* **Mandatory Data Elements:**
  1. **Carrier Identification:**
     * Freight Carrier Name, SCAC Code, and Master Tracking / PRO Number.
     * Trailer / Container Number and Tractor Unit ID.
  2. **Security & Seal Verification:**
     * High-Security Bolt Seal Number(s) applied at supplier origin.
     * Receiving clerk seal intactness verification checkbox and physical signature.
  3. **Freight Summary:**
     * Total Pallet / Skid Count and Handling Unit Description (e.g., `4 Wooden Pallets / 80 Fiber Drums`).
     * Declared Total Gross Weight (kg / lbs).
     * Freight Class and NMFC Code.
     * Special Carrier Instructions (e.g., `Reefer Unit Set to +4°C continuous`).
  4. **Receipt Confirmation:**
     * Receiving Dock Clerk Signature, Date, and Time of Dock Arrival.
     * Driver Printed Name, Signature, and Delivery Timestamp.

---

## 4. Class-Specific Mandatory Companion Documents

Depending on the material classification and international origin, inbound shipments must also include the following secondary compliance certificates:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              CLASS-SPECIFIC COMPANION DOCUMENTS MATRIX                                 │
├───────────────────────────┬─────────────────────────────────────┬──────────────────────────────────────┤
│ MATERIAL CATEGORY         │ REQUIRED COMPANION DOCUMENT         │ REGULATORY / QUALITY PURPOSE         │
├───────────────────────────┼─────────────────────────────────────┼──────────────────────────────────────┤
│ 1. Cold-Chain Sensitive   │ Cold-Chain Temperature Logger       │ Continuous temperature logging data  │
│    (Probiotics & Lipids)  │ Report (TempTale / USB Data PDF)    │ (Must not breach 8°C for > 4 hours)  │
├───────────────────────────┼─────────────────────────────────────┼──────────────────────────────────────┤
│ 2. Certified Organic      │ Organic Transaction Certificate &   │ Validates COR / USDA NOP / EU        │
│    Botanical Extracts     │ Scope Certificate (Pro-Cert/Kiwa)   │ organic equivalency and chain-of-cust│
├───────────────────────────┼─────────────────────────────────────┼──────────────────────────────────────┤
│ 3. International Imported │ Health Canada Foreign Site Annex    │ Verifies supplier site compliance    │
│    APIs & Extracts        │ Attestation (FSA-EU/JP/NO Annex)    │ under Health Canada GMP MRA treaties │
├───────────────────────────┼─────────────────────────────────────┼──────────────────────────────────────┤
│ 4. Chemical Raw Materials │ Safety Data Sheet (SDS)             │ WHMIS 2015 / GHS hazard control, PPE │
│    and Solvents           │ (16-Section GHS Format)             │ and safe warehouse staging directives│
├───────────────────────────┼─────────────────────────────────────┼──────────────────────────────────────┤
│ 5. Dietary Ingredients    │ Technical Safety Declarations       │ Attests absence of allergens, GMOs,  │
│    & Fermentation Inputs  │ (Allergen, BSE/TSE, Non-GMO, Solv)  │ and Class 1/2 solvent residues       │
└───────────────────────────┴─────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 5. Dock Receiving Verification & Reconciliation Protocol

Receiving dock clerks must execute the standard 5-step receiving protocol before raw materials are unloaded:

```
[Carrier Truck Docks at Receiving Bay]
                 │
                 ▼
[Step 1: Physical Trailer & Seal Audit]
  • Verify trailer security seal matches BOL seal number.
  • Inspect trailer hygiene, odor, pest evidence, and temperature.
                 │
                 ▼
[Step 2: Documentation Packet Extraction]
  • Extract BOL, Packing Slip, CoA, TempTale logger, and Organic certs.
                 │
                 ▼
[Step 3: 3-Way Cross-Reconciliation Check]
  ┌──────────────────────────────────────────────────────────────────┐
  │ Match 1: Packing Slip PO# == Open Acumatica Purchase Order       │
  │ Match 2: Physical Drum Lot Tags == Packing Slip Lot# == CoA Lot# │
  │ Match 3: Physical Drum Count == Packing Slip Qty == BOL Pieces   │
  └──────────────────────────────────────────────────────────────────┘
                 │
          ┌──────┴────────────────────────┐
          │ ALL MATCH                     │ DISCREPANCY / MISSING DOC
          ▼                               ▼
[Step 4A: Accept & Quarantine]     [Step 4B: Rejection / Delivery Hold]
  • Unload pallets to dock bay.      • Reject delivery or hold in dock quarantine.
  • Generate Acumatica `POReceipt`.  • Generate immediate Dock Incident NCR.
  • Set Status: "QC Hold".           • Refuse trailer sign-off pending QA review.
  • Affix Yellow QC Hold Placards.
                 │
                 ▼
[Step 5: Digital Ingestion Engine Hand-off]
  • Scan physical documents or trigger webhook ingestion.
  • AI Ingestion Engine extracts analytical values into `QMSInspectionOrder`.
  • Specification Engine checks tolerances -> Automatic Release or NCR.
```

---

## 6. Acumatica ERP Digital Integration Schema

When receiving documentation is captured, the system maps header and lot metadata into Acumatica `POReceipt` and document attachment endpoints:

### 6.1 Inbound Document Manifest JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "InboundShipmentDocumentManifest",
  "type": "object",
  "required": [
    "manifest_id",
    "receipt_number",
    "vendor_id",
    "purchase_order_number",
    "carrier_details",
    "shipping_documents",
    "line_items"
  ],
  "properties": {
    "manifest_id": { "type": "string" },
    "receipt_number": { "type": "string" },
    "vendor_id": { "type": "string" },
    "purchase_order_number": { "type": "string" },
    "carrier_details": {
      "type": "object",
      "properties": {
        "carrier_name": { "type": "string" },
        "tracking_pro_number": { "type": "string" },
        "trailer_number": { "type": "string" },
        "seal_number": { "type": "string" },
        "seal_intact": { "type": "boolean" }
      }
    },
    "shipping_documents": {
      "type": "object",
      "required": ["certificate_of_analysis", "packing_slip", "bill_of_lading"],
      "properties": {
        "certificate_of_analysis": {
          "type": "object",
          "properties": {
            "document_id": { "type": "string" },
            "testing_lab_id": { "type": "string" },
            "document_standard": { "type": "string" },
            "accreditation_number": { "type": "string" },
            "verified_in_packet": { "type": "boolean" }
          }
        },
        "packing_slip": {
          "type": "object",
          "properties": {
            "packing_slip_number": { "type": "string" },
            "verified_in_packet": { "type": "boolean" }
          }
        },
        "bill_of_lading": {
          "type": "object",
          "properties": {
            "bol_number": { "type": "string" },
            "piece_count": { "type": "integer" },
            "gross_weight_kg": { "type": "number" },
            "verified_in_packet": { "type": "boolean" }
          }
        },
        "cold_chain_logger": {
          "type": "object",
          "properties": {
            "logger_serial_number": { "type": "string" },
            "min_transit_temp_c": { "type": "number" },
            "max_transit_temp_c": { "type": "number" },
            "excursion_detected": { "type": "boolean" }
          }
        },
        "organic_certificate": {
          "type": "object",
          "properties": {
            "certifier_name": { "type": "string" },
            "certificate_number": { "type": "string" },
            "cor_compliant": { "type": "boolean" }
          }
        }
      }
    },
    "line_items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["inventory_id", "lot_serial_number", "received_qty_kg", "container_count"],
        "properties": {
          "inventory_id": { "type": "string" },
          "lot_serial_number": { "type": "string" },
          "received_qty_kg": { "type": "number" },
          "container_count": { "type": "integer" },
          "expiration_date": { "type": "string", "format": "date" },
          "default_quarantine_location": { "type": "string" }
        }
      }
    }
  }
}
```

---

## 7. Operational Discrepancy & Non-Conformance Rules

| Condition / Discrepancy | Operational Risk Level | Immediate Dock Action | Acumatica ERP Action |
| :--- | :--- | :--- | :--- |
| **Missing Certificate of Analysis (CoA)** | **Critical** | Hard stop on unloading. Pallet staged in Dock Hold Bay. | Lot created in `QC Hold`; cannot be released without CoA. |
| **Lot # Mismatch (Physical Drum $\ne$ CoA $\ne$ Packing Slip)** | **Critical** | Physical quarantine segregation. Delivery sign-off withheld. | Immediate `QMSNonConformance` (NCR) ticket generated. |
| **Tamper Seal Broken / Mismatched on BOL** | **High** | Full container inspection; QA Director alerted immediately. | `QMSNonConformance` (NCR) opened for security breach. |
| **Cold-Chain Excursion ($> 8.0^\circ\text{C}$ for $> 4\text{ hours}$)** | **Critical** | Material moved directly to locked `QC-COLD-HOLD-01`. | Lot locked in `Quarantine`; NCR flagged for vendor RTV. |
| **Missing Organic Transaction Certificate** | **Major** | Material received but downgraded from Organic inventory. | QA Hold on Organic product allocation until cert received. |
| **Damaged Packaging / Torn Fiber Drums** | **Major** | Damaged containers photographed and segregated. | Line split quantity reduced; damaged units marked `Rejected`. |
