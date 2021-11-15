from dataclasses import dataclass, field
from typing import Optional

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
    properties: list[str]

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
