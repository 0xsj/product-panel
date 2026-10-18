#!/usr/bin/env python3
"""Focused format, link, embedding and file-write checks; no dependencies."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

SCRIPT = Path(__file__).with_name('render_panel.py')
spec = importlib.util.spec_from_file_location('render_panel', SCRIPT)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
EXAMPLE = SCRIPT.parents[1] / 'assets/round-record.example.json'


class ScriptParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.script_count = 0
        self.in_data = False
        self.data = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.script_count += 1
            self.in_data = dict(attrs).get('id') == 'round-data'
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_data = False
    def handle_data(self, data):
        if self.in_data:
            self.data += data


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(EXAMPLE.read_text())
    def test_example(self):
        self.assertEqual(len(renderer.validate_record(self.record)['reviewers']), 4)
    def test_unknown_evidence_link(self):
        self.record['reviewers'][0]['evidence_ids'] = ['not-a-source']
        with self.assertRaisesRegex(ValueError, 'unknown evidence'):
            renderer.validate_record(self.record)
    def test_duplicate_reviewer(self):
        self.record['reviewers'].append(copy.deepcopy(self.record['reviewers'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate identifiers'):
            renderer.validate_record(self.record)
    def test_candidate_needs_customer_job(self):
        self.record['candidates'][0]['need_ids'] = []
        with self.assertRaisesRegex(ValueError, 'customer need'):
            renderer.validate_record(self.record)
    def test_invalid_scope_and_types(self):
        self.record['needs'][0]['reviewer_ids'] = ['unknown-role']
        with self.assertRaisesRegex(ValueError, 'unknown reviewers'):
            renderer.validate_record(self.record)
        self.record = json.loads(EXAMPLE.read_text())
        self.record['reviewers'][0]['new'] = 'yes'
        with self.assertRaisesRegex(ValueError, 'expected boolean'):
            renderer.validate_record(self.record)
    def test_source_links(self):
        for url in ['javascript:alert(1)', 'https://person:secret@example.com/source']:
            self.record['evidence'][0]['url'] = url
            with self.assertRaisesRegex(ValueError, 'source URL'):
                renderer.validate_record(self.record)
    def test_untrusted_text_roundtrip(self):
        self.record['project']['name'] = '</script><script>alert("not executed")</script> & café'
        self.record['reviewers'][0]['objection'] = '<img src=x onerror=alert(1)>\u2028'
        parser = ScriptParser()
        html = renderer.render(self.record)
        parser.feed(html)
        self.assertEqual(parser.script_count, 2)
        self.assertEqual(json.loads(parser.data), self.record)
        self.assertNotIn('<script>alert("not executed")</script>', html)
    def test_cli_preserves_existing_output(self):
        with tempfile.TemporaryDirectory(prefix='panel-render-test-') as directory:
            output = Path(directory) / 'canvas.html'
            output.write_text('keep existing artifact')
            args = [sys.executable, str(SCRIPT), str(EXAMPLE), '--out', str(output)]
            result = subprocess.run(args, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(), 'keep existing artifact')
            result = subprocess.run(args + ['--overwrite'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('round-data', output.read_text())


if __name__ == '__main__':
    unittest.main()
