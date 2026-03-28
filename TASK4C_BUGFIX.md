# Task 4C — Bug Fix and Recovery

## Root Cause

The planted bug was in `backend/app/routers/items.py` in the `get_items` endpoint.

**Bug (commit 1a608316):**
```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Items not found",
        ) from exc
```

This caught ALL exceptions (including database connection errors) and incorrectly returned HTTP 404 "Items not found" instead of letting the real error propagate.

## Fix

**Fixed (commit 0482c26e):**
```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    return await read_items(session)
```

The try/except block was removed, allowing database exceptions to propagate as 500 errors.

## Diff

```diff
@@ -14,13 +14,7 @@ router = APIRouter()
 @router.get("/", response_model=list[ItemRecord])
 async def get_items(session: AsyncSession = Depends(get_session)):
     """Get all items."""
-    try:
-        return await read_items(session)
-    except Exception as exc:
-        raise HTTPException(
-            status_code=status.HTTP_404_NOT_FOUND,
-            detail="Items not found",
-        ) from exc
+    return await read_items(session)
```

## Post-Fix Failure Check

With PostgreSQL stopped, the agent's response to "What went wrong?" now shows:
- Real database connection error in logs
- Proper 500 status code (not 404)
- Accurate root cause: database unavailable

## Healthy Follow-Up

After restarting PostgreSQL, the health check reports:
- No recent errors
- System looks healthy
- All endpoints responding normally
