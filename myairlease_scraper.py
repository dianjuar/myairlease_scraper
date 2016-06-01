# -*- coding: utf-8 -*
import argparse
# import os

import scrapy
from scrapy.crawler import CrawlerProcess

from twisted.internet 				import reactor
from scrapy.crawler 				import Crawler
from scrapy.utils.project 			import get_project_settings