""" Request Body
{
  "platform" : "https://www.bestjobs.eu/",
  "keywords": ["java", "spring", "rest"],
  "location": "timisoara",
  "roles": ["java developer", "backend engineer", "team lead"],
  "remote": true,
  "hybrid": true,
  "onsite": true,
  "exclude": ["intern", "junior","was expired","is expired","no longer exists","This job was available"],
  "max_results": 30
}"""


""" Response Body
{
    "results": [
		{
			"company": "bosch",
			"job_url": "https://company.com/jobs/123",
			"meta_inf": "{{key1}}:{{value1}},{{key2}}:{{value2}},{{key3}}:{{value3}},..."
		},
		{
			"company": "bosch",
			"job_url": "https://company.com/jobs/123",
			"meta_inf": "{{key1}}:{{value1}},{{key2}}:{{value2}},{{key3}}:{{value3}},..."
		}
	]
}
	
"""

import asyncio
import itertools
import traceback
from typing import List
from xml.sax.xmlreader import Locator
from playwright.async_api import async_playwright
from models.filter import Filter
from models.response import AppResponse
from models.result import Result
from playwright.sync_api import Page

def formatRoles(filter:Filter) -> Filter:
    if(filter.roles):
        filter.roles = [role.replace(" ", "-") for role in filter.roles]
    return filter


def buildSearchUrls (filter: Filter) -> List[str]:
    baseUrl = "https://www.bestjobs.eu/"
    
    if(filter.location):
        baseUrl+= 'locuri-de-munca-in-'+filter.location
    return [baseUrl + "/"+role for role in filter.roles]



async def scrape_single_page(page:Page, url:str) -> List[str]:
    try:
        await page.goto(url, timeout=3000)
        links:List[Locator] = await page.locator("a[href].absolute.inset-0.z-1").all()
        return ["https://www.bestjobs.eu" + await link.get_attribute("href") for link in links]
    except Exception as e:
        return []
    
def getCompanies(page:Page)->List[str]:
    #To be implemented
    return

def getMetadata(page:Page) -> List[dict]:
    #To be implemented
    return 



async def scrape(filter: Filter) -> AppResponse:
    formatRoles(filter)
    search_urls = buildSearchUrls(filter)
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(timeout=50000)
            page = await browser.new_page()
            pages = [await browser.new_page() for _ in range(len(search_urls))]

            tasks = [ 
                scrape_single_page(pages[i % len(pages)], url)
                        for i, url in enumerate(search_urls)
            ] 
            res:List[List[str]] = await asyncio.gather(*tasks, return_exceptions=True)

            return AppResponse(
                results=[
                    Result(company="", job_url=job_url, meta_info="") for job_url in list(itertools.chain(*res))
                ],
            )
        except Exception:
            raise
        finally:
            await page.close()
            await browser.close()

    