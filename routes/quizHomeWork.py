from fastapi import APIRouter
from models.quizHomeWork import QuizHomeWorkDetail
from fastapi.responses import JSONResponse
from deta import Deta 

quizHW = APIRouter() 
deta = Deta("c01JK2yDofss_kB5xE7hNU5F2CE8a8gSHz93mxqc6yzZg")
# This how to connect to or create a database.
db = deta.Base("quiz_hw_db")
class QuizHWDetail :
    @quizHW.post('/create_quiz_detail')
    def create_Quiz_HW_Detail(quiz: QuizHomeWorkDetail):
        try:   
            db.put(quiz.dict())       
            return JSONResponse({"message":"insert thanh cong"},status_code=200) 
        except Exception:
            return JSONResponse({"message":"loi"},status_code=404)
    
    @quizHW.get('/getAllQuizHWByResultID')
    def get_Quiz_HW_ByResultID(resultID:str):
        preQ=db.fetch([{"resultHWID": resultID}]) 
        if preQ:      
            return preQ
        return JSONResponse({"message":"data not found"},status_code=404)
    
    
    @quizHW.get('/getAllQuizHWByResultIDWithPagi')
    def get_Quiz_HW_ByResultID_With_Pagi(resultID:str,page_num : int = 1, page_size : int =10):
        data=db.fetch([{"resultHWID": resultID}]) 
        start =(page_num -1) * page_size
        end =start +page_size
        response = {
            "data":data.items[start:end],
            "total":data.count,
            "count":page_size,
        }
        if(response) :
            return response
        return JSONResponse({"message":"data not found"},status_code=404)
