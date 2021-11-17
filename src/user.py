from elements import SyncElement
from dataclasses import dataclass
from typing import Optional
from aulis_interaction import SeleniumIliasWrapper
from pathlib import Path
import datetime


_wrapper = SeleniumIliasWrapper()

@dataclass
class Settings:
    """ Represents the settings a user can make in the GUI """
    ELEMENTS_TO_SYNC: Optional[list[SyncElement]] = None
    SYNC_DESTINATION: Optional[Path] = Path(__file__).parent # use the root project directory as default


@dataclass
class User:
    """
    The class User represents the user of the application.
    """
    username: str
    password_hash: str
    settings: Optional[Settings] = None
    synced_elements: Optional[list[SyncElement]] = None
    # The last time the user has synchronized his AULIS courses
    last_sync_action: datetime = None

    def update_credentials(self, username, password):
        """ Updates the credentials of the user. Arguments are optional. """
        if username:
            self.username = username
        if password:
            self.password_hash = password # TODO encrypt
    
    def login(self):
        """ 
        Logs in the user with the current or passed credentials.
        This will call selenium in order to open the authentication procedure.
        """
        # Raise an exception if the credentials are not set
        if not(self.username and self.password_hash):
            raise Exception
        
        # Authenticate the user via selenium
        try:
            _wrapper.login(username=self.username, password=self.password_hash)
        except:
            return False
        else:
            return True
    
    # TODO sync options -> only sync specific courses etc. 
    def synchronize(self):
        # Raise an exception if the credentials are not set
        if not(self.username and self.password_hash):
            raise Exception
        
        # Sync AULIS
        try:
            self.synced_elements = _wrapper.synchronize()
        except Exception as e:
            self.synced_elements = []
            print(e.__traceback__)
        finally:
            return self.synced_elements
