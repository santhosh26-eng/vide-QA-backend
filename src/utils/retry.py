import time

from src.utils.logger import logger


def retry(function, retries=3, delay=2):
    """
    Retry a function if it fails.

    Parameters:
        function : callable
        retries : number of retry attempts
        delay : delay between retries (seconds)
    """

    last_exception = None

    for attempt in range(1, retries + 1):

        try:
            logger.info(f"Attempt {attempt}/{retries}")

            return function()

        except Exception as e:

            last_exception = e

            logger.warning(
                f"Attempt {attempt} failed: {str(e)}"
            )

            if attempt < retries:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)

    logger.error("All retry attempts failed.")

    raise last_exception