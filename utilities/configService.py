from dynaconf import settings

class ConfigService(object):
    """Class used to read config values from settings file
    """
    __settings = settings

    def __init__(self):
        self.__settings = settings      
    
 
    def get(self,configName):
        stn = self.__settings.get(configName)
        return stn


    def set(self,configName,value):
        self.__settings[configName] = value
     

    def getCustomSettings(self,customKeyName):
        stn = self.__settings.from_env(env=customKeyName)
        return stn


    def setCustomSettings(self,customKeyName,configName,value):
        self.__settings.setenv(customKeyName)
        self.__settings[configName] = value
        self.__settings.setenv()
        
        
    