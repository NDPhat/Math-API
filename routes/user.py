from fastapi import APIRouter
from models.user import UserUpdate
from models.resultHomeWork import ResultHomeWorkUpdate
from fastapi.responses import JSONResponse
from deta import Deta 
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
import random
import smtplib
from email.mime.text import MIMEText
from routes.preTest import PreTest
from routes.prePractice import PrePra
from routes.resultHomeWork import ResultHW


user = APIRouter() 

deta = Deta("c01JK2yDofss_kB5xE7hNU5F2CE8a8gSHz93mxqc6yzZg")
# This how to connect to or create a database.
db = deta.Base("user_db")

@user.post('/create_user')
def create_user(user: UserUpdate):
    db.put(user.dict())
    return JSONResponse({"message":"insert thanh cong"},status_code=200)

@user.get('/getListUser')
def get_List_User():
    res = db.fetch()
    all_items = res.items
    while res.last:
        res = db.fetch(last=res.last)
        all_items += res.items
    return all_items
@user.get('/getListUserWithPagination')
def get_List_User_With_Pagination(page_num : int = 1, page_size : int =10):
    all_items = db.fetch()
    start =(page_num -1) * page_size
    end =start +page_size
    response = {
        "data":all_items.items[start:end],
        "total":all_items.count,
        "count":page_size,
    }
    return response
@user.get('/getListUserByClass')
def get_List_User_By_Class(lop:str):
    res=db.fetch([{"lop": lop,"role":"user"}]) 
    return res
@user.get('/getListUserByClassPagination')
def get_List_User_By_Class_With_Pagination(lop:str,page_num : int = 1, page_size : int =5):
    all_items=db.fetch([{"lop": lop,"role":"user"}]) 
    start =(page_num -1) * page_size
    end =start +page_size
    response = {
        "data":all_items.items[start:end],
        "total":all_items.count,
        "count":page_size,
    }
    return response
@user.get('/getUserById')
def get_User_ByID(uId:str):
    user=db.get(uId)      
    if user:      
        return user
    return JSONResponse({"message":"user not found"},status_code=404)
@user.get('/getUserByEmail')
def get_User_ByEmail(email:str):
    user=db.fetch([{"email": email}],limit=1) 
    if user:      
        return user
    return JSONResponse({"message":"user not found"},status_code=404)

@user.get('/checkOTPCode')
def check_otp_code(email:str,otp:str):
    user=db.fetch([{"email": email,"otpCode": otp}],limit=1) 
    if user:      
        return user
    return JSONResponse({"message":"user not found"},status_code=404)

@user.get('/getUserByEmailAndPassword')
def get_User_ByEmail_Password(email:str,password:str):
    user=db.fetch([{"email": email,"password": password}],limit=1) 
    if user:      
        return user
    return JSONResponse({"message":"user not found"},status_code=404)

@user.delete('/deleteUserById')
def delete_user(id):
    db.delete(id)
    PreTest.delete_All_PreQ_Test_ByUID(userID=id)
    PrePra.delete_All_PreQ_Game_ByUID(userID=id)
    return JSONResponse({"message":"delete done"},status_code=200)


@user.patch('/updateUserById')
def update_User_ById(id: str,user : UserUpdate):
    updates={k:v for k,v in user.dict().items() if v is not None}
    db.update(updates,id)
    ResultHW.update_All_ResultQuizHW_ByUId(userId=id,resultUpdate=ResultHomeWorkUpdate(name=user.fullName))
    return db.get(id)


@user.patch('/updateUserByEmail')
def update_User_ByEmail(email: str,user : UserUpdate): 
    response=db.fetch([{"email": email}],limit=1) 
    if response.count!=0 :  
        keyID = response.items[0]["key"]
        updates={k:v for k,v in user.dict().items() if v is not None}
        db.update(updates,keyID)
        return db.get(keyID)
    else :
        return JSONResponse({"message":"update loi"},status_code=404)


@user.get('/forgetPassWordAndGetOTP')
def send__otp_to_email(email :str):
    user=db.fetch([{"email": email}],limit=1) 
    if user.count!=0:
        n = random.randint(10000,50000)
        update_User_ByEmail(email=email,user=UserUpdate(otpCode=str(n)))
        msg = MIMEText('This is an RESET PASSWORD email send from MATHEZ!! \nYour OTP CODE is '+str(n)) 
        msg['Subject'] = 'Cap nhat mat khau tren MathEZ'
        msg['From'] = 'daiphatcbl@gmail.com'
        msg['To'] = (email)
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login('daiphatcbl@gmail.com', 'lvnvyxjxybnsrnhr')
        smtp_server.sendmail('daiphatcbl@gmail.com', email, msg.as_string())
        smtp_server.quit()    
        return user
    return JSONResponse({"message":"user not found"},status_code=404)
        

@user.get('/sendTextToPhone')
def send_text_to_phone(phone :str,mess:str):


    # Your Twilio account SID and auth token
    account_sid = 'AC5f0543b5dd90a8d6b7db37024f0cdb27'
    auth_token = '79b2213c305703aa88819d31091301f8'

    # The Twilio phone number that you want to use for sending messages
    from_phone_number = '+13203773621'

    # The phone number that you want to send the message to
    to_phone_number = phone

    # The message that you want to send

    # Create a Twilio client object
    client = Client(account_sid, auth_token)

    # Use the Twilio client to send a text message
    message = client.messages \
    .create(
        body=mess,
        from_=from_phone_number,
        to=  to_phone_number
    )
    return JSONResponse({"message":"send thanh cong"},status_code=202)
