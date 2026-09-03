#!/usr/bin/env python3
"""
Synthetic Demo & Test Document Generator for CanNordic BioNutra Inc.
Multi-Vendor, Multi-Lab Certificate of Analysis (CoA) Ingestion Platform for Acumatica Cloud ERP.
Targeting 5 Qualified Global Suppliers mapped 1-to-1 to 5 ISO/IEC 17025 Accredited Laboratories
with heterogeneous Document Standards, distinct Units of Measure (SI Normalized), and Multilingual Synonyms.

Usage:
    python3 generate_demo_documents.py [--count 5] [--outdir ./generated_samples] [--include-failures]
"""

import os
import sys
import json
import random
import argparse
from datetime import datetime, timedelta

# 5 Qualified Testing Laboratories matching 5 Qualified Suppliers
LABORATORIES = {
    "LAB-GL-ANALYTICAL": {
        "lab_id": "LAB-GL-ANALYTICAL",
        "legal_name": "Great Lakes Bio-Analytical Services Inc.",
        "short_name": "Great Lakes Analytical",
        "accreditation": "ISO/IEC 17025:2017 (CALA Scope #9481) / DEL #104928",
        "document_standard": "HEALTH_CANADA_CALA_ISO17025",
        "city": "Mississauga",
        "state_prov": "ON",
        "postal_code": "L5N 2W7",
        "country": "CA",
        "primary_language": "en-CA",
        "secondary_language": "fr-CA",
        "signatory": "Dr. Ronald Henderson, Ph.D., C.Chem.",
        "signatory_title": "Laboratory Director & Chief Chemist"
    },
    "LAB-EURO-PHYTO": {
        "lab_id": "LAB-EURO-PHYTO",
        "legal_name": "Euro-Phyto Analytics GmbH",
        "short_name": "Euro-Phyto Analytics",
        "accreditation": "DIN EN ISO/IEC 17025:2018 (DAkkS #D-PL-14192-01) / EU GMP #DE_BY_01_GMP_2025_0112",
        "document_standard": "DIN_EN_ISO17025_PHEUR",
        "city": "München",
        "state_prov": "Bavaria",
        "postal_code": "80807",
        "country": "DE",
        "primary_language": "de-DE",
        "secondary_language": "en-GB",
        "signatory": "Dr. Manfred Weiss, Dr. rer. nat., Dipl.-Chem.",
        "signatory_title": "Laborleiter & Leitender Chemiker"
    },
    "LAB-PACIFIC-TEST": {
        "lab_id": "LAB-PACIFIC-TEST",
        "legal_name": "Pacific Rim BioNutra Testing Laboratories Ltd.",
        "short_name": "Pacific Rim Labs",
        "accreditation": "ISO/IEC 17025:2017 (SCC Scope #8172) / AOAC-RI PTM #092101 / DEL #203819",
        "document_standard": "SCC_AOAC_PTM_USP",
        "city": "Burnaby",
        "state_prov": "BC",
        "postal_code": "V5C 6A7",
        "country": "CA",
        "primary_language": "en-CA",
        "secondary_language": "fr-CA",
        "signatory": "Dr. Fiona MacIntyre, Ph.D., RMCCM",
        "signatory_title": "Laboratory Director & Chief Microbiologist"
    },
    "LAB-TOKYO-BIO": {
        "lab_id": "LAB-TOKYO-BIO",
        "legal_name": "Tokyo Bio-Analytical Testing Laboratories Inc.",
        "short_name": "Tokyo Bio-Analytical Labs",
        "accreditation": "JIS Q 17025:2018 / ISO 17025 (JNLA #JNLA-09418) / PMDA #JP-PMDA-LAB-2024-819",
        "document_standard": "JP18_JIS_SHIKEN_SEISEKISHO",
        "city": "Tokyo (Chuo-ku)",
        "state_prov": "Tokyo",
        "postal_code": "103-0022",
        "country": "JP",
        "primary_language": "ja-JP",
        "secondary_language": "en-US",
        "signatory": "Dr. Hiroshi Nakamura, Ph.D., P.Chem.",
        "signatory_title": "試験責任者 (Laboratory Director & Chief Analyst)"
    },
    "LAB-FJORD-ANALYTICAL": {
        "lab_id": "LAB-FJORD-ANALYTICAL",
        "legal_name": "Fjord Marine Bio-Testing Laboratories AS",
        "short_name": "Fjord Marine Labs",
        "accreditation": "NS-EN ISO/IEC 17025:2018 (Norsk Akkreditering #TEST-092) / Mattilsynet #NO-LAB-HACCP-9481",
        "document_standard": "GOED_PHEUR_ANALYSESERTIFIKAT",
        "city": "Ålesund",
        "state_prov": "Møre og Romsdal",
        "postal_code": "6003",
        "country": "NO",
        "primary_language": "no-NO",
        "secondary_language": "en-GB",
        "signatory": "Dr. Solveig Haugen, Ph.D., C.Chem.",
        "signatory_title": "Laboratorieleder & Sjefskjemiker"
    }
}

