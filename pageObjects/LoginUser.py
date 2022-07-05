from selenium import webdriver
import win32com.client
import time

class LoginsPage():
    textbox_username_id = "login-form-email"
    textbox_password_id = "login-form-password"
    login_button_xpath = "//button[@type='submit'][text()='Login']"
    shell = win32com.client.Dispatch("WScript.Shell") #this is only used for the environment login (storefront,pxg1234)

    def __int__(self,driver):
        self.driver = driver

    #set login username
    def setUserName(self,username):
        self.find_element_by_id(self.textbox_username_id).clear() #clears username field
        self.driver.find_element_by_id(self.textbox_username_id).send_keys(username) #sends username keys

    #send login password
    def setPassword (self,password):
        self.driver.find_element_by_id(self.textbox_password_id).clear() #clears pw field
        self.driver.find_element_by_id(self.textbox_password_id).send_keys(password)  # sends password keys

    def clickLogin(self):
        self.driver.find_element_by_xpath(self.login_button_xpath).click()

    #this is only used for environment login (storefront,pxg1234) this is reason for hardcode :(
    def sendEnviornmentKeys(self):
       self.shell.Sendkeys("storefront")
       time.sleep(1)
       self.shell.Sendkeys("{TAB}")
       time.sleep(1)
       self.shell.Sendkeys("pxg1234")
       time.sleep(1)
       self.shell.Sendkeys("{ENTER}")


