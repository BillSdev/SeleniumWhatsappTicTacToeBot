
import sys
#sys.path.append("./")

from selenium.webdriver.common.by import By
from elements.locators import XPathLocs, WhatsappChatLocators
from utility import find_element_or_none, find_element_or_none_wait


# This class receives the raw message element from the messages container and processes it.
# the given elem might not even be a message, in this case is_valid_msg() = False ( e.g. could be a date info like "Yesterday"... )
# In this class we assume that if the raw_msg_elem was loaded, then all its other relevant sub-elements were also loaded
class WhatsappChatMessage:
    
    def __init__(self, driver, raw_msg_elem):
        self._driver = driver
        self._raw_msg_elem = raw_msg_elem
        self._is_valid_msg = None
        self._is_my_msg = None
        self._msg_text = None
        self._msg_id = None

    # Basically if message has copiable and selectable text ( e.g. stickers \ no-comment photos do not have )
    def is_valid_msg(self):
        if self._is_valid_msg is not None:
            return self._is_valid_msg


        role_attr = self._raw_msg_elem.get_attribute("role")
        if role_attr == None or "row" not in role_attr:
            self._is_valid_msg = False

        else:
            selectable_copyable_elem = find_element_or_none(self._raw_msg_elem,
                                                            By.XPATH,
                                                            WhatsappChatLocators.SELECTABLE_COPYABLE_MSG)

            self._is_valid_msg = selectable_copyable_elem is not None

        return self._is_valid_msg


    def is_my_msg(self):
        if not self.is_valid_msg():
            return None

        # lazy info load, assumes element is const
        if self._is_my_msg != None:
            return self._is_my_msg

        msg_id = self.get_msg_id()
        self._is_my_msg = msg_id is not None    and \
                          len(msg_id) >= 4      and \
                          "true" == msg_id[0:4]

        return self._is_my_msg 
        #return "@@@" in self.get_msg_text()


    def get_msg_text(self):
        if not self.is_valid_msg():
            return None

        # lazy info load, assumes element is const
        if self._msg_text != None:
            return self._msg_text
            
        self._msg_text = self._raw_msg_elem.find_element(By.XPATH, WhatsappChatLocators.MSG_TEXT_SPAN).text

        return self._msg_text


    def get_msg_id(self):
        if not self.is_valid_msg():
            return None
        
        if self._msg_id is not None:
            return self._msg_id

        self._msg_id = self._raw_msg_elem.find_element(By.XPATH, XPathLocs.FIRST_CHILD).get_attribute("data-id")

        return self._msg_id

    def _get_next_raw_msg_elem(self, should_wait=False):
        if should_wait:
            return find_element_or_none_wait(self._driver, self._raw_msg_elem, By.XPATH, XPathLocs.NEXT_SIBLING, 1, 0.2)
        
        return find_element_or_none(self._raw_msg_elem, By.XPATH, XPathLocs.NEXT_SIBLING)

    def get_next_valid_msg(self, should_wait=False):
        curr_msg_elem = self._get_next_raw_msg_elem(should_wait)
        curr_msg = WhatsappChatMessage(self._driver, curr_msg_elem) if curr_msg_elem else None

        # stop when ran out of siblings or found a valid msg
        while curr_msg is not None and not curr_msg.is_valid_msg():
            curr_msg_elem = curr_msg._get_next_raw_msg_elem(should_wait)
            curr_msg = WhatsappChatMessage(self._driver, curr_msg_elem) if curr_msg_elem else None

        # if no siblings -> no next valid msg
        return curr_msg
        

    def __eq__(self, obj):
        return isinstance(obj, WhatsappChatMessage) and \
               self.get_msg_id() == obj.get_msg_id()