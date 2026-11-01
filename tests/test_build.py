import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from build import parse_domain, parse_classical, allowed

class TestRules(unittest.TestCase):
    def test_suffix(self):
        self.assertEqual(parse_domain('+.Ads.Example.com'), ('suffix', 'ads.example.com'))
    def test_exact(self):
        self.assertEqual(parse_classical('DOMAIN,ads.example.com'), ('exact', 'ads.example.com'))
    def test_ip(self):
        self.assertEqual(parse_classical('IP-CIDR,1.2.3.4/32'), ('ip', '1.2.3.4/32'))
    def test_allowlist(self):
        self.assertTrue(allowed('exact', 'ads.example.com', {('suffix', 'example.com')}))
        self.assertFalse(allowed('exact', 'ads.example.net', {('suffix', 'example.com')}))

if __name__ == '__main__':
    unittest.main()
