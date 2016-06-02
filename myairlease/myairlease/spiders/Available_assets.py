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
        self.categories = list()

    def parse(self, response):
    	hxs = Selector(response)

    	#get the categories
        self.get_niceCategoryName( hxs=hxs, response=response )
        # self.get_unguaranteedCategoryNames( hxs )

        for x in self.categories:
            print ( x['name'] )
            print ( x['link'] )
            print ( '---------' )


    def get_niceCategoryName(self, hxs, response):
        categories_hxs = hxs.xpath('//td[@id="links9"]//h4')

        for cat in categories_hxs:
            catNames     = cat.xpath('.//descendant-or-self::*/text()').extract()
            catLink     = cat.xpath('.//a/@href' ).extract()
            
            # pdb.set_trace()

            cat         = dict()
            cat['name'] = ','.join(catNames)
            cat['link'] = response.urljoin( catLink[0] )

            self.categories.append( cat )

    '''
    At http://www.myairlease.com/available/available_for_lease there is a no guarantee data base. 
    This function scrap that links
    '''
    def get_unguaranteedCategoryNames(self, hxs):
        print('----------*-*--------------------*-*-*-')
        base = '//td[@id="links9"]//p'
        # categories_hxs = hxs.xpath( base + '/*[ not( self::br or self::b ) ] | ' +
        #                                base + '/*[ not( parent::br ) ]/text()' )
        # categories_hxs = hxs.xpath( base + '/descendant-or-self::*[ not( self::b or self::br ) ]/text()')
        categories_hxs = hxs.xpath( base + '/descendant-or-self::*[ not( self::b or self::br ) ]/text()').extract()
        categoryNamesLINKS_hxs = hxs.xpath( base + '/a/@href').extract()
        # I don't need the first two elements
        del categories_hxs[0:2]

        #remove white spaces
        self.eraseWhiteSpaces( categories_hxs )

        for x in categories_hxs:
            print ( x )
            print ( "-")

        print('----------*-*--------------------*-*-*-')
        pass

    def eraseWhiteSpaces(self, vec):
        
        for i, x in enumerate(vec):
            vec[i] = x.strip()

            if re.compile("\n").search( x ):
                del vec[i]    