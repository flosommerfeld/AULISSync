import globals
from gui import gui_loop

if __name__ == '__main__':
    # loads the saved data and makes it globally available -> User data
    globals.load_saved_data()
    # start the gui window loop
    gui_loop()
