from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.common.filters.best_jobs_filter import BestJobsFilter
from src.common.models.app_request import AppRequest
from src.common.models.best_jobs_models.response import AppResponse
from src.common.types.response_options import ResponseOptions
from src.scrapers.best_jobs_scrapper import BestJobsScrapper
from src.scrapper_handler import ScraperHandler

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=429,
    content={"detail": "Rate limit exceeded"}
))
app.add_middleware(SlowAPIMiddleware)

scraper_handler = ScraperHandler()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/search/jobs")
@limiter.limit("10/minute") # Limit to 10 requests per minute per IP
async def getScrapedJobs(request:Request, app_request:AppRequest) -> ResponseOptions: 
    try:
        scraper_handler.set_scraper(app_request)
        return await scraper_handler.run()
    except Exception as e:
        raise
