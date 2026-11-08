"""Extract resume text in memory; uploaded documents are never saved."""
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote
from zipfile import ZipFile
from xml.etree import ElementTree

MAX_FILE_BYTES = 5 * 1024 * 1024


def extract_resume(filename, content):
    extension = Path(unquote(filename)).suffix.lower()
    if extension not in ('.pdf', '.docx'):
        raise ValueError('Choose a PDF or Word .docx file. For older .doc files, save as .docx or paste the text.')
    if not content or len(content) > MAX_FILE_BYTES:
        raise ValueError('Choose a non-empty document smaller than 5 MB.')
    try:
        if extension == '.pdf':
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(content))
            if reader.is_encrypted:
                raise ValueError('Password-protected PDFs are not supported. Upload an unlocked copy or paste the text.')
            if len(reader.pages) > 20:
                raise ValueError('Use a resume PDF with 20 pages or fewer.')
            text = '\n'.join(page.extract_text() or '' for page in reader.pages)
        else:
            with ZipFile(BytesIO(content)) as archive:
                info = archive.getinfo('word/document.xml')
                if info.file_size > 2 * 1024 * 1024:
                    raise ValueError('This Word document is too large to extract. Paste the resume text instead.')
                xml = archive.read(info)
                if b'<!DOCTYPE' in xml or b'<!ENTITY' in xml:
                    raise ValueError('Unsupported Word document structure. Paste the text instead.')
                root = ElementTree.fromstring(xml)
                ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
                # Paragraphs include those inside tables; headers and text boxes may need manual correction.
                paragraphs = []
                for paragraph in root.iter(ns + 'p'):
                    parts = []
                    for node in paragraph.iter():
                        if node.tag == ns + 't':
                            parts.append(node.text or '')
                        elif node.tag in (ns + 'tab', ns + 'br'):
                            parts.append(' ')
                    paragraphs.append(''.join(parts))
                text = '\n'.join(paragraphs)
    except ImportError:
        raise ValueError('PDF support needs setup: install requirements.txt in .venv and run .venv/bin/python server.py.') from None
    except ValueError:
        raise
    except Exception:
        raise ValueError('Could not read this document. It may be damaged or unsupported. Try another file or paste the text.') from None
    text = text.strip()
    if len(text) < 30:
        raise ValueError('Not enough readable text found. Scanned/image-only PDFs need OCR first; you can paste the text instead.')
    if len(text) > 20000:
        raise ValueError('Extracted text exceeds 20,000 characters. Upload a shorter resume or paste the relevant text.')
    return text
