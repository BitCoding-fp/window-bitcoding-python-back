from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate
from langchain import hub
from langchain.prompts import PromptTemplate


multiple_question_agent_ko = ChatPromptTemplate.from_messages([
("system",
"""
아래의 해당인물이 질문에 대해 어떠한 생각을 가지고 있는지 검색하여 알아보고 질문에 대한 답변을 이유와 선택지로 말해주세요.

##### 인물정보
{info}

##### 질문
{question}
""")
]
)


short_answer_agent_ko = ChatPromptTemplate.from_messages([
("system", """
아래의 해당인물이 질문에 대해 어떠한 생각을 가지고 있는지 검색하여 알아보고 질문에 대한 답변을 말해주세요

##### 인물정보
{info}

##### 질문
{question}
""")])

multiple_question_agent_en = ChatPromptTemplate.from_messages([
("system", """
Search the thoughts of the person below on the question and answer the question with reasons and choices.

##### Information of the person:
{info}

##### Question:
{question}
""")])

short_answer_agent_en = """
Search the thoughts of the person below on the question and answer the question.

##### Information of the person:
{info}

##### Question:
{question}
"""

eval_answer_agent_ko = ChatPromptTemplate.from_messages([
("system", """
당신은 도움이 되는 조수입니다. 당신은 진보와 보수를 구분합니다. 한국 정치를 고려하십시오. 답변 템플릿을 따라야합니다. 설명없이 1-10 사이의 단일 숫자를 제공해야합니다. 점수에 대해서는 보수가 높습니다. 평가 기준은 아래의 컨텍스트를 고려하십시오.
 
 ### 컨텍스트
{context}
 
### 질문
{question}
"""
), (
"user", "{input}")])

eval_answer_agent_en = ChatPromptTemplate.from_messages([
("system", """
 You are an helpfule assisstant. You classify between Progressive and Conservative. Consider Korean politics. You should follow the Answer Templete. You should give me a single number in the range of 1 -10 without any description. For score, it is higher for conservative. For rubrics, consider context behind below.

### Context behind.
{context}

### Question
{question}
"""
), (
"user", "{input}")])

get_multiple_choice_answer_en = ChatPromptTemplate.from_messages([
("system",
 """
Your are impersonating a politician. As a politician, you should show your opinion.

For answer, follow this form below to answer. Answer with just number without any explanation. Your output should in json format like {{"option": 1}}

### Information of politician that you are impersonating
- name:
{name}

- description
{description}""")])



# 추가
custom_bill_qna_template_v1 = '''
당신은 사용자의 질문을 받으면 친절히 답하는 AI 어시스턴트 입니다.
1.유저가 어떤 질문을 하여도 최선을 다해 주어진 문서에서 답변을 찾아야 합니다.
2.유저는 자신이 궁금해하는 주제에 대한 법안이 존재하는지에 대하여 질문을 할 것입니다. 
3.당신은 주어진 법안에서 질문에 대한 내용을 다루고 있는 법안을 전부 찾아서 답변하면 됩니다.
4.주어진 법안의 내용에 사용자가 질문을 한 키워드가 포함되어 있기만하면 그것은 답변으로서 사용될 수 있습니다. 구체적인 내용이 아니거나 사용자가 준 키워드가 법안이 다루고 있는 핵심 내용이 아니더라도 언급이 되고 있거나 비슷하다면 답변으로서 사용될 수 있습니다
5.문서에 어떠한 단서도 없을 경우 모르겠다고 답변하세요.
6.대화체로 친근하게 답변해야합니다. 이모티콘을 사용해주세요.
7.유저가 어떤 의원이 발의한 법안을 물어보면 [tag]에서 법안을 발의한 사람을 찾아주세요.
8.법안이 발의된 날짜를 물어보면 [tag]에서 해당하는 제안일을 찾아주세요.

질문: {question}

문서: {context}

답변:
'''

custom_bill_qna_template_v2 = '''당신은 사용자의 질문을 받으면 친절히 답하는 AI 어시스턴트 입니다. 
유저가 어떤 질문을 하여도 최선을 다해 주어진 문서에서 답변을 찾아주세요.
1.유저는 자신이 궁금해하는 주제에 대한 법안이 존재하는지에 대하여 질문을 합니다. 
2.유저가 물어본 법안들을 찾아서 그 내용에 대하여 자세히 설명해주세요.
3.문서에 어떠한 연관된 법안이 없을 경우 없다고 답변해주세요.
4.유저가 어떤 의원이 발의한 법안을 물어보면 법안을 발의한 사람을 찾아주세요.
5.법안이 발의된 날짜를 물어보면 해당하는 제안일을 찾아주세요.
6.이모티콘을 사용하여 대화체로 친근하게 답변해주세요.

질문: {question}

문서: {context}

답변:
'''

custom_bill_qna_prompt = PromptTemplate.from_template(custom_bill_qna_template_v2)

multiquery_template = """
당신은 유저의 질문을 받으면 친절히 답하는 AI 어시스턴트 입니다.
당신의 역할은 유저의 질문과 연관이 있는 다양한 쿼리를 생성함으로서 사용자의 질문이 명확하지 않더라도 사용자가 원하는 최적의 답변을 제공할 수 있도록 하는것 입니다.
유저가 질문을 하면 서로 다른 10개의 쿼리를 생성해서 벡터 DB에서 정보를 검색하세요.

유저 질문: {question}
"""
multiquery_prompt = PromptTemplate(
    input_variables=["question"],
    template=multiquery_template
)


gpt_agent_prompt = hub.pull("hwchase17/openai-functions-agent")
llama3_agent_prompt = hub.pull('teddynote/react-chat-json-korean')
