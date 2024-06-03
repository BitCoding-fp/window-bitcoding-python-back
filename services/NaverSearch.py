import os
import requests

def NaverSearch(query:str, display:int, start:int, sort:int):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display}&start={start}&sort={sort}"
    response = requests.get(url, headers=headers)
    return response.json()
