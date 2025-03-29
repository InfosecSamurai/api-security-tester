from core.utils import make_api_request

def check(target_url, config):
    test_payloads = config.get("sql_injection", {}).get("test_payloads", [
        "' OR '1'='1",
        "' OR 1=1--",
        "admin'--"
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
                "vulnerable": "sql" in response["content"].lower()
            })
    
    return {
        "name": "SQL Injection",
        "description": "Tests for SQL injection vulnerabilities",
        "results": results,
        "severity": "High"
    }
