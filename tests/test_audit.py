import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('audit', Path(__file__).resolve().parents[1] / 'scripts/audit_manifest.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.table = '| 序号 | 1 |\n|---|---|\n| 频率 | 1KHz |'
        self.manifest = {'requirements': [{'id': 'r1', 'source': '第3页',
                         'quote': '计算时间常数', 'status': 'covered', 'evidence': '计算时间常数'}],
                         'source_tables': [self.table], 'forbidden_text': ['额外实测内阻']}
        self.report = '计算时间常数\n\n' + self.table

    def test_preserves_source(self):
        self.assertEqual(module.audit(self.manifest, self.report, self.root), [])

    def test_rejects_unit_normalization(self):
        self.assertTrue(module.audit(self.manifest, self.report.replace('1KHz', '1 kHz'), self.root))

    def test_detects_uncovered_requirement(self):
        self.manifest['requirements'][0]['evidence'] = '不存在的结果'
        self.assertTrue(module.audit(self.manifest, self.report, self.root))

    def test_detects_extra_measurement(self):
        self.assertTrue(module.audit(self.manifest, self.report + '\n额外实测内阻', self.root))

    def test_detects_missing_image(self):
        self.assertTrue(module.audit(self.manifest, self.report + '\n![图](missing.png)', self.root))

    def test_requires_reason_for_exclusion(self):
        self.manifest['requirements'][0]['status'] = 'excluded'
        self.assertTrue(module.audit(self.manifest, self.report, self.root))


if __name__ == '__main__':
    unittest.main()
