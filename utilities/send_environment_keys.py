import win32com.client
import time

class send_keys:
    # this is the send sandbox keys class
    shell = win32com.client.Dispatch("WScript.Shell")
    def __init__(self):
        return

    def send_env_keys(self):
        self.shell.Sendkeys("storefront")
        time.sleep(1)
        self.shell.Sendkeys("{TAB}")
        time.sleep(1)
        self.shell.Sendkeys("pxg1234")
        time.sleep(1)
        self.shell.Sendkeys("{ENTER}")
        time.sleep(3)

