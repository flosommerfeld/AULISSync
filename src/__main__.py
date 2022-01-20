import webview
from gui.api import get_entrypoint, Api


if __name__ == '__main__':
    # instantiate api for the frontend
    api = Api()
    
    # start the gui window loop
    webview.create_window("AulisSync", get_entrypoint(), js_api=api)
    webview.start(debug=True)
