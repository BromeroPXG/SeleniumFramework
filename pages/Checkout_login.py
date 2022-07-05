import time
from pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from utilities.ExcelUtils import ExcelData


# all page specfic class will call BasePage objects
class Cart_Login_Page(BasePage):
    title = (By.XPATH, './/*[contains(@class, "page-title pt-3 mb-0")]')
    guest_check_button_ele = (By.XPATH, './/*[contains(@class, "btn btn-block btn-secondary checkout-as-guest mt-4")]')
    email_field_ele = (By.ID, 'login-form-email')
    password_field_ele = (By.ID, 'login-form-password')
    login_button = (By.XPATH, './/*[contains(@class, "btn btn-block btn-secondary")]')

    def __init__(self, driver):
        self.driver = driver

    def get_page_title(self):
        return self.get_element(self.title)

    def checkout_guest(self):
        self.do_click(self.guest_check_button_ele)

    def checkout_with_credentials(self, username, password):
        self.do_send_keys(self.email_field_ele, username)
        self.do_send_keys(self.password_field_ele, password)
        self.do_click(self.login_button)
