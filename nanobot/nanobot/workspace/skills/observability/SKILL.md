---
name: observability
description: Use observability tools (logs and traces) to investigate system issues
always: true
---

# Observability Skill

You can see the system's "eyes" — logs and traces. Use these tools when a user reports an error, asks about system health, or when a tool call fails.

## Strategy

When investigating failures (e.g., when the user asks "What went wrong?" or "Check system health"):

1. **Recent error logs first**: Use `mcp_obs_logs_search` with a short window (e.g. `_time:10m` and error severity) to find the newest relevant ERROR lines and any embedded `trace_id`.
2. **Error counts (optional context)**: Use `mcp_obs_logs_error_count` on the same window for services such as "Learning Management Service" if it helps quantify impact.
3. **Trace correlation**: If a log line contains a `trace_id`, fetch that trace with `mcp_obs_traces_get` and use it to explain where the request failed.
4. **Summarization**: Provide a single coherent explanation that:
   - Cites **log evidence** (e.g., "Logs show a `db_query` failure in the backend...")
   - Cites **trace evidence** (e.g., "...and the matching trace `e242...` confirms the span for PostgreSQL timed out.")
   - Identifies the **affected service** and **root cause**.
   - **Do not dump raw JSON.** Be concise and technical.

## Specific Tasks

### What went wrong? / Check system health
Follow the multi-step investigation flow above (logs first, then trace if present):
- `mcp_obs_logs_search` (recent errors)
- `mcp_obs_logs_error_count` if useful
- `mcp_obs_traces_get` when a `trace_id` is available
- Summarize with citations to **both** log and trace evidence where applicable.

### Any errors in the last X minutes?
- Use `mcp_obs_logs_search` with `_time:Xm severity:ERROR`.
- If errors are found, optionally fetch a trace for the most recent one to add more context.

### Proactive Health Checks (Cron)
If the user asks to schedule a health check:
- Follow the **`cron`** skill: use the **`cron`** tool (not `HEARTBEAT.md`) to add a recurring job with `deliver` appropriate for posting into this chat.
- Each run should perform the investigation flow above and post a summary.
- If no errors are found, report that the system looks healthy.
