from elements.locators import WhatsappChatLocators, XPathLocs
from elements.message_elem import WhatsappChatMessage
from utility import find_element_or_none, find_element_or_none_wait

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class WhatsappMessagesContainer:

    def __init__(self, driver):
        self._driver = driver
        self._container_element = WebDriverWait(self._driver, 5).until(
                                      lambda driver: driver.find_element(By.XPATH, WhatsappChatLocators.MESSAGES_CONTAINER))
        
        print("[mydebug] loaded message container : {}".format(self._container_element.get_dom_attribute("class")))

        
    def get_first_child_elem(self, should_wait=True):
        if should_wait:
            return find_element_or_none_wait(self._driver, self._container_element, By.XPATH, XPathLocs.FIRST_CHILD, 3, 0.4)
        
        return find_element_or_none(self._container_element, By.XPATH, XPathLocs.FIRST_CHILD)


    def get_last_child_elem(self, should_wait=True):
        if should_wait:
            return find_element_or_none_wait(self._driver, self._container_element, By.XPATH, XPathLocs.LAST_CHILD, 3, 0.4)
        
        return find_element_or_none(self._container_element, By.XPATH, XPathLocs.LAST_CHILD)
        

