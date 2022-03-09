#from elementService import ElementService
import pywinauto
from pywinauto import application
from pywinauto.application import WindowSpecification
import time
from utilities.testCache import TestCache
        

class BaseElement(object):    
    """Base class with all Common actions. 

    .. note::
        Use only when not sure about the control type. Otherwise use custom classes

    :param locators: Key-Value pair of all identifiers used to locate the element
    :type locators: kwargs

    """
    def __init__(self, **kwargs):   
        self._currentElement:WindowSpecification = None     
        self.criteria = kwargs 
   
    def __get__(self, obj, owner):
        self.testCache:TestCache = obj.testCache
        return self

    def _searchElement(self):
        try:
            __app:application.Application = self.testCache.driver_service.driver
            self._currentElement = __app.top_window().child_window(**self.criteria)
            
        except:
            self.testCache.logger_service.logger.exception("SearchFailure:")

    def FindElement(self,**searchCriteria):  
        self._searchElement()   
        el = self._currentElement.child_window(searchCriteria)
        return el
    
    def SetFocus(self):
        """Set focus on the specified element.   

        """
        self._searchElement()
        try:
            self._currentElement.set_focus()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SetFocus:")

    def Click(self):
        """Click on the specified element.   

        """
        self._searchElement()
        try:
            try:
                self._currentElement.click()
            except:
                self._currentElement.click_input()
            
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-Click:")

    def RightClick(self):
        """Right Click on the specified element.   

        """
        self._searchElement()
        try:
            self._currentElement.right_click_input()
            
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-RightClick:")

    def DoubleClick(self):
        """Click on the specified element.   

        """
        self._searchElement()
        try:
            try:
                self._currentElement.double_click()
            except:
                self._currentElement.double_click_input()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-DoubleClick:")

    def IsEnabled(self):
        """Check if the specified element is enabled.   

        :rtype: boolean
        """
        self._searchElement()
        found = None
        try:
            found = self._currentElement.is_enabled()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsEnabled:")
        return found

    def IsVisible(self):
        """Check if the specified element is visible on the screen.   

        :rtype: boolean
        """
        self._searchElement()
        found = None
        try:
            found = self._currentElement.is_visible()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsVisible:")
        return found

    def SendKeystrokes(self,keycodes):  
        """Send the keystrokes to the specified element.   

        :param text: Keys to be entered
        :type text: str
        """      
        # self._searchElement()        
        try:            
            self._currentElement.type_keys(keycodes)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SendKeystrokes:")

    def WaitForVisible(self,timeoutInSeconds=20):  
        """Wait for the element to be visible for a maximum timeout specified.   

        :param timeoutInSeconds: Maximum time to wait
        :type timeoutInSeconds: int
        """      
        self._searchElement()        
        try:            
            self._currentElement.wait('visible',timeout=timeoutInSeconds)
        except:
            pass

class TextBox(BaseElement):    
    """Custom class to define a Window TextBox. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.

    """
    def EnterText(self,text):  
        """Enter the given text in the specified element.   

        :param text: Text to be entered
        :type text: str
        """      
        self._searchElement()        
        try:            
            self._currentElement.wait('exists ready',timeout=2).type_keys(text,with_spaces=True)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-EnterText:")

    def ClearText(self):
        """Clear all the text in the specified element.  

        """        
        self._searchElement()        
        try:            
            self._currentElement.set_text("")
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-EnterText:")

    def GetText(self):
        """Fetch the text from the specified element.   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.get_value()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-Click:")
        return text



class Button(BaseElement):
    """Custom class to define a Window Button. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.
        
    """    
    pass
    

class RadioButton(BaseElement): 
    """Custom class to define a Window RadioButton. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.
        
    """   
    pass


class CheckBox(BaseElement):
    """Custom class to define a Window CheckBox. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.
        
    """

    def IsSelected(self):
        """Check if the specified checkbox is selected.   

        :rtype: boolean
        """
        self._searchElement()
        found = False
        try:
            found = self._currentElement.is_checked()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsSelected:")
        return found

    def Check(self):
        """Check the specified checkbox if it is not already checked.  

        """ 
        self._searchElement()
        try:
            if not self._currentElement.is_checked(): self._currentElement.check()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-Check:")

    def UnCheck(self):
        """Un-Check the specified checkbox if it is already checked.  

        """ 
        self._searchElement()
        try:
            if self._currentElement.is_checked(): self._currentElement.uncheck()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-UnCheck:")
    

class ComboBox(BaseElement):   
    """Custom class to define a Window ComboBox. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.
        
    """ 

    def EnterText(self,text): 
        """Enter the given text in the specified element.   

        :param text: Text to be entered
        :type text: str
        """         
        self._searchElement()        
        try:            
            self._currentElement.wait('exists ready',timeout=2).type_keys(text,with_spaces=True)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-EnterText:")

    def SelectByIndex(self,index:int):    
        """Select an item from the ComboBox using index.   

        :param index: index of the item to be selected
        :type index: int
        """      
        self._searchElement()        
        try:            
            self._currentElement.select(index)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByIndex:")

    def SelectByText(self,text:str):   
        """Select an item from the ComboBox using text.   

        :param text: text of the item to be selected
        :type text: str
        """     
        self._searchElement()        
        try:            
            self._currentElement.select(text)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByText:")

    def GetSelectedText(self):
        """Fetch the text of the selected item from the ComboBox.   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.selected_text()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetSelectedText:")
        return text
    

class TreeView(BaseElement):   
    """Custom class to define a Window TreeView. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.
        
    """ 

    def SelectByPath(self,path):   
        """Select an item from the TreeView.   

        :param path: a path to the item to return. This can be one of
            the following:
            * A string separated by \\ characters. The first character must
                be \\. This string is split on the \\ characters and each of
                these is used to find the specific child at each level. The
                \\ represents the root item - so you don't need to specify the
                root itself.
            * A list/tuple of strings - The first item should be the root
                element.
            * A list/tuple of integers - The first item the index which root
                to select. Indexing always starts from zero: SelectByPath((0, 2, 3))
        :type text: str or list
        """     
        self._searchElement()        
        try:            
            self._currentElement.get_item(path).select()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByPath:")
