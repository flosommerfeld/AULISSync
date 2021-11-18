from logging import debug
import globals
import webview
from gui.api import get_entrypoint
import codecs



if __name__ == '__main__':
    # loads the saved data and makes it globally available -> User data
    globals.load_saved_data()
    # start the gui window loop
    #gui_loop()
    webview.create_window("AulisSync", get_entrypoint())
    webview.start(debug=True)
