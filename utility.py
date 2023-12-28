from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# When it's preferable to work with values instead of exceptions + we expect element to be immediately present 
def find_element_or_none(root_elem, locate_by, locator):
    try:
        return root_elem.find_element(locate_by, locator)
    except NoSuchElementException:
        return None


#POLL_FREQUENCY = 0.5 # based on selenium default val

# When it's preferable to work with values instead of exceptions + element might take a bit to appear
# Those functions should not be used in crucial places where we except and require certain elements.
# ( e.g. messages container, unlike messages, has to exist and we expect it to )
def find_element_or_none_wait(driver, root_elem, locate_by, locator, time_out, poll_frequency=0.5):
    try:
        return WebDriverWait(driver, time_out, poll_frequency=poll_frequency).until(
                lambda driver: root_elem.find_element(locate_by, locator))
    except TimeoutException:
        return None