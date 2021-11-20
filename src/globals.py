from storage import Storage
from user import User, Settings

def load_saved_data():
    """ Loads the saved data via a Storage object and makes the storage and the user globally available """
    # global storage instance
    global storage
    storage = Storage()
    
    # load user data and make it globally available
    global user
    try:
        user = storage.user
    except Exception:
        # if the user couldn't be read, create a new one
        user = storage.user = User("", "", Settings())

def get_current_user() -> User:
    return user
