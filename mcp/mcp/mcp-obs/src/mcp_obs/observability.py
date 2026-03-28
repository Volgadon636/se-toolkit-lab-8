from __future__ import annotations

import json
from typing import Any, List, Optional
import httpx
from pydantic import BaseModel, Field

class LogEntry(BaseModel):
    timestamp: str = Field(alias="_msg", default="") # VictoriaLogs returns message in _msg usually or the whole line
    fields: dict[str, Any]

class VictoriaLogsResponse(BaseModel):
    # VictoriaLogs query returns stream of JSON objects, not a single JSON array
    pass

class TraceSummary(BaseModel):
    traceID: str
    spans: List[dict[str, Any]]

class JaegerTraceResponse(BaseModel):
    data: List[TraceSummary]

class ObservabilityClient:
    def __init__(
        self,
        victorialogs_url: str,
        victoriatraces_url: str,
        timeout: float = 10.0
    ):
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victoriatraces_url = victoriatraces_url.rstrip("/")
        self.timeout = timeout

    async def search_logs(self, query: str, limit: int = 50) -> List[dict[str, Any]]:
        # VictoriaLogs returns ndjson
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.victorialogs_url}/select/logsql/query",
                params={"query": query, "limit": limit}
            )
            response.raise_for_status()
            lines = response.text.strip().split("\n")
            return [json.loads(line) for line in lines if line.strip()]

    async def list_traces(self, service: str, limit: int = 10) -> List[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.victoriatraces_url}/select/jaeger/api/traces",
                params={"service": service, "limit": limit}
            )
            response.raise_for_status()
            return response.json().get("data", [])

    async def get_trace(self, trace_id: str) -> Optional[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json().get("data", [])
            return data[0] if data else None
