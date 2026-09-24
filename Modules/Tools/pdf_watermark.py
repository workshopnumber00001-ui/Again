import os
import tempfile
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter




#=========================== WATERMARK CODE ===================================
def create_text_watermark(text, output_path, page_size=letter, rotation=45):
    """Creates a watermark PDF with given text."""
    c = canvas.Canvas(output_path, pagesize=page_size)
    width, height = page_size
    c.setFont("Helvetica", 40)
    c.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.3)  # Light gray watermark
    c.saveState()
    c.translate(width / 2, height / 2)
    c.rotate(rotation)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()

def add_text_watermark(input_pdf_path, watermark_text, output_pdf_path):
    """Overlays a text watermark on every page of the input PDF."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        watermark_pdf_path = temp_pdf.name
    create_text_watermark(watermark_text, watermark_pdf_path)

    with open(input_pdf_path, "rb") as input_file, open(watermark_pdf_path, "rb") as watermark_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        watermark_reader = PyPDF2.PdfReader(watermark_file)
        watermark_page = watermark_reader.pages[0]
        
        pdf_writer = PyPDF2.PdfWriter()
        for page in pdf_reader.pages:
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)
        
        with open(output_pdf_path, "wb") as output_file:
            pdf_writer.write(output_file)

    for file in [watermark_pdf_path, watermark_file, watermark_page, watermark_reader, watermark_text]:
        os.remove(file)