import os

def get_entrypoint():
    """ Returns the entrypoint/main html file of the gui """
    if os.path.exists(os.path.join(os.path.dirname(__file__), "index.html")):
        return os.path.join(os.path.dirname(__file__), "index.html")
        
    raise Exception('No index.html found')


class Api():
    """ Python API which is callable from JavaScript """
    
    def handleButton(self):
        print("The button in the frontend was clicked!")
