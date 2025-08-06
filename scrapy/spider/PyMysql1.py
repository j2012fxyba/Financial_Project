import pymysql
import re

import urllib

class Myspider:
    db=pymysql.connect(host='localhost',
                    user='root',
                    passwd='888888',
                    database='waihui')
    # 创建一个游标对象
    cursor=db.cursor()

    def openDB(self):
        cursor=Myspider.db.cursor()
        try:
            # 执行建库语句
            create_database_query = "CREATE DATABASE IF NOT EXISTS waihui DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            cursor.execute(create_database_query)
            
        # 提交事务
            cursor.commit()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")

    sql='''
        'create table rates (
        currency varchar(256) primary key,
        TSP float,
        CSP float, 
        TBP float,
        CBP float,
        Time varchar(256))" 

        '''

    cursor.execute(sql)
    cursor.commit()

        
    def closeDB(self):
    #关闭数据库
        self.con.commit()
        self.con.close()


    def insertDB(self,currency,TSP,CSP,TBP,CBP,Time):
 #记录插入数据库
        cursor=Myspider.db.cursor()
        try:
            sql="insert into rates (currency,TSP,CSP,TBP,CBP,Time) values (?,?,?,?,?,?)"
            cursor.execute(sql,[currency,TSP,CSP,TBP,CBP,Time])
        except Exception as err:
            print(err)



    def show(self):
 #显示函数
        cursor=Myspider.db.cursor()
        self.cursor.execute("select Currency,TSP,CSP,TBP,CBP,Time from rates")
        rows=self.cursor.fetchall()
        print("%-18s%-12s%-12s%-12s%-12s%-12s" %("Currency","TSP","CSP","TBP","CBP","Time"))
        for row in rows:
            print("%-18s%-12.2f%-12.2f%-12.2f%-12.2f%-12s" % (row[0],row[1],row[2],row[3],row[4],row[5]))
            cursor.close()


    def match(self,t, s):
        #匹配函数
        m = re.search(r"<" + t, s)
        if m:
            a= m.start()
            m = re.search(r">", s[a:])
            if m:
                b= a + m.end()
                return {"start": a, "end": b}
        return None


    def spider(self,url):
        #爬虫函数
        try:
                
                resp = urllib.request.urlopen(url)
                data = resp.read()
                html = data.decode()
                m = re.search(r'<div id="realRateInfo">', html)
                html = html[m.end():]
                m = re.search(r'</div>', html)
        # 取出<div id="realRateInfo">...</div>部分
                html = html[:m.start()]
                i=0
                while True:
                    p = self.match("tr", html)
                    q = self.match("/tr", html)
                    if p and q:
                        i=i+1
                    a = p["end"]
                    b = q["start"]
                    tds = html[a:b]
                    row=[]
                    count = 0
                    while True:
                        m = self.match("td", tds)
                        n = self.match("/td", tds)
                        if m and n:
                            u = m["end"]
                            v = n["start"]
                            count += 1
                            if count <= 8:
                                row.append(tds[u:v].strip())
                            tds = tds[n["end"]:]
                        else:
                    # 匹配不到<td>...</td>，退出内层循环
                            break
                    if i>=2 and len(row)==8:
                        Currency = row[0]
                        TSP = float(row[3])
                        CSP = float(row[4])
                        TBP = float(row[5])
                        CBP = float(row[6])
                        Time=row[7]
                        self.insertDB(Currency,TSP,CSP,TBP,CBP,Time)
                        html = html[q["end"]:]
                    else:
                        # 匹配不到<tr>...</tr>，退出外层循环
                
                     break
            
        except Exception as err:
            print(err)
    

    def process(self):
        #爬取过程
        self.openDB()
        self.spider("http://fx.cmbchina.com/hq/")
        self.show()
        self.closeDB()

#主程序
spider=Myspider()
spider.process()

'''
    m=re.search(r'<div id="realRateInfo">',html)
    html=html[m.end():]
    m=re.search(r'</div>',html)
    #取出<div id="realRateInfo">...</div>部分
    html=html[:m.start()]
    p = match("tr", html)
    q = match("/tr", html)
    a=p["end"]
    b=q["start"]
    tds=html[a:b]
    m = match("td", tds)
    n = match("/td", tds)
'''
