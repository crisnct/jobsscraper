from fastapi import FastAPI
from scrapers.best_jobs_scrapper import BestJobsScrapper
from models.filter import Filter
from models.response import AppResponse
from src.scraper_handler import ScraperHandler

app = FastAPI()
scraper_handler = ScraperHandler(BestJobsScrapper())


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/scrape/jobs")
async def getScrapedJobs(request_body:Filter) -> AppResponse: 
    try:
        return await scraper_handler.run(request_body)
    except Exception as e:
        print(f"Error scraping : {e}")
        return AppResponse()