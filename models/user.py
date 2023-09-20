from pydantic import BaseModel

class User(BaseModel):
    fullName: str
    email: str
    password: str
    lop : str
    otpCode:str
    address:str
    sex:str
    birthDay:str
    linkImage:str
    deleteHash:str =None
    phone:str
    role:str
   
    
class UserUpdate(BaseModel):
    fullName: str= None
    email: str= None
    password: str= None
    lop : str= None
    otpCode : str=None
    address:str=None
    deleteHash:str =None
    phone:str=None
    sex:str=None
    linkImage:str=None
    birthDay:str=None
    role:str=None
    

   