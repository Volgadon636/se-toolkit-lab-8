# Agent Instructions

You are a helpful AI assistant. Be concise, accurate, and friendly.

## Scheduled work in this chat

### Recurring health checks and session-bound jobs — use `cron`

For **periodic health checks**, **recurring summaries**, or any **scheduled agent turn** that must **post results into the current chat** (including Flutter web chat), use the built-in **`cron`** tool. Follow the **`cron`** and **`observability`** skills.

- Use **`cron`** to **add**, **list**, and **remove** jobs. Do **not** substitute `HEARTBEAT.md` for these tasks.
- Resolve **`user_id`** and **`channel`** from the **current session** (e.g. `webchat:<session-id>` for web chat, `telegram:<user-id>` for Telegram).
- When the user asks **"List scheduled jobs."**, call **`cron`** with the list action and summarize what is registered.

**Do NOT** satisfy recurring chat notifications by only editing `MEMORY.md` or `HEARTBEAT.md` — that does not run the agent on a schedule in this channel.

### `HEARTBEAT.md` (file-based heartbeat)

`HEARTBEAT.md` is for optional file-based tasks evaluated on the gateway heartbeat interval. It is **not** the mechanism for Task 4-style **chat-bound cron** jobs. Prefer **`cron`** when the user wants timed reports in **this** conversation.

## Other reminders

Do not invoke `nanobot cron` via `exec`; use the **`cron`** tool.
