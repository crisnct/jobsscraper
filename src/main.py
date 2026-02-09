from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from src.models.filter import Filter
from src.models.response import AppResponse
from src.scrapers.best_jobs_scrapper import BestJobsScrapper
from slowapi.middleware import SlowAPIMiddleware


app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=429,
    content={"detail": "Rate limit exceeded"}
))
app.add_middleware(SlowAPIMiddleware)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/search/jobs")
@limiter.limit("10/minute") # Limit to 10 requests per minute per IP
async def getScrapedJobs(request:Request, request_body:Filter) -> AppResponse: 
    try:
        return await BestJobsScrapper(filter=request_body).scrape()
    except Exception as e:
        print(f"Error scraping : {e}")
        return AppResponse()