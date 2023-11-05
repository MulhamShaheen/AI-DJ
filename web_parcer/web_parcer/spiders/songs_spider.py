import logging
import time
from pathlib import Path
from scrapy.selector import Selector
import scrapy


class SongsSpider(scrapy.Spider):
    name = "songs"

    def start_requests(self):
        urls = [
            "file:///E:/AI%20Talent%20Hub/ML%20System%20Design/AI-DJ/experements/test.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

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

            next_page = song.css("::attr(href)").get()

            yield {
                "artist": artist,
                "title": title,
                "key": key,
                "BPM": bpm,
                "Camelot": camelot,
                "Popularity": popularity,
                "next_page": next_page,
            }
