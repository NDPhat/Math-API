from pydantic import BaseModel

class QuizTest(BaseModel):
    quiz: str
    preTestId: str
    answer:int
    answerSelect:int
    infoQuiz:bool

class QuizTestUpdate(BaseModel):
    quiz: str=None
    preTestId: str=None
    answer:int=None
    answerSelect:int=None
    infoQuiz:bool=None