import os
import logging
import logging.config

class LoggerService(object):
    
    def __init__(self,logLevel:str="NOTSET"):
        if not os.path.exists("PytestLogs"):
            os.makedirs("PytestLogs")
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        logging.basicConfig(filename='PytestLogs/app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%d-%m-%y %H:%M:%S')
        self.logger = logging.getLogger(name="pytest_gsapython")
        if logLevel is not None and logLevel.upper() in ["INFO","DEBUG","WARNING","ERROR","CRITICAL"]:
            self.logger.setLevel(logLevel.upper())
        else:
            self.logger.disabled = True