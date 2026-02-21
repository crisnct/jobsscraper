


from src.common.scrapper import Scrapper
from src.common.types.response_options import ResponseOptions
from src.core.models.app_request import AppRequest
from src.core.scrapers.best_jobs_scrapper import BestJobsScrapper


class ScraperHandler():
    def set_scraper(self,request:AppRequest):
        match request.scrapper.value:
            case "bestjobs":
                self.scrapper:Scrapper = BestJobsScrapper(filter=request.filter)
            case "ejobs":
                pass    
    async def run(self) -> ResponseOptions:
        return await self.scrapper.scrape()
