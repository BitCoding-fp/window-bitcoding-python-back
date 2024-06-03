from fastapi import APIRouter
from pydantic import BaseModel
from llm.get_answer_final import persona_short_answer, persona_multiple_question, the_best_multiple, get_score_of_short_answer

router = APIRouter()

class ShortAnswer(BaseModel):
    name:     str
    party:    str
    opinion:  str
    question: str
    tendency: str

@router.post('/getShortAnswerFinal')
async def getShortAnswerFinal(body: ShortAnswer):
    result = persona_short_answer(body.name, body.party, body.opinion, body.question, body.tendency)
    return result

class MultipleChoice(BaseModel):
    name:     str
    party:    str
    opinion:  str
    question: str
    option1:  str
    option2:  str
    option3:  str
    option4:  str

@router.post('/getMultipleChoiceAnswerFinal')
async def getMultipleChoiceAnswerFinal(body: MultipleChoice):
    result = persona_multiple_question(body.name, body.party, body.opinion, body.question, body.option1, body.option2, body.option3, body.option4)
    return result

class ShortAnswer(BaseModel):
    tendency: str
    question: str
    answer: str

@router.post('/evalAnswer')
async def evalAnswer(body: ShortAnswer):
    result = get_score_of_short_answer(body.tendency, body.question, body.answer)
    return result

@router.post('/best')
async def theBest(body: MultipleChoice):
    result = the_best_multiple(body.name, body.party, body.opinion, body.question, body.option1, body.option2, body.option3, body.option4)
    return result