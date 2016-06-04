# -*- coding: utf-8 -*
import argparse
# import os

import scrapy
from scrapy.crawler import CrawlerProcess


from twisted.internet                 import reactor
from scrapy.crawler                 import Crawler
from scrapy.utils.project             import get_project_settings

#--the spiders
from myairlease.spiders.fleetintel_list import FleetintelListSpider
from myairlease.spiders.Available_assets import AvailableAssetsSpider
#--the spiders


des='''\
Van Truong.
Web Crawler - http://myairlease.com/

This tool will scrap the information at
   1) http://www.myairlease.com/available/fleetintel_list
   2) http://www.myairlease.com/available/available_for_lease
   3) both links

And generates its corresponding CSV file
'''

def check_argument(value):

    try:
        value = int(value)

        if value is not 1 and value is not 2 and value is not 3:
            raise ValueError

    except ValueError:
        raise argparse.ArgumentTypeError("%s is invalid. Only (only 1, 2 or 3)" % value)
    
    return value 

def spider_closing(self, spider):
        log.msg("Spider closed: %s" % spider, level=log.INFO)
        self.running_crawlers.remove(spider)
        if not self.running_crawlers:
            reactor.stop()

parser = argparse.ArgumentParser(
    prog='myairlease_scraper.py',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=des)

parser.add_argument(
    'link', 
    metavar='Nº_link',
    nargs=1, 
    help='Define which link want to scrap (only 1, 2 or 3).',
    type=check_argument
    )

args = parser.parse_args()


if args.link[0] is 1:
    spider = FleetintelListSpider()
    process = CrawlerProcess( get_project_settings() )
    process.crawl(spider)
    process.start()
elif args.link[0] is 2:
    spider = AvailableAssetsSpider()
    process = CrawlerProcess( get_project_settings() )
    process.crawl(spider)

    process.start()
elif args.link[0] is 3:
    process = CrawlerProcess( get_project_settings() )
    process.crawl(FleetintelListSpider()) 
    process.crawl(AvailableAssetsSpider())
    process.start()

"""
# -------------------------------------------
spider = getStringsSpider()
process = CrawlerProcess( get_project_settings() )

process.crawl(spider, toTranslate=args.toTranslate, translated=args.translated, nameOfFile=args.file )
process.start()
# -------------------------------------------
"""