# cad_pipeline/cad_engine/globals/error_handler.py
import logging

# Configure logging as needed
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def log_error(message, exception=None):
    """
    Logs an error message with optional exception details.
    """
    if exception:
        logging.error(f"{message}: {exception}")
    else:
        logging.error(message)
