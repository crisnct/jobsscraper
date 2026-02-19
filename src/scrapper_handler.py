from src.common.models.app_request import AppRequest
from src.common.types.response_options import ResponseOptions
from src.scrapers.best_jobs_scrapper import BestJobsScrapper
from src.scrapers.scrapper import Scrapper


class ScraperHandler():
    def set_scraper(self,request:AppRequest):
        match request.scrapper.value:
            case "bestjobs":
                self.scrapper:Scrapper = BestJobsScrapper(filter=request.filter)
            case "ejobs":
                pass    
    async def run(self) -> ResponseOptions:
        return await self.scrapper.scrape()
