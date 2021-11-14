from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, pickle
from time import sleep
from dataclasses import dataclass, field
from typing import Optional

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
    folders: Optional[list["Folder"]] = field(default_factory=list)


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

def get_items(driver: WebDriver, url: str) -> list[AulisElement]:
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

    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
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

def get_course_elements(driver, url, toplevel_element):
    """ 
    Recursive function which get all of the courses elements (files, oflder etc) 
    The toplevel_element is the element which contains the added files and folders.
    In the recursion call, the toplevel element will be changed to a new sub toplevel element:
    For example: Item 'Mathematics' has a folder named 'Calculus'. This folder will be added to the 
    top level element mathematics. Then we go into the calculus folder and see other files and folders.
    These will be added to calculus, the new topl level element.
    """
    # get items of the course and add them to the list
    for item in get_items(driver, url):
        # add files
        if type(item) is File:
            toplevel_element.files.append(item)
        # add folders
        elif type(item) is Folder:
            toplevel_element.folders.append(item)
            # For every subitem get in the folder, get the files and folders and add them like above
            for subitem in get_items(driver, item.url):
                # TODO Prevent calling a file bug
                if type(subitem) is Folder:
                    toplevel_element.folders.append(subitem)
                    get_course_elements(driver, subitem.url, subitem)
                elif type(item) is File:
                    toplevel_element.files.append(subitem)
                else:
                    pass
        else:
            pass

def pickle_courses(courses: list[SyncElement], file_name: str):
    """ Creates a pickle byte file which holds the courses """
    # create a pickle file
    file = open(file_name, "wb")
    # pickle the list and write it to file
    pickle.dump(courses, file)
    # close the file
    file.close()

def unpickle_courses(file_name: str) -> list[SyncElement]:
    """ 
    Loads the pickle byte file and converts the data back to python objects.
    Returns a list of the courses. 
    """
    # read the pickle file
    file = open(file_name, "rb")
    # unpickle the dataframe
    synced_elements = pickle.load(file)
    # close fthe ile
    file.close()
    return synced_elements


def login():
    """
    Opens the AULIS login page and enters the login credentials which are currently
    being provided by the env vars.
    """
    # Visit the login page
    driver.get("https://aulis.hs-bremen.de/saml.php?returnTo=")

    # Find the username input field and insert the username
    username_input_elem = driver.find_element_by_id("username")
    username_input_elem.clear()
    username_input_elem.send_keys(os.getenv("AULIS_USERNAME")) # TODO get from config etc.

    # Find the password input field and insert the password
    password_input_elem = driver.find_element_by_id("password")
    password_input_elem.clear()
    password_input_elem.send_keys(os.getenv("AULIS_PASSWORD"))

    # Login via RETURN key
    password_input_elem.send_keys(Keys.RETURN)

    # wait until we are redirected after the login
    wait = WebDriverWait(driver, 20)
    heading = wait.until(EC.visibility_of_element_located((By.ID, "il_mhead_t_focus")))
    
    # raise exception if the new page is not the dashboard
    if "Dashboard" not in heading.get_attribute("text"):
        raise Exception


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

    # Login the user
    login()
    
    # get elements which hold the courses
    content = driver.find_element_by_class_name("ilDashboardMainContent")
    courseElements = content.find_elements_by_class_name("il-item-title")
 
    # iterate over the courses to get their names etc.
    courses = [course.find_element_by_tag_name("a") for course in courseElements]
    
    # convert to set in order to remove duplicates
    courses = list(set(courses))

    # TODO remove courses where the user doesn't want to sync them

    # Convert to SyncElements which hold the name and url to the element.
    # The description will be added later
    courses = [SyncElement(name=i.get_attribute("text"), description="", url=i.get_attribute("href")) for i in courses]

    my_objects = []

    # Iterate over all of the courses and get the nested data: description, files and folders
    for i in courses:
        # Visit the course/group 
        driver.get(i.url)
        wait = WebDriverWait(driver, 20)

        # Find the description and add it to the current object
        try:
            i.description = driver.find_elements_by_class_name("ilHeaderDesc")[0].get_attribute("text")
        except:
            i.description = ""

        # Get all the files and folders of the current course
        get_course_elements(driver, url=i.url, toplevel_element=i)
        
        # Add the course to the course list
        my_objects.append(i)

        # Go back a page
        driver.execute_script("window.history.go(-1)")
    
    print(my_objects)

    old_sync_courses = None
    # Open the pickled data from the last session
    try:
        old_sync_courses = unpickle_courses("oldSyncData")
    except:
        print("Something went wrong while unpickleing!")
    
    # Save the courses to a pickle file
    pickle_courses(my_objects, "oldSyncData")

    # compare old pickled objects with the new ones
    for course in my_objects:
        if not course in old_sync_courses:
            print("This course is probably out of data -> needs to be synced")
        else:
            print("This course is up to date.")
    
    

def _driver_go_back(driver):
    """ Goes to the last page in history """
    # ran via JavaScript so it doesn't really refresh the page
    driver.execute_script("window.history.go(-1)")