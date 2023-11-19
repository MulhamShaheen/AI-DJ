import requests
import json
from urllib.parse import urlencode


with open('token.json', 'r') as fp:
    TOKEN = json.load(fp)["scrapeops_token"]

dic = {
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

    response = requests.get(get_scrapeops_url(url),)
    item = json.loads(response.content)['data']['items'][0]
    info = {
        v: item[list(dic.keys())[i]] for i, v in enumerate(dic.values())
    }
    return info