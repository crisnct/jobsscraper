from src.common.filters.best_jobs_filter import Filter
from scrapers.scrapper import Scrapper
from src.common.types.filter_options import FilterOptions


class ScraperHandler():
    def __init__(self, scrapper:Scrapper):
        self.scrapper = scrapper
    def set_scraper(self,scraper:Scrapper):
        self.scrapper = scraper
        return self
    async def run(self,filter:FilterOptions):
        self.scrapper.set_filter(filter)
        return await self.scrapper.scrape()
