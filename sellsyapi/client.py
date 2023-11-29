from json import dumps
from time import time, sleep
from requests import post, request, RequestException
from functools import wraps

class SellsyAPI:
    """A class to interact with the Sellsy API, handling authentication and requests."""

    def __init__(self, client_id: str, client_secret: str):
        """
        Initializes the API client with client credentials.

        Args:
            client_id (str): The client ID for Sellsy API authentication.
            client_secret (str): The client secret for Sellsy API authentication.
        """
        self.auth_url = "https://login.sellsy.com/oauth2/access-tokens"
        self.api_base_url = "https://api.sellsy.com/v2/"
        self.post_content_type = {
            "batch": "text/plain",
            "opportunities/search": "application/json",
            "individuals/search": "application/json",
            "invoices/search": "application/json",
            "credit-notes/search": "application/json",
            "estimates/search": "application/json",
            "comments/search": "application/json",
            "companies/search": "application/json",
            "contacts/search": "application/json"
        }
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token, self.token_expiry = self._request_new_token()

    def _get_access_token(self) -> str:
        """
        Retrieves the current access token, requesting a new one if it's expired.
        """
        if time() >= self.token_expiry:
            self.access_token, self.token_expiry = self._request_new_token()
        return self.access_token

    def _request_new_token(self) -> (str, float):
        """
        Requests a new access token from the Sellsy API.

        Returns:
            tuple: A tuple containing the access token and its expiry time.

        Raises:
            RuntimeError: If the request for a new token fails.
        """
        try:
            response = post(self.auth_url, data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            })
            response.raise_for_status()
            res = response.json()
            expiry_time = time() + res["expires_in"]
            return res['access_token'], expiry_time
        except RequestException as e:
            raise RuntimeError(f"Failed to obtain access token: {e}")

    def _check_access_token(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self._get_access_token()  # Refresh the token if needed
            return func(self, *args, **kwargs)
        return wrapper

    def _request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> dict:
        """
        Sends a GET or POST request to the Sellsy API.
        Args:
            method (str): The HTTP method to use ('get' or 'post').
            endpoint (str): The API endpoint to call.
            params (dict, optional): URL parameters for the request.
            data (dict, optional): Data to be sent in the request body.
        
        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.HTTPError: For HTTP-related errors.
            ValueError: If the response body does not contain valid JSON.
        """
        MAX_RETRIES = 5
        params = params or {}
        params.setdefault('limit', 100)
        data = data or {}
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.api_base_url}{endpoint}"
        content_type = self.post_content_type.get(endpoint, "application/json")
        headers["Content-Type"] = content_type

        data = dumps(data) if content_type == "application/json" else data

        retries = 0
        while retries < MAX_RETRIES
        for attempt in range(MAX_RETRIES):
            try:
                response = request(method, url, headers=headers, params=params, data=data)
                response.raise_for_status()
                return response.json()
            except RequestException as err:
                retries += 1
                time.sleep(2 ** retries)  # Exponential backoff
                if retries == max_retries:
                    raise Exception(f"All retries failed for {endpoint}: {e}")

    @_check_access_token
    def get(self, endpoint: str, params: dict = {}) -> dict:
        """
        Sends a GET request to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): URL parameters for the GET request.

        Returns:
            dict: The JSON response from the API.
        """
        response = self._request("get", endpoint, params=params)
        data = response.get('data', [])
        pagination_info = response.get('pagination', {})

        return self._request(
            method="get",
            endpoint=endpoint,
            params=params
            )

    @_check_access_token
    def post(self, endpoint: str, params: dict = {}, data: dict = {}) -> dict:
        """
        Sends a POST request to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): URL parameters for the POST request.
            data (dict, optional): Data to be sent in the request body.

        Returns:
            dict: The JSON response from the API.
        """
        return self._request(
            method="post",
            endpoint=endpoint,
            params=params,
            data=data
            )
