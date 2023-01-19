import re
from datetime import datetime

import pandas as pd
from lxml import html

from utilities import clean_text_list, get_first

html_page_link = 'candidateEvalData/webpage.html'
html_tree = html.parse(html_page_link)

# parse artist name
artist_name_x = '//*[@id="main_center_0_lblLotPrimaryTitle"]//text()'
artist_name_re = '^[\w\s]+'

raw_artist_name = get_first(clean_text_list(html_tree.xpath(artist_name_x)))
artist_name = get_first(clean_text_list(re.findall(artist_name_re, raw_artist_name)))

# parse painting name
painting_name_x = '//*[@id="main_center_0_lblLotSecondaryTitle"]//text()'
painting_name = get_first(clean_text_list(html_tree.xpath(painting_name_x)))

# parse price GBP
gbp_price_x = '//*[@id="main_center_0_lblPriceRealizedPrimary"]//text()'
gbp_price_re = '[\d,.]+'

raw_gbp_price = ' '.join(clean_text_list(html_tree.xpath(gbp_price_x)))
gbp_price = get_first(re.findall(gbp_price_re, raw_gbp_price)) or ''
gbp_price = gbp_price.replace(',', ' ')

# parse price US
usd_price_x = '//*[@id="main_center_0_lblPriceRealizedSecondary"]//text()'
usd_price_re = '[\d,.]+'

raw_usd_price = ' '.join(clean_text_list(html_tree.xpath(usd_price_x)))
usd_price = get_first(re.findall(usd_price_re, raw_usd_price)) or ''
usd_price = usd_price.replace(',', ' ')

# parse price GBP est
gbp_price_est_x = '//*[@id="main_center_0_lblPriceEstimatedPrimary"]//text()'
gbp_price_est_re = '[\d,.]+'

raw_gbp_price_est = ' '.join(clean_text_list(html_tree.xpath(gbp_price_est_x)))
gbp_price_est = ' , '.join([price.replace(',', ' ') for price in re.findall(gbp_price_est_re, raw_gbp_price_est)])

# parse price US est
usd_price_est_x = '//*[@id="main_center_0_lblPriceEstimatedSecondary"]//text()'
usd_price_est_re = '[\d,.]+'

raw_usd_price_est = ' '.join(clean_text_list(html_tree.xpath(usd_price_est_x)))
usd_price_est = ' , '.join([price.replace(',', ' ') for price in re.findall(usd_price_est_re, raw_usd_price_est)])

# image link
image_link_x = '//*[@id="imgLotImage"]/@src'
image_link = get_first(clean_text_list(html_tree.xpath(image_link_x)))

# sale date
sale_date_x = '//*[@id="main_center_0_lblSaleDate"]//text()'
raw_sale_date = get_first(clean_text_list(html_tree.xpath(sale_date_x)))
sale_date = datetime.strptime(raw_sale_date, '%d %B %Y,').strftime('%Y-%m-%d')

# Paintings Dataframe
paintings_df = pd.DataFrame([
    {
        'artist_name': artist_name,
        'painting_name': painting_name,
        'gbp_price': gbp_price,
        'usd_price': usd_price,
        'gbp_price_est': gbp_price_est,
        'usd_price_est': usd_price_est,
        'image_link': image_link,
        'sale_date': sale_date,
    }
])
