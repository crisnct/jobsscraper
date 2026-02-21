from ast import pattern
import asyncio
import itertools
import re
from typing import Coroutine, List
from playwright.async_api import async_playwright, Page, Browser

from src.common.scrapper import Scrapper
from src.core.filters.best_jobs_filter import BestJobsFilter
from src.core.models.best_jobs_models.metadata import Metadata
from src.core.models.best_jobs_models.response import BestJobsResponse
from src.core.models.best_jobs_models.result import Result
from src.core.selectors.best_jobs_selectors import BestJobsSelectors





class BestJobsScrapper(Scrapper):
    def __init__(self, filter:BestJobsFilter):
        super().__init__(filter)
    def __formatRoles(self):
        if(self.filter.roles):
            self.filter.roles = [role.replace(" ", "-") for role in self.filter.roles]
    
    def __buildSearchUrls (self) -> List[str]:
        baseUrl = BestJobsSelectors.BASE_URL.value
        if(self.filter.location):
            baseUrl+= "/" +  BestJobsSelectors.LOCATION_SEARCH.value + self.filter.location
        return [baseUrl + role for role in self.filter.roles]
    async def __generate_page(self,browser:Browser) -> Page:
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(60000)
        return page

    async def __scrape_hrefs(self,page:Page) -> List[Metadata]:    
        return [BestJobsSelectors.BASE_URL.value + await selector.get_attribute("href") for selector in await page.locator(BestJobsSelectors.JOB_URL.value).all()]

    async def __scrape_companies(self,page:Page) -> str:
        return [await selector.text_content() for selector in await page.locator(BestJobsSelectors.COMPANY_NAME.value).all()]
    async def __includes_keywords(self, page:Page, keywords:List[str]) -> bool:
        visible_text = await page.locator("body").text_content()
        visible_text = visible_text.lower()
        visible_text = re.sub(r'ex:\s*[^\s]*\s*[^\s]*', '', visible_text, flags=re.IGNORECASE)
        for keyword in keywords:
            if not re.search(rf'\b{keyword}\b', visible_text):
                return False    
        return True
    
    async def __validate_url(self, page:Page, filters:BestJobsFilter, job_url:str) -> bool:
        await page.goto(job_url)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_load_state("networkidle") 
        await page.evaluate("window.scrollTo(0, 0)")
        work_type:List[str] = []
        if filters.remote and filters.remote == True:
            work_type.append("remote")
        if filters.hybrid and filters.hybrid == True:
            work_type.append("hybrid")
        if filters.onsite and filters.onsite == True:
            work_type.append("onsite")
        return await self.__includes_keywords(page=page, keywords=work_type + filters.keywords) and not await self.__includes_keywords(page=page, keywords=filters.exclude)
       
    async def __scrape_metadata(self, page:Page, jobUrl:str)-> Metadata:
        try:
            print(jobUrl)
            await page.goto(jobUrl)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_load_state("networkidle") 
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
           
            return metadata
        except Exception:
            raise
        finally:
            await page.close()
    async def __get_job_urls(self, page:Page, url:str) -> List[str]:
        try:
            await page.goto(url)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_load_state("networkidle") 
            await page.evaluate("window.scrollTo(0, 0)")
            return [BestJobsSelectors.BASE_URL.value + await selector.get_attribute("href") for selector in await page.locator(BestJobsSelectors.JOB_URL.value).all()]
        except Exception:
            raise
        finally:
            await page.close()        

            
    async def __delay_task(self,delay:float,task:Coroutine):
        await asyncio.sleep(delay)
        return await task
    
    async def scrape(self) -> BestJobsResponse:
        if(not self.filter):
            raise "No Filter Set"
        self.__formatRoles()
        search_urls = self.__buildSearchUrls()
        async with async_playwright() as p:
            try:
                results:List[Result] = []
                browser = await p.chromium.launch()
                res = await asyncio.gather(*[self.__delay_task(3,self.__get_job_urls(await self.__generate_page(browser), url=url)) 
                                                        for url in search_urls],
                                                        return_exceptions=True)
                
                job_urls = list(itertools.chain(*res))
                i:int=0
                while i < len(job_urls) and len(results) < self.filter.max_results:
                        # validate url
                        # if valid, scrape metadata
                        # if metadata matches filter, add to results
                        print(f"Validating {job_urls[i]}...")
                        crt_job_url = job_urls[i]
                        if await self.__validate_url(
                            page=await self.__generate_page(browser), 
                            filters=self.filter,
                            job_url=crt_job_url):
                                metadata= await self.__scrape_metadata(page=await self.__generate_page(browser), jobUrl=crt_job_url)
                                results.append(Result(job_url=crt_job_url, meta_info=metadata))
                                
                        i+=1
                           
                return BestJobsResponse(
                  results=results

                )
            except Exception:
                raise
            finally:
                await browser.close()
