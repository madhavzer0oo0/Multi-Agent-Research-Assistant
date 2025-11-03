from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

def generate_pdf(title, content):
    buffer = BytesIO()

    # Add safe margins (left, right, top, bottom)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=60,
        rightMargin=60,
        topMargin=60,
        bottomMargin=60
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Custom', fontSize=11, leading=15, alignment=TA_LEFT))

    story = [
        Paragraph(f"<b>{title}</b>", styles["Title"]),
        Spacer(1, 12),
        Paragraph(content.replace("\n", "<br/>"), styles["Custom"])
    ]

    doc.build(story)
    buffer.seek(0)
    return buffer
