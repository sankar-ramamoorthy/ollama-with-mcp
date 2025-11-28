from datetime import datetime, timezone

def current_datetime() -> str:
    """Return current UTC date/time."""
    return datetime.now(timezone.utc).isoformat()
