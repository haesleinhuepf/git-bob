class Logger:
    def __init__(self, log_file):
        """
        Initialize the Logger.

        Parameters
        ----------
        log_file : str
            Path to the log file where messages will be written.
        """
        self.log_file = log_file

    def log(self, message, level='INFO'):
        """
        Log a message to the log file.

        Parameters
        ----------
        message : str
            The message to be logged.
        level : str, optional
            The severity level of the log message (default is 'INFO').

        Returns
        -------
        None
        """
        with open(self.log_file, 'a') as f:
            f.write(f"{level}: {message}\n")

    def info(self, message):
        """
        Log an informational message.

        Parameters
        ----------
        message : str
            The message to be logged.

        Returns
        -------
        None
        """
        self.log(message, level='INFO')

    def warning(self, message):
        """
        Log a warning message.

        Parameters
        ----------
        message : str
            The message to be logged.

        Returns
        -------
        None
        """
        self.log(message, level='WARNING')

    def error(self, message):
        """
        Log an error message.

        Parameters
        ----------
        message : str
            The message to be logged.

        Returns
        -------
        None
        """
        self.log(message, level='ERROR')