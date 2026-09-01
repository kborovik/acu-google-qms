#!/usr/bin/env python3
"""
Synthetic Demo & Test Document Generator for CanNordic BioNutra Inc.
Certificate of Analysis (CoA) Ingestion Platform for Acumatica Cloud ERP.
Targeting Health Canada GMP (GUI-0001), NHPR (SOR/2003-196), and CFIA SFCR compliance.

Usage:
    python3 generate_demo_documents.py [--count 5] [--outdir ./generated_samples] [--include-failures]
"""

import os
import sys
import json
import random
import argparse
from datetime import datetime, timedelta

CANADIAN_CITIES = [
    ("Toronto", "ON", "M5G 1V2"),
    ("Mississauga", "ON", "L5N 6S2"),
    ("Montreal", "QC", "H4S 1J2"),
    ("Vancouver", "BC", "V6B 1A1"),
    ("Calgary", "AB", "T2C 2N8"),
    ("Saint-Laurent", "QC", "H4S 2A1")
]

CANADIAN_LABS = [
    "Great Lakes Bio-Analytical Services Inc.",
    "Maple Leaf Quality Testing Laboratories Ltd.",
    "Pacific Rim BioNutra Labs Inc.",
    "CanNordic Analytical Quality Services Ltd."
]

INGREDIENT_CATALOG = [
    {
        "item_id": "RAW-ECH-EXT4",
        "product_name": "Organic Echinacea Purpurea Extract 4% Standardized",
        "botanical_source": "Echinacea purpurea (L.) Moench (Aerial)",
        "npn": "NPN-80029384",
        "assay_param": "Active Polyphenols Content",
        "assay_min": 4.0,
        "assay_max": None,
        "assay_unit": "% (w/w)",
        "assay_method": "HPLC-DAD (USP Monograph)"
    },
    {
        "item_id": "RAW-ASH-EXT5",
        "product_name": "Organic Ashwagandha Root Extract 5% Withanolides",
        "botanical_source": "Withania somnifera (L.) Dunal (Root)",
        "npn": "NPN-80041289",
        "assay_param": "Total Withanolides Assay",
        "assay_min": 5.0,
        "assay_max": None,
        "assay_unit": "% (w/w)",
        "assay_method": "HPLC-UV (USP Monograph)"
    },
    {
        "item_id": "RAW-CURC-95",
        "product_name": "Turmeric Curcuminoid Extract 95%",
        "botanical_source": "Curcuma longa L. (Rhizome)",
        "npn": "NPN-80053912",
        "assay_param": "Total Curcuminoids Purity",
        "assay_min": 95.0,
        "assay_max": None,
        "assay_unit": "% (w/w)",
        "assay_method": "HPLC-DAD (USP <2021>)"
    },
    {
        "item_id": "RAW-VIT-C-ASC",
        "product_name": "Ascorbic Acid USP Grade Powder (Vitamin C)",
        "botanical_source": "Synthetic / Fermentation-Derived",
        "npn": "NPN-80012845",
        "assay_param": "Ascorbic Acid Potency",
        "assay_min": 99.0,
        "assay_max": 100.5,
        "assay_unit": "% (w/w)",
        "assay_method": "Titration (USP Monograph)"
    }
]

VENDORS = [
    {"vendor_id": "VEND-NORTH-BIO", "vendor_name": "Northern BioNutra Imports Corp."},
    {"vendor_id": "VEND-ALPINE-EXT", "vendor_name": "Alpine Botanical Extracts GmbH"},
    {"vendor_id": "VEND-PACIFIC-ORG", "vendor_name": "Pacific Organic Ingredients Ltd."},
    {"vendor_id": "VEND-NIPPON-PHARMA", "vendor_name": "Nippon Pure Bioactives Inc."}
]

def random_city():
    return random.choice(CANADIAN_CITIES)

