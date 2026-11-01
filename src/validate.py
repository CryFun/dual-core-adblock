#!/usr/bin/env python3
"""Fail closed before publishing malformed or unexpectedly shrunken output."""
import argparse
import json
from pathlib import Path
import yaml


def validate(dist, previous=None, min_ratio=0.70, min_count=1000):
    stats = json.loads((dist / 'stats.json').read_text(encoding='utf-8'))
    rules = yaml.safe_load((dist / 'domain.yaml').read_text(encoding='utf-8'))
    if not isinstance(rules, dict) or not isinstance(rules.get('payload'), list):
        raise ValueError('Invalid domain YAML payload')
    count = len(rules['payload'])
    if count < min_count or count != stats['output']['domain']:
        raise ValueError(f'Unexpected domain count: {count}')
    if len(set(rules['payload'])) != count:
        raise ValueError('Duplicate rules in final output')
    if stats.get('allowlist_conflicts'):
        raise ValueError('Allowlist conflicts present')
    if previous is not None and previous.exists():
        old = json.loads(previous.read_text(encoding='utf-8'))
        old_count = old.get('output', {}).get('domain', 0)
        if old_count > 0 and count < old_count * min_ratio:
            raise ValueError(f'Rule count dropped from {old_count} to {count} (minimum ratio {min_ratio})')
    if not (dist / 'domain.mrs').is_file() or (dist / 'domain.mrs').stat().st_size < 100:
        raise ValueError('Missing or implausibly small domain.mrs')
    print(f'Validated {count} domain rules')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--dist', type=Path, default=Path('dist'))
    p.add_argument('--previous', type=Path)
    p.add_argument('--min-ratio', type=float, default=0.70)
    a = p.parse_args()
    validate(a.dist, a.previous, a.min_ratio)
