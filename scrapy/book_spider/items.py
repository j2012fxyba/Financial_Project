# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookScraperItem(scrapy.Item):
    # define the fields for your item here like:
    '''
    书名（name）价格（price）评价等级（review_rating，1-5星） 产品编码（UPC） 库存量（stock） 评价数量（review_num）
    '''
    # 对任何类型的 Item 进行适配
  
   
    title=scrapy.Field()
    price=scrapy.Field()
    rating=scrapy.Field()
    stock=scrapy.Field()
    upc=scrapy.Field()
    description=scrapy.Field()

