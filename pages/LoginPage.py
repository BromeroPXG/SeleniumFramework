from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import win32com.client
from pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from configurations.config import TestData

class LoginPage(BasePage):
    email_login = (By.ID, "login-form-email")
    password_login = (By.ID, "login-form-password")
    login_button = (By.XPATH, "//button[normalize-space()='Login']")
    my_account_title = (By.CLASS_NAME, "page-title")

    # creating an unbound super object (ill explain later) - Brian R
    # unfortunately i have to hardcode this bullshit to send environment login keys
    def __init__(self, driver):
        self.driver = driver

    # below functions are page actions for the login page
    # get page title for validation
    def get_login_page_title(self, title):
        return self.get_class_text(self.my_account_title)

    # loginto account with credentials
    def do_login(self, username, password):
        self.do_send_keys(self.email_login, username)
        self.do_send_keys(self.password_login, password)
        self.do_click(self.login_button)