# 5 Qualified Suppliers
VENDORS = [
    {
        "vendor_id": "VEND-NORTH-BIO",
        "vendor_name": "Northern BioNutra Imports Corp.",
        "country": "CA",
        "assigned_lab_id": "LAB-GL-ANALYTICAL",
        "products": ["RAW-ECH-EXT4", "RAW-ELD-EXT10"]
    },
    {
        "vendor_id": "VEND-ALPINE-EXT",
        "vendor_name": "Alpine Botanical Extracts GmbH",
        "country": "DE",
        "assigned_lab_id": "LAB-EURO-PHYTO",
        "products": ["RAW-ASH-EXT5", "RAW-RHOD-EXT3"]
    },
    {
        "vendor_id": "VEND-PACIFIC-ORG",
        "vendor_name": "Pacific Organic Ingredients Ltd.",
        "country": "CA",
        "assigned_lab_id": "LAB-PACIFIC-TEST",
        "products": ["RAW-CURC-95", "RAW-GUT-PRB100"]
    },
    {
        "vendor_id": "VEND-NIPPON-PHARMA",
        "vendor_name": "Nippon Pure Bioactives Inc.",
        "country": "JP",
        "assigned_lab_id": "LAB-TOKYO-BIO",
        "products": ["RAW-COQ10-99", "RAW-THEA-98"]
    },
    {
        "vendor_id": "VEND-NORDIC-MAR",
        "vendor_name": "Nordic Marine Extracts AS",
        "country": "NO",
        "assigned_lab_id": "LAB-FJORD-ANALYTICAL",
        "products": ["RAW-OMEGA3-70", "RAW-ASTA-10"]
    }
]

