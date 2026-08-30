import unittest

import numpy as np
from langchain_core.documents import Document

from src.rag.embeddings import MultilingualEmbedder, create_embedding_documents
from tests.test_rag_knowledge_base import WordTokenizer


class FakeTokenizer(WordTokenizer):
    def num_special_tokens_to_add(self, pair: bool = False) -> int:
        return 2


class FakeSentenceTransformer:
    def __init__(self) -> None:
        self.tokenizer = FakeTokenizer()
        self.max_seq_length = 128

    def encode_document(self, texts, **kwargs):
        return np.asarray(
            [[len(text.split()), index + 1, 1.0] for index, text in enumerate(texts)],
            dtype=np.float32,
        )

    def encode_query(self, texts, **kwargs):
        return np.asarray([[len(texts[0].split()), 1.0, 1.0]], dtype=np.float32)


class EmbeddingsTest(unittest.TestCase):
    def test_500_token_parent_is_split_without_model_truncation(self) -> None:
        tokenizer = FakeTokenizer()
        parent = Document(
            page_content=" ".join(f"t{index}" for index in range(500)),
            metadata={"chunk_id": "parent-1", "document_id": "doc-1"},
        )

        children = create_embedding_documents([parent], tokenizer, 128)

        self.assertEqual(len(children), 5)
        self.assertTrue(
            all(child.metadata["embedding_token_count"] <= 126 for child in children)
        )
        self.assertEqual(children[0].metadata["parent_chunk_id"], "parent-1")
        self.assertEqual(
            children[0].page_content.split()[-24:], children[1].page_content.split()[:24]
        )

    def test_adapter_normalizes_document_and_query_vectors(self) -> None:
        adapter = MultilingualEmbedder(model=FakeSentenceTransformer())
        documents = [
            Document(page_content="um dois", metadata={"chunk_id": "a"}),
            Document(page_content="três quatro cinco", metadata={"chunk_id": "b"}),
        ]

        vectors = adapter.encode_documents(documents)
        query = adapter.encode_query("consulta MED")

        np.testing.assert_allclose(np.linalg.norm(vectors, axis=1), [1.0, 1.0])
        self.assertAlmostEqual(float(np.linalg.norm(query)), 1.0, places=6)

    def test_query_above_content_limit_is_rejected(self) -> None:
        adapter = MultilingualEmbedder(model=FakeSentenceTransformer())
        query = " ".join(f"q{index}" for index in range(127))

        with self.assertRaises(ValueError):
            adapter.encode_query(query)


if __name__ == "__main__":
    unittest.main()
