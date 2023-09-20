from fastapi import APIRouter
from models.prePractice import PrePracticeUpdate
from fastapi.responses import JSONResponse
from deta import Deta 
from routes.quizPracice import QuizGame
prePractice = APIRouter() 
deta = Deta("c01JK2yDofss_kB5xE7hNU5F2CE8a8gSHz93mxqc6yzZg")
# This how to connect to or create a database.
db = deta.Base("pre_practice_db")
class PrePra : 
    @prePractice.post('/create_prequiz_game')
    def create_PreQuiz_Game(preQ: PrePracticeUpdate):
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
    
    @prePractice.get('/getPreQuizGameByID')
    def get_PreQuizGame_ByID(id:str):
        preQ=db.get(id)
        return preQ
    @prePractice.get('/getPreQuizGameByUidOnGoing')
    def get_PreQuizGame_ByUID_OnGoing(uid:str):
        res=db.fetch([{"userId": uid,"status": "GOING"}],limit=1) 
        return res
    @prePractice.delete('/deletePreGameByID')
    def delete_PreQ_Game(id:str):
        db.delete(id)
        QuizGame.delete_Quiz_Game_ByPreQuizGameID(prequizGameID=id)
        return JSONResponse({"message":"delete done"},status_code=200)
    @prePractice.delete('/deletePreGameByUId')
    def delete_All_PreQ_Game_ByUID(userID:str):
        db.delete(userID)
        return JSONResponse({"message":"delete done"},status_code=200)
    @prePractice.delete('/deletePreGameByUIdAndDoing')
    def delete_All_PreQ_Game_ByUIDAndDoing(userID:str):
        res=db.fetch([{"userId": userID,"status": "GOING"}],limit=1)
        keyID = res.items[0]["key"]   
        db.delete(key=keyID)      
        return JSONResponse({"message":"delete done"},status_code=200)
    @prePractice.get('/getAllPreQuizGame')
    def get_All_Pre_Quiz_Game():
        res = db.fetch()
        return res
    @prePractice.get('/getAllPreQuizGameByUIdAndOptionGame')
    def get_All_Pre_Quiz_Game_ByUid_OptionGame(uid:str,optionGame:str):
        res = db.fetch([{"userId": uid,"optionGame":optionGame,"status":"DONE"}]) 
        return res
    @prePractice.get('/getTop3ScorePreQuizGameByUIdAndOptionGame')
    def get_Top3_Score_Pre_Quiz_Game_ByUid_OptionGame(uid:str,optionGame:str):
        res = db.fetch([{"userId": uid,"optionGame":optionGame,"status":"DONE"}])
        sorted(res.items,key=lambda x: x['score'], reverse=True)
        return res.items[0:3]
    @prePractice.get('/getAllPreQuizGameByUIdAndOptionGameWithPage')
    def get_All_Pre_Quiz_Game_ByUid_OptionGame_WithPagi(uid:str,optionGame:str,page_num : int = 1, page_size : int =5):
        data = db.fetch([{"userId": uid,"optionGame":optionGame,"status":"DONE"}]) 
        start =(page_num -1) * page_size
        end =start +page_size
        response = {
            "data":data.items[start:end],
            "total":data.count,
            "count":page_size,
        }
        if(response) :
            return response
        return JSONResponse({"message":"update loi"},status_code=404)
    def get_All_Pre_Quiz_Game_ByUid_Status(uid:str):
        res = db.fetch([{"userId": uid,"status":"DONE"}]) 
        return res
    @prePractice.patch('/updatePreQuizGameById')
    def update_PreQuizGame_ById(id: str,preUpdate : PrePracticeUpdate):
        updates={k:v for k,v in preUpdate.dict().items() if v is not None}
        try:
            db.update(updates,id)
            return db.get(id)
        except Exception:
            return JSONResponse({"message":"update loi"},status_code=404)
    @prePractice.delete('/deleteAllPreQuizGameByUID')
    def delete_All_PreQ_Game_ByUID(userID:str):
        response =db.fetch([{"userId": userID}])
        if response.count!=0 : 
            for i in range(response.count):
                keyID = response.items[i]["key"]
                try:
                    db.delete(keyID)
                    QuizGame.delete_Quiz_Game_ByPreQuizGameID(prequizGameID=keyID)
                except Exception:
                    return JSONResponse({"message":"user not found"},status_code=404)
            return JSONResponse({"message":"delete done"},status_code=200)
        else :
            return JSONResponse({"message":"empty "},status_code=200)
    @prePractice.delete('/deleteAllPreQuizGameByUIDAndOptionGame')
    def delete_All_PreQ_Game_ByUIDAndOptionGame(userID:str,option:str):
        response =db.fetch([{"userId": userID,"optionGame":option}])
        if response.count!=0 : 
            for i in range(response.count):
                keyID = response.items[i]["key"]
                try:
                    db.delete(keyID)
                    QuizGame.delete_Quiz_Game_ByPreQuizGameID(prequizGameID=keyID)
                except Exception:
                    return JSONResponse({"message":"user not found"},status_code=404)
            return JSONResponse({"message":"delete done"},status_code=200)
        else :
            return JSONResponse({"message":"empty "},status_code=200)
    @prePractice.delete('/deleteAllPreQuizGameLowScoreByUIDAndOptionGame')
    def delete_All_PreQ_Game_ByUIDAndOptionGameWithLowScore(userID:str,option:str):
        response =db.fetch([{"userId": userID,"optionGame":option}])
        if response.count!=0 : 
            for i in range(response.count):
                score= response.items[i]["score"]
                numQ= response.items[i]["numQ"]
                if((score / numQ ) * 10 < 5 ) :
                    keyID = response.items[i]["key"]
                    try:
                        db.delete(keyID)
                        QuizGame.delete_Quiz_Game_ByPreQuizGameID(prequizGameID=keyID)
                    except Exception:
                        return JSONResponse({"message":"error"},status_code=404)
            return JSONResponse({"message":"delete done"},status_code=200)
        else :
            return JSONResponse({"message":"empty "},status_code=200)