# Product Definitions with regional parameter terms and UoM representations
PRODUCT_CATALOG = {
    "RAW-ECH-EXT4": {
        "item_id": "RAW-ECH-EXT4",
        "product_name": "Organic Echinacea Purpurea Extract 4% Polyphenols",
        "botanical_source": "Echinacea purpurea (L.) Moench (Aerial)",
        "npn": "NPN-80029384",
        "vendor_id": "VEND-NORTH-BIO",
        "lab_id": "LAB-GL-ANALYTICAL",
        "tests": [
            {
                "raw_param": "Active Polyphenols Content (Teneur en polyphénols)",
                "canonical_param": "active_potency",
                "method": "HPLC-DAD (USP Monograph)",
                "spec_min": 4.0, "spec_max": None,
                "raw_uom": "% (w/w)", "si_uom": "% (w/w)",
                "conv_factor": 1.0, "base_val": 4.28
            },
            {
                "raw_param": "Loss on Drying (Perte au séchage)",
                "canonical_param": "loss_on_drying",
                "method": "USP <731> (105°C, 2h)",
                "spec_min": None, "spec_max": 5.0,
                "raw_uom": "%", "si_uom": "% (w/w)",
                "conv_factor": 1.0, "base_val": 3.75
            },
            {
                "raw_param": "Lead (Pb) / Plomb",
                "canonical_param": "heavy_metal_lead",
                "method": "ICP-MS (USP <2232>)",
                "spec_min": None, "spec_max": 0.50,
                "raw_uom": "ppm", "si_uom": "ppm",
                "conv_factor": 1.0, "base_val": 0.084
            },
            {
                "raw_param": "Total Aerobic Microbial Count (TAMC / DGAT)",
                "canonical_param": "microbial_tamc",
                "method": "USP <2021>",
                "spec_min": None, "spec_max": 10000,
                "raw_uom": "CFU/g", "si_uom": "CFU/g",
                "conv_factor": 1.0, "base_val": 380
            }
        ]
    },
    "RAW-ASH-EXT5": {
        "item_id": "RAW-ASH-EXT5",
        "product_name": "Organic Ashwagandha Root Extract 5% Withanolides",
        "botanical_source": "Withania somnifera (L.) Dunal (Root)",
        "npn": "NPN-80041289",
        "vendor_id": "VEND-ALPINE-EXT",
        "lab_id": "LAB-EURO-PHYTO",
        "tests": [
            {
                "raw_param": "Withanolid-Gesamtgehalt (Withanolides HPLC)",
                "canonical_param": "active_potency",
                "method": "HPLC-UV (Ph. Eur. Monograph)",
                "spec_min": 5.0, "spec_max": None,
                "raw_uom": "% (m/m)", "si_uom": "% (w/w)",
                "conv_factor": 1.0, "base_val": 5.38
            },
            {
                "raw_param": "Trocknungsverlust (Loss on Drying 105°C)",
                "canonical_param": "loss_on_drying",
                "method": "Ph. Eur. 2.2.32",
                "spec_min": None, "spec_max": 5.0,
                "raw_uom": "% (m/m)", "si_uom": "% (w/w)",
                "conv_factor": 1.0, "base_val": 3.45
            },
            {
                "raw_param": "Blei (Pb) / Lead ICP-MS",
                "canonical_param": "heavy_metal_lead",
                "method": "ICP-MS (DIN EN 15763)",
                "spec_min": None, "spec_max": 0.50,
                "raw_uom": "mg/kg", "si_uom": "ppm",
                "conv_factor": 1.0, "base_val": 0.072
            },
            {
                "raw_param": "Gesamtkeimzahl (Aerobe mesophile Keime - TAMC)",
                "canonical_param": "microbial_tamc",
                "method": "Ph. Eur. 2.6.12",
                "spec_min": None, "spec_max": 10000,
                "raw_uom": "KbE/g", "si_uom": "CFU/g",
                "conv_factor": 1.0, "base_val": 420
            }
        ]
    },
    "RAW-GUT-PRB100": {
        "item_id": "RAW-GUT-PRB100",
        "product_name": "Multi-Strain Probiotic Blend 100 Billion CFU/g",
        "botanical_source": "L. acidophilus, B. lactis, L. plantarum, B. bifidum",
        "npn": "NPN-80084920",
        "vendor_id": "VEND-PACIFIC-ORG",
        "lab_id": "LAB-PACIFIC-TEST",
        "tests": [
            {
                "raw_param": "Viable Probiotic Cell Count (Bactéries viables)",
                "canonical_param": "active_potency",
                "method": "ISO 7889 / ISO 20128",
                "spec_min": 100.0, "spec_max": None,
                "raw_uom": "Billion CFU/g", "si_uom": "Billion CFU/g",
                "conv_factor": 1.0, "base_val": 118.5
            },
            {
                "raw_param": "Water Activity (Activité de l'eau Aw)",
                "canonical_param": "ph_value",
                "method": "USP <922> Dewpoint",
                "spec_min": None, "spec_max": 0.20,
                "raw_uom": "Aw", "si_uom": "Aw",
                "conv_factor": 1.0, "base_val": 0.114
            },
            {
                "raw_param": "Residual Ethanol (Solvants résiduels)",
                "canonical_param": "residual_solvents",
                "method": "USP <467> Headspace GC-MS",
                "spec_min": None, "spec_max": 5000,
                "raw_uom": "ppm", "si_uom": "ppm",
                "conv_factor": 1.0, "base_val": 320
            }
        ]
    },
    "RAW-COQ10-99": {
        "item_id": "RAW-COQ10-99",
        "product_name": "Pure Coenzyme Q10 (Ubiquinone) USP Grade 99.0% - 101.0%",
        "botanical_source": "Fermentation-Derived API",
        "npn": "NPN-80019283",
        "vendor_id": "VEND-NIPPON-PHARMA",
        "lab_id": "LAB-TOKYO-BIO",
        "tests": [
            {
                "raw_param": "定量法: ユビデカレノン (Ubidecarenone Assay)",
                "canonical_param": "active_potency",
                "method": "HPLC-UV (JP 18 / USP Monograph)",
                "spec_min": 99.0, "spec_max": 101.0,
                "raw_uom": "mass%", "si_uom": "% (w/w)",
                "conv_factor": 1.0, "base_val": 99.85
            },
            {
                "raw_param": "強熱残分 (Residue on Ignition JP 2.44)",
                "canonical_param": "loss_on_drying",
                "method": "JP 2.44 / USP <281>",
                "spec_min": None, "spec_max": 0.10,
                "raw_uom": "%", "si_uom": "% (w/w)",
                "conv_factor": 1.0, "base_val": 0.035
            },
            {
                "raw_param": "純度試験: 鉛 (Lead Pb by ICP-MS)",
                "canonical_param": "heavy_metal_lead",
                "method": "JP 1.07 / ICP-MS",
                "spec_min": None, "spec_max": 0.20,
                "raw_uom": "ppb", "si_uom": "ppm",
                "conv_factor": 0.001, "base_val": 25.0
            },
            {
                "raw_param": "生菌数試験: 一般生菌数 (TAMC)",
                "canonical_param": "microbial_tamc",
                "method": "JP 4.05",
                "spec_min": None, "spec_max": 1000,
                "raw_uom": "個/g", "si_uom": "CFU/g",
                "conv_factor": 1.0, "base_val": 40
            }
        ]
    },
    "RAW-OMEGA3-70": {
        "item_id": "RAW-OMEGA3-70",
        "product_name": "Marine Omega-3 Triglyceride Oil (70% EPA/DHA min)",
        "botanical_source": "Engraulis ringens (Wild Pelagic Fish Oil)",
        "npn": "NPN-80092104",
        "vendor_id": "VEND-NORDIC-MAR",
        "lab_id": "LAB-FJORD-ANALYTICAL",
        "tests": [
            {
                "raw_param": "Fettsyreinnhold: EPA (Eicosapentaenoic Acid)",
                "canonical_param": "active_potency",
                "method": "GC-FID (Ph. Eur. 2.4.29 / GOED)",
                "spec_min": 40.0, "spec_max": None,
                "raw_uom": "mg/g", "si_uom": "% (w/w)",
                "conv_factor": 0.1, "base_val": 425.0
            },
            {
                "raw_param": "Fettsyreinnhold: DHA (Docosahexaenoic Acid)",
                "canonical_param": "active_potency",
                "method": "GC-FID (Ph. Eur. 2.4.29 / GOED)",
                "spec_min": 20.0, "spec_max": None,
                "raw_uom": "mg/g", "si_uom": "% (w/w)",
                "conv_factor": 0.1, "base_val": 218.0
            },
            {
                "raw_param": "Peroksidverdi (Peroxide Value - PV)",
                "canonical_param": "other_custom_assay",
                "method": "Ph. Eur. 2.5.5 Potentiometric",
                "spec_min": None, "spec_max": 5.0,
                "raw_uom": "meq O2/kg", "si_uom": "meq O2/kg",
                "conv_factor": 1.0, "base_val": 2.2
            },
            {
                "raw_param": "Anisidintall (p-Anisidine Value - p-AV)",
                "canonical_param": "other_custom_assay",
                "method": "Ph. Eur. 2.5.36 Spectrophotometric",
                "spec_min": None, "spec_max": 20.0,
                "raw_uom": "index", "si_uom": "index",
                "conv_factor": 1.0, "base_val": 11.8
            },
            {
                "raw_param": "Totalt oksidasjonstall (TOTOX = 2*PV + p-AV)",
                "canonical_param": "other_custom_assay",
                "method": "Calculated (2*PV + p-AV)",
                "spec_min": None, "spec_max": 26.0,
                "raw_uom": "index", "si_uom": "index",
                "conv_factor": 1.0, "base_val": 16.2
            }
        ]
    }
}

