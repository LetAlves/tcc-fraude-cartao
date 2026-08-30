import json
import unittest
from pathlib import Path
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class JulyDeliverablesTest(unittest.TestCase):
    def test_corpus_catalog_contains_unique_official_sources(self) -> None:
        config = json.loads(
            (PROJECT_ROOT / "config" / "rag_corpus_sources.json").read_text(
                encoding="utf-8"
            )
        )
        sources = config["sources"]
        document_ids = [source["document_id"] for source in sources]

        self.assertEqual(len(sources), 4)
        self.assertEqual(len(document_ids), len(set(document_ids)))
        self.assertEqual(
            set(document_ids),
            {
                "bcb-regulamento-pix-resolucao-1-2020",
                "bcb-resolucao-103-2021",
                "bcb-guia-med-4-3",
                "febraban-tecnologia-bancaria-2024-volume-1",
            },
        )
        for source in sources:
            self.assertEqual(urlparse(source["source_url"]).scheme, "https")
            self.assertEqual(
                urlparse(source.get("download_url", source["source_url"])).scheme,
                "https",
            )

    def test_large_rag_artifacts_are_ignored(self) -> None:
        gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")

        self.assertIn("data/rag/raw/", gitignore)
        self.assertIn("data/rag/processed/", gitignore)
        self.assertIn("data/rag/index/", gitignore)
        self.assertIn("data/rag/manifest.json", gitignore)

    def test_shap_methodology_records_scale_and_anonymous_feature_limit(self) -> None:
        methodology = (
            PROJECT_ROOT / "monografia" / "capitulos" / "03_metodologia.tex"
        ).read_text(encoding="utf-8")

        self.assertIn("TreeExplainer", methodology)
        self.assertIn("log-odds", methodology)
        self.assertIn("atributo anonimizado de alta influência", methodology)
        self.assertIn("não como causalidade", methodology)

    def test_joint_llm_decision_is_not_marked_complete(self) -> None:
        report = (
            PROJECT_ROOT / "reports" / "pessoa_2" / "julho" / "README.md"
        ).read_text(encoding="utf-8")

        self.assertIn("decisão conjunta pendente", report)
        self.assertIn("m3_p1_1", report)
        self.assertIn("não foram marcadas como concluídas", report)

    def test_snapshot_has_sha256_for_every_catalog_document(self) -> None:
        snapshot = json.loads(
            (
                PROJECT_ROOT
                / "reports"
                / "pessoa_2"
                / "julho"
                / "corpus_snapshot_2026-08-30.json"
            ).read_text(encoding="utf-8")
        )

        self.assertEqual(len(snapshot["documents"]), 4)
        for document in snapshot["documents"]:
            self.assertEqual(len(document["sha256"]), 64)
            int(document["sha256"], 16)


if __name__ == "__main__":
    unittest.main()
