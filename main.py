from fastapi import FastAPI
from routes.user import user 
from routes.preHomeWork import preHomeWork 
from routes.resultHomeWork import resultHW 
from routes.quizHomeWork import quizHW 
from routes.prePractice import prePractice 
from routes.quizPracice import quizPra 
from routes.preTest import preTest 
from routes.quizTest import quizTest 

app = FastAPI()
app.include_router(user)
app.include_router(preHomeWork)
app.include_router(resultHW)
app.include_router(quizHW)
app.include_router(prePractice)
app.include_router(quizPra)
app.include_router(preTest)
app.include_router(quizTest)

@app.get("/")
async def root():
    return {"message": "Hello World"}

 # Import Deta
