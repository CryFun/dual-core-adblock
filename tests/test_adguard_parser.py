import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from adguard_parser import parse_text_rule
from build import domain

class TestAdguardParser(unittest.TestCase):
    def parse(self, s, fmt='adguard'):
        return parse_text_rule(s, fmt, domain)
    def test_suffix(self): self.assertEqual(self.parse('||Ads.Example.COM^'), ('suffix', 'ads.example.com'))
    def test_plain(self): self.assertEqual(self.parse('ads.example.com'), ('exact', 'ads.example.com'))
    def test_exception(self): self.assertEqual(self.parse('@@||ads.example.com^'), ('exception', None))
    def test_path(self): self.assertEqual(self.parse('||example.com/ads/*'), ('unsupported', None))
    def test_modifier(self): self.assertEqual(self.parse('||ads.example.com^$third-party'), ('unsupported', None))
    def test_cosmetic(self): self.assertEqual(self.parse('example.com##.ad'), ('unsupported', None))
    def test_hosts(self): self.assertEqual(self.parse('0.0.0.0 ads.example.com', 'hosts'), ('exact', 'ads.example.com'))
    def test_hosts_nonblocking(self): self.assertEqual(self.parse('1.2.3.4 ads.example.com', 'hosts'), ('unsupported', None))
    def test_skip(self): self.assertEqual(self.parse('! comment'), ('skip', None))