def generate_coa(doc_idx: int, force_failure: bool = False) -> dict:
    item_keys = list(PRODUCT_CATALOG.keys())
    product_key = item_keys[doc_idx % len(item_keys)]
    product = PRODUCT_CATALOG[product_key]
    lab = LABORATORIES[product["lab_id"]]
    vendor = next(v for v in VENDORS if v["vendor_id"] == product["vendor_id"])

    lot_suffix = f"{random.randint(100, 999)}-{chr(random.randint(65, 90))}"
    lot_num = f"LOT-{product_key.split('-')[1]}26{random.randint(10, 99)}-{lot_suffix}"
    po_num = f"PO-0{random.randint(10000, 99999)}"
    pr_num = f"PR-0{random.randint(10000, 99999)}"
    mfg_date = datetime.now() - timedelta(days=random.randint(10, 60))
    exp_date = mfg_date + timedelta(days=365 * 3)

    test_results = []
    overall_status = "APPROVED"
    discrepancy_count = 0
    reasons = []

    for t_idx, test_meta in enumerate(product["tests"]):
        # Simulate slight random variance
        variance = random.uniform(-0.03, 0.05) * test_meta["base_val"]
        raw_val = round(test_meta["base_val"] + variance, 3 if test_meta["base_val"] < 1 else 2)

        # Failure injection on heavy metal or oxidation if force_failure is True
        is_failing_step = False
        if force_failure and t_idx == (len(product["tests"]) - 1):
            if test_meta["spec_max"] is not None:
                raw_val = round(test_meta["spec_max"] * 1.5, 2)
                is_failing_step = True
            elif test_meta["spec_min"] is not None:
                raw_val = round(test_meta["spec_min"] * 0.7, 2)
                is_failing_step = True

        # SI Normalization
        si_val = round(raw_val * test_meta["conv_factor"], 4 if raw_val * test_meta["conv_factor"] < 1 else 2)

        # Status determination
        status = "PASS"
        if test_meta["spec_min"] is not None and si_val < test_meta["spec_min"]:
            status = "FAIL"
        if test_meta["spec_max"] is not None and si_val > test_meta["spec_max"]:
            status = "FAIL"

        if status == "FAIL" or is_failing_step:
            status = "FAIL"
            overall_status = "REJECTED"
            discrepancy_count += 1
            reasons.append(f"{test_meta['raw_param']} measured {si_val} {test_meta['si_uom']} breached spec limits.")

        test_results.append({
            "step_nbr": (t_idx + 1) * 10,
            "raw_parameter_name": test_meta["raw_param"],
            "canonical_parameter": test_meta["canonical_param"],
            "test_method": test_meta["method"],
            "specification_min": test_meta["spec_min"],
            "specification_max": test_meta["spec_max"],
            "raw_measured_value": raw_val,
            "raw_unit": test_meta["raw_uom"],
            "normalized_si_value": si_val,
            "normalized_si_unit": test_meta["si_uom"],
            "conversion_applied": f"{test_meta['raw_uom']} -> {test_meta['si_uom']} (factor {test_meta['conv_factor']})",
            "status": status
        })

    lot_status = "Released" if overall_status == "APPROVED" else "Quarantine"
    create_ncr = overall_status == "REJECTED"
    auto_approve = overall_status == "APPROVED"

    doc = {
        "document_metadata": {
            "document_type": "Certificate of Analysis (CoA)",
            "document_id": f"COA-{lab['lab_id'][:6]}-2026-{random.randint(10000, 99999)}",
            "issued_date": datetime.now().strftime("%Y-%m-%d"),
            "document_standard": lab["document_standard"],
            "primary_language": lab["primary_language"],
            "secondary_language": lab["secondary_language"],
            "acumatica_erp_mapping": {
                "acumatica_po_number": po_num,
                "acumatica_receipt_number": pr_num,
                "inventory_item_id": product["item_id"],
                "lot_serial_number": lot_num,
                "vendor_id": vendor["vendor_id"],
                "testing_lab_id": lab["lab_id"]
            }
        },
        "issuer_information": {
            "laboratory_name": lab["legal_name"],
            "short_name": lab["short_name"],
            "accreditation": lab["accreditation"],
            "address": f"{lab['city']}, {lab['state_prov']} {lab['postal_code']}, {lab['country']}"
        },
        "product_information": {
            "product_name": product["product_name"],
            "botanical_source": product["botanical_source"],
            "lot_number": lot_num,
            "batch_size_kg": round(random.uniform(500.0, 2500.0), 1),
            "manufacturing_date": mfg_date.strftime("%Y-%m-%d"),
            "expiry_date": exp_date.strftime("%Y-%m-%d"),
            "supplier_vendor_id": vendor["vendor_id"],
            "supplier_vendor_name": vendor["vendor_name"],
            "health_canada_npn": product["npn"]
        },
        "test_results": test_results,
        "authorization": {
            "signatory_name": lab["signatory"],
            "title": lab["signatory_title"],
            "approval_date": datetime.now().isoformat()
        },
        "evaluation_summary": {
            "overall_status": overall_status,
            "discrepancy_count": discrepancy_count,
            "reasons": reasons
        },
        "acumatica_action_directive": {
            "auto_approve_lot": auto_approve,
            "lot_status": lot_status,
            "create_ncr_ticket": create_ncr
        }
    }
    return doc

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Multi-Lab & Multi-Vendor CoA compliance test documents for Acumatica ERP.")
    parser.add_argument("--count", type=int, default=5, help="Number of CoA documents to generate (1 per vendor/lab)")
    parser.add_argument("--outdir", type=str, default="./generated_samples", help="Output directory")
    parser.add_argument("--include-failures", action="store_true", help="Include out-of-spec/fail documents to test Acumatica NCR triggers")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    print(f"Generating {args.count} CoA document sets across 5 distinct vendor/lab configurations in: {args.outdir}")

    for i in range(1, args.count + 1):
        coa_fail = args.include_failures and (i % 2 == 0)
        coa = generate_coa(i - 1, force_failure=coa_fail)
        lab_id = coa["document_metadata"]["acumatica_erp_mapping"]["testing_lab_id"]
        vendor_id = coa["document_metadata"]["acumatica_erp_mapping"]["vendor_id"]
        status_tag = "fail" if coa_fail else "pass"
        coa_fname = f"coa_sample_{i}_{vendor_id}_{lab_id}_{status_tag}.json"
        with open(os.path.join(args.outdir, coa_fname), "w", encoding="utf-8") as f:
            json.dump(coa, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {args.count} multi-lab synthetic CoA documents.")

if __name__ == "__main__":
    main()
