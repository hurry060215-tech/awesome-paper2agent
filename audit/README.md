# Local audit harness

These scripts are local acceptance checks for the three catalog packages. They
are intentionally outside `packages/` and are not copied into release ZIPs.
They create all inputs under a caller-supplied temporary directory, start each
entry point over MCP stdio, enumerate tools, call every declared tool on a small
input, and include relevant rejection calls. The harness returns non-zero when
an expected success/error state differs.

The fixed checkout used for this run is `3315ce749cff8cc935ff966586296f21ca0a5819`.
The package environments were Python 3.12.13 virtual environments rebuilt from
each package's pinned `src/requirements.txt`.

Example Windows commands from the repository root:

```powershell
$audit = "$env:TEMP\paper2agent-audit-3315ce7"
$scan = "$env:TEMP\paper2agent-envs\scanpy-0.1.1\Scripts\python.exe"
& $scan audit/run_mcp_checks.py --package scanpy `
  --entry packages/scanpy-workflow/src/scanpy_workflow_mcp.py `
  --work "$audit\scanpy" --report "$audit\scanpy.json"

$scrub = "$env:TEMP\paper2agent-envs\scrublet-0.1.1\Scripts\python.exe"
& $scrub audit/run_mcp_checks.py --package scrublet `
  --entry packages/scrublet-doublets/src/scrublet_doublets_mcp.py `
  --work "$audit\scrublet" --report "$audit\scrublet.json"

& $scan audit/check_scanpy_semantics.py `
  --entry packages/scanpy-workflow/src/scanpy_workflow_mcp.py `
  --work "$audit\scanpy-semantics"
```

The harness records per-call wall time and the JSON reports retain the tool
enumeration, structured/text results and expected-error states. Native peak
RSS is not reported by these scripts because neither declared runtime pins
`psutil`; resource limits were therefore applied by dataset size and wall-time
observation, with any unrun larger size called out in the final report.
