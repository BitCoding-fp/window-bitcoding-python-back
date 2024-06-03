from langchain import hub
from llm.llms import GPT4_turbo as GPT
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_tools_agent

GPT.temperature = 0.1
GPT.verbose = True

class ShortAnswer(BaseModel):
    score: str = Field(..., description="The score of the answer")

class MultipleChoice(BaseModel):
    option: str = Field(..., description="The option of the answer")

def get_prompt(query: str):
    # 객관식 답변
    if ("get_multiple_choice_answer" == query):
        prompt = hub.pull("pollytheparrotaz/get_multiple_choice_answer_ko")
    # 주관식 의견 얻기
    elif ("get_opinion" == query):
        prompt = hub.pull("pollytheparrotaz/get_opinion_ko")
    # 주관식 채점
    elif ("get_short_answer_question" == query):
        prompt = hub.pull("pollytheparrotaz/get_short_answer_question_ko")
    return prompt

# 객관식 답변 묻기
def persona_multiple_question(name: str, party: str, opinion: str, question: str, option1: str, option2: str, option3: str, option4: str):
    prompt = get_prompt("get_multiple_choice_answer")
    llm = GPT.with_structured_output(MultipleChoice, method="json_mode")
    pipe = prompt | llm
    res = pipe.invoke({
        "name": name,
        "party": party,
        "opinion": opinion,
        "question": question,
        "option1": option1,
        "option2": option2,
        "option3": option3,
        "option4": option4
    })
    return res

# 주관식 의견 묻기
def persona_get_opinion(name: str, party: str, opinion: str, question: str):
    prompt = get_prompt("get_opinion")
    pipe = prompt | GPT
    res = pipe.invoke({
        "name": name,
        "party": party,
        "opinion": opinion,
        "question": question
    })
    return res

# 주관식 채점
def get_score_of_short_answer(tendency: str, question: str, answer: str):
    prompt = get_prompt("get_short_answer_question")
    llm = GPT.with_structured_output(ShortAnswer, method="json_mode")
    pipe = prompt | llm
    res = pipe.invoke({
        "tendency": tendency,
        "question": question,
        "answer": answer
    })
    print(res)
    return res

def persona_short_answer(name: str, party: str, opinion: str, question: str, tendency: str):
    res = persona_get_opinion(name, party, opinion, question)
    res = get_score_of_short_answer(tendency, question, res)
    return res

def the_best_multiple(name: str, party: str, opinion: str, question: str, option1: str, option2: str, option3: str, option4: str):
    tools = [TavilySearchResults(max_results=100)]
    prompt = hub.pull("hwchase17/openai-tools-agent")
    llm = GPT.with_structured_output(MultipleChoice, method="json_mode")
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    res = agent_executor.invoke({
        "name": name,
        "party": party,
        "opinion": opinion,
        "question": question,
        "option1": option1,
        "option2": option2,
        "option3": option3,
        "option4": option4
    })
    return res
