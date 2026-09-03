"""Supplier Packing Slip / Delivery Note PDF Builder."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from docgen.models import InboundShipmentSuite
from docgen.styles import (
    BG_ALT_GRAY,
    BG_LIGHT_GRAY,
    BORDER_GRAY,
    NAVY_PRIMARY,
    NumberedCanvas,
    get_document_styles,
)


def generate_packing_slip_pdf(
    suite: InboundShipmentSuite, output_path: str | Path
) -> Path:
    """Generates a Supplier Packing Slip PDF for the given shipment suite."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(out_file),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=40,
    )

    styles = get_document_styles()
    story: list[object] = []

    # 1. Header Banner: Supplier / Vendor Info
    vendor = suite.vendor
    vendor_title = f"{vendor.legal_name.upper()}"
    vendor_sub = (
        f"QUALITY ASSURED FACILITY | GMP STATUS: {vendor.gmp_certification_status}"
    )
    vendor_addr = (
        f"{vendor.headquarters_address}<br/>"
        f"{vendor.city_region}, {vendor.country}<br/>"
        f"<b>Sales & Dispatch:</b> {vendor.primary_contact_name} "
        f"({vendor.primary_contact_email})"
    )

    header_table_data = [
        [
            Paragraph(
                f"<b>{vendor_title}</b><br/>"
                f"<font size=8 color='#1E3D59'>{vendor_sub}</font>",
                styles["DocTitle"],
            ),
            Paragraph(vendor_addr, styles["HeaderMeta"]),
        ]
    ]

    header_table = Table(header_table_data, colWidths=[330, 210])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(header_table)
    story.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=NAVY_PRIMARY,
            spaceBefore=4,
            spaceAfter=8,
        )
    )

    # 2. Document Title & Order Metadata
    sub_title = "PACKING SLIP / DELIVERY NOTE / BORDEREAU DE LIVRAISON"
    story.append(Paragraph(sub_title, styles["DocSubtitle"]))
    story.append(Spacer(1, 4))

    slip_nbr = f"DN-{suite.manifest_id[4:]}"
    order_ref = f"ORD-{suite.manifest_id[4:]}"
    meta_col1 = [
        Paragraph(f"<b>Delivery Note Nbr:</b> {slip_nbr}", styles["MetaValue"]),
        Paragraph(
            f"<b>Supplier Order Ref:</b> {order_ref}",
            styles["MetaValue"],
        ),
        Paragraph(f"<b>Ship Date:</b> {suite.manufacturing_date}", styles["MetaValue"]),
        Paragraph(
            f"<b>Ship Via / Carrier:</b> {suite.carrier_name}",
            styles["MetaValue"],
        ),
    ]
    meta_col2 = [
        Paragraph("<b>Ship To (Consignee):</b>", styles["MetaLabel"]),
        Paragraph("CanNordic BioNutra Inc. - Receiving Dock", styles["MetaValue"]),
        Paragraph("2450 Meadowpine Blvd, Warehouse Gate 3", styles["MetaValue"]),
        Paragraph("Mississauga, ON L5N 6S2 Canada", styles["MetaValue"]),
    ]

    meta_table_data = [
        [
            Table([[p] for p in meta_col1], colWidths=[265]),
            Table([[p] for p in meta_col2], colWidths=[265]),
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[270, 270])
    meta_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 3. Line Items & Lot Allocation Table
    story.append(
        Paragraph("SHIPPED LINE ITEMS & LOT ALLOCATION", styles["SectionHeader"])
    )
    story.append(Spacer(1, 3))

    tare_per_drum = 2.5  # kg per drum
    total_net = suite.received_quantity_kg
    total_gross = (
        total_net
        + (suite.container_count * tare_per_drum)
        + (suite.pallet_count * 20.0)
    )

    item_headers = [
        Paragraph("Line", styles["TableTH"]),
        Paragraph("Description of Goods", styles["TableTH"]),
        Paragraph("Lot / Batch Nbr", styles["TableTH"]),
        Paragraph("Expiry Date", styles["TableTH"]),
        Paragraph("Packaging / Units", styles["TableTH"]),
        Paragraph("Net Qty", styles["TableTH"]),
        Paragraph("Gross Qty", styles["TableTH"]),
    ]

    item_desc = f"<b>{suite.product.description}</b>"
    if suite.product.botanical_source:
        item_desc += (
            f"<br/><font size=6.5 color='#333333'>"
            f"<i>{suite.product.botanical_source}</i></font>"
        )
    pkg_desc = (
        f"{suite.container_count} x Fiber Drums<br/>"
        f"<font size=6 color='#555555'>({suite.pallet_count} Pallets)</font>"
    )

    item_row = [
        Paragraph("01", styles["TableTDCenter"]),
        Paragraph(item_desc, styles["TableTD"]),
        Paragraph(f"<b>{suite.lot_serial_number}</b>", styles["TableTDCenter"]),
        Paragraph(suite.expiration_date, styles["TableTDCenter"]),
        Paragraph(pkg_desc, styles["TableTDCenter"]),
        Paragraph(f"<b>{total_net:.1f} KG</b>", styles["TableTDCenter"]),
        Paragraph(f"{total_gross:.1f} KG", styles["TableTDCenter"]),
    ]

    total_row = [
        Paragraph("", styles["TableTD"]),
        Paragraph("<b>SHIPMENT TOTALS:</b>", styles["TableTD"]),
        Paragraph("", styles["TableTD"]),
        Paragraph("", styles["TableTD"]),
        Paragraph(f"<b>{suite.container_count} Drums</b>", styles["TableTDCenter"]),
        Paragraph(f"<b>{total_net:.1f} KG</b>", styles["TableTDCenter"]),
        Paragraph(f"<b>{total_gross:.1f} KG</b>", styles["TableTDCenter"]),
    ]

    items_table_data = [item_headers, item_row, total_row]
    items_table = Table(items_table_data, colWidths=[30, 160, 95, 65, 80, 55, 55])
    items_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY_PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("BACKGROUND", (0, 2), (-1, 2), BG_ALT_GRAY),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(items_table)
    story.append(Spacer(1, 10))

    # 4. Storage Directives & Regulatory Compliance Card
    story.append(
        Paragraph(
            "STORAGE DIRECTIVES & HANDLING INSTRUCTIONS",
            styles["SectionHeader"],
        )
    )
    story.append(Spacer(1, 3))

    fsa_ref = vendor.foreign_site_annex_ref or "Canadian Qualified Site"
    fsa_info = f"<b>Regulatory Export / Annex Compliance:</b> {fsa_ref}"
    storage_info = f"<b>Prescribed Storage:</b> {suite.storage_conditions}"
    handling_info = (
        "<b>Handling Directives:</b> Store in original sealed containers in a cool, "
        "dry warehouse. Protect from light, moisture, and extreme temperature. "
        "Food grade / dietary supplement raw material."
    )

    compliance_data = [
        [
            Paragraph(
                f"{storage_info}<br/>{handling_info}<br/>{fsa_info}",
                styles["CalloutText"],
            ),
        ]
    ]
    comp_table = Table(compliance_data, colWidths=[540])
    comp_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(comp_table)
    story.append(Spacer(1, 10))

    # 5. Receiving Dock Checklist (Consignee Dock Verification)
    c_count = suite.container_count
    lot_sn = suite.lot_serial_number
    checklist_p1 = (
        "[ &nbsp; ] Physical Drum / Container Seal Integrity Verified<br/>"
        f"[ &nbsp; ] Container Count Matches Packing Slip (<b>{c_count} Drums</b>)<br/>"
        f"[ &nbsp; ] Physical Lot Tag Label Matches (<b>{lot_sn}</b>)<br/>"
        "[ &nbsp; ] Attached Certificate of Analysis (CoA) Present in Pouch"
    )
    checklist_p2 = (
        "<b>Received By (Dock Clerk):</b> ___________________________<br/>"
        "<b>Date Received:</b> ___________________________<br/>"
        "<b>Dock Triage:</b> [ &nbsp; ] Staged for Inspection &nbsp; "
        "[ &nbsp; ] Hold / Discrepancy<br/>"
        "<b>Physical Placard:</b> Inbound Quarantine Placard Affixed"
    )

    checklist_data = [
        [
            Paragraph(
                "<b>CONSIGNEE RECEIVING VERIFICATION (DOCK USE ONLY)</b>",
                styles["DocSubtitle"],
            ),
            Paragraph(
                "<b>Status:</b> INBOUND DOCK RECEIPT",
                styles["MetaValue"],
            ),
        ],
        [
            Paragraph(checklist_p1, styles["CalloutText"]),
            Paragraph(checklist_p2, styles["CalloutText"]),
        ],
    ]

    check_table = Table(checklist_data, colWidths=[290, 250])
    check_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BG_ALT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.75, NAVY_PRIMARY),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(KeepTogether([check_table]))

    doc.build(story, canvasmaker=NumberedCanvas)  # type: ignore
    return out_file
