import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import UnicreditroItem
from itemloaders.processors import TakeFirst


class UnicreditroSpider(scrapy.Spider):
	name = 'unicreditro'
	start_urls = ['https://www.unicredit.ro/ro/institutional/centru-media/comunicate-de-presa.html']

	def parse(self, response):
		next_page = response.xpath('(//div[@class="col-xs-24 large"])[2]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse_post)

	def parse_post(self, response):
		post_links = response.xpath('//div[@class="accordion"]')
		for post in post_links:
			title = post.xpath('./h3//text()').get()
			description = post.xpath('.//div[@class="sm_text section"]//text()[normalize-space()]').getall()
			description = [p.strip() for p in description]
			description = ' '.join(description).strip()
			try:
				date = re.findall(r"\d{1,2}\s[a-z]+\s\d{4}", description)[0]
			except:
				date = ''

			item = ItemLoader(item=UnicreditroItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
