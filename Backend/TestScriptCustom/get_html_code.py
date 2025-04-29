import requests

def get_html_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
url = "https://example.com"
html_code = get_html_from_url(url)
if html_code:
    print(html_code)
