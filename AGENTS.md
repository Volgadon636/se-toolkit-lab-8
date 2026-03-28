## Project structure

- `bot/` — the Telegram bot (built across tasks 1–4).
  - `bot/bot.py` — entry point with `--test` mode.
  - `bot/handlers/` — command handlers, intent router.
  - `bot/services/` — API client, LLM client.
  - `bot/PLAN.md` — implementation plan.
- `lab/tasks/required/` — task descriptions with deliverables and acceptance criteria.
- `wiki/` — project documentation.
- `backend/` — the FastAPI backend the bot queries.
- `client-web-flutter/` — the Flutter web client.
- `.env.docker.secret` — all credentials: backend API, bot token, LLM (gitignored).

## Flutter

Flutter is not installed locally. Run Flutter CLI commands via the poe task (uses Docker):

```sh
uv run poe flutter <args>
```

For example: `uv run poe flutter analyze lib/chat_screen.dart`
