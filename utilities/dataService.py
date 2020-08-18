
import dynaconf

class DataService(object):
    """Class used to read and store data from data file
    """
    _testCache = None

    @classmethod
    def Init(cls,obj):
        cls._testCache = obj.testCache

    def __init__(self):  
        self.__readTestData()

    def __readTestData(self):
        filePath = self._testCache.config_service.get('testdatapath')
        self._testCache.logger_service.logger.debug("Reading test data from - " + filePath)
        self.__defaultdata = dynaconf.LazySettings(SETTINGS_FILE_FOR_DYNACONF=filePath)

    def switchTestData(self,testCaseId):
        self._testCache.logger_service.logger.debug("Switching current test case data to - "+testCaseId)
        self.testCaseId = testCaseId
        self.__testdata = self.__defaultdata
        try: self.__testdata = self.__defaultdata.from_env(self.testCaseId) 
        except: self._testCache.logger_service.logger.error("Switching test data failed")

    def get(self,dataName):
        data = None
        try: data = self.__testdata.get(dataName)
        except: self._testCache.logger_service.logger.error("Getting test data failed : "+dataName)
        return data