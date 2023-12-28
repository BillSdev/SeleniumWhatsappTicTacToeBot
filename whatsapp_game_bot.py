import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from whatsapp_page import WhatsappPage

from tic_tac_toe_engine import TicTacToeGame

class WhatappGameBot:

    def __init__(self):
        self._init_web_driver()

    def _init_web_driver(self):
        chromedriver = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\chromedriver.exe"
        option = webdriver.ChromeOptions()
        option.add_argument("--user-data-dir=C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\my-chrome-selenium-data11") #C:\Program Files\BraveSoftware\Brave-Browser\Application\my-chrome-selenium-data

        # Adding argument to disable the AutomationControlled flag 
        option.add_argument("--disable-blink-features=AutomationControlled") 
 
        # Exclude the collection of enable-automation switches 
        option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
        # Turn-off userAutomationExtension 
        option.add_experimental_option("useAutomationExtension", False) 

        option.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
        s = Service(chromedriver)
        self.driver = webdriver.Chrome(service=s, options=option)

        # Changing the property of the navigator value for webdriver to undefined 
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print(self.driver.execute_script("return navigator.userAgent;")) 

    # Only israel phone numbers for now, later can use phonenumbers module
    def _is_valid_number(self, phone_str):
        if len(phone_str) != 13:
            return False
        if phone_str[0:4] != "+972":
            return False
        if not phone_str[4:].isdigit():
            return False
        return True

    def start(self):
        whatsapp_page = WhatsappPage(self.driver)
        whatsapp_page.load_main_whatsapp_page()
        time.sleep(3)
        player_number = input("Enter player's phone number ( e.g. : +972541234567 ) :")
        while not self._is_valid_number(player_number):
            player_number = input("Invalid number format, try again :")

        whatsapp_page.start_chat_with(player_number)
        time.sleep(1)

        game = TicTacToeGame()
        resp = game.start()

        print("Bot says : \n{}\n".format(resp))
        #whatsapp_page.send_msg("@@@" + resp)
        whatsapp_page.send_msg(resp)

        while not game.get_should_quit():
            [ret, client_resp] = whatsapp_page.recv_resp()
            assert ret, "Error occured {}".format(client_resp)
            print("Player says : \n{}\n".format(client_resp))

            resp = game.handle_cmd_recv_resp(client_resp)
            print("Bot says : \n{}\n".format(resp))
            #whatsapp_page.send_msg("@@@" + resp)
            whatsapp_page.send_msg(resp)
            
    ######################################################
    #
    #def manual_clear(self, elem):
    #    elem.send_keys(Keys.CONTROL + "a")
    #    time.sleep(0.3)
    #    elem.send_keys(Keys.DELETE)
    #    time.sleep(0.3)
    #
    #
    #def test_send_message(self):
    #    elem = self.driver.find_element(By.XPATH, "//div[@id='main']//div[@role='textbox']")
    #    elem.clear()
    #    elem.send_keys("TEST_SEND")
    #    time.sleep(0.5)
    #    elem.clear()
    #    elem.send_keys("v2TEST_SENDv2")
    #    time.sleep(1)
    #    elem.send_keys(Keys.BACKSPACE)
    #    print(f"len = {len(elem.text)}")
    #    print(f"text = {elem.text}")
    #    #elem.send_keys(Keys.RETURN) WORKS
    #    self.manual_clear(elem)
    #    time.sleep(3)
    #    
    #
    #def test_msg_object(self, elem_row):
    #    from elements.message_elem import WhatsappChatMessage
    #    msg = WhatsappChatMessage(self.driver, elem_row)
    #    is_valid = msg.is_valid_msg()
    #    print("--------------")
    #    print("--------------")
    #    print("is valid = {}".format(is_valid))
    #    if not is_valid:
    #        return
    #    msg_id = msg.get_msg_id()
    #    msg_text = msg.get_msg_text()
    #    print("msg_id = {}".format(msg_id))
    #    print("msg_text = {}".format(msg_text))
    #
    #    next_valid_msg = msg.get_next_valid_msg()
    #    next_valid_elem = msg._get_next_raw_msg_elem()
    #
    #    print("next_valid_msg = {}".format(next_valid_msg.get_msg_text() if next_valid_msg else None))
    #    print("next_valid_elem = {}".format(next_valid_elem))
    #
    #    print("--------------")
    #    print("--------------")
    #
    #
    # test getting to message containers and iterating and printing messages
    #def temp_func(self):
    #    #elem = self.driver.find_element(By.XPATH, "//div[@data-testid=\"conversation-panel-messages\"]//div[@role=\"application\"]")
    #    elem = self.driver.find_element(By.XPATH, "//div[@role=\"application\"]")
    #    elem_row = None
    #    i = 1
    #    while True:
    #        try:
    #            elem_row = elem.find_element(By.XPATH, f"./div[{i}]")
    #        except:
    #            break
    #
    #        role_attr = elem_row.get_attribute("role")
    #        class_attr = elem_row.get_attribute("class")
    #        print("role={}, class={}".format(role_attr, class_attr))
    #        
    #
    #        if role_attr and "row" in elem_row.get_attribute("role"):
    #            break
    #
    #        i = i+1
    #    
    #    print(elem_row.get_attribute("role"))
    #    elem_row = elem_row.find_element(By.XPATH, "./following-sibling::*[1]")
    #    print("class = {}".format(elem_row.get_attribute("class")))
    #
    #    # attempting to reach the end with following-sibling : 
    #    while True and elem_row != None:
    #        print("@@@")
    #        try:
    #            elem_row = elem_row.find_element(By.XPATH, "./following-sibling::*[1]")
    #
    #            role_attr = elem_row.get_attribute("role")
    #            class_attr = elem_row.get_attribute("class")                
    #
    #            if role_attr != None:
    #                print(f"!!! role = {role_attr}")
    #                self.test_msg_object(elem_row)
    #                
    #
    #            if class_attr != None:
    #                print(f"!!! class = {class_attr}")
    #        except Exception  as err:
    #            print(f"Done loop, exception : {err}")
    #            elem_row = None
    #
    ######################################################

      

def game_engine_testing():
    game = TicTacToeGame()
    resp = game.start()
    print(resp)

    while not game.get_should_quit():
        inp = input(">>>")
        resp = game.handle_cmd_recv_resp(inp)
        print(resp)
    
    exit()

def main():
    #game_engine_testing()
    whatsapp_game_bot = WhatappGameBot()
    whatsapp_game_bot.start()


if __name__ == "__main__":
    main()