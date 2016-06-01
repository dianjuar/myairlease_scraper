# -*- coding: utf-8 -*-
import scrapy
from scrapy    			import Selector
from scrapy.http    	import Request

from myairlease.items 	import fleetIntelList_Item

#python debugger
import pdb
import re

class FleetintelListSpider(scrapy.Spider):
    name = "fleetintel_list"
    allowed_domains = ["myairlease.com"]
    start_urls = (
        'http://www.myairlease.com/available/fleetintel_list',
    )

    # Constructor
    def __init__ (self):
    	self.nameOfFile = 'FleetIntel_List.csv'
        

    def parse(self, response):
    	hxs = Selector(response)

    	#path to company list
    	companies_hxs = hxs.xpath('//td[@id="links3"]//p[@id="plist2"]//a')

    	# go through the companies
    	for com_hxs in companies_hxs:

    		#extract the name of the company
    		self.company 	= com_hxs.xpath('./text()')[0].extract()

    		item = fleetIntelList_Item()
    		item['Company'] = self.company

    		#extract the url of the company 
    		companyUrl 		= response.urljoin( com_hxs.xpath('./@href')[0].extract() )
    		# print ( '------------------------------>' + item['Company'] +' - '+ companyUrl )
    		# continue
    		
    		#extract the company
    		# yield Request( companyUrl, callback=self.parse_company)
    		yield Request( companyUrl, meta={'item':item}, callback=self.parse_company)


    # scrap the company list e.g http://www.myairlease.com/available/fleetintel_A320
    def parse_company(self, response):
    	hxs = Selector(response)    	
    	item = response.request.meta['item']

    	#get all the elements of the table except the 1st child 
    	#the 1st child is the head of the table with useless information
    	modelsRows = hxs.xpath('//div[@id="table"]/table//tr[position()>1]')

    	items = list()
 
    	for tr in modelsRows:
            #some comments have several childs and you get it all with 'descendant-or-self::*/text()'
    		tds = tr.xpath('./td/descendant-or-self::*/text()').extract()

    		item['Model']		= tds[0]
    		item['MSN']			= tds[1]
    		item['YoM']			= tds[2]
    		item['Reg']			= tds[3]
    		item['Comments']	= tds[4:]  #in case have multiple childs  		
    		
    		#export the item
    		yield item
