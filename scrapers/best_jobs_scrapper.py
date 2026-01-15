import asyncio
import itertools
from typing import List
from scrapers.scrapper import Scrapper
from models.filter import Filter
from playwright.async_api import async_playwright, Page

from models.response import AppResponse
from models.result import Result

class BestJobsScrapper(Scrapper):

    def __formatRoles(self):
        if(self.filter.roles):
            self.filter.roles = [role.replace(" ", "-") for role in self.filter.roles]
            return self
        return self
    
    def __buildSearchUrls (self) -> List[str]:
        baseUrl = "https://www.bestjobs.eu/"
        if(self.filter.location):
            baseUrl+= 'locuri-de-munca-in-'+self.filter.location
        return [baseUrl + "/"+role for role in self.filter.roles]
    def set_filter(self, filter):
        return super().set_filter(filter)
    
    async def __scrape_hrefs(self,page:Page):    
        return ["https://www.bestjobs.eu" + await selector.get_attribute("href") for selector in await page.locator("a[href].absolute.inset-0.z-1").all()]

    async def __scrape_companies(self,page:Page):
        return [await selector.text_content() for selector in await page.locator("div .mt-2.line-clamp-1.w-full.text-sm.text-ink-medium").all()]
    async def __scrap_page(self,page:Page, url:str) -> zip:
        try:
            await page.goto(url)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_load_state("networkidle") 
            await page.evaluate("window.scrollTo(0, 0)")
            hrefs = await self.__scrape_hrefs(page)
            companies = await self.__scrape_companies(page)
            await page.close()
            return zip(hrefs,companies)
        except Exception as e:
            return zip()
    async def scrape(self) -> AppResponse:
        if(not self.filter):
            raise "No Filter Set"
        self.__formatRoles()
        search_urls = self.__buildSearchUrls()
        print(search_urls)
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(timeout=50000)
                pages = [await browser.new_page() for _ in range(len(search_urls))]
                tasks = [self.__scrap_page(pages[i % len(pages)], url) for i, url in enumerate(search_urls)]
                res = await asyncio.gather(*tasks, return_exceptions=True)
                
                return AppResponse(results=[Result(company=company, job_url=job_url, meta_info="") for job_url,company in list(itertools.chain(*res))])
            except Exception:
                raise
            finally:
                await browser.close()
