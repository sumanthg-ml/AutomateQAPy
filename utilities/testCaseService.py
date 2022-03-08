import csv
from .configService import ConfigService
from .loggerService import LoggerService
from os import path
class TestCaseService(object):    

    sourceFilePath = None
    currentTestCase = None
    _testCache = None

   # place holders for test case management services
    @classmethod
    def Init(cls,obj):
        cls._testCache = obj.testCache

    def __init__(self):
        self.sourceFilePath = self._testCache.config_service.get("testcasesource")
        

    def __readTestCases(self,sourceFilePath):
        self._testCache.logger_service.logger.debug("Reading test case mapper file - "+sourceFilePath)


    def __checkFileExists(self,sourceFilePath):
        return path.exists(sourceFilePath)

    def __generateTestCaseMap(self,sourceFilePath):
        self._testCache.logger_service.logger.debug("Creating test case mapper file - "+sourceFilePath)

