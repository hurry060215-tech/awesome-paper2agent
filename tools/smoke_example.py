"""Runtime smoke test for the bundled example package; independent of CI."""
import asyncio
import json
import os
from pathlib import Path
import sys
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ModuleNotFoundError:
    raise SystemExit(
        'This smoke test needs its own environment:\n'
        '  python3.11 -m venv .runtime-venv\n'
        '  .runtime-venv/bin/pip install -r examples/sequence-stats/src/requirements.txt\n'
        '  .runtime-venv/bin/python tools/smoke_example.py'
    )

async def main():
    path = Path(__file__).resolve().parents[1] / 'examples/sequence-stats/src/sequence_stats_mcp.py'
    params = StdioServerParameters(command=sys.executable, args=['-B', str(path)], env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert [t.name for t in tools.tools] == ['sequence_stats']
            result = await session.call_tool('sequence_stats', {'sequence': 'ACGTGG'})
            assert not result.isError
            value = json.loads(result.content[0].text)
            assert value['length'] == 6 and abs(value['gc_fraction'] - 2/3) < 1e-10
            bad = await session.call_tool('sequence_stats', {'sequence': 'XYZ'})
            assert bad.isError
            print('PASS: MCP initialize, list_tools, valid call, invalid-input rejection')

if __name__ == '__main__':
    asyncio.run(main())
