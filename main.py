import asyncio
from typing import List
from fastapi import FastAPI
from models.filter import Filter
from models.response import AppResponse
from models.result import Result
from models.statistic import Statistic
from scraper import scrape

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/scrape/jobs")
async def getScrapedJobs(request_body:Filter) -> AppResponse: 
    try:
        return await scrape(request_body)
    except Exception as e:
        print(f"Error scraping : {e}")
        return AppResponse()