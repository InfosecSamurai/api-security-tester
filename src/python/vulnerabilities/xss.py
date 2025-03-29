from core.utils import make_api_request

def check(target_url, config):
    test_payloads = config.get("xss", {}).get("test_payloads", [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "\"><script>alert('XSS')</script>"
    ])
    
    results = []
    for payload in test_payloads:
        response = make_api_request(
            f"{target_url}?input={payload}",
            method="GET"
        )
        
        if "error" in response:
            results.append({
                "payload": payload,
                "error": response["error"]
            })
        else:
            results.append({
                "payload": payload,
                "status_code": response["status_code"],
                "vulnerable": payload in response["content"]
            })
    
    return {
        "name": "Cross-Site Scripting (XSS)",
        "description": "Tests for XSS vulnerabilities",
        "results": results,
        "severity": "Medium"
    }
