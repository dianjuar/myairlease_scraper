# -*- coding: utf-8 -*-
import scrapy

from scrapy    			import Selector
from scrapy.http    	import Request

from myairlease.items 	import AvailableAssets_Item

#python debugger
import pdb
import re

class AvailableAssetsSpider(scrapy.Spider):
    name = "Available_assets"
    allowed_domains = ["myairlease.com"]
    start_urls = (
        'http://www.myairlease.com/available/available_for_lease',
    )

    # Constructor
    def __init__ (self):
    	self.nameOfFile = 'Available_assets_list.csv'

    def parse(self, response):
    	hxs = Selector(response)

    	#get the categories
    	companies_hxs = hxs.xpath('//td[@id="links9"]//a/text()').extract()

    	for c in companies_hxs:
    		print( c )

        pass
