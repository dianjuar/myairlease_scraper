# -*- coding: utf-8 -*-
import scrapy

from scrapy    			import Selector
from scrapy.http    	import Request
from enum               import Enum   

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

        self.case = Enum('case','largeTable shortTable')


    def parse(self, response):
    	hxs = Selector(response)

    	#get the categories
        self.get_niceCategoryName( hxs=hxs, response=response )
        # self.get_unguaranteedCategoryNames( hxs )

        for i, cat in enumerate( self.categories ):
            
            meta    = dict()
            meta['Category']  = cat['name']

            if i == 0:
                yield Request( cat['link'], 
                               meta={'meta':meta, 'case':self.case.largeTable }, 
                               callback=self.parse_companyList)
            elif i == 1:
                #the second link doesn't have any company list
                meta['Company'] = ''
                
                #extract the company
                yield Request( cat['link'], 
                               meta={'meta':meta, 'case':self.case.largeTable },
                               callback=self.parse_company)
            elif i == 2:
                yield Request( cat['link'], 
                               meta={'meta':meta, 'case':self.case.shortTable}, 
                               callback=self.parse_companyList)

    def parse_companyList(self, response):
        hxs = Selector(response)        
        meta = response.request.meta['meta']
        case = response.request.meta['case']

        #path to company list
        companies_hxs = hxs.xpath('//td[@id="links3"]//p[@id="plist"]//a')

        # go through the companies
        for com_hxs in companies_hxs:

            #extract the name of the company
            company    = com_hxs.xpath('./text()')[0].extract()
            meta['Company'] = company
            
            #extract the url of the company 
            companyUrl      = response.urljoin( com_hxs.xpath('./@href')[0].extract() )
                        
            metaCopy = dict()
            metaCopy['Company'] = meta['Company']
            metaCopy['Category'] = meta['Category']

            yield Request( companyUrl, 
                           meta={'meta':metaCopy,'case':case}, 
                           callback=self.parse_company)

        pass

    def parse_company(self, response):
        hxs = Selector(response)        
        meta = response.request.meta['meta']    
        case = response.request.meta['case']

        #get all the elements of the table except the 1st child 
        #the 1st child is the head of the table with useless information
        modelsRows = hxs.xpath('//div[@id="table"]//table//tr[position()>1]')

        # some tables are completely empty
        if len(modelsRows) == 0:
            return

        for tr in modelsRows:

            tds = tr.xpath('./td')
            
            # some rows are empty or has a single empty td, very strange but just they are there
            if len(tds) == 0 or len(tds) == 1:
                continue

            #create the item
            item = AvailableAssets_Item()
            item['Category']    = meta['Category']
            item['Company']     = meta['Company']


            contacts = list()

            '''
            The 1st col has 2 link the most part of the time but 
            sometimes has only 1, I need to validate when it has 1 for prevent
            crashes
            '''
            numberOfContact = len(tds[0].xpath('./descendant::*[ self::a ]').extract())
            
            for x in range(0, numberOfContact):
                Contact_info = dict()
                basePath = tds[0].xpath('./a[position()>'+str(x)+']')
            
                Contact_info['name'] = basePath.xpath('./text()')[0].extract().strip()
                Contact_info['link'] = basePath.xpath('./@href')[0].extract().strip()

                contacts.append( Contact_info['name']+', '+Contact_info['link'] )                


            self.processContact(numberOfContact=numberOfContact, contacts=contacts, item=item, tds=tds, response=response)
            
            item['Model']           = tds[1].xpath('./text()')[0].extract()

            if case is self.case.shortTable:
                item['ESN']         = tds[2].xpath('./text()')[0].extract().strip()
                item['L_E_S']       = tds[3].xpath('./text()')[0].extract()  
                item['LU']          = tds[4].xpath('./text()')[0].extract() 
                item['AD']          = tds[5].xpath('./text()')[0].extract() 
            else:
                item['YoM']         = tds[2].xpath('./text()')[0].extract()
                item['MSN']             = tds[3].xpath('./descendant-or-self::text()').extract()
                self.eraseWhiteSpaces(item['MSN'])
            
                item['TFHs_TFCs']       = tds[4].xpath('./text()')[0].extract()             
                item['Engines']         = tds[5].xpath('./text()')[0].extract() 
                item['F_B_E']           = tds[6].xpath('./text()')[0].extract() 
                item['OL_A_S']          = tds[7].xpath('./text()')[0].extract() 
                item['LU']              = tds[8].xpath('./text()')[0].extract() 
                item['AD']              = tds[9].xpath('./text()')[0].extract() 
            yield item
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

    def processContact(self, numberOfContact, contacts, item, tds, response=None):
        
        if numberOfContact == 2:
            item['Contact_webPage'] = contacts[0]
            item['Contact_email']   = contacts[1]
            item['Contact_phone']   = tds[0].xpath('./text()')[1].extract()
        else:

            try:
                item['Contact_phone']   = tds[0].xpath('./text()')[0].extract()
            except Exception, e:
                pdb.set_trace()
                # raise

            if re.compile("mailto").search( contacts[0] ):
                item['Contact_email']   = contacts[0]
                item['Contact_phone']   = ''
            else:
                item['Contact_email']   = ''
                item['Contact_phone']   = contacts[0]
                



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
            x = x.strip()
            vec[i] = x

            if x == '':
                del vec[i]    