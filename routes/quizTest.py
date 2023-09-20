from fastapi import APIRouter
from models.quizTest import QuizTest
from fastapi.responses import JSONResponse
from deta import Deta 

quizTest = APIRouter() 
deta = Deta("c01JK2yDofss_kB5xE7hNU5F2CE8a8gSHz93mxqc6yzZg")
# This how to connect to or create a database.
db = deta.Base("quiz_test_db")
class QuizTest:
    @quizTest.post('/create_quiz_test')
    def create_Quiz_Game(quiz: QuizTest):
        try:   
            db.put(quiz.dict())       
            return JSONResponse({"message":"insert thanh cong"},status_code=200) 
        except Exception:
            return JSONResponse({"message":"loi"},status_code=404)
    
    @quizTest.get('/getAllQuizTestByPreID')
    def get_AllQuizTest_PreID(preID:str):
        preQ=db.fetch([{"preTestId": preID}]) 
        if preQ:      
            return preQ
        return JSONResponse({"message":"data not found"},status_code=404)
    @quizTest.delete('/deleteAllQuizTestByPreTestID')
    def delete_AllQuiz_Test_ByPreTestID(preTestID:str):
        response =db.fetch([{"preTestId": preTestID}])
        if response.count!=0 : 
            for i in range(response.count):
                keyID = response.items[i]["key"]
                try:
                    db.delete(keyID)
                except Exception:
                    return JSONResponse({"message":"test not found"},status_code=404)
            return JSONResponse({"message":"delete done"},status_code=200)
        else :
            return JSONResponse({"message":"test not done"},status_code=404)
    @quizTest.get('/getAllQuizTestByPreIDWithPagination')
    def get_AllQuizTest_PreID_With_Pagination(preID:str,page_num : int = 1, page_size : int =10):
        data=db.fetch([{"preTestId": preID}]) 
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
