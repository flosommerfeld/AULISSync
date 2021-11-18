import os

def get_entrypoint():
    if os.path.exists(os.path.join(os.path.dirname(__file__), "index.html")):
        return os.path.join(os.path.dirname(__file__), "index.html")
        
    raise Exception('No index.html found')
