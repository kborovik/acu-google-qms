"""Data models and master data loaders for document generation."""

import json
import random
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any, cast

MASTER_DATA_DIR = Path(__file__).resolve().parent.parent / "acumatica" / "master_data"

DEFAULT_LAB_SIGNATORIES: dict[str, tuple[str, str]] = {
    "LAB-GL-ANALYTICAL": (
        "Dr. Arthur Pendelton, Ph.D., C.Chem.",
        "Director of Analytical Chemistry",
    ),
    "LAB-PACIFIC-TEST": (
        "Dr. Fiona MacLeod, Ph.D.",
        "Chief Microbiologist & QA Director",
    ),
    "LAB-EURO-PHYTO": (
        "Dr. rer. nat. Hans-Jürgen Weber",
        "Leiter der Qualitätskontrolle (Head of QC)",
    ),
    "LAB-TOKYO-BIO": (
        "Kenji Takahashi, Ph.D. (高橋 健司)",
        "Director of Pharmaceutical Quality Testing",
    ),
    "LAB-FJORD-ANALYTICAL": (
        "Dr. Ingrid Solberg, Ph.D.",
        "Head of Marine Lipid Analytics",
    ),
}

PREFERRED_CARRIERS: dict[str, str] = {
    "VEND-NORTH-BIO": "FedEx Freight Canada",
    "VEND-ALPINE-EXT": "DHL Global Forwarding",
    "VEND-PACIFIC-ORG": "Day & Ross Freight",
    "VEND-NIPPON-PHARMA": "Nippon Express Global Logistics",
    "VEND-NORDIC-MAR": "Kuehne+Nagel Cold-Chain Logistics",
}

TEST_ID_TO_CANONICAL: dict[str, str] = {
    "ASSAY_POLYPHENOLS": "active_potency",
    "ASSAY_ANTHOCYANINS": "active_potency",
    "ASSAY_WITHANOLIDES": "active_potency",
    "ASSAY_ROSAVINS": "active_potency",
    "ASSAY_CURCUMINOIDS": "active_potency",
    "ASSAY_PROBIOTIC_COUNT": "active_potency",
    "ASSAY_COQ10": "active_potency",
    "ASSAY_THEANINE": "active_potency",
    "ASSAY_OMEGA3_EPA_DHA": "active_potency",
    "ASSAY_ASTAXANTHIN": "active_potency",
    "PHYS_LOD": "loss_on_drying",
    "PHYS_AW": "water_activity",
    "PHYS_RESIDUE_ON_IGNITION": "residue_on_ignition",
    "PHYS_OPTICAL_ROTATION": "optical_rotation",
    "CHEM_PEROXIDE_VALUE": "peroxide_value",
    "CHEM_ANISIDINE_VALUE": "anisidine_value",
    "CHEM_TOTOX": "totox_value",
    "HM_LEAD": "heavy_metal_lead",
    "HM_ARSENIC": "heavy_metal_arsenic",
    "HM_CADMIUM": "heavy_metal_cadmium",
    "HM_MERCURY": "heavy_metal_mercury",
    "MICRO_TAMC": "microbial_tamc",
    "MICRO_TYMC": "microbial_tymc",
    "PATH_ECOLI": "pathogen_e_coli",
    "PATH_SALMONELLA": "pathogen_salmonella",
    "CONTAM_DIOXINS_PCBS": "dioxins_and_pcbs",
    "SOLV_RESIDUAL_ETHANOL": "residual_solvents",
    "SOLV_RESIDUAL_METHANOL": "residual_solvents",
}


@dataclass(frozen=True)
class Vendor:
    vendor_id: str
    legal_name: str
    country: str
    headquarters_address: str
    city_region: str
    primary_contact_name: str
    primary_contact_email: str
    primary_contact_phone: str
    primary_preferred_lab_id: str
    gmp_certification_status: str
    foreign_site_annex_ref: str | None
    carrier_preferred: str


@dataclass(frozen=True)
class Product:
    inventory_id: str
    vendor_id: str
    vendor_name: str
    description: str
    botanical_source: str | None
    item_class: str
    base_uom: str
    purchase_uom: str
    lot_serial_class: str
    valuation_method: str
    default_warehouse: str
    default_quarantine_location: str
    health_canada_npn_reference: str | None
    shelf_life_days: int
    min_shelf_life_receiving_days: int
    qms_inspection_plan_id: str
    assigned_primary_lab: str
    assigned_secondary_lab: str
    storage_conditions: str


