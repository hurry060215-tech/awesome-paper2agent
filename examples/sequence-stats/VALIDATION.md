# Validation

Synthetic example package: it exercises the catalog pipeline and makes no scientific claim.

## How this was verified

- Environment: Python 3.11; `src/requirements.txt` pins one distribution (`mcp`).
- `sequence_stats` — started over MCP stdio with `tools/smoke_example.py`: `initialize` and
  `list_tools` succeed, `ACGTGG` returns length 6 and a GC fraction of 0.666…, and an invalid
  sequence is rejected.

## What remains unverified

- Nothing about a paper: this package does not reproduce any published result.
- Behaviour on inputs larger than the documented 1,000,000-base limit.
