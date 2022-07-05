import time
from configurations.config import TestData
from testCases.basetest import BaseTest
from pages.Driver_Configurators import driver_configurator
from pages.BasePage import BasePage
from utilities.customLogger import logGen
from pages.LoginPage import LoginPage
from pages.Cart_Review_Page import Cart_Review_Page
from utilities.ExcelUtils import ExcelData
from utilities.send_environment_keys import send_keys
import win32com.client

class Test_01(BaseTest):
    page_url = ExcelData().get_URL_from_page('Drivers', "DR-PXG15")
    logger = logGen.loggen()
    shell = win32com.client.Dispatch("WScript.Shell")

    def test_driver_launch(self, init_driver):
        self.driver.get(self.page_url)
        send_keys().send_env_keys()
        assert True

    def test_add_to_cart(self):
        self.logger.info("******Test SKU is added to cart******")
        self.logger.info("******Verify configurator Title matches data******")
        self.driver.get(self.page_url)
        self.driver_page = driver_configurator(self.driver)
        minicart_qty_old = BasePage(self.driver).get_minicart_value() # gets the current minicart quantity in order to test if add to cart was successful
        time.sleep(3)
        self.driver_page.click_checkout()
        time.sleep(5)
        minicart_qty_new = BasePage(self.driver).get_minicart_value()
        if minicart_qty_new > minicart_qty_old:
            self.logger.info(f"******PASS: Old cart value == {minicart_qty_old} New cart value == {minicart_qty_new}******")
            assert True
        else:
            self.logger.info(f"******FAIL: Old cart val == {minicart_qty_old} New cart va == {minicart_qty_new}******")
            self.driver.save_screenshot(".\\screenshots\\" + "test_end_to_end.png")
            assert False

