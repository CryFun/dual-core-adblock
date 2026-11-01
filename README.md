# Mihomo / FIClash AdBlock Builder

Automatically merge three Clash ad-blocking lists, deduplicate, apply allowlist, and compile domain MRS using Mihomo. Unsupported classical rules remain in `classical.yaml` instead of being silently converted.

## Deployment

1. Create a **public** GitHub repository and upload all files (including `.github/workflows/build.yml`).
2. In repository Settings → Actions → General, allow Actions to run and grant **Read and write permissions** to `GITHUB_TOKEN` (where available).
3. Run Actions → Build adblock rules → Run workflow.
4. Check that branch `rules` contains `domain.mrs`, `domain.yaml`, `stats.json` and, if generated, `classical.yaml` / `ipcidr.mrs`.
5. Edit `ficlash.js` and replace `YOUR_GITHUB_USERNAME/YOUR_REPOSITORY`. In FIClash, open subscription → Extension → Script and paste it.
6. To retain all supported rules, uncomment the `custom-ad-classical` and `custom-ad-ip` provider declarations **and add** `RULE-SET,custom-ad-classical,REJECT` and `RULE-SET,custom-ad-ip,REJECT,no-resolve` to `config.rules` only when those files are present.

## Behavior and caveats

- Builds daily at 02:17 UTC and on relevant pushes; FIClash checks daily.
- Sources: REIJI007, Anti-AD, AWAvenue. Source formats are assumed based on their documented Clash variants; build fails rather than silently accepting unknown domain syntax.
- Domain suffix and exact match semantics are preserved; no unsafe suffix widening.
- `allowlist.txt`: `example.com` excludes exact domain; `+.example.com` excludes the suffix and its children from **generated domain entries**, but overlapping broader source suffixes may still block it. Use an explicit FIClash `DOMAIN,example.com,DIRECT` rule ahead of the adblock RULE-SET for reliable exceptions.
- Allowlist does not override classical/IP rules. Validate actual matching behavior before treating it as a guaranteed exception.
- The workflow force-updates only its generated `rules` branch. Do not edit that branch manually.
- Downloaded Mihomo binary is taken from the latest official GitHub release, without checksum pinning; for a higher-assurance supply chain, pin release and SHA256.
- Some upstream licenses require attribution or restrict redistribution. Review the upstream licenses before making generated outputs public.
- MRS supports domain/ipcidr, not classical; complex classical rules remain YAML.
- Test with a small set of apps first; DNS bypass, encrypted DNS, first-party ads, and in-app content filtering cannot be solved by route rules alone.
