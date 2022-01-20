import os
from user import User
from storage import Storage

storage = Storage()


def get_entrypoint():
    """ Returns the entrypoint/main html file of the gui """
    
    def get_path(path):
        """ Returns the joined path if it exists. None if it doesnt. """
        if os.path.exists(os.path.join(os.path.dirname(__file__), path)):
            return os.path.join(os.path.dirname(__file__), path)
   
    index_file = get_path("../../public/dist/index.html")
    if index_file: return index_file
        
    raise Exception('No index.html found')



class Api():
    """ Python API which is callable from JavaScript """
    def __init__(self):
        self.recent_selenium_aulis_login = False
    
    def getCourses(self):
        """ Returns a list of all course names. This will trigger Selenium to analyze the present courses. """
        return [str(course.name) for course in storage.user.get_courses()] # TODO is it even possible send str lists to js?

    def synchronizeCourses(self):
        """ Triggers the synchronization of the users courses """
        storage.user.synchronize()

    def loginUser(self, username=None, password=None):
        """ Creates a new temporary user instance and tries to login via selenium. If the login was successful the global user will be updated """
        if User(username, password).login():
            # update credentials of the global user if the login was successful
            # the global user will be saved via the storage
            storage.user = User(username, password, logged_in=True)
            # toggle the login flag
            self.recent_selenium_aulis_login
            return True
        
        return False

    def loginAuthenticatedUserToAulis(self):
        """ Logs in the current user into AULIS via Selenium """
        # NOTE: by using the stored credentials we can login without knowing the password in the gui
        return storage.user.login()

    def logoutUser(self):
        """ Logs out the user by setting the user instance to None """
        storage.user = None

    def isUserLoggedIn(self):
        """ Checks whether the stored user has successfully logged in the last time and return a bool """
        try:
            # If there is a saved user then return the login flag
            if(storage.user):
                return storage.user.logged_in
        except:
            # return False if a saved user was not found
            return False
    
    def isUserLoggedIntoAulis(self):
        """ Returns true if the user has recently signed into AULIS by clicking the login button on the gui """
        return self.recent_selenium_aulis_login
    
    def getUsername(self):
        """ Returns the username of the currently logged in user """
        return storage.user.username
