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
import PySimpleGUI as sg
from psgtray import SystemTray


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

@dataclass
class User:
    """
    The class User represents the user of the application.
    """
    username: str
    password_hash: str
    synced_elements: Optional[list[SyncElement]] = None

    def update(self, username, password):
        """ Updates the credentials of the user. Arguments are optional. """
        if username:
            self.username = username
        if password:
            self.password_hash = password # TODO encrypt
    
    def login(self):
        """ 
        Logs in the user with the current or passed credentials.
        This will call selenium in order to open the authentication procedure.
        """
        # Raise an exception if the credentials are not set
        if not(self.username and self.password_hash):
            raise Exception
        
        # Authenticate the user via selenium
        try:
            SeleniumIliasWrapper().login(username=self.username, password=self.password_hash)
        except:
            return False
        else:
            return True


class Storage:
    """ The Storage is used for writing and loading of data via 'pickle' """

    _pickle_file = "localData.pickle"

    @property
    def user(self) -> User:
        # read the pickle file
        file = open(self._pickle_file, "rb")
        # unpickle the dataframe
        user = pickle.load(file)
        # close fthe ile
        file.close()
        return user

    @user.setter
    def user(self, new_user: User):
         # create a pickle file
        file = open(self._pickle_file, "wb")
        # pickle the list and write it to file
        pickle.dump(new_user, file)
        # close the file
        file.close()
    
    @property
    def synced_elements(self) -> list[SyncElement]:
        return self.user.synced_elements
    
    @synced_elements.setter
    def synced_elements(self, new_synced_elements: list[SyncElement]):
        new_user = self.user
        new_user.synced_elements = new_synced_elements
        self.user = new_user


class SeleniumIliasWrapper:
    # TODO change options based on selected/detected browser
    firefox_options = Options()  
    #firefox_options.add_argument("--headless") 
    # TODO put into Driver class
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub', # TODO put into config.py
        options=firefox_options,
        desired_capabilities=DesiredCapabilities.FIREFOX.copy()
    )

    def get_items(self, url: str) -> list[AulisElement]:
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

        self.driver.get(url)
        wait = WebDriverWait(self.driver, 20)
        
        for item in self.driver.find_elements_by_class_name("ilListItemIcon"):
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

    def get_course_elements(self, url, toplevel_element):
        """ 
        Recursive function which get all of the courses elements (files, oflder etc) 
        The toplevel_element is the element which contains the added files and folders.
        In the recursion call, the toplevel element will be changed to a new sub toplevel element:
        For example: Item 'Mathematics' has a folder named 'Calculus'. This folder will be added to the 
        top level element mathematics. Then we go into the calculus folder and see other files and folders.
        These will be added to calculus, the new topl level element.
        """
        # get items of the course and add them to the list
        for item in self.get_items(self.driver, url):
            # add files
            if type(item) is File:
                toplevel_element.files.append(item)
            # add folders
            elif type(item) is Folder:
                toplevel_element.folders.append(item)
                # For every subitem get in the folder, get the files and folders and add them like above
                for subitem in self.get_items(self.driver, item.url):
                    # TODO Prevent calling a file bug
                    if type(subitem) is Folder:
                        toplevel_element.folders.append(subitem)
                        self.get_course_elements(self.driver, subitem.url, subitem)
                    elif type(item) is File:
                        toplevel_element.files.append(subitem)
                    else:
                        pass
            else:
                pass

    def login(self, username: str, password: str):
        """
        Opens the AULIS login page and enters the login credentials which are currently
        being provided by the env vars.
        """
        # Visit the login page
        self.driver.get("https://aulis.hs-bremen.de/saml.php?returnTo=")

        # Find the username input field and insert the username
        username_input_elem = self.driver.find_element_by_id("username")
        username_input_elem.clear()
        username_input_elem.send_keys(username) # TODO get from config etc.

        # Find the password input field and insert the password
        password_input_elem = self.driver.find_element_by_id("password")
        password_input_elem.clear()
        password_input_elem.send_keys(password)

        # Login via RETURN key
        password_input_elem.send_keys(Keys.RETURN)

        # wait until we are redirected after the login
        wait = WebDriverWait(self.driver, 20)
        heading = wait.until(EC.visibility_of_element_located((By.ID, "il_mhead_t_focus")))
        
        # raise exception if the new page is not the dashboard
        # This can also mean that the authentication was not successful
        if "Dashboard" not in heading.get_attribute("text"):
            raise Exception

    def pickle_courses(self, courses: list[SyncElement], file_name: str):
        """ Creates a pickle byte file which holds the courses """
        # create a pickle file
        file = open(file_name, "wb")
        # pickle the list and write it to file
        pickle.dump(courses, file)
        # close the file
        file.close()

    def unpickle_courses(self, file_name: str) -> list[SyncElement]:
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
            
    def synchronize(self):
        # Login the user
        self.login(os.getenv("AULIS_USERNAME"), os.getenv("AULIS_PASSWORD"))
        
        # get elements which hold the courses
        content = self.driver.find_element_by_class_name("ilDashboardMainContent")
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
            self.driver.get(i.url)
            wait = WebDriverWait(self.driver, 20)

            # Find the description and add it to the current object
            try:
                i.description = self.driver.find_elements_by_class_name("ilHeaderDesc")[0].get_attribute("text")
            except:
                i.description = ""

            # Get all the files and folders of the current course
            self.get_course_elements(self.driver, url=i.url, toplevel_element=i)
            
            # Add the course to the course list
            my_objects.append(i)

            # Go back a page
            self.driver.execute_script("window.history.go(-1)")
        
        print(my_objects)

        old_sync_courses = None
        # Open the pickled data from the last session
        try:
            old_sync_courses = self.unpickle_courses("oldSyncData")
        except:
            print("Something went wrong while unpickleing!")
        
        # Save the courses to a pickle file
        self.pickle_courses(my_objects, "oldSyncData")

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


