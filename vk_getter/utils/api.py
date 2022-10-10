import requests

from ..errors import AccessError, RequestError


def get_api(url, session=None):
    """Function to get api and deal with errors."""
    if session is None:
        req = requests.get(url)
    else:
        req = session.get(url)

    if req.status_code != 200:
        raise AccessError(f"Bad response: {req.status_code}")

    if req.json().get("error"):
        # hint to where error might be.
        error_url = url.replace('&', '&\n\t\t').replace('?', '?\n\t\t')
        raise RequestError(f"Something went wrong. Error message: {req.json()['error']['error_msg']}"
                           f"\n\nPlease check parameters in the URL below.\n"
                           f"URL: \t{error_url}")
    return req
