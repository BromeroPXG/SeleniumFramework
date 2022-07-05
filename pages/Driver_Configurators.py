import time
from pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from configurations.config import TestData
from utilities.ExcelUtils import ExcelData
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# all page specfic class will call BasePage objects
class driver_configurator(BasePage):
    # pageelement locations (this will be the same for most configurators)
    title = (By.CLASS_NAME, "h1.mb-3")
    original_price = (By.CLASS_NAME, 'c-cc__cta__pricing__savings__regular__price')
    selected_price = (By.CLASS_NAME, 'c-cc__cta__pricing__price')
    add_to_bag_btn = (By.XPATH, '//[contains(@class, "btn c-cc__cta__add-to-cart mb-2 btn-primary")]')
    minicart_locator = (By.XPATH, '/html/body/div[2]/header/nav/div/div[2]/div/div/div[1]/a/span')
    head_model_selector = (By.XPATH, '//*[@id="model"]')
    club_select_btn = (By.NAME, 'clubNumber')
    dexterity_radio_btn = (By.NAME, 'dexterity')
    shaft_flex_btn = (By.NAME, 'shaftFlex')
    shaft_length_selector = (By.XPATH, '//*[@id="shaftLength"]')
    shaft_selector = (By.XPATH, '//*[@id="shaftChoice"]')
    grip_size_selector = (By.XPATH, '//*[@id="gripSize"]')
    grip_selector = (By.XPATH, '//*[@id="gripManufacturer"]')
    all_radio_buttons = (By.XPATH, '//*[contains(@class,"custom-control-label")]')
    buy_now_ele = (By.XPATH, '//*[contains(@data-eventlabel,"buy now")]')
    configurator_title = (By.XPATH, '//*[contains(@class,"text-center display-8")]')

    def __init__(self, driver):
        self.driver = driver

    def get_page_title(self):
        return self.get_class_text(self.title)

    def get_configurator_title(self):
        title = self.get_element(self.configurator_title)
        up_title = title.text.upper()
        out_title = up_title.split('YOUR ')
        return out_title[1]

    def click_buy_now(self):
        self.do_click(self.buy_now_ele)

    def click_checkout(self):
        self.do_click(self.add_to_bag_btn)

    def minicart_qty(self):
        qty = self.get_class_text(self.minicart_locator)
        qty_int = int(qty.strip())
        return qty_int

    # takes a snapshot of all configurator selections and returns a dictionary
    # i.e. ({dexterity: R, model: GEN4 0811XF Driuer, club: DR-PXG15-10.5, flex:r.....})
    def get_current_configurator_selection(self):
        out_dict = {'Dexterity': self.get_current_dexterity(),
                    'Shaft Flex': self.get_current_shaft_flex(),
                    'Shaft Length': self.get_current_shaft_length(),
                    'Shaft Choice': self.get_current_shaft(),
                    'Grip Size': self.get_current_grip_size(),
                    'Grip Name': self.get_current_grip(),
                    'Club Selection': self.get_current_club_selection(),
                    'Original Price': self.get_original_price(),
                    'Selected Price': self.get_selected_price(),
                    'Title': self.get_configurator_title()}
        return out_dict

    def make_configurator_selection(self):
        # this is for when i have help with this nightmare - brian
        # i need to figure out a good set of logic to randomly select configurator parameters for the page
        return

        # get a dictionary output of configurator selection for validation
        # i.e.{dexterity: L, model: GEN4 0811X Driver, club: 10.5, sflex: R}

    def get_current_club_selection(self):
        for i in self.get_elements(self.club_select_btn):
            if i.is_selected():
                club_number = i.get_attribute("value")
        return club_number

    def get_all_clubhead_SKUs(self):
        return [i.get_attribute("value") for i in self.get_elements(self.club_select_btn)]

    def get_all_shafts(self):  # returns a list of all shaft SKUs in configurator
        shaftlist_element = self.get_element(self.shaft_selector)
        shaftlist = Select(shaftlist_element)
        return [sku.text for sku in shaftlist.options]

    def get_all_shaft_SKUs(self):
        shaftlist_element = self.get_element(self.shaft_selector)
        shaftlist = Select(shaftlist_element)
        sku_list = []
        for sku in shaftlist.options:
            raw = sku.get_attribute("value")
            sku_list.append(raw.split("/ ", 1)[1])
        return sku_list

    def get_current_shaft(self):  # gets current shaft
        shaftlist_element = self.get_element(self.shaft_selector)
        shaftlist = Select(shaftlist_element)
        return shaftlist.first_selected_option.text

    def get_all_shaft_lengths(self):  # get list of available shaft lengths
        shaft_length_element = self.get_element(self.shaft_length_selector)
        shaft_length_list = Select(shaft_length_element)
        return [sku.text for sku in shaft_length_list.options]

    def get_current_shaft_length(self):  # get current shaft length
        shaft_length_element = self.get_element(self.shaft_length_selector)
        shaft_length_list = Select(shaft_length_element)
        return shaft_length_list.first_selected_option.text

    def get_all_shaft_flex(self):  # get list of available flex selections
        flex_elements = self.get_elements(self.shaft_flex_btn)
        return [flex.get_attribute("value") for flex in flex_elements]

    def get_current_shaft_flex(self):  # get shaft flex currently selected
        for i in self.get_elements(self.shaft_flex_btn):
            if i.is_selected():
                flex = i.get_attribute("value")
        return flex

    def get_all_grip_sizes(self):  # get grip sizes available
        grip_size_list_element = self.get_element(self.grip_size_selector)
        grip_size = Select(grip_size_list_element)
        return grip_size.options

    def get_current_grip_size(self):  # get current grip size selected
        grip_size_list_element = self.get_element(self.grip_size_selector)
        grip_size = Select(grip_size_list_element)
        return grip_size.first_selected_option.text

    def get_all_grips(self):  # get all grip skus available in dropdown
        grip_list_element = self.get_element(self.grip_selector)
        grips = Select(grip_list_element)
        return [grip.text for grip in grips.options]

    def get_all_grip_SKUs(self):
        grip_list_element = self.get_element(self.grip_selector)
        grips = Select(grip_list_element)
        grip_skus = [(i.get_attribute("value")).split("/ ", 1)[1] for i in grips.options]
        return grip_skus

    def get_current_grip(self):  # get current grip selected
        grip_list_element = self.get_element(self.grip_selector)
        grips = Select(grip_list_element)
        return grips.first_selected_option.text

    def get_current_dexterity(self):  # get current dexterity selected
        for i in self.get_elements(self.dexterity_radio_btn):
            if i.is_selected():
                dexterity = i.get_attribute("value")
        return dexterity

    def get_selected_price(self):
        selected_price = self.get_element(self.selected_price)
        return selected_price.text

    def get_original_price(self):
        original_price = self.get_element(self.original_price)
        return original_price.text

    def get_list_of_all_configurator_SKU(self):
        master_SKUs = []
        #cycle through grip size dropdown and get all grip SKUs
        for k in self.get_all_grip_sizes():
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(k)).click()
            time.sleep(1)
            master_SKUs.append(self.get_all_grip_SKUs())
            time.sleep(1)
        #cycle through shaft flex radio buttons and get all shafts
        shaft_flex_elements = self.get_elements(self.shaft_flex_btn)
        for i in shaft_flex_elements:
            #this is a step-up step-down method
            #find unique element, step up to parent, step down to adjacent child
            parent_element = i.find_element_by_xpath('..')
            child_button = parent_element.find_element_by_class_name('custom-control-label')
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(child_button)).click()
            time.sleep(1)
            master_SKUs.append(self.get_all_shaft_SKUs())
        dex_element = self.get_elements(self.dexterity_radio_btn)
        #cycle through dexterity and get club head SKUs
        for j in dex_element:
            parent_dex_element = j.find_element_by_xpath('..')
            child_dex_element = parent_dex_element.find_element_by_xpath('//label')
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(child_dex_element)).click()
            time.sleep(1)
            master_SKUs.append(self.get_all_clubhead_SKUs())
            time.sleep(1)
        return master_SKUs


