import logging
from fastmcp import tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def current_date():
    """
    Returns the current date as a string.
    """
    import datetime
    now = datetime.datetime.now()
    logger.info(f"[current_date] Returning current date: {now}")
    return now.isoformat()
