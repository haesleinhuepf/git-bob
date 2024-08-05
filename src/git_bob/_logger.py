import logging

def get_logger(name):
  """Gets a logger with the given name.

  Parameters
  ----------
  name : str
      The name of the logger.

  Returns
  -------
  logging.Logger
      A logger with the given name.
  """
  logger = logging.getLogger(name)
  logger.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  # Create a file handler
  file_handler = logging.FileHandler('git_bob.log')
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)
  return logger