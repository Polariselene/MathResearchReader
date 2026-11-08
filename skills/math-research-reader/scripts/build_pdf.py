#!/usr/bin/env python3
"""Build Chinese PDF from Markdown. Standard library only; no installation or QA claims."""
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
from urllib.parse import unquote, urlsplit


class BuildError(Exception):
    pass


FULL_READ_MIN_PAGES = 90
FULL_READ_MAX_CHAPTERS = 10
# Recognize older task contracts too; their exports now use the current 90-page gate.
LEGACY_FULL_READ_SCOPE_PAGES = 70


def check_full_read_structure(documents: list[dict]) -> dict:
    levels = []
    for doc in documents:
        if not isinstance(doc, dict) or not isinstance(doc.get("blocks"), list):
            raise BuildError("Cannot verify full-read chapter structure.")
        for node in nodes(doc["blocks"]):
            if node["t"] == "Header":
                levels.append(node["c"][0])
            elif node["t"] in {"RawBlock", "RawInline"}:
                fmt, raw = node["c"]
                if fmt in {"tex", "latex"} and re.search(r"\\(?:part|chapter|section)\*?\s*(?:\[[^\]]*\]\s*)?\{", raw):
                    raise BuildError("Use Markdown chapter headings for verifiable full-read structure, not raw TeX section commands.")
    level = min(levels) if levels else None
    count = levels.count(level) if levels else 1
    if count > FULL_READ_MAX_CHAPTERS:
        raise BuildError(f"Full-read document has {count} top-level chapters; maximum is {FULL_READ_MAX_CHAPTERS}. "
                         "Reorganize the teaching narrative; do not merely hide headings.")
    return {"status": "pass", "visible_chapters": count, "heading_level": level,
            "maximum": FULL_READ_MAX_CHAPTERS, "scope": "Pandoc heading structure; final PDF outline still needs visual review"}


