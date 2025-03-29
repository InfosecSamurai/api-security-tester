import requests

def make_api_request(url, method="GET", headers=None, params=None, data=None):
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers or {},
            params=params or {},
            data=data or {}
        )
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text
        }
    except requests.RequestException as e:
        return {"error": str(e)}
