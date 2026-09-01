#!/usr/bin/env python3
"""
Generate Standard PDF Certificate of Analysis for COA-2026-HC-88412
Using ReportLab
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

def create_coa_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=16,
        textColor=colors.HexColor('#0F2942'),
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1E3D59'),
        alignment=0
    )

    header_meta_style = ParagraphStyle(
        'HeaderMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#555555'),
        alignment=2
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0F2942'),
        spaceAfter=3
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#333333')
    )

    meta_value_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#111111')
    )

    table_th_style = ParagraphStyle(
        'TableTH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_td_style = ParagraphStyle(
        'TableTD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#222222')
    )

    table_td_bold_style = ParagraphStyle(
        'TableTDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#111111')
    )

    pass_style = ParagraphStyle(
        'PassStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#00701A'),
        alignment=1
    )

    elements = []

    # 1. Header Banner Table (Lab Info on Left, Accreditation / Cert Info on Right)
    lab_info = [
        Paragraph("<b>GREAT LAKES BIO-ANALYTICAL SERVICES INC.</b>", title_style),
        Paragraph("Health Canada Licensed & ISO/IEC 17025:2017 Accredited Laboratory", subtitle_style),
        Paragraph("450 University Ave, Toronto, ON M5G 1V2, Canada | Tel: +1 (416) 555-0199 | CALA Accr. #9481", meta_value_style)
    ]

    cert_info = [
        Paragraph("<b>CERTIFICATE OF ANALYSIS</b>", ParagraphStyle('CertHeading', parent=title_style, alignment=2, fontSize=13, textColor=colors.HexColor('#8B0000'))),
        Paragraph("<b>Cert ID:</b> COA-2026-HC-88412", header_meta_style),
        Paragraph("<b>Date of Issue:</b> 2026-02-14", header_meta_style),
        Paragraph("<b>Acumatica Ref:</b> PO-009842 / PR-014520", header_meta_style)
    ]

    header_table = Table([[lab_info, cert_info]], colWidths=[360, 180])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0F2942'), spaceAfter=8))

    # 2. Product Identification & Metadata Box
    meta_data = [
        [
            Paragraph("<b>Product Name:</b>", meta_label_style),
            Paragraph("Organic Echinacea Purpurea Extract 4%", meta_value_style),
            Paragraph("<b>Lot / Batch Number:</b>", meta_label_style),
            Paragraph("<b>LOT-EC2602-09A</b>", ParagraphStyle('LotB', parent=meta_value_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#0F2942')))
        ],
        [
            Paragraph("<b>Botanical Source:</b>", meta_label_style),
            Paragraph("<i>Echinacea purpurea</i> (L.) Moench (Aerial)", meta_value_style),
            Paragraph("<b>Batch Quantity:</b>", meta_label_style),
            Paragraph("1,500.0 kg", meta_value_style)
        ],
        [
            Paragraph("<b>Acumatica Item ID:</b>", meta_label_style),
            Paragraph("RAW-ECH-EXT4", meta_value_style),
            Paragraph("<b>Mfg Date:</b>", meta_label_style),
            Paragraph("2026-02-01", meta_value_style)
        ],
        [
            Paragraph("<b>Health Canada NPN:</b>", meta_label_style),
            Paragraph("NPN-80029384", meta_value_style),
            Paragraph("<b>Retest / Expiry Date:</b>", meta_label_style),
            Paragraph("<b>2029-01-31</b>", meta_value_style)
        ],
        [
            Paragraph("<b>Standards Compliance:</b>", meta_label_style),
            Paragraph("Health Canada GMP (GUI-0001) | NHPR (SOR/2003-196) | USP <2021>/<2022>", meta_value_style),
            Paragraph("<b>Country of Origin:</b>", meta_label_style),
            Paragraph("Canada", meta_value_style)
        ]
    ]

    meta_table = Table(meta_data, colWidths=[95, 185, 100, 160])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F7F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CCD6DD')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#E1E8ED')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 10))

    # 3. Test Results Table
    elements.append(Paragraph("<b>ANALYTICAL TEST RESULTS / RÉSULTATS D'ANALYSE</b>", section_header_style))

    test_headers = [
        Paragraph("<b>Test Parameter</b>", table_th_style),
        Paragraph("<b>Test Method</b>", table_th_style),
        Paragraph("<b>Specification Limit</b>", table_th_style),
        Paragraph("<b>Actual Result</b>", table_th_style),
        Paragraph("<b>Status</b>", table_th_style)
    ]

    test_rows = [
        test_headers,
        [
            Paragraph("Appearance & Color", table_td_style),
            Paragraph("Organoleptic / Visual", table_td_style),
            Paragraph("Fine brown powder", table_td_style),
            Paragraph("Conforms", table_td_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("Active Total Polyphenols", table_td_bold_style),
            Paragraph("HPLC-DAD (USP Monograph)", table_td_style),
            Paragraph("≥ 4.0 % (w/w)", table_td_style),
            Paragraph("<b>4.32 %</b>", table_td_bold_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("Loss on Drying (Moisture)", table_td_style),
            Paragraph("USP <731> (105°C, 3h)", table_td_style),
            Paragraph("≤ 5.0 %", table_td_style),
            Paragraph("3.45 %", table_td_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("Heavy Metal: Lead (Pb)", table_td_bold_style),
            Paragraph("ICP-MS (USP <2232>)", table_td_style),
            Paragraph("≤ 0.50 ppm (mg/kg)", table_td_style),
            Paragraph("<b>0.08 ppm</b>", table_td_bold_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("Heavy Metal: Arsenic (As)", table_td_style),
            Paragraph("ICP-MS (USP <2232>)", table_td_style),
            Paragraph("≤ 1.00 ppm (mg/kg)", table_td_style),
            Paragraph("0.12 ppm", table_td_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("Heavy Metal: Cadmium (Cd)", table_td_style),
            Paragraph("ICP-MS (USP <2232>)", table_td_style),
            Paragraph("≤ 0.30 ppm (mg/kg)", table_td_style),
            Paragraph("0.02 ppm", table_td_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("Heavy Metal: Mercury (Hg)", table_td_style),
            Paragraph("ICP-MS (USP <2232>)", table_td_style),
            Paragraph("≤ 0.10 ppm (mg/kg)", table_td_style),
            Paragraph("0.01 ppm", table_td_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("Total Aerobic Microbial Count (TAMC)", table_td_style),
            Paragraph("USP <2021>", table_td_style),
            Paragraph("≤ 10,000 CFU/g", table_td_style),
            Paragraph("450 CFU/g", table_td_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("Total Combined Yeast & Mold (TYMC)", table_td_style),
            Paragraph("USP <2021>", table_td_style),
            Paragraph("≤ 1,000 CFU/g", table_td_style),
            Paragraph("60 CFU/g", table_td_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("<i>Escherichia coli</i>", table_td_style),
            Paragraph("USP <2022>", table_td_style),
            Paragraph("Absent in 10g", table_td_style),
            Paragraph("Absent", table_td_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("<i>Salmonella spp.</i>", table_td_style),
            Paragraph("USP <2022>", table_td_style),
            Paragraph("Absent in 25g", table_td_style),
            Paragraph("Absent", table_td_style),
            Paragraph("PASS", pass_style)
        ],
        [
            Paragraph("Residual Solvents (Ethanol)", table_td_style),
            Paragraph("GC-FID (USP <467>)", table_td_style),
            Paragraph("≤ 5,000 ppm", table_td_style),
            Paragraph("410 ppm", table_td_style),
            Paragraph("PASS", pass_style)
        ]
    ]

    results_table = Table(test_rows, colWidths=[150, 115, 115, 100, 60])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2942')),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (4,1), (4,-1), 'CENTER'),
        ('ALIGN', (3,1), (3,-1), 'LEFT'),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#0F2942')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(results_table)
    elements.append(Spacer(1, 8))

    # 4. Quality Statement & Sign-off Block
    auth_data = [
        [
            Paragraph("<b>COMPLIANCE DECLARATION / DÉCLARATION DE CONFORMITÉ:</b><br/>"
                      "This material batch has been sampled, tested, and analyzed in accordance with Health Canada "
                      "Good Manufacturing Practices (GUI-0001) and the Natural Health Products Regulations (SOR/2003-196). "
                      "All analytical parameters conform to established release specifications.", 
                      ParagraphStyle('AuthText', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=colors.HexColor('#333333'))),
            Paragraph("<b>DIGITALLY VERIFIED BY QA</b><br/>"
                      "<b>Dr. Élodie Tremblay, Ph.D., C.Chem.</b><br/>"
                      "Director of Quality Assurance & Validation<br/>"
                      "<i>Signed: 2026-02-14 16:30 EST | Auth ID: HC-CALA-9481</i>", 
                      ParagraphStyle('SignText', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=colors.HexColor('#0F2942'), alignment=2))
        ]
    ]

    auth_table = Table(auth_data, colWidths=[360, 180])
    auth_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#B0BEC5')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F6F8')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    elements.append(KeepTogether([auth_table]))

    doc.build(elements)
    print(f"Successfully generated PDF: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    target_pdf = os.path.join(out_dir, "COA-2026-HC-88412.pdf")
    create_coa_pdf(target_pdf)
