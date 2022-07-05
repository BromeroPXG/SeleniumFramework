import time
from configurations.config import TestData
from testCases.basetest import BaseTest
from pages.Driver_Configurators import driver_configurator
from utilities.customLogger import logGen
from pages.Cart_Review_Page import Cart_Review_Page
from pages.Checkout_login import Cart_Login_Page
import win32com.client
from utilities.ExcelUtils import ExcelData
from utilities.SOQL_query import SOQL_query
from utilities.send_environment_keys import send_keys
import pytest


class Test_SKU_Validator(BaseTest):
    username = ExcelData().get_user_data_dict('Logins', 'hero')["Username"]
    password = ExcelData().get_user_data_dict('Logins', 'hero')["Password"]
    shell = win32com.client.Dispatch("WScript.Shell")
    logger = logGen.loggen()
    current_SKU = "DR-PXG15"  # this will be replaced with a pytest fixture list of test skus for this test(all drivers
    page_url = ExcelData().get_URL_from_page('Drivers', current_SKU)
    cart_url = ExcelData().get_URL_from_page('General', 'cart')
    environment = "production"
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

    @pytest.mark.parametrize("page_url,SKU", ExcelData().get_SKU_validation_params(environment, pages))
    def test_all_SKUs_exist(self,page_url,SKU):
        self.driver.get(page_url)
        configurator_sku_list_master = SOQL_query().get_all_online_skus_by_master(SKU, "Direct")
        time.sleep(2)
        self.driver_page = driver_configurator(self.driver)
        configurator_sku_list_test = self.driver_page.get_list_of_all_configurator_SKU()
        #get_list_of_all_configurator_SKU() comes back as a nested list
        #flatlist flattens that output into a clean single list
        flatlist = [item for elem in configurator_sku_list_test for item in elem]
        #skus_in_configurator = (set(flatlist) - set(configurator_sku_list_master))
        skus_NOT_in_configurator = (set(configurator_sku_list_master) - set(flatlist))

        if all(x in flatlist for x in configurator_sku_list_master):
            self.logger.info(f"******PASS******")
            self.logger.info(f"******All SKUs in {SKU} Configurator are in the configurator******")
            assert True
        else:
            self.logger.info(f"******FAIL******")
            self.logger.info(f"******RESULTS FOR {SKU}******")
            self.logger.info(f"******-------------------------------------------******")
            self.logger.info(f"SKUs MISSING from configurator: {skus_NOT_in_configurator}")
            assert False

    def test_add_to_cart(self):
        self.logger.info("******Test SKU is added to cart******")
        self.logger.info("******Verify configurator Title matches data******")
        self.driver.get(self.page_url)
        self.driver_page = driver_configurator(self.driver)
        minicart_qty_old = self.driver_page.minicart_qty()  # gets the current minicart quantity in order to test if add to cart was successful
        time.sleep(3)
        self.driver_page.click_checkout()
        time.sleep(5)
        minicart_qty_new = self.driver_page.minicart_qty()
        if minicart_qty_new > minicart_qty_old:
            self.logger.info(f"******PASS: Old cart val == {minicart_qty_old} New cart va == {minicart_qty_new}******")
            assert True
        else:
            self.logger.info(f"******FAIL: Old cart val == {minicart_qty_old} New cart va == {minicart_qty_new}******")
            self.driver.save_screenshot(".\\screenshots\\" + "test_end_to_end.png")
            assert False

    # this is a non_test step that builds a nested dictionary with the current selection with the key of the configurator title
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
            self.logger.info(f"******{results_dict}********")
            assert False
        else:
            self.logger.info("******Shopping Cart Values Match Expected Values********")
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
        assert True
