import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from build import parse_domain, parse_classical, allowed, allowlist_conflicts, build

class TestRules(unittest.TestCase):
    def test_suffix(self):
        self.assertEqual(parse_domain('+.Ads.Example.com'), ('suffix', 'ads.example.com'))
    def test_exact(self):
        self.assertEqual(parse_classical('DOMAIN,ads.example.com'), ('exact', 'ads.example.com'))
    def test_ip(self):
        self.assertEqual(parse_classical('IP-CIDR,1.2.3.4/32'), ('ip', '1.2.3.4/32'))
    def test_invalid_domain(self):
        self.assertIsNone(parse_domain('http://ads.example.com/path'))

    def test_invalid_ip(self):
        self.assertIsNone(parse_classical('IP-CIDR,not-an-ip'))

    def test_conflict_detection(self):
        conflicts = allowlist_conflicts(set(), {'example.com'}, {('exact', 'api.example.com')})
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]['covering_suffixes'], ['example.com'])

    def test_no_conflict(self):
        self.assertEqual(allowlist_conflicts(set(), {'ads.example.com'}, {('exact', 'api.example.com')}), [])

    def test_allowlist(self):
        self.assertTrue(allowed('exact', 'ads.example.com', {('suffix', 'example.com')}))
        self.assertFalse(allowed('exact', 'ads.example.net', {('suffix', 'example.com')}))

if __name__ == '__main__':
    unittest.main()
