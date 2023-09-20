from fastapi import APIRouter
from models.resultHomeWork import ResultHomeWork,ResultHomeWorkUpdate
from config.db import conn 
from fastapi.responses import JSONResponse
from deta import Deta 


resultHW = APIRouter() 
deta = Deta("c01JK2yDofss_kB5xE7hNU5F2CE8a8gSHz93mxqc6yzZg")
# This how to connect to or create a database.
db = deta.Base("result_hw_db")
class ResultHW : 
    @resultHW.post('/create_result_quiz')
    def create_Result_Quiz_HW(resultQ: ResultHomeWork):
        resultData=db.fetch([{"userId": resultQ.userId,"week": resultQ.week,"status":"GOING"}]) 
        if resultData.count == 1 :
            keyID = resultData.items[0]["key"]  
            db.delete(keyID)
            db.put(resultQ.dict())
            resultData=db.fetch([{"userId": resultQ.userId,"week": resultQ.week,"status":"GOING"}]) 
            if resultData:      
                return resultData
            else:
                return JSONResponse({"message":"loi"},status_code=404)
        else :
            db.put(resultQ.dict())
            resultData=db.fetch([{"userId": resultQ.userId,"week": resultQ.week}]) 
            if resultData:      
                return resultData
            else:
                return JSONResponse({"message":"loi"},status_code=404)
    @resultHW.post('/createResultHWForNoJoin')
    def create_Result_Quiz_HW_For_student_NoJoin(resultQ: ResultHomeWork):
        try:   
            db.put(resultQ.dict())       
            resultData=db.fetch([{"userId": resultQ.userId,"week": resultQ.week}]) 
            if resultData:      
                return resultData
        except Exception:
            return JSONResponse({"message":"loi"},status_code=404)
    @resultHW.patch('/updateResultQuizHWById')
    def update_ResultQuizHW_ById(id: str,resultUpdate : ResultHomeWorkUpdate):
        updates={k:v for k,v in resultUpdate.dict().items() if v is not None}
        try:
            db.update(updates,id)
            return db.get(id)
        except Exception:
            return JSONResponse({"message":"update loi"},status_code=404)
    @resultHW.patch('/updateAllResultQuizHWByUid')
    def update_All_ResultQuizHW_ByUId(userId: str,resultUpdate : ResultHomeWorkUpdate):
        response=db.fetch([{"userId": userId}]) 
        if response.count!=0 : 
            for i in range(response.count):
                keyID = response.items[i]["key"]
                updates={k:v for k,v in resultUpdate.dict().items() if v is not None}
                try:
                    db.update(updates,keyID)
                except Exception:
                    return JSONResponse({"message":"update loi"},status_code=404)
            response=db.fetch([{"userId": userId}]) 
            return response
        else :
            return JSONResponse({"message":"user not found"},status_code=404)

    @resultHW.get('/getResultQuizByWeek')
    def get_Result_Quiz_HW(week:str):
        preQ=db.fetch([{"week": week}],limit=1) 
        if preQ:      
            return preQ
        return JSONResponse({"message":"data not found"},status_code=404)
    @resultHW.delete('/deleteResultQHWResultId')
    def delete_Result_Quiz_HW(resultID:str):
        db.delete(resultID)
        return JSONResponse({"message":"delete done"},status_code=200)
    @resultHW.get('/getAllResultQuizHW')
    def get_All_Result_Quiz_HW():
        res=db.fetch() 
        if res:      
            return res
        return JSONResponse({"message":"data not found"},status_code=404)
    @resultHW.get('/getAllResultQuizHWByUId')
    def get_All_Result_Quiz_HWByUId(userID:str):
        res=db.fetch([{"userId": userID,"status":"DONE"}]) 
        if res:      
            return res
        return JSONResponse({"message":"data not found"},status_code=404)
    @resultHW.get('/getAllResultQuizHWByUIdWithPagi')
    def get_All_Result_Quiz_HWByUId_WithPagi(userID:str,page_num : int = 1, page_size : int =5):
        data=db.fetch([{"userId": userID,"status":"DONE"}]) 
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
    @resultHW.get('/getAllResultQuizHWByWeek')
    def get_All_Result_Quiz_HWByWeek(week:str):
        res=db.fetch([{"week": week}]) 
        if res:      
            return res
        return JSONResponse({"message":"data not found"},status_code=404)
    @resultHW.get('/getAllResultQuizHWByLop')
    def get_All_Result_Quiz_HWByLop(lop:str):
        res=db.fetch([{"lop": lop}]) 
        if res:      
            return res
        return JSONResponse({"message":"data not found"},status_code=404)
    @resultHW.get('/getAllResultQuizHWByWeekAndClass')
    def get_All_Result_Quiz_HWByWeek(week:str,lop:str):
        res=db.fetch([{"week": week,"lop":lop}]) 
        if res:      
            return res
        return JSONResponse({"message":"data not found"},status_code=404)
    @resultHW.get('/getAllResultQuizHWByWeekAndClassWithPagi')
    def get_All_Result_Quiz_HWByWeek_AndClass_WithPagi(week:str,lop:str,page_num : int = 1, page_size : int =5):
        data=db.fetch([{"week": week,"lop":lop}]) 
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
    @resultHW.get('/getResultQuizHWByUIdAndWeek')
    def get_Result_Quiz_HWByUIdandWeek(userID:str,week:str):
        res=db.fetch([{"userId": userID,"week":week,"status":"DONE"}]) 
        if res:      
            return res
        return JSONResponse({"message":"data not found"},status_code=404)
