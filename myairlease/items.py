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

class AvailableAssets_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Category			= scrapy.Field()
    Company	 			= scrapy.Field()
    Contact_webPage		= scrapy.Field()
    Contact_email		= scrapy.Field()
    Contact_phone		= scrapy.Field()
    Model				= scrapy.Field()
    YoM					= scrapy.Field()
    MSN					= scrapy.Field()
    TFHs_TFCs			= scrapy.Field()
    Engines				= scrapy.Field()
    F_B_E				= scrapy.Field()
    OL_A_S				= scrapy.Field()
    LU					= scrapy.Field()
    AD					= scrapy.Field()
    ESN                 = scrapy.Field()
    L_E_S               = scrapy.Field()
    pass
