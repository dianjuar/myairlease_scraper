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
        self.categoryNames = list()

    def parse(self, response):
    	hxs = Selector(response)

    	#get the categories
        # self.get_niceCategoryNames( hxs )
        self.get_unguaranteedCategoryNames( hxs )

        # for x in self.categoryNames:
            # print ( x )

    def get_niceCategoryNames(self, hxs):
        categoryNames_hxs = hxs.xpath('//td[@id="links9"]//h4')

        for cat in categoryNames_hxs:
            catNames            = cat.xpath('.//descendant-or-self::*/text()').extract()
            self.categoryNames.append( ','.join(catNames) )

    def get_unguaranteedCategoryNames(self, hxs):
        print('----------*-*--------------------*-*-*-')
        base = '//td[@id="links9"]//p'
        # categoryNames_hxs = hxs.xpath( base + '/*[ not( self::br or self::b ) ] | ' +
        #                                base + '/*[ not( parent::br ) ]/text()' )
        # categoryNames_hxs = hxs.xpath( base + '/descendant-or-self::*[ not( self::b or self::br ) ]/text()')
        categoryNames_hxs = hxs.xpath( base + '/descendant-or-self::*[ not( self::b or self::br ) ]/text()').extract()
        
        # I don't need the first two elements
        del categoryNames_hxs[0:2]

        #remove white spaces
        self.eraseWhiteSpaces( categoryNames_hxs )

        for x in categoryNames_hxs:
            print ( x )
            print ( "-")

        print('----------*-*--------------------*-*-*-')
        pass

    def eraseWhiteSpaces(self, vec):
        

        for i, x in enumerate(vec):
            vec[i] = x.strip()

            if re.compile("\n").search( x ):
                del vec[i]    