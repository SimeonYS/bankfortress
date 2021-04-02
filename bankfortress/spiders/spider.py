import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbankfortressItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BbankfortressSpider(scrapy.Spider):
	name = 'bankfortress'
	start_urls = ['https://www.bankfortress.com/fortress-bank/coronavirus-news-and-updates']

	def parse(self, response):
		yield response.follow(response.url, self.parse_post)

	def parse_post(self, response):
		articles = response.xpath('//div[@data-content-block="bodyCopy"]/h3')

		for index in range(len(articles)):
			item = ItemLoader(item=BbankfortressItem(), response=response)
			item.default_output_processor = TakeFirst()

			date = ''.join(response.xpath(f'//div[@data-content-block="bodyCopy"]/h3[{index+1}]//text()[not (ancestor::sup)]').getall())
			try:
				title = response.xpath(f'//div[@data-content-block="bodyCopy"]/div[@style="line-height: 200%;"][{index+1}]//span[@class="biggest"]/strong/text()').get().strip()
			except AttributeError:
				title = ""
			content = response.xpath(f'//div[@data-content-block="bodyCopy"]/div[@style="line-height: 200%;"][{index+1}]//span[@class="big"]//text()').getall()
			content = [p.strip() for p in content if p.strip()]
			content = re.sub(pattern, "", ' '.join(content))

			item.add_value('title', title)
			item.add_value('link', response.url)
			item.add_value('content', content)
			item.add_value('date', date)

			yield item.load_item()
