#!/usr/bin/env python3
"""Cache local PDF text and return only requested pages. No OCR or math verification."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


class CacheError(Exception):
    pass


OPTIONS = ["-layout", "-enc", "UTF-8"]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inside(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise CacheError("Path escapes the paper workspace.")
    return resolved


def source_file(root: Path, name: str) -> Path:
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise CacheError("Source must be a workspace-relative PDF path without '..'.")
    path = inside(root, root / relative)
    if path.suffix.lower() != ".pdf" or not path.is_file():
        raise CacheError("Source must be an existing PDF.")
    return path


def pages_digest(pages: list[str]) -> str:
    return digest(json.dumps(pages, ensure_ascii=False).encode("utf-8"))


def cache_path(root: Path, source_hash: str) -> Path:
    path = root / ".mrr" / "source-cache" / (source_hash + ".json")
    resolved = inside(root, path)
    if resolved != path:
        raise CacheError("Cache paths must not follow links into other workspace files.")
    return path


def load_cache(path: Path, source_hash: str) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise ValueError("schema")
        pages = data.get("pages")
        if (data.get("source_sha256") != source_hash or not isinstance(pages, list) or not pages or
                not all(isinstance(page, str) for page in pages) or
                pages_digest(pages) != data.get("pages_sha256")):
            raise ValueError("content")
        return data
    except (OSError, UnicodeError, ValueError) as exc:
        raise CacheError("Missing, stale or damaged source cache; run prepare again.") from exc


def command(args: list[str]) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(args, capture_output=True, encoding="utf-8", errors="replace", timeout=180)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CacheError("PDF text tool failed or timed out.") from exc


def prepare(root: Path, name: str, pdftotext: str = "pdftotext") -> dict:
    source = source_file(root, name)
    source_hash = digest(source.read_bytes())
    target = cache_path(root, source_hash)
    tool = shutil.which(pdftotext)
    if not tool:
        raise CacheError("Missing pdftotext. Pass --pdftotext with an existing tool; nothing is installed.")
    version = command([tool, "-v"])
    if version.returncode:
        raise CacheError("Cannot identify pdftotext version.")
    identity = {"binary_sha256": digest(Path(tool).read_bytes()),
                "version": (version.stdout + version.stderr).strip(), "options": OPTIONS}
    try:
        data = load_cache(target, source_hash)
    except CacheError:
        data = None
    hit = data is not None and data.get("extractor") == identity
    if not hit:
        target.parent.mkdir(parents=True, exist_ok=True)
        inside(root, target.parent)
        with tempfile.NamedTemporaryFile(dir=target.parent, suffix=".txt", delete=False) as output:
            text_path = Path(output.name)
        temporary = None
        try:
            result = command([tool, *OPTIONS, str(source), str(text_path)])
            if result.returncode:
                raise CacheError("PDF extraction failed; no cache was published.")
            text = text_path.read_text(encoding="utf-8")
            pages = text.split("\f")
            if pages and not pages[-1].strip():
                pages.pop()
            if not pages:
                raise CacheError("No page boundaries/text extracted; inspect the PDF or use OCR.")
            if digest(source.read_bytes()) != source_hash:
                raise CacheError("Source changed during extraction; no cache was published.")
            data = {"schema_version": 1, "source_sha256": source_hash, "extractor": identity,
                    "pages": pages, "pages_sha256": pages_digest(pages)}
            with tempfile.NamedTemporaryFile(dir=target.parent, suffix=".json", delete=False) as staged:
                temporary = Path(staged.name)
                staged.write((json.dumps(data, ensure_ascii=False) + "\n").encode("utf-8"))
            cache_path(root, source_hash)
            os.replace(temporary, target)
        finally:
            inside(root, text_path).unlink(missing_ok=True)
            if temporary is not None:
                inside(root, temporary).unlink(missing_ok=True)
    elif digest(source.read_bytes()) != source_hash:
        raise CacheError("Source changed while checking the cache; run prepare again.")
    return {"status": "cached", "cache_hit": hit, "source_sha256": source_hash,
            "pages": len(data["pages"]), "empty_pages": [i + 1 for i, p in enumerate(data["pages"]) if not p.strip()],
            "cache": str(target.relative_to(root)), "visual_math_check": "required separately"}


def read_pages(root: Path, name: str, selection: str) -> dict:
    source = source_file(root, name)
    source_hash = digest(source.read_bytes())
    data = load_cache(cache_path(root, source_hash), source_hash)
    wanted = set()
    try:
        for part in selection.split(","):
            ends = part.strip().split("-")
            if len(ends) not in (1, 2):
                raise ValueError()
            start, end = int(ends[0]), int(ends[-1])
            if not 1 <= start <= end <= len(data["pages"]):
                raise ValueError()
            wanted.update(range(start, end + 1))
    except ValueError as exc:
        raise CacheError("Use existing 1-based pages, e.g. --pages 2,5-7; no text was returned.") from exc
    if digest(source.read_bytes()) != source_hash:
        raise CacheError("Source changed while reading cache; run prepare again.")
    return {"kind": "untrusted-source-text", "source_sha256": source_hash,
            "pages": [{"page": i, "text": data["pages"][i - 1]} for i in sorted(wanted)],
            "truncated": False, "visual_math_check": "required separately"}


def locate(root: Path, name: str, query: str | list[str], limit: int = 12) -> dict:
    """Small literal-search result for navigation, never a substitute for a reading unit."""
    batch = isinstance(query, list)
    terms = query if batch else [query]
    if (not 1 <= len(terms) <= 16 or not 1 <= limit <= 50 or
            any(not isinstance(term, str) or not term.strip() for term in terms)):
        raise CacheError("Use 1-16 nonempty literal queries and --limit between 1 and 50.")
    unique = {}
    for term in terms:
        unique.setdefault(term.casefold(), term)
    terms = list(unique.values())
    source = source_file(root, name)
    source_hash = digest(source.read_bytes())
    data = load_cache(cache_path(root, source_hash), source_hash)
    found = []
    total = 0
    patterns = [re.compile(re.escape(term), re.IGNORECASE) for term in terms]
    counts = [0] * len(terms)
    returned = [0] * len(terms)
    for page_number, page in enumerate(data["pages"], 1):
        for line_number, line in enumerate(page.splitlines(), 1):
            hits = [(index, match) for index, pattern in enumerate(patterns)
                    if (match := pattern.search(line)) is not None]
            if not hits:
                continue
            total += 1
            for index, _ in hits:
                counts[index] += 1
            if len(found) < limit:
                start = max(0, min(match.start() for _, match in hits) - 60)
                snippet = line[start:start + 240]
                item = {"page": page_number, "line": line_number, "snippet": snippet,
                        "snippet_truncated": start > 0 or start + len(snippet) < len(line)}
                if batch:
                    item["matched_queries"] = [terms[index] for index, _ in hits]
                found.append(item)
                for index, _ in hits:
                    returned[index] += 1
    if digest(source.read_bytes()) != source_hash:
        raise CacheError("Source changed while locating text; run prepare again.")
    result = {"kind": "source-locations-only", "source_sha256": source_hash,
              "matching_lines": total, "returned_lines": len(found), "more_matches": total > len(found),
              "matches": found, "next_step": "read the full relevant page range; verify math/figures visually"}
    if batch:
        result["queries"] = [{"query": term, "matching_lines": counts[index],
                              "returned_lines": returned[index], "more_matches": counts[index] > returned[index]}
                             for index, term in enumerate(terms)]
    else:
        result["query"] = query
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    for mode in ("prepare", "read", "locate"):
        sub = modes.add_parser(mode)
        sub.add_argument("--root", required=True)
        sub.add_argument("--source", required=True)
        if mode == "prepare":
            sub.add_argument("--pdftotext", default="pdftotext")
        elif mode == "read":
            sub.add_argument("--pages", required=True)
        else:
            sub.add_argument("--query", action="append", required=True,
                             help="Literal search; repeat for one deduplicated batch (at most 16 queries).")
            sub.add_argument("--limit", type=int, default=12, help="Maximum returned lines across all queries (1-50).")
    args = parser.parse_args()
    try:
        root = Path(args.root).resolve(strict=True)
        if not root.is_dir():
            raise CacheError("Root must be a paper workspace directory.")
        if args.mode == "prepare":
            result = prepare(root, args.source, args.pdftotext)
        elif args.mode == "read":
            result = read_pages(root, args.source, args.pages)
        else:
            queries = args.query[0] if len(args.query) == 1 else args.query
            result = locate(root, args.source, queries, args.limit)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (CacheError, OSError, UnicodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
