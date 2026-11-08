"""Behavioral tests for the single packaged helper; no Pandoc required."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/math-research-reader/scripts/build_pdf.py"
TEST_TEMP = Path(__file__).resolve().parents[1] / ".local-test/unit"
SPEC = importlib.util.spec_from_file_location("mrr_build_pdf", SCRIPT)
pdf = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pdf)


class BuildTests(unittest.TestCase):
    def setUp(self):
        TEST_TEMP.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=TEST_TEMP)
        self.root = Path(self.directory.name).resolve()
        self.source = self.root / "report.md"
        self.source.write_text("# 中文数学\n\n$C=I$.\n", encoding="utf-8")
        self.original = self.source.read_bytes()
        self.args = argparse.Namespace(root=str(self.root), input=["report.md"],
            output="exports/report.pdf", pandoc="pandoc", xelatex="xelatex",
            cjk_font=None, check=False, replace=False)
        self.tools = {"pandoc": "pandoc", "xelatex": "xelatex", "versions": {}}
        self.diagnostic = patch.object(pdf, "diagnose", return_value=self.tools)
        self.diagnostic.start()
        self.addCleanup(self.diagnostic.stop)
        self.addCleanup(self.directory.cleanup)

    def compile(self, command, cwd, **options):
        target = next(x.split("=", 1)[1] for x in command if x.startswith("--output="))
        Path(target).write_bytes(b"%PDF-1.7\nlocal-test\n")
        self.assertIn("--pdf-engine-opt=-no-shell-escape", command)
        return subprocess.CompletedProcess(command, 0, "", "")

    def test_success_preserves_markdown_and_keeps_qa_unverified(self):
        with patch.object(pdf, "run", side_effect=self.compile):
            result = pdf.build(self.args)
        self.assertEqual(self.source.read_bytes(), self.original)
        manifest = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "built")
        self.assertEqual(manifest["visual_qa"], "unverified")
        self.assertEqual(manifest["inputs"][0]["sha256"], pdf.digest(self.source))

    def test_existing_pdf_requires_explicit_replace(self):
        output = self.root / self.args.output
        output.parent.mkdir()
        output.write_bytes(b"original")
        with self.assertRaisesRegex(pdf.BuildError, "Output exists"):
            pdf.build(self.args)
        self.assertEqual(output.read_bytes(), b"original")

    def test_failed_compilation_preserves_previous_pdf(self):
        output = self.root / self.args.output
        output.parent.mkdir()
        output.write_bytes(b"original")
        self.args.replace = True
        with patch.object(pdf, "run", return_value=subprocess.CompletedProcess([], 1, "", "error")):
            with self.assertRaisesRegex(pdf.BuildError, "compilation failed"):
                pdf.build(self.args)
        self.assertEqual(output.read_bytes(), b"original")
        manifest = next((self.root / "build").glob("*/manifest.json"))
        self.assertEqual(json.loads(manifest.read_text())["status"], "failed")

    def test_missing_glyph_does_not_publish(self):
        def missing(command, cwd, **options):
            self.compile(command, cwd)
            return subprocess.CompletedProcess(command, 0, "", "Missing character: 中")
        with patch.object(pdf, "run", side_effect=missing):
            with self.assertRaisesRegex(pdf.BuildError, "Missing glyphs"):
                pdf.build(self.args)
        self.assertFalse((self.root / self.args.output).exists())

    def test_path_traversal_absolute_and_protected_paths_rejected(self):
        for value in ["../outside.pdf", str(self.root / "absolute.pdf"), "source/original.pdf",
                      ".git/data.pdf", ".agents/report.pdf"]:
            with self.subTest(value=value), self.assertRaises(pdf.BuildError):
                pdf.scoped(self.root, value)

    def test_output_symlink_cannot_escape_root(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as outside:
            link = self.root / "exports"
            try:
                link.symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("OS does not allow test symlinks")
            with self.assertRaisesRegex(pdf.BuildError, "escapes"):
                pdf.scoped(self.root, "exports/report.pdf")

    def test_missing_executable_fails_explicitly(self):
        with patch.object(pdf.shutil, "which", return_value=None):
            with self.assertRaisesRegex(pdf.BuildError, "Missing executable"):
                pdf.executable("unavailable-pandoc")

    def test_compiler_uses_workspace_temp_without_changing_process_env(self):
        (self.root / "build").mkdir()
        before = pdf.os.environ.copy()
        with patch.object(pdf.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")) as call:
            pdf.run(["compiler"], self.root)
        self.assertEqual(call.call_args.kwargs["env"]["TEMP"], str(self.root / "build"))
        self.assertEqual(pdf.os.environ.copy(), before)

    def test_check_only_creates_nothing(self):
        self.args.check = True
        self.assertEqual(pdf.build(self.args)["status"], "tools-available")
        self.assertEqual(list(self.root.iterdir()), [self.source])

    def test_invalid_input_never_invokes_compiler(self):
        self.args.input = ["missing.md"]
        with patch.object(pdf, "run") as run:
            with self.assertRaisesRegex(pdf.BuildError, "existing Markdown"):
                pdf.build(self.args)
            run.assert_not_called()

    def test_multiple_inputs_keep_requested_order(self):
        (self.root / "audit.md").write_text("# 审计\n", encoding="utf-8")
        self.args.input.append("audit.md")
        def ordered(command, cwd, **options):
            self.assertEqual(command[1:3], [str(self.source), str(self.root / "audit.md")])
            return self.compile(command, cwd)
        with patch.object(pdf, "run", side_effect=ordered):
            pdf.build(self.args)

    def test_input_edit_during_build_prevents_stale_publish(self):
        def edited(command, cwd, **options):
            result = self.compile(command, cwd)
            self.source.write_text("# 用户的新假设\n", encoding="utf-8")
            return result
        with patch.object(pdf, "run", side_effect=edited):
            with self.assertRaisesRegex(pdf.BuildError, "Markdown changed during build"):
                pdf.build(self.args)
        self.assertFalse((self.root / self.args.output).exists())

    def test_concurrent_output_edit_is_preserved(self):
        output = self.root / self.args.output
        output.parent.mkdir()
        output.write_bytes(b"old version")
        self.args.replace = True
        def edited(command, cwd, **options):
            result = self.compile(command, cwd)
            output.write_bytes(b"other writer")
            return result
        with patch.object(pdf, "run", side_effect=edited):
            with self.assertRaisesRegex(pdf.BuildError, "Output changed during build"):
                pdf.build(self.args)
        self.assertEqual(output.read_bytes(), b"other writer")

    def gated_run(self, pages=None, fail=False):
        def execute(command, cwd, **options):
            if "--to=json" in command:
                return subprocess.CompletedProcess(command, 0, json.dumps({"blocks": [
                    {"t": "Header", "c": [1, ["main", [], []], [{"t": "Str", "c": "正文"}]]}]}), "")
            if command[0] == "test-pdfinfo":
                return subprocess.CompletedProcess(command, int(fail),
                    "unreadable" if pages is None else f"Pages: {pages}\n", "")
            return self.compile(command, cwd, **options)
        return execute

    def test_full_read_rejects_89_pages_and_preserves_previous_output(self):
        self.args.full_read = True
        output = self.root / self.args.output
        output.parent.mkdir()
        output.write_bytes(b"previous reviewed document")
        self.args.replace = True
        with patch.object(pdf, "executable", return_value="test-pdfinfo"), \
             patch.object(pdf, "run", side_effect=self.gated_run(89)):
            with self.assertRaisesRegex(pdf.BuildError, "requires at least 90"):
                pdf.build(self.args)
        self.assertEqual(output.read_bytes(), b"previous reviewed document")
        manifest = json.loads(next((self.root / "build").glob("*/manifest.json")).read_text())
        self.assertEqual(manifest["page_gate"]["status"], "fail")

    def test_full_read_accepts_90_pages_without_certifying_visual_quality(self):
        self.args.full_read = True
        with patch.object(pdf, "executable", return_value="test-pdfinfo"), \
             patch.object(pdf, "run", side_effect=self.gated_run(90)):
            result = pdf.build(self.args)
        manifest = json.loads(Path(result["manifest"]).read_text())
        self.assertEqual(manifest["page_gate"]["pages"], 90)
        self.assertEqual(result["visual_qa"], "unverified")

    def test_full_read_unreadable_page_count_fails_closed(self):
        for pages, failed in [(None, False), (90, True)]:
            with self.subTest(pages=pages, failed=failed):
                with patch.object(pdf, "run", side_effect=self.gated_run(pages, failed)):
                    with self.assertRaisesRegex(pdf.BuildError, "Cannot verify"):
                        pdf.check_full_read_pages(self.source, "test-pdfinfo", self.root)

    def test_full_read_missing_pdfinfo_stops_before_compilation(self):
        self.args.full_read = True
        with patch.object(pdf, "executable", side_effect=pdf.BuildError("Missing executable")), \
             patch.object(pdf, "run") as run:
            with self.assertRaisesRegex(pdf.BuildError, "Missing executable"):
                pdf.build(self.args)
        run.assert_not_called()

    def test_book_deep_read_mode_enables_gate_without_cli_flag(self):
        self.args.input = None
        self.args.book = "book.json"
        book = {"schema_version": 1, "task_mode": "deep-read",
                "chapters": [{"id": "main", "file": "report.md"}]}
        (self.root / "book.json").write_text(json.dumps(book), encoding="utf-8")
        assembled = self.root / "assembled.json"
        assembled.write_text('{"blocks": []}', encoding="utf-8")
        with patch.object(pdf, "assemble_book", return_value=assembled), \
             patch.object(pdf, "executable", return_value="test-pdfinfo"), \
             patch.object(pdf, "run", side_effect=self.gated_run(30)):
            with self.assertRaisesRegex(pdf.BuildError, "requires at least 90"):
                pdf.build(self.args)
        self.assertFalse((self.root / self.args.output).exists())

    def test_invalid_book_mode_is_rejected(self):
        (self.root / "book.json").write_text(json.dumps({"schema_version": 1,
            "task_mode": "short-complete", "chapters": []}), encoding="utf-8")
        with self.assertRaisesRegex(pdf.BuildError, "task_mode"):
            pdf.load_book(self.root, "book.json")

    def test_workspace_state_enforces_gate_on_plain_input_export(self):
        (self.root / ".mrr").mkdir()
        (self.root / ".mrr/state.json").write_text('{"mode":"deep-read"}', encoding="utf-8")
        with patch.object(pdf, "executable", return_value="test-pdfinfo"), \
             patch.object(pdf, "run", side_effect=self.gated_run(40)):
            with self.assertRaisesRegex(pdf.BuildError, "requires at least 90"):
                pdf.build(self.args)
        self.assertFalse((self.root / self.args.output).exists())

    def test_plan_page_contract_enforces_gate_without_mode(self):
        (self.root / ".mrr").mkdir()
        (self.root / ".mrr/reading-plan.json").write_text(
            '{"delivery_contract":{"minimum_teaching_pages":90}}', encoding="utf-8")
        with patch.object(pdf, "executable", return_value="test-pdfinfo"), \
             patch.object(pdf, "run", side_effect=self.gated_run(89)):
            with self.assertRaisesRegex(pdf.BuildError, "requires at least 90"):
                pdf.build(self.args)

    def test_broken_workspace_state_does_not_silently_disable_gate(self):
        (self.root / ".mrr").mkdir()
        (self.root / ".mrr/state.json").write_text('{broken', encoding="utf-8")
        with patch.object(pdf, "run") as run:
            with self.assertRaisesRegex(pdf.BuildError, "Invalid task contract"):
                pdf.build(self.args)
        run.assert_not_called()

    def test_task_contract_change_during_build_preserves_output(self):
        (self.root / ".mrr").mkdir()
        state = self.root / ".mrr/state.json"
        state.write_text('{"mode":"export"}', encoding="utf-8")
        def changed(command, cwd, **options):
            result = self.compile(command, cwd, **options)
            state.write_text('{"mode":"deep-read"}', encoding="utf-8")
            return result
        with patch.object(pdf, "run", side_effect=changed):
            with self.assertRaisesRegex(pdf.BuildError, "Task contract changed"):
                pdf.build(self.args)
        self.assertFalse((self.root / self.args.output).exists())

    def test_legacy_70_71_page_contracts_inherit_current_90_page_gate(self):
        (self.root / ".mrr").mkdir()
        for minimum in [70, 71]:
            (self.root / ".mrr/state.json").write_text(
                json.dumps({"minimum_teaching_pages": minimum}), encoding="utf-8")
            with self.subTest(minimum=minimum), \
                 patch.object(pdf, "executable", return_value="test-pdfinfo"), \
                 patch.object(pdf, "run", side_effect=self.gated_run(89)):
                with self.assertRaisesRegex(pdf.BuildError, "requires at least 90"):
                    pdf.build(self.args)

    def test_plain_input_full_read_rejects_11_chapters_before_compilation(self):
        self.args.full_read = True
        def too_many(command, cwd, **options):
            self.assertIn("--to=json", command)
            return subprocess.CompletedProcess(command, 0, json.dumps({"blocks": [
                {"t": "Header", "c": [1, [str(i), [], []], []]} for i in range(11)]}), "")
        with patch.object(pdf, "executable", return_value="test-pdfinfo"), \
             patch.object(pdf, "run", side_effect=too_many):
            with self.assertRaisesRegex(pdf.BuildError, "maximum is 10"):
                pdf.build(self.args)
        self.assertFalse((self.root / self.args.output).exists())

    def test_first_manuscript_is_completed_before_full_read_export(self):
        (self.root / ".mrr").mkdir()
        state = self.root / ".mrr/state.json"
        for status in ("planned", "composing"):
            state.write_text(json.dumps({"mode": "deep-read", "first_manuscript_status": status}), encoding="utf-8")
            with self.subTest(status=status), patch.object(pdf, "run") as run, \
                 patch.object(pdf, "diagnose") as diagnose:
                with self.assertRaisesRegex(pdf.BuildError, "first full teaching manuscript"):
                    pdf.build(self.args)
                run.assert_not_called()
                diagnose.assert_not_called()

    def test_ready_first_manuscript_still_has_to_pass_actual_page_gate(self):
        (self.root / ".mrr").mkdir()
        (self.root / ".mrr/state.json").write_text(json.dumps({"mode": "deep-read",
            "first_manuscript_status": "content-reviewed"}), encoding="utf-8")
        with patch.object(pdf, "executable", return_value="test-pdfinfo"), \
             patch.object(pdf, "run", side_effect=self.gated_run(89)):
            with self.assertRaisesRegex(pdf.BuildError, "requires at least 90"):
                pdf.build(self.args)


if __name__ == "__main__":
    unittest.main()
