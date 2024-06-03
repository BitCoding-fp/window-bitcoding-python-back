from fastapi import APIRouter
from services import mongodb_service
from services import rag
from pydantic import BaseModel


router = APIRouter()

ms = mongodb_service.MongodbService('bill', 'bill')

class BillSearchRequest(BaseModel):
    q: str


@router.post("/search/", tags=["search"], summary='search for bills')
async def qna(request: BillSearchRequest):
    q = request.q
    retriever_results = rag.compression_retriever.invoke(q)
    relevalent_results = await ms.aget_top_ten_json(retriever_results)
    qna_result = rag.hybrid_chain.invoke(q)
    return {
        "qna_result": qna_result, 
        "relevalent_results": relevalent_results
        } 



