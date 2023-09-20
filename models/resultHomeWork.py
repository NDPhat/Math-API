from pydantic import BaseModel

class ResultHomeWork(BaseModel):
    week: str
    numQ: int
    name:str
    userId:str
    score:int
    trueQ:int
    falseQ:int
    lop:str
    dateSave:str
    status:str

  
class ResultHomeWorkUpdate(BaseModel):
    week: str= None
    numQ: int= None
    name:str=None
    userId: str= None
    score : int= None
    trueQ:int=None
    falseQ:int=None
    lop:str=None
    dateSave:str=None
    status:str=None

   

   