def generate_coa(doc_idx: int, force_failure: bool = False) -> dict:
    city, prov, postal = random_city()
    lab = random.choice(CANADIAN_LABS)
    ingredient = INGREDIENT_CATALOG[doc_idx % len(INGREDIENT_CATALOG)]
    vendor = VENDORS[doc_idx % len(VENDORS)]

    lot_suffix = f"{random.randint(100, 999)}-{chr(random.randint(65, 90))}"
    lot_num = f"LOT-EC26{random.randint(10, 99)}-{lot_suffix}"
    po_num = f"PO-0{random.randint(10000, 99999)}"
    pr_num = f"PR-0{random.randint(10000, 99999)}"
    mfg_date = datetime.now() - timedelta(days=random.randint(10, 60))
    exp_date = mfg_date + timedelta(days=365 * 3)

    # Lead failure simulation if force_failure is True
    if force_failure:
        lead_val = round(random.uniform(0.65, 1.20), 3)
        lead_status = "FAIL"
        overall_status = "REJECTED"
        lot_status = "Quarantine"
        create_ncr = True
        auto_approve = False
    else:
        lead_val = round(random.uniform(0.01, 0.15), 3)
        lead_status = "PASS"
        overall_status = "APPROVED"
        lot_status = "Released"
        create_ncr = False
        auto_approve = True

    # Assay actual calculation
    if ingredient["assay_min"] is not None:
        assay_actual = round(ingredient["assay_min"] + random.uniform(0.1, 1.2), 2)
    else:
        assay_actual = 99.5

    doc = {
        "document_metadata": {
            "document_type": "Certificate of Analysis (CoA)",
            "document_id": f"COA-2026-HC-{random.randint(10000, 99999)}",
            "issued_date": datetime.now().strftime("%Y-%m-%d"),
            "standards_compliance": [
                "Health Canada Good Manufacturing Practices (GUI-0001)",
                "Natural Health Products Regulations (SOR/2003-196)",
                "USP <2021> / <2022>",
                "ISO/IEC 17025:2017 Accredited Laboratory"
            ],
            "acumatica_erp_mapping": {
                "acumatica_po_number": po_num,
                "acumatica_receipt_number": pr_num,
                "inventory_item_id": ingredient["item_id"],
                "lot_serial_number": lot_num,
                "vendor_id": vendor["vendor_id"]
            }
        },
        "issuer_information": {
            "laboratory_name": lab,
            "accreditation_number": f"CALA-ISO17025-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 999)} Meadowpine Blvd, {city}, {prov} {postal}, Canada",
            "contact": f"qa@{lab.lower().replace(' ', '')[:12]}.ca"
        },
        "product_information": {
            "product_name": ingredient["product_name"],
            "botanical_source": ingredient["botanical_source"],
            "lot_number": lot_num,
            "batch_size_kg": round(random.uniform(500.0, 2500.0), 1),
            "manufacturing_date": mfg_date.strftime("%Y-%m-%d"),
            "expiry_date": exp_date.strftime("%Y-%m-%d"),
            "country_of_origin": "Canada",
            "health_canada_npn": ingredient["npn"]
        },
        "test_results": [
            {
                "test_category": "Physical & Chemical Assay",
                "parameter": ingredient["assay_param"],
                "test_method": ingredient["assay_method"],
                "specification_min": ingredient["assay_min"],
                "specification_max": ingredient["assay_max"],
                "unit": ingredient["assay_unit"],
                "actual_result": assay_actual,
                "status": "PASS"
            },
            {
                "test_category": "Physical & Chemical Assay",
                "parameter": "Loss on Drying (Moisture)",
                "test_method": "USP <731> (105°C, 3h)",
                "specification_min": None,
                "specification_max": 5.0,
                "unit": "%",
                "actual_result": round(random.uniform(2.5, 4.2), 2),
                "status": "PASS"
            },
            {
                "test_category": "Physical & Chemical Assay",
                "parameter": "Heavy Metals - Lead (Pb)",
                "test_method": "ICP-MS (USP <2232>)",
                "specification_min": None,
                "specification_max": 0.50,
                "unit": "ppm (mg/kg)",
                "actual_result": lead_val,
                "status": lead_status
            },
            {
                "test_category": "Physical & Chemical Assay",
                "parameter": "Heavy Metals - Arsenic (As)",
                "test_method": "ICP-MS (USP <2232>)",
                "specification_min": None,
                "specification_max": 1.00,
                "unit": "ppm (mg/kg)",
                "actual_result": round(random.uniform(0.05, 0.25), 3),
                "status": "PASS"
            },
            {
                "test_category": "Physical & Chemical Assay",
                "parameter": "Heavy Metals - Cadmium (Cd)",
                "test_method": "ICP-MS (USP <2232>)",
                "specification_min": None,
                "specification_max": 0.30,
                "unit": "ppm (mg/kg)",
                "actual_result": round(random.uniform(0.01, 0.05), 3),
                "status": "PASS"
            },
            {
                "test_category": "Physical & Chemical Assay",
                "parameter": "Heavy Metals - Mercury (Hg)",
                "test_method": "ICP-MS (USP <2232>)",
                "specification_min": None,
                "specification_max": 0.10,
                "unit": "ppm (mg/kg)",
                "actual_result": round(random.uniform(0.005, 0.02), 3),
                "status": "PASS"
            },
            {
                "test_category": "Microbiological Assay",
                "parameter": "Total Aerobic Microbial Count (TAMC)",
                "test_method": "USP <2021>",
                "specification_min": None,
                "specification_max": 10000,
                "unit": "CFU/g",
                "actual_result": random.randint(100, 850),
                "status": "PASS"
            },
            {
                "test_category": "Microbiological Assay",
                "parameter": "Total Combined Yeast & Mold (TYMC)",
                "test_method": "USP <2021>",
                "specification_min": None,
                "specification_max": 1000,
                "unit": "CFU/g",
                "actual_result": random.randint(20, 150),
                "status": "PASS"
            },
            {
                "test_category": "Microbiological Assay",
                "parameter": "Escherichia coli",
                "test_method": "USP <2022>",
                "specification_min": None,
                "specification_max": None,
                "unit": "in 10g",
                "actual_result": "Absent",
                "status": "PASS"
            },
            {
                "test_category": "Microbiological Assay",
                "parameter": "Salmonella spp.",
                "test_method": "USP <2022>",
                "specification_min": None,
                "specification_max": None,
                "unit": "in 25g",
                "actual_result": "Absent",
                "status": "PASS"
            }
        ],
        "authorization": {
            "signatory_name": "Dr. Élodie Tremblay, Ph.D., C.Chem.",
            "title": "Director of Quality Assurance & Analytical Validation",
            "approval_date": datetime.now().isoformat()
        },
        "evaluation_summary": {
            "overall_status": overall_status,
            "discrepancy_count": 1 if force_failure else 0,
            "reasons": [f"Heavy Metal Lead (Pb) measured {lead_val} ppm exceeds limit 0.50 ppm."] if force_failure else []
        },
        "acumatica_action_directive": {
            "auto_approve_lot": auto_approve,
            "lot_status": lot_status,
            "create_ncr_ticket": create_ncr
        }
    }
    return doc

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Canadian CoA quality/compliance test documents for Acumatica ERP.")
    parser.add_argument("--count", type=int, default=3, help="Number of CoA documents to generate")
    parser.add_argument("--outdir", type=str, default="./generated_samples", help="Output directory")
    parser.add_argument("--include-failures", action="store_true", help="Include out-of-spec/fail documents to test Acumatica NCR triggers")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    print(f"Generating {args.count} CoA document sets in: {args.outdir}")

    for i in range(1, args.count + 1):
        coa_fail = args.include_failures and (i % 2 == 0)
        coa = generate_coa(i, force_failure=coa_fail)
        coa_fname = f"coa_sample_{i}_{'fail' if coa_fail else 'pass'}.json"
        with open(os.path.join(args.outdir, coa_fname), "w", encoding="utf-8") as f:
            json.dump(coa, f, indent=2)

    print(f"Successfully generated {args.count} synthetic CoA documents.")

if __name__ == "__main__":
    main()
