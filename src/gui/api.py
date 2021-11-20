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
    
    def synchronizeCourses(self):
        """ Triggers the synchronization of the users courses """
        storage.user.synchronize()

    def loginUser(self, username, password):
        """ Creates a new temporary user instance and tries to login via selenium. If the login was successful the global user will be updated """
        if User(username, password).login():
            # update credentials of the global user if the login was successful
            # the global user will be saved via the storage
            storage.user = User(username, password, logged_in=True)
            return True
        
        return False

    def logoutUser(self):
        """ Logs out the user by setting the user instance to None """
        storage.user = None

    def isUserLoggedIn(self):
        """ Checks whether the stored user has successfully logged in the last time and return a bool """
        return storage.user.logged_in
    
    def getUsername(self):
        """ Returns the username of the currently logged in user """
        return storage.user.username
