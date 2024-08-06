import shutil
from docx import Document

def remove_trace_lines(docx_path, new_docx_path):
    # Copy the original DOCX file to a new file
    shutil.copy(docx_path, new_docx_path)

    # Open the new DOCX file
    doc = Document(new_docx_path)

    # List to hold paragraphs to delete
    paragraphs_to_delete = []

    # Iterate through all paragraphs in the document and collect paragraphs to delete
    for para in doc.paragraphs:
        if para.text.startswith("追溯："):# 修改此处的判断条件
            paragraphs_to_delete.append(para)

    # Remove collected paragraphs from the document
    for para in paragraphs_to_delete:
        p = para._element
        p.getparent().remove(p)

    # Save the modified document
    doc.save(new_docx_path)

# Example usage
remove_trace_lines('./test/推力系统形式化需求-三期-有追溯.docx', './test/推力系统形式化需求-三期-无追溯.docx')
