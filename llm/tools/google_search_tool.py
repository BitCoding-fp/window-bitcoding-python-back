# from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from dotenv import load_dotenv
import os

load_dotenv()

search = GoogleSearchAPIWrapper(
    google_api_key=os.environ.get("GOOGLE_API_KEY"),
    google_cse_id=os.environ.get("GOOGLE_CSE_ID")
)

google_search = Tool(
    name="google_search",
    description="Must use this tool first.",
    func=search.run,
)