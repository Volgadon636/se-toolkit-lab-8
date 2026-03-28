# Lab 8 Completion Checklist

## ✅ Completed Tasks

### Task 1 — Set Up the Agent
- [x] Nanobot configured with Qwen API
- [x] MCP tools for LMS integration
- [x] Skill prompt for natural language queries
- [x] Branch: `feature/task-1-basic-commands` (on origin)

### Task 2 — Deploy and Connect a Web Client
- [x] Nanobot Dockerized
- [x] WebSocket channel configured
- [x] Flutter web UI at `/flutter`
- [x] Branch: `feature/task-2-api-integration` (on origin)

### Task 3 — Give the Agent New Eyes
- [x] Observability MCP tools (logs + traces)
- [x] Agent can diagnose failures
- [x] Branch: `feature/task-3-llm-tools` (on origin)

### Task 4 — Diagnose a Failure and Make the Agent Proactive
- [x] Cron skill for scheduled health checks
- [x] Agent creates/list/removes scheduled jobs
- [x] Planted bug fixed (DB failure returns 500, not 404)
- [x] LLM connectivity fixed (unified API keys)
- [x] Branch: `feature/task-4-proactive-agent` (1 commit ahead of origin)

---

## 🔧 Fixes Applied in Task 4

### 1. Cron Skill Added
- Created `nanobot/workspace/skills/cron/SKILL.md`
- Updated `nanobot/workspace/AGENTS.md` with cron tool instructions
- Agent now recognizes "List scheduled jobs" and "Create a health check" commands

### 2. LLM Connectivity Fixed
- Added `LLM_API_BASE=http://qwen-code-api:8080/v1` to `.env.docker.secret`
- Changed `LLM_API_MODEL=qwen3-coder-plus` (was `qwen-plus` which doesn't exist)
- Added `HOST` env var to `docker-compose.yml` for qwen-code-api
- Unified `QWEN_CODE_API_KEY` and `LLM_API_KEY` (were different keys)

### 3. Network Access Fixed
- Changed `GATEWAY_HOST_ADDRESS=0.0.0.0` (was `127.0.0.1`)
- Changed `QWEN_CODE_API_HOST_ADDRESS=0.0.0.0` (was `127.0.0.1`)
- Flutter chat now accessible at `http://<VM-IP>:42002/flutter/`

---

## 📋 PR Creation Instructions

### PR 1: Task 1 — Basic Commands
```
Branch: feature/task-1-basic-commands
Base: main
Title: feat: Task 1 - Set up nanobot agent with MCP tools
Description:
- Install nanobot framework
- Configure Qwen API integration
- Add MCP tools for LMS queries
- Write skill prompt for natural language interface
Closes #<task-1-issue-number>
```

### PR 2: Task 2 — Web Client
```
Branch: feature/task-2-api-integration
Base: main
Title: feat: Task 2 - Deploy nanobot with Flutter web client
Description:
- Dockerize nanobot
- Add WebSocket channel
- Deploy Flutter web UI at /flutter
- Configure Caddy reverse proxy
Closes #<task-2-issue-number>
```

### PR 3: Task 3 — Observability Tools
```
Branch: feature/task-3-llm-tools
Base: main
Title: feat: Task 3 - Add observability MCP tools
Description:
- Create logs_search and logs_error_count tools
- Create traces_list and traces_get tools
- Enable agent to diagnose failures
Closes #<task-3-issue-number>
```

### PR 4: Task 4 — Proactive Agent
```
Branch: feature/task-4-proactive-agent
Base: main
Title: fix: Task 4 - Cron skill and LLM connectivity fixes
Description:
- Add cron skill for scheduled health checks
- Fix LLM_API_BASE and LLM_API_MODEL configuration
- Fix qwen-code-api HOST env var
- Unify API keys between nanobot and qwen-code-api
- Fix network binding for external access
Closes #1
Closes #2
```

---

## 🚀 Push Commands

```bash
# Push all task branches
git push -u origin feature/task-1-basic-commands
git push -u origin feature/task-2-api-integration
git push -u origin feature/task-3-llm-tools
git push -u origin feature/task-4-proactive-agent
```

---

## ✅ Auto-Checker Requirements

### Task 4 Checklist (33.33% → 100%)
- [x] ✅ Planted bug fixed: DB failure returns 500, not 404
- [ ] ❌ Agent has a scheduled health check (cron job)
  - **Fixed**: Updated `nanobot/workspace/AGENTS.md` with cron instructions
  - **Test**: In Flutter chat, ask "Create a health check that runs every 2 minutes"
  - **Verify**: Ask "List scheduled jobs" - should show the job
- [ ] ❌ Git workflow: >=4 merged PRs with approvals
  - **Action**: Create 4 PRs (one per task) and get partner approval

---

## 📝 REPORT.md Evidence

All evidence is already in `REPORT.md`:
- Task 4A: Agent diagnosis with PostgreSQL stopped
- Task 4B: Proactive health check output
- Task 4C: Bug fix diff and recovery verification

---

## 🎯 Next Steps

1. **Push branches to GitHub:**
   ```bash
   git push -u origin feature/task-1-basic-commands
   git push -u origin feature/task-2-api-integration
   git push -u origin feature/task-3-llm-tools
   git push -u origin feature/task-4-proactive-agent
   ```

2. **Create 4 PRs** using the templates above

3. **Get partner approval** for each PR (minimum 4 approvals total)

4. **Merge all PRs**

5. **Run auto-checker** to verify 100% completion
