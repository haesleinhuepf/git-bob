import logging

def setup_logger(log_level=logging.INFO, log_file=None):
    """
    Sets up a logger with the given log level and log file.

    Parameters
    ----------
    log_level : int, optional
        The logging level, by default logging.INFO.
    log_file : str or None, optional
        The file to log to, by default None (logs to stdout).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger('git_bob_logger')
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def log_message(logger, message, level=logging.INFO):
    """
    Logs a message with the given logger and level.

    Parameters
    ----------
    logger : logging.Logger
        The logger instance to use for logging.
    message : str
        The message to log.
    level : int, optional
        The logging level, by default logging.INFO.

    Returns
    -------
    None
    """
    if level == logging.DEBUG:
        logger.debug(message)
    elif level == logging.INFO:
        logger.info(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.CRITICAL:
        logger.critical(message)

def close_logger(logger):
    """
    Closes all handlers for the given logger.

    Parameters
    ----------
    logger : logging.Logger
        The logger instance to close.

    Returns
    -------
    None
    """
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)