def main():
    menu = ['', ['Show Window', 'Hide Window', '---', '!Disabled Item', 'Change Icon', ['Happy', 'Sad', 'Plain'], 'Exit']]
    tooltip = 'Tooltip'

    layout = [[sg.Text('My PySimpleGUI Celebration Window - X will minimize to tray')],
              [sg.T('Double clip icon to restore or right click and choose Show Window')],
              [sg.T('Icon Tooltip:'), sg.Input(tooltip, key='-IN-', s=(20,1)), sg.B('Change Tooltip')],
              [sg.Multiline(size=(60,10), reroute_stdout=False, reroute_cprint=True, write_only=True, key='-OUT-')],
              [sg.Button('Go'), sg.B('Hide Icon'), sg.B('Show Icon'), sg.B('Hide Window'), sg.Button('Exit')]]

    window = sg.Window("IliasSync", layout, finalize=True, enable_close_attempted_event=True)


    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon=sg.DEFAULT_BASE64_ICON)
    sg.cprint(sg.get_versions())
    while True:
        event, values = window.read()

        # IMPORTANT step. It's not required, but convenient. Set event to value from tray
        # if it's a tray event, change the event variable to be whatever the tray sent
        if event == tray.key:
            sg.cprint(f'System Tray Event = ', values[event], c='white on red')
            event = values[event]       # use the System Tray's event as if was from the window

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        sg.cprint(event, values)

        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()

            # TODO try logging in the user
            user = User(os.getenv("AULIS_USERNAME"), os.getenv("AULIS_PASSWORD"))
            if user.login():
                sg.cprint("We successfully logged in")
            else:
                sg.cprint("Login was not successfull, please check your password")
                
        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()        # if hiding window, better make sure the icon is visible
            # tray.notify('System Tray Item Chosen', f'You chose {event}')
        elif event == 'Happy':
            tray.change_icon(sg.EMOJI_BASE64_HAPPY_JOY)
        elif event == 'Sad':
            tray.change_icon(sg.EMOJI_BASE64_FRUSTRATED)
        elif event == 'Plain':
            tray.change_icon(sg.DEFAULT_BASE64_ICON)
        elif event == 'Hide Icon':
            tray.hide_icon()
        elif event == 'Show Icon':
            tray.show_icon()
        elif event == 'Change Tooltip':
            tray.set_tooltip(values['-IN-'])

    tray.close()            # optional but without a close, the icon may "linger" until moused over
    window.close()


if __name__ == '__main__':
    main()
