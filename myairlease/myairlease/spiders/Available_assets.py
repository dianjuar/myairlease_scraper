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

        for cat in self.categories:
            item = AvailableAssets_Item()
            item['Category'] = cat['name']
            yield Request( cat['link'], meta={'item':item}, callback=self.parse_companyList)


    def parse_companyList(self, response):
        hxs = Selector(response)        
        item = response.request.meta['item']

        #path to company list
        companies_hxs = hxs.xpath('//td[@id="links3"]//p[@id="plist"]//a')

        # go through the companies
        for com_hxs in companies_hxs:

            #extract the name of the company
            company    = com_hxs.xpath('./text()')[0].extract()

            item['Company'] = company

            #extract the url of the company 
            companyUrl      = response.urljoin( com_hxs.xpath('./@href')[0].extract() )
                        
            #extract the company
            yield Request( companyUrl, meta={'item':item}, callback=self.parse_company)

        pass

    def parse_company(self, response):
        hxs = Selector(response)        
        item = response.request.meta['item']

        #get all the elements of the table except the 1st child 
        #the 1st child is the head of the table with useless information
        modelsRows = hxs.xpath('//div[@id="table"]//table//tr[position()>1]')

        items = list()

        for tr in modelsRows:

            tds = tr.xpath('./td')
            if len(tds) == 0:
                continue
            
            contacts = list()

            for x in xrange(0,2):
                try:
                    Contact_info = dict()
                    basePath = tds[0].xpath('./a[position()>'+str(x)+']')
                
                    Contact_info['name'] = basePath.xpath('./text()')[0].extract().strip()
                    Contact_info['link'] = basePath.xpath('./@href')[0].extract().strip()

                    contacts.append( Contact_info['name']+', '+Contact_info['link'] )                
                except IndexError:
                    # pdb.set_trace()
                    pass

            item['Contact_webPage'] = contacts[0]
            item['Contact_email']   = contacts[1]
            item['Contact_phone']   = tds[0].xpath('./text()')[1].extract()
            
            item['Model']           = tds[1].xpath('./text()')[0].extract()
            item['YoM']             = tds[2].xpath('./text()')[0].extract()
            
            try:
                item['MSN']             = tds[3].xpath('./descendant-or-self::*/text()').extract() 
            except IndexError:
                pdb.set_trace()
                
            
            # item['TFHs_TFCs']       = tds[4].xpath('./text()')[0].extract() 
            # print ( item['TFHs_TFCs'] ) 
            # item['Engines']         = tds[5].xpath('./text()')[0].extract() 
            # item['F_B_E']           = tds[6].xpath('./text()')[0].extract() 
            # item['OL_A_S']          = tds[7].xpath('./text()')[0].extract() 
            # item['LU']              = tds[8].xpath('./text()')[0].extract() 
            # item['AD']              = tds[9].xpath('./text()')[0].extract() 
            # pdb.set_trace()
            
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