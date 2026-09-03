"""Command-line interface (CLI) for generating shipping document PDF suites.

Uses Click to provide subcommands for generating individual or complete
3-document suites (CoA, Packing Slip, BOL).

LLM agents: invoke bare ``docgen`` / ``python -m docgen`` (no subcommand) or
``docgen --help`` to print the full multi-command agent help in one shot.
"""

from __future__ import annotations

import json
from pathlib import Path

import click

from docgen.bol_builder import generate_bol_pdf
from docgen.coa_builder import generate_coa_pdf
from docgen.models import (
    InboundShipmentSuite,
    MasterDataRegistry,
    build_shipment_suite_from_po_data,
    build_synthetic_shipment_suite,
)
from docgen.packing_slip_builder import generate_packing_slip_pdf

# ---------------------------------------------------------------------------
# Agent-oriented help surfaces (shown on bare `docgen` and `docgen --help`)
# ---------------------------------------------------------------------------

AGENT_HELP_EPILOG = """
========================================================================
LLM AGENT OPERATING MANUAL
========================================================================

AUDIENCE
  This CLI is the synthetic inbound shipping-document factory for the
  GCP Acumatica CoA ingestion platform. Agents use it to produce the
  three mandatory dock-receiving PDFs plus a machine-readable manifest.

INVOCATION (prefer uv)
  uv run python -m docgen              # full agent help (this text)
  uv run python -m docgen --help       # identical full agent help
  uv run docgen <COMMAND> [OPTIONS]    # console-script entry point
  uv run python -m docgen <COMMAND> ...

COMMAND SELECTION (decision tree)
  1. Need valid IDs?              -> list-master-data
  2. Have Acumatica PO JSON?      -> from-po  (or generate-suite --po-json)
  3. Need full 3-doc suite?       -> generate-suite
  4. Need only CoA / pack / BOL?  -> generate-coa | generate-packing-slip | generate-bol
  5. Need multi-vendor corpus?    -> batch

MASTER DATA (resolve IDs here; never invent)
  Source dir: acumatica/master_data/
    vendors.json | products.json | test_labs.json | qms_inspection_plans.json

  Vendors (vendor_id -> preferred lab):
    VEND-NORTH-BIO     -> LAB-GL-ANALYTICAL      (CA)
    VEND-ALPINE-EXT    -> LAB-EURO-PHYTO         (DE)
    VEND-PACIFIC-ORG   -> LAB-PACIFIC-TEST       (CA)
    VEND-NIPPON-PHARMA -> LAB-TOKYO-BIO          (JP)
    VEND-NORDIC-MAR    -> LAB-FJORD-ANALYTICAL   (NO)

  Products (inventory_id -> default vendor):
    RAW-ECH-EXT4   VEND-NORTH-BIO      Echinacea 4% polyphenols
    RAW-ELD-EXT10  VEND-NORTH-BIO      Elderberry 10% anthocyanins
    RAW-ASH-EXT5   VEND-ALPINE-EXT     Ashwagandha 5% withanolides
    RAW-RHOD-EXT3  VEND-ALPINE-EXT     Rhodiola 3% rosavins
    RAW-CURC-95    VEND-PACIFIC-ORG    Curcuminoids 95%
    RAW-GUT-PRB100 VEND-PACIFIC-ORG    Probiotic 100B CFU
    RAW-COQ10-99   VEND-NIPPON-PHARMA  CoQ10 USP 99%
    RAW-THEA-98    VEND-NIPPON-PHARMA  L-Theanine 98.5%
    RAW-OMEGA3-70  VEND-NORDIC-MAR     Omega-3 TG 70% EPA+DHA
    RAW-ASTA-10    VEND-NORDIC-MAR     Astaxanthin oleoresin 10%

RESOLUTION RULES
  --inventory-id omitted  -> random product from master data
  --vendor-id omitted     -> product.vendor_id (then random vendor)
  Lab                     -> product.assigned_primary_lab
  QMS plan                -> product.qms_inspection_plan_id
  --lot-nbr omitted       -> LOT-<CODE>2603-<NNN>A  (CODE from product map)
  --po-nbr / --receipt-nbr omitted -> synthetic PO-04#### / PR-2026-00####
  --status pass|fail      -> forces CoA overall evaluation (default: pass)
  Unknown inventory/vendor IDs fall back to random master-data picks (no hard fail).

OUTPUT ARTIFACTS
  generate-suite / from-po (default outdir=output/shipping_docs):
    COA_<inventory_id>_<lot>.pdf
    PACKING_SLIP_<inventory_id>_<lot>.pdf
    BOL_<inventory_id>_<lot>.pdf
    MANIFEST_<inventory_id>_<lot>.json   (--emit-json, default ON)

  batch (default outdir=output/batch_shipping_docs):
    COA_suite_<n>_<vendor_id>_<inventory_id>_<lot>.pdf
    PACKING_SLIP_suite_<n>_...pdf
    BOL_suite_<n>_...pdf
    MANIFEST_suite_<n>_...json

  Standalone defaults:
    generate-coa           -> output/coa/
    generate-packing-slip  -> output/packing_slips/
    generate-bol           -> output/bol/

MANIFEST JSON (ground truth for agents; NOT printed on PDFs)
  Top-level keys:
    manifest_id, overall_status ("PASS"|"FAIL"),
    erp_association_metadata  -> PO#, receipt#, vendor_id, inventory_id,
                                 warehouse, quarantine bin, inspection_plan_id
    external_document_metadata -> delivery note / CoA / BOL external fields
    line_items, analytical_results, failure_reasons

ZERO ERP LEAKAGE (invariant)
  PDFs must NEVER contain internal Acumatica identifiers:
    no internal PO#, VendorID, InventoryID, POReceipt#, QMS plan ID, warehouse bins.
  ERP identifiers live ONLY in MANIFEST_*.json under erp_association_metadata.
  External PDFs show commercial names, lot numbers, delivery-note / CoA / BOL numbers.

PO JSON INPUT (--po-json / from-po)
  Accepts Acumatica REST-shaped or flat JSON. Field aliases supported:
    PO number:  po_number | purchase_order_number | OrderNbr | OrderNo
                (also {"value": "..."} wrappers)
    Vendor:     vendor_id | VendorID | Vendor
    Lines:      lines | Details | line_items
      line inventory: inventory_id | InventoryID | item_id
      line qty:       order_qty | OrderQty | quantity | quantity_kg
    Top-level inventory_id / OrderQty also accepted when lines absent.
  Uses FIRST line only. Qty drives received_quantity_kg + container/pallet math.

STATUS / FAIL SIMULATION
  --status pass  -> all QMS plan analytes in-spec (PASS)
  --status fail  -> first plan criterion forced out-of-spec; failure_reasons populated
  batch --include-failures (default): odd suites FAIL, even PASS
  batch --all-pass: every suite PASS

CANONICAL AGENT RECIPES
  # Discover IDs
  uv run python -m docgen list-master-data

  # In-spec receiving suite for a known SKU
  uv run python -m docgen generate-suite \\
    --inventory-id RAW-ECH-EXT4 --status pass --outdir ./output/shipping_docs

  # Out-of-spec suite for quarantine / NCR testing
  uv run python -m docgen generate-suite \\
    --inventory-id RAW-ASH-EXT5 --status fail --outdir ./output/shipping_docs_failed

  # From Acumatica PO payload
  uv run python -m docgen from-po \\
    --po-json ./path/to/po_order.json --status pass --outdir ./output/po_shipping_docs

  # Multi-vendor corpus (5 suites, alternating pass/fail)
  uv run python -m docgen batch --count 5 --include-failures \\
    --outdir ./output/batch_shipping_docs

RELATED SPECS (read before changing behavior)
  docgen/SPEC.md
  domain/MANDATORY_SHIPPING_DOCUMENTS_SPEC.md
  domain/COA_INGESTION_SPEC.md
  AGENTS.md §3.1
"""


