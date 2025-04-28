from docx import Document
from bs4 import BeautifulSoup
import os

def save_resume_as_docx(rendered_html, filename):
    document = Document()

    # Parse HTML
    soup = BeautifulSoup(rendered_html, "html.parser")

    for element in soup.descendants:
        if element.name == "h1":
            p = document.add_paragraph(element.get_text())
            p.style = "Heading 1"
        elif element.name == "h2":
            p = document.add_paragraph(element.get_text())
            p.style = "Heading 2"
        elif element.name == "p":
            document.add_paragraph(element.get_text())
        elif element.name == "li":
            document.add_paragraph(element.get_text(), style="List Bullet")

    # Ensure downloads folder exists
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    # Save document
    safe_filename = filename.replace(" ", "_")
    file_path = os.path.join(downloads_dir, safe_filename)
    document.save(file_path)

    return file_path
