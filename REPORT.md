# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

## Task 2A — Deployed agent

```text
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-03-28 15:49:57.663 | INFO     | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | 2026-03-28 15:49:57.668 | INFO     | nanobot.cron.service:start:202 - Cron service started with 0 jobs
nanobot-1  | 2026-03-28 15:50:00.406 | INFO     | nanobot.agent.loop:run:280 - Agent loop started
```

## Task 2B — Web client

WebSocket connection test through Caddy:
```text
Response: {"type":"text","content":"Here are the available labs:\n\n| Lab ID | Title |\n|--------|-------|\n| lab-01 | Lab 01 – Products, Architecture & Roles |\n| lab-02 | Lab 02 — Run, Fix, and Deploy a Backend Service |\n| lab-03 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy |\n| lab-04 | Lab 04 — Testing, Front-end, and AI Agents |\n| lab-05 | Lab 05 — Data Pipeline and Analytics Dashboard |\n| lab-06 | Lab 06 — Build Your Own Agent |\n| lab-07 | Lab 07 — Build a Client with an AI Coding Agent |\n| lab-08 | lab-08 |\n\nYou can ask me about any specific lab's performance metrics, completion rates, pass rates, top learners, submission timeline, or group performance. Just let me know which lab you're interested in!","format":"markdown"}
```

Verified end-to-end path through Caddy reverse-proxy:
- Flutter UI accessible at `/flutter`
- WebSocket connection available at `/ws/chat` with `access_key` authentication.
- Agent uses `mcp_lms` to fetch real data and `mcp_webchat` to deliver structured messages.

## Task 3A — Structured logging

Happy-path log excerpt:
```text
backend-1  | 2026-03-28 15:58:09,749 INFO [lms_backend.main] [main.py:62] [trace_id=e242ec3c660506333e0c48f81e58f625 span_id=b48939f5ef7520aa resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-28 15:58:09,750 INFO [lms_backend.auth] [auth.py:30] [trace_id=e242ec3c660506333e0c48f81e58f625 span_id=b48939f5ef7520aa resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-28 15:58:09,753 INFO [lms_backend.db.items] [items.py:16] [trace_id=e242ec3c660506333e0c48f81e58f625 span_id=b48939f5ef7520aa resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-28 15:58:09,833 INFO [lms_backend.main] [main.py:74] [trace_id=e242ec3c660506333e0c48f81e58f625 span_id=b48939f5ef7520aa resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.5:51554 - "GET /items/ HTTP/1.1" 200 OK
```

Error-path log excerpt:
```text
backend-1  | socket.gaierror: [Errno -2] Name or service not known
backend-1  | 2026-03-28 15:57:24,421 INFO [lms_backend.main] [main.py:62] [trace_id=03cf781f670cfcf50fd6da1399bad487 span_id=7fc7cd33a2aa4dd6 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-28 15:57:24,424 INFO [lms_backend.auth] [auth.py:30] [trace_id=03cf781f670cfcf50fd6da1399bad487 span_id=7fc7cd33a2aa4dd6 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-28 15:57:24,425 INFO [lms_backend.db.items] [items.py:16] [trace_id=03cf781f670cfcf50fd6da1399bad487 span_id=7fc7cd33a2aa4dd6 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-28 15:57:25,089 ERROR [lms_backend.db.items] [items.py:23] [trace_id=03cf781f670cfcf50fd6da1399bad487 span_id=7fc7cd33a2aa4dd6 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-28 15:57:25,091 WARNING [lms_backend.routers.items] [items.py:23] [trace_id=03cf781f670cfcf50fd6da1399bad487 span_id=7fc7cd33a2aa4dd6 resource.service.name=Learning Management Service trace_sampled=True] - items_list_failed_as_not_found
backend-1  | 2026-03-28 15:57:25,094 INFO [lms_backend.main] [main.py:74] [trace_id=03cf781f670cfcf50fd6da1399bad487 span_id=7fc7cd33a2aa4dd6 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.5:59170 - "GET /items/ HTTP/1.1" 404 Not Found
```

## Task 3B — Traces

Observations from VictoriaTraces:
- Healthy trace (e.g., `e242ec3c660506333e0c48f81e58f625`) shows sequential spans for `request_started`, `auth_success`, `db_query`, and `request_completed`.
- Error trace (e.g., `03cf781f670cfcf50fd6da1399bad487`) shows `db_query` span with an error tag and the `socket.gaierror` exception details when PostgreSQL was stopped.

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

**What went wrong?**

## Root Cause Analysis

**What went wrong:** The LMS backend cannot connect to its PostgreSQL database due to a **DNS resolution failure**.

