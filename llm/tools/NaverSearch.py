from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from services.NaverSearch import NaverSearch

class NaverSearchInput(BaseModel):
    query: str = Field(..., description="query sentence", required=True)
    display: int = Field(..., description="how many results to display", required=False)
    start: int = Field(..., description="search start position", required=False)
    sort: str = Field(..., description="sort mechanism sim(similarity), date(date descending order))", required=False)

@tool("Naver-search-tool", args_schema=NaverSearchInput, return_direct=False)
def NaverSearchTool(query:str) -> str:
    """It is naver search tool. If you need to search concurrent information from naver, you can use this tool."""
    return NaverSearch(query, display, start, sort)
