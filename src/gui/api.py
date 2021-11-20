import os
from user import User
from globals import get_current_user


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
    
    def handleButton(self):
        print("The button in the frontend was clicked!")

    def loginUser(self, username, password):
        """ Creates a new temporary user instance and tries to login via selenium. If the login was successful the global user will be updated """
        if User(username, password).login():
            # update credentials of the global user if the login was successful
            # the global user will be saved via the storage
            get_current_user().update_credentials(username, password) 
            return True
        
        return False

    def isUserLoggedIn(self):
        """ Checks whether the stored user has successfully logged in the last time and return a bool """
        return True
        #return get_current_user().logged_in
