from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Path to the text file and output PDF
text_file_path = '/workspaces/PDFTranslations/2005_1_1065_1068-0_translated.txt'
output_pdf_path = '/workspaces/PDFTranslations/output/output.pdf'

# Register a TrueType font that supports Gurmukhi script
pdfmetrics.registerFont(TTFont('NotoSansGurmukhi', '/workspaces/PDFTranslations/Noto_Sans_Gurmukhi/NotoSansGurmukhi-VariableFont_wdth,wght.ttf'))

def create_pdf(input_text_path, output_pdf_path):
    # Create a PDF canvas
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    c.setFont('NotoSansGurmukhi', 12)  # Set the font to Noto Sans Gurmukhi
    
    # Read the text file
    with open(input_text_path, 'r', encoding='utf-8') as file:
        text = file.read().splitlines()
    
    # Coordinates for text placement
    x = 72  # 1 inch from the left
    y = 750  # Start 1 inch from the top of the page, move down for each line
    
    # Write each line of text to the PDF
    for line in text:
        c.drawString(x, y, line)
        y -= 14  # Move to the next line
        if y < 72:  # Check if we are close to the bottom of the page
            c.showPage()  # Start a new page
            c.setFont('NotoSansGurmukhi', 12)
            y = 750  # Reset y coordinate

    c.save()  # Save the PDF

# Run the function to create the PDF
create_pdf(text_file_path, output_pdf_path)
