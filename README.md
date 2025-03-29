# API Security Tester 🔒

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Node.js](https://img.shields.io/badge/node.js-16+-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-InfosecSamurai-FFDD00)](https://www.buymeacoffee.com/InfosecSamurai)

A comprehensive security testing tool for RESTful APIs that identifies common vulnerabilities including SQLi, XSS, broken authentication, and more. Available in both Python and JavaScript implementations.

## Features 🚀

- **SQL Injection Testing** - Detects SQLi vulnerabilities with multiple payloads
- **Cross-Site Scripting (XSS)** - Tests for reflected/stored XSS vulnerabilities
- **Broken Authentication** - Checks for weak credentials and session issues
- **Sensitive Data Exposure** - Identifies unprotected sensitive data
- **Rate Limiting** - Verifies API rate limiting protections
- **Dual Implementation** - Choose between Python or JavaScript version
- **Detailed Reporting** - JSON reports with vulnerability details

## Installation ⚙️

### Python Version
```bash
git clone https://github.com/InfosecSamurai/api-security-tester.git
cd api-security-tester
pip install -r requirements.txt
```

### JavaScript Version
```bash
git clone https://github.com/InfosecSamurai/api-security-tester.git
cd api-security-tester/src/javascript
npm install
```

## Usage 🛠️

### Basic Scan
```bash
# Python
python src/python/main.py --target http://example.com/api

# JavaScript
node src/javascript/index.js --target http://example.com/api
```

### Advanced Options
```bash
# Custom config file
python src/python/main.py --target http://example.com/api --config custom_config.yaml

# Specify output directory
node src/javascript/index.js --target http://example.com/api --output ./custom_reports
```

## Configuration ⚙️

Modify the config files to customize tests:
- Python: `src/python/config/config.yaml`
- JavaScript: `src/javascript/config/config.json`

Example configuration:
```yaml
# Python config.yaml
sql_injection:
  test_payloads:
    - "' OR 1=1--"
    - "admin'--"
```

## Sample Report 📊

Reports are generated in JSON format:
```json
{
  "target": "http://example.com/api",
  "timestamp": "2023-11-15T14:30:00Z",
  "vulnerabilities": [
    {
      "name": "SQL Injection",
      "severity": "High",
      "results": [
        {
          "payload": "' OR 1=1--",
          "status_code": 200,
          "vulnerable": true
        }
      ]
    }
  ]
}
```

## Supported Tests 🛡️

| Test Type               | Python | JavaScript | Severity |
|-------------------------|--------|------------|----------|
| SQL Injection           | ✅     | ✅         | High     |
| XSS                     | ✅     | ✅         | Medium   |
| Broken Authentication   | ✅     | ✅         | High     |
| Sensitive Data Exposure | ✅     | ✅         | High     |
| Rate Limiting           | ✅     | ✅         | Medium   |

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Running Tests 🧪

```bash
# Python tests
pytest src/python/tests/

# JavaScript tests (from src/javascript)
npm test
```

## Security Considerations ⚠️

- Only use on systems you have permission to test
- Some tests may cause disruption to services
- Review payloads before using in production environments

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Support the Project ☕

If you find this tool useful, consider supporting my work:

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://www.buymeacoffee.com/InfosecSamurai)

Your support helps me maintain and improve this tool!

---

**Created by Infosec Samurai** - Making APIs safer one test at a time 🔐
