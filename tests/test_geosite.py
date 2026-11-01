import sys
import tempfile
import unittest
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from build_geosite import build, domain_message, field_bytes, field_int, varint

class TestGeoSite(unittest.TestCase):
    def test_varint(self):
        self.assertEqual(varint(300), b'\xac\x02')
    def test_full(self):
        self.assertEqual(domain_message('ads.example.com'), field_int(1, 3) + field_bytes(2, b'ads.example.com'))
    def test_suffix(self):
        self.assertEqual(domain_message('+.example.com'), field_int(1, 2) + field_bytes(2, b'example.com'))
    def test_reject_wildcard(self):
        with self.assertRaises(ValueError): domain_message('*.example.com')
    def test_build(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            (p/'domain.yaml').write_text(yaml.safe_dump({'payload':['ads.example.com','+.track.example.com']}))
            report=build(p/'domain.yaml',p/'dist')
            self.assertEqual(report['domain_rules'],2)
            self.assertEqual((p/'dist/adblock.dat').read_bytes(),(p/'dist/geosite.dat').read_bytes())
            self.assertIn(b'ADBLOCK',(p/'dist/adblock.dat').read_bytes())

if __name__=='__main__': unittest.main()
