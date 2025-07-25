from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_inspection_report(violations, filename="inspection_report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Site Inspection Report")
    
    y = 700
    for v in violations:
        c.drawString(100, y, f"- {v}")
        y -= 20

    c.save()

# Example:
generate_inspection_report([
    "Missing helmet detected at zone_3",
    "Obstructed fire exit near zone_1"
])
