from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# this class is the parent of all pages
# it contains all generic methods for all pages

class BasePage:
    minicart = (By.XPATH, '//*[contains(@class,"minicart-quantity")]')

    def __init__(self, driver):
        self.driver = driver

    # clicks element
    def do_click(self, by_locator):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(by_locator))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator)).click()

    # sends text keys to element
    def do_send_keys(self, by_locator, text):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(by_locator)).clear()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(by_locator)).send_keys(text)

    # return element text as var or action
    def get_element_text(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        return element.text

    # return bool if element or condition exists or is visible
    def is_visible(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    # gets page title
    def get_title(self, title):
        WebDriverWait(self.driver, 10).until(EC.title_is(title))
        return self.driver.title

    def get_class_text(self, by_locator):
        class_title = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        return class_title.text

    def get_elements(self, by_locator):
        elements = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located(by_locator))
        return elements

    def get_element(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(by_locator))
        return element

    # strips out minicart value as an integer (can be called from any test)
    def get_minicart_value(self):
        elements = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.minicart))
        for i in elements:
            raw = (i.text).strip()
            if raw.isnumeric():
                output = raw
        return int(output)

    def is_clickable(self, by_locator):
        button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
        return button

    # this is specifically to target braintree elements within their iframe
    def switch_to_iframe(self, by_locator):
        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it(by_locator))
