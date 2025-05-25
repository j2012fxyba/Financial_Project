# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import json


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('ddbook.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True
    
    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()
    
    
    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)
        if not self.first_item:
            line = ',\n' + line
        else:
            self.first_item = False
        self.file.write(line)
        return item


class DdbookPipeline(object):

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
    
        '''
        使用 utf8mb4 而非 utf8，以支持完整的 Unicode 字符（包括emoji）

        排序规则推荐 utf8mb4_unicode_ci
        '''
    def open_spider(self,spider):
        print('opend')
        try:
            self.conn=pymysql.connect(
                host=self.mysql_host,
                user=self.mysql_user,
                passwd=self.mysql_password,
                database=self.mysql_db,
                port=3306,
                charset='utf8mb4')
            
            #创建了字典类型的数据游标，并赋值给 self.cursor变量
            #self.conn()是数据库连接实例  self.conn.cursor()是创建新的游标
            '''
            数据库连接对象（self.conn）的 .cursor() 方法实际上是一个工厂方法（Factory Method），它的作用是：
            正确的实例化过程
        
            # DictCursor 类（未实例化）
            pymysql.cursors.DictCursor  

            # 通过连接的cursor()方法实例化
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            # 等价于：
            # 1. 连接对象self.conn准备游标需要的资源
            # 2. 创建DictCursor实例
            # 3. 将连接与游标绑定
            '''
            self.cursor=self.conn.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute('delete from ddbooks')
            #self.opened=True
            self.count=0       #计数器 初始化为0

            #使用有效执行sql 创建表 dbbooks. 基础表 price DECIMAL(10, 2),  注意金额字符类型
            self.cursor.execute("""

                CREATE TABLE IF NOT EXISTS ddbooks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255),
                    price VARCHAR(255),  
                    pinglun VARCHAR(255),
                    author VARCHAR(255),
                    publisher VARCHAR(50),
                    publisher_date DATETIME,
                    detail TEXT,
                    
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

          
        except Exception as er:
            print(er)

         
    def process_item(self, item, spider):
        #推送到 pipelines 里面，显示打印输出一下，然后保存到数据库里面 insert into 
        try:
            print(item['title'])
            print(item['price'])
            print(item['pinglun'])
            print(item['author'])
            print(item['publisher'])
            print(item['detail'])
            print(item['publisher_date'])

            #if self.opened:
            

            #insert into 表数据
            sql='INSERT INTO ddbooks (title, price,pinglun, author, publisher, detail, publisher_date)\
                VALUES (%s, %s, %s, %s, %s, %s,%s)'
            
            self.cursor.execute(sql,
            
            (
            item['title'],
            item['price'],
            item['pinglun'],
            item['author'],
            item['publisher'],
            item['detail'],
            item['publisher_date']
            ))
            self.count +=1    #每插入一条数据，计数器 自身+1
        #self.connect.commit()
        except Exception as er:
            print(er)
        return item


    def close_spider(self,spider):
        #if self.opened:
        self.conn.commit()
        self.conn.close()
        #self.opened=False
        print("close")
        print('总共爬取',self.count,'书籍')   #最后调取一共多少本书