### Evidence from Trace `a9eb93b817e9d2e466f233a304fbd579`

| Span | Operation | Status | Details |
|------|-----------|--------|---------|
| `GET /items/` | HTTP Request | ❌ 404 | Main request to list labs |
| `connect` | DB Connection | ❌ ERROR | `socket.gaierror: [Errno -2] Name or service not known` |

### Failure Chain

1. **Request received:** `GET /items/` at `http://backend:8000/items/`
2. **Database connection attempted:** 
   - Target: `postgres:5432` (hostname: `postgres`, port: `5432`)
   - Database: `db-lab-8`
   - User: `postgres`
3. **DNS resolution failed:** The hostname `postgres` cannot be resolved
4. **Request failed:** Returned HTTP 404 instead of lab data

### Technical Details

```
Exception: socket.gaierror: [Errno -2] Name or service not known
Location: asyncpg/connect_utils.py → _connect_addr
```

The LMS backend is trying to connect to a PostgreSQL database at hostname `postgres`, but that hostname doesn't resolve in the network. This is typically a **Docker/networking configuration issue** where:

- The database container isn't running
- The database container isn't on the same Docker network
- The database hostname in the connection string is incorrect

### Affected Services
- **Learning Management Service** (backend:8000) - Unable to serve any lab data
- All LMS queries (labs, learners, pass rates, etc.) will fail

**Fix required:** Infrastructure team needs to verify the PostgreSQL database container is running and properly networked with the LMS backend.

## Task 4B — Proactive health check

**Proactive Report:**

```text
## 🔍 Health Check Summary (2-minute window)

**Status: ⚠️ Issues Detected**

### Errors Found: 2

**Service:** Learning Management Service  
**Time Window:** 17:02 - 17:04 UTC

**Root Cause:** Database connectivity failure (recurring issue)
- **Error:** `socket.gaierror: [Errno -2] Name or service not known`
- **Operation:** PostgreSQL connection attempts to `postgres:5432`
- **Impact:** GET `/items/` requests returning HTTP 404

**Trace Analysis:**
Both errors show the same pattern - the LMS backend cannot resolve the PostgreSQL database hostname (`postgres`). This is a persistent DNS/network connectivity issue in the container network.

**Timeline:**
- 17:03:14 UTC - First db_query failure
- 17:03:21 UTC - Second db_query failure

**Recommendation:** The PostgreSQL service appears to be down or unreachable. Check:
1. PostgreSQL container/service status
2. Docker network connectivity between backend and postgres
3. DNS resolution within the container network
```

## Task 4C — Bug fix and recovery

1. **Root cause** — The planted bug was in `backend/src/lms_backend/routers/items.py` in the `get_items` function. It caught any `Exception` and raised an `HTTPException` with status code 404, which hid the real error (like a database connection failure) and misreported it as "Items not found".
2. **Fix** — Removed the `try...except` block that was suppressing the real error. Now the exception bubbles up and results in an HTTP 500 Internal Server Error, allowing the agent to see the real cause in logs and traces.
   
   ```python
   @router.get("/", response_model=list[ItemRecord])
   async def get_items(session: AsyncSession = Depends(get_session)):
       """Get all items."""
       return await read_items(session)
   ```
3. **Post-fix failure check** — Agent's response to **"What went wrong?"** after redeploy and stopping PostgreSQL:

```text
## What Went Wrong: LMS Backend Failure

**Summary:** The Learning Management Service is down due to a **database connectivity failure** caused by DNS resolution issues.

---

### Evidence

**Logs (last 10 minutes):**
- **7 errors** detected in the Learning Management Service
- Error message: `[Errno -2] Name or service not known`
- Failed operation: `db_query` on table `item`

**Trace Analysis (`4b64afd66def539e05e678a701d06246`):**
The trace shows the complete failure chain:

| Span | Operation | Duration | Status |
|------|-----------|----------|--------|
| `GET /items/` | HTTP request | 412ms | ❌ Error |
| `connect` | PostgreSQL connection | 356ms | ❌ Error |
| `http send` | Response | 45ms | ❌ HTTP 500 |

**Root Cause Span Details:**
- **Database**: PostgreSQL (`db-lab-8`)
- **Target**: `postgres:5432`
- **Error**: `socket.gaierror: [Errno -2] Name or service not known`
- **Location**: `asyncpg/connect_utils.py` → DNS lookup failed
```

4. **Healthy follow-up** — Healthy report after restarting PostgreSQL:

```text
**Health Check Report** ✅

- **Backend errors (last 2 min):** 0
- **ERROR logs (last 2 min):** None found

System looks healthy.
```
Task 3 completion confirmed.
