import asyncio
import itertools
from typing import Coroutine, List
from playwright.async_api import async_playwright, Page, Browser
from src.models.metadata import Metadata
from src.models.response import AppResponse
from src.models.result import Result
from src.scrapers.scrapper import Scrapper
from src.screper_selectors.best_jobs_selectors import BestJobsSelectors

class BestJobsScrapper(Scrapper):
    def __init__(self, filter):
        super().__init__(filter)
    def __formatRoles(self):
        if(self.filter.roles):
            self.filter.roles = [role.replace(" ", "-") for role in self.filter.roles]
            return self
        return self
    
    def __buildSearchUrls (self) -> List[str]:
        baseUrl = BestJobsSelectors.BASE_URL.value
        if(self.filter.location):
            baseUrl+= BestJobsSelectors.LOCATION_SEARCH.value + self.filter.location
        return [baseUrl + "/"+role for role in self.filter.roles]
    async def __generate_page(self,browser:Browser) -> Page:
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(60000)
        return page

    async def __scrape_hrefs(self,page:Page) -> List[Metadata]:    
        return [BestJobsSelectors.BASE_URL.value + await selector.get_attribute("href") for selector in await page.locator(BestJobsSelectors.JOB_URL.value).all()]

    async def __scrape_companies(self,page:Page) -> str:
        return [await selector.text_content() for selector in await page.locator(BestJobsSelectors.COMPANY_NAME.value).all()]
    async def __scrape_metadata(self, page:Page, jobUrl:str)-> Metadata:
        try:
            print(jobUrl)
            await page.goto(jobUrl)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_load_state("domcontentloaded") 
            await page.evaluate("window.scrollTo(0, 0)")
            metadata = Metadata()
            payment_locator = page.locator(BestJobsSelectors.PAYMENT.value).nth(0)
            experience = ", ".join([await selector.text_content() for selector in await page.locator(BestJobsSelectors.EXPERIENCE.value).all()])
            metadata.experience = experience
            if await payment_locator.is_visible():
                metadata.payment = await payment_locator.text_content()
            work_type_locator = page.locator(BestJobsSelectors.WORK_TYPE.value).nth(1)
            if await work_type_locator.is_visible():
                metadata.work_type = await work_type_locator.text_content()
            print(metadata)
            return metadata
        except Exception:
            raise
        finally:
            await page.close()
        
    async def __scrape_page(self,page:Page, url:str) -> zip:
        try:
            await page.goto(url)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_load_state("domcontentloaded") 
            await page.evaluate("window.scrollTo(0, 0)")
            hrefs = await self.__scrape_hrefs(page)
            companies = await self.__scrape_companies(page)
           
            return zip(hrefs,companies)
        except Exception:
            raise
        finally:
            await page.close()
            
    async def __delay_task(self,delay:float,task:Coroutine):
        await asyncio.sleep(delay)
        return await task

    async def scrape(self) -> AppResponse:
        if(not self.filter):
            raise "No Filter Set"
        self.__formatRoles()
        search_urls = self.__buildSearchUrls()
        async with async_playwright() as p:
            try:
                
                browser = await p.chromium.launch()
                response = await asyncio.gather(*[self.__delay_task(3,self.__scrape_page(page=await self.__generate_page(browser), url=url)) 
                                                  for url 
                                                  in search_urls], 
                                                  return_exceptions=True)
                datas = list(itertools.chain(*response))
                metadatas:List[Metadata] = await asyncio.gather(*[self.__delay_task(3, self.__scrape_metadata(await self.__generate_page(browser), jobUrl=job_url)) 
                                                  for (job_url,_) 
                                                  in datas], 
                                                  return_exceptions=True)
               
                results = [Result(company=company, job_url=job_url, meta_info=metadata) 
                           for (job_url,company), metadata 
                           in zip(datas, metadatas)]
                
                return AppResponse(
                  results=results
                )
            except Exception:
                raise
            finally:
                await browser.close()