class AgentHelpGroup(click.Group):
    """Click group that expands ``--help`` to the full multi-command agent view.

    Bare invocation (no subcommand) and ``--help`` both render:
    group usage + options + every subcommand's full help + agent epilog.
    """

    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Render each subcommand's full Click help instead of a one-line list."""
        commands: list[tuple[str, click.Command]] = []
        for name in self.list_commands(ctx):
            cmd = self.get_command(ctx, name)
            if cmd is None or cmd.hidden:
                continue
            commands.append((name, cmd))

        if not commands:
            return

        formatter.write_paragraph()
        formatter.write("Commands (full help for each subcommand):\n")
        for name, cmd in commands:
            # Child context so Click formats Usage: with the subcommand name.
            sub_ctx = click.Context(cmd, info_name=name, parent=ctx)
            formatter.write("\n")
            formatter.write("-" * 72)
            formatter.write(f"\nCommand: {name}\n")
            formatter.write("-" * 72)
            formatter.write("\n")
            formatter.write(cmd.get_help(sub_ctx))
            formatter.write("\n")

    def format_epilog(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Write the agent operating manual without Click text-reflow wrapping."""
        if not self.epilog:
            return
        formatter.write_paragraph()
        # write() preserves monospace layout; write_text() would collapse it.
        formatter.write(self.epilog.rstrip("\n"))
        formatter.write("\n")


def emit_manifest_json(suite: InboundShipmentSuite, out_path: Path) -> Path:
    """Emits the structured InboundShipmentDocumentManifest JSON.

    Distinguishes external document representations (visible on physical PDFs)
    from ground-truth ERP association metadata (used for automated validation/matching).
    """
    gross_kg = (
        suite.received_quantity_kg
        + (suite.container_count * 2.5)
        + (suite.pallet_count * 20.0)
    )
    manifest_data = {
        "manifest_id": suite.manifest_id,
        "overall_status": suite.overall_status,
        "erp_association_metadata": {
            "purchase_order_number": suite.purchase_order_number,
            "receipt_number": suite.receipt_number,
            "vendor_id": suite.vendor.vendor_id,
            "inventory_id": suite.product.inventory_id,
            "default_warehouse": suite.product.default_warehouse,
            "default_quarantine_location": suite.product.default_quarantine_location,
            "inspection_plan_id": suite.inspection_plan.plan_id,
        },
        "external_document_metadata": {
            "supplier_delivery_note": {
                "delivery_note_number": f"DN-{suite.manifest_id[4:]}",
                "supplier_order_ref": f"ORD-{suite.manifest_id[4:]}",
                "supplier_name": suite.vendor.legal_name,
                "consignee_name": "CanNordic BioNutra Inc.",
                "product_description": suite.product.description,
                "lot_number": suite.lot_serial_number,
                "net_weight_kg": suite.received_quantity_kg,
                "container_count": suite.container_count,
                "ship_date": suite.manufacturing_date,
            },
            "certificate_of_analysis": {
                "certificate_number": f"COA-{suite.manifest_id[4:]}",
                "testing_laboratory": suite.test_lab.lab_name,
                "document_standard": suite.test_lab.document_standard,
                "accreditation_number": suite.test_lab.accreditation_number,
                "product_description": suite.product.description,
                "lot_number": suite.lot_serial_number,
                "overall_evaluation": suite.overall_status,
            },
            "bill_of_lading": {
                "bol_number": f"BOL-{suite.manifest_id[4:]}",
                "carrier_name": suite.carrier_name,
                "tracking_pro_number": suite.tracking_pro_number,
                "trailer_number": suite.trailer_number,
                "seal_number": suite.seal_number,
                "pallet_count": suite.pallet_count,
                "container_count": suite.container_count,
                "gross_weight_kg": gross_kg,
            },
        },
        "line_items": [
            {
                "product_description": suite.product.description,
                "lot_serial_number": suite.lot_serial_number,
                "received_qty_kg": suite.received_quantity_kg,
                "container_count": suite.container_count,
                "manufacturing_date": suite.manufacturing_date,
                "expiration_date": suite.expiration_date,
            }
        ],
        "analytical_results": [
            {
                "step_nbr": tr.step_nbr,
                "test_id": tr.test_id,
                "analyte_name": tr.analyte_name,
                "test_method": tr.test_method,
                "specification_text": tr.specification_text,
                "observed_value_text": tr.observed_value_text,
                "numeric_value": tr.numeric_value,
                "uom": tr.uom,
                "passed": tr.passed,
                "criticality": tr.criticality,
                "regional_term": tr.regional_analyte_name,
                "regional_uom": tr.regional_uom,
            }
            for tr in suite.test_results
        ],
        "failure_reasons": suite.failure_reasons,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)
    return out_path


@click.group(
    cls=AgentHelpGroup,
    invoke_without_command=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "max_content_width": 100,
    },
    epilog=AGENT_HELP_EPILOG,
)
@click.version_option(version="0.1.0", prog_name="docgen")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Inbound Shipping Document PDF Generator CLI (LLM-agent help entrypoint).

    Generates Certificate of Analysis (CoA), Supplier Packing Slip, and
    Bill of Lading (BOL) documents for dock-to-stock ERP compliance testing
    (Health Canada GMP GUI-0001/0158, CFIA SFCR, USP / Ph. Eur. lab variants).

    \b
    AGENT CONTRACT
      • Bare `docgen` (no subcommand) prints this FULL help and exits 0.
      • `docgen --help` / `-h` prints the same FULL help (all subcommands expanded).
      • Prefer `uv run docgen ...` or `uv run python -m docgen ...` (after `uv sync`).
      • Never hardcode vendor/product IDs — resolve via list-master-data or
        acumatica/master_data/*.json.
      • PDFs are external-facing (zero ERP leakage). Use MANIFEST_*.json for
        ground-truth ERP association keys.
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help(), color=ctx.color)


@cli.command("generate-suite")
@click.option(
    "--po-json",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Optional path to Acumatica Purchase Order JSON file.",
)
@click.option(
    "--inventory-id",
    "-i",
    type=str,
    help="Acumatica Inventory Item ID (e.g., RAW-ECH-EXT4, RAW-ASH-EXT5).",
)
@click.option(
    "--vendor-id",
    "-v",
    type=str,
    help="Acumatica Vendor ID (e.g., VEND-NORTH-BIO, VEND-ALPINE-EXT).",
)
@click.option(
    "--lot-nbr",
    "-l",
    type=str,
    help="Explicit Lot/Batch number (e.g., LOT-EC2603-01A).",
)
@click.option(
    "--po-nbr",
    "-p",
    type=str,
    help="Acumatica Purchase Order number (e.g., PO-04819).",
)
@click.option(
    "--receipt-nbr",
    "-r",
    type=str,
    help="Acumatica POReceipt number (e.g., PR-2026-00102).",
)
@click.option(
    "--status",
    "-s",
    type=click.Choice(["pass", "fail"], case_sensitive=False),
    default="pass",
    show_default=True,
    help="Simulated quality outcome for CoA testing.",
)
@click.option(
    "--outdir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output/shipping_docs"),
    show_default=True,
    help="Output directory where generated PDFs will be written.",
)
@click.option(
    "--emit-json/--no-emit-json",
    default=True,
    show_default=True,
    help="Also emit structured manifest JSON alongside PDFs.",
)
def generate_suite_cmd(
    po_json: Path | None,
    inventory_id: str | None,
    vendor_id: str | None,
    lot_nbr: str | None,
    po_nbr: str | None,
    receipt_nbr: str | None,
    status: str,
    outdir: Path,
    emit_json: bool,
) -> None:
    """Generate all 3 mandatory dock receiving PDFs (CoA, Packing Slip, BOL).

    Primary agent entrypoint for a single inbound shipment suite. Writes CoA,
    Packing Slip, BOL, and (by default) MANIFEST JSON under --outdir.

    Provide either --po-json OR --inventory-id (and optional --vendor-id).
    Omitting both picks a random product from master data.
    """
    registry = MasterDataRegistry()

    if po_json is not None:
        with po_json.open("r", encoding="utf-8") as f:
            po_data = json.load(f)
        suite = build_shipment_suite_from_po_data(
            registry=registry,
            po_data=po_data,
            force_status=status.upper(),
            lot_nbr=lot_nbr,
        )
    else:
        suite = build_synthetic_shipment_suite(
            registry=registry,
            inventory_id=inventory_id,
            vendor_id=vendor_id,
            force_status=status.upper(),
            lot_nbr=lot_nbr,
            po_nbr=po_nbr,
            receipt_nbr=receipt_nbr,
        )

    prefix = f"{suite.product.inventory_id}_{suite.lot_serial_number}"
    coa_path = outdir / f"COA_{prefix}.pdf"
    pack_path = outdir / f"PACKING_SLIP_{prefix}.pdf"
    bol_path = outdir / f"BOL_{prefix}.pdf"

    click.echo(
        f"Generating 3-document suite for {suite.product.inventory_id} "
        f"(Lot: {suite.lot_serial_number})..."
    )
    generate_coa_pdf(suite, coa_path)
    generate_packing_slip_pdf(suite, pack_path)
    generate_bol_pdf(suite, bol_path)

    click.echo(f"  [1/3] CoA PDF:          {coa_path}")
    click.echo(f"  [2/3] Packing Slip PDF: {pack_path}")
    click.echo(f"  [3/3] BOL PDF:          {bol_path}")

    if emit_json:
        json_path = outdir / f"MANIFEST_{prefix}.json"
        emit_manifest_json(suite, json_path)
        click.echo(f"  [+]   Manifest JSON:    {json_path}")

    status_color = "green" if suite.overall_status == "PASS" else "red"
    click.secho(
        f"Generated document suite [{suite.overall_status}]",
        fg=status_color,
        bold=True,
    )


@cli.command("from-po")
@click.option(
    "--po-json",
    "-p",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Path to Acumatica Purchase Order JSON file.",
)
@click.option(
    "--lot-nbr",
    "-l",
    type=str,
    help="Explicit Lot/Batch number (e.g., LOT-EC2603-01A).",
)
@click.option(
    "--status",
    "-s",
    type=click.Choice(["pass", "fail"], case_sensitive=False),
    default="pass",
    show_default=True,
    help="Simulated quality outcome for CoA testing.",
)
@click.option(
    "--outdir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output/shipping_docs"),
    show_default=True,
    help="Output directory where generated PDFs will be written.",
)
@click.option(
    "--emit-json/--no-emit-json",
    default=True,
    show_default=True,
    help="Also emit structured manifest JSON alongside PDFs.",
)
def from_po_cmd(
    po_json: Path,
    lot_nbr: str | None,
    status: str,
    outdir: Path,
    emit_json: bool,
) -> None:
    """Generate 3-document suite from an Acumatica Purchase Order JSON file.

    Dedicated PO path (equivalent to generate-suite --po-json). Reads the first
    PO line for inventory_id + qty; maps vendor_id; synthesizes external docs
    that match the open PO without leaking ERP IDs onto the PDFs.
    """
    with po_json.open("r", encoding="utf-8") as f:
        po_data = json.load(f)

    registry = MasterDataRegistry()
    suite = build_shipment_suite_from_po_data(
        registry=registry,
        po_data=po_data,
        force_status=status.upper(),
        lot_nbr=lot_nbr,
    )

    prefix = f"{suite.product.inventory_id}_{suite.lot_serial_number}"
    coa_path = outdir / f"COA_{prefix}.pdf"
    pack_path = outdir / f"PACKING_SLIP_{prefix}.pdf"
    bol_path = outdir / f"BOL_{prefix}.pdf"

    click.echo(
        f"Generating 3-document suite from PO {suite.purchase_order_number} for "
        f"{suite.product.inventory_id} (Lot: {suite.lot_serial_number})..."
    )
    generate_coa_pdf(suite, coa_path)
    generate_packing_slip_pdf(suite, pack_path)
    generate_bol_pdf(suite, bol_path)

    click.echo(f"  [1/3] CoA PDF:          {coa_path}")
    click.echo(f"  [2/3] Packing Slip PDF: {pack_path}")
    click.echo(f"  [3/3] BOL PDF:          {bol_path}")

    if emit_json:
        json_path = outdir / f"MANIFEST_{prefix}.json"
        emit_manifest_json(suite, json_path)
        click.echo(f"  [+]   Manifest JSON:    {json_path}")

    status_color = "green" if suite.overall_status == "PASS" else "red"
    click.secho(
        f"Generated document suite [{suite.overall_status}]",
        fg=status_color,
        bold=True,
    )


@cli.command("generate-coa")
@click.option("--inventory-id", "-i", type=str, help="Inventory Item ID.")
@click.option("--vendor-id", "-v", type=str, help="Vendor ID.")
@click.option("--lot-nbr", "-l", type=str, help="Lot number.")
@click.option(
    "--status",
    "-s",
    type=click.Choice(["pass", "fail"], case_sensitive=False),
    default="pass",
    show_default=True,
)
@click.option(
    "--outdir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output/coa"),
    show_default=True,
)
def generate_coa_cmd(
    inventory_id: str | None,
    vendor_id: str | None,
    lot_nbr: str | None,
    status: str,
    outdir: Path,
) -> None:
    """Generate standalone Certificate of Analysis (CoA) PDF.

    Lab header, units, and bilingual analyte terms adapt to the product's
    assigned primary lab. Use --status fail to force an out-of-spec CoA.
    Does not emit Packing Slip, BOL, or MANIFEST JSON.
    """
    registry = MasterDataRegistry()
    suite = build_synthetic_shipment_suite(
        registry=registry,
        inventory_id=inventory_id,
        vendor_id=vendor_id,
        force_status=status.upper(),
        lot_nbr=lot_nbr,
    )
    coa_path = (
        outdir / f"COA_{suite.product.inventory_id}_{suite.lot_serial_number}.pdf"
    )
    generate_coa_pdf(suite, coa_path)
    click.secho(f"Generated CoA: {coa_path} [{suite.overall_status}]", fg="green")


@cli.command("generate-packing-slip")
@click.option("--inventory-id", "-i", type=str, help="Inventory Item ID.")
@click.option("--vendor-id", "-v", type=str, help="Vendor ID.")
@click.option("--lot-nbr", "-l", type=str, help="Lot number.")
@click.option(
    "--outdir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output/packing_slips"),
    show_default=True,
)
def generate_packing_slip_cmd(
    inventory_id: str | None,
    vendor_id: str | None,
    lot_nbr: str | None,
    outdir: Path,
) -> None:
    """Generate standalone Supplier Packing Slip PDF.

    External delivery note with commercial product name, lot, containers,
    net weight, and storage notes. No CoA / BOL / MANIFEST JSON.
    """
    registry = MasterDataRegistry()
    suite = build_synthetic_shipment_suite(
        registry=registry,
        inventory_id=inventory_id,
        vendor_id=vendor_id,
        lot_nbr=lot_nbr,
    )
    pack_path = (
        outdir
        / f"PACKING_SLIP_{suite.product.inventory_id}_{suite.lot_serial_number}.pdf"
    )
    generate_packing_slip_pdf(suite, pack_path)
    click.secho(f"Generated Packing Slip: {pack_path}", fg="green")


@cli.command("generate-bol")
@click.option("--inventory-id", "-i", type=str, help="Inventory Item ID.")
@click.option("--vendor-id", "-v", type=str, help="Vendor ID.")
@click.option("--lot-nbr", "-l", type=str, help="Lot number.")
@click.option(
    "--outdir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output/bol"),
    show_default=True,
)
def generate_bol_cmd(
    inventory_id: str | None,
    vendor_id: str | None,
    lot_nbr: str | None,
    outdir: Path,
) -> None:
    """Generate standalone Carrier Bill of Lading (BOL) PDF.

    Carrier PRO#, trailer/seal, pallet/container counts, and freight gross
    weight. Carrier is resolved from the vendor's preferred carrier map.
    No CoA / Packing Slip / MANIFEST JSON.
    """
    registry = MasterDataRegistry()
    suite = build_synthetic_shipment_suite(
        registry=registry,
        inventory_id=inventory_id,
        vendor_id=vendor_id,
        lot_nbr=lot_nbr,
    )
    bol_path = (
        outdir / f"BOL_{suite.product.inventory_id}_{suite.lot_serial_number}.pdf"
    )
    generate_bol_pdf(suite, bol_path)
    click.secho(f"Generated BOL: {bol_path}", fg="green")


@cli.command("batch")
@click.option(
    "--count",
    "-c",
    type=int,
    default=5,
    show_default=True,
    help="Number of document suites to generate.",
)
@click.option(
    "--outdir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output/batch_shipping_docs"),
    show_default=True,
    help="Output directory for generated batch files.",
)
@click.option(
    "--include-failures/--all-pass",
    default=True,
    show_default=True,
    help="Include out-of-specification failure cases in the batch.",
)
@click.option(
    "--emit-json/--no-emit-json",
    default=True,
    show_default=True,
    help="Also emit structured manifest JSON alongside PDFs.",
)
def batch_cmd(
    count: int, outdir: Path, include_failures: bool, emit_json: bool
) -> None:
    """Generate a batch of 3-document suites covering multiple vendors & labs.

    Cycles products in master-data order. With --include-failures (default),
    odd suites are FAIL and even suites are PASS. Filenames are prefixed
    suite_<n>_<vendor_id>_<inventory_id>_<lot>.
    """
    registry = MasterDataRegistry()
    products_list = list(registry.products.values())

    click.echo(f"Generating batch of {count} document suites in {outdir}...")
    outdir.mkdir(parents=True, exist_ok=True)

    for i in range(count):
        prod = products_list[i % len(products_list)]
        force_status = None
        if include_failures:
            force_status = "FAIL" if (i % 2 == 1) else "PASS"
        else:
            force_status = "PASS"

        suite = build_synthetic_shipment_suite(
            registry=registry,
            inventory_id=prod.inventory_id,
            force_status=force_status,
        )

        p_id = suite.product.inventory_id
        v_id = suite.vendor.vendor_id
        lot_sn = suite.lot_serial_number
        prefix = f"suite_{i + 1}_{v_id}_{p_id}_{lot_sn}"

        coa_path = outdir / f"COA_{prefix}.pdf"
        pack_path = outdir / f"PACKING_SLIP_{prefix}.pdf"
        bol_path = outdir / f"BOL_{prefix}.pdf"

        generate_coa_pdf(suite, coa_path)
        generate_packing_slip_pdf(suite, pack_path)
        generate_bol_pdf(suite, bol_path)

        if emit_json:
            emit_manifest_json(suite, outdir / f"MANIFEST_{prefix}.json")

        status_tag = f"[{suite.overall_status}]"
        fg_col = "green" if suite.overall_status == "PASS" else "red"
        click.secho(
            f"  • Suite {i + 1}/{count}: {p_id} -> "
            f"{status_tag} ({suite.test_lab.lab_id})",
            fg=fg_col,
        )

    click.secho(
        f"Successfully generated {count} complete document suites in {outdir}",
        fg="green",
        bold=True,
    )


@cli.command("list-master-data")
def list_master_data_cmd() -> None:
    """List available vendors, testing labs, and products.

    Agent discovery command. Print vendor_id, lab_id, and inventory_id values
    that are safe to pass to generate-* / batch / from-po. Do not invent IDs.
    """
    registry = MasterDataRegistry()
    click.secho("=== REGISTERED QUALIFIED VENDORS ===", bold=True, fg="blue")
    for v in registry.vendors.values():
        click.echo(
            f"  • {v.vendor_id:18} | {v.legal_name:40} | "
            f"{v.country:10} | Lab: {v.primary_preferred_lab_id}"
        )

    click.secho("\n=== ACCREDITED TESTING LABORATORIES ===", bold=True, fg="blue")
    for lab in registry.test_labs.values():
        click.echo(
            f"  • {lab.lab_id:20} | {lab.lab_name:45} | "
            f"Standard: {lab.document_standard}"
        )

    click.secho("\n=== RAW MATERIAL PRODUCTS ===", bold=True, fg="blue")
    for p in registry.products.values():
        click.echo(
            f"  • {p.inventory_id:15} | {p.vendor_id:18} | {p.description[:45]}..."
        )


if __name__ == "__main__":
    cli()
