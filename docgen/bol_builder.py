"""Carrier Bill of Lading (BOL) / Delivery Manifest PDF Builder."""

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


def generate_bol_pdf(suite: InboundShipmentSuite, output_path: str | Path) -> Path:
    """Generates a Bill of Lading (BOL) PDF for the given shipment suite."""
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

    # 1. Header Banner: Freight Carrier & Logistics Identification
    carrier_title = f"{suite.carrier_name.upper()}"
    carrier_sub = "STANDARD BILL OF LADING / STRAIGHT CONSIGNMENT MANIFEST"
    carrier_meta = (
        f"<b>PRO / Tracking Nbr:</b> {suite.tracking_pro_number}<br/>"
        f"<b>BOL Number:</b> BOL-{suite.manifest_id[4:]}<br/>"
        f"<b>Date:</b> {suite.manufacturing_date}"
    )

    header_table_data = [
        [
            Paragraph(
                f"<b>{carrier_title}</b><br/>"
                f"<font size=8 color='#1E3D59'>{carrier_sub}</font>",
                styles["DocTitle"],
            ),
            Paragraph(carrier_meta, styles["HeaderMeta"]),
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

    # 2. Shipper, Consignee & Carrier Equipment Block
    v_contact = (
        f"Contact: {suite.vendor.primary_contact_name} "
        f"({suite.vendor.primary_contact_phone})"
    )
    shipper_info = [
        Paragraph("<b>1. SHIP FROM (SHIPPER):</b>", styles["MetaLabel"]),
        Paragraph(suite.vendor.legal_name, styles["MetaValue"]),
        Paragraph(suite.vendor.headquarters_address, styles["MetaValue"]),
        Paragraph(
            f"{suite.vendor.city_region}, {suite.vendor.country}",
            styles["MetaValue"],
        ),
        Paragraph(v_contact, styles["MetaValue"]),
    ]

    consignee_info = [
        Paragraph("<b>2. SHIP TO (CONSIGNEE):</b>", styles["MetaLabel"]),
        Paragraph("CanNordic BioNutra Inc.", styles["MetaValue"]),
        Paragraph("Mississauga Distribution Center & Warehouse", styles["MetaValue"]),
        Paragraph("2450 Meadowpine Blvd, Receiving Gate 3", styles["MetaValue"]),
        Paragraph("Mississauga, ON L5N 6S2 Canada", styles["MetaValue"]),
    ]

    freight_routing_info = [
        Paragraph("<b>3. FREIGHT & EQUIPMENT:</b>", styles["MetaLabel"]),
        Paragraph(f"<b>Carrier:</b> {suite.carrier_name}", styles["MetaValue"]),
        Paragraph(f"<b>Trailer Nbr:</b> {suite.trailer_number}", styles["MetaValue"]),
        Paragraph(
            f"<b>Seal Nbr:</b> {suite.seal_number} (High Security)",
            styles["MetaValue"],
        ),
        Paragraph(
            f"<b>Acumatica PO:</b> {suite.purchase_order_number}",
            styles["MetaValue"],
        ),
        Paragraph("<b>Payment Terms:</b> Prepaid / 3rd Party", styles["MetaValue"]),
    ]

    routing_table_data = [
        [
            Table([[p] for p in shipper_info], colWidths=[175]),
            Table([[p] for p in consignee_info], colWidths=[175]),
            Table([[p] for p in freight_routing_info], colWidths=[170]),
        ]
    ]
    routing_table = Table(routing_table_data, colWidths=[180, 180, 180])
    routing_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(routing_table)
    story.append(Spacer(1, 10))

    # 3. Freight Commodity Description Table
    story.append(
        Paragraph(
            "FREIGHT COMMODITY & HANDLING UNIT SPECIFICATION",
            styles["SectionHeader"],
        )
    )
    story.append(Spacer(1, 3))

    tare_per_drum = 2.5
    total_net = suite.received_quantity_kg
    total_gross_kg = (
        total_net
        + (suite.container_count * tare_per_drum)
        + (suite.pallet_count * 20.0)
    )
    total_gross_lbs = total_gross_kg * 2.20462

    freight_headers = [
        Paragraph("Handling Units", styles["TableTH"]),
        Paragraph("Pkg Type & Qty", styles["TableTH"]),
        Paragraph("Commodity Description & Shipping Marks", styles["TableTH"]),
        Paragraph("NMFC / Class", styles["TableTH"]),
        Paragraph("Gross Weight (KG)", styles["TableTH"]),
        Paragraph("Gross Weight (LBS)", styles["TableTH"]),
    ]

    p_id = suite.product.inventory_id
    p_lot = suite.lot_serial_number
    item_desc = (
        f"<b>{suite.product.description}</b><br/>"
        f"<font size=6.5 color='#333333'>Item ID: {p_id} | Lot: {p_lot}</font><br/>"
        f"<font size=6 color='#555555'>Non-Hazardous Dietary / Food Supplement</font>"
    )

    freight_row = [
        Paragraph(f"<b>{suite.pallet_count} Pallet(s)</b>", styles["TableTDCenter"]),
        Paragraph(f"{suite.container_count} Fiber Drums", styles["TableTDCenter"]),
        Paragraph(item_desc, styles["TableTD"]),
        Paragraph("NMFC 59380-02<br/>Class 70", styles["TableTDCenter"]),
        Paragraph(f"<b>{total_gross_kg:.1f}</b>", styles["TableTDCenter"]),
        Paragraph(f"{total_gross_lbs:.1f}", styles["TableTDCenter"]),
    ]

    freight_total_row = [
        Paragraph(
            f"<b>TOTAL: {suite.pallet_count} Skid(s)</b>",
            styles["TableTDCenter"],
        ),
        Paragraph(f"<b>{suite.container_count} Drums</b>", styles["TableTDCenter"]),
        Paragraph("<b>GRAND TOTALS</b>", styles["TableTD"]),
        Paragraph("", styles["TableTD"]),
        Paragraph(f"<b>{total_gross_kg:.1f} KG</b>", styles["TableTDCenter"]),
        Paragraph(f"{total_gross_lbs:.1f} LBS", styles["TableTDCenter"]),
    ]

    freight_table_data = [freight_headers, freight_row, freight_total_row]
    freight_table = Table(freight_table_data, colWidths=[75, 75, 200, 70, 60, 60])
    freight_table.setStyle(
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
    story.append(freight_table)
    story.append(Spacer(1, 10))

    # 4. Special Handling & Carrier Instructions
    story.append(
        Paragraph(
            "SPECIAL INSTRUCTIONS & TEMPERATURE CONTROL",
            styles["SectionHeader"],
        )
    )
    story.append(Spacer(1, 3))

    temp_directive = (
        "<b>CLIMATE CONTROL MANDATE:</b> Maintain transit temperature in "
        "compliance with product profile. Do not double stack skids. Protect "
        "from freezing and direct sunlight. Tamper seal must remain intact."
    )
    haz_declaration = (
        "<b>CARRIER DECLARATION:</b> This is to certify that the above named "
        "materials are properly classified, packaged, marked, and labeled per "
        "regulations of Transport Canada TDG and US DOT."
    )

    special_data = [
        [
            Paragraph(
                f"{temp_directive}<br/><br/>{haz_declaration}",
                styles["CalloutText"],
            ),
        ]
    ]
    spec_table = Table(special_data, colWidths=[540])
    spec_table.setStyle(
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
    story.append(spec_table)
    story.append(Spacer(1, 10))

    # 5. Chain of Custody Signatures Table (Shipper, Driver, Consignee)
    driver_info = (
        f"<b>Carrier:</b> {suite.carrier_name}<br/>"
        "<b>Driver Name:</b> R. Kowalski<br/>"
        f"<b>Trailer:</b> {suite.trailer_number} | "
        f"<b>Seal:</b> {suite.seal_number}<br/>"
        "<i>Received freight in sealed unit</i>"
    )

    sign_data = [
        [
            Paragraph("<b>SHIPPER CERTIFICATION</b>", styles["SectionHeader"]),
            Paragraph("<b>CARRIER DRIVER ACCEPTANCE</b>", styles["SectionHeader"]),
            Paragraph("<b>CONSIGNEE RECEIPT & SEAL</b>", styles["SectionHeader"]),
        ],
        [
            Paragraph(
                f"<b>Shipper:</b> {suite.vendor.legal_name}<br/>"
                f"<b>Signatory:</b> {suite.vendor.primary_contact_name}<br/>"
                f"<b>Date:</b> {suite.manufacturing_date}<br/>"
                "<i>Freight tendered in good order</i>",
                styles["SignatureLabel"],
            ),
            Paragraph(
                driver_info,
                styles["SignatureLabel"],
            ),
            Paragraph(
                "<b>Consignee:</b> CanNordic BioNutra Inc.<br/>"
                "<b>Receiver:</b> Devon Singh<br/>"
                f"<b>POReceipt:</b> {suite.receipt_number}<br/>"
                "<b>Seal Verified Intact:</b> [ √ ] Yes",
                styles["SignatureLabel"],
            ),
        ],
    ]

    sign_table = Table(sign_data, colWidths=[180, 180, 180])
    sign_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BG_ALT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.75, NAVY_PRIMARY),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    story.append(KeepTogether([sign_table]))

    doc.build(story, canvasmaker=NumberedCanvas)  # type: ignore
    return out_file
