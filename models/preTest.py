from pydantic import BaseModel

class PreTest(BaseModel):
    numQ:int
    score:int
    trueQ:int
    userId:str
    falseQ:int
    dateSave:str
    status:str

   
class PreTestUpdate(BaseModel):
    numQ:int=None
    score:int=None
    trueQ:int=None
    userId:str=None
    falseQ:int=None
    dateSave:str=None
    status:str=None

