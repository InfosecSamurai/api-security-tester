import time
from core.utils import make_api_request

def check(target_url, config):
    endpoint = config.get("rate_limiting", {}).get("test_endpoint", "/api/data")
    max_requests = config.get("rate_limiting", {}).get("max_requests", 100)
    threshold = config.get("rate_limiting", {}).get("threshold_seconds", 10)
    
    results = []
    start_time = time.time()
    request_count = 0
    
    while time.time() - start_time < threshold and request_count < max_requests:
        response = make_api_request(
            f"{target_url}{endpoint}",
            method="GET"
        )
        request_count += 1
        
        if response.get("status_code") == 429:
            break
    
    results.append({
        "requests_sent": request_count,
        "time_elapsed": time.time() - start_time,
        "rate_limit_hit": response.get("status_code") == 429,
        "requests_per_second": request_count / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
    })
    
    return {
        "name": "Rate Limiting",
        "description": "Tests for rate limiting protection",
        "results": results,
        "severity": "Medium"
    }
