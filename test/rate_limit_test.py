from fastapi.testclient import TestClient
from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=429,
    content={"detail": "Rate limit exceeded"}
))
app.add_middleware(SlowAPIMiddleware)

@app.post("/api/data")
@limiter.limit("5/minute")
async def create_data(request: Request, data: dict):
    return {"status": "success"}

# Test file: test_rate_limit.py
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_rate_limit():
    # Make 5 successful requests
    for i in range(5):
        response = client.post("/api/data", json={"test": "data"})
        assert response.status_code == 200
        print(f"Request {i+1}: {response.status_code}")
    
    # 6th request should be rate limited
    response = client.post("/api/data", json={"test": "data"})
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["detail"]
    print(f"Request 6: {response.status_code} - Rate limited as expected")

if __name__ == "__main__":
    test_rate_limit()