from core.utils import make_api_request

def check(target_url, config):
    endpoints_to_check = config.get("sensitive_data", {}).get("endpoints", [
        "/users",
        "/profile",
        "/account"
    ])
    
    results = []
    
    for endpoint in endpoints_to_check:
        response = make_api_request(
            f"{target_url}{endpoint}",
            method="GET"
        )
        
        if "error" in response:
            results.append({
                "endpoint": endpoint,
                "error": response["error"]
            })
        else:
            sensitive_fields = []
            content = response.get("content", "")
            
            if "password" in content:
                sensitive_fields.append("password")
            if "credit_card" in content:
                sensitive_fields.append("credit_card")
            if "ssn" in content:
                sensitive_fields.append("ssn")
            
            results.append({
                "endpoint": endpoint,
                "status_code": response["status_code"],
                "sensitive_data_exposed": len(sensitive_fields) > 0,
                "fields_found": sensitive_fields
            })
    
    return {
        "name": "Sensitive Data Exposure",
        "description": "Checks for exposed sensitive data",
        "results": results,
        "severity": "High"
    }
