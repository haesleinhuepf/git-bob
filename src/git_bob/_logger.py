import logging
import sys

def setup_logger(name, level=logging.INFO):
    """
    Set up and configure a logger.

    Parameters
    ----------
    name : str
        Name of the logger.
    level : int, optional
        Logging level, by default logging.INFO.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger