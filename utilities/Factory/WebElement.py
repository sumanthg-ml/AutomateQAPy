#from elementService import ElementService
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import time
        
# def _locatorSwitcher(searchBy):
#     switcher ={
#         "id":lambda:webdriver.Remote.find_element_by_id,
#         "class_name":lambda:webdriver.Remote.find_elements_by_class_name,
#     }
#     return switcher.get(searchBy,lambda: "expression")()

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
    """Base class with all Common actions. 

    .. note::
        Use only when not sure about the control type. Otherwise use custom classes

    :param locators: Key-Value pair of identifier used to locate the element. Available locators- id,class_name,css_selector,name,tag_name,link_text,partial_link_text,xpath
    :type locators: kwargs

    """
    def __init__(self, **kwargs):   
        self._currentElement:WebElement = None     
        self.criteria = kwargs 
   
    def __get__(self, obj, owner):
        self.testCache:TestCache = obj.testCache
        return self
   
    # def __set__(self, obj, value): 
    #     raise Exception('Cannot set value')    
    
    def _searchElement(self,parentElement=None,timeoutInSeconds=5):
        try:
            self._webdriver = self.testCache.driver_service.driver
            if not parentElement:
                parentElement = self._webdriver            
            # if self._currentElement is None:
            if self.criteria.__len__() == 1:
                locator,val = list(self.criteria.items())[0]
                if locator == "current_element" and isinstance(val,WebElement):
                    self._currentElement = val
                else:
                    # self._currentElement = parentElement.find_element(by=_locatorSwitcher(locator),value=val)      
                    wait = WebDriverWait(self._webdriver, timeoutInSeconds)
                    self._currentElement = wait.until(ec.presence_of_element_located((_locatorSwitcher(locator),val)))
                  
        except:
            self.testCache.logger_service.logger.exception("SearchFailure:")
            
    # def FindElement(self,**searchCriteria):  
    #     self._searchElement()   
    #     el = self._currentElement.find_element()
    #     return el
    
    def FindElement(self,elementType,**searchCriteria):
        """Returns a child element as a Wrapped element based on Element type.

        :param elementType: Type of element to be returned
        :type elementType: Type of WebElement
        :param locators: Key-Value pair of identifier used to locate the element. Available locators- id,class_name,css_selector,name,tag_name,link_text,partial_link_text,xpath
        :type locators: kwargs
        :returns: Returns element of the type specified
        """
        el = None
        self._searchElement()
        try:           
            locator,val = list(searchCriteria.items())[0]
            cell:WebElement = self._currentElement.find_element(by=_locatorSwitcher(locator),value=val)
            el = elementType(current_element=cell)
            el.testCache = self.testCache
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-FindElement:")        
        return el

    def FindElements(self,elementType,**searchCriteria):
        """Returns a list of child elements as a Wrapped element based on Element type.

        :param elementType: Type of element to be returned
        :type elementType: Type of WebElement
        :param locators: Key-Value pair of identifier used to locate the element. Available locators- id,class_name,css_selector,name,tag_name,link_text,partial_link_text,xpath
        :type locators: kwargs
        :returns: Returns list of elements of the type specified
        """
        els = None
        self._searchElement()
        try:           
            locator,val = list(searchCriteria.items())[0]
            elements:list(WebElement) = self._currentElement.find_elements(by=_locatorSwitcher(locator),value=val)
            els = [elementType(current_element=element) for element in elements] 
            for el in els:
                el.testCache = self.testCache
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-FindElements:")        
        return els


    def SetFocus(self):
        """Set focus on the specified element.   

        """
        self._searchElement()
        try:
            self._webdriver.execute_script("arguments[0].focus();", self._currentElement)
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
                self._webdriver.execute_script("arguments[0].click();", self._currentElement)            
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-Click:")

    def ClickElementAtCoordinates(self, xoffset, yoffset):
        """Click the element at ``xoffset/yoffset``.
        The Cursor is moved from the center of the element and x/y coordinates are
        calculated from that point.

        :param xoffset: Distance on the x coordinate
        :type xoffset: int
        :param yoffset: Distance on the y coordinate
        :type yoffset: int

        """
        # self.info("Clicking element '%s' at coordinates x=%s, y=%s."
        #           % (locator, xoffset, yoffset))
        self._searchElement()        
        try:
            action = ActionChains(self._webdriver)        
            action.move_to_element(self._currentElement)        
            action.move_by_offset(xoffset, yoffset)
            action.click()
            action.perform()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-ClickElementAtCoordinates:")

    def DoubleClick(self):
        """Double Click on the specified element.   

        """       
        self._searchElement()        
        try:
            action = ActionChains(self._webdriver)        
            action.double_click(self._currentElement).perform()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-DoubleClick:")

    def IsEnabled(self):
        """Check if the specified element is enabled.   

        :rtype: boolean
        """
        self._searchElement()
        found = False
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
        found = False
        try:
            found = self._currentElement.is_displayed()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsVisible:")
        return found

    def ScrollIntoView(self):
        """Scroll the specified element into viewable area on the screen.   

        """
        self._searchElement()
        try:
            ActionChains(self._webdriver).move_to_element(self._currentElement).perform()           
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-ScrollIntoView:")

    def WaitForExists(self,timeoutInSeconds=30):
        """Wait for the specified element to be visible on the screen.   

        """
        try:
            self._searchElement(timeoutInSeconds)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-WaitForExists:")

    def WaitForVisible(self,timeoutInSeconds=30):
        """Wait for the specified element to be visible on the screen.   

        """
        self._searchElement()
        wait = WebDriverWait(self._webdriver, timeoutInSeconds)
        try:
            wait.until(ec.visibility_of(self._currentElement))
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-WaitForVisible:")

    def WaitForInVisible(self,timeoutInSeconds=30):
        """Wait for the specified element to be visible on the screen.   

        """
        self._searchElement()
        wait = WebDriverWait(self._webdriver, timeoutInSeconds)
        try:
            wait.until(ec.invisibility_of_element(self._currentElement))
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-WaitForInVisible:")


