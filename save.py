# save.py

from docx import Document
import os

UPLOAD_FOLDER = 'downloads'

def save_resume_as_docx(resume_json, filename):
    document = Document()

    # Professional Summary
    document.add_heading('Professional Summary', level=1)
    document.add_paragraph(resume_json['summary'])

    # Education
    document.add_heading('Education', level=1)
    document.add_paragraph(resume_json['education'])

    # Skills
    document.add_heading('Skills', level=1)
    skills = ', '.join(resume_json['skills'])
    document.add_paragraph(skills)

    # Experience
    document.add_heading('Experience', level=1)
    for exp in resume_json['experience']:
        document.add_heading(f"{exp['title']} at {exp['company']} ({exp['dates']})", level=2)
        for bullet in exp['bullets']:
            document.add_paragraph(bullet, style='List Bullet')

    # Save to downloads folder
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    document.save(filepath)
    return filepath
