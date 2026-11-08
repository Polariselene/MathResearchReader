"""Cache behavior, invalidation, page selection and failure safety without PDF dependencies."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from test_build_pdf import TEST_TEMP

SCRIPT = Path(__file__).resolve().parents[1] / "skills/math-research-reader/scripts/reading_cache.py"
SPEC = importlib.util.spec_from_file_location("mrr_reading_cache", SCRIPT)
cache = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cache)


class ReadingCacheTests(unittest.TestCase):
    def setUp(self):
        TEST_TEMP.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=TEST_TEMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "paper.pdf"
        self.source.write_bytes(b"%PDF-local-test-original")
        self.tool = self.root / "extractor.exe"
        self.tool.write_bytes(b"test-extractor")
        self.version = "pdftotext test-version-1"
        self.extractions = 0
        self.extraction_fails = False
        self.change_source = False
        self.page_text = "first page α\fsecond page β\fthird page γ\f"
        tool = patch.object(cache.shutil, "which", return_value=str(self.tool))
        run = patch.object(cache, "command", side_effect=self.execute)
        tool.start()
        run.start()
        self.addCleanup(tool.stop)
        self.addCleanup(run.stop)

    def execute(self, command):
        if command[-1] == "-v":
            return subprocess.CompletedProcess(command, 0, "", self.version)
        self.extractions += 1
        Path(command[-1]).write_text(self.page_text, encoding="utf-8")
        if self.change_source:
            self.source.write_bytes(b"%PDF-changed-during-read")
        return subprocess.CompletedProcess(command, int(self.extraction_fails), "", "")

    def test_repeated_prepare_reuses_extraction_and_preserves_original(self):
        original = self.source.read_bytes()
        first = cache.prepare(self.root, "paper.pdf")
        second = cache.prepare(self.root, "paper.pdf")
        self.assertFalse(first["cache_hit"])
        self.assertTrue(second["cache_hit"])
        self.assertEqual(self.extractions, 1)
        self.assertEqual(self.source.read_bytes(), original)
        self.assertNotIn("pages_sha256", second)

    def test_selected_pages_are_complete_without_unrequested_pages(self):
        cache.prepare(self.root, "paper.pdf")
        result = cache.read_pages(self.root, "paper.pdf", "3,1-1,3")
        self.assertEqual(result["pages"], [{"page": 1, "text": "first page α"},
                                         {"page": 3, "text": "third page γ"}])
        self.assertFalse(result["truncated"])
        self.assertEqual(self.extractions, 1)

    def test_invalid_ranges_do_not_silently_clip_a_proof(self):
        cache.prepare(self.root, "paper.pdf")
        for selection in ["0", "4", "3-2", "1-4", "", "x", "1-2-3"]:
            with self.subTest(selection=selection), self.assertRaises(cache.CacheError):
                cache.read_pages(self.root, "paper.pdf", selection)

    def test_changed_source_requires_new_cache(self):
        first = cache.prepare(self.root, "paper.pdf")
        self.source.write_bytes(b"%PDF-new-version")
        with self.assertRaises(cache.CacheError):
            cache.read_pages(self.root, "paper.pdf", "1")
        second = cache.prepare(self.root, "paper.pdf")
        self.assertNotEqual(first["source_sha256"], second["source_sha256"])
        self.assertEqual(self.extractions, 2)

    def test_changed_extractor_invalidates_cache(self):
        cache.prepare(self.root, "paper.pdf")
        self.version = "pdftotext test-version-2"
        self.assertFalse(cache.prepare(self.root, "paper.pdf")["cache_hit"])
        self.tool.write_bytes(b"changed-binary")
        self.assertFalse(cache.prepare(self.root, "paper.pdf")["cache_hit"])
        self.assertEqual(self.extractions, 3)

    def test_cache_corruption_is_detected_then_repaired(self):
        result = cache.prepare(self.root, "paper.pdf")
        path = self.root / result["cache"]
        data = json.loads(path.read_text(encoding="utf-8"))
        data["pages"][0] = "wrong text"
        path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(cache.CacheError):
            cache.read_pages(self.root, "paper.pdf", "1")
        self.assertFalse(cache.prepare(self.root, "paper.pdf")["cache_hit"])
        self.assertEqual(cache.read_pages(self.root, "paper.pdf", "1")["pages"][0]["text"], "first page α")

    def test_failure_or_concurrent_source_change_never_publishes_cache(self):
        for mode in ["extraction_fails", "change_source"]:
            setattr(self, mode, True)
            with self.assertRaises(cache.CacheError):
                cache.prepare(self.root, "paper.pdf")
            self.assertEqual(list((self.root / ".mrr/source-cache").glob("*")), [])
            setattr(self, mode, False)

    def test_workspace_path_escape_is_rejected(self):
        for name in ["../paper.pdf", str(self.source)]:
            with self.subTest(name=name), self.assertRaises(cache.CacheError):
                cache.prepare(self.root, name)

    def test_cache_alias_cannot_redirect_a_write_to_original(self):
        original = self.source.read_bytes()
        with patch.object(cache, "inside", return_value=self.source):
            with self.assertRaisesRegex(cache.CacheError, "must not follow links"):
                cache.cache_path(self.root, "test-hash")
        self.assertEqual(self.source.read_bytes(), original)

    def test_empty_page_is_preserved_and_not_mistaken_for_absent_page(self):
        self.page_text = "first\f\fthird\f"
        result = cache.prepare(self.root, "paper.pdf")
        self.assertEqual(result["empty_pages"], [2])
        self.assertEqual(result["pages"], 3)
        self.assertEqual(cache.read_pages(self.root, "paper.pdf", "2")["pages"], [{"page": 2, "text": ""}])

    def test_locator_returns_bounded_locations_and_complete_match_count(self):
        self.page_text = "Alpha definition\nother line\fALPHA theorem\falpha proof\f"
        cache.prepare(self.root, "paper.pdf")
        result = cache.locate(self.root, "paper.pdf", "alpha", 2)
        self.assertEqual(result["matching_lines"], 3)
        self.assertEqual([m["page"] for m in result["matches"]], [1, 2])
        self.assertTrue(result["more_matches"])
        self.assertNotIn("pages", result)
        self.assertEqual(self.extractions, 1)

    def test_locator_marks_snippet_cropping_without_truncating_page_reads(self):
        text = "x" * 300 + "TARGET" + "y" * 300
        self.page_text = text + "\f"
        cache.prepare(self.root, "paper.pdf")
        result = cache.locate(self.root, "paper.pdf", "TARGET")
        hit = result["matches"][0]
        self.assertTrue(hit["snippet_truncated"])
        self.assertIn("TARGET", hit["snippet"])
        self.assertLessEqual(len(hit["snippet"]), 240)
        self.assertEqual(cache.read_pages(self.root, "paper.pdf", "1")["pages"][0]["text"], text)

    def test_locator_handles_no_match_and_rejects_invalid_requests(self):
        cache.prepare(self.root, "paper.pdf")
        self.assertEqual(cache.locate(self.root, "paper.pdf", "not-present")["matching_lines"], 0)
        for query, limit in [(" ", 12), ("x", 0), ("x", 51)]:
            with self.subTest(query=query, limit=limit), self.assertRaises(cache.CacheError):
                cache.locate(self.root, "paper.pdf", query, limit)

    def test_batch_locator_deduplicates_lines_and_loads_cache_once(self):
        self.page_text = "Alpha and Beta\nAlpha only\fBeta only\f"
        cache.prepare(self.root, "paper.pdf")
        with patch.object(cache, "load_cache", wraps=cache.load_cache) as loader:
            result = cache.locate(self.root, "paper.pdf", ["Alpha", "Beta", "ALPHA"], 3)
        self.assertEqual(loader.call_count, 1)
        self.assertEqual(result["matching_lines"], 3)
        self.assertEqual(len(result["matches"]), 3)
        self.assertEqual(result["matches"][0]["matched_queries"], ["Alpha", "Beta"])
        self.assertEqual([(q["query"], q["matching_lines"]) for q in result["queries"]], [("Alpha", 2), ("Beta", 2)])
        self.assertFalse(result["more_matches"])
        self.assertEqual(self.extractions, 1)

    def test_batch_locator_limit_reports_each_omitted_query_without_clipping_reads(self):
        self.page_text = "Alpha\nAlpha\fBeta\f"
        cache.prepare(self.root, "paper.pdf")
        result = cache.locate(self.root, "paper.pdf", ["Alpha", "Beta", "absent"], 1)
        self.assertEqual(result["returned_lines"], 1)
        self.assertEqual(result["matching_lines"], 3)
        self.assertEqual(result["queries"][1], {"query": "Beta", "matching_lines": 1,
                                               "returned_lines": 0, "more_matches": True})
        self.assertFalse(result["queries"][2]["more_matches"])
        self.assertEqual(cache.read_pages(self.root, "paper.pdf", "1-2")["pages"],
                         [{"page": 1, "text": "Alpha\nAlpha"}, {"page": 2, "text": "Beta"}])

    def test_batch_locator_rejects_invalid_queries_before_cache_access(self):
        for queries in [[], [""], ["Alpha", 7], ["x"] * 17]:
            with self.subTest(queries=queries), patch.object(cache, "load_cache") as loader:
                with self.assertRaises(cache.CacheError):
                    cache.locate(self.root, "paper.pdf", queries)
                loader.assert_not_called()

    def test_locator_cli_preserves_single_query_and_accepts_batch(self):
        cache.prepare(self.root, "paper.pdf")
        base = ["reading_cache.py", "locate", "--root", str(self.root), "--source", "paper.pdf"]
        for args, batch in [(["--query", "first"], False),
                            (["--query", "first", "--query", "second"], True)]:
            with self.subTest(batch=batch), patch.object(cache.sys, "argv", base + args), \
                    patch("sys.stdout", new_callable=io.StringIO) as output:
                self.assertEqual(cache.main(), 0)
                result = json.loads(output.getvalue())
                self.assertEqual("queries" in result, batch)
                self.assertEqual("query" in result, not batch)


if __name__ == "__main__":
    unittest.main()
