from langchain import hub
from langchain.agents import AgentExecutor, create_json_chat_agent, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.prompts import PromptTemplate
from llm.llms import Llama3_70B
from llm.tools.NaverSearch import NaverSearchTool
from llm.prompts.QA import multiple_question_agent_ko, short_answer_agent_ko, eval_answer_agent_ko


llm = Llama3_70B
llm.temperature = 0.1

def jsonParser():

    json_prompt = PromptTemplate.from_template(
    """
    {qq}
    위 질문을 읽고 json 객체를 answer키 와 reason키를 가진 객체로 반환해주세요.
    answer은 답변의 번호이고 reason은 답변의 이유를 완벽한 한국어 문장으로 적어주세요.
    """)
    json_parser = SimpleJsonOutputParser()

    chain = json_prompt | llm | json_parser
    
    return chain

def eval_json_parser():
    json_prompt = eval_answer_agent_ko
    json_parser = SimpleJsonOutputParser()
    chain = json_prompt | llm | json_parser
    return chain

def multiple_answer(info, question):
    print(info)
    print(question)

    tools = [TavilySearchResults(max_results=1)]
    json_prompt=hub.pull("teddynote/react-chat-json-korean")

    agent=create_tool_calling_agent(llm, tools, json_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )

    response = agent_executor.invoke({"input": multiple_question_agent_ko.format(info=info, question=question), "tools": tools, "tool_names": ["TavilySearchResults"]})

    json = jsonParser().invoke({"qq": response})

    return json

def short_answer(info, question):
    # response = agent().invoke({"input": short_answer_agent_ko, "info":info, "question":question})

    # json = jsonParser().invoke({"input": response})

    return 1

def eval_answer(answer):
    response = agent().invoke({"input": eval_answer_agent_ko, "context":answer["context"], "question":answer["question"]})
    json = eval_json_parser().invoke({"input": response})
    return json
