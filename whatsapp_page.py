from datetime import datetime, timedelta
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from whatsapp_chat import WhatsappChat

class WhatsappPage:

    def __init__(self, driver):
        self.driver = driver
        self.chat = None

    # NOTE : when the qr page loads completely, luckily wf-loading does not appear.
    #        but maybe should change it to notice if we are just waiting for the real page to load, or if we are waiting for a qr to be inserted, maybe remove TO in the latter case.
    def load_main_whatsapp_page(self):
        self.driver.get("https://web.whatsapp.com/")

        print("Opening web.whatsapp.com...")
        
        # from what I noticed, the whatsapp web page finished loading properly when the html element received another class tag named wf-loading or wf-loaded or wf-active
        # ( added wf-loaded and wf-active just in case because they also exist and used in general when web page finishes loading, have not seen this happen on the whatsapp web page though )\
        WebDriverWait(self.driver, 60).until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, "html[class*=\"wf-loading\"], html[class*=\"wf-loaded\"], html[class*=\"wf-active\"]"))

        print("Finished loading web.whatsapp.com main page")

    def start_chat_with(self, phone):
        print(f"Opening chat with {phone}")

        javascript_start_chat_script = f"""
            const openChat = phone => {{
            const link = document.createElement(\"a\");
            link.setAttribute(\"href\", \"whatsapp://send?phone=\" + phone);
            document.body.append(link);
            link.click();
            document.body.removeChild(link);
            }}
            
            openChat({phone})
        """

        self.driver.execute_script(javascript_start_chat_script)

        self.chat = WhatsappChat(self.driver)

        print(f"Finished loading chat with {phone}")
        
    def send_msg(self, msg):
        assert self.chat != None, "Cant send message when chat is not initialized"

        self.chat.send_msg(msg)

    # Return a pair : [res, res_data] where:
    # res : True - Completed successfully,   False - Error occured
    # res_data : Message to return to the client
    # TODO : one potential util function : wrapper for predicate with timeout and optional period per checks
    # TODO : allow more than 60 seconds to answer 
    def recv_resp(self):
        sleep_time_sec = 0.5
        timeout_sec = timedelta(seconds=240)

        start_time = datetime.now()
        while not self.chat.has_response():
            time.sleep(sleep_time_sec)
            if datetime.now() - start_time > timeout_sec:
                return [False, "Timed-out, took longer than 240 seconds to answer... Bye Bye"]
        
        response = self.chat.read_reponse()
        assert response is not None, "Should have received a response, it's None"
        return [True, response]

