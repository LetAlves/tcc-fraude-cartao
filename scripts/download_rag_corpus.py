"""Baixa e versiona o corpus documental oficial usado pelo RAG.

Os documentos brutos e o manifesto de execução ficam fora do Git. A lista de
fontes permitidas, por outro lado, é versionada em ``config`` para manter a
coleta reproduzível e impedir downloads arbitrários.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_CONFIG = PROJECT_ROOT / "config" / "rag_corpus_sources.json"
DEFAULT_RAW_DIR = PROJECT_ROOT / "data" / "rag" / "raw"
DEFAULT_MANIFEST = PROJECT_ROOT / "data" / "rag" / "manifest.json"
MAX_DOCUMENT_BYTES = 100 * 1024 * 1024
DOWNLOAD_TIMEOUT_SECONDS = 90
USER_AGENT = "TCC-Fraude-Pix-RAG/1.0 (academic reproducibility)"


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, dict):
        raise ValueError(f"O JSON deve conter um objeto na raiz: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_output(raw_dir: Path, filename: object) -> Path:
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Toda fonte deve definir um filename não vazio.")
    if Path(filename).name != filename:
        raise ValueError(f"Filename inseguro no catálogo: {filename!r}")

    raw_dir = raw_dir.resolve()
    output = (raw_dir / filename).resolve()
    if output.parent != raw_dir:
        raise ValueError(f"Arquivo sairia do diretório autorizado: {filename!r}")
    return output


def _validate_source(source: dict[str, Any]) -> None:
    required = {
        "document_id",
        "title",
        "issuer",
        "document_type",
        "format",
        "source_url",
        "filename",
        "version_label",
    }
    missing = sorted(required - source.keys())
    if missing:
        raise ValueError(f"Fonte incompleta; campos ausentes: {', '.join(missing)}")
    for field in required:
        if not isinstance(source[field], str) or not source[field].strip():
            raise ValueError(f"Campo {field!r} deve ser uma string não vazia.")

    source_url = source["source_url"]
    if not isinstance(source_url, str) or urlparse(source_url).scheme != "https":
        raise ValueError(f"Somente fontes HTTPS são aceitas: {source_url!r}")
    if source["format"] not in {"html", "pdf", "bcb_normativo_json"}:
        raise ValueError(f"Formato não suportado: {source['format']!r}")
    download_url = source.get("download_url", source_url)
    if not isinstance(download_url, str) or urlparse(download_url).scheme != "https":
        raise ValueError(f"Somente downloads HTTPS são aceitos: {download_url!r}")


def _content_type_is_allowed(document_format: str, content_type: str) -> bool:
    media_type = content_type.partition(";")[0].strip().lower()
    allowed = {
        "html": {"text/html", "application/xhtml+xml"},
        "pdf": {"application/pdf", "application/octet-stream"},
        "bcb_normativo_json": {"application/json", "text/json"},
    }
    return media_type in allowed[document_format]


def _download_one(source: dict[str, Any], output: Path) -> dict[str, Any]:
    request = urllib.request.Request(
        source.get("download_url", source["source_url"]),
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/pdf,application/json",
        },
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    temporary_path: Path | None = None
    try:
        with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
            final_url = response.geturl()
            if urlparse(final_url).scheme != "https":
                raise ValueError(f"Redirecionamento para URL não HTTPS: {final_url}")

            content_type = response.headers.get("Content-Type", "")
            if not _content_type_is_allowed(source["format"], content_type):
                raise ValueError(
                    f"Content-Type inesperado para {source['document_id']}: {content_type!r}"
                )

            declared_size = response.headers.get("Content-Length")
            if declared_size and int(declared_size) > MAX_DOCUMENT_BYTES:
                raise ValueError(f"Documento excede {MAX_DOCUMENT_BYTES} bytes.")

            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, dir=output.parent, suffix=".part"
            ) as temporary:
                temporary_path = Path(temporary.name)
                copied = 0
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    copied += len(block)
                    if copied > MAX_DOCUMENT_BYTES:
                        raise ValueError(f"Documento excede {MAX_DOCUMENT_BYTES} bytes.")
                    temporary.write(block)

        os.replace(temporary_path, output)
        temporary_path = None
        return {
            **source,
            "final_url": final_url,
            "retrieved_at": datetime.now(UTC).isoformat(),
            "content_type": content_type,
            "bytes": output.stat().st_size,
            "sha256": _sha256(output),
            "local_filename": output.name,
        }
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def download_corpus(
    source_config: Path = DEFAULT_SOURCE_CONFIG,
    raw_dir: Path = DEFAULT_RAW_DIR,
    manifest_path: Path = DEFAULT_MANIFEST,
    *,
    refresh: bool = False,
) -> dict[str, Any]:
    """Baixa as fontes catalogadas e devolve o manifesto com hashes SHA-256."""

    catalog = _read_json(source_config)
    sources = catalog.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("O catálogo deve conter uma lista não vazia em 'sources'.")

    previous_by_id: dict[str, dict[str, Any]] = {}
    if manifest_path.exists():
        previous = _read_json(manifest_path)
        previous_by_id = {
            item["document_id"]: item
            for item in previous.get("documents", [])
            if isinstance(item, dict) and "document_id" in item
        }

    documents: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for raw_source in sources:
        if not isinstance(raw_source, dict):
            raise ValueError("Cada fonte deve ser representada por um objeto JSON.")
        source = dict(raw_source)
        _validate_source(source)
        document_id = str(source["document_id"])
        if document_id in seen_ids:
            raise ValueError(f"document_id duplicado: {document_id}")
        seen_ids.add(document_id)

        output = _safe_output(raw_dir, source["filename"])
        previous = previous_by_id.get(document_id)
        can_reuse = (
            not refresh
            and output.exists()
            and previous is not None
            and previous.get("source_url") == source["source_url"]
            and previous.get("download_url") == source.get("download_url")
            and previous.get("version_label") == source["version_label"]
            and previous.get("sha256") == _sha256(output)
        )
        if can_reuse:
            documents.append({**previous, **source, "local_filename": output.name})
            print(f"[reutilizado] {document_id}")
        else:
            documents.append(_download_one(source, output))
            print(f"[baixado] {document_id}")

    manifest = {
        "schema_version": "1.0",
        "catalog_schema_version": catalog.get("schema_version"),
        "generated_at": datetime.now(UTC).isoformat(),
        "documents": documents,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
        dir=manifest_path.parent,
        suffix=".part",
    ) as temporary:
        json.dump(manifest, temporary, ensure_ascii=False, indent=2)
        temporary.write("\n")
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, manifest_path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-config", type=Path, default=DEFAULT_SOURCE_CONFIG)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--refresh", action="store_true", help="Baixa novamente mesmo se o hash local for válido."
    )
    args = parser.parse_args()
    manifest = download_corpus(
        args.source_config,
        args.raw_dir,
        args.manifest,
        refresh=args.refresh,
    )
    total_bytes = sum(document["bytes"] for document in manifest["documents"])
    print(f"Corpus pronto: {len(manifest['documents'])} documentos, {total_bytes} bytes.")


if __name__ == "__main__":
    main()
