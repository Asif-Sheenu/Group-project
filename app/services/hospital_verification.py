import requests


def verify_url(url: str) -> bool:
    try:
        response = requests.get(
            url,
            timeout=5
        )

        return response.status_code < 400

    except Exception:
        return False