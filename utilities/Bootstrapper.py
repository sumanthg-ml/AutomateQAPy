from re import S
import sys,os 
import pytest               
import importlib
import driverhandles
from .testCache import TestCache
from .loggerService import LoggerService
from .configService import ConfigService
from .dataService import DataService
from driverhandles.driverService import DriverService
from .testCaseService import TestCaseService
from .emailService import EmailService

class Bootstrapper(): 
    """Bootstrapper class use to control the setup and teardown activities.
    Initializes new instance of :class:`TestCache`

    """
    def __init__(self,applicationType=None):        
        self.testCache = TestCache()        
        #Config service
        if self.testCache.config_service is None:            
            self.testCache.config_service = ConfigService()

    def InitServices(self):
        #Intialize all services for TestCache
        #Logger service
        if self.testCache.logger_service is None:            
            self.testCache.logger_service = LoggerService(self.testCache.config_service.get('loglevel'))
        self.testCache.logger_service.logger.info("Bootstrap Master Initialize...")

        #Data service
        if self.testCache.data_service is None and (self.testCache.config_service.get('framework')=="pytest"): 
            DataService.Init(self)           
            self.testCache.data_service = DataService()
        
        #Driver service
        if self.testCache.driver_service is None and (self.testCache.config_service.get('framework')=="pytest"):  
            DriverService.Init(self)          
            self.testCache.driver_service = DriverService()

        #Testcase service
        if self.testCache.testcase_service is None:
            TestCaseService.Init(self)
            self.testCache.testcase_service = TestCaseService()

        #Email service
        if self.testCache.email_service is None:
            EmailService.Init(self)
            self.testCache.email_service = EmailService()
    
       
    def DriverInitialize(self,driverName):    
        if (self.testCache.config_service.get('framework')=="pytest"):    
            self.testCache.driver_service.initializeDriver(driverName)
        
    def SwitchTestCase(self,testCase):
        self._testCaseId = testCase['TestCaseId']
        if (self.testCache.config_service.get('framework')=="pytest"):
            self.testCache.data_service.switchTestData(self._testCaseId)
        self.testCache.testcase_service.currentTestCase = testCase

    def DriverCleanup(self):      
        if (self.testCache.config_service.get('framework')=="pytest"):            
            self.testCache.driver_service.killDriver()

    def SessionCleanup(self):         
        if (self.testCache.config_service.get('framework')=="pytest"):            
            self.testCache.driver_service.cleanupAllDrivers()
        self.testCache.logger_service.logger.info("Bootstrap Master Cleanup...")
        self.testCache = None

   
           

        

    
    




        
