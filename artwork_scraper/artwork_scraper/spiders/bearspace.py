import re

import scrapy
from scrapy.link import Link
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner, add_or_replace_parameter

from ..items import ArtworkItem
from ..utilities import clean_text_list, get_first


class BearSpaceParseSpider(scrapy.Spider):
    name = 'bearspace-parse'

    media_keywords = [
        'acrylic',
        'spray',
        'vinyl',
        'card',
        'board',
        'wood',
        'oil',
        'paint',
        'gold leaf',
        'goldleaf',
        'cement',
        'iron',
        'sculpted',
        'watercolour',
        'digital print',
        'resins',
        'pigments',
        'inkjet',
        'arches paper',
        'sculpture',
        'paper'
    ]
    media_keywords = sorted(media_keywords, key=len, reverse=True)
    media_re = re.compile(r'|'.join(media_keywords), re.I)

    def parse(self, response, *args, **kwargs):
        return ArtworkItem(
            url=response.url,
            title=self.extract_title(response),
            price_gbp=self.extract_price(response),
            media=self.extract_media(response),
            **self.extract_dimensions(response)
        )

    def extract_title(self, response):
        title_css = '[data-hook="product-title"]::text'
        return get_first(clean_text_list(response.css(title_css).extract()))

    def extract_dimensions(self, response):
        dimensions_css = '[data-hook="description"] ::text'
        dimensions_re = re.compile(r'([\d\.]+)\s*(?:cms?)?\s*x\s*([\d\.]+)\s*(?:cms?)?\s*', re.I)
        height_re = re.compile(r'height\s*([\d\.]+)\s*(?:cm)?|([\d\.]+)\s*h\s*(?:cm)?', re.I)
        width_re = re.compile(r'width\s*([\d\.]+)\s*(?:cm)?|([\d\.]+)\s*w\s*(?:cm)?|([\d\.]+)\s*(?:cm)?\s*diam', re.I)

        width, height = None, None
        dimensions = clean_text_list(response.css(dimensions_css).re(dimensions_re))
        if len(dimensions) == 2:
            width, height = clean_text_list(response.css(dimensions_css).re(dimensions_re))[:2]

        if not width:
            width = get_first(clean_text_list(response.css(dimensions_css).re(width_re)))

        if not height:
            height = get_first(clean_text_list(response.css(dimensions_css).re(height_re)))

        return {
            'height_cm': float(height) if height else height,
            'width_cm': float(width) if width else width
        }

    def extract_price(self, response):
        price_css = '[data-hook="formatted-primary-price"] ::text'
        price_re = '[\d,.]+'
        price = response.css(price_css).re_first(price_re).replace(',', '')
        return float(price)

    def extract_media(self, response):
        media_css = '[data-hook="description"] ::text'
        for media in response.css(media_css).extract():
            if re.search(self.media_re, media):
                return media
        return ''


class PaginationLE(LinkExtractor):
    ITEMS_PER_PAGE = 20

    def extract_links(self, response):
        total_items = int(response.css('#wix-warmup-data').re_first(r'"totalCount":(\d+)') or '0')
        total_pages = (total_items // self.ITEMS_PER_PAGE) + 1

        return [
            Link(add_or_replace_parameter(response.url, 'page', str(page_no)))
            for page_no in range(1, total_pages + 1)
        ]


class BearSpaceCrawlSpider(CrawlSpider):
    name = 'bearspace-crawl'
    parse_spider = BearSpaceParseSpider()

    allowed_domains = ['www.bearspace.co.uk']
    start_urls = ['https://www.bearspace.co.uk/purchase']

    item_css = '[data-hook="product-list-grid-item"]'

    rules = [
        Rule(
            LinkExtractor(
                restrict_css=item_css,
                process_value=url_query_cleaner
            ),
            callback='parse_item'
        ),
        Rule(
            PaginationLE(),
            follow=True
        ),
    ]

    def parse_item(self, response):
        return self.parse_spider.parse(response)
