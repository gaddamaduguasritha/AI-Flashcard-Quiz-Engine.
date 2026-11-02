import os

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}


def extract_text(file_path):
    extension = file_path.rsplit(".", 1)[1].lower()
    if extension == "txt":
        return _extract_txt(file_path)
    if extension == "pdf":
        return _extract_pdf(file_path)
    if extension == "docx":
        return _extract_docx(file_path)
    return "", "Unsupported file type."


def _extract_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
            return handle.read(), None
    except OSError as exc:
        return "", f"Could not read TXT file: {exc}"


def _extract_pdf(file_path):
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        pages = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            pages.append(page_text)
        text = "\n".join(pages).strip()
        if not text:
            return "", "No readable text was found in the PDF. It may be a scanned document."
        return text, None
    except Exception as exc:
        return "", f"Could not read PDF file: {exc}"


def _extract_docx(file_path):
    try:
        import docx
        document = docx.Document(file_path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        text = "\n".join(paragraphs).strip()
        if not text:
            return "", "No readable text was found in the DOCX file."
        return text, None
    except Exception as exc:
        return "", f"Could not read DOCX file: {exc}"
