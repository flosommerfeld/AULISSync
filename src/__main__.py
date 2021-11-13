from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys  
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep

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


    # Nach dem Einloggen sollte man auf: https://aulis.hs-bremen.de/ilias.php?baseClass=ilDashboardGUI&cmd=jumpToSelectedItems sein

    # class ilDashboardMainContent beinhaltet alle il-item-title -> child <a> hat link
    
    # after the login we are being redirected, so we are waiting until the
    # dashboard is shown
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.visibility_of_element_located((By.ID, "il_mhead_t_focus")))


    if element.get_attribute("text") == "Dashboard":
        print("we are on the dashboard!")
    else:
        print(element.get_attribute("text"))
    
    # get elements which hold the courses
    content = driver.find_element_by_class_name("ilDashboardMainContent")
    courseElements = content.find_elements_by_class_name("il-item-title")
 
    # iterate over the courses to get their names etc.
    courses = [course.find_element_by_tag_name("a") for course in courseElements]
    
    # convert to set in order to remove duplicates
    courses = list(set(courses))

    courses_links = [course.get_attribute("href") for course in courses]

    # print the courses/elements which were found
    print([i.get_attribute("text") for i in courses])

    for link  in courses_links:
        print("click")
        driver.get(link)
        wait = WebDriverWait(driver, 20)
        driver.execute_script("window.history.go(-1)")
        wait = WebDriverWait(driver, 20)
    #driver.close()
