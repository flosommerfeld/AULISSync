from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys  
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
from dataclasses import dataclass, field
from typing import Optional, no_type_check_decorator

@dataclass
class AulisElement:
    # Name/title of the element
    name: str
    # Optional description text
    description: str
    # URL to the element
    url: str

@dataclass
class File(AulisElement):
    # Properties are file type, size, timestamp, number of pages.
    # Based on the AULIS HTML code, there is no easy way to distinguish these + they may differ for some files 
    properties: list[str]

@dataclass
class Folder(AulisElement):
    files: Optional[list[File]] = field(default_factory=list)
    subfolders: Optional[list["Folder"]] = field(default_factory=list)


@dataclass
class SyncElement(AulisElement):
    """ 
    A SyncElement is what will be synchronized. In AULIS this is usually 
    a course or group. Courses and groups are composed of files and folders which also
    may contain subfolders with files.
    """
    # Elements which are shown under the section 'Files' in AULIS.
    files: Optional[list[File]] = field(default_factory=list)
    # Elements which are shown under the section 'Folders' in AULIS
    # Folders may have subfolder or files.
    folders: Optional[list[Folder]] = field(default_factory=list)

def get_items(driver: WebDriver) -> list[AulisElement]:
    """
    Gets the AulisElements of a course or folder and returns them as a list.
    
    The items are identified by their images:
    File -> src="./Customizing/global/skin/Aulis_Hsb1/images/icon_file_inline.svg"
    Folder -> src="./Customizing/global/skin/Aulis_Hsb1/images/icon_fold.svg"
    Weblink -> src="./Customizing/global/skin/Aulis_Hsb1/images/icon_webr.svg"
    Survey -> src="./Customizing/global/skin/Aulis_Hsb1/images/icon_svy.svg"
    Learn materials -> src="./Customizing/global/skin/Aulis_Hsb1/images/icon_lm.svg"
    """
    result = []
    
    for item in driver.find_elements_by_class_name("ilListItemIcon"):
            # Get the url of the image/icon of the item
            image_url = item.get_attribute("src")
            # Find the parent element of the item
            grandparent = item.find_element_by_xpath("./../..")
            # Find alle titles of the item
            titles = grandparent.find_elements_by_class_name("il_ContainerItemTitle")
            # The last nested title is the one we are looking for
            # It contains the name of the item and also the link/url
            title = titles[-1]

            # Name and url of the item
            item_name = title.get_attribute("text")
            item_url = title.get_attribute("href")

            # Skip this element if id doesnt have an url. This most likely means that
            # the element is protected in AULIS and can't be read.
            if item_url is None:
                continue

            try:
                item_description = grandparent.find_elements_by_class_name("ilListItemSection il_Description")[0].get_attribute("text")
            except:
                item_description = ""

            # Detect items and convert to objects
            if "icon_file_inline.svg" in image_url:
                # get file properties
                properties = [prop.get_attribute("innerText") for prop in grandparent.find_elements_by_class_name("il_ItemProperty")]
                # add the File object to the courses files
                result.append(File(name=item_name, description=item_description, url=item_url, properties=properties))
                print("file")
            elif "icon_fold.svg" in image_url:
                result.append(Folder(name=item_name,description=item_description, url=item_url))
            elif "icon_webr.svg" in image_url:
                pass
            elif "icon_svy.svg" in image_url:
                pass
            elif "icon_lm.svg" in image_url:
                pass
            else:
                pass
    return result


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

    # Convert to SyncElements which hold the name and url to the element.
    # The description will be added later
    courses = [SyncElement(name=i.get_attribute("text"), description="", url=i.get_attribute("href")) for i in courses]

    my_objects = []
    for i in courses:
        # Visit the course/group and get the description, files and folders
        driver.get(i.url)

        wait = WebDriverWait(driver, 20)

        # Find the description and add it to the current object
        try:
            i.description = driver.find_elements_by_class_name("ilHeaderDesc")[0].get_attribute("text")
        except:
            i.description = ""

        # get items of the course and add them to the list
        for item in get_items(driver):
            # add files
            if type(item) is File:
                i.files.append(item)
            # add folders
            elif type(item) is Folder:
                i.folders.append(item)
            else:
                pass
        

        for folder in i.folders:
            driver.get(folder.url)
            wait = WebDriverWait(driver, 20)
            driver.execute_script("window.history.go(-1)")
            print("I just opened a folder")


        # Add the course to the course list
        my_objects.append(i)

        # Go back a page
        driver.execute_script("window.history.go(-1)")
    
    print(my_objects)

def get_all_folders(driver: WebDriver, folders: list[Folder]) -> list[Folder]:
    result = []
    
    for folder in folders:
        driver.get(folder.url)
        wait = WebDriverWait(driver, 20)
        driver.execute_script("window.history.go(-1)")

        # add files to the current folder <-------<
        # add folders to the current folder       ^
        # visit folders                           ^
        # repeat ---------------------------------^

        # search for files and add them to the folder


