from vulnerabilities import sql_injection, xss, broken_auth, sensitive_data, rate_limiting
from core.utils import make_api_request
import time

class APIScanner:
    def __init__(self, target_url, config):
        self.target_url = target_url
        self.config = config
        self.vulnerability_checks = [
            sql_injection.check,
            xss.check,
            broken_auth.check,
            sensitive_data.check,
            rate_limiting.check
        ]
    
    def run_scan(self):
        results = {
            "target": self.target_url,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "vulnerabilities": []
        }
        
        for check in self.vulnerability_checks:
            try:
                result = check(self.target_url, self.config)
                results["vulnerabilities"].append(result)
            except Exception as e:
                print(f"Error running {check.__name__}: {str(e)}")
        
        return results
