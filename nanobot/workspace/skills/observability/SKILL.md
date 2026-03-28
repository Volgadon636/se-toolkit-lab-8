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

## Multi-Step Investigation Pattern

When diagnosing failures (e.g., PostgreSQL stopped, backend errors):

1. **Start with logs**: Call `logs_error_count(service="backend", minutes=5)` to find recent errors
2. **Extract trace ID**: Look for `trace_id` in the error log lines
3. **Fetch the trace**: Call `traces_get(trace_id="<id>")` to see the full request flow
4. **Identify root cause**: Look for the first span with an error, note the exception message
5. **Summarize**: Provide a 2-3 sentence summary connecting logs + traces

**Example response structure:**
```
1. Symptom: Backend returned 500 error on /items/ endpoint
2. Log evidence: "Connection refused" to PostgreSQL on port 5432
3. Trace evidence: Span "get_items" failed with sqlalchemy.exc.OperationalError
4. Root cause: PostgreSQL container is stopped or unreachable
```

## LMS tools

Use **lms_*** tools for course data; use **logs_*** / **traces_*** for incidents and debugging.
