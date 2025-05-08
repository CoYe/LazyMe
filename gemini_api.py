import requests

# Your API key
api_key = "YOUR_API_KEY"

# Base URL for the API
base_url = "https://api.example.com"


def get_data(endpoint):
    url = base_url + endpoint
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")


def post_data(endpoint, data):
    url = base_url + endpoint
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")


endpoint = "/users"
data = {"name": "John Doe", "email": "john.doe@example.com"}

# Get data
response = get_data(endpoint)
print(response)

# Post data
response = post_data(endpoint, data)
print(response)


def call_gemini(url):
    """
    Args:
        url: URL to fetch with headers including API key
    Returns:
        string: fetched contents
    """

    gemini_headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'X-gemini-api-key': 'YOUR_API_KEY_HERE'}
    response = requests.get(url, headers=gemini_headers, timeout=60)
    response.raise_for_status()
    return response.content

if __name__ == "__main__":
    gemini_url = urlunparse(('https', 'gemini.googleusercontent.com',
                              'v1/datasets/central_tenure_geospatial:lookup',
                              None, None, None))
    gemini_request_payload = {'addresses': request_data}
    gemini_request = {'method': 'GET', 'url': gemini_url,
                       'data': json.dumps(gemini_request_payload)}
    response = requests.request(**gemini_request)
    response.raise_for_status()
