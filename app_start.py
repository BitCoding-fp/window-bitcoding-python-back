import os
import uvicorn
from dotenv import load_dotenv
load_dotenv()

from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache

set_llm_cache(SQLiteCache(database_path="./llm/my_llm_cache.db"))

if __name__ == "__main__":
    uvicorn.run("main:app",
                host='localhost',
                port=int(os.environ.get("LLM_BE_PORT")),
                reload=True)