def check_full_read_pages(path: Path, pdfinfo: str, root: Path) -> dict:
    """Fail closed before publication. Page count does not certify teaching quality."""
    result = run([pdfinfo, str(path)], root)
    match = re.search(r"^Pages:\s*(\d+)\s*$", result.stdout, re.MULTILINE)
    if result.returncode or not match:
        raise BuildError("Cannot verify full-read PDF pages with pdfinfo; publication stopped.")
    pages = int(match.group(1))
    if pages < FULL_READ_MIN_PAGES:
        raise BuildError(f"Full-read PDF has {pages} pages; requires at least {FULL_READ_MIN_PAGES}. "
                         "Expand relevant teaching content and rebuild; do not pad pages.")
    return {"pages": pages, "minimum": FULL_READ_MIN_PAGES, "status": "pass",
            "scope": "physical PDF pages only; substantive teaching pages require content review"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def full_read_scope(root: Path, book: dict | None, explicit: bool) -> tuple[list[str], dict[str, str]]:
    """Inherit the task contract even when an export command omits the mode flag."""
    reasons = ["cli"] if explicit else []
    if book and book.get("task_mode") == "deep-read":
        reasons.append("book")
    snapshots = {}
    unfinished = []
    for filename in (".mrr/state.json", ".mrr/reading-plan.json"):
        if not (root / filename).exists():
            continue
        path = scoped(root, filename)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as exc:
            raise BuildError(f"Invalid task contract: {filename}; repair it before export.") from exc
        if not isinstance(data, dict):
            raise BuildError(f"Task contract must be an object: {filename}")
        snapshots[filename] = digest(path)
        manuscript = data.get("first_manuscript_status")
        if manuscript is not None:
            if manuscript not in ("planned", "composing", "content-reviewed"):
                raise BuildError(f"Invalid first_manuscript_status in {filename}.")
            if manuscript != "content-reviewed":
                unfinished.append(filename)
        contract = data.get("delivery_contract", {})
        minimum = data.get("minimum_teaching_pages")
        if isinstance(contract, dict):
            minimum = contract.get("minimum_teaching_pages", minimum)
        if (data.get("mode") == "deep-read" or data.get("task_mode") == "deep-read" or
                (isinstance(minimum, (int, float)) and minimum >= LEGACY_FULL_READ_SCOPE_PAGES)):
            reasons.append(filename)
    if reasons and unfinished:
        raise BuildError("Complete and review the first full teaching manuscript before PDF export; "
                         "do not compile a short book to drive page-filling iterations.")
    return reasons, snapshots


def scoped(root: Path, value: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise BuildError(f"Use a relative path without '..': {value}")
    result = (root / relative).resolve()
    if not result.is_relative_to(root):
        raise BuildError(f"Path escapes workspace: {value}")
    if any(part.lower() in {"source", ".git", ".agents", ".codex"}
           for part in (*relative.parts, *result.relative_to(root).parts)):
        raise BuildError(f"Protected path: {value}")
    return result


def executable(value: str) -> str:
    found = shutil.which(value)
    if not found:
        raise BuildError(f"Missing executable: {value}. Install it or pass its executable path.")
    return str(Path(found).resolve())


def run(command: list[str], cwd: Path, timeout: int = 180) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    # Some Windows sandbox TEMP paths contain braces that break TeX media names.
    # Keep compiler intermediates in the declared, validated build directory.
    if (cwd / "build").is_dir():
        environment.update({key: str(cwd / "build") for key in ("TEMP", "TMP", "TMPDIR")})
    try:
        return subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout, check=False, env=environment)
    except subprocess.TimeoutExpired as exc:
        raise BuildError(f"Command timed out after {timeout} seconds: {command[0]}") from exc


def diagnose(args, root: Path) -> dict:
    pandoc = executable(args.pandoc)
    xelatex = executable(args.xelatex)
    kpse = shutil.which("kpsewhich", path=str(Path(xelatex).parent) + os.pathsep + os.environ.get("PATH", ""))
    if not kpse:
        raise BuildError("Missing kpsewhich from the selected TeX installation.")
    ctex = run([kpse, "ctexart.cls"], root)
    if ctex.returncode or not ctex.stdout.strip():
        raise BuildError("Missing ctexart.cls. Install ctex in the selected TeX installation.")
    versions = {}
    for name, tool in (("pandoc", pandoc), ("xelatex", xelatex)):
        result = run([tool, "--version"], root)
        if result.returncode:
            raise BuildError(f"Unable to run {name}: {result.stderr.strip()}")
        versions[name] = result.stdout.splitlines()[0]
    return {"pandoc": pandoc, "xelatex": xelatex, "ctex": ctex.stdout.strip(), "versions": versions}


def load_book(root: Path, filename: str) -> tuple[Path, dict, list[tuple[str, Path]]]:
    path = scoped(root, filename)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise BuildError("Book must be an object with schema_version=1.")
    if "task_mode" in data and data["task_mode"] not in (
            "deep-read", "proof-audit", "explain", "compare", "export"):
        raise BuildError("Unsupported book task_mode.")
    rows = data.get("chapters")
    if not isinstance(rows, list) or not rows:
        raise BuildError("Book needs a nonempty ordered chapters list.")
    chapters, ids, paths = [], set(), set()
    for row in rows:
        if not isinstance(row, dict):
            raise BuildError("Each chapter must have id and file.")
        chapter_id, filename = row.get("id"), row.get("file")
        if not isinstance(chapter_id, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", chapter_id):
            raise BuildError("Chapter id must start with a letter and use lowercase letters, digits or hyphens.")
        if not isinstance(filename, str):
            raise BuildError("Chapter file must be a workspace-relative Markdown path.")
        source = scoped(root, filename)
        if chapter_id in ids or source in paths:
            raise BuildError("Duplicate chapter id or file in book.")
        if source.suffix.lower() != ".md" or not source.is_file():
            raise BuildError(f"Missing chapter Markdown: {filename}")
        source.read_text(encoding="utf-8")
        ids.add(chapter_id)
        paths.add(source)
        chapters.append((chapter_id, source))
    for key in ("title", "author", "date", "lang"):
        if key in data and not isinstance(data[key], str):
            raise BuildError(f"Book metadata '{key}' must be a string.")
    return path, data, chapters


def nodes(value):
    if isinstance(value, dict):
        if "t" in value:
            yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def assemble_book(root: Path, data: dict, chapters: list[tuple[str, Path]],
                  work: Path, pandoc: str) -> Path:
    """Use Pandoc's Markdown parser, not regex, for namespace/link/media rewriting."""
    docs, anchors = {}, {}
    attr_positions = {"Header": 1, "Div": 0, "Span": 0, "CodeBlock": 0,
                      "Code": 0, "Image": 0, "Link": 0, "Table": 0, "Figure": 0}
    for chapter_id, source in chapters:
        result = run([pandoc, str(source), "--from=markdown+tex_math_dollars+link_attributes", "--to=json"], root)
        (work / f"parse-{chapter_id}.log").write_text(result.stderr, encoding="utf-8")
        if result.returncode:
            raise BuildError(f"Unable to parse chapter {source}; see {work}.")
        try:
            doc = json.loads(result.stdout)
            if not isinstance(doc.get("blocks"), list) or "pandoc-api-version" not in doc:
                raise ValueError("Not a Pandoc document")
        except (ValueError, AttributeError) as exc:
            raise BuildError(f"Invalid parser output for {source}") from exc
        anchor_map = {}
        for node in nodes(doc["blocks"]):
            position = attr_positions.get(node["t"])
            if position is None:
                continue
            attr = node["c"][position]
            original_id = attr[0]
            if original_id:
                if original_id in anchor_map:
                    raise BuildError(f"Duplicate anchor '{original_id}' in {source}")
                anchor_map[original_id] = chapter_id + "--" + original_id
                attr[0] = anchor_map[original_id]
        docs[source], anchors[source] = doc, anchor_map
    chapter_targets = {source: "chapter-" + chapter_id for chapter_id, source in chapters}
    for _, source in chapters:
        for node in nodes(docs[source]["blocks"]):
            if node["t"] not in {"Link", "Image"}:
                continue
            target = node["c"][2]
            url = urlsplit(target[0])
            if url.scheme or url.netloc:
                if node["t"] == "Link" and url.scheme in {"https", "http", "mailto"}:
                    continue
                raise BuildError(f"Materialize remote media or unsupported URL first: {target[0]}")
            if url.query:
                raise BuildError(f"Query strings in local book links are unsupported: {target[0]}")
            destination = (source.parent / unquote(url.path)).resolve() if url.path else source
            if not destination.is_relative_to(root):
                raise BuildError(f"Book resource escapes workspace: {target[0]}")
            if node["t"] == "Image":
                if not destination.is_file():
                    raise BuildError(f"Missing book image: {target[0]}")
                target[0] = destination.as_posix()
            elif not url.path or destination.suffix.lower() == ".md":
                if destination not in docs:
                    raise BuildError(f"Linked chapter is not in book: {target[0]}")
                fragment = unquote(url.fragment)
                if fragment:
                    if fragment not in anchors[destination]:
                        raise BuildError(f"Unknown book anchor: {target[0]}")
                    target[0] = "#" + anchors[destination][fragment]
                else:
                    target[0] = "#" + chapter_targets[destination]
            else:
                if not destination.is_file():
                    raise BuildError(f"Missing local book link: {target[0]}")
                target[0] = destination.as_uri() + ("#" + url.fragment if url.fragment else "")
    first = docs[chapters[0][1]]
    combined = {"pandoc-api-version": first["pandoc-api-version"], "meta": dict(first.get("meta", {})), "blocks": []}
    for key in ("title", "author", "date", "lang"):
        if key in data:
            combined["meta"][key] = {"t": "MetaString", "c": data[key]}
    for _, source in chapters:
        doc = docs[source]
        if doc["pandoc-api-version"] != combined["pandoc-api-version"]:
            raise BuildError("Pandoc AST versions differ between chapters.")
        combined["blocks"].append({"t": "Div", "c": [[chapter_targets[source], [], []], doc["blocks"]]})
    assembled = work / "book.json"
    assembled.write_text(json.dumps(combined, ensure_ascii=False), encoding="utf-8")
    return assembled


def build(args) -> dict:
    compile_timeout = getattr(args, "timeout", 600)
    if not isinstance(compile_timeout, int) or not 1 <= compile_timeout <= 3600:
        raise BuildError("Compile timeout must be between 1 and 3600 seconds.")
    root = Path(args.root).resolve(strict=True)
    if not root.is_dir():
        raise BuildError("Root must be a directory.")
    if args.check:
        tools = diagnose(args, root)
        return {"status": "tools-available", "font_check": "requires-build", **tools}
    book_file, book_data, chapters = None, None, None
    if getattr(args, "book", None):
        if args.input:
            raise BuildError("Choose either --book or --input.")
        book_file, book_data, chapters = load_book(root, args.book)
        inputs = [source for _, source in chapters]
    elif not args.input:
        raise BuildError("At least one --input Markdown file is required.")
    else:
        inputs = [scoped(root, item) for item in args.input]
    full_read_sources, task_snapshot = full_read_scope(root, book_data, getattr(args, "full_read", False))
    full_read = bool(full_read_sources)
    pdfinfo = executable(getattr(args, "pdfinfo", "pdfinfo")) if full_read else None
    for path in inputs:
        if path.suffix.lower() != ".md" or not path.is_file():
            raise BuildError(f"Input is not an existing Markdown file: {path}")
        path.read_text(encoding="utf-8")
    output = scoped(root, args.output)
    if output.suffix.lower() != ".pdf":
        raise BuildError("Output must have .pdf extension.")
    if output.exists() and not args.replace:
        raise BuildError(f"Output exists; review it and use --replace: {output}")
    output_before = digest(output) if output.exists() else None
    tools = diagnose(args, root)
    header = Path(__file__).resolve().parents[1] / "assets" / "pdf-header.tex"
    build_root = scoped(root, "build")
    build_root.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="pdf-", dir=build_root))
    target = work / "report.pdf"
    command = [tools["pandoc"], *map(str, inputs), "--from=markdown+tex_math_dollars+link_attributes",
               "--standalone", "--table-of-contents", "--number-sections",
               "--pdf-engine=" + tools["xelatex"], "--pdf-engine-opt=-no-shell-escape",
               "--include-in-header=" + str(header), "-V", "documentclass=ctexart",
               "-V", "classoption=fontset=fandol", "-V", "papersize=a4", "-V", "fontsize=11pt",
               "-V", "geometry:margin=23mm", "--resource-path=" + os.pathsep.join(
                   dict.fromkeys([str(root), *(str(p.parent) for p in inputs)])), "--output=" + str(target)]
    if args.cjk_font:
        command.extend(["-V", "CJKmainfont=" + args.cjk_font])
    manifest = {"schema_version": 1, "status": "building", "visual_qa": "unverified",
                "full_read": full_read,
                "full_read_sources": full_read_sources, "task_snapshot": task_snapshot,
                "inputs": [{"path": str(p.relative_to(root)), "sha256": digest(p)} for p in inputs],
                "header_sha256": digest(header), "tools": tools, "command": command,
                "builder_sha256": digest(Path(__file__)),
                "output": str(output.relative_to(root))}
    manifest_path = work / "manifest.json"
    try:
        if chapters:
            assembled = assemble_book(root, book_data, chapters, work, tools["pandoc"])
            command[1:1 + len(inputs)] = [str(assembled)]
            command[command.index("--from=markdown+tex_math_dollars+link_attributes")] = "--from=json"
            manifest["book"] = {"path": str(book_file.relative_to(root)), "sha256": digest(book_file),
                                "chapters": [chapter_id for chapter_id, _ in chapters]}
            manifest["assembled_sha256"] = digest(assembled)
            manifest["command"] = command
        if full_read:
            manifest["structure_gate"] = {"status": "unverified", "maximum": FULL_READ_MAX_CHAPTERS}
            try:
                if chapters:
                    documents = [json.loads(assembled.read_text(encoding="utf-8"))]
                else:
                    documents = []
                    for i, source in enumerate(inputs):
                        parsed = run([tools["pandoc"], str(source), "--from=markdown+tex_math_dollars+link_attributes", "--to=json"], root)
                        (work / f"structure-{i}.log").write_text(parsed.stderr, encoding="utf-8")
                        if parsed.returncode:
                            raise BuildError("Cannot parse full-read chapter structure.")
                        documents.append(json.loads(parsed.stdout))
                manifest["structure_gate"] = check_full_read_structure(documents)
            except (BuildError, ValueError):
                manifest["structure_gate"]["status"] = "fail"
                raise
        result = run(command, root, timeout=compile_timeout)
        log = result.stdout + "\n" + result.stderr
        (work / "build.log").write_text(log, encoding="utf-8")
        manifest["exit_code"] = result.returncode
        if result.returncode or not target.is_file():
            raise BuildError(f"PDF compilation failed. See {work / 'build.log'}")
        if "Missing character:" in log:
            raise BuildError(f"Missing glyphs detected. See {work / 'build.log'}")
        if not target.read_bytes().startswith(b"%PDF-"):
            raise BuildError("Compiler did not produce a PDF file.")
        if full_read:
            manifest["page_gate"] = {"status": "unverified", "minimum": FULL_READ_MIN_PAGES}
            try:
                manifest["page_gate"] = check_full_read_pages(target, pdfinfo, root)
            except BuildError:
                manifest["page_gate"]["status"] = "fail"
                raise
        if any(digest(root / item["path"]) != item["sha256"] for item in manifest["inputs"]):
            raise BuildError("Source Markdown changed during build; recheck it before publishing.")
        if book_file and digest(book_file) != manifest["book"]["sha256"]:
            raise BuildError("Book manifest changed during build.")
        current_scope, current_snapshot = full_read_scope(root, book_data, getattr(args, "full_read", False))
        if current_scope != full_read_sources or current_snapshot != task_snapshot:
            raise BuildError("Task contract changed during build; recheck it before publishing.")
        if digest(header) != manifest["header_sha256"]:
            raise BuildError("PDF template changed during build.")
        if (digest(output) if output.exists() else None) != output_before:
            raise BuildError("Output changed during build; preserving the other writer's version.")
        output.parent.mkdir(parents=True, exist_ok=True)
        # Copy then atomically replace; failed builds never replace an existing delivery.
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".pdf", delete=False) as staged:
            staged_path = Path(staged.name)
        try:
            shutil.copyfile(target, staged_path)
            os.replace(staged_path, output)
        finally:
            staged_path.unlink(missing_ok=True)
        manifest.update(status="built", output_sha256=digest(output))
    except (BuildError, OSError, ValueError) as exc:
        manifest.update(status="failed", error=str(exc))
        raise
    finally:
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "built", "output": str(output), "manifest": str(manifest_path),
            "visual_qa": "unverified"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--input", action="append")
    parser.add_argument("--book", help="Workspace-relative book JSON: ordered chapters and metadata.")
    parser.add_argument("--full-read", action="store_true",
                        help="Require at least 90 PDF pages and at most 10 visible chapters for a complete reading.")
    parser.add_argument("--pdfinfo", default="pdfinfo", help="Poppler pdfinfo for full-read page verification.")
    parser.add_argument("--output", default="exports/report.zh-CN.pdf")
    parser.add_argument("--pandoc", default="pandoc")
    parser.add_argument("--xelatex", default="xelatex")
    parser.add_argument("--cjk-font")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--timeout", type=int, default=600, help="PDF compile timeout in seconds (1–3600).")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args), ensure_ascii=False, indent=2))
        return 0
    except (BuildError, OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
