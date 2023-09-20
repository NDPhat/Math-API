from fastapi import APIRouter
from models.quizPractice import QuizPractice
from fastapi.responses import JSONResponse
from deta import Deta 

quizPra = APIRouter() 
deta = Deta("c01JK2yDofss_kB5xE7hNU5F2CE8a8gSHz93mxqc6yzZg")
# This how to connect to or create a database.
db = deta.Base("quiz_pra_db")
class QuizGame : 
    @quizPra.post('/create_quiz_game')
    def create_Quiz_Game(quiz: QuizPractice):
        try:   
            db.put(quiz.dict())       
            return JSONResponse({"message":"insert thanh cong"},status_code=200) 
        except Exception:
            return JSONResponse({"message":"loi"},status_code=404)
    
    @quizPra.get('/getAllQuizGameByPreID')
    def get_AllQuizGame_PreID(preID:str):
        preQ=db.fetch([{"prePraId": preID}]) 
        if preQ:      
            return preQ
        return JSONResponse({"message":"data not found"},status_code=404)
    @quizPra.get('/getAllQuizGameByPreIDWithPagination')
    def get_AllQuizGame_PreID_With_Pagination (preID:str,page_num : int = 1, page_size : int =10):
        data=db.fetch([{"prePraId": preID}])
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
    @quizPra.get('/getAllQuizGameByPreIDAndSign')
    def get_AllQuizGame_PreID(preID:str,sign:str):
        preQ=db.fetch([{"prePraId": preID,"sign":sign}]) 
        if preQ:      
            return preQ
        return JSONResponse({"message":"data not found"},status_code=404)
    @quizPra.delete('/deleteAlLQuizGameByPreQuizGame')
    def delete_Quiz_Game_ByPreQuizGameID(prequizGameID:str):
        response =db.fetch([{"prePraId": prequizGameID}])
        if response.count!=0 : 
            for i in range(response.count):
                keyID = response.items[i]["key"]
                try:
                    db.delete(keyID)
                except Exception:
                    return JSONResponse({"message":"quiz not found"},status_code=404)
            return JSONResponse({"message":"delete done"},status_code=200)
        else :
            return JSONResponse({"message":"delete not done"},status_code=404)