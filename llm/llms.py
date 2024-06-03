import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

Llama3_70B = ChatOpenAI(
    base_url=os.environ.get("XIONIC_URL"),
    api_key=os.environ.get("XIONIC_API_KEY"),
    model="xionic-ko-llama-3-70b",
)

GPT4o = ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-4o",
    streaming=True
)

GPT4_turbo= ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-4-turbo",
)

GPT35_turbo = ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
)

Claude_Opus = ChatAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    model="claude-3-opus-20240229",
)

Claude_Sonnet = ChatAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    model="claude-3-sonnet-20240229",
)

Local_EEVE = ChatOpenAI(
    base_url="https://8b38-121-135-209-235.ngrok-free.app/v1",
    model="teddylee777/EEVE-Korean-Instruct-10.8B-v1.0-gguf",
    api_key="lm-studio"
)
