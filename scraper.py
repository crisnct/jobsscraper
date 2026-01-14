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

import pprint
from typing import List
from playwright.sync_api import sync_playwright
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
    searchUrls: List[str] = []
    
    if(filter.location):
        baseUrl+= 'locuri-de-munca-in-'+filter.location
    for role in filter.roles:
        searchUrl = baseUrl + "/"+role
        searchUrls.append(searchUrl)
    return searchUrls

"""def scrapJobUrls(:List[str]) -> List[Result]:
    jobUrls = List[Result]
    for link in links:
        href = link.get_attribute("href")
        jobUrls.append(Result(job_url="https://www.bestjobs.eu"+href))
    return jobUrls"""

def getJobUrls(page:Page, searchUrls:List[str]) -> List[str]:
    for url in searchUrls:
        page.goto(url)
        links = page.locator("a[href].absolute.inset-0.z-1").all()
    return ["https://www.bestjobs.eu" + link.get_attribute("href") for link in links] 
    
def getCompanies(page:Page)->List[str]:
    #To be implemented
    return

def getMetadata(page:Page) -> List[dict]:
    #To be implemented
    return 


def scrape(filter:Filter) -> AppResponse:
   
    filter = formatRoles(filter)
    searchUrls = buildSearchUrls(filter)
    jobUrls:List[str] = []
    companies:List[str] = []
    metadatas:List[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        jobUrls = getJobUrls(page,searchUrls)
        companies = getCompanies(page)
        metadatas = getMetadata(page)
        browser.close()
    
    
    return AppResponse(
        results=[
            Result(company="", job_url=job_url, meta_info="") for job_url in jobUrls
        ],
        statistics=[]
    )

    