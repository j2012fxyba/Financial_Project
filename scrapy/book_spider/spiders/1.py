import pymysql



#数据库连接测试
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='bigdata'
)

cursor = connection.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("MySQL 版本:", data)
connection.close()