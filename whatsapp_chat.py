from elements.locators import WhatsappChatLocators, XPathLocs
from elements.message_elem import WhatsappChatMessage
from elements.messages_container_elem import WhatsappMessagesContainer
from elements.chat_text_field_elem import TextSender

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class WhatsappChat:

    def __init__(self, driver):
        self._driver = driver
        self._my_last_msg = None
        self._messages_container = WhatsappMessagesContainer(self._driver)
        self._text_sender = TextSender(self._driver)
    
    def send_msg(self, msg):
        self._text_sender.send_message(msg)
        self._update_my_last_msg(expect_new=True)
    
    def has_response(self):
        has_resp =  self._my_last_msg is not None and \
                    self._my_last_msg.get_next_valid_msg() is not None
        
        assert not ( has_resp and self._my_last_msg.get_next_valid_msg().is_my_msg() ), "Next message after Bot's last cannot be Bot's message"

        return has_resp

    # We only look at the FIRST response to the bot's last message
    # If response exists, return it, else return None
    def read_reponse(self):
        assert self._my_last_msg is not None, "Can't ask for response when bot has not yet sent any requests."
        
        if not self.has_response():
            return None
        
        return self._my_last_msg.get_next_valid_msg().get_msg_text()

        
    def _get_first_valid_msg(self):
        first_raw_msg_elem = self._messages_container.get_first_child_elem(should_wait=True)
        print("[mydebug] first_raw_msg_elem = {}".format(first_raw_msg_elem))

        # container completely empty
        if first_raw_msg_elem is None:
            return None
        
        curr_msg = WhatsappChatMessage(self._driver, first_raw_msg_elem)
        if not curr_msg.is_valid_msg():
            print("Not valid first message get next valid message : class = {}".format(first_raw_msg_elem.get_dom_attribute("class")))
            # if no valid messages, will return None
            curr_msg = curr_msg.get_next_valid_msg(should_wait=True)

        return curr_msg

    def _update_my_last_msg(self, expect_new=True):
        curr_msg = self._my_last_msg
        
        if curr_msg is None:
            curr_msg = self._get_first_valid_msg()
        
        if curr_msg is None:
            assert not expect_new, "Expected new messages"
            return

        # Note : Still problematic, after reaching the end, we might still need to wait for our message to appear,
        #        but then a new client message might appear instead and "swallow" the single wait and we will miss the message
        #        It's probably an extremely rare and unlikely case so what ever
        #        To PROPERLY fix, gotta change the get_next_valid_msg to get_my_next_valid_msg which doesnt exist because
        #        I need to add a locator similar to the sibling row one + look for my number string in the id or some other way, basically :
        #        TODO : add above locator using sibling + is_my_msg locator xPath
        curr_my_last_msg = curr_msg
        should_quit = False
        while curr_msg is not None and not should_quit:
            temp_msg = curr_msg.get_next_valid_msg()
            if temp_msg is None and curr_my_last_msg == self._my_last_msg:
                temp_msg = curr_msg.get_next_valid_msg(should_wait=True)
                should_quit = True

            curr_msg = temp_msg

            if curr_msg is not None and curr_msg.is_my_msg():
                curr_my_last_msg = curr_msg
        
        if expect_new:
            assert not curr_my_last_msg == self._my_last_msg, "Expected to see a new bots message, old = {}, new={}".format(self._my_last_msg.get_msg_text(), curr_my_last_msg.get_msg_text())

        self._my_last_msg = curr_my_last_msg
