from fastapi import APIRouter
from models.preTest import PreTest,PreTestUpdate
from fastapi.responses import JSONResponse
from deta import Deta 
from routes.quizTest import QuizTest


preTest = APIRouter() 

deta = Deta("c01JK2yDofss_kB5xE7hNU5F2CE8a8gSHz93mxqc6yzZg")
# This how to connect to or create a database.
db = deta.Base("pre_test_db")
class PreTest :
    @preTest.post('/create_prequiz_test')
    def create_PreQuiz_Test(preQ: PreTest): 
        res=db.fetch([{"userId": preQ.userId,"status": "GOING"}]) 
        if res.count == 1: 
            keyID = res.items[0]["key"]         
            db.delete(keyID)      
            db.put(preQ.dict())       
            res=db.fetch([{"userId": preQ.userId,"status": "GOING"}],limit=1) 
            if res :
                return res
            else : 
                return JSONResponse({"message":"insert loi"},status_code=404)
        else : 
            db.put(preQ.dict())       
            res=db.fetch([{"userId": preQ.userId,"status": "GOING"}],limit=1) 
            if res :
                return res
            else : 
                return JSONResponse({"message":"insert loi"},status_code=404)
    
    @preTest.get('/getpreTestByID')
    def get_PreQuizTest_ByID(id:str):
        preQ=db.get(id)
        return preQ
    @preTest.delete('/deletePreTestByID')
    def delete_PreQ_Test(id:str):
        db.delete(id)
        QuizTest.delete_AllQuiz_Test_ByPreTestID(preTestID=id)
        return JSONResponse({"message":"delete done"},status_code=200)
    @preTest.delete('/deleteAllPreTestByUID')
    def delete_All_PreQ_Test_ByUID(userID:str):
        response =db.fetch([{"userId": userID}])
        if response.count!=0 : 
            for i in range(response.count):
                keyID = response.items[i]["key"]
                try:
                    db.delete(keyID)
                    QuizTest.delete_AllQuiz_Test_ByPreTestID(preTestID=keyID)
                except Exception:
                    return JSONResponse({"message":"user not found"},status_code=404)
            return JSONResponse({"message":"delete done"},status_code=200)
        else :
            return JSONResponse({"message":"delete not done"},status_code=404)
    @preTest.delete('/deleteAllPreTestLowScoreByUID')
    def delete_All_PreQ_Test_LowScore_ByUID(userID:str):
        response =db.fetch([{"userId": userID}])
        if response.count!=0 : 
            for i in range(response.count):
                score= response.items[i]["score"]
                numQ= response.items[i]["numQ"]
                if((score / numQ ) * 10 < 5 ) :
                    keyID = response.items[i]["key"]
                    try:
                        db.delete(keyID)
                        QuizTest.delete_AllQuiz_Test_ByPreTestID(preTestID=keyID)
                    except Exception:
                        return JSONResponse({"message":"user not found"},status_code=404)
            return JSONResponse({"message":"delete done"},status_code=200)
        else :
            return JSONResponse({"message":"delete not done"},status_code=404)
    @preTest.get('/getAllPreQuizTest')
    def get_All_Pre_Quiz_Game():
        res = db.fetch()
        return res
    @preTest.get('/getAllPreQuizTestByUId')
    def get_All_Pre_Quiz_Game_ByUid_OptionGame(uid:str):
        res = db.fetch([{"userId": uid,}]) 
        return res
    @preTest.get('/getAllPreQuizTestByUIdWithPagi')
    def get_All_Pre_Quiz_Game_ByUid_OptionGame_WithPagi(uid:str,page_num : int = 1, page_size : int =5):
        data = db.fetch([{"userId": uid,}]) 
        start =(page_num -1) * page_size
        end =start +page_size
        response = {
            "data":data.items[start:end],
            "total":data.count,
            "count":page_size,
        }
        if(response) :
            return response
        return JSONResponse({"message":"not found"},status_code=404)
    @preTest.patch('/updatePreQuizTesteById')
    def update_PreQuizTest_ById(id: str,preUpdate : PreTestUpdate):
        updates={k:v for k,v in preUpdate.dict().items() if v is not None}
        try:
            db.update(updates,id)
            return db.get(id)
        except Exception:
            return JSONResponse({"message":"update loi"},status_code=404)