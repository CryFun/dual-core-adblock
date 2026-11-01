# Mihomo AdBlock — stable release

For **CryFun/mihomo-adblock**. Uses REIJI007, Anti-AD and AWAvenue Clash-format sources, conservatively merges rules, and publishes `domain.mrs` to `rules` branch daily at 02:17 UTC. FIClash loads only `domain.mrs` (no missing-file dependencies).

## One-time upgrade from Termux

Download `mihomo-adblock-final-stable.zip` into the Android Download folder, then run:

```sh
cd ~/github-upload
unzip -o ~/storage/downloads/mihomo-adblock-final-stable.zip -d .
python -m unittest discover -s tests -v  # optional if Python/PyYAML installed
 git add .github/workflows/build.yml src tests config requirements.txt ficlash.js README.md
 git commit -m "Install stable adblock builder"
 git -c credential.helper= push origin main
```

Use your GitHub PAT when prompted. Do not share the PAT. The workflow requires GitHub Actions Contents write permissions. After push, verify Actions green and `rules/domain.mrs` exists. Import `ficlash.js` into the subscription extension Script mode if not already configured; existing working FIClash script may remain unchanged.

## Safety and limitations

- A failed source download, invalid input, missing/small MRS, invalid output count, or more than 30% drop vs prior stats stops publication. Existing `rules` branch remains intact. First builds require at least 1000 domain entries.
- Exact/suffix semantics are preserved; overlapping suffix rules are not aggressively pruned. Source-order deduplication statistics are in `rules/stats.json`.
- Allowlist is **not** a general bypass. If a broader blocked suffix covers an allowlisted domain, the build fails rather than claiming an ineffective exception. For exceptions, add a higher-priority `DOMAIN,example.com,DIRECT` in FIClash ahead of the adblock RULE-SET. Classical and IP rules are generated only if present; FIClash script does not load these optional files by default.
- Domain routing cannot implement AdGuard cosmetic, URL-path, JavaScript or HTTPS content filters; first-party ads and apps bypassing proxy/DNS can remain.
- Upstream source availability, GitHub runner changes, and Mihomo releases can still cause failures. Official Mihomo binary is downloaded from latest release without a pinned digest; for stronger supply-chain assurance pin a verified binary and SHA256.
- `rules` is generated and force-updated automatically. Never manually edit that branch. For rollback, restore a known good commit on `main` and rerun the workflow, or use a previously saved MRS artifact.
- Check upstream redistribution licenses before distributing merged outputs publicly.
