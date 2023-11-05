from html.parser import HTMLParser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
from pathlib import Path
import scrapy


with open('test.html', 'r') as fp:
    content = fp.read()


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        filter = ('class','ant-typography ant-typography-ellipsis ant-typography-ellipsis-multiple-line aZDDf')
        if not( tag == 'div' and filter in attrs):
            return None

        print("Encountered a start tag:", tag, attrs)

    def handle_endtag(self, tag):
        if tag != 'div':
            return None
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


class QuotesSpider(scrapy.Spider):
    name = "somgs"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"songs-{page}.html"
        Path(filename).write_bytes(response.body)
