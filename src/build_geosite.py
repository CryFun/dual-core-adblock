#!/usr/bin/env python3
"""Build Xray/V2Ray GeoSite protobuf from existing Mihomo domain.yaml.

GeoSiteList.entry=1; GeoSite.country_code=1, domain=2;
Domain.type=1 (RootDomain=2, Full=3), value=2.
"""
import argparse
import hashlib
import json
from pathlib import Path
import yaml


def varint(n):
    if n < 0:
        raise ValueError('negative varint')
    result = bytearray()
    while n > 127:
        result.append((n & 127) | 128)
        n >>= 7
    result.append(n)
    return bytes(result)


def field_bytes(number, value):
    return varint(number << 3 | 2) + varint(len(value)) + value


def field_int(number, value):
    return varint(number << 3) + varint(value)


def domain_message(rule):
    if not isinstance(rule, str):
        raise ValueError('non-string domain rule')
    if rule.startswith('+.'):
        match_type, value = 2, rule[2:]
    elif rule.startswith('.'):
        match_type, value = 2, rule[1:]
    elif rule.startswith('*.'):
        # Mihomo wildcard semantics may differ; refuse rather than broaden.
        raise ValueError('wildcard rule cannot be converted safely')
    else:
        match_type, value = 3, rule
    if not value or '/' in value or ' ' in value or value.startswith('.'):
        raise ValueError(f'invalid domain rule: {rule!r}')
    return field_int(1, match_type) + field_bytes(2, value.encode('ascii'))


def build(input_yaml, output_dir):
    parsed = yaml.safe_load(Path(input_yaml).read_text(encoding='utf-8'))
    if not isinstance(parsed, dict) or not isinstance(parsed.get('payload'), list):
        raise ValueError('expected YAML payload list')
    rules = parsed['payload']
    if not rules:
        raise ValueError('empty domain payload')
    # GeoSite message holds one category; stream encoding avoids large intermediary list.
    country = field_bytes(1, b'ADBLOCK')
    entry = bytearray(country)
    for rule in rules:
        entry += field_bytes(2, domain_message(rule))
    blob = field_bytes(1, bytes(entry))
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for filename in ('adblock.dat', 'geosite.dat'):
        (out / filename).write_bytes(blob)
    report = {'category': 'ADBLOCK', 'domain_rules': len(rules), 'bytes': len(blob),
              'sha256': hashlib.sha256(blob).hexdigest(),
              'warning': 'geosite.dat is adblock-only; use adblock.dat with ext:adblock.dat:adblock to preserve built-in geosite categories'}
    (out / 'geosite-info.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='dist/domain.yaml')
    parser.add_argument('--output', default='dist')
    args = parser.parse_args()
    print(json.dumps(build(args.input, args.output), indent=2))
