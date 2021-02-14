import sys,os 
import pytest               
import importlib
from .testCache import TestCache
from .loggerService import LoggerService
from .configService import ConfigService
from .dataService import DataService
from .driverService import DriverService
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

    def RunNunitTest(self,nunitmodel:str):
        assemblyName =  self.testCache.config_service.getCustomSettings('nunitsettings').get('assemblyname')
        outputPath = os.path.join(os.path.curdir,"Output")

        import subprocess
        from subprocess import Popen,PIPE

        if("unicorn" in nunitmodel.lower()):
            tmp = nunitmodel.split(sep='=',maxsplit=1)
            testcaseid = tmp[1]
            testfilter = "\"test=~\'"+testcaseid+"\'\""
        elif("specflow" in nunitmodel.lower()):
            tmp = nunitmodel.split(sep='=',maxsplit=1)
            testcaseid = tmp[1]
            testfilter = "\"cat=~\'"+testcaseid+"\'\""
        elif(nunitmodel.strip().isnumeric()): 
            testcaseid = nunitmodel.strip()
            testfilter = "\"test=~\'"+testcaseid+"\'\""
        else:
            raise NotImplementedError("Option not available in RunNunitTest")        

        arg = "C:\\Temp\\sg_mutate\\NUnit.Console\\bin\\net35\\nunit3-console.exe "+assemblyName+" --work="+outputPath+" --where "+testfilter
      
        self.testCache.logger_service.logger.debug("Triggering Nunit Test from Console")
        self.testCache.logger_service.logger.debug("Cmd: "+arg)
        process = Popen(args=arg,stdout=PIPE,stderr=PIPE)
        stdout, stderr = process.communicate() 

        stdstr = stdout.decode('utf8')
        print(stdstr)
        if(str.__contains__(stdstr,"Passed: 1")):
            self.testCache.logger_service.logger.debug("Nunit Test Passed")
        else:
            self.testCache.logger_service.logger.debug("Nunit Test Failed")
            pytest.fail(msg="",pytrace=False)
       

       

        
        # pytest.fail(msg="failure message")
        
        


     

           

        

    
    




        
