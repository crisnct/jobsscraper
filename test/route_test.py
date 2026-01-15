from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_scrape_jobs():
    response = client.post(
        "/scrape/jobs/",
        json={
            "platform": "https://www.bestjobs.eu/",
            "keywords": ["java"],
            "location": "timisoara"
        }
    )
    assert response.status_code == 200
    assert "results" in response.json()
    assert "statistics" in response.json()