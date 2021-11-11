from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys  
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import os

if __name__ == '__main__':
    # TODO change options based on selected/detected browser
    firefox_options = Options()  
    #firefox_options.add_argument("--headless") 

    # TODO put into Driver class
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub', # TODO put into config.py
        options=firefox_options,
        desired_capabilities=DesiredCapabilities.FIREFOX.copy()
    )

    driver.get("https://aulis.hs-bremen.de/saml.php?returnTo=")
    
    # TODO put into login() etc.
    username_input_elem = driver.find_element_by_id("username")
    username_input_elem.clear()
    username_input_elem.send_keys(os.getenv("AULIS_USERNAME")) # TODO get from config etc.

    password_input_elem = driver.find_element_by_id("password")
    password_input_elem.clear()
    password_input_elem.send_keys(os.getenv("AULIS_PASSWORD"))
    password_input_elem.send_keys(Keys.RETURN)

    #driver.close()
