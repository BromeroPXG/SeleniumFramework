import time
from configurations.config import TestData
from testCases.basetest import BaseTest
from pages.Driver_Configurators import driver_configurator
from utilities.customLogger import logGen
from pages.Cart_Review_Page import Cart_Review_Page
from pages.Checkout_login import Cart_Login_Page
import win32com.client
from utilities.ExcelUtils import ExcelData
from pages.BasePage import BasePage
from utilities.send_environment_keys import send_keys
from pages.Checkout_page import Checkout_Page
from pages.Order_Confirmation_Page import Order_Confirmation
import pytest


class Test_end_to_end_test(BaseTest):
    username = ExcelData().get_user_data_dict('guest')["Username"]
    password = ExcelData().get_user_data_dict('guest')["Password"]
    user_data = ExcelData().get_user_data_dict('guest')
    shell = win32com.client.Dispatch("WScript.Shell")
    logger = logGen.loggen()
    current_SKU = "DR-PXG15"  # this will be replaced with a pytest fixture list of test skus for this test(all drivers
    page_url = ExcelData().get_URL_from_page('Drivers', current_SKU)
    cart_url = ExcelData().get_URL_from_page('General', 'cart')
    environment = "Production"
    pages = "Drivers"

    # global configurator_selection
    # configurator_selection = {} # this will be edited as a global throughout tests
    # future work, need to work:
    # use fixture @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])

    # due to send keys annoyance, this always needs to be first test
    def test_driver_launch(self, init_driver):
        self.driver.get(self.page_url)
        send_keys().send_env_keys()
        assert True


    def test_config_page(self):
        self.logger.info("******Test configurator page is correct******")
        self.logger.info("******Verify configurator Title matches data******")
        self.driver.get(self.page_url)
        self.driver_page = driver_configurator(self.driver)
        title = self.driver_page.get_page_title()
        if title.lower() in (TestData.page_title_dict[self.current_SKU]).lower():  # needs to be not be harcoded from excel utils
            self.logger.info(f"******PASS Page title == {title}******")
            assert True
        else:
            self.logger.info(f"******FAIL Page title == {title}******")
            self.driver.save_screenshot(".\\screenshots\\" + "test_end_to_end.png")
            assert False

    def test_add_to_cart(self):
        self.logger.info("******Test SKU is added to cart******")
        self.logger.info("******Verify configurator Title matches data******")
        self.driver.get(self.page_url)
        self.driver_page = driver_configurator(self.driver)
        minicart_qty_old = BasePage(self.driver).get_minicart_value()  # gets the current minicart quantity in order to test if add to cart was successful
        time.sleep(3)
        self.driver_page.click_buy_now()
        time.sleep(3)
        self.driver_page.click_checkout()
        time.sleep(3)
        minicart_qty_new = BasePage(self.driver).get_minicart_value()
        if minicart_qty_new > minicart_qty_old:
            self.logger.info(
                f"******PASS: Old cart value == {minicart_qty_old} New cart value == {minicart_qty_new}******")
            assert True
        else:
            self.logger.info(f"******FAIL: Old cart val == {minicart_qty_old} New cart va == {minicart_qty_new}******")
            self.driver.save_screenshot(".\\screenshots\\" + "test_end_to_end.png")
            assert False

    # i.e. ({PXG 0811 XF GEN4 DRIVER:{configurator selection sent to cart}, PXG 0811 X GEN4 DRIVER{config....}
    def test_shopping_cart_validation(self):
        # this section gets the dictionary from the configurator {self.DR_PXG
        self.logger.info("******Get current configurator selection, add to cart, and test********")
        self.driver_page = driver_configurator(self.driver)
        club_selection_dict = self.driver_page.get_current_configurator_selection()
        time.sleep(2)
        self.driver.get(self.cart_url)
        time.sleep(3)
        self.cart_page = Cart_Review_Page(self.driver)
        cart_dict = self.cart_page.get_cart_details_dict()

        # this section runs dictionary logic to compare keyvalues
        results_dict = {}
        keys = club_selection_dict.keys()
        for key in club_selection_dict.keys():
            if cart_dict[key].lower() in club_selection_dict[key].lower():
                results_dict[key] = "Pass"
            else:
                results_dict[key] = "Fail"
        self.cart_page.click_checkout()
        if "Fail" in results_dict.values():
            self.logger.info("******Shopping Cart Values FAIL********")
            self.logger.info(f"******Configurator Selection: {club_selection_dict}********")
            self.logger.info(f"******Cart data: {cart_dict}********")
            self.logger.info(f"******{results_dict}********")
            assert False
        else:
            self.logger.info("******Shopping Cart Values Match Expected Values********")
            self.logger.info(f"******Configurator Selection: {club_selection_dict}********")
            self.logger.info(f"******Cart data: {cart_dict}********")
            self.logger.info(f"******{results_dict}********")
            assert True

    def test_checkout_login(self):
        self.checkout_login = Cart_Login_Page(self.driver)
        if TestData.user_type == "guest":
            time.sleep(4)
            self.checkout_login.checkout_guest()
        else:
            time.sleep(4)
            self.checkout_login.checkout_with_credentials(self.username, self.password)
        time.sleep(10)
        self.checkout_page = Checkout_Page(self.driver)
        if (self.checkout_page.get_page_title()).lower() == (TestData.page_title_dict["Checkout"]).lower():
            self.logger.info(f"******Successfully entered check as {TestData.user_type}********")
            assert True
        else:
            self.logger.info(f"******Checkout Login Failed********")
            self.logger.info(f"******See Screen Shot********")
            assert False

    def test_checkout_shipping(self):
        self.checkout_page = Checkout_Page(self.driver)
        self.checkout_page.select_delivery_method(self.user_data["Delivery"])
        self.checkout_page.enter_shipping_data(self.user_data["First"], self.user_data["Last"], self.user_data["Street"],self.user_data["Country"], self.user_data["State"], self.user_data["City"], self.user_data["Zip"], self.user_data["Phone"])
        self.checkout_page.select_shipping_method(self.user_data["Shipping"])
        if self.user_data["Gift"].lower() == "y":
            self.checkout_page.add_gift_message(self.user_data["Gift_message"])
        self.checkout_page.click_next_payment()
        assert True

    def test_checkout_payment(self):
        self.checkout_page = Checkout_Page(self.driver)
        self.checkout_page.enter_payment_data(f"{self.user_data['First']} {self.user_data['Last']}", self.user_data['Card'], self.user_data['Expiration'], self.user_data['CVV'], self.user_data['Username'], self.user_data['Phone'])
        self.checkout_page.click_review_order()
        time.sleep(5)
        self.checkout_page.click_place_order()
        assert True

    def test_checkout_validated_finish(self):
        self.order_review_page = Order_Confirmation(self.driver)
        order_details = self.order_review_page.order_detail_dict()
        product_summary = self.order_review_page.product_summary_dict()
        order_summary = self.order_review_page.order_summary_dict()
        if self.user_data["Gift"].lower() == "y":
            order_details["Gift"] = self.order_review_page.get_gift_message()
        self.logger.info(f"{order_details}")
        self.logger.info(f"{product_summary}")
        self.logger.info(f"{order_summary}")
        assert True
