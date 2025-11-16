from datetime import datetime, timezone


def get_datetime() -> datetime:
    """Return current UTC datetime without timezone info (naive datetime)."""
    utc_time = datetime.now(timezone.utc)
    return utc_time.replace(tzinfo=None)
