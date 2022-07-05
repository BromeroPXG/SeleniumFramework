import pytest
import time
from configurations.config import TestData
from testCases.basetest import BaseTest
from pages.LoginPage import LoginPage
from pages.BasePage import BasePage
from utilities.customLogger import logGen


class Test_Login(BaseTest):
    logger = logGen.loggen()  # logger i built in utilities folder

    def test_login_page_title(self):
        self.logger.info("******Test login page is correct******")
        self.logger.info("******Verify Home Page Title******")
        self.loginPage = LoginPage(self.driver)
        title = self.loginPage.get_login_page_title(LoginPage.my_account_title)
        if title == TestData.login_page_title:
            self.logger.info(f"******PASS Page title == {title}******")
            assert True
        else:
            self.logger.info(f"******FAIL Page title == {title}******")
            self.driver.save_screenshot(".\\screenshots\\" + "test_login_page_title.png")
            assert False

    def test_login(self):
        self.logger.info("******Test login function******")
        self.logger.info("******Verify my account page as validation of successful login******")
        self.loginPage = LoginPage(self.driver)
        self.loginPage.do_login(TestData.direct_account_user, TestData.direct_account_pw)
        time.sleep(10)
        if self.loginPage.get_login_page_title(LoginPage.my_account_title) == TestData.account_page_title:
            self.logger.info(f"******PASS Page title == {self.loginPage.get_login_page_title(LoginPage.my_account_title)}******")
            assert True
        else:
            self.logger.info(f"******FAIL Page title == {self.loginPage.get_login_page_title(LoginPage.my_account_title)}******")
            self.driver.save_screenshot(".\\screenshots\\" + "test_login.png")
            assert False
