# Upgrade v2

- Per-source duplicate and allowlist counters in `stats.json`.
- Detect potentially ineffective allowlist exceptions covered by broader blocking suffixes. This is a warning, **not** a bypass guarantee.
- Additional unit tests.
- GitHub Actions job summary table.

The FIClash extension and published `rules` branch are unchanged until the new build succeeds.

Important: The counters track encountered duplicates and may count repeated occurrences within a source. The allowlist still does not override IP or classical rules.
