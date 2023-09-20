from fastapi import APIRouter
from models.preHomeWork import PreHomeWork,PreHomeWorkUpdate
from fastapi.responses import JSONResponse
from deta import Deta 

preHomeWork = APIRouter() 

deta = Deta("c01JK2yDofss_kB5xE7hNU5F2CE8a8gSHz93mxqc6yzZg")
# This how to connect to or create a database.
db = deta.Base("pre_hw_db")
class PreQuizHW :
    @preHomeWork.post('/create_prequiz_hw')
    def create_PreQuiz_HW(preQ: PreHomeWork):
        preQGet=db.fetch([{"week": preQ.week}])
        if preQGet.count!=0:
            return JSONResponse({"message":"quiz da ton tai"},status_code=404)
        else :    
            db.put(preQ.dict())
            return JSONResponse({"message":"insert thanh cong"},status_code=200)

    @preHomeWork.get('/getPreQuizHWByWeekAndClass')
    def get_PreQHW(week:str, lop:str):
        preQ=db.fetch([{"week": week,"lop": lop}],limit=1) 
        if preQ:      
            return preQ
        return JSONResponse({"message":"data not found"},status_code=404)
    @preHomeWork.delete('/deletePreQHWByWeekAndClass')
    def delete_PreQ_HW_ByWeek_Class(week :str, lop:str):
        pre=db.fetch([{"week":week,"lop":lop}])
        keyId=pre.items[0]["key"]
        db.delete(keyId)
        return JSONResponse({"message":"delete done"},status_code=200)
    @preHomeWork.get('/getAllPreQuizHW')
    def get_All_Pre_Quiz_HW():
        res = db.fetch()
        return res
    @preHomeWork.patch('/updatePreHWByID')
    def update_Pre_Quiz_HW(preUp:PreHomeWorkUpdate,key :str):
        updates={k:v for k,v in preUp.dict().items() if v is not None}
        try:
            db.update(updates,key)
            return db.get(key)
        except Exception:
            return JSONResponse({"message":"update loi"},status_code=404)
    @preHomeWork.patch('/updateStatusPreHWByWeekAndClass')
    def update_status_Pre_Quiz_HW(preUp:PreHomeWorkUpdate,week :str,lop:str):
        preQ=db.fetch([{"week": week,"lop":lop}],limit=1) 
        updates={k:v for k,v in preUp.dict().items() if v is not None}
        try:
            keyID=preQ.items[0]["key"]
            db.update(updates,keyID)
            return db.get(keyID)
        except Exception:
            return JSONResponse({"message":"update loi"},status_code=404)
    @preHomeWork.get('/getPreWStatusOnGoingByClass')
    def get_prehw_ongoing(lop:str):
        data=db.fetch([{"status": "GOING","lop":lop}],limit=1) 
        if data:      
            return data
        return JSONResponse({"message":"data not found"},status_code=404)
    @preHomeWork.get('/getLatestPreQuizHWByWeekAndClass')
    def get_latest_prehw(lop:str):
        res = db.fetch()
        data=db.fetch([{"week": str(res._count),"lop":lop}],limit=1) 
        if data:      
            return data
        return JSONResponse({"message":"data not found"},status_code=404)
    @preHomeWork.get('/getAllDonePreHWByClass')
    def get_all_done_prehw(lop:str):
        data=db.fetch([{"status": "DONE","lop":lop}]) 
        if data:      
            return data
        return JSONResponse({"message":"data not found"},status_code=404)
    @preHomeWork.get('/getAllDonePreHWWithPagiByClass')
    def get_all_done_prehw_with_pagi(lop :str,page_num : int = 1, page_size : int =5):
        data=db.fetch([{"status": "DONE","lop":lop}]) 
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
