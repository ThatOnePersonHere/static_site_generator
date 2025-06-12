import os
import shutil
import logging
from datetime import datetime
from enum import Enum

class LogLevel(Enum):
	INFO = "info"
	DEBUG = "debug"
	ERROR = "error"


class LogRecord():
    def __init__(self):
        self.name = logging.getLogger(__name__)
        self.location = './logs/'
       
    def logger_setup(self, logging_level):
        if os.path.exists(self.location) == False:
            os.mkdir(self.location)
        LOGFILENAME = self.location + datetime.now().strftime('logfile_%H%M%S_%d%m%Y.log')
        logging.basicConfig(format='%(asctime)s %(message)s',filename=LOGFILENAME, encoding='utf-8', level=logging_level)
        self.remove_old_logs()

    def remove_old_logs(self):
        if len(os.listdir(path=self.location)) > 5:
            oldest_file = min(os.listdir(path=self.location))
            self.name.info(f'Deleted file: {oldest_file}')
            os.remove(self.location+oldest_file)
            self.remove_old_logs()
    
    def logItem(self, level, text):
       self.getLogLevel(level)(text)
    
    def getLogLevel(self, level):
        if level not in LogLevel:
            raise ValueError(f"Invalid log level: {level}")
        match LogLevel(level):
            case LogLevel.INFO:
                return self.name.info
            case LogLevel.DEBUG:
                return self.name.debug
            case LogLevel.ERROR:
                return self.name.error