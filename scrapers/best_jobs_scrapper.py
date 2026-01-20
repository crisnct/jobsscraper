import asyncio
import itertools
from typing import List, Self
from scrapers.scrapper import Scrapper
from models.filter import Filter
from playwright.async_api import async_playwright, Page, Browser, Locator
from models.response import AppResponse
from models.result import Result
from models.statistic import Statistic

class BestJobsScrapper(Scrapper):
    def __init__(self, filter):
        super().__init__(filter)
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
    async def __scrape_hrefs(self,page:Page):    
        return ["https://www.bestjobs.eu" + await selector.get_attribute("href") for selector in await page.locator("a[href] .absolute.inset-0.z-1").all()]

    async def __scrape_companies(self,page:Page) -> str:
        return [await selector.text_content() for selector in await page.locator("div .mt-2.line-clamp-1.w-full.text-sm.text-ink-medium").all()]
    async def __scrape_metadata(self, page:Page, jobUrl:str)->str:
        print(jobUrl)
        await page.goto(jobUrl)
        await page.wait_for_load_state("networkidle") 
        await page.screenshot(path="screenshot.png", full_page=True)
    
        return "work_type"
        
    async def __scrape_page(self,page:Page, url:str) -> zip:
        try:
            await asyncio.sleep(5) #Set a 5 sec delay before each scrapping
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
        async with async_playwright() as p:
            try:
                total_search_urls:int = len(search_urls)
                browser = await p.chromium.launch()
                pages = [await browser.new_page() for _ in range(total_search_urls)]
                tasks = [self.__scrape_page(pages[i % len(pages)], url) for i, url in enumerate(search_urls)]
                response = await asyncio.gather(*tasks, return_exceptions=True)
               
                results = [Result(company=company, job_url=job_url, meta_info="") for job_url,company in list(itertools.chain(*response))]
                return AppResponse(
                    results=results,
                    statistics=Statistic(
                        totalRequestsSent=total_search_urls,
                        jobsFound=len(results)
                    )
                )
            except Exception:
                raise
            finally:
                await browser.close()
