from fastapi import FastAPI
from types.filter import Filter

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/scrape/jobs/")
def getScrapedJobs(request_body:Filter):
    return {"filters":request_body}