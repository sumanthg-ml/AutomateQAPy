from traceback import print_stack
import os
import time

class WindowBasePage(object):
    """Base Page for all Window based pages.
    Contains generic actions that can be directly accessed from inherited Windows Page.
    
    """
    def __init__(self,bootstrap:Bootstrapper):
        self.testCache = bootstrap.testCache
        self.logger = self.testCache.logger_service.logger  
    

    def getData(self,dataName):
        """Fetch test data based on field name.
        Data will be fetched from key-value test data file based on the test case

        :param dataName: Key value used to fetch the data
        :type dataName: str
        :return: Returns a string if Key is present. Returns None otherwise

        """
        data = None
        try:
            data = self.testCache.data_service.get(dataName)
        except:
            self.testCache.logger_service.logger.exception("DataFailure-getData:")        
        return data
    
    def sleep(self,seconds):
        """Used to sleep/wait for the specified time.
       
        :param seconds: Seconds to sleep
        :type seconds: int

        """
        time.sleep(seconds)
    
    def keyPress(self,keyCode): 
        """Used send a key event to the current active window.
       
        :param keyCode: Key code to send to the Window
        :type keyCode: str

        """      
        try:
            self.testCache.driver_service.driver.top_window().type_keys(keyCode)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-keyPress:")        


class WebBasePage(object):
    """Base Page for all Web based pages.
    Contains generic actions that can be directly accessed from inherited Web Page.
    
    """
    def __init__(self,bootstrap:Bootstrapper):
        self.testCache = bootstrap.testCache
        self.logger = self.testCache.logger_service.logger
    

    def getData(self,dataName):
        """Fetch test data based on field name.
        Data will be fetched from key-value test data file based on the test case

        :param dataName: Key value used to fetch the data
        :type dataName: str
        :return: Returns a string if Key is present. Returns None otherwise

        """
        data = None
        try:
            data = self.testCache.data_service.get(dataName)
        except:
            self.testCache.logger_service.logger.exception("DataFailure-getData:")        
        return data
  
    def sleep(self,seconds):
        """Used to sleep/wait for the specified time.
       
        :param seconds: Seconds to sleep
        :type seconds: int

        """
        time.sleep(seconds)

    def navigateToUrl(self,url):
        """Navigate to the specified URL.
       
        :param url: URL to be navigated
        :type url: str

        """
        try:
            self.testCache.driver_service.driver.get(url)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-navigateToUrl:")

    def switchToFrame(self,frameReference):
        """Switch to the specified frame.
       
        :param frameReference: Name of the frame to be switched to
        :type frameReference: str

        """
        try:
            self.testCache.driver_service.driver.switch_to.frame(frameReference)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-switchToFrame:")

    def switchToWindow(self,windowName):
        """Switch to the specified window.
       
        :param windowName: Name of the window to be switched to
        :type windowName: str

        """
        try:
            self.testCache.driver_service.driver.switch_to.window(windowName)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-switchToWindow:")

    def handleAlert(self,accept=True,text=None):
        """Handle alerts produced by the Window.
        Alerts can be accepted or dismissed. Text can be entered incase alert has textbox

        :param accept: (Optional) True to Accept, False to Dismiss. Defaults to True
        :type accept: boolean
        :param text: (Optional) Text to be entered in the alert
        :type text: str

        """
        try:
            if text: self.testCache.driver_service.driver.switch_to.alert.send_keys(text)
            if accept:
                self.testCache.driver_service.driver.switch_to.alert.accept()
            else:
                self.testCache.driver_service.driver.switch_to.alert.dismiss()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-handleAlert:")
        