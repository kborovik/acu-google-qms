#!/usr/bin/env python3
"""
Synthetic Demo & Test Document Generator for Inbound Quality & Compliance Platform
Targeting the Canadian Market (Health Canada, CSA, WHMIS 2015, CFIA, AS9100D)
Integration target: Acumatica Cloud ERP

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
    ("Montreal", "QC", "H4S 1J2"),
    ("Calgary", "AB", "T2C 2N8"),
    ("Vancouver", "BC", "V6B 1A1"),
    ("Sault Ste. Marie", "ON", "P6A 5K7"),
    ("Edmonton", "AB", "T5J 2R7"),
    ("Winnipeg", "MB", "R3C 1A5"),
    ("Halifax", "NS", "B3J 1S9")
]

CANADIAN_LABS = [
    "Great Lakes Bio-Analytical Services Inc.",
    "Maple Leaf Quality Testing Laboratories Ltd.",
    "St. Lawrence Metallurgical & Chemical Testing Corp.",
    "Pacific Rim Material Sciences Labs Inc."
]

STEEL_MILLS = [
    "Algoma Canadian Steel Corp.",
    "Hamilton Primary Metal Fabricators Ltd.",
    "Stelco Heavy Plate Processing Corp.",
    "Quebec Special Alloys & Forgings Inc."
]

AEROSPACE_VENDORS = [
    "Apex Precision Aerospace Machining Inc.",
    "Laurentian Flight Dynamics Components Ltd.",
    "Vanguard Aerospace Defense Parts Corp.",
    "Ontario Precision Structures Inc."
]

CHEMICAL_VENDORS = [
    "Northern Industrial Chemicals Ltd.",
    "Canuck Industrial Solvents & Specialty Fluids Inc.",
    "BioShield Solutions Canada Corp.",
    "Great White North Chemical Specialties Ltd."
]

def random_city():
    return random.choice(CANADIAN_CITIES)

def generate_coa(doc_idx: int, force_failure: bool = False) -> dict:
    city, prov, postal = random_city()
    lab = random.choice(CANADIAN_LABS)
    lot_suffix = f"{random.randint(100, 999)}-{chr(random.randint(65, 90))}"
    lot_num = f"LOT-CA26{random.randint(10, 99)}-{lot_suffix}"
    po_num = f"PO-0{random.randint(10000, 99999)}"
    pr_num = f"PR-0{random.randint(10000, 99999)}"
    mfg_date = datetime.now() - timedelta(days=random.randint(10, 60))
    exp_date = mfg_date + timedelta(days=365 * 3)

    # If force_failure, push heavy metal or microbial over limit
    lead_val = round(random.uniform(0.65, 1.20), 3) if force_failure else round(random.uniform(0.01, 0.15), 3)
    lead_status = "FAIL" if lead_val > 0.50 else "PASS"

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
                "inventory_item_id": "RAW-ECH-EXT4",
                "lot_serial_number": lot_num,
                "vendor_id": "VEND-NORTH-BIO"
            }
        },
        "issuer_information": {
            "laboratory_name": lab,
            "accreditation_number": f"CALA-ISO17025-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 999)} King St W, {city}, {prov} {postal}, Canada",
            "contact": f"qa@{lab.lower().replace(' ', '')[:12]}.ca"
        },
        "product_information": {
            "product_name": "Organic Botanical Raw Extract 4% Standardized",
            "lot_number": lot_num,
            "batch_size_kg": round(random.uniform(500.0, 2500.0), 1),
            "manufacturing_date": mfg_date.strftime("%Y-%m-%d"),
            "expiry_date": exp_date.strftime("%Y-%m-%d"),
            "country_of_origin": "Canada"
        },
        "test_results": [
            {
                "parameter": "Active Potency Assay",
                "test_method": "HPLC-DAD (USP Monograph)",
                "specification_min": 4.0,
                "specification_max": None,
                "unit": "% (w/w)",
                "actual_result": round(random.uniform(4.1, 4.8), 2),
                "status": "PASS"
            },
            {
                "parameter": "Loss on Drying (Moisture)",
                "test_method": "USP <731>",
                "specification_min": None,
                "specification_max": 5.0,
                "unit": "%",
                "actual_result": round(random.uniform(2.5, 4.2), 2),
                "status": "PASS"
            },
            {
                "parameter": "Heavy Metals - Lead (Pb)",
                "test_method": "ICP-MS (USP <2232>)",
                "specification_min": None,
                "specification_max": 0.50,
                "unit": "ppm (mg/kg)",
                "actual_result": lead_val,
                "status": lead_status
            },
            {
                "parameter": "Heavy Metals - Arsenic (As)",
                "test_method": "ICP-MS (USP <2232>)",
                "specification_min": None,
                "specification_max": 1.00,
                "unit": "ppm (mg/kg)",
                "actual_result": round(random.uniform(0.05, 0.25), 3),
                "status": "PASS"
            },
            {
                "parameter": "Total Aerobic Microbial Count (TAMC)",
                "test_method": "USP <2021>",
                "specification_min": None,
                "specification_max": 10000,
                "unit": "CFU/g",
                "actual_result": random.randint(100, 850),
                "status": "PASS"
            }
        ],
        "authorization": {
            "signatory_name": "Dr. Jean-Marc Boucher, Ph.D.",
            "title": "Director of Quality Control & Analytical Validation",
            "approval_date": datetime.now().isoformat()
        },
        "acumatica_action_directive": {
            "auto_approve_lot": not force_failure,
            "lot_status": "Quarantine" if force_failure else "Released",
            "create_ncr_ticket": force_failure
        }
    }
    return doc

def generate_mtr(doc_idx: int, force_failure: bool = False) -> dict:
    city, prov, postal = random_city()
    mill = random.choice(STEEL_MILLS)
    heat_num = f"HEAT-H{random.randint(10000, 99999)}B"
    po_num = f"PO-0{random.randint(10000, 99999)}"
    pr_num = f"PR-0{random.randint(10000, 99999)}"

    # If force_failure, lower yield strength below CSA G40.21 350W min (350 MPa)
    yield_val = round(random.uniform(310.0, 335.0), 1) if force_failure else round(random.uniform(365.0, 420.0), 1)
    yield_status = "FAIL" if yield_val < 350.0 else "PASS"

    c_val = round(random.uniform(0.12, 0.18), 3)
    mn_val = round(random.uniform(1.10, 1.35), 3)
    ce_val = round(c_val + mn_val / 6.0 + 0.05 / 5.0 + 0.10 / 15.0, 3)

    doc = {
        "document_metadata": {
            "document_type": "Material Test Report (MTR) / Mill Test Certificate (MTC)",
            "certificate_number": f"MTR-2026-CA-{random.randint(100000, 999999)}",
            "issued_date": datetime.now().strftime("%Y-%m-%d"),
            "standards_compliance": [
                "CSA G40.20-13 / CSA G40.21-13 Grade 350W",
                "ASTM A572 / A572M Grade 50 (Dual Certified)",
                "ASME BPVC Section II Part A SA-572 Grade 50",
                "ISO 9001:2015 Registered Mill"
            ],
            "acumatica_erp_mapping": {
                "acumatica_po_number": po_num,
                "acumatica_receipt_number": pr_num,
                "inventory_item_id": "STEEL-PL-350W-0500",
                "lot_serial_number": heat_num,
                "vendor_id": "VEND-ALGOMA-MET"
            }
        },
        "mill_information": {
            "mill_name": mill,
            "facility_location": f"{city}, {prov}, Canada",
            "melt_and_manufacture_country": "Canada",
            "furnace_type": "Electric Arc Furnace (EAF) / Vacuum Degassed"
        },
        "material_identification": {
            "product_description": "Hot Rolled Structural Steel Plate",
            "grade": "CSA G40.21 350W / ASTM A572 Gr 50",
            "heat_number": heat_num,
            "slab_number": f"SLAB-{random.randint(10000, 99999)}",
            "total_weight_kg": round(random.uniform(15000.0, 45000.0), 1)
        },
        "ladle_chemical_analysis_percent": {
            "carbon": { "specified_max": 0.20, "actual": c_val, "status": "PASS" },
            "manganese": { "specified_min": 0.80, "specified_max": 1.50, "actual": mn_val, "status": "PASS" },
            "phosphorus": { "specified_max": 0.035, "actual": 0.011, "status": "PASS" },
            "sulfur": { "specified_max": 0.035, "actual": 0.005, "status": "PASS" },
            "silicon": { "specified_max": 0.40, "actual": 0.22, "status": "PASS" },
            "carbon_equivalent_ce": { "specified_max": 0.45, "actual": ce_val, "status": "PASS" }
        },
        "mechanical_test_results": [
            {
                "test_type": "Tensile Testing (ASTM A370 / CSA G40.20)",
                "yield_strength_mpa": { "specified_min": 350.0, "specified_max": 500.0, "actual": yield_val, "status": yield_status },
                "tensile_strength_mpa": { "specified_min": 450.0, "specified_max": 650.0, "actual": round(random.uniform(490.0, 560.0), 1), "status": "PASS" },
                "elongation_percentage": { "specified_min": 19.0, "actual": round(random.uniform(22.0, 28.0), 1), "status": "PASS" }
            },
            {
                "test_type": "Charpy V-Notch Impact Test (CSA G40.21 Type WT)",
                "test_temperature_celsius": -20.0,
                "average_joules": round(random.uniform(45.0, 68.0), 1),
                "specified_min_average_joules": 27.0,
                "status": "PASS"
            }
        ],
        "authorization": {
            "chief_metallurgist_name": "Marc-André Fortin, P.Eng.",
            "signature_status": "Certified Digital Mill Stamp & Signature"
        },
        "acumatica_action_directive": {
            "auto_approve_lot": not force_failure,
            "lot_status": "Quarantine" if force_failure else "Released",
            "create_ncr_ticket": force_failure
        }
    }
    return doc

def generate_coc(doc_idx: int) -> dict:
    city, prov, postal = random_city()
    vendor = random.choice(AEROSPACE_VENDORS)
    batch_num = f"BATCH-2026-{random.randint(1000, 9999)}"
    po_num = f"PO-0{random.randint(10000, 99999)}"
    pr_num = f"PR-0{random.randint(10000, 99999)}"

    doc = {
        "document_metadata": {
            "document_type": "Certificate of Conformance (CoC)",
            "certificate_id": f"COC-2026-AERO-{random.randint(1000, 9999)}",
            "issued_date": datetime.now().strftime("%Y-%m-%d"),
            "standards_compliance": [
                "AS9100D / ISO 9001:2015 Aerospace Quality System",
                "Canadian Controlled Goods Directorate (CGD)",
                "AS9102 Rev B FAIR Standards"
            ],
            "acumatica_erp_mapping": {
                "acumatica_po_number": po_num,
                "acumatica_receipt_number": pr_num,
                "inventory_item_id": "AERO-BRKT-HYD-7075",
                "lot_serial_number": batch_num,
                "vendor_id": "VEND-APEX-AERO"
            }
        },
        "supplier_information": {
            "company_name": vendor,
            "cage_code": f"L{random.randint(1000, 9999)}",
            "address": f"{random.randint(1000, 9999)} Blvd Aviation, {city}, {prov} {postal}, Canada"
        },
        "order_and_part_details": {
            "customer_po_number": po_num,
            "part_number": "AERO-BRKT-HYD-7075",
            "drawing_revision": "Rev D",
            "quantity_shipped": random.choice([50, 100, 150, 200, 500]),
            "batch_lot_number": batch_num
        },
        "compliance_declarations": {
            "conformance_statement": "All articles have been manufactured, inspected, and tested in accordance with drawings and purchase specifications.",
            "controlled_goods_compliant": True,
            "anti_counterfeit_plan_compliant": True
        },
        "authorization": {
            "signatory": "Jean-Pierre Lefebvre, CQE",
            "title": "Director of Aerospace Quality"
        },
        "acumatica_action_directive": {
            "auto_approve_lot": True,
            "lot_status": "Released"
        }
    }
    return doc

def generate_sds(doc_idx: int) -> dict:
    city, prov, postal = random_city()
    vendor = random.choice(CHEMICAL_VENDORS)

    doc = {
        "document_metadata": {
            "document_type": "Safety Data Sheet (SDS) / Fiche de Données de Sécurité (FDS)",
            "document_id": f"SDS-CA-2026-CHEM{random.randint(100, 999)}",
            "revision_date": datetime.now().strftime("%Y-%m-%d"),
            "standards_compliance": [
                "WHMIS 2015 (Hazardous Products Regulations - SOR/2015-17)",
                "Globally Harmonized System (GHS Rev 7)",
                "Canadian Environmental Protection Act (CEPA 1999 - DSL Compliant)"
            ],
            "acumatica_erp_mapping": {
                "inventory_item_id": "CHEM-IND-SOLV400",
                "vendor_id": "VEND-NORTH-CHEM",
                "hazard_flag": True,
                "un_number": "UN1993"
            }
        },
        "sections": {
            "section_1_identification": {
                "product_identifier": "EcoSolv Industrial Degreaser & Precision Cleaner",
                "supplier_name": vendor,
                "supplier_address": f"{random.randint(100, 999)} Industrial Way, {city}, {prov} {postal}, Canada",
                "emergency_telephone": "CANUTEC +1 (613) 996-6666"
            },
            "section_2_hazard_identification": {
                "ghs_classification": ["Flammable Liquids (Category 2)", "Skin Irritation (Category 2)"],
                "signal_word": "DANGER",
                "hazard_pictograms": ["GHS02 (Flame)", "GHS07 (Exclamation Mark)"]
            },
            "section_14_transport_information": {
                "un_number": "UN1993",
                "proper_shipping_name": "FLAMMABLE LIQUIDS, N.O.S. (Isopropanol, Heptane)",
                "tdg_class": "3",
                "packing_group": "II"
            }
        },
        "acumatica_action_directive": {
            "update_item_safety_profile": True,
            "sds_valid_until": (datetime.now() + timedelta(days=365*3)).strftime("%Y-%m-%d")
        }
    }
    return doc

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Canadian quality/compliance test documents for Acumatica ERP.")
    parser.add_argument("--count", type=int, default=3, help="Number of document sets to generate")
    parser.add_argument("--outdir", type=str, default="./generated_samples", help="Output directory")
    parser.add_argument("--include-failures", action="store_true", help="Include out-of-spec/fail documents to test Acumatica NCR triggers")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    print(f"Generating {args.count} document sets in: {args.outdir}")

    for i in range(1, args.count + 1):
        # CoA
        coa_fail = args.include_failures and (i % 2 == 0)
        coa = generate_coa(i, force_failure=coa_fail)
        coa_fname = f"coa_sample_{i}_{'fail' if coa_fail else 'pass'}.json"
        with open(os.path.join(args.outdir, coa_fname), "w", encoding="utf-8") as f:
            json.dump(coa, f, indent=2)

        # MTR
        mtr_fail = args.include_failures and (i % 3 == 0)
        mtr = generate_mtr(i, force_failure=mtr_fail)
        mtr_fname = f"mtr_sample_{i}_{'fail' if mtr_fail else 'pass'}.json"
        with open(os.path.join(args.outdir, mtr_fname), "w", encoding="utf-8") as f:
            json.dump(mtr, f, indent=2)

        # CoC
        coc = generate_coc(i)
        coc_fname = f"coc_sample_{i}.json"
        with open(os.path.join(args.outdir, coc_fname), "w", encoding="utf-8") as f:
            json.dump(coc, f, indent=2)

        # SDS
        sds = generate_sds(i)
        sds_fname = f"sds_sample_{i}.json"
        with open(os.path.join(args.outdir, sds_fname), "w", encoding="utf-8") as f:
            json.dump(sds, f, indent=2)

    print(f"Successfully generated {args.count * 4} synthetic documents.")

if __name__ == "__main__":
    main()
