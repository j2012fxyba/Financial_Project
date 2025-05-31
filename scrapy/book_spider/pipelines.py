# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

#编写通用 Pipeline（需要处理多种 Item 类型）

import pymysql
import json
from itemadapter import ItemAdapter
#from book_scraper.items import BookScraperItem



'''
json数组中，字符串之间使用,隔开的。 但是数组的第一个元素之前 不应该有逗号，
因此在将每条数据转换为json时，需要判断数据是否是json数组中的第一个元素
如果是，则直接写入，并将fist_item设置为False 表示后续的条目不是第一条。


json 的格式规范：如果第一个元素之前加了, 或者元素之间没有用,分隔， 那么解析json时会报错。
'''
class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('books.json', 'w', encoding='utf-8')
        #在文件中写入一个 [表示json 的开始
        self.file.write('[\n')
        #代表json的第一元素
        self.first_item = True
    
    def close_spider(self, spider):
        #在文件关闭时写入] 和\n 换行符  表示json 的结束
        self.file.write('\n]')
        self.file.close()
    
    def process_item(self, item, spider):
        #使用 json.dumps 方法将 json转换为字符串 ensure_ascii=False 允许输入非ascii码
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)
        #如果不是第一条，则在前面添加, 或者\n 
        if not self.first_item:
            line = ',\n' + line
        else:
            #如果是第一条，则设置为False
            self.first_item = False
            #将处理好的字符串写入 文件
        self.file.write(line)
        #返回 item。以便给其他管道或处理过程调用
        return item


class MySQLPipeline:
    #MySQLPipeline 类  #初始化方法 __init__,接收并存储 MySQL 数据库的连接参数
    def __init__(self, mysql_settings):
        self.mysql_settings = mysql_settings
        
    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_db):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
    
    #Scrapy 的标准类方法 from_crawler ，用于从 settings.py 中获取配置信息，并初始化 pipeline
    @classmethod
    def from_crawler(cls, crawler):
       
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )
    

#在爬虫启动时执行：
# 建立 MySQL 数据库连接\创建游标对象\创建 books 表（如果不存在），表结构包括：

# id: 自增主键\title: 书名\price: 价格（带2位小数）\rating: 评分\stock: 库存\upc: UPC编码\description: 描述文本

# created_at: 记录创建时间（自动设置为当前时间）


    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host=self.mysql_host,
            user=self.mysql_user,
            password=self.mysql_password,
            db=self.mysql_db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()
        
        # 创建表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                price DECIMAL(10, 2),
                rating VARCHAR(20),
                stock INT,
                upc VARCHAR(50),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    

    #在爬虫关闭时执行，关闭数据库连接
    def close_spider(self, spider):
        self.connection.close()
    

    '''
    处理每个爬取的 item：

执行 SQL 插入语句\ 对数据进行适当处理：

价格：移除英镑符号(£)并转换为浮点数

库存：转换为整数，默认为0

提交事务

返回 item 以便其他 pipeline 继续处理
    '''
    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO books (title, price, rating, stock, upc, description)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            item['title'],
            float(item['price'].replace('£', '')) if item['price'] else None,
            item['rating'],
            int(item['stock']) if item['stock'] else 0,
            item['upc'],
            item['description']
        ))
        self.connection.commit()
        return item
