from pydantic import BaseModel
from typing import List

class QuizPractice(BaseModel):
    quiz: str
    prePraId: str
    answer:int
    sign:str
    answerSelect:int
    infoQuiz:bool
 
class QuizPracticeUpdate(BaseModel):
    quiz: str=None
    prePraId: str=None
    answer:int=None
    sign:str=None
    answerSelect:int=None
    infoQuiz:bool=None
