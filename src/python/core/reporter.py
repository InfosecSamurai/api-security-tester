import json
import os
from datetime import datetime

def generate_report(scan_results, output_dir="reports"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"api_scan_report_{timestamp}.json"
    report_path = os.path.join(output_dir, report_filename)
    
    with open(report_path, 'w') as report_file:
        json.dump(scan_results, report_file, indent=4)
    
    return report_path
