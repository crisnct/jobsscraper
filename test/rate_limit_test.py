import sys
import os

# Get the absolute path to the project root (parent of test folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Add project root to Python path
sys.path.insert(0, project_root)

from fastapi.testclient import TestClient

# Now we can import from src
from src.main import app

client = TestClient(app)

def test_rate_limit_scrape_jobs():
    """Test that /scrape/jobs is rate limited to 10 requests per minute"""
    
    filter_data = {
        "location": "timisoara",
        "roles": ["java developer"]
    }
    
    successful = 0
    rate_limited = 0
    
    print("Testing rate limit (10 requests per minute)...\n")
    
    for i in range(11):
        response = client.post("/scrape/jobs", json=filter_data)
        
        if i < 10:
            if response.status_code == 200:
                successful += 1
                print(f"Request {i+1}: ✓ Success (200)")
            else:
                print(f"Request {i+1}: ✗ Failed with status {response.status_code}")
        else:
            if response.status_code == 429:
                rate_limited += 1
                print(f"Request {i+1}: ✓ Rate Limited (429) as expected")
            else:
                print(f"Request {i+1}: ✗ Expected 429 but got {response.status_code}")
    
    print(f"\n--- Test Results ---")
    print(f"Successful requests: {successful}/10")
    print(f"Rate limited requests: {rate_limited}/1")
    
    assert successful == 10, f"Expected 10 successful requests, got {successful}"
    assert rate_limited == 1, f"Expected 1 rate limited request, got {rate_limited}"
    
    print("✓ Rate limit test PASSED!")

if __name__ == "__main__":
    test_rate_limit_scrape_jobs()