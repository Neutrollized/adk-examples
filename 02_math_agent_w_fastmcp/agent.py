import os
import asyncio
from contextlib import AsyncExitStack

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams


#-----------------
# settings
#-----------------
model="gemini-2.0-flash"
fastmcp_server_url=os.environ.get("FASTMCP_SERVER_URL")


#-----------------
# tools
#-----------------
async def get_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers.

    Args:
        a: number
        b: number

    Returns:
        the sum of two numbers.
    """
    tools, _ = await MCPToolset.from_server(
        connection_params=SseServerParams(
            url=fastmcp_server_url + "/sse",
        ),
        async_exit_stack=AsyncExitStack()
    )

    return await tools[0].run_async(
        args={
            "a": a,
            "b": b,
        },
        tool_context=None,
    )

async def get_difference(a: int, b: int) -> int:
    """Calculate the difference of two numbers.

    Args:
        a: number
        b: number

    Returns:
        the difference of two numbers.
    """
    tools, _ = await MCPToolset.from_server(
        connection_params=SseServerParams(
            url=fastmcp_server_url + "/sse",
        ),
        async_exit_stack=AsyncExitStack()
    )

    return await tools[1].run_async(
        args={
            "a": a,
            "b": b,
        },
        tool_context=None,
    )

async def get_product(a: int, b: int) -> int:
    """Calculate the product of two numbers.

    Args:
        a: number
        b: number

    Returns:
        the product of two numbers.
    """
    tools, _ = await MCPToolset.from_server(
        connection_params=SseServerParams(
            url=fastmcp_server_url + "/sse",
        ),
        async_exit_stack=AsyncExitStack()
    )

    return await tools[2].run_async(
        args={
            "a": a,
            "b": b,
        },
        tool_context=None,
    )

async def get_division(a: int, b: int) -> float:
    """Calculate the division of two numbers.

    Args:
        a: number
        b: number

    Returns:
        the division of two numbers.
    """
    tools, _ = await MCPToolset.from_server(
        connection_params=SseServerParams(
            url=fastmcp_server_url + "/sse",
        ),
        async_exit_stack=AsyncExitStack()
    )

    return await tools[3].run_async(
        args={
            "a": a,
            "b": b,
        },
        tool_context=None,
    )

async def get_quotient(a: int, b: int) -> int:
    """Calculate the quotient of two numbers.

    Args:
        a: number
        b: number

    Returns:
        the quotient of two numbers.
    """
    tools, _ = await MCPToolset.from_server(
        connection_params=SseServerParams(
            url=fastmcp_server_url + "/sse",
        ),
        async_exit_stack=AsyncExitStack()
    )

    return await tools[4].run_async(
        args={
            "a": a,
            "b": b,
        },
        tool_context=None,
    )


#-----------------
# agents
#-----------------
root_agent = Agent(
    name="math_agent",
    model=model,
    instruction=(
        "You are a helpful AI assistant designed to provide accurate and useful information. Use only the tools you are given to do math."
    ),
    tools=[
        get_sum,
        get_difference,
        get_product,
        get_division,
        get_quotient
    ],
)
