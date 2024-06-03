from llm.llms import Llama3_70B, Local_EEVE
from langchain import hub
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
llm = Local_EEVE
llm.temperature = 0.1
llama = Llama3_70B

def get_multiple_question_answer(name:str, description: str, question: str, option1: str, option2: str, option3: str, option4: str):
    print(name)
    print(description)
    print(question)
    print(option1)
    prompt = hub.pull("pollytheparrotaz/get_multiple_choice_answer_fewshot_en")

    class Answer(BaseModel):
        option: int = Field(description="답변")

    query = "답변을 알려주세요"
    parser = JsonOutputParser(pydantic_object = Answer)
    parser_prompt = PromptTemplate(
        template="쿼리에 답변하십시오.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    chain = prompt | llm | parser_prompt | llama | parser

    result = chain.invoke({
        "query": query,
        "name": name,
        "description": description,
        "input": question,
        "option1": option1,
        "option2": option2,
        "option3": option3,
        "option4": option4
    })
    
    return result

def get_short_answer_question(description: str, question: str, context: str):
    print(description)
    print(question)

    prompt = hub.pull("pollytheparrotaz/get_short_answer_answer_en")
    eval_prompt = hub.pull("pollytheparrotaz/get_eval_from_opinion_en")

    class Answer(BaseModel):
        opinion: int = Field(description="선택지")

    query = "선택지를 알려주세요"
    parser = JsonOutputParser(pydantic_object = Answer)
    parser_prompt = PromptTemplate(
        template="쿼리에 답변하십시오.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    answer_chain = prompt | llm 

    eval_chain =  eval_prompt| llm | parser_prompt | llama | parser
    result = answer_chain.invoke({
        "description": description,
        "question": question,
    })
    print(result)

    eval_result = eval_chain.invoke({
        "query": query,
        "context": context,
        "answer": result.content
    })

    return eval_result

def get_short_answer_question_test(question: str, tendency: str, answer: str):

    class Output(BaseModel):
        score: float = Field(description="The score of the answer")

    prompt = hub.pull("pollytheparrotaz/get_short_answer_answer_ko")

    llm = ChatOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model="gpt-4o",
        streaming=True,
        temperature=0
    )
    struct = llm.with_structured_output(Output, method="json_mode")

    pipe = prompt | struct

    return pipe.invoke({
        "question": question,
        "tendency": tendency,
        "answer": answer
    })


def get_eval_answer():
    pass

def get_eval_json_parser():
    pass

