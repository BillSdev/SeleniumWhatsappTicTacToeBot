from selenium.webdriver.common.by import By

class XPathLocs:
    FIRST_CHILD = "./*[1]"
    LAST_CHILD = "./*[last()]"
    NEXT_SIBLING = "./following-sibling::*[1]"
    PREV_SIBLING = "./preceding-sibling::*[1]"

    @staticmethod
    def NTH_CHILD(n):
        assert isinstance(n, int) and n > 0, f"Invalid child num : {n}"
        return f"./*[{n}]"

    @staticmethod
    def NTH_NEXT_SIBLING(n):
        assert isinstance(n, int) and n > 0, f"Invalid sibling num : {n}"
        return f"./following-sibling::*[{n}]"

class WhatsappChatLocators:
    #MESSAGES_CONTAINER = "//div[@data-testid=\"conversation-panel-messages\"]//div[@role=\"application\"]"
    MESSAGES_CONTAINER = "//div[@role=\"application\"]"
    SELECTABLE_COPYABLE_MSG = ".//span[contains(@class, 'selectable-text copyable-text')]"
    #MSG_TEXT_SPAN = SELECTABLE_COPYABLE_MSG + XPathLocs.FIRST_CHILD
    MSG_TEXT_SPAN = SELECTABLE_COPYABLE_MSG + "/*[1]" # TODO: above is bad, need without '.' prefix here, or leave it like this or change FIRST_CHILD to be without '.'
    CHAT_TEXT_FIELD = "//div[@id='main']//div[@role='textbox']"
