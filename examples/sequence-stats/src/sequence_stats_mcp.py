"""Original, local-only MCP demonstration; no paper claims or external inputs."""
from mcp.server.fastmcp import FastMCP

MAX_BASES = 1_000_000

mcp = FastMCP("Sequence Stats")

@mcp.tool()
def sequence_stats(sequence: str) -> dict:
    """Return length and GC fraction for a nonempty A/C/G/T DNA sequence."""
    value = "".join(sequence.upper().split())
    if not value or len(value) > MAX_BASES or set(value) - set("ACGT"):
        raise ValueError(f"Expected 1-{MAX_BASES:,} A/C/G/T bases")
    return {"length": len(value), "gc_fraction": (value.count("G") + value.count("C")) / len(value)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
