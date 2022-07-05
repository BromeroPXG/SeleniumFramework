import time
from pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# all page specfic class will call BasePage objects
class Checkout_Page(BasePage):

    title = (By.XPATH, '//*[contains(@class, "page-title")]')
    delivery_method_delivery = (By.XPATH, '//*[contains(@for, "shippingDelivery-home")]')
    delivery_method_store = (By.XPATH, '//*[contains(@for, "shippingDelivery-store")]')
    first_name = (By.XPATH, '//*[contains(@id, "shippingFirstNamedefault")]')
    last_name = (By.XPATH, '//*[contains(@id, "shippingLastNamedefault")]')
    address1 = (By.XPATH, '//*[contains(@id, "shippingAddressOnedefault")]')
    country_ele = (By.XPATH, '//*[contains(@id, "shippingCountrydefault")]')
    state_ele = (By.XPATH, '//*[contains(@id, "shippingStatedefault")]')
    city_ele = (By.XPATH, '//*[contains(@id, "shippingAddressCitydefault")]')
    zip_ele = (By.XPATH, '//*[contains(@id, "shippingZipCodedefault")]')
    phone_ele = (By.XPATH, '//*[contains(@id, "shippingPhoneNumberdefault")]')
    ground_ship_ele = (By.XPATH, '//*[contains(@for, "shippingMethod-PXG-001")]')
    air_ship_ele = (By.XPATH, '//*[contains(@for, "shippingMethod-PXG-002")]')
    fast_ship_ele = (By.XPATH, '//*[contains(@for, "shippingMethod-PXG-003")]')
    gift_ele = (By.XPATH, '//*[contains(@for, "isGift")]')
    gift_message_ele = (By.XPATH, '//*[contains(@name, "dwfrm_shipping_shippingAddress_giftMessage")]')
    next_payment_btn_ele = (By.XPATH, '//*[contains(@value, "submit-shipping")]')
    name_on_card_ele = (By.XPATH, '//*[contains(@name, "dwfrm_billing_creditCardFields_cardOwner")]')
    cc_ele = (By.ID, 'credit-card-number')
    exp_ele = (By.ID, 'expiration')
    cvv_ele = (By.ID, 'cvv')
    payment_email_ele = (By.XPATH, './/*[contains(@name, "dwfrm_billing_contactInfoFields_email")]')
    payment_phone_ele = (By.XPATH, './/*[contains(@name, "dwfrm_billing_contactInfoFields_phone")]')
    ##the below locators are braintree iframe fields needed to pass cc#, exp, and CVV
    cc_parent_ele = (By.ID, 'braintree-hosted-field-number')
    exp_parent_ele = (By.ID, 'braintree-hosted-field-expirationDate')
    cvv_parent_ele = (By.ID, 'braintree-hosted-field-cvv')
    ##
    review_order_button = (By.XPATH, '//*[contains(@class, "btn btn-secondary btn-block submit-payment")]')
    place_order_button = (By.XPATH, '//*[contains(@class, "btn btn-secondary btn-block place-order")]')

    def __init__(self, driver):
        self.driver = driver

    def get_page_title(self):
        title = self.get_element(self.title)
        return title.text.strip()

    # method arg should be "delivery" or "store" for delivery or free store pickup
    def select_delivery_method(self, method):
        method_lower = method.lower()  # makes method param case-insensitive
        if method_lower == 'delivery':
            button_ele = self.get_elements(self.delivery_method_delivery)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button_ele[0])).click()
        if method_lower == 'store':
            button_ele = self.get_elements(self.delivery_method_store)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button_ele[0])).click()

    # find all elements and pass string inputs
    def enter_shipping_data(self, first, last, address, country, state, city, zip, phone):
        self.do_send_keys(self.first_name, first)
        self.do_send_keys(self.last_name, last)
        self.do_send_keys(self.address1, address)
        country_select = Select(self.get_element(self.country_ele))
        country_select.select_by_value(country)
        state_select = Select(self.get_element(self.state_ele))
        state_select.select_by_value(state)
        self.do_send_keys(self.city_ele, city)
        self.do_send_keys(self.zip_ele, zip)
        self.do_send_keys(self.phone_ele, phone)
        time.sleep(2)

    def select_shipping_method(self, shipping_method):
        shipping_method_lower = shipping_method.lower()  # makes method param case-insensitive
        if shipping_method_lower == "ground":
            self.do_click(self.ground_ship_ele)
        if shipping_method_lower == "air":
            self.do_click(self.air_ship_ele)
        if shipping_method_lower == "fast":
            self.do_click(self.fast_ship_ele)

    def add_gift_message(self, gift_message):
        self.do_click(self.gift_ele)
        time.sleep(4)
        self.do_send_keys(self.gift_message_ele, gift_message)

    def click_next_payment(self):
        self.do_click(self.next_payment_btn_ele)
        time.sleep(5)

    #in order to enter CC#, exp and cvv the follow was needed:
    #1. find braintrain iframe element and switch to frame
    #2. find braintree textbox element and add desired text
    #3. invoke driver to switch back to main HTML DOM
    #4. find next braintree iframe and repeat
    def enter_payment_data(self, name, card, exp, cvv, email, phone):
        self.do_send_keys(self.name_on_card_ele, name)
        self.switch_to_iframe(self.cc_parent_ele)
        self.do_send_keys(self.cc_ele, card)
        self.driver.switch_to.default_content()
        self.switch_to_iframe(self.exp_parent_ele)
        self.do_send_keys(self.exp_ele, exp)
        self.driver.switch_to.default_content()
        self.switch_to_iframe(self.cvv_parent_ele)
        self.do_send_keys(self.cvv_ele, cvv)
        self.driver.switch_to.default_content()
        self.do_send_keys(self.payment_email_ele, email)
        self.do_send_keys(self.payment_phone_ele, phone)

    def click_review_order(self):
        self.do_click(self.review_order_button)

    def click_place_order(self):
        self.do_click(self.place_order_button)







