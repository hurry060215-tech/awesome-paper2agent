# Sequence Stats

Original synthetic example used to exercise the catalog pipeline. The tool performs no
external data access or network calls.

Install the pinned requirements and run `python src/sequence_stats_mcp.py` for MCP stdio.

Tool: `sequence_stats(sequence)` accepts A/C/G/T characters (case-insensitive, whitespace ignored).
Example input `ACGTGG` returns length 6 and GC fraction 0.6666666666666666.
Invalid or empty sequences are rejected. Maximum length: 1,000,000 bases.

Dependencies require network access during installation. Runtime smoke testing is distinct from catalog validation.
