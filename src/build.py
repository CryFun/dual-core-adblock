#!/usr/bin/env python3
"""Conservative Mihomo adblock rule merger: never broaden domain matches."""
import argparse
import ipaddress
import json
import re
import urllib.request
from pathlib import Path
import yaml

DOMAIN = re.compile(r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", re.I)

def domain(s):
    s = s.strip().lower().rstrip('.')
    try:
        s = s.encode('idna').decode('ascii')
    except UnicodeError:
        return None
    return s if DOMAIN.fullmatch(s) else None

def parse_domain(s):
    s = str(s).strip()
    if s.startswith('+.') or s.startswith('*.'):
        d = domain(s[2:])
        return ('suffix', d) if d else None
    if s.startswith('.'):
        d = domain(s[1:])
        return ('suffix', d) if d else None
    d = domain(s)
    return ('exact', d) if d else None

def parse_classical(s):
    parts = [p.strip() for p in str(s).split(',')]
    if len(parts) < 2:
        return None
    kind, value = parts[:2]
    if kind in ('DOMAIN', 'DOMAIN-SUFFIX'):
        d = domain(value)
        return ('exact' if kind == 'DOMAIN' else 'suffix', d) if d else None
    if kind in ('IP-CIDR', 'IP-CIDR6'):
        try:
            net = ipaddress.ip_network(value, strict=False)
            if (kind == 'IP-CIDR') != (net.version == 4):
                return None
            return ('ip', str(net))
        except ValueError:
            return None
    return None

def allowed(kind, value, allow):
    return any(value == d or (k == 'suffix' and (value == d or value.endswith('.' + d))) for k, d in allow)

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'MihomoAdblockBuilder/1.0'})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read(30_000_001)
    if len(raw) > 30_000_000:
        raise ValueError('source exceeds 30 MB')
    data = yaml.safe_load(raw)
    if not isinstance(data, dict) or not isinstance(data.get('payload'), list):
        raise ValueError(f'Expected YAML payload list: {url}')
    return data['payload']

def build(sources, allow_lines, output):
    allow = set(filter(None, (parse_domain(x.strip()) for x in allow_lines if x.strip() and not x.lstrip().startswith('#'))))
    exact, suffix, ips, classical = set(), set(), set(), set()
    stats = {}
    for source in sources:
        name, behavior = source['name'], source['behavior']
        payload = fetch(source['url'])
        if not payload:
            raise ValueError(f'{name}: empty payload')
        count = {'input': len(payload), 'domain': 0, 'ip': 0, 'classical': 0}
        for item in payload:
            if not isinstance(item, str):
                raise ValueError(f'{name}: non-string rule')
            parsed = parse_domain(item) if behavior == 'domain' else parse_classical(item)
            if parsed:
                kind, value = parsed
                if kind == 'ip':
                    ips.add(value); count['ip'] += 1
                elif value and not allowed(kind, value, allow):
                    (exact if kind == 'exact' else suffix).add(value)
                    count['domain'] += 1
            elif behavior == 'classical':
                # Keep unknown/advanced rules verbatim; don't pretend they are domains.
                if ',' not in item:
                    raise ValueError(f'{name}: malformed classical entry: {item}')
                classical.add(item.strip()); count['classical'] += 1
            else:
                raise ValueError(f'{name}: unsupported domain entry: {item}')
        stats[name] = count
    # Avoid dropping exact rules merely because a suffix rule exists.
    # Exclude overlapping rules only when provably redundant and no allowlist ambiguity.
    domain_rules = sorted(exact) + ['+.' + d for d in sorted(suffix)]
    output.mkdir(parents=True, exist_ok=True)
    def dump(path, payload):
        path.write_text(yaml.safe_dump({'payload': payload}, allow_unicode=True, sort_keys=False, width=1000), encoding='utf-8')
    if not domain_rules:
        raise ValueError('no domain rules generated')
    dump(output / 'domain.yaml', domain_rules)
    if ips:
        dump(output / 'ipcidr.yaml', sorted(ips))
    if classical:
        dump(output / 'classical.yaml', sorted(classical))
    stats['output'] = {'domain': len(domain_rules), 'ipcidr': len(ips), 'classical': len(classical)}
    (output / 'stats.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return stats

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--sources', default='config/sources.yaml')
    p.add_argument('--allowlist', default='config/allowlist.txt')
    p.add_argument('--output', default='dist')
    a = p.parse_args()
    config = yaml.safe_load(Path(a.sources).read_text(encoding='utf-8'))
    print(json.dumps(build(config['sources'], Path(a.allowlist).read_text(encoding='utf-8').splitlines(), Path(a.output)), indent=2))
