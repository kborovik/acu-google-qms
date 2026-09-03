"""ReportLab styling and canvas layout for shipping documents."""

from typing import Any

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas

# Corporate & Compliance Color Palette
NAVY_PRIMARY = colors.HexColor("#0F2942")  # Deep Nordic Navy
SLATE_BLUE = colors.HexColor("#1E3D59")  # Secondary Header Blue
BORDER_GRAY = colors.HexColor("#D1D5DB")  # Neutral Border Gray
BG_LIGHT_GRAY = colors.HexColor("#F9FAFB")  # Subtle Row Fill
BG_ALT_GRAY = colors.HexColor("#F3F4F6")  # Alternating Table Row
TEXT_DARK = colors.HexColor("#111827")  # Primary Text
TEXT_MUTED = colors.HexColor("#4B5563")  # Secondary / Subtitle Text
ACCENT_GREEN = colors.HexColor("#059669")  # In-Spec / Pass / Released
ACCENT_GREEN_BG = colors.HexColor("#ECFDF5")
ALERT_RED = colors.HexColor("#DC2626")  # OOS / Quarantine / Failed
ALERT_RED_BG = colors.HexColor("#FEF2F2")
ACCENT_AMBER = colors.HexColor("#D97706")  # Warning / Hold
ACCENT_AMBER_BG = colors.HexColor("#FFFBEB")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render total page count."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)  # type: ignore
        self._saved_page_states: list[dict[str, Any]] = []

    def showPage(self) -> None:  # noqa: N802
        self._saved_page_states.append(dict(self.__dict__))
        # Call base startPage method
        self._startPage()  # pyright: ignore[reportAttributeAccessIssue,reportUnknownMemberType]

    def save(self) -> None:
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)  # type: ignore
        canvas.Canvas.save(self)  # type: ignore

    def draw_page_number(self, page_count: int) -> None:
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(TEXT_MUTED)

        # Footer divider line
        self.setStrokeColor(BORDER_GRAY)
        self.setLineWidth(0.5)
        self.line(36, 30, 576, 30)

        # Left footer info
        footer_note = (
            "CanNordic BioNutra Inc. Gateway | Acumatica ERP & Health Canada GMP"
        )
        self.drawString(36, 20, footer_note)

        # Right footer page count
        curr_page = int(getattr(self, "_pageNumber", 1))  # pyright: ignore[reportUnknownArgumentType]
        page_text = f"Page {curr_page} of {page_count}"
        self.drawRightString(576, 20, page_text)
        self.restoreState()


def get_document_styles() -> dict[str, ParagraphStyle]:
    """Returns a curated dictionary of ParagraphStyles for all documents."""
    base_styles = getSampleStyleSheet()

    styles: dict[str, ParagraphStyle] = {
        "DocTitle": ParagraphStyle(
            "DocTitle",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=15,
            textColor=NAVY_PRIMARY,
        ),
        "DocSubtitle": ParagraphStyle(
            "DocSubtitle",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=SLATE_BLUE,
        ),
        "HeaderMeta": ParagraphStyle(
            "HeaderMeta",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=TEXT_MUTED,
            alignment=2,  # Right aligned
        ),
        "SectionHeader": ParagraphStyle(
            "SectionHeader",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=NAVY_PRIMARY,
            spaceAfter=2,
        ),
        "MetaLabel": ParagraphStyle(
            "MetaLabel",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9.5,
            textColor=TEXT_DARK,
        ),
        "MetaValue": ParagraphStyle(
            "MetaValue",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=TEXT_DARK,
        ),
        "TableTH": ParagraphStyle(
            "TableTH",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=8.5,
            textColor=colors.white,
            alignment=1,  # Center
        ),
        "TableTD": ParagraphStyle(
            "TableTD",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=8.5,
            textColor=TEXT_DARK,
        ),
        "TableTDCenter": ParagraphStyle(
            "TableTDCenter",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=8.5,
            textColor=TEXT_DARK,
            alignment=1,
        ),
        "TableTDBold": ParagraphStyle(
            "TableTDBold",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=8.5,
            textColor=TEXT_DARK,
        ),
        "BadgePass": ParagraphStyle(
            "BadgePass",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=8.5,
            textColor=ACCENT_GREEN,
            alignment=1,
        ),
        "BadgeFail": ParagraphStyle(
            "BadgeFail",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=8.5,
            textColor=ALERT_RED,
            alignment=1,
        ),
        "CalloutText": ParagraphStyle(
            "CalloutText",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=TEXT_DARK,
        ),
        "SignatureLabel": ParagraphStyle(
            "SignatureLabel",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            textColor=TEXT_MUTED,
        ),
    }

    return styles
