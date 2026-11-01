# Universal sources upgrade for CryFun/mihomo-adblock

Keep your existing `ficlash.js`, workflow, `src/validate.py`, and existing sources. This upgrade replaces `src/build.py`, adds `src/adguard_parser.py`, `tests/test_adguard_parser.py`, and extends `config/sources.yaml`.

## Included curated sources
- REIJI007 (Clash classical, existing)
- anti-AD (Clash domain, existing)
- AWAvenue 秋风 (Clash domain, existing)
- HaGeZi Multi Normal (AdGuard DNS syntax; selected instead of Pro++ for lower breakage)
- AdGuard Chinese filter (network domain-only subset)
- AdGuard Mobile Ads filter (network domain-only subset)
- 乘风 / Chengfeng Adblock Plus rule (network domain-only subset)

**AdGuard parsing is deliberately partial**: `||domain^` and plain domain/hosts entries only. `@@` exceptions are counted but not implemented, and cosmetic, path, regex, scriptlet, modifier rules are counted as unsupported. Never claim equivalent AdGuard filtering. Some lists are redistributed by their authors under licenses: verify terms before publishing derived outputs.

## Future additions
Edit `config/sources.yaml` and add `name`, `url`, `behavior: adguard` for AdGuard TXT, `behavior: hosts` for hosts TXT, `behavior: domain` for Clash domain YAML, or `behavior: classical` for Clash classical YAML. Keep names unique. Use only trusted sources. A source failure stops publication rather than silently publishing incomplete data.

The GitHub Actions workflow already triggers on `src/**`, `tests/**`, and `config/**`. It will rebuild automatically after push. Check `rules/stats.json` and GitHub Actions logs for `unsupported` and `exceptions`. The current workflow summary table does not show those two new fields; they are included in `stats.json`.

**Warning:** Sources with `@@` exceptions may conflict with the merged blocking set. This parser reports them but does not enforce them. Adding filter lists increases risk of false positives. Review blocked connections in FIClash and use higher-priority `DIRECT` exceptions as needed.