@dataclass(frozen=True)
class TestLab:
    lab_id: str
    lab_name: str
    country: str
    city_region: str
    address: str
    accreditation_body: str
    accreditation_number: str
    document_standard: str
    document_type_bilingual: str
    primary_language: str
    secondary_language: str
    signature_title: str
    authorized_signatory_name: str
    uom_conversions_to_si: dict[str, Any]
    bilingual_test_synonyms: dict[str, dict[str, str]]


def safe_float(val: Any) -> float | None:
    """Safely converts numeric or string values to float, returning None on failure."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    try:
        return float(str(val).strip())
    except ValueError, TypeError:
        return None


@dataclass(frozen=True)
class TestCriterion:
    step_nbr: int
    test_id: str
    description: str
    method: str
    target_value: float | None
    min_value: float | None
    max_value: float | None
    uom: str
    criticality: str
    raw_target_text: str | None = None


@dataclass(frozen=True)
class InspectionPlan:
    plan_id: str
    description: str
    inventory_id: str
    sampling_plan: str
    test_criteria: list[TestCriterion]


@dataclass
class TestResult:
    step_nbr: int
    test_id: str
    analyte_name: str
    test_method: str
    specification_text: str
    observed_value_text: str
    numeric_value: float | None
    uom: str
    passed: bool
    criticality: str
    regional_analyte_name: str | None = None
    regional_uom: str | None = None
    regional_value_text: str | None = None


@dataclass
class InboundShipmentSuite:
    manifest_id: str
    receipt_number: str
    purchase_order_number: str
    lot_serial_number: str
    vendor: Vendor
    product: Product
    test_lab: TestLab
    inspection_plan: InspectionPlan
    carrier_name: str
    tracking_pro_number: str
    trailer_number: str
    seal_number: str
    manufacturing_date: str
    expiration_date: str
    received_quantity_kg: float
    container_count: int
    pallet_count: int
    storage_conditions: str
    overall_status: str  # "PASS" or "FAIL"
    test_results: list[TestResult] = field(default_factory=list)
    failure_reasons: list[str] = field(default_factory=list)


class MasterDataRegistry:
    def __init__(self, data_dir: Path = MASTER_DATA_DIR) -> None:
        self.data_dir = data_dir
        self.vendors: dict[str, Vendor] = {}
        self.products: dict[str, Product] = {}
        self.test_labs: dict[str, TestLab] = {}
        self.inspection_plans: dict[str, InspectionPlan] = {}
        self._load_all()

    def _load_all(self) -> None:
        vendors_file = self.data_dir / "vendors.json"
        with vendors_file.open("r", encoding="utf-8") as f:
            v_data = json.load(f)
            for v in v_data.get("vendors", []):
                v_id = v["vendor_id"]
                addr = v.get("address", {})
                comp = v.get("compliance", {})
                contacts = v.get("contacts", {})
                c_country = addr.get("country", "CA")
                c_addr = addr.get("address_line1", "")
                c_city = f"{addr.get('city', '')}, {addr.get('state_province', '')}"

                pref_labs = v.get("preferred_test_labs", [])
                pref_lab_id = (
                    pref_labs[0]
                    if pref_labs
                    else v.get("primary_preferred_lab_id", "LAB-GL-ANALYTICAL")
                )

                vendor = Vendor(
                    vendor_id=v_id,
                    legal_name=v.get("legal_name", v.get("vendor_name", v_id)),
                    country=c_country,
                    headquarters_address=c_addr,
                    city_region=c_city,
                    primary_contact_name=contacts.get(
                        "qa_contact_name",
                        contacts.get("sales_contact", "QA Manager"),
                    ),
                    primary_contact_email=contacts.get(
                        "qa_email",
                        contacts.get("sales_email", "qa@vendor.com"),
                    ),
                    primary_contact_phone=contacts.get("phone", "+1-800-555-0100"),
                    primary_preferred_lab_id=pref_lab_id,
                    gmp_certification_status=comp.get(
                        "gmp_certification_body", "GMP Certified"
                    ),
                    foreign_site_annex_ref=comp.get("health_canada_foreign_site_annex"),
                    carrier_preferred=PREFERRED_CARRIERS.get(
                        v_id, "FedEx Freight Canada"
                    ),
                )
                self.vendors[vendor.vendor_id] = vendor

        products_file = self.data_dir / "products.json"
        with products_file.open("r", encoding="utf-8") as f:
            p_data = json.load(f)
            for p in p_data.get("raw_materials", []):
                prod = Product(
                    inventory_id=p["inventory_id"],
                    vendor_id=p["vendor_id"],
                    vendor_name=p["vendor_name"],
                    description=p["description"],
                    botanical_source=p.get("botanical_source"),
                    item_class=p["item_class"],
                    base_uom=p["base_uom"],
                    purchase_uom=p["purchase_uom"],
                    lot_serial_class=p["lot_serial_class"],
                    valuation_method=p["valuation_method"],
                    default_warehouse=p["default_warehouse"],
                    default_quarantine_location=p["default_quarantine_location"],
                    health_canada_npn_reference=p.get("health_canada_npn_reference"),
                    shelf_life_days=int(p["shelf_life_days"]),
                    min_shelf_life_receiving_days=int(
                        p["min_shelf_life_receiving_days"]
                    ),
                    qms_inspection_plan_id=p["qms_inspection_plan_id"],
                    assigned_primary_lab=p.get(
                        "assigned_primary_lab", "LAB-GL-ANALYTICAL"
                    ),
                    assigned_secondary_lab=p.get(
                        "assigned_secondary_lab", "LAB-PACIFIC-TEST"
                    ),
                    storage_conditions=p["storage_conditions"],
                )
                self.products[prod.inventory_id] = prod

        labs_file = self.data_dir / "test_labs.json"
        with labs_file.open("r", encoding="utf-8") as f:
            l_data = json.load(f)
            for lab in l_data.get("testing_laboratories", []):
                lab_id = lab["lab_id"]
                f_addr = lab.get("facility_address", {})
                accs = lab.get("accreditations", [])
                doc_std = lab.get("document_standard", {})

                acc_body = (
                    accs[0].get("body", "ISO/IEC 17025") if accs else "ISO/IEC 17025"
                )
                acc_num = (
                    accs[0].get(
                        "scope_number",
                        accs[0].get("licence_number", "CALA-9481"),
                    )
                    if accs
                    else "CALA-9481"
                )
                signatory_name, signatory_title = DEFAULT_LAB_SIGNATORIES.get(
                    lab_id, ("Dr. Arthur Pendelton", "Lab Director")
                )

                synonyms_map: dict[str, dict[str, str]] = {}
                for item in lab.get("bilingual_terms_and_synonyms", []):
                    param = item.get("canonical_parameter", "")
                    syn_en = item.get("synonyms_en", [])
                    syn_fr = item.get("synonyms_fr", [])
                    syn_de = item.get("synonyms_de", [])
                    syn_ja = item.get("synonyms_ja", [])
                    syn_no = item.get("synonyms_no", [])
                    reg_term = (
                        (syn_de[0] if syn_de else "")
                        or (syn_ja[0] if syn_ja else "")
                        or (syn_no[0] if syn_no else "")
                        or (syn_fr[0] if syn_fr else "")
                    )
                    synonyms_map[param] = {
                        "en": syn_en[0] if syn_en else "",
                        "regional_term": reg_term,
                    }

                test_lab = TestLab(
                    lab_id=lab_id,
                    lab_name=lab.get("legal_name", lab.get("short_name", lab_id)),
                    country=f_addr.get("country", "CA"),
                    city_region=(
                        f"{f_addr.get('city', '')}, {f_addr.get('state_province', '')}"
                    ),
                    address=f_addr.get("address_line1", ""),
                    accreditation_body=acc_body,
                    accreditation_number=acc_num,
                    document_standard=doc_std.get(
                        "framework",
                        doc_std.get("standard_name", "ISO/IEC 17025"),
                    ),
                    document_type_bilingual=doc_std.get(
                        "layout_type", "Certificate of Analysis"
                    ),
                    primary_language=doc_std.get("primary_language", "en-CA"),
                    secondary_language=doc_std.get("secondary_language", "fr-CA"),
                    signature_title=signatory_title,
                    authorized_signatory_name=signatory_name,
                    uom_conversions_to_si=lab.get(
                        "measurement_units_and_si_conversion", {}
                    ),
                    bilingual_test_synonyms=synonyms_map,
                )
                self.test_labs[test_lab.lab_id] = test_lab

        plans_file = self.data_dir / "qms_inspection_plans.json"
        with plans_file.open("r", encoding="utf-8") as f:
            pl_data = json.load(f)
            for pl in pl_data.get("qms_inspection_plans", []):
                criteria: list[TestCriterion] = []
                for c in pl.get("test_criteria", []):
                    criterion = TestCriterion(
                        step_nbr=int(c["step_nbr"]),
                        test_id=c["test_id"],
                        description=c["description"],
                        method=c["method"],
                        target_value=safe_float(c.get("target_value")),
                        min_value=safe_float(c.get("min_value")),
                        max_value=safe_float(c.get("max_value")),
                        uom=c.get("uom", c.get("expected_text", "Absent")),
                        criticality=c.get("criticality", "Major"),
                        raw_target_text=(
                            str(c["target_value"])
                            if c.get("target_value") is not None
                            else None
                        ),
                    )
                    criteria.append(criterion)
                plan = InspectionPlan(
                    plan_id=pl["plan_id"],
                    description=pl["description"],
                    inventory_id=pl["inventory_id"],
                    sampling_plan=pl.get(
                        "sampling_plan",
                        "ISO 2859-1 Level II Normal Single Sampling",
                    ),
                    test_criteria=criteria,
                )
                self.inspection_plans[plan.plan_id] = plan


def plus_years(anchor: date, years: int) -> date:
    """Shifts anchor by whole calendar years; Feb 29 collapses to Feb 28."""
    try:
        return anchor.replace(year=anchor.year + years)
    except ValueError:  # leap-day anchor into a non-leap target year
        return anchor.replace(year=anchor.year + years, month=2, day=28)


def build_synthetic_shipment_suite(
    registry: MasterDataRegistry,
    inventory_id: str | None = None,
    vendor_id: str | None = None,
    force_status: str | None = None,
    lot_nbr: str | None = None,
    po_nbr: str | None = None,
    receipt_nbr: str | None = None,
    quantity_kg: float | None = None,
    as_of: date | None = None,
) -> InboundShipmentSuite:
    """Builds a complete, consistent InboundShipmentSuite for all 3 documents."""
    # Resolve product
    if inventory_id and inventory_id in registry.products:
        product = registry.products[inventory_id]
    else:
        product = random.choice(list(registry.products.values()))

    # Resolve vendor
    if vendor_id and vendor_id in registry.vendors:
        vendor = registry.vendors[vendor_id]
    elif product.vendor_id in registry.vendors:
        vendor = registry.vendors[product.vendor_id]
    else:
        vendor = random.choice(list(registry.vendors.values()))

    # Resolve lab
    lab_id = product.assigned_primary_lab or vendor.primary_preferred_lab_id
    test_lab = registry.test_labs.get(
        lab_id,
        next(iter(registry.test_labs.values())),
    )

    # Resolve plan
    plan = registry.inspection_plans.get(
        product.qms_inspection_plan_id,
        next(iter(registry.inspection_plans.values())),
    )

    # Identifiers
    rnd_suffix = f"{random.randint(100, 999)}"
    seq = random.randint(1000, 9999)
    prefix_map = {
        "RAW-ECH-EXT4": "EC",
        "RAW-ELD-EXT10": "EL",
        "RAW-ASH-EXT5": "AS",
        "RAW-RHOD-EXT3": "RH",
        "RAW-CURC-95": "CU",
        "RAW-GUT-PRB100": "PR",
        "RAW-COQ10-99": "CQ",
        "RAW-THEA-98": "TH",
        "RAW-ASTA-10": "AT",
        "RAW-OMEGA3-70": "OM",
    }
    code = prefix_map.get(product.inventory_id, "RM")
    actual_lot = lot_nbr or f"LOT-{code}2603-{rnd_suffix}A"
    actual_po = po_nbr or f"PO-04{seq}"
    actual_receipt = receipt_nbr or f"PR-2026-00{seq}"
    manifest_id = f"MAN-2026-{seq}"

    # Determine status
    if force_status:
        overall_status = force_status.upper()
    else:
        overall_status = "FAIL" if random.random() < 0.20 else "PASS"

    # Dates (V10): as-of anchor defaults to the run date (local). Manufacture,
    # ship, and CoA/BOL stamps all render the anchor; expiry = as-of + product
    # shelf-life (3-year fallback when absent).
    anchor_date = as_of if as_of is not None else date.today()
    mfg_date = anchor_date.isoformat()
    if product.shelf_life_days > 0:
        expiry_date = (
            anchor_date + timedelta(days=product.shelf_life_days)
        ).isoformat()
    else:
        expiry_date = plus_years(anchor_date, 3).isoformat()

    # Quantities & Containers
    if quantity_kg is not None and quantity_kg > 0:
        qty_kg = float(quantity_kg)
    else:
        qty_kg = random.choice([250.0, 500.0, 750.0, 1000.0])
    drum_count = max(1, int(qty_kg / 25.0))
    pallet_count = max(1, int(drum_count / 16))

    # Carrier details
    carrier = vendor.carrier_preferred
    pro_number = f"PRO-{random.randint(10000000, 99999999)}"
    trailer_nbr = f"TR-{random.randint(1000, 9999)}"
    seal_nbr = f"SEAL-{random.randint(100000, 999999)}"

    # Generate Test Results
    test_results: list[TestResult] = []
    failure_reasons: list[str] = []

    for crit in plan.test_criteria:
        # Check synonyms
        canonical_key = TEST_ID_TO_CANONICAL.get(crit.test_id, crit.test_id.lower())
        synonym_data = test_lab.bilingual_test_synonyms.get(canonical_key, {})
        regional_name = synonym_data.get("regional_term") or synonym_data.get("en")

        # Format spec text
        if crit.min_value is not None and crit.max_value is not None:
            spec_text = f"{crit.min_value:.2f} - {crit.max_value:.2f} {crit.uom}"
        elif crit.min_value is not None:
            spec_text = f"≥ {crit.min_value:.2f} {crit.uom}"
        elif crit.max_value is not None:
            spec_text = f"≤ {crit.max_value:.2f} {crit.uom}"
        elif crit.raw_target_text:
            spec_text = crit.raw_target_text
        else:
            spec_text = f"{crit.uom}"

        # Determine pass/fail for this analyte
        is_failing_item = False
        if overall_status == "FAIL" and not failure_reasons:
            is_failing_item = True

        if is_failing_item:
            passed = False
            if crit.min_value is not None:
                numeric_val = round(crit.min_value * 0.85, 3)
                obs_text = f"{numeric_val} {crit.uom}"
                failure_reasons.append(
                    f"{crit.description} below limit ({obs_text} < {spec_text})"
                )
            elif crit.max_value is not None:
                numeric_val = round(crit.max_value * 1.5, 3)
                obs_text = f"{numeric_val} {crit.uom}"
                failure_reasons.append(
                    f"{crit.description} exceeded limit ({obs_text} > {spec_text})"
                )
            else:
                numeric_val = None
                obs_text = "Out of Spec / Positive"
                failure_reasons.append(f"{crit.description} failed specification")
        else:
            passed = True
            if crit.target_value is not None:
                delta = (
                    (crit.max_value - crit.target_value) * 0.2
                    if crit.max_value
                    else max(0.1, crit.target_value * 0.05)
                )
                numeric_val = max(
                    0.001,
                    round(
                        crit.target_value + random.uniform(-delta / 2, delta / 2),
                        3,
                    ),
                )
                obs_text = f"{numeric_val} {crit.uom}"
            elif crit.max_value is not None and crit.min_value is not None:
                mid = (crit.min_value + crit.max_value) / 2.0
                mid_delta = crit.max_value - crit.min_value
                numeric_val = max(
                    crit.min_value,
                    round(
                        mid + random.uniform(-0.1, 0.1) * mid_delta,
                        3,
                    ),
                )
                obs_text = f"{numeric_val} {crit.uom}"
            elif crit.max_value is not None:
                if "CFU" in crit.uom or "個" in crit.uom or "KbE" in crit.uom:
                    numeric_val = float(
                        random.randint(10, min(500, int(crit.max_value * 0.3)))
                    )
                    obs_text = f"{int(numeric_val)} {crit.uom}"
                else:
                    numeric_val = max(
                        0.0001,
                        round(crit.max_value * random.uniform(0.05, 0.35), 4),
                    )
                    obs_text = (
                        f"{numeric_val} {crit.uom}"
                        if numeric_val > 0.001
                        else f"< {crit.max_value * 0.1:.3f} {crit.uom}"
                    )
            elif "Absent" in crit.uom or "Conforms" in crit.uom:
                numeric_val = None
                obs_text = crit.uom
            else:
                numeric_val = None
                obs_text = "Conforms"

        # Check regional UoM conversions
        regional_uom = crit.uom
        regional_val_text = obs_text
        if test_lab.lab_id == "LAB-EURO-PHYTO":
            if crit.uom == "% (w/w)":
                regional_uom = "% (m/m)"
            elif crit.uom == "ppm":
                regional_uom = "mg/kg"
            elif crit.uom == "CFU/g":
                regional_uom = "KbE/g"
        elif test_lab.lab_id == "LAB-TOKYO-BIO":
            if crit.uom == "% (w/w)":
                regional_uom = "mass%"
            elif crit.uom == "CFU/g":
                regional_uom = "個/g"
        elif test_lab.lab_id == "LAB-FJORD-ANALYTICAL":
            if crit.uom == "meq O2/kg":
                regional_uom = "meq O2/kg"

        if regional_uom != crit.uom and numeric_val is not None:
            regional_val_text = f"{numeric_val} {regional_uom}"

        test_results.append(
            TestResult(
                step_nbr=crit.step_nbr,
                test_id=crit.test_id,
                analyte_name=crit.description,
                test_method=crit.method,
                specification_text=spec_text,
                observed_value_text=obs_text,
                numeric_value=numeric_val,
                uom=crit.uom,
                passed=passed,
                criticality=crit.criticality,
                regional_analyte_name=regional_name,
                regional_uom=regional_uom,
                regional_value_text=regional_val_text,
            )
        )

    return InboundShipmentSuite(
        manifest_id=manifest_id,
        receipt_number=actual_receipt,
        purchase_order_number=actual_po,
        lot_serial_number=actual_lot,
        vendor=vendor,
        product=product,
        test_lab=test_lab,
        inspection_plan=plan,
        carrier_name=carrier,
        tracking_pro_number=pro_number,
        trailer_number=trailer_nbr,
        seal_number=seal_nbr,
        manufacturing_date=mfg_date,
        expiration_date=expiry_date,
        received_quantity_kg=qty_kg,
        container_count=drum_count,
        pallet_count=pallet_count,
        storage_conditions=product.storage_conditions,
        overall_status=overall_status,
        test_results=test_results,
        failure_reasons=failure_reasons,
    )


def extract_field_value(val: object) -> object:
    """Helper to unpack {'value': ...} Acumatica REST payload or plain value."""
    if isinstance(val, dict):
        d_val = cast(dict[str, object], val)
        if "value" in d_val:
            return d_val["value"]
        return d_val
    return val


def build_shipment_suite_from_po_data(
    registry: MasterDataRegistry,
    po_data: dict[str, Any],
    force_status: str | None = None,
    lot_nbr: str | None = None,
    as_of: date | None = None,
) -> InboundShipmentSuite:
    """Builds an InboundShipmentSuite from an Acumatica Purchase Order JSON payload."""
    raw_po = cast(
        object,
        po_data.get("po_number")
        or po_data.get("purchase_order_number")
        or po_data.get("OrderNbr")
        or po_data.get("OrderNo")
        or "PO-049000",
    )
    po_nbr = str(extract_field_value(raw_po))

    raw_vendor = cast(
        object,
        po_data.get("vendor_id") or po_data.get("VendorID") or po_data.get("Vendor"),
    )
    vendor_id = str(extract_field_value(raw_vendor)) if raw_vendor is not None else None

    inventory_id: str | None = None
    order_qty: float | None = None

    lines_val = cast(
        object,
        po_data.get("lines") or po_data.get("Details") or po_data.get("line_items"),
    )
    if isinstance(lines_val, list):
        typed_lines = cast(list[object], lines_val)
        if len(typed_lines) > 0:
            first_line = typed_lines[0]
            if isinstance(first_line, dict):
                fl_dict = cast(dict[str, object], first_line)
                line_inv = (
                    fl_dict.get("inventory_id")
                    or fl_dict.get("InventoryID")
                    or fl_dict.get("item_id")
                )
                if line_inv is not None:
                    inventory_id = str(extract_field_value(line_inv))

                line_qty = extract_field_value(
                    fl_dict.get("order_qty")
                    or fl_dict.get("OrderQty")
                    or fl_dict.get("quantity")
                    or fl_dict.get("quantity_kg")
                )
                order_qty = safe_float(line_qty)

    if not inventory_id:
        top_inv = cast(
            object,
            po_data.get("inventory_id") or po_data.get("InventoryID"),
        )
        if top_inv is not None:
            inventory_id = str(extract_field_value(top_inv))

    if order_qty is None:
        top_qty = cast(
            object,
            po_data.get("order_qty")
            or po_data.get("quantity_kg")
            or po_data.get("OrderQty"),
        )
        order_qty = safe_float(extract_field_value(top_qty))

    return build_synthetic_shipment_suite(
        registry=registry,
        inventory_id=inventory_id,
        vendor_id=vendor_id,
        force_status=force_status,
        lot_nbr=lot_nbr,
        po_nbr=po_nbr,
        quantity_kg=order_qty,
        as_of=as_of,
    )
