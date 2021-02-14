#from elementService import ElementService
import appium
from appium import webdriver
from appium.webdriver.common.mobileby import By
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.select import Select
import time


def _locatorSwitcher(searchBy):
    switcher ={
        "id":By.ID,
        "class_name":By.CLASS_NAME,
        "css_selector":By.CSS_SELECTOR,
        "name":By.NAME,
        "tag_name":By.TAG_NAME,
        "link_text":By.LINK_TEXT,
        "partial_link_text":By.PARTIAL_LINK_TEXT,
        "xpath":By.XPATH,
    }
    return switcher.get(searchBy,"Locator type not supported")

class BaseElement(object):    
  
    def __init__(self, **kwargs):   
        self._currentElement:WebElement = None     
        self.criteria = kwargs 
   
    def __get__(self, obj, owner):
        self.testCache:TestCache = obj.testCache
        return self
   
    # def __set__(self, obj, value): 
    #     raise Exception('Cannot set value')    
    
    def _searchElement(self,parentElement=None):
        try:
            __webdriver:webdriver.Remote = self.testCache.driver_service.driver
            if not parentElement:
                parentElement = __webdriver
            # object._currentElement = __app.top_window().child_window(**object.criteria)
            if self._currentElement is None:
                if self.criteria.__len__() == 1:
                    locator,val = (self.criteria.items())[0]
                    self._currentElement = parentElement.find_element(by=_locatorSwitcher(locator),value=val)
                    __webdriver.execute_script("arguments[0].scrollIntoView(true);",self._currentElement)            
        except:
            self.testCache.logger_service.logger.exception("SearchFailure:")

    # def FindElement(self,**searchCriteria):  
    #     self._searchElement()   
    #     el = self._currentElement.find_element()
    #     return el
    
    def Click(self):
        self._searchElement()
        try:
            self._currentElement.click()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-Click:")

    def IsEnabled(self):
        self._searchElement()
        found = None
        try:
            found = self._currentElement.is_enabled()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsEnabled:")
        return found

    def IsVisible(self):
        self._searchElement()
        found = None
        try:
            found = self._currentElement.is_displayed()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsVisible:")
        return found



class TextBox(BaseElement):    
  
    def EnterText(self,text):        
        self._searchElement()        
        try:            
            self._currentElement.send_keys(text)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-EnterText:")

    def GetText(self):
        self._searchElement()
        text = None
        try:
            text = self._currentElement.text()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-Click:")
        return text



class Button(BaseElement):    
    pass


class RadioButton(BaseElement):    
    pass
    

class CheckBox(BaseElement):
    pass
    

class ComboBox(BaseElement):    
      
    def SelectByIndex(self,index:int):        
        self._searchElement()        
        try:            
            Select(self._currentElement).select_by_index(index)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByIndex:")

    def SelectByText(self,text:str):        
        self._searchElement()        
        try:            
            Select(self._currentElement).select_by_visible_text(text)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByText:")

    def SelectByValue(self,text:str):        
        self._searchElement()        
        try:            
            Select(self._currentElement).select_by_value(text)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByValue:")

    def GetSelectedText(self):
        self._searchElement()
        text = None
        try:
            text = self._currentElement.selected_text()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetSelectedText:")
        return text
    