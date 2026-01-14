from typing import List
from fastapi import FastAPI
from models.filter import Filter
from models.result import Result
from models.statistic import Statistic

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/scrape/jobs/")
def getScrapedJobs(request_body:Filter) -> dict: 
    results:List[Result] = []
    statistics:List[Statistic] = []
    return {
        "results":results,
        "statistics":statistics
    }