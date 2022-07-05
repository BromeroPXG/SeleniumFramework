from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pytest
from selenium.webdriver.chrome.options import Options
from configurations.config import TestData
import chromedriver_autoinstaller


# this creates the global fixture and confidence test to launching the driver
# can be chrome or firefox

# install the correct driver managers based on browser selection
# this eliminates the need for hardcoded driver file
@pytest.fixture(params=["chrome"], scope='class')
def init_driver(request):
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("detach", True)
    if request.param == "chrome":
        chromedriver_autoinstaller.install()  # no more hardcoded chromedriver .exe
        web_driver = webdriver.Chrome(options=chrome_options)
    if request.param == "firefox":
        web_driver = webdriver.Chrome(GeckoDriverManager().install())
    request.cls.driver = web_driver
    yield
