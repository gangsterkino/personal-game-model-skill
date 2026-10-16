"""Offline regression checks for adopted source fixes. Never calls remote services."""
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / 'skills/build-reference-scene'


def module(name, rel):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(value)
    finally:
        sys.path.pop(0)
    return value


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def download_module(self):
        with patch.dict(sys.modules, {'bpy': types.ModuleType('bpy')}):
            return module('reviewed_fetch', 'modules/bpy/assets/asset_fetch_lib.py')

    def test_network_requires_explicit_task_configuration(self):
        value = self.download_module()
        with self.assertRaises(ValueError):
            value._checked_url('https://api.polyhaven.com/assets')
        value.configure_downloads(self.root / 'cache', ['api.polyhaven.com', 'dl.polyhaven.org'])
        self.assertEqual(value._checked_url('https://api.polyhaven.com/assets'), 'https://api.polyhaven.com/assets')
        for bad in ['file:///etc/passwd', 'https://evil.example/a', 'http://api.polyhaven.com/a', 'https://api.polyhaven.com:123/a']:
            with self.assertRaises(ValueError): value._checked_url(bad)

    def test_manifest_paths_cannot_escape_cache(self):
        value = self.download_module()
        value.configure_downloads(self.root / 'cache', ['api.polyhaven.com'])
        for bad in ['../outside', '/tmp/outside', 'C:\\outside', 'a/../../out']:
            with self.assertRaises(ValueError): value._dependency_path(self.root / 'cache', bad)
        outside = self.root / 'outside'; outside.mkdir()
        (self.root / 'cache' / 'link').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError): value._dependency_path(self.root / 'cache', 'link/out')

    def test_download_preserves_existing_and_cleans_oversize(self):
        value = self.download_module()
        value.configure_downloads(self.root / 'cache', ['api.polyhaven.com'], max_bytes=3)
        file = self.root / 'cache' / 'image.png'
        file.write_bytes(b'KEEP')
        with self.assertRaises(FileExistsError): value._http_download('https://api.polyhaven.com/a', file)
        self.assertEqual(file.read_bytes(), b'KEEP')
        file.unlink()
        with patch.object(value, '_open', return_value=io.BytesIO(b'oversize')):
            with self.assertRaises(ValueError): value._http_download('https://api.polyhaven.com/a', file)
        self.assertFalse(file.exists())

    def test_job_fixed_tmp_symlink_cannot_clobber(self):
        job = module('reviewed_job', 'modules/curio/skills/mesh-split-fill/scripts/job.py')
        sentinel = self.root / 'sentinel'; sentinel.write_text('KEEP')
        (self.root / 'job.json.tmp').symlink_to(sentinel)
        job.write_json(self.root / 'job.json', {'safe': True})
        self.assertEqual(sentinel.read_text(), 'KEEP')
        self.assertEqual(json.loads((self.root / 'job.json').read_text()), {'safe': True})

    def test_storyboard_rejects_outside_evidence(self):
        story = module('reviewed_story', 'modules/curio/skills/mesh-split-fill/scripts/storyboard.py')
        job = self.root / 'job'; job.mkdir()
        outside = self.root / 'outside.png'; outside.write_bytes(b'fake')
        (job / 'alias.png').symlink_to(outside)
        for bad in ['../outside.png', str(outside), 'alias.png']:
            with self.assertRaises(ValueError): story.asset(job, bad)

    def test_surface_bounds_and_fresh_output(self):
        paint = module('reviewed_paint', 'modules/curio/skills/curio-oil-paintings/scripts/paint_surface.py')
        valid = {'resolution': [32, 40], 'canvas_m': [.4,.5], 'brush_strokes': 2}
        for update in [{'resolution':[100000,100000]}, {'weave_spacing_m':0}, {'canvas_m':[float('nan'),.5]}, {'brush_strokes':100000}]:
            with self.assertRaises(ValueError): paint.build({**valid, **update}, self.root/'invalid')
            self.assertFalse((self.root/'invalid').exists())
        result = paint.build(valid, self.root/'valid')
        self.assertEqual(result['mode'], 'generic-relief-preview-not-form-aware')
        self.assertTrue((self.root/'valid'/'surface-report.json').exists())
        with self.assertRaises(FileExistsError): paint.build(valid, self.root/'valid')

    def test_character_report_hardlink_preserves_input(self):
        checker = module('reviewed_character', 'modules/curio/skills/noir-character-pipeline/scripts/check_character_maps.py')
        source = self.root/'source.png'; source.write_bytes(b'KEEP')
        report = self.root/'report.json'; os.link(source, report)
        with patch.object(checker, 'check_maps', return_value={'technical_checks_passed':True}), patch.object(sys,'argv',['checker','--albedo',str(source),'--normal',str(source),'--report',str(report)]):
            with self.assertRaises(FileExistsError): checker.main()
        self.assertEqual(source.read_bytes(), b'KEEP')


if __name__ == '__main__':
    unittest.main()
