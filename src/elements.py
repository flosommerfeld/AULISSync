from dataclasses import dataclass, field
from typing import Optional
import datetime

@dataclass
class AulisElement:
    # Name/title of the element
    name: str
    # Optional description text
    description: str
    # URL to the element
    url: str

@dataclass
class File(AulisElement):
    # Properties are file type, size, timestamp, number of pages.
    # Based on the AULIS HTML code, there is no easy way to distinguish these + they may differ for some files
    # NOTE: the getters may cause nasty bugs because we can never be sure that for example the first
    # element of the properties is always the file type etc.
    # Thus it is not recommended for something to strongly rely on these values!
    properties: list[str] # example: ["pdf", "32,7 KB", "08. Aug 2020, 15:59", "Anzahl Seiten: 1"]  

    def get_type(self) -> str:
        return self.properties[0]
    
    def get_size(self) -> float:
        return float(self.properties[1])
    
    def get_date_of_last_modification(self) -> datetime:
        # see strptime directives https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
        # AULIS uses the abbreviated name for months -> Jun == Juni
        return datetime.strptime(self.properties[2], "%d %b %Y %X").date()
    
    def get_name_with_ending(self) -> str:
        return "{file_name}.{file_type_ending}".format(file_name=self.name, file_type_ending=self.get_type())

@dataclass
class Folder(AulisElement):
    files: Optional[list[File]] = field(default_factory=list)
    folders: Optional[list["Folder"]] = field(default_factory=list)


@dataclass
class SyncElement(AulisElement):
    """ 
    A SyncElement is what will be synchronized. In AULIS this is usually 
    a course or group. Courses and groups are composed of files and folders which also
    may contain subfolders with files.
    """
    # Elements which are shown under the section 'Files' in AULIS.
    files: Optional[list[File]] = field(default_factory=list)
    # Elements which are shown under the section 'Folders' in AULIS
    # Folders may have subfolder or files.
    folders: Optional[list[Folder]] = field(default_factory=list)
