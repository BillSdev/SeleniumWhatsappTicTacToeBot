import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from elements.locators import WhatsappChatLocators, XPathLocs

class TextSender:

    def __init__(self, driver):
        self._driver = driver
        self._text_field_elem = WebDriverWait(self._driver, 3).until(
                                      lambda driver: driver.find_element(By.XPATH, WhatsappChatLocators.CHAT_TEXT_FIELD))

        
    def clear_text(self):
        self._text_field_elem.send_keys(Keys.CONTROL + "a")
        time.sleep(0.3)
        self._text_field_elem.send_keys(Keys.DELETE)
        time.sleep(0.3)

    def send_message(self, message):
        print("Sending message...")
        assert isinstance(message, str), f"Cannot write non-string message! : {message}"

        self.clear_text()

        for char in message:
            if char == "\n":
                print("New line printing")
                action = ActionChains(self._driver, duration=100) 
                action                                          \
                .key_down(Keys.SHIFT)    \
                .key_down(Keys.RETURN)   \
                .key_up(Keys.RETURN)     \
                .key_up(Keys.SHIFT)      \
                .perform()
            else:
                time_to_sleep = random.randint(30, 60) / 1000
                time.sleep(time_to_sleep)
                self._text_field_elem.send_keys(char)

        self._text_field_elem.send_keys(Keys.RETURN)

