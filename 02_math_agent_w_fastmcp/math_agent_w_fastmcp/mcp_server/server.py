from fastmcp import FastMCP
import asyncio

mcp = FastMCP("FastMCP Math Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    return a / b

@mcp.tool()
def quotient(a: int, b: int) -> int:
    """Divide two numbers, ignoring remainder"""
    return a // b


# https://gofastmcp.com/deployment/running-server
if __name__ == "__main__":
    #asyncio.run(mcp.run(transport="sse", host="0.0.0.0", port=8080))
    asyncio.run(mcp.run(transport="streamable-http", host="0.0.0.0", port=8080))
