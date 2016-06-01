# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class fleetIntelList_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Company	 	= scrapy.Field()
    Model		= scrapy.Field()
    MSN			= scrapy.Field()
    YoM			= scrapy.Field()
    Reg			= scrapy.Field()
    Comments	= scrapy.Field()
    pass
