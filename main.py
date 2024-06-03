""" FastAPI main file """

import os, importlib
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from langsmith import Client
from routes import search

client = Client()

# MSA - Symmetric Key validation
async def verify_token(token: str = Depends(APIKeyHeader(name="Authorization"))):
    if token != os.getenv("LLM_BE_TOKEN"):
        raise HTTPException(status_code=403, detail="Unauthorized")

# FastAPI Initialization
app = FastAPI(dependencies=[Depends(verify_token)])

# Add main router
app.include_router(importlib.import_module("routes.main").router)

# 추가
app.include_router(search.router, prefix='/search', tags=['search'])


