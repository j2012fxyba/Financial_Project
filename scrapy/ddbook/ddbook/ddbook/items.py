# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import scrapy.item


class DdbookItem_basicInfo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #需要先 继承 scrapy.Item 类 并定义 Field() 字段,适合 固定字段 的数据模型
    
    #创建 item book基本信息 数据项类  base.html
    title=scrapy.Field()
    author=scrapy.Field()
    #href=scrapy.Field() #详情跳转href  https://product.dangdang.com/29564789.html
    pinglun=scrapy.Field()
    publisher_date=scrapy.Field()
    publisher=scrapy.Field()
    detail=scrapy.Field()
    price=scrapy.Field()
    

    # book detail 来自 detail_html
class DbbookTtem_detailInfo(scrapy.Item):
    #产品特色
    feature=scrapy.Field()
    #编辑推荐
    abstract=scrapy.Field()
    #content 内容简介
    content=scrapy.Field()
    #作者简介
    authorIntroduction=scrapy.Field()
    #目录
    catalog=scrapy.Field()
    #媒体评论
    mediaFeedback=scrapy.Field()
    




