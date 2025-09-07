import logging

def get_logger(name: str):
    """
    Returns a logger with consistent formatting.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # Prevent duplicate handlers
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
