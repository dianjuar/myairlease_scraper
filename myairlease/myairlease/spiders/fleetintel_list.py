# -*- coding: utf-8 -*-
import scrapy
from scrapy                                    import Selector
from scrapy.http                            import Request

#python debugger
import pdb

class FleetintelListSpider(scrapy.Spider):
    name = "fleetintel_list"
    allowed_domains = ["myairlease.com"]
    start_urls = (
        'http://www.myairlease.com/available/fleetintel_list',
    )

    # Constructor
    def __init__ (self):
    	pass
        

    def parse(self, response):
    	hxs = Selector(response)

    	#path to company list
    	companies_hxs = hxs.xpath('//td[@id="links3"]//p[@id="plist2"]//a')

    	# go through the companies
    	for com_hxs in companies_hxs:

    		#extract the name of the company
    		self.company 	= com_hxs.xpath('./text()')[0].extract()

    		#extract the url of the company
    		companyUrl 		= response.urljoin( com_hxs.xpath('./@href')[0].extract() )
    		
    		self.parse_company( companyUrl )
        pass

    def parse_company(self, response):
    	hxs = Selector(response)

    	modelsRows = hxs.xpath()
    	pass