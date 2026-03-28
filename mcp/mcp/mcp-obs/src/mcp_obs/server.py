from __future__ import annotations

import asyncio
import json
import os
from typing import Any, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from mcp_obs.observability import ObservabilityClient

class LogsSearchArgs(BaseModel):
    query: str = Field(description="LogsQL query string (e.g., '_time:10m severity:ERROR')")
    limit: int = Field(default=20, description="Max logs to return")

class LogsErrorCountArgs(BaseModel):
    service: str = Field(description="Service name to count errors for")
    window: str = Field(default="1h", description="Time window (e.g., '1h', '10m')")

class TracesListArgs(BaseModel):
    service: str = Field(description="Service name to list traces for")
    limit: int = Field(default=10, description="Max traces to return")

class TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")

def _text(data: Any) -> list[TextContent]:
    return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]

def create_server(client: ObservabilityClient) -> Server:
    server = Server("observability")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="mcp_obs_logs_search",
                description="Search logs in VictoriaLogs using LogsQL.",
                inputSchema=LogsSearchArgs.model_json_schema()
            ),
            Tool(
                name="mcp_obs_logs_error_count",
                description="Count error logs for a specific service over a time window.",
                inputSchema=LogsErrorCountArgs.model_json_schema()
            ),
            Tool(
                name="mcp_obs_traces_list",
                description="List recent traces for a specific service.",
                inputSchema=TracesListArgs.model_json_schema()
            ),
            Tool(
                name="mcp_obs_traces_get",
                description="Fetch a specific trace by ID.",
                inputSchema=TracesGetArgs.model_json_schema()
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        try:
            if name == "mcp_obs_logs_search":
                args = LogsSearchArgs.model_validate(arguments or {})
                result = await client.search_logs(args.query, args.limit)
                return _text(result)
            
            elif name == "mcp_obs_logs_error_count":
                args = LogsErrorCountArgs.model_validate(arguments or {})
                # LogsQL to count errors: _time:WINDOW service.name:SERVICE severity:ERROR | stats count() as total
                query = f"_time:{args.window} \"service.name\":\"{args.service}\" severity:ERROR"
                logs = await client.search_logs(query, limit=1000)
                return _text({"service": args.service, "window": args.window, "error_count": len(logs)})

            elif name == "mcp_obs_traces_list":
                args = TracesListArgs.model_validate(arguments or {})
                result = await client.list_traces(args.service, args.limit)
                return _text(result)

            elif name == "mcp_obs_traces_get":
                args = TracesGetArgs.model_validate(arguments or {})
                result = await client.get_trace(args.trace_id)
                if result is None:
                    return [TextContent(type="text", text=f"Trace {args.trace_id} not found.")]
                return _text(result)

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    return server

async def main():
    victorialogs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")
    victoriatraces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")
    
    client = ObservabilityClient(victorialogs_url, victoriatraces_url)
    server = create_server(client)
    
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    asyncio.run(main())
