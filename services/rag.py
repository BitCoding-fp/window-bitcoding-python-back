import json
import re
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_transformers import LongContextReorder
from services import pinecone_service
from langchain_community.embeddings import HuggingFaceEmbeddings
from llm.llms import GPT35_turbo
from llm.prompts import QA
from langchain.retrievers import EnsembleRetriever, ParentDocumentRetriever, ContextualCompressionRetriever
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv  # 추가된 부분

load_dotenv()

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_metadata(record):
    return {
        "_id": record.get("_id")['$oid'],
        "proposer": record.get("proposer"),
        "politician_code": record.get("politician_code"),
        "bill_code": record.get("bill_code"),
        "propose_date": record.get("propose_date"),
    }

def normalize_text(text, metadata):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    proposer = metadata['proposer']
    date = metadata['propose_date']
    text += f'\n[tag] 법안을 발의한 사람: {proposer}, 제안일: {date}'
    return text.replace('제안이유 및 주요내용', '').replace('제안이유', '')

def load_and_process_documents(file_path):
    data = load_json(file_path)
    docs = []

    for record in data:
        metadata = extract_metadata(record)
        content = record.get("content", "")
        normalized_text = normalize_text(content, metadata)
        docs.append(Document(page_content=normalized_text, metadata=metadata))

    return docs

# Load and process documents
file_path = 'json/bill_0528.json'
docs = load_and_process_documents(file_path)
print(f"문서의 수: {len(docs)}")

# ############### Split ###############
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

splits = text_splitter.split_documents(docs)
print('split_length =', len(splits))

# ############### Embed and Store ###############
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

index_name = 'bill-search'
namespace = 'bill'

ps = pinecone_service.PineconeService(
    host=os.environ.get('PINECONE_HOST'),
    index_name=index_name,
    namespace=namespace,
    embeddings=embeddings
)

if not ps.get_total_vector_count():
    ps.add_documents(splits)

pinecone_retriever = ps.vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'k': 10, 'score_threshold': 0.75},
)

bm25_retriever = BM25Retriever.from_documents(
    documents=splits,
    k=10,
)

multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=pinecone_retriever,
    llm=GPT35_turbo,
    prompt=QA.multiquery_prompt
)

parent_document_retriever = ParentDocumentRetriever(
    vectorstore=ps.vectorstore,
    docstore=InMemoryStore(),
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50),
    search_kwargs={"k": 10}
)

document_content_description = "법안의 제안 이유 및 주요 내용입니다."
metadata_field_info = [
    AttributeInfo(
        name="proposer",
        description="법안을 발의한 의원입니다.",
        type="string",
    ),
    AttributeInfo(
        name="propose_date",
        description="법안이 발의된 날짜입니다.",
        type="integer",
    )
]
self_query_retriever = SelfQueryRetriever.from_llm(
    llm=GPT35_turbo,
    vectorstore=Chroma.from_documents(documents=splits, embedding=embeddings),
    document_contents=document_content_description,
    metadata_field_info=metadata_field_info,
    search_kwargs={"k": 10}
)

hybrid_retriever = EnsembleRetriever(
    retrievers=[
        bm25_retriever, 
        pinecone_retriever, 
        multiquery_retriever, 
        parent_document_retriever, 
        self_query_retriever
        ],
    weights=[
        0.2, 
        0.2, 
        0.2, 
        0.2,
        0.2
        ],
)

model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
compressor = CrossEncoderReranker(model=model, top_n=10)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=hybrid_retriever
)

reordering = LongContextReorder()
def reordering_format_docs(docs):
    reordered_docs = reordering.transform_documents(docs)
    return "\n\n".join(doc.page_content for doc in reordered_docs)

############### Prompt and Chain ###############
hybrid_chain = (
    {"context": compression_retriever | reordering_format_docs, "question": RunnablePassthrough()}
    | QA.custom_bill_qna_prompt
    | GPT35_turbo
    | StrOutputParser()
)
