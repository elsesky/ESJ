from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import copy
from time import sleep
desired_capabilities = copy.deepcopy(DesiredCapabilities.CHROME)
desired_capabilities["pageLoadStrategy"] = "none"
options = webdriver.ChromeOptions()
options.binary_location = "D:\\Program Files\\Twinkstar Browser\\chrome.exe"
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options,desired_capabilities = desired_capabilities)
r = driver.get("https://www.esjzone.cc/forum/1580565850/112935.html")
time.sleep(6)
content = driver.page_source
print content.encode('UTF-8')


--headless --disable-dev-shm-usage --no-sandbox