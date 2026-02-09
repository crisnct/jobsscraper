from models.filter import Filter
from scrapers.scrapper import Scrapper


class ScraperHandler():
    def __init__(self, scrapper:Scrapper):
        self.scrapper = scrapper
    def set_scraper(self,scraper:Scrapper):
        self.scrapper = scraper
        return self
    async def run(self,filter:Filter):
        self.scrapper.set_filter(filter)
        return await self.scrapper.scrape()
