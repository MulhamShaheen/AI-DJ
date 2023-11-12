import logging
import time
from pathlib import Path
from urllib.parse import urlencode
from scrapy.selector import Selector
import scrapy

API_KEY = 'c3859fa1-1fc5-4f4b-97d8-58e9c2546e79' # DO NOT COMMIT

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class SongsSpider(scrapy.Spider):
    name = "songs"

    def start_requests(self):
        urls = [
            "file:///E:/AI%20Talent%20Hub/ML%20System%20Design/AI-DJ/experements/test.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            #
            # yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse, method='POST',
            #              body=json.dumps(my_data), headers={'Content-Type': 'application/json'})


    def parse(self, response):

        songs = response.css('div.d8O1K')
        for song in songs:
            info = song.css('p.lAjUd::text').getall()

            artist = str(song.css('div._2zAVA::text').get()).strip()
            title = str(song.css('div.aZDDf::text').get()).strip()
            key = str(info[0]).replace(" ", "").replace("\r\n", " ")
            bpm = str(info[1]).replace(" ", "").replace("\r\n", " ")
            camelot = str(info[2]).replace(" ", "").replace("\r\n", " ")
            popularity = str(info[3]).replace(" ", "").replace("\r\n", " ")

            next_page = 'https://tunebat.com'+ song.css("::attr(href)").get()

            data = {
                "artist": artist,
                "title": title,
                "key": key,
                "BPM": bpm,
                "Camelot": camelot,
                "Popularity": popularity,
            }

            yield response.follow(url=get_scrapeops_url(next_page), callback=self.parse_details, cb_kwargs={
                "song_data": data})

    def parse_details(self, response, song_data):
        infos = response.css('span.ant-progress-text')
        values = []
        for info in infos:
            a = info.css("::text").get()
            values.append(a)

        song_data["energy"] = int(values[1].strip())
        song_data["danceability"] = int(values[2].strip())
        song_data["happiness"] = int(values[3].strip())
        song_data["accousticness"] = int(values[4].strip())
        song_data["instrumentalness"] = int(values[5].strip())
        song_data["liveness"] = int(values[6].strip())
        song_data["speechiness"] = int(values[7].strip())
        song_data["loudness"] = int(values[7].strip())

        yield song_data
