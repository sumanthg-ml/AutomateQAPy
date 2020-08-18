from selenium import webdriver as seleniumWebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from appium import webdriver as appiumDriver
import pywinauto
from pywinauto import application

from utilities.configService import ConfigService
from utilities.loggerService import LoggerService

class DriverService(object):
    
    _testCache = None

    @classmethod
    def Init(cls,obj):
        cls._testCache = obj.testCache

    def __init__(self):
        self._configService = self._testCache.config_service
        self.driver = None
        self.drivers = list()
        
        _driverType = self._configService.get("drivertype") 
        if isinstance(_driverType,list):
            #create multi drivers         
            for item in _driverType:
                self.drivers.append({'driverName':item[0],'driverType':item[1],'driver':None})
        else:
            #create single driver
            self.drivers.append({'driverName':"Default",'driverType':_driverType,'driver':None})  


    def __create_driver(self,driverName,driverType): 
        dr = None

        if (driverType == "pywinauto"):
            pywinautoSettings = self._configService.getCustomSettings('pywinautosettings-'+driverName)
            if pywinautoSettings.get('launchapp'):
                self._testCache.logger_service.logger.debug("Launching windows driver")                
                dr = application.Application(backend=pywinautoSettings.get('backend')).start(pywinautoSettings.get('apppath'),timeout=10,wait_for_idle=True)
 
            else:
                self._testCache.logger_service.logger.debug("Connecting to existing driver")
                dr = application.Application(backend=pywinautoSettings.get('backend')).connect(title_re=pywinautoSettings.get('apptitle'),timeout=10)
  

        elif (driverType == "selenium"):
            self.selenium_options = None
            seleniumSettings = self._configService.getCustomSettings('seleniumsettings-'+driverName)
            self._testCache.logger_service.logger.debug("Launching selenium driver")
            dr:WebDriver = self.__create_selenium_driver(seleniumSettings.get('browser'))
           
            dr.maximize_window()
            dr.implicitly_wait(5)
            dr.get(seleniumSettings.get('appurl'))           

        elif (driverType == "appium"): 
            desired_caps = self._configService.getCustomSettings('appiumsettings-'+driverName)      
            self._testCache.logger_service.logger.debug("Launching appium driver")     
            dr = appiumDriver.Remote(self._configService.get('remoteurl'), desired_caps)

        elif (driverType == "nunit"):            
            pass
            
        else:
            pass
        #Add driver to dict
        self.__addToDriverCache(driverName,driverType,dr)
        return dr
    

    def __addToDriverCache(self,driverName,driverType,driver):
        self._testCache.logger_service.logger.debug("Adding driver to cache")
        next(filter((lambda d: d['driverName']==driverName),self.drivers))['driver'] = driver
        

    def initializeDriver(self,driverName):
        self._testCache.logger_service.logger.debug("Switching current driver to - "+driverName)
        drDict = next(filter((lambda d: d['driverName']==driverName),self.drivers))
        if(drDict['driver'] == None):
            self.__create_driver(drDict['driverName'],drDict['driverType'])
        self.driver = next(filter((lambda d: d['driverName']==driverName),self.drivers))['driver']

    def killDriver(self): 
        dr = next(filter((lambda d: d['driver']==self.driver),self.drivers))  
        driverName = dr['driverName']     
        driverType = dr['driverType']
        driver = dr['driver']     
           
        if driver is not None:       
            self._testCache.logger_service.logger.debug("Killing current driver - "+driverName)     
            if (driverType == "pywinauto"):
                pywinautoSettings = self._configService.getCustomSettings('pywinautosettings-'+driverName)
                killApp = pywinautoSettings.get("killapp")
                if killApp:
                    driver.kill()
                    
            elif (driverType == "selenium"):
                driver.close()
                driver.quit()

            elif (driverType == "appium"): 
                driver.close()
                driver.quit()

            self.driver = None
            next(filter((lambda d: d['driverName']==driverName),self.drivers))['driver'] = None

    def cleanupAllDrivers(self):
        for dr in self.drivers:
            driverName = dr['driverName']
            driverType = dr['driverType']
            driver = dr['driver']
            if driver is not None:       
                self._testCache.logger_service.logger.debug("Killing driver - "+driverName)     
                if (driverType == "pywinauto"):
                    pywinautoSettings = self._configService.getCustomSettings('pywinautosettings-'+driverName)
                    killApp = pywinautoSettings.get("killapp")
                    if killApp:
                        driver.kill()
                        
                elif (driverType == "selenium"):
                    driver.close()
                    driver.quit()
                elif (driverType == "appium"): 
                    driver.close()
                    driver.quit()

    #---------------------------------------Selenium driver Private functions---------------------------------------------------#

    __browser_names = {
        'googlechrome': "chrome",
        'gc': "chrome",
        'chrome': "chrome",
        'headlesschrome': 'headless_chrome',
        'ff': 'firefox',
        'firefox': 'firefox',
        'headlessfirefox': 'headless_firefox',
        'ie': 'ie',
        'internetexplorer': 'ie',
        'edge': 'edge',
        'opera': 'opera',
        'safari': 'safari',
        'phantomjs': 'phantomjs',
        'htmlunit': 'htmlunit',
        'htmlunitwithjs': 'htmlunit_with_js',
        'android': 'android',
        'iphone': 'iphone'
    }

    def __create_selenium_driver(self, browser, desired_capabilities=None, remote_url=None,
                      profile_dir=None, options=None, service_log_path=None):
        browser = self.__normalise_browser_name(browser)
        creation_method = self.__get_creator_method(browser)
        if (creation_method == self.__create_firefox
                or creation_method == self.__create_headless_firefox):
            return creation_method(desired_capabilities, remote_url, profile_dir,
                                   options=options, service_log_path=service_log_path)
        return creation_method(desired_capabilities, remote_url, options=options,
                               service_log_path=service_log_path)

    def __normalise_browser_name(self, browser):
        return browser.lower().replace(' ', '')

    def __get_creator_method(self, browser):
        if browser in self.__browser_names:
            return getattr(self, '_DriverService__create_{}'.format(self.__browser_names[browser]))
        raise ValueError('{} is not a supported browser.'.format(browser))
    
    def __remote_capabilities_resolver(self, set_capabilities, default_capabilities):
        if not set_capabilities:
            return {'desired_capabilities': default_capabilities}
        if 'capabilities' in set_capabilities:
            caps = set_capabilities['capabilities']
        else:
            caps = set_capabilities['desired_capabilities']
        if 'browserName' not in caps:
            caps['browserName'] = default_capabilities['browserName']
        return {'desired_capabilities': caps}

    def __create_chrome(self, desired_capabilities, remote_url, options=None, service_log_path=None):
        if not options:
            options = seleniumWebDriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        experimentalFlags = ['native-file-system-api@1']
        chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
        options.add_experimental_option('localState',chromeLocalStatePrefs)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-notifications")
        options.set_capability('unhandledPromptBehavior', 'accept')  
        if (remote_url):
            defaul_caps = seleniumWebDriver.DesiredCapabilities.CHROME.copy()
            desired_capabilities = self.__remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self.__remote(desired_capabilities, remote_url, options=options)

        return seleniumWebDriver.Chrome(executable_path=ChromeDriverManager().install(),options=options)

    def __create_headless_chrome(self, desired_capabilities, remote_url, options=None, service_log_path=None):
        if not options:
            options = seleniumWebDriver.ChromeOptions()
        options.headless = True
        return self.__create_chrome(desired_capabilities, remote_url, options, service_log_path)

    def __create_firefox(self, desired_capabilities, remote_url, ff_profile_dir, options=None, service_log_path=None):
        profile = self.__get_ff_profile(ff_profile_dir)
        if (remote_url):
            default_caps = seleniumWebDriver.DesiredCapabilities.FIREFOX.copy()
            desired_capabilities = self.__remote_capabilities_resolver(desired_capabilities, default_caps)
            return self.__remote(desired_capabilities, remote_url,
                                profile, options)
    
        return seleniumWebDriver.Firefox(executable_path=GeckoDriverManager().install(),options=options, firefox_profile=profile)

    def __get_ff_profile(self, ff_profile_dir):
        if isinstance(ff_profile_dir,seleniumWebDriver.FirefoxProfile):
            return ff_profile_dir
        if not (ff_profile_dir):
            return seleniumWebDriver.FirefoxProfile()
        try:
            return seleniumWebDriver.FirefoxProfile(ff_profile_dir)
        except (OSError, FileNotFoundError):
            ff_options = self.selenium_options._parse(ff_profile_dir)
            ff_profile = seleniumWebDriver.FirefoxProfile()
            for option in ff_options:
                for key in option:
                    attr = getattr(ff_profile, key)
                    if callable(attr):
                        attr(*option[key])
                    else:
                        setattr(ff_profile, key, *option[key])
            return ff_profile
            
    def __create_headless_firefox(self, desired_capabilities, remote_url,
                                ff_profile_dir, options=None, service_log_path=None):
        if not options:
            options = seleniumWebDriver.FirefoxOptions()
        options.headless = True
        return self.__create_firefox(desired_capabilities, remote_url, ff_profile_dir, options, service_log_path)

    def __create_ie(self, desired_capabilities, remote_url, options=None, service_log_path=None):
        if not options : seleniumWebDriver.IeOptions()
        if (remote_url):
            defaul_caps = seleniumWebDriver.DesiredCapabilities.INTERNETEXPLORER.copy()
            desired_capabilities = self.__remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self.__remote(desired_capabilities, remote_url, options=options)

        return seleniumWebDriver.Ie(executable_path=IEDriverManager().install(),options=options)

    def __remote(self, desired_capabilities, remote_url,
                profile_dir=None, options=None):
        remote_url = str(remote_url)
        file_detector = None
        return seleniumWebDriver.Remote(command_executor=remote_url,
                                browser_profile=profile_dir, options=options,
                                file_detector=file_detector,
                                **desired_capabilities)
