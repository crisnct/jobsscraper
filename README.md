# jobsscraper
Search jobs for Jobs Hunter app
# to run the app:
python -m uvicorn src.main:app


# BestJobs Request Example 
{
    "scrapper": "bestjobs",
    "filter": {
        "remote": true,
        "onsite":true,
        "location": "timisoara",
        "roles": ["java developer"],
        "exclude":["php", "junior"]
    }
}