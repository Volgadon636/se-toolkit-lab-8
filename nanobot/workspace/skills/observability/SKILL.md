# Observability (logs & traces)

You can inspect **VictoriaLogs** and **VictoriaTraces** via MCP tools.

## Tools

- **logs_search** — run a LogsQL query (e.g. `_stream:{service="backend"} AND level:error`).
- **logs_error_count** — shortcut for recent **error** lines for a given `service` (default `backend`).
- **traces_list** — list recent traces for a service name (often `backend`).
- **traces_get** — load one trace by ID when you see a trace id in logs or listings.

## Strategy

1. When the user asks about **errors**, **what went wrong**, **health**, or **issues in the last hour**, call **logs_error_count** or **logs_search** first.
2. If logs mention a **trace id** (or you need latency/causality), call **traces_list** and then **traces_get** for the relevant id.
3. Summarize in plain language: service, time window, error message, and what the trace shows. **Do not paste huge JSON blobs** unless the user asks for raw data.
4. For **"What went wrong?"** or **"Check system health"**: search error logs → pull a trace if it clarifies the failure → give a short numbered summary (symptom → evidence → likely cause).

## LMS tools

Use **lms_*** tools for course data; use **logs_*** / **traces_*** for incidents and debugging.
