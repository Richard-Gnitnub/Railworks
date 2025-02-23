import logging

def log_error(message: str, exception: Exception = None):
    """
    Logs an error message in a standardised format.
    
    Parameters:
        message (str): The error message to log.
        exception (Optional[Exception]): An optional exception instance for additional context.
    """
    if exception:
        logging.error(f"{message}: {exception}")
    else:
        logging.error(message)
