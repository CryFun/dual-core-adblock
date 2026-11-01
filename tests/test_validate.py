import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from validate import validate

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name)
        self.dist = self.dir / 'dist'
        self.dist.mkdir()
        (self.dist / 'domain.yaml').write_text('payload:\n' + ''.join(f'- ads{i}.example.com\n' for i in range(1000)))
        (self.dist / 'domain.mrs').write_bytes(b'0'*101)
        (self.dist / 'stats.json').write_text(json.dumps({'output': {'domain': 1000}, 'allowlist_conflicts': []}))
    def tearDown(self): self.temp.cleanup()
    def test_good(self): validate(self.dist)
    def test_missing_mrs(self):
        (self.dist / 'domain.mrs').unlink()
        with self.assertRaises(ValueError): validate(self.dist)
    def test_large_drop(self):
        old = self.dir / 'old.json'
        old.write_text(json.dumps({'output': {'domain': 2000}}))
        with self.assertRaises(ValueError): validate(self.dist, old)
    def test_inconsistent_count(self):
        (self.dist / 'stats.json').write_text(json.dumps({'output': {'domain': 1001}}))
        with self.assertRaises(ValueError): validate(self.dist)
if __name__ == '__main__': unittest.main()
