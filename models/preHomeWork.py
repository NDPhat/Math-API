from pydantic import BaseModel
from typing import List

class PreHomeWork(BaseModel):
    week: str
    numQ: int
    sign: List[str] = []
    sNum : int
    eNum : int
    dstart:str
    dend:str
    status:str
    color:str
    lop:str
class PreHomeWorkUpdate(BaseModel):
    week: str=None
    numQ: int=None
    sign: List[str] = []
    numQ: int=None
    sNum : int=None
    eNum : int=None
    dstart:str=None
    dend:str=None
    status:str=None
    color:str=None
    lop:str=None

