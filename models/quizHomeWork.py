from pydantic import BaseModel

class QuizHomeWorkDetail(BaseModel):
    quiz: str
    resultHWID: str
    answer:int
    answerSelect:int
    infoQuiz:bool
