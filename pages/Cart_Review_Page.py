import time
from pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from configurations.config import TestData
from utilities.ExcelUtils import ExcelData
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options


# all page specfic class will call BasePage objects
class Cart_Review_Page(BasePage):
    title = (By.XPATH, '//*[@id="maincontent"]/div[2]/h1')
    line_item_title = (By.CLASS_NAME, "line-item-name")
    original_price = (By.XPATH, '//*[@id="maincontent"]/div[3]/div[1]/div[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div/span/del/span/span')
    selected_price = (By.XPATH, './/*[contains(@class, "pricing line-item-total-price-amount item-total")]')
    dexterity = (By.XPATH, './/*[contains(@class, "line-item-attributes dexterity")]')
    shaft_flex = (By.XPATH, './/*[contains(@class, "line-item-attributes shaftFlex")]')
    shaft_length = (By.XPATH, './/*[contains(@class, "line-item-attributes shaftLength")]')
    shaft_selection = (By.XPATH, './/*[contains(@class, "line-item-attributes shaftChoice")]')
    grip_size = (By.XPATH, './/*[contains(@class, "line-item-attributes gripSize")]')
    grip_selection = (By.XPATH, './/*[contains(@class, "line-item-attributes gripName")]')
    club_selection = (By.XPATH, './/*[contains(@class, "line-item-attributes clubNumber")]')
    checkout_button_ele = (By.XPATH, '//*[contains(@class, "btn btn-secondary btn-block checkout-btn")]')

    def __init__(self, driver):
        self.driver = driver

    def get_page_title(self):
        return self.get_element(self.title)

    # takes a snapshot of all configurator selections and returns a dictionary
    # i.e. ({dexterity: R, model: GEN4 0811XF Driuer, club: DR-PXG15-10.5, flex:r.....})
    def get_cart_details_dict(self):
        out_dict = {'Dexterity': self.get_cart_dexterity(),
                    'Shaft Flex': self.get_cart_shaft_flex(),
                    'Shaft Length': self.get_cart_shaft_length(),
                    'Shaft Choice': self.get_cart_shaft(),
                    'Grip Size': self.get_cart_grip_size(),
                    'Grip Name': self.get_cart_grip(),
                    'Club Selection': self.get_cart_club_selection(),
                    'Original Price': self.get_cart_original_price(),
                    'Selected Price': self.get_cart_price(),
                    'Title': self.get_line_item_title()}
        return out_dict

    def get_line_item_title(self):
        line_item_title = self.get_element(self.line_item_title)
        return line_item_title.text

    def get_cart_original_price(self):
        original_price_ele = self.get_element(self.original_price)
        op_attrib = original_price_ele.get_attribute('content')
        op_fixed = op_attrib[0:3]
        op_final_form = "$" + str(op_fixed)
        return op_final_form

    def get_cart_price(self):
        sp_element = self.get_element(self.selected_price)
        return sp_element.text

    def get_cart_dexterity(self):
        dex_ele = self.get_element(self.dexterity)
        return (dex_ele.text).split(": ", 1)[1]

    def get_cart_shaft_flex(self):
        sf_ele = self.get_element(self.shaft_flex)
        return (sf_ele.text).split(": ", 1)[1]

    def get_cart_shaft(self):
        shaft_ele = self.get_element(self.shaft_selection)
        return (shaft_ele.text).split(": ", 1)[1]

    def get_cart_grip_size(self):
        gs_ele = self.get_element(self.grip_size)
        return (gs_ele.text).split(": ", 1)[1]

    def get_cart_grip(self):
        grip_ele = self.get_element(self.grip_selection)
        return (grip_ele.text).split(": ", 1)[1]

    def get_cart_shaft_length(self):
        sl_ele = self.get_element(self.shaft_length)
        return (sl_ele.text).split(": ", 1)[1]

    def get_cart_club_selection(self):
        cs_ele = self.get_element(self.club_selection)
        return (cs_ele.text).split(": ", 1)[1]

    def click_checkout(self):
        self.do_click(self.checkout_button_ele)


