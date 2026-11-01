"""Conservative DNS-only subset of AdGuard/ABP and hosts formats.
Unsupported network, cosmetic, script and exception rules are counted, never broadened.
"""
import re
import ipaddress

HOST_IPS = {'0.0.0.0', '127.0.0.1', '::', '::1'}


def parse_text_rule(line, fmt, domain_func):
    """Return (kind, domain) or (status, None). kind=exact/suffix; status=skip/exception/unsupported."""
    s = line.strip().lstrip('\ufeff')
    if not s or s.startswith(('!', '#', '[', '//')):
        return ('skip', None)
    if fmt == 'hosts':
        fields = s.split('#', 1)[0].split()
        if len(fields) < 2:
            return ('unsupported', None)
        try:
            ipaddress.ip_address(fields[0])
        except ValueError:
            return ('unsupported', None)
        if fields[0] not in HOST_IPS:
            return ('unsupported', None)
        if len(fields) != 2:
            return ('unsupported', None)  # avoid multi-host ambiguity
        d = domain_func(fields[1])
        return ('exact', d) if d and d not in ('localhost',) else ('unsupported', None)
    if fmt != 'adguard':
        raise ValueError('Unknown text format')
    if s.startswith('@@'):
        return ('exception', None)
    # Only the unmodified ||domain^ form has safe domain-suffix semantics.
    m = re.fullmatch(r'\|\|([^\^|/$*?#\s]+)\^', s)
    if m:
        d = domain_func(m.group(1))
        return ('suffix', d) if d else ('unsupported', None)
    # Plain DNS-style domain entries, as emitted by some DNS lists.
    d = domain_func(s)
    if d:
        return ('exact', d)
    # Standard hosts lines can also occur in DNS filter lists.
    if re.match(r'^(?:0\.0\.0\.0|127\.0\.0\.1|::1?)\s+', s):
        return parse_text_rule(s, 'hosts', domain_func)
    return ('unsupported', None)
