from pydantic import BaseModel
from typing import List

class PrePractice(BaseModel):
    userId: str
    sign: str
    optionGame: str
    dateSave:str
    numQ: int=None
    score:int=None
    status:str
 
class PrePracticeUpdate(BaseModel):
    userId: str=None
    sign: str=None
    optionGame: str=None
    dateSave:str=None
    numQ: int=None
    score:int=None
    status:str=None
