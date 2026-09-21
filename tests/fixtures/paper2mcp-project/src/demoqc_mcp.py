"""A stand-in for a Paper2MCP server entry point (test fixture, never executed)."""
from fastmcp import FastMCP

mcp = FastMCP("Demo QC")


@mcp.tool()
def qc_summary(expr_path: str) -> dict:
    """Summarise a small expression table."""
    return {"rows": 12}


if __name__ == "__main__":
    mcp.run(transport="stdio")
