from logging import RootLogger
from .loggerService import LoggerService
from .configService import ConfigService
from .dataService import DataService
from .driverService import DriverService
from .testCaseService import TestCaseService
from .emailService import EmailService

class TestCache(object):
    """Test Cache object to store all the services used by the framework. 
    Test Cache object will be initialized and controlled by Bootstrapper 
    
    :param config_service: Config service used to store all configurations
    :type config_service: :class:`ConfigService`
    :param driver_service: Driver service used to create and maintain all the drivers
    :type driver_service: :class:`DriverService`
    :param data_service: Data service used to fetch data from different data sources
    :type data_service: :class:`DataService`
    :param logger_service: Logger service used for logging
    :type logger_service: :class:`LoggerService`
    :param testcase_service: Testcase service used for connecting with Test case management tools
    :type testcase_service: :class:`TestCaseService`
    :param email_service: Email service used for sending reports
    :type email_service: :class:`EmailService`

    """
    def __init__(self,config_service:ConfigService=None,driver_service:DriverService=None,data_service:DataService=None,logger_service:LoggerService=None,testcase_service:TestCaseService=None,email_service:EmailService=None):
        self.config_service = config_service
        self.driver_service = driver_service
        self.data_service = data_service
        self.logger_service = logger_service
        self.testcase_service = testcase_service
        self.email_service = email_service
        self.cache = dict()


    
        
    

    