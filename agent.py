from langchain.agents import create_openai_functions_agent, AgentExecutor, create_json_chat_agent
from llm.llms import GPT35_turbo, Llama3_70B
import llm.tools.google_search_tool as google_search_tool
import llm.tools.naver_search_tool as naver_search_tool
import os
from langchain import hub
from llm.prompts import QA


os.environ["LANGCHAIN_PROJECT"] = "default"

tools = [google_search_tool.google_search, 
        naver_search_tool.NaverSearchTool(description='If you can\'t find anything with google_search, use this tool')
        ]

llama3_agent_executor = AgentExecutor(
    agent=create_json_chat_agent(Llama3_70B, tools, QA.llama3_agent_prompt),
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)

gpt_agent_executor = AgentExecutor(
    agent=create_openai_functions_agent(GPT35_turbo, tools, QA.gpt_agent_prompt), 
    tools=tools, 
    verbose=True)
