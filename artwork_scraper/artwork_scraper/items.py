# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from dataclasses import dataclass


@dataclass
class ArtworkItem:
    url: str
    title: str
    media: str
    price_gbp: float
    height_cm: float
    width_cm: float
