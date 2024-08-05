import atexit

class Log():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
            cls._instance._log = []
            atexit.register(cls._instance.print_log)
        return cls._instance

    def clear(self):
        self._log = []

    def log(self, message):
        print(message)
        self._log.append(message)

    def get(self):
        return self._log

    def print_log(self):
        for message in self._log:
            print(message)
