from typing import List
from fastapi import FastAPI
from types.filter import Filter
from types.result import Result
from types.statistic import Statistic

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/scrape/jobs/")
def getScrapedJobs(request_body:Filter) -> dict: 
    results:List[Result] = []
    statistics:List[Statistic] = []
    return {"filters":request_body}