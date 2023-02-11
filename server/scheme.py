from pydantic import BaseModel, Field
from typing import List
class child_url(BaseModel):
    type : str = Field(
        "url"
    )
    id : int = Field(
        2
    )
    index : int = Field(
        0
    )
    url : str = Field(
        "https://www.googld.com"
    )
    title : str = Field(
        "Google"        
    )
    date_added : int = Field(
        0        
    )
    icon : str = Field(
        None
    )
    iconuri : str = Field(
        None
    )
    tags : str = Field(
        None
    )

class api_scheme(BaseModel):
    type : str = Field(
        "folder"
    )
    id : int = Field(
        1
    )
    index : int = Field(
        0
    )
    title : str = Field(
        "Main Folder" 
    )
    date_added : int = Field(
        "0"
    )

    children : child_url = Field(
        None
    )