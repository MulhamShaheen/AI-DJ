import requests
import json
from urllib.parse import urlencode
import urllib3

urllib3.disable_warnings()

with open('token.json', 'r') as fp:
    data = json.load(fp)
    TOKEN = data["scrapeops_token"]
    zenrows_token = data["zenrows_token"]


props_dict = {
    "n": "title",
    "as": "artists",
    "an": "album",
    "p": "popularity",
    "c": "camelot",
    "b": "BPM",
    "k": "key",
    "ac": "acousticness",
    "h": "happiness",
    "i": "instrumentalness",
    "li": "liveness",
    "lo": "loudness",
    "da": "danceability",
    "e": "energy",
}

def get_scrapeops_url(url):
    payload = {'api_key': TOKEN, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


def get_zenrow_url(url):
    url = "https://httpbin.io/anything"
    proxy = f"http://{zenrows_token}:@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}
    return proxies


def search_tracks(term, page):
    """
    Search tracks using the Tunebat API.

    Args:
    term (str): The search term.
    page (int): The page number.

    Returns:
    dict: The response from the API.
    """
    url = f'https://api.tunebat.com/api/tracks/search?term={term}&page={page}'
    headers = {
        'authority': 'api.tunebat.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,ar;q=0.7',
        'cache-control': 'no-cache',
        'origin': 'https://tunebat.com',
        'pragma': 'no-cache',
        'referer': 'https://tunebat.com/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    # url_scrapeops = get_scrapeops_url(url)
    proxies = get_zenrow_url(url)
    response = requests.get(url, proxies=proxies, verify=False)
    item = json.loads(response.content)['data']['items'][0]
    info = {
        v: item[list(props_dict.keys())[i]] for i, v in enumerate(props_dict.values())
    }
    return info