from pathlib import Path
from uuid import uuid4
from urllib.parse import urlparse

from fpdf import FPDF
from PIL import Image

from app.config import BASE_DIR, EXPORTS_DIR
from app.models import ComicPanel


def _local_image_path(image_url: str) -> Path:
    parsed = urlparse(image_url)
    relative = parsed.path.lstrip("/")
    path = BASE_DIR / relative

    if not path.is_file():
        raise FileNotFoundError(
            f"Generated image not found: {path}"
        )

    return path


def _clean_text(text: str) -> str:
    """
    Convert AI-generated Unicode characters into
    characters supported by the Helvetica font.
    """

    if not text:
        return ""

    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "-",
        "©": "(c)",
        "®": "(R)",
        "™": "(TM)",
        "\u00a0": " ",  # non-breaking space
        "\u200b": "",   # zero-width space
        "\u200c": "",
        "\u200d": "",
        "\ufeff": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Helvetica is not Unicode capable.
    text = text.encode(
        "latin-1",
        errors="replace"
    ).decode("latin-1")

    return text


def _write_text(pdf: FPDF, text: str, height: float) -> None:
    """
    Safely write text using character wrapping.

    This prevents FPDF from failing when the AI produces
    a very long word/token with no spaces.
    """

    text = _clean_text(text)

    if not text:
        return

    pdf.multi_cell(
        0,
        height,
        text,
        wrapmode="CHAR"
    )


def save_pdf(title: str, panels: list[ComicPanel]) -> str:
    filename = f"comic_{uuid4().hex}.pdf"
    output = EXPORTS_DIR / filename

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=14
    )

    for panel in panels:

        # ==========================================
        # NEW PAGE
        # ==========================================

        pdf.add_page()

        # ==========================================
        # PANEL TITLE
        # ==========================================

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        panel_title = (
            f"Panel {panel.panel_number}: "
            f"{panel.title}"
        )

        _write_text(
            pdf,
            panel_title,
            10
        )

        pdf.ln(2)

        # ==========================================
        # PANEL IMAGE
        # ==========================================

        image_path = _local_image_path(
            panel.image_url
        )

        with Image.open(image_path) as img:
            width, height = img.size

        max_w = 180
        max_h = 105

        scale = min(
            max_w / width,
            max_h / height
        )

        draw_w = width * scale
        draw_h = height * scale

        x = (210 - draw_w) / 2

        pdf.image(
            str(image_path),
            x=x,
            y=pdf.get_y(),
            w=draw_w,
            h=draw_h
        )

        pdf.set_y(
            pdf.get_y() + draw_h + 6
        )

        # ==========================================
        # SCENE DESCRIPTION
        # ==========================================

        pdf.set_font(
            "Helvetica",
            "I",
            10
        )

        _write_text(
            pdf,
            panel.scene_description,
            6
        )

        pdf.ln(2)

        # ==========================================
        # CAPTION
        # ==========================================

        if panel.caption:

            pdf.set_font(
                "Helvetica",
                "B",
                10
            )

            _write_text(
                pdf,
                f"Caption: {panel.caption}",
                6
            )

            pdf.ln(1)

        # ==========================================
        # NARRATION
        # ==========================================

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        _write_text(
            pdf,
            panel.narration,
            6
        )

        # ==========================================
        # DIALOGUE
        # ==========================================

        if panel.dialogue:

            pdf.ln(2)

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            _write_text(
                pdf,
                "Dialogue",
                6
            )

            pdf.set_font(
                "Helvetica",
                "",
                10
            )

            for line in panel.dialogue:

                clean_line = _clean_text(line)

                _write_text(
                    pdf,
                    f"- {clean_line}",
                    5.5
                )

    # ==========================================
    # SAVE PDF
    # ==========================================

    pdf.output(str(output))

    return f"/static/exports/{filename}"