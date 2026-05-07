# API Security Tester

A lightweight REST API security scanner for authorized testing. The Python implementation is the maintained path in this repository. The JavaScript implementation remains available as an experimental mirror.

## What It Checks

- SQL injection error disclosure and unstable server responses
- Reflected XSS payloads in API responses
- Weak/default login credentials
- Unauthenticated access to a configured protected endpoint
- Sensitive data exposure in unauthenticated responses
- Missing or weak rate limiting through bounded request bursts

## Safety Notice

Only run this tool against APIs you own or have explicit permission to test. The scanner sends test payloads and request bursts that may be disruptive on fragile systems.

## Install

```bash
git clone https://github.com/InfosecSamurai/api-security-tester.git
cd api-security-tester
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install pytest
```

## Basic Usage

```bash
python src/python/main.py --target https://example.com/api
```

The scanner writes reports to `reports/` by default:

- `api_scan_report_<timestamp>.json`
- `api_scan_report_<timestamp>.md`

The CLI exits with:

- `0` when no findings are detected
- `1` when findings are detected
- `2` when configuration or target validation fails

## Custom Config

```bash
python src/python/main.py \
  --target https://example.com/api \
  --config src/python/config/config.yaml \
  --output ./reports
```

Core config options:

```yaml
general:
  timeout_seconds: 10
  verify_ssl: true
  allow_redirects: true
  user_agent: "api-security-tester/1.0"
  headers: {}

tests:
  sql_injection: true
  xss: true
  broken_auth: true
  sensitive_data: true
  rate_limiting: true
```

Each module can be configured in `src/python/config/config.yaml`.

## Example Target-Specific Config

```yaml
general:
  headers:
    Authorization: "Bearer YOUR_TEST_TOKEN"

sql_injection:
  test_endpoint: "/search"
  parameter: "q"

xss:
  test_endpoint: "/search"
  parameter: "q"

broken_auth:
  auth_endpoints:
    login: "/auth/login"
    protected: "/admin"
  test_credentials:
    - username: "admin"
      password: "admin"

sensitive_data:
  endpoints:
    - "/users"
    - "/profile"

rate_limiting:
  test_endpoint: "/login"
  max_requests: 20
  threshold_seconds: 10
  delay_seconds: 0.05
```

## Run Tests

```bash
pytest src/python/tests/
```

## JavaScript Version

The JavaScript implementation is still present under `src/javascript`, but the Python scanner is currently the more complete maintained implementation.

```bash
cd src/javascript
npm install
node index.js --target https://example.com/api
npm test
```

## Recommended Next Improvements

- Add OpenAPI/Swagger parsing so endpoints and parameters are discovered automatically
- Add authentication profiles for API keys, bearer tokens, cookies, and basic auth
- Add CI workflow for Python tests
- Expand JavaScript parity or remove it to reduce maintenance overhead

## License

MIT
