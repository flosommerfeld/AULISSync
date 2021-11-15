from user import User
import pickle
from elements import SyncElement

class Storage:
    """ The Storage is used for writing and loading of data via 'pickle' """

    _pickle_file = "localData.pickle"

    @property
    def user(self) -> User:
        # read the pickle file
        file = open(self._pickle_file, "rb")
        # unpickle the dataframe
        user = pickle.load(file)
        # close fthe ile
        file.close()
        return user

    @user.setter
    def user(self, new_user: User):
         # create a pickle file
        file = open(self._pickle_file, "wb")
        # pickle the list and write it to file
        pickle.dump(new_user, file)
        # close the file
        file.close()
    
    @property
    def synced_elements(self) -> list[SyncElement]:
        return self.user.synced_elements
    
    @synced_elements.setter
    def synced_elements(self, new_synced_elements: list[SyncElement]):
        new_user = self.user
        new_user.synced_elements = new_synced_elements
        self.user = new_user
