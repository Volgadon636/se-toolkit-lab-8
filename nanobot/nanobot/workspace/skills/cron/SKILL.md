---
name: cron
description: Create, list, and remove chat-bound scheduled jobs with the built-in cron tool (health checks, recurring reports)
always: true
---

# Cron — scheduled jobs

Use the built-in **`cron`** tool so recurring work runs in the agent and can **deliver** results to the **current** chat. Jobs persist under `workspace/cron/jobs.json` and survive gateway restarts.

## When to use

- The user asks for a **health check** on a schedule (e.g. every 2 or 15 minutes).
- The user asks to **list scheduled jobs** or **remove** / **stop** a job.

## Adding a job

- Use a **recurring interval** with `schedule.kind: "every"` and `every_ms` in milliseconds (e.g. 2 minutes → `120000`, 15 minutes → `900000`).
- Set **`deliver: true`** so each run posts the summary back to the chat when that is what the user wants.
- The **`message`** for each run should instruct the agent to: run the observability flow (`mcp_obs_logs_error_count` / `mcp_obs_logs_search`, then `mcp_obs_traces_get` if a `trace_id` appears), then give a **short** summary; if there are no recent errors, state that the **system looks healthy**.
- Bind the job to the **current session**: set **`channel`** and **`to`** (or the fields your tool schema uses for routing) from the **active** user/channel context — e.g. web chat is typically `webchat` with `to` set to the current session identifier.

## Listing and removing

- **"List scheduled jobs."** → use **`cron`** with the **list** action and echo job names, intervals, and ids clearly.
- **Remove a test job** → use **`cron`** with the **remove** action and the job **id**.

## Do not

- Do not use **`HEARTBEAT.md`** instead of **`cron`** for these recurring in-chat health checks.
- Do not use shell **`crontab`** or **`exec`** to call `nanobot cron` CLI; use the **`cron`** tool.
