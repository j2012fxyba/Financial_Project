import scrapy

from book_scraper.items import BookScraperItem

class book_spider(scrapy.Spider):

    '''
    name 是 Scrapy Spider 的唯一标识符，用于：

在运行爬虫时指定要运行的 Spider（scrapy crawl books）

在项目中区分不同的 Spider（当项目有多个爬虫时）

用于日志记录和统计信息中的标识,为什么不用 Python 类名（如 BookSpider）作为标识？因为Scrapy 的设计要求名称与代码结构解耦
    '''
    name='books'
    
    def start_requests(self):
        start_url='http://books.toscrape.com'
        yield scrapy.Request(url=start_url,callback=self.Myparse)
    
    def Myparse(self, response):
        # 提取所有书籍链接
       
        book_links = response.css('h3 a::attr(href)').getall()
        for link in book_links:
            yield response.follow(link, callback=self.parse_book)
        
        # 翻页处理
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.Myparse)
    
    def parse_book(self, response):
        item = BookScraperItem()
        
        # 提取书籍信息
        item['title'] = response.css('h1::text').get()
        item['price'] = response.css('.price_color::text').get()
        item['rating'] = response.css('p.star-rating::attr(class)').get().split()[-1]
        item['upc'] = response.css('tr:nth-child(1) td::text').get()
        
        # 库存信息
        availability = response.css('tr:nth-child(6) td::text').get().strip()
        item['stock'] = availability.split('(')[1].split()[0] if '(' in availability else '0'
        
        # 描述
        description = response.css('#product_description + p::text').get()
        item['description'] = description.strip() if description else ''
        
        yield item