import os

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
