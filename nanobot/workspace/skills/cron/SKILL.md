# Cron — Scheduled Jobs

You have a built-in `cron` tool for creating scheduled jobs that run periodically in the current chat session.

## Tools

- **cron_create** — Create a scheduled job with a cron expression and a prompt to execute
- **cron_list** — List all scheduled jobs in the current session
- **cron_remove** — Remove a scheduled job by its ID

## Usage

### Create a scheduled job

When the user asks for a recurring/periodic task (e.g., "Create a health check that runs every 15 minutes"), use `cron_create` with:

- **schedule**: A cron expression (e.g., `*/15 * * * *` for every 15 minutes)
- **prompt**: The instruction to execute on each run

**Example cron expressions:**
- `*/2 * * * *` — Every 2 minutes
- `*/15 * * * *` — Every 15 minutes
- `0 * * * *` — Every hour at minute 0
- `0 0 * * *` — Every day at midnight

**Example:**
```
User: "Create a health check that runs every 15 minutes."

You call: cron_create(
  schedule="*/15 * * * *",
  prompt="Check for backend errors in the last 15 minutes. If there are errors, summarize them. If no errors, report that the system looks healthy."
)
```

### List scheduled jobs

When the user asks "List scheduled jobs" or "What jobs are running?", call `cron_list` with no arguments.

**Example:**
```
User: "List scheduled jobs."

You call: cron_list()
Response: Shows all active scheduled jobs with their IDs, schedules, and prompts.
```

### Remove a scheduled job

When the user asks to remove or cancel a scheduled job, use `cron_remove` with the job ID.

**Example:**
```
User: "Remove the health check job."

You call: cron_remove(job_id="job-123")
```

## Health Check Pattern

For proactive health checks, the prompt should:

1. Check for recent errors using `logs_error_count` or `logs_search`
2. If errors are found, optionally fetch a trace using `traces_list` and `traces_get`
3. Post a short summary to the chat

**Example health check prompt:**
> Check for backend errors in the last 2 minutes using logs_error_count. If errors exist, fetch recent traces and summarize the failure. If no errors, report that the system looks healthy. Post your findings here.

## Important Notes

- Jobs are tied to the current chat session (USER_ID and CHANNEL)
- Do not use `exec` to run `nanobot cron` commands — use the built-in `cron_*` tools directly
- For recurring tasks, prefer scheduled jobs over writing to `HEARTBEAT.md` (which runs on a different interval)
- Always confirm with the user before creating or removing scheduled jobs