class TextBox(BaseElement):    
    """Custom class to define a Web TextBox. It subclasses :class:`BaseElement`.

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
            self._currentElement.send_keys(text)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-EnterText:")

    def ClearText(self):    
        """Clear all the text in the specified element.  

        """      
        self._searchElement()        
        try:            
            self._currentElement.clear()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-ClearText:")

    def GetText(self):
        """Fetch the text from the specified element.   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.text
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetText:")
        return text

    def GetValue(self):
        """Fetch the value attribute from the specified element.(For cases where GetText doesn't work)   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.get_attribute("value")
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetValue:")
        return text

    def GetColorValue(self):
        from selenium.webdriver.support.color import Color
        import webcolors
        """Fetch the value attribute from the specified element.(For cases where GetText doesn't work)   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.value_of_css_property("color")
            hexform = Color.from_string(text).hex
            if hexform=="#303f9f":
                colname = 'blue'
            else:
                colname = webcolors.hex_to_name(hexform,spec='css3')
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetCSSValue:")
        return colname



class Button(BaseElement):   
    """Custom class to define a Web Button. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.
        
    """     
    pass
    

class RadioButton(BaseElement): 
    """Custom class to define a Web RadioButton. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.
        
    """      
    pass


class CheckBox(BaseElement):
    """Custom class to define a Web CheckBox. It subclasses :class:`BaseElement`.

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
            found = self._currentElement.is_selected()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsSelected:")
        return found

    def Check(self):
        """Check the specified checkbox if it is not already checked.  

        """
        self._searchElement()
        try:
            if not self._currentElement.is_selected(): self._currentElement.click()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-Check:")

    def UnCheck(self):
        """Un-Check the specified checkbox if it is already checked.  

        """ 
        self._searchElement()
        try:
            if self._currentElement.is_selected(): self._currentElement.click()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-UnCheck:")
    

class MatSlideToggle(BaseElement):
    """Custom class to define a Web MatSlideToggle. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.
        
    """

    def IsSelected(self):
        """Check if the specified Toggle is selected.   

        :rtype: boolean
        """
        self._searchElement()
        found = False
        try:
            class_name = self._currentElement.get_attribute("class")            
            if "mat-checked" in class_name: found = True
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsSelected:")
        return found
    
    def Toggle(self,toggleon=True):
        """Check the specified Toggle if it is not already checked.  

        """
        self._searchElement()
        try:
            if toggleon:
                if not self.IsSelected(): self.Click()
            else:
                if self.IsSelected(): self.Click()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-Toggle:")         

    def GetColorValue(self):
        from selenium.webdriver.support.color import Color
        import webcolors
        """Fetch the value attribute from the specified element.(For cases where GetText doesn't work)   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.value_of_css_property("background-color")
            hexform = Color.from_string(text).hex
            if hexform == "#303f9f":
                colname = 'blue'
            else:
                colname = webcolors.hex_to_name(hexform,spec='css3')
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetCSSValue:")
        return colname

class ComboBox(BaseElement): 
    """Custom class to define a Web ComboBox. It subclasses :class:`BaseElement`.

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
            self._currentElement.send_keys(text)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-EnterText:")

    def SelectByIndex(self,index:int):  
        """Select an item from the ComboBox using index.   

        :param index: index of the item to be selected
        :type index: int
        """         
        self._searchElement()        
        try:      
            Select(self._currentElement).select_by_index(index)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByIndex:")

    def SelectByText(self,text:str):  
        """Select an item from the ComboBox using visible text.   

        :param text: text of the item to be selected
        :type text: str
        """        
        self._searchElement()        
        try:            
            Select(self._currentElement).select_by_visible_text(text)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByText:")

    def SelectByValue(self,text:str):     
        """Select an item from the ComboBox using value attribute.   

        :param text: text of the item to be selected
        :type text: str
        """     
        self._searchElement()        
        try:            
            Select(self._currentElement).select_by_value(text)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByValue:")

    def SelectByNgText(self,text:str):  
        """Select an item from the ComboBox using visible text based on ng select model.   

        :param text: text of the item to be selected
        :type text: str
        """        
        self._searchElement()        
        try:  
            self._currentElement.click()
            xpath = "//ng-dropdown-panel//*[text()='" +text+ "']"
            el = self._webdriver.find_element_by_xpath(xpath)
            el.click()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SelectByNgText:")

    def GetSelectedText(self):
        """Fetch the text of the selected item from the ComboBox.   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = Select(self._currentElement).first_selected_option().text()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetSelectedText:")
        return text

    def GetText(self):
        """Fetch the text from the specified element.

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.text
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetText:")
        return text

    def GetValue(self):
        """Fetch the value attribute from the specified element.(For cases where GetText doesn't work)

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.get_attribute("value")
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetValue:")
        return text

    def GetAllOptions(self):
        """Fetch the text of the all items from the ComboBox.   

        :rtype: list of str
        """
        self._searchElement()
        text = list()
        try:
            options = Select(self._currentElement).options
            text = [opt.text() for opt in options]
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetAllOptions:")
        return text


class Table(BaseElement):    
    """Custom class to define a Web Table. It subclasses :class:`BaseElement`.

    .. note::
        Check base class for params and usage.
        
    """ 

    def GetTableCellElement(self, row, column,elementType:BaseElement):
        """Returns a table cell as a Wrapped element based on Element type.
        The cell is found using ``row index`` and ``column index`` or ``row index`` and ``column header``. 
        Both row and column indexes start from 1, and header and footer
        rows are not included in the count.  

        :param row: Index of the required row    
        :type row: int
        :param column: Index or Header of the required column
        :type column: int or str
        :param elementType: Type of element to be returned
        :type elementType: Type of WebElement
        :returns: Returns element of the type specified
        """
        el:BaseElement = None
        self._searchElement()
        try:            
            row = int(row)
            if isinstance(column,str): column = self.GetColumnByHeader(column)
            column = int(column)
            if row == 0 or column == 0:
                raise ValueError('Both row and column must be non-zero, '
                                'got row %d and column %d.' % (row, column))        
            cell:WebElement = self._get_cell(row, column)
            el = elementType(current_element=cell)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetTableCellElement:")        
        return el
      
    def GetTableCellText(self, row, column):
        """Returns contents of a table cell.
        The cell is found using ``row`` and ``column``. 
        Both row and column indexes start from 1, and header and footer
        rows are not included in the count.  

        :param row: Index of the required row    
        :type row: int
        :param column: Index or Header of the required column
        :type column: int or str       
        :rtype: str    
        """
        text:str = None
        self._searchElement()
        try:            
            row = int(row)
            if isinstance(column,str): column = self.GetColumnByHeader(column)
            column = int(column)
            if row == 0 or column == 0:
                raise ValueError('Both row and column must be non-zero, '
                                'got row %d and column %d.' % (row, column))        
            cell = self._get_cell(row, column)
            text = cell.text
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetTableCellText:")   
        
        return text

    # def GetTableCellIndex(self,cellValue):
    #     """Returns row and column index for the corresponding cell value in the table.
    #     Used for searching a value in the table        
    #     """
    #     text:int = None              
    #     rows = self._get_rows()
    #     for row in rows:
    #         pass
    #     cells = rows[0].find_elements_by_xpath('./th|./td')
    #     headers = [cell.text for cell in cells]
    #     index = headers.index(columnHeader) #raised error
    #     text = len(cells)
    #     return text

    def GetRowCount(self):
        """Returns number of a rows in the table. 

        :rtype: int           
        """
        text:int = None   
        self._searchElement()
        try:            
            rows = self._get_rows()
            text = len(rows)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetRowCount:")  
        return text

    def GetColumnCount(self):
        """Returns number of a columns in the table. 

        :rtype: int           
        """
        text:int = None 
        self._searchElement() 
        try:            
            rows = self._get_rows()
            cells = rows[0].find_elements_by_xpath('./th|./td|./mat-cell')
            text = len(cells)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetColumnCount:") 
        return text

    def GetColumnByHeader(self,columnHeader):
        """Returns column number based on the table header.  

        :rtype: int          
        """
        index:int = None      
        self._searchElement()
        try:            
            rows = self._get_headers()
            cells = rows[0].find_elements_by_xpath('./th|./td|./mat-header-cell')
            headers = [cell.text for cell in cells]
            index = headers.index(columnHeader) #raised error
            if index:index+1
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetColumnByHeader:") 
        return index

    def GetVisibleTableData(self,getTextByValue=False):
        """Scrap the complete visible table data.  

        :rtype: list          
        """
        fulltable = list()      
        self._searchElement()
        try:            
            headerrows = self._get_headers()
            headercells = headerrows[0].find_elements_by_xpath('./th|./td|./mat-header-cell')
            headers = [cell.text for cell in headercells]
            
            rows = self._get_rows()
           
            for row in rows:                
                cells = row.find_elements_by_xpath('./th|./td|./mat-cell//input')
                if getTextByValue: 
                    cellsText = [cell.get_attribute("value") for cell in cells]
                else:
                    cellsText = [cell.text for cell in cells]
                fulltable.append(dict(zip(headers,cellsText)))            

        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetVisibleTableData:") 
        return fulltable
           
    def _get_cell(self, row, column):
        rows = self._get_rows()
        if len(rows) < abs(row):
            raise AssertionError("Table should have had at least %d "
                                 "rows but had only %d."
                                 % (abs(row), len(rows)))
        index = row - 1 if row > 0 else row
        cells = rows[index].find_elements_by_xpath('./th|./td|./mat-cell')
        if len(cells) < abs(column):
            raise AssertionError("Table row %d should have had at "
                                 "least %d columns but had only %d."
                                 % (row, abs(column), len(cells)))
        index = column - 1 if column > 0 else column
        return cells[index]

    def _get_rows(self):
        # Get rows in same order as browsers render them.
        table = self._currentElement
        rows = table.find_elements_by_xpath("./tbody/tr|./mat-row")       
        return rows

    def _get_headers(self):
        # Get rows in same order as browsers render them.
        table = self._currentElement
        rows = table.find_elements_by_xpath("./thead/tr|./mat-header-row")       
        return rows

    def _get_footers(self):
        # Get rows in same order as browsers render them.
        table = self._currentElement
        rows = table.find_elements_by_xpath("./tfoot/tr|./mat-footer-row")       
        return rows
    