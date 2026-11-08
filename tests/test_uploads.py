import io
import json
import threading
import unittest
import urllib.error
import urllib.request
from zipfile import ZipFile

from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
from resume_files import extract_resume, MAX_FILE_BYTES
from server import Handler, ThreadingHTTPServer

TEXT = 'Fictional MBA candidate with product research and SQL experience.'


def docx_bytes():
    out = io.BytesIO()
    with ZipFile(out, 'w') as archive:
        archive.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:tbl><w:tr><w:tc><w:p><w:r><w:t>' + TEXT + '</w:t></w:r></w:p></w:tc></w:tr></w:tbl></w:body></w:document>')
    return out.getvalue()


def pdf_bytes(blank=False, encrypted=False):
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    if not blank:
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'), NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): writer._add_object(font)})})
        stream = DecodedStreamObject()
        stream.set_data(('BT /F1 12 Tf 50 700 Td (' + TEXT + ') Tj ET').encode())
        page[NameObject('/Contents')] = writer._add_object(stream)
    if encrypted:
        writer.encrypt('fictional-password')
    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()


class ExtractionTests(unittest.TestCase):
    def test_pdf_extracts_actual_text(self):
        self.assertEqual(extract_resume('resume.PDF', pdf_bytes()), TEXT)

    def test_docx_includes_table_paragraphs(self):
        self.assertEqual(extract_resume('resume.docx', docx_bytes()), TEXT)

    def test_rejects_invalid_unsupported_blank_encrypted_and_oversize(self):
        cases = [('x.doc', b'old'), ('x.pdf', b'broken'), ('x.docx', b'broken'), ('x.pdf', pdf_bytes(blank=True)), ('x.pdf', pdf_bytes(encrypted=True)), ('x.docx', b'x' * (MAX_FILE_BYTES + 1))]
        for filename, data in cases:
            with self.subTest(filename=filename, size=len(data)):
                with self.assertRaises(ValueError):
                    extract_resume(filename, data)


class UploadHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_upload_both_formats_then_analyze_extracted_text(self):
        for filename, content in [('resume.pdf', pdf_bytes()), ('resume.docx', docx_bytes())]:
            request = urllib.request.Request(self.url + '/api/extract', data=content, headers={'X-Filename': filename})
            with urllib.request.urlopen(request) as response:
                text = json.load(response)['text']
            self.assertEqual(text, TEXT)
            body = json.dumps({'resume': text, 'job_description': 'Product manager with SQL and customer research skills.', 'mode': 'local'}).encode()
            with urllib.request.urlopen(urllib.request.Request(self.url + '/api/analyze', data=body)) as response:
                self.assertEqual(len(json.load(response)['result']['improvements']), 3)

    def test_invalid_file_returns_safe_error(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(urllib.request.Request(self.url + '/api/extract', data=b'broken', headers={'X-Filename': 'resume.docx'}))
        self.assertEqual(error.exception.code, 400)
        self.assertIn('Could not read', json.load(error.exception)['error'])
