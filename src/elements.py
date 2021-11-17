from dataclasses import dataclass, field
from typing import Optional
import datetime

@dataclass
class AulisElement:
    """ 
    Generic superclass for specific elements which are shown on the AULIS website.
    For example: Files, Folders and Courses. 
    """
    # Name/title of the element
    name: str
    # Optional description text
    description: str
    # URL to the element
    url: str

@dataclass
class File(AulisElement):
    """ This dataclass represents a file which is shown in an AULIS course, folder etc."""
    # Properties are file type, size, timestamp, number of pages.
    # Based on the AULIS HTML code, there is no easy way to distinguish these + they may differ for some files
    # NOTE: the getters may cause nasty bugs because we can never be sure that for example the first
    # element of the properties is always the file type etc.
    # Thus it is not recommended for something to strongly rely on these values!
    properties: list[str] # example: ["pdf", "32,7 KB", "08. Aug 2020, 15:59", "Anzahl Seiten: 1"]  TODO refactor this class to have each property as an attribute 

    def get_type(self) -> str:
        """ Returns the file type as a string"""
        return self.properties[0]
    
    def get_size(self) -> float:
        """" Returns the size of the file, estimated by AULIS """
        return float(self.properties[1])
    
    def get_date_of_last_modification(self) -> datetime:
        """ Returns the date of the last modification. Converts the AULIS time string to datetime. """
        # see strptime directives https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
        # AULIS uses the abbreviated name for months -> Jun == Juni
        return datetime.strptime(self.properties[2], "%d %b %Y %X").date()
    
    def get_name_with_ending(self) -> str:
        """ Returns the full file name i.e. 'python.pdf' """
        return "{file_name}.{file_type_ending}".format(file_name=self.name, file_type_ending=self.get_type())
    
    def get_numer_of_pages(self) -> int:
        """ Returns the number of pages if the file is of type pdf. """
        # only working for pdf files
        if self.get_type != "pdf":
            raise Warning("AULIS only displays the number of pages for pdf files! The return value of ths function might be empty!")
        # since there will only be a signle number in the string, we can use a filter
        return int("".join(filter(str.isdigit, self.properties[3])))

@dataclass
class Folder(AulisElement):
    """ This dataclass represents an AULIS folder which may have files and subfolders. """
    files: Optional[list[File]] = field(default_factory=list)
    folders: Optional[list["Folder"]] = field(default_factory=list)


@dataclass
class SyncElement(AulisElement): # TODO rename to course
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
