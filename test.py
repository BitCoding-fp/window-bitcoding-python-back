# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import os, json, logging ,asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from llm.llms import GPT35_turbo
import agent


load_dotenv()



q = '''
1. {party} 소속 {politician} 의원이 아래 문제에 대해서 어떻게 생각할지 검색하여 알아보세요. 
2. 필요하다면 아래 [기본 정보]를 참고하여 추가적으로 정보를 알아보세요.
3. 알아낸 정보를 가지고 아래 [문제]의 선택지 중 {politician} 의원이 선택할만한 가능성이 가장 높아 보이는 것을 하나 선택해주세요. 
4. 1번부터 4번까지의 선택지 중에서 반드시 하나를 선택해야합니다.
5. 선택지의 번호로 답변해주세요.

[기본 정보]:
강기윤 의원은 1960년 6월 4일 생으로 국민의힘 소속의 간사로 활동 중이며, 보건복지위원회에 속해 있습니다.\n\n-발의법안 : \n1. 영유아보육법 일부개정법률안\n2. 치매관리법 일부개정법률안\n3. 개발제한구역의 지정 및 관리에 관한 특별조치법 일부개정법률안\n4. 국민건강보험법 일부개정법률안\n5. 국가유공자 등 예우 및 지원에 관한 법률 일부개정법률안\n\n-외교/안보 : \n강기윤 의원은 보수 성향이 강한 외교노선을 가지고 있으며, 안보의식은 전통적인 보수성향을 보여줍니다.\n\n-사회 : \n사회 정책에 다양한 의견을 포함시키며, 초고령사회, 방문간호, 산후도우미 등 사회서비스 관리 문제에 관심을 가지고 있습니다.\n\n-경제 : \n경제 정책은 지역개발과 지역경제 활성화를 중시하며, 의료현안협의체를 통해 구체적 대안을 제시하고자 합니다.\n\n-법/제도 : \n법치와 제도에 대한 견해는 노사 법치주의를 중시하며, 국민의힘 당의 쇄신을 위해 노력하고 국민의 권익을 보호하고자 합니다.\n\n-정치인에 대한 한 줄 평가 : \n강기윤 의원은 보수 성향이 강한 정치인으로, 다양한 분야에서 활발한 활동을 펼치고 있습니다.

[문제]:
부자들에게 세금을 더 걷어서 대중을 위해 써야한다.
1.매우 그렇다
2.약간 그렇다
3.약간 아니다
4.전혀 아니다
'''
x = agent.llama3_agent_executor.invoke({"input": q.format(party='국민의 힘', politician='강기윤')})
print(x['output'])


