from core.utils import make_api_request

def check(target_url, config):
    auth_endpoints = config.get("broken_auth", {}).get("auth_endpoints", {
        "login": "/login",
        "protected": "/admin"
    })
    
    results = []
    
    # Test for weak credentials
    weak_creds = [
        {"username": "admin", "password": "admin"},
        {"username": "user", "password": "123456"},
        {"username": "test", "password": "password"}
    ]
    
    for creds in weak_creds:
        response = make_api_request(
            f"{target_url}{auth_endpoints['login']}",
            method="POST",
            data=creds
        )
        
        if response.get("status_code") == 200 and "token" in response.get("content", ""):
            results.append({
                "test": "Weak credentials accepted",
                "vulnerable": True,
                "credentials": creds
            })
    
    # Test for session fixation
    # (Implementation would depend on specific API)
    
    return {
        "name": "Broken Authentication",
        "description": "Tests for authentication vulnerabilities",
        "results": results,
        "severity": "High"
    }
