"""Book assembly behavior using Pandoc-shaped ASTs, without external tools."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from test_build_pdf import pdf, TEST_TEMP


def document(name, target=None, image=None):
    blocks = [{"t": "Header", "c": [1, ["definition", [], []], [{"t": "Str", "c": name}]]}]
    for kind, value in (("Link", target), ("Image", image)):
        if value:
            blocks.append({"t": "Para", "c": [{"t": kind, "c": [["", [], []],
                [{"t": "Str", "c": "说明"}], [value, ""]]}]})
    return {"pandoc-api-version": [1, 23, 1], "meta": {}, "blocks": blocks}


class BookTests(unittest.TestCase):
    def setUp(self):
        TEST_TEMP.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=TEST_TEMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "chapters").mkdir()
        self.work = self.root / "build"
        self.work.mkdir()
        self.a = self.root / "chapters/a.md"
        self.b = self.root / "chapters/b.md"
        self.a.write_text("# 定义 {#definition}\n", encoding="utf-8")
        self.b.write_text("# 证明 {#definition}\n", encoding="utf-8")
        self.data = {"schema_version": 1, "title": "中文讲义", "chapters": [
            {"id": "a", "file": "chapters/a.md"}, {"id": "b", "file": "chapters/b.md"}]}

    def load(self, data=None):
        (self.root / "book.json").write_text(json.dumps(data or self.data), encoding="utf-8")
        return pdf.load_book(self.root, "book.json")

    def parse(self, docs):
        def execute(command, cwd):
            return subprocess.CompletedProcess(command, 0, json.dumps(copy.deepcopy(docs[Path(command[1]).name])), "")
        return patch.object(pdf, "run", side_effect=execute)

    def test_cross_chapter_same_named_headers_and_local_links(self):
        _, data, chapters = self.load()
        with self.parse({"a.md": document("A", "b.md#definition"), "b.md": document("B", "#definition")}):
            output = pdf.assemble_book(self.root, data, chapters, self.work, "pandoc")
        result = json.loads(output.read_text(encoding="utf-8"))
        headers = [n["c"][1][0] for n in pdf.nodes(result) if n["t"] == "Header"]
        links = [n["c"][2][0] for n in pdf.nodes(result) if n["t"] == "Link"]
        self.assertEqual(headers, ["a--definition", "b--definition"])
        self.assertEqual(links, ["#b--definition", "#b--definition"])
        self.assertEqual(self.a.read_text(encoding="utf-8"), "# 定义 {#definition}\n")

    def test_relative_image_resolves_against_chapter_not_cwd(self):
        (self.root / "figures").mkdir()
        figure = self.root / "figures/a.pdf"
        figure.write_bytes(b"%PDF-fixture")
        _, data, chapters = self.load()
        with self.parse({"a.md": document("A", image="../figures/a.pdf"), "b.md": document("B")}):
            output = pdf.assemble_book(self.root, data, chapters, self.work, "pandoc")
        images = [n for n in pdf.nodes(json.loads(output.read_text(encoding="utf-8"))) if n["t"] == "Image"]
        self.assertEqual(images[0]["c"][2][0], figure.as_posix())

    def test_missing_anchor_rejected_instead_of_silent_broken_pdf_link(self):
        _, data, chapters = self.load()
        with self.parse({"a.md": document("A", "b.md#typo"), "b.md": document("B")}):
            with self.assertRaisesRegex(pdf.BuildError, "Unknown book anchor"):
                pdf.assemble_book(self.root, data, chapters, self.work, "pandoc")

    def test_duplicate_chapter_id_or_path_rejected(self):
        for field in ("id", "file"):
            data = copy.deepcopy(self.data)
            data["chapters"][1][field] = data["chapters"][0][field]
            with self.subTest(field=field), self.assertRaisesRegex(pdf.BuildError, "Duplicate chapter"):
                self.load(data)

    def test_chapter_traversal_missing_file_and_invalid_metadata(self):
        for field, value in (("file", "../outside.md"), ("file", "missing.md"), ("id", "Bad ID")):
            data = copy.deepcopy(self.data)
            data["chapters"][0][field] = value
            with self.subTest(value=value), self.assertRaises(pdf.BuildError):
                self.load(data)
        data = copy.deepcopy(self.data)
        data["title"] = ["wrong type"]
        with self.assertRaisesRegex(pdf.BuildError, "metadata"):
            self.load(data)

    def test_remote_image_not_fetched_at_compile_time(self):
        _, data, chapters = self.load()
        with self.parse({"a.md": document("A", image="https://example.invalid/image.png"), "b.md": document("B")}):
            with self.assertRaisesRegex(pdf.BuildError, "Materialize remote media"):
                pdf.assemble_book(self.root, data, chapters, self.work, "pandoc")

    def test_assembly_keeps_all_fragments_in_manifest_order(self):
        chapters = [(f"c{i}", self.a if i == 0 else self.root / f"c{i}.md") for i in range(121)]
        with patch.object(pdf, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(document("单元")), "")):
            output = pdf.assemble_book(self.root, {}, chapters, self.work, "pandoc")
        result = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(len(result["blocks"]), 121)
        self.assertEqual(result["blocks"][-1]["c"][0][0], "chapter-c120")

    def test_parser_failure_preserves_diagnostic(self):
        _, data, chapters = self.load()
        with patch.object(pdf, "run", return_value=subprocess.CompletedProcess([], 1, "", "parse failed")):
            with self.assertRaisesRegex(pdf.BuildError, "Unable to parse chapter"):
                pdf.assemble_book(self.root, data, chapters, self.work, "pandoc")
        self.assertEqual((self.work / "parse-a.log").read_text(), "parse failed")

    def test_compile_timeout_has_explicit_limits(self):
        import argparse
        with self.assertRaisesRegex(pdf.BuildError, "Compile timeout"):
            pdf.build(argparse.Namespace(timeout=0))

    def test_full_read_chapter_cap_accepts_10_rejects_11(self):
        def headings(n, level=1):
            return {"blocks": [{"t": "Header", "c": [level, [str(i), [], []], []]} for i in range(n)]}
        self.assertEqual(pdf.check_full_read_structure([headings(10)])["visible_chapters"], 10)
        for level in [1, 2]:
            with self.subTest(level=level), self.assertRaisesRegex(pdf.BuildError, "maximum is 10"):
                pdf.check_full_read_structure([headings(11, level)])

    def test_full_read_counts_visible_chapters_not_fragment_files(self):
        docs = [document("one chapter")] + [{"blocks": [{"t": "Para", "c": [
            {"t": "Str", "c": "continuous proof"}]}]} for _ in range(120)]
        self.assertEqual(pdf.check_full_read_structure(docs)["visible_chapters"], 1)

    def test_raw_tex_cannot_hide_extra_chapters(self):
        for raw in [r"\section{extra}", r"\chapter*{extra}", r"\part[short]{extra}"]:
            with self.subTest(raw=raw), self.assertRaisesRegex(pdf.BuildError, "Markdown chapter headings"):
                pdf.check_full_read_structure([{"blocks": [{"t": "RawBlock", "c": ["latex", raw]}]}])


if __name__ == "__main__":
    unittest.main()
