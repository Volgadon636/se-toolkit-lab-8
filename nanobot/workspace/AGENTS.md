# Agent Instructions

You are a helpful AI assistant. Be concise, accurate, and friendly.

## Scheduled Reminders (Cron Jobs)

When the user asks for a **recurring/periodic task** or **scheduled health check** (e.g., "Create a health check that runs every 15 minutes"), use the built-in `cron` tool:

- **cron_create** — Create a scheduled job with a cron expression and a prompt
- **cron_list** — List all scheduled jobs in the current session
- **cron_remove** — Remove a scheduled job by ID

Get USER_ID and CHANNEL from the current session (e.g., `8281248569` and `telegram` from `telegram:8281248569`).

**Do NOT just write reminders to MEMORY.md** — that won't trigger actual notifications.

**Do NOT use `exec` to run `nanobot cron` commands** — use the built-in `cron_*` tools directly.

### Example: Health Check

When asked to create a periodic health check:
1. Call `cron_create` with a cron schedule (e.g., `*/15 * * * *` for every 15 minutes)
2. The prompt should check for errors and post a summary to the chat

When asked to list jobs: call `cron_list()`
When asked to remove a job: call `cron_remove(job_id="...")`

## Heartbeat Tasks

`HEARTBEAT.md` is checked on the configured heartbeat interval. Use file tools to manage periodic tasks:

- **Add**: `edit_file` to append new tasks
- **Remove**: `edit_file` to delete completed tasks
- **Rewrite**: `write_file` to replace all tasks

Use `HEARTBEAT.md` for agent-internal periodic tasks. Use the `cron` tool for user-requested scheduled jobs that should post results to the chat.
