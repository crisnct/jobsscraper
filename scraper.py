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

from playwright.sync_api import sync_playwright

def formatRoles(filters):
    filters["roles"] = [role.replace(" ", "-") for role in filters["roles"]]
    return filters
def setLocation(filters):
    return

def buildUrls (filters: map) :
    url = "https://www.bestjobs.eu/"
    results = []
    filters = formatRoles(filters)
    if(filters["location"]):
        url+= 'locuri-de-munca-in-'+filters["location"]
    for role in filters["roles"]:
        url+="/"+role
        results.append(url)
    return results
def getJobUrls(links):
    results = []
    for link in links:
        href = link.get_attribute("href")
        results.append(
           {
               "job_url":"https://www.bestjobs.eu"+href
           }
       )
    return results

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    filters = {
        "location": "timisoara",
        "roles": ["java developer"],
    }
    filters = formatRoles(filters)
    urls = buildUrls(filters)
    jobUrls = []
    for url in urls:
        page.goto(url)
        links = page.locator("a[href].absolute.inset-0.z-1").all()
        jobUrls.append(getJobUrls(links))
    response = {
        "results": jobUrls
    }

    import json
    print(json.dumps(response, indent=2, sort_keys=True))
    browser.close()

    