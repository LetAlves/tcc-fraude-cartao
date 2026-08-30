import tempfile
import unittest
from pathlib import Path

from scripts.download_rag_corpus import (
    _content_type_is_allowed,
    _safe_output,
    _validate_source,
)


def valid_source() -> dict[str, str]:
    return {
        "document_id": "doc-1",
        "title": "Documento",
        "issuer": "Emissor",
        "document_type": "regulamento",
        "format": "pdf",
        "source_url": "https://example.org/documento",
        "filename": "documento.pdf",
        "version_label": "1.0",
    }


class DownloaderTest(unittest.TestCase):
    def test_catalog_rejects_non_https_source(self) -> None:
        source = valid_source()
        source["source_url"] = "http://example.org/documento"

        with self.assertRaises(ValueError):
            _validate_source(source)

    def test_output_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            with self.assertRaises(ValueError):
                _safe_output(Path(temporary_directory), "../fora.pdf")

    def test_content_type_must_match_catalog_format(self) -> None:
        self.assertTrue(_content_type_is_allowed("pdf", "application/pdf"))
        self.assertTrue(
            _content_type_is_allowed("bcb_normativo_json", "application/json; charset=utf-8")
        )
        self.assertFalse(_content_type_is_allowed("pdf", "text/html"))


if __name__ == "__main__":
    unittest.main()
