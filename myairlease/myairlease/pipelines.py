# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy             import signals
from scrapy.exporters   import CsvItemExporter

#python debugger
import pdb

class MyairleasePipeline(object):
    def process_item(self, item, spider):
        return item

class CSVExportPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):

        # print( str(spider) )
        # pdb.set_trace()

        file = open('%s' % spider.nameOfFile, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)

        #each spider has a different items
        if ( spider.name is 'fleetintel_list' ):
            self.exporter.fields_to_export = ['Company', 'Model', 'MSN', 'YoM', 'Reg', 'Comments']
        elif ( spider.name is 'Available_assets' ):
            self.exporter.fields_to_export = ['Category', 'Company', 'Contact_webPage', 'Contact_email', 'Contact_phone', 'Model', 'YoM', 'MSN', 'TFHs_TFCs', 'Engines', 'F_B_E', 'OL_A_S', 'LU', 'AD']
        
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item