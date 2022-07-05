from pages.BasePage import BasePage
from selenium.webdriver.common.by import By


# all page specfic class will call BasePage objects
class Order_Confirmation(BasePage):
    title = (By.CLASS_NAME, 'order-thank-you-msg')
    continue_shopping = (By.XPATH, '//*[contains(@class, "btn btn-secondary btn-block order-confirmation-continue-shopping")]')
    line_item_title_parent = (By.CLASS_NAME, "line-item-header")
    original_price_parent = (By.XPATH, '//*[contains(@class, "strike-through list")]')
    selected_price = (By.XPATH, './/*[contains(@class, "pricing line-item-total-price-amount item-total")]')
    dexterity = (By.XPATH, './/*[contains(@class, "line-item-attributes dexterity")]')
    shaft_flex = (By.XPATH, './/*[contains(@class, "line-item-attributes shaftFlex")]')
    shaft_length = (By.XPATH, './/*[contains(@class, "line-item-attributes shaftLength")]')
    shaft_selection = (By.XPATH, './/*[contains(@class, "line-item-attributes shaftChoice")]')
    grip_size = (By.XPATH, './/*[contains(@class, "line-item-attributes gripSize")]')
    grip_selection = (By.XPATH, './/*[contains(@class, "line-item-attributes gripName")]')
    club_selection = (By.XPATH, './/*[contains(@class, "line-item-attributes clubNumber")]')
    shipping_address_parent = (By.XPATH, '//*[contains(@class, "summary-details shipping")]')
    billing_address_parent = (By.XPATH, '//*[contains(@class, "summary-details billing")]')
    # have to xpath order number and date for now
    order_number = (By.XPATH, '//*[@id="maincontent"]/div[2]/div[1]/div[2]/div[1]/div/div/div/div[2]/div[2]')
    order_date = (By.XPATH, '//*[@id="maincontent"]/div[2]/div[1]/div[2]/div[1]/div/div/div/div[3]/div[2]')
    shipping_method = (By.CLASS_NAME, 'shipping-method-title')
    shipping_cost = (By.XPATH, './/*[contains(@class, "text-right text-md-left pricing shipping-method-price mb-0")]')
    payment_method = (By.CLASS_NAME, 'creditcard-method-name')
    payment_total = (By.CLASS_NAME, 'creditcard-amount')
    gift_message = (By.CLASS_NAME, 'gift-message-summary')
    shipping_first = "firstName"
    shipping_last = "lastName"
    shipping_street = 'address1'
    shipping_city = 'city'
    shipping_state = 'stateCode'
    shipping_zip = 'postalCode'
    shipping_phone = 'shipping-phone'
    billing_first = "firstName"
    billing_last = "lastName"
    billing_street = 'address1'
    billing_city = 'city'
    billing_state = 'stateCode'
    billing_zip = 'postalCode'
    billing_email = 'order-summary-email'
    billing_phone = 'order-summary-phone'
    summary_subtotal = (By.CLASS_NAME, 'sub-total')
    summary_shipping_cost = (By.CLASS_NAME, 'shipping-total-cost')
    summary_sales_tax = (By.CLASS_NAME, 'tax-total')
    summary_total = (By.CLASS_NAME, 'grand-total-sum')

    def __init__(self, driver):
        self.driver = driver

    def get_page_title(self):
        return (self.get_element(self.title)).text

    # there are going to be 3 data dictionaries for this page output (in anticipation of growth)
    # order_detail_dict = billing, shipping, payment details
    # this dict is nested with shipping address and billing address
    # call billing street by order_detail_dict()["Billing"]["Street"
    # product_summary_dict = ({dexterity: R, model: GEN4 0811XF Driuer, club: DR-PXG15-10.5, flex:r.....})
    # summary_dict = ({ subtotal, shipping, tax, total])
    def order_detail_dict(self):
        out_dict = {'Order': self.get_order_number(),
                    'Date': self.get_order_date(),
                    "Shipping": {
                        "First": self.get_shipping_first_name(),
                        "Last": self.get_shipping_last_name(),
                        "Street": self.get_shipping_street(),
                        "City": self.get_shipping_city(),
                        "State": self.get_shipping_state(),
                        "Zip": self.get_shipping_zip(),
                        "Phone": self.get_shipping_phone()},
                    "Billing": {
                        "First": self.get_billing_first_name(),
                        "Last": self.get_billing_last_name(),
                        "Street": self.get_billing_street(),
                        "City": self.get_billing_city(),
                        "State": self.get_billing_state(),
                        "Zip": self.get_billing_zip(),
                        "Email": self.get_billing_email(),
                        "Phone": self.get_billing_phone()},
                    'Shipping_method': self.get_shipping_method(),
                    'Shipping_price': self.get_shipping_price(),
                    'Payment': self.get_payment_type(),
                    'Order_total': self.get_order_detail_total()}
        return out_dict

    # for multi product, loop and use title as highest level for dict and attributes as 2nd level
    def product_summary_dict(self):
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

    def order_summary_dict(self):
        out_dict = {'Subtotal': self.get_summary_subtotal(),
                    'Shipping': self.get_summary_shipping(),
                    'Tax': self.get_summary_tax(),
                    'Total': self.get_summary_total()}
        return out_dict

    def get_line_item_title(self):
        line_item_title_parent = self.get_element(self.line_item_title_parent)
        title_ele = line_item_title_parent.find_element(By.TAG_NAME, "span")
        return title_ele.text

    def get_cart_original_price(self):
        original_price_parent_ele = self.get_element(self.original_price_parent)
        original_price_ele = original_price_parent_ele.find_element(By.CLASS_NAME, 'value')
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

    def click_continue_shopping(self):
        self.do_click(self.continue_shopping)

    def get_shipping_first_name(self):
        parent = self.get_element(self.shipping_address_parent)
        child = parent.find_element_by_class_name(self.shipping_first)
        return child.text

    def get_shipping_last_name(self):
        parent = self.get_element(self.shipping_address_parent)
        child = parent.find_element_by_class_name(self.shipping_last)
        return child.text

    def get_shipping_street(self):
        parent = self.get_element(self.shipping_address_parent)
        child = parent.find_element_by_class_name(self.shipping_street)
        return child.text

    def get_shipping_city(self):
        parent = self.get_element(self.shipping_address_parent)
        child = parent.find_element_by_class_name(self.shipping_city)
        return child.text

    def get_shipping_state(self):
        parent = self.get_element(self.shipping_address_parent)
        child = parent.find_element_by_class_name(self.shipping_state)
        return child.text

    def get_shipping_zip(self):
        parent = self.get_element(self.shipping_address_parent)
        child = parent.find_element_by_class_name(self.shipping_zip)
        return child.text

    def get_shipping_phone(self):
        parent = self.get_element(self.shipping_address_parent)
        child = parent.find_element_by_class_name(self.shipping_phone)
        return child.text

    def get_billing_first_name(self):
        parent = self.get_element(self.billing_address_parent)
        child = parent.find_element_by_class_name(self.billing_first)
        return child.text

    def get_billing_last_name(self):
        parent = self.get_element(self.billing_address_parent)
        child = parent.find_element_by_class_name(self.billing_last)
        return child.text

    def get_billing_street(self):
        parent = self.get_element(self.billing_address_parent)
        child = parent.find_element_by_class_name(self.billing_first)
        return child.text

    def get_billing_city(self):
        parent = self.get_element(self.billing_address_parent)
        child = parent.find_element_by_class_name(self.billing_first)
        return child.text

    def get_billing_state(self):
        parent = self.get_element(self.billing_address_parent)
        child = parent.find_element_by_class_name(self.billing_state)
        return child.text

    def get_billing_zip(self):
        parent = self.get_element(self.billing_address_parent)
        child = parent.find_element_by_class_name(self.billing_state)
        return child.text

    def get_billing_email(self):
        parent = self.get_element(self.billing_address_parent)
        child = parent.find_element_by_class_name(self.billing_email)
        return child.text

    def get_billing_phone(self):
        parent = self.get_element(self.billing_address_parent)
        child = parent.find_element_by_class_name(self.billing_phone)
        return child.text

    def get_order_number(self):
        return self.get_element(self.order_number).text

    def get_order_date(self):
        return self.get_element(self.order_date).text

    def get_shipping_method(self):
        return self.get_element(self.shipping_method).text

    def get_shipping_price(self):
        return self.get_element(self.shipping_cost).text

    def get_gift_message(self):
        return self.get_element(self.gift_message).text

    def get_payment_type(self):
        return self.get_element(self.payment_method).text

    def get_order_detail_total(self):
        return self.get_element(self.payment_total).text

    def get_summary_subtotal(self):
        return self.get_element(self.summary_subtotal).text

    def get_summary_shipping(self):
        return self.get_element(self.summary_shipping_cost).text

    def get_summary_tax(self):
        return self.get_element(self.summary_sales_tax).text

    def get_summary_total(self):
        return self.get_element(self.summary_total).text
