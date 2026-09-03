"""Certificate of Analysis (CoA) PDF Builder."""

from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
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
    ACCENT_GREEN,
    ACCENT_GREEN_BG,
    ALERT_RED,
    ALERT_RED_BG,
    BG_ALT_GRAY,
    BG_LIGHT_GRAY,
    BORDER_GRAY,
    NAVY_PRIMARY,
    NumberedCanvas,
    get_document_styles,
)


def generate_coa_pdf(suite: InboundShipmentSuite, output_path: str | Path) -> Path:
    """Generates a Certificate of Analysis PDF for the shipment suite."""
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
    story: list[Any] = []

    # 1. Header Banner: Laboratory Information & Accreditation
    lab = suite.test_lab
    lab_title = f"{lab.lab_name.upper()}"
    lab_sub = (
        f"{lab.document_standard} | ACCREDITATION: "
        f"{lab.accreditation_number} ({lab.accreditation_body})"
    )
    lab_addr = (
        f"{lab.address}, {lab.city_region}, {lab.country}<br/>"
        f"<b>Standard:</b> {lab.document_type_bilingual}"
    )

    header_table_data = [
        [
            Paragraph(
                f"<b>{lab_title}</b><br/><font size=8 color='#1E3D59'>{lab_sub}</font>",
                styles["DocTitle"],
            ),
            Paragraph(lab_addr, styles["HeaderMeta"]),
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

    # 2. Document Title & CoA Metadata Card
    doc_title = f"{lab.document_type_bilingual.upper()} / CERTIFICATE OF ANALYSIS"
    story.append(Paragraph(doc_title, styles["DocSubtitle"]))
    story.append(Spacer(1, 4))

    meta_col1 = [
        Paragraph(
            f"<b>Certificate Nbr:</b> COA-{suite.manifest_id[4:]}",
            styles["MetaValue"],
        ),
        Paragraph(
            f"<b>Product Description:</b> {suite.product.description}",
            styles["MetaValue"],
        ),
        Paragraph(
            f"<b>Manufacturer / Supplier:</b> {suite.vendor.legal_name}",
            styles["MetaValue"],
        ),
    ]
    if suite.product.botanical_source:
        meta_col1.append(
            Paragraph(
                f"<b>Botanical Source:</b> {suite.product.botanical_source}",
                styles["MetaValue"],
            )
        )

    sample_id = f"SMP-{suite.manifest_id[4:]}"
    meta_col2 = [
        Paragraph(
            f"<b>Lot / Batch Nbr:</b> {suite.lot_serial_number}",
            styles["MetaValue"],
        ),
        Paragraph(
            f"<b>Manufacture Date:</b> {suite.manufacturing_date}",
            styles["MetaValue"],
        ),
        Paragraph(
            f"<b>Retest / Expiry:</b> {suite.expiration_date}",
            styles["MetaValue"],
        ),
        Paragraph(
            f"<b>Batch Quantity:</b> {suite.received_quantity_kg:.1f} KG "
            f"({suite.container_count} Drums)",
            styles["MetaValue"],
        ),
        Paragraph(
            f"<b>Laboratory Sample ID:</b> {sample_id}",
            styles["MetaValue"],
        ),
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

    # 3. Analytical Test Results Table
    story.append(
        Paragraph(
            "ANALYTICAL TEST RESULTS & SPECIFICATION VERIFICATION",
            styles["SectionHeader"],
        )
    )
    story.append(Spacer(1, 3))

    test_headers: list[Any] = [
        Paragraph("Step", styles["TableTH"]),
        Paragraph("Test Parameter / Analyte", styles["TableTH"]),
        Paragraph("Test Method", styles["TableTH"]),
        Paragraph("Specification Limit", styles["TableTH"]),
        Paragraph("Observed Value", styles["TableTH"]),
        Paragraph("Result", styles["TableTH"]),
    ]

    test_rows: list[list[Any]] = [test_headers]

    for _idx, tr in enumerate(suite.test_results):
        badge_style = styles["BadgePass"] if tr.passed else styles["BadgeFail"]
        badge_text = "PASS / CONFORMS" if tr.passed else "OUT OF SPEC"

        analyte_display = tr.analyte_name
        if tr.regional_analyte_name:
            analyte_display = (
                f"{tr.analyte_name}<br/>"
                f"<font size=6 color='#555555'><i>{tr.regional_analyte_name}</i></font>"
            )

        obs_display = tr.observed_value_text
        if tr.regional_value_text and tr.regional_value_text != tr.observed_value_text:
            obs_display = (
                f"{tr.observed_value_text}<br/>"
                f"<font size=6 color='#0F2942'>({tr.regional_value_text})</font>"
            )

        row: list[Any] = [
            Paragraph(str(tr.step_nbr), styles["TableTDCenter"]),
            Paragraph(analyte_display, styles["TableTD"]),
            Paragraph(tr.test_method, styles["TableTD"]),
            Paragraph(tr.specification_text, styles["TableTD"]),
            Paragraph(obs_display, styles["TableTDCenter"]),
            Paragraph(badge_text, badge_style),
        ]
        test_rows.append(row)

    # Column widths total 540 pt (8.5in - 2*0.5in = 7.5in = 540pt)
    test_table = Table(
        test_rows,
        colWidths=[25, 145, 120, 110, 80, 60],
        repeatRows=1,
    )

    t_style: list[Any] = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]

    for i in range(1, len(test_rows)):
        bg_col = BG_ALT_GRAY if i % 2 == 0 else colors.white
        t_style.append(("BACKGROUND", (0, i), (-1, i), bg_col))

    test_table.setStyle(TableStyle(t_style))
    story.append(test_table)
    story.append(Spacer(1, 10))

    # 4. Overall Disposition & QA Sign-off Block
    disp_pass = suite.overall_status == "PASS"
    disp_title = (
        "OVERALL DISPOSITION: PASS / CONFORMS"
        if disp_pass
        else "OVERALL DISPOSITION: FAIL / OUT OF SPEC"
    )
    disp_bg = ACCENT_GREEN_BG if disp_pass else ALERT_RED_BG
    disp_color = ACCENT_GREEN if disp_pass else ALERT_RED

    disp_style = ParagraphStyle(
        "DispStyle",
        parent=styles["DocSubtitle"],
        textColor=disp_color,
        fontSize=9,
        leading=11,
    )

    sign_data = [
        [
            Paragraph(f"<b>{disp_title}</b>", disp_style),
            Paragraph(
                f"<b>Laboratory Standard:</b> {lab.document_standard}",
                styles["MetaValue"],
            ),
        ],
        [
            Paragraph(
                f"<b>Authorized Lab Signatory:</b> {lab.authorized_signatory_name}<br/>"
                f"<b>Title:</b> {lab.signature_title}<br/>"
                f"<b>Date:</b> {suite.manufacturing_date} | <i>Digitally Certified</i>",
                styles["CalloutText"],
            ),
            Paragraph(
                f"<b>Accreditation Body:</b> {lab.accreditation_body}<br/>"
                f"<b>Accreditation Number:</b> {lab.accreditation_number}<br/>"
                "<b>Attestation:</b> Testing conducted per ISO/IEC 17025 standard. "
                "Results apply solely to the submitted lot batch sample.",
                styles["CalloutText"],
            ),
        ],
    ]

    sign_table = Table(sign_data, colWidths=[310, 230])
    sign_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), disp_bg),
                ("BOX", (0, 0), (-1, -1), 0.75, disp_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(KeepTogether([sign_table]))

    doc.build(story, canvasmaker=NumberedCanvas)  # type: ignore
    return out_file
