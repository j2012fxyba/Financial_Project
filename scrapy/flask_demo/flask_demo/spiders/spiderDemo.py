


import scrapy
import urllib.parse
from bs4 import BeautifulSoup


class flask_spider(scrapy.Spider):
    name='flask_spider'
    
    def start_requests(self):
        start_url='http://127.0.0.1:5000/in1'
        yield scrapy.Request(url=start_url,callback=self.parse)


    def process_spider(self):
        try:
            #处理网站爬取数据
            source=scrapy.Selector(text=self.data)
            h3=source.xpath('//h3/text()').extract()
            print(h3)

            link_list=source.xpath('//a/@href').extract()
            
            #打印列表的长度
            print(len(link_list))

            #for循环遍历输出
            for link in link_list:
                print(link)
                
                full_url=urllib.parse.urljoin(link,scrapy.Selector.response.url)
                yield scrapy.Request(url=full_url,callback=self.parse)
                
                #列表推导式中的 if link.get('href')是一个条件，它确保只有当<a>标签具有href属性时，才会将其URL添加到结果列表中。
                #hrefs=[link.get('href') for link in BeautifulSoup.find_all('a') if link.get('href')]
        except Exception as er:
            print(er)

    def parse(self,response):
        try:
            print(response.url)
            data=response.body.decode()
            print(data)
            
            self.process_spider()
        except Exception as er:
            